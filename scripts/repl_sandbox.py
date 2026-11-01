#!/usr/bin/env python3
"""
Antigravity Agent OS - In-Memory Micro-Sandbox & Hypothesis REPL Engine.
Provides ultra-fast (<15ms), zero-disk-pollution ephemeral execution
for Python snippets, SQL schema experiments, regex testing, and data transforms.
"""

import ast
import builtins
import collections
import datetime
import hashlib
import io
import itertools
import json
import math
import os
import re
import sqlite3
import sys
import threading
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_AST_NAMES = {
    "__import__",
    "__builtins__",
    "__loader__",
    "__spec__",
    "open",
    "eval",
    "exec",
    "compile",
    "getattr",
    "setattr",
    "delattr",
    "globals",
    "locals",
    "vars",
    "dir",
    "input",
    "breakpoint",
    "help",
    "memoryview",
    "Path",
}

SAFE_BUILTIN_NAMES = (
    "abs", "all", "any", "ascii", "bin", "bool", "bytes", "bytearray", "callable",
    "chr", "complex", "dict", "divmod", "enumerate", "filter", "float", "format",
    "frozenset", "hash", "hex", "int", "isinstance", "issubclass", "iter", "len",
    "list", "map", "max", "min", "next", "oct", "ord", "pow", "print", "range",
    "repr", "reversed", "round", "set", "slice", "sorted", "str", "sum", "tuple",
    "type", "zip",
    "ArithmeticError", "AssertionError", "AttributeError", "EOFError", "Exception",
    "IndexError", "KeyError", "LookupError", "NameError", "NotImplementedError",
    "OverflowError", "RuntimeError", "StopIteration", "SyntaxError", "TimeoutError",
    "TypeError", "ValueError", "ZeroDivisionError",
)
SAFE_BUILTINS: Dict[str, Any] = {
    name: getattr(builtins, name) for name in SAFE_BUILTIN_NAMES if hasattr(builtins, name)
}


def _validate_safe_ast(code: str) -> None:
    """Rejects imports, private/dunder attribute traversal, dangerous builtin names, and single-expression CPU/RAM bombs."""
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise PermissionError("SecurityViolation: 'import' statements are forbidden in the sandbox.")
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            raise PermissionError("SecurityViolation: 'global'/'nonlocal' statements are forbidden in the sandbox.")
        if isinstance(node, ast.Attribute) and node.attr.startswith("_"):
            raise PermissionError(
                f"SecurityViolation: Access to private/dunder attribute '{node.attr}' is forbidden."
            )
        if isinstance(node, ast.Name) and (
            node.id in FORBIDDEN_AST_NAMES or node.id.startswith("__")
        ):
            raise PermissionError(
                f"SecurityViolation: Identifier '{node.id}' is forbidden in the sandbox."
            )
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
            if isinstance(node.right, ast.BinOp) and isinstance(node.right.op, ast.Pow):
                raise PermissionError("SecurityViolation: Chained exponentiation bombs are forbidden in the sandbox.")
            if isinstance(node.right, ast.Constant) and isinstance(node.right.value, (int, float)) and node.right.value > 10000:
                raise PermissionError(
                    f"SecurityViolation: Exponent {node.right.value} exceeds sandbox safety cap (10,000)."
                )
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("range", "pow"):
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, (int, float)) and abs(arg.value) > 10_000_000:
                    raise PermissionError(
                        f"SecurityViolation: '{node.func.id}' argument {arg.value} exceeds sandbox memory cap (10,000,000)."
                    )


def run_python(code: str, timeout_seconds: float = 3.0) -> Dict[str, Any]:
    """
    Executes a Python snippet in an isolated in-memory environment,
    capturing stdout, stderr, and the return/evaluated value with AST and timeout guards.
    """
    start_time = time.perf_counter()
    captured_stdout = io.StringIO()
    captured_stderr = io.StringIO()

    sandbox_globals: Dict[str, Any] = {
        "__builtins__": dict(SAFE_BUILTINS),
        "__name__": "__sandbox__",
        "json": json,
        "re": re,
        "math": math,
        "collections": collections,
        "itertools": itertools,
        "datetime": datetime,
        "hashlib": hashlib,
    }
    sandbox_locals: Dict[str, Any] = {}

    status = "SUCCESS"
    error_msg: Optional[str] = None
    eval_result: Any = None

    try:
        _validate_safe_ast(code)
        try:
            compiled = compile(code, "<sandbox>", "eval")
            mode = "eval"
        except SyntaxError:
            compiled = compile(code, "<sandbox>", "exec")
            mode = "exec"

        deadline = time.perf_counter() + max(0.05, float(timeout_seconds))
        worker_outcome: Dict[str, Any] = {}

        def _trace_timeout(frame: Any, event: str, arg: Any) -> Any:
            frame.f_trace_opcodes = True
            if time.perf_counter() > deadline:
                raise TimeoutError(f"Execution exceeded {timeout_seconds}s timeout")
            return _trace_timeout

        def _worker() -> None:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            try:
                sys.stdout = captured_stdout
                sys.stderr = captured_stderr
                sys.settrace(_trace_timeout)
                if mode == "eval":
                    worker_outcome["result"] = eval(compiled, sandbox_globals, sandbox_locals)
                else:
                    exec(compiled, sandbox_globals, sandbox_locals)
                    if "result" in sandbox_locals:
                        worker_outcome["result"] = sandbox_locals["result"]
                    elif "output" in sandbox_locals:
                        worker_outcome["result"] = sandbox_locals["output"]
            except BaseException as exc:
                worker_outcome["error"] = exc
                worker_outcome["tb"] = traceback.format_exc()
            finally:
                sys.settrace(None)
                sys.stdout = old_stdout
                sys.stderr = old_stderr

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
        t.join(timeout=max(0.05, float(timeout_seconds)))

        if t.is_alive():
            status = "ERROR"
            error_msg = f"TimeoutError: Execution exceeded {timeout_seconds}s timeout"
        elif "error" in worker_outcome:
            exc = worker_outcome["error"]
            status = "ERROR"
            error_msg = f"{type(exc).__name__}: {str(exc)}"
            captured_stderr.write(worker_outcome.get("tb", ""))
        else:
            eval_result = worker_outcome.get("result")

    except Exception as e:
        status = "ERROR"
        error_msg = f"{type(e).__name__}: {str(e)}"
        captured_stderr.write(traceback.format_exc())

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    return {
        "status": status,
        "result": eval_result,
        "stdout": captured_stdout.getvalue(),
        "stderr": captured_stderr.getvalue(),
        "error": error_msg,
        "elapsed_ms": round(elapsed_ms, 2)
    }


def _sqlite_authorizer(
    action: int,
    arg1: Optional[str],
    arg2: Optional[str],
    dbname: Optional[str],
    source: Optional[str],
) -> int:
    """Blocks ATTACH/DETACH DATABASE and load_extension in the in-memory SQLite sandbox."""
    if action in (sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH):
        return sqlite3.SQLITE_DENY
    if action == sqlite3.SQLITE_FUNCTION and arg2 and arg2.lower() == "load_extension":
        return sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_OK


def run_sql(statements: str) -> Dict[str, Any]:
    """
    Executes SQL statements in an ephemeral in-memory SQLite database (:memory:)
    and returns query results with column metadata and ascii table.
    """
    start_time = time.perf_counter()
    status = "SUCCESS"
    error_msg = None
    results = []

    try:
        conn = sqlite3.connect(":memory:")
        conn.set_authorizer(_sqlite_authorizer)
        cursor = conn.cursor()

        # Split multiple queries by semicolon safely
        query_list = [q.strip() for q in statements.split(";") if q.strip()]

        for query in query_list:
            cursor.execute(query)
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                results.append({
                    "query": query,
                    "columns": columns,
                    "rows": rows,
                    "row_count": len(rows)
                })
            else:
                conn.commit()
                results.append({
                    "query": query,
                    "rows_affected": cursor.rowcount
                })

        conn.close()
    except Exception as e:
        status = "ERROR"
        error_msg = f"{type(e).__name__}: {str(e)}"

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    return {
        "status": status,
        "queries_executed": len(results),
        "results": results,
        "error": error_msg,
        "elapsed_ms": round(elapsed_ms, 2)
    }


def run_regex(
    pattern: str,
    text: str,
    replacement: Optional[str] = None,
    timeout_seconds: float = 3.0,
) -> Dict[str, Any]:
    """
    Tests regular expression matches, capture groups, and substitutions with a timeout guard.
    """
    start_time = time.perf_counter()
    status = "SUCCESS"
    error_msg = None
    matches_data: List[Dict[str, Any]] = []
    replaced_text = None

    worker_outcome: Dict[str, Any] = {}

    def _regex_worker() -> None:
        try:
            compiled = re.compile(pattern)
            local_matches = []
            for idx, m in enumerate(compiled.finditer(text), 1):
                local_matches.append({
                    "match_index": idx,
                    "full_match": m.group(0),
                    "span": m.span(),
                    "groups": list(m.groups()),
                    "groupdict": m.groupdict()
                })
            worker_outcome["matches"] = local_matches
            if replacement is not None:
                worker_outcome["replaced"] = compiled.sub(replacement, text)
        except Exception as exc:
            worker_outcome["error"] = exc

    t = threading.Thread(target=_regex_worker, daemon=True)
    t.start()
    t.join(timeout=max(0.05, float(timeout_seconds)))

    if t.is_alive():
        status = "ERROR"
        error_msg = f"TimeoutError: Regex evaluation exceeded {timeout_seconds}s timeout"
    elif "error" in worker_outcome:
        e = worker_outcome["error"]
        status = "ERROR"
        error_msg = f"{type(e).__name__}: {str(e)}"
    else:
        matches_data = worker_outcome.get("matches", [])
        replaced_text = worker_outcome.get("replaced")

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    return {
        "status": status,
        "pattern": pattern,
        "match_count": len(matches_data),
        "matches": matches_data,
        "replaced_text": replaced_text,
        "error": error_msg,
        "elapsed_ms": round(elapsed_ms, 2)
    }

def format_sql_table(result: Dict[str, Any]) -> str:
    """Formats SQL rows into clean ASCII markdown table."""
    columns = result.get("columns", [])
    rows = result.get("rows", [])
    if not columns:
        return "No rows returned."

    col_widths = {col: len(col) for col in columns}
    for row in rows:
        for idx, col in enumerate(columns):
            val_str = str(row[idx]) if idx < len(row) else "NULL"
            col_widths[col] = max(col_widths[col], len(val_str))

    header = " | ".join(col.ljust(col_widths[col]) for col in columns)
    sep = "-+-".join("-" * col_widths[col] for col in columns)
    row_lines = []
    for row in rows:
        line = " | ".join((str(row[i]) if i < len(row) else "NULL").ljust(col_widths[col]) for i, col in enumerate(columns))
        row_lines.append(line)

    return f"{header}\n{sep}\n" + "\n".join(row_lines)

def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/repl_sandbox.py <py|sql|regex> <expression/query> [extra_args...]")
        print("Examples:")
        print("  python scripts/repl_sandbox.py py \"2**16\"")
        print("  python scripts/repl_sandbox.py sql \"CREATE TABLE t (x INT); INSERT INTO t VALUES (42); SELECT * FROM t;\"")
        print("  python scripts/repl_sandbox.py regex \"(?P<id>\\d+)\" \"User 123 in room 456\"")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    arg1 = sys.argv[2]

    if cmd in ["py", "python", "eval"]:
        res = run_python(arg1)
        print(f"[{res['status']}] Evaluated in {res['elapsed_ms']}ms")
        if res["stdout"]:
            print(f"Stdout:\n{res['stdout'].strip()}")
        if res["result"] is not None:
            print(f"Result: {repr(res['result'])}")
        if res["error"]:
            print(f"Error: {res['error']}")
        sys.exit(0 if res["status"] == "SUCCESS" else 1)

    elif cmd == "sql":
        res = run_sql(arg1)
        print(f"[{res['status']}] Executed in {res['elapsed_ms']}ms")
        if res["error"]:
            print(f"Error: {res['error']}")
            sys.exit(1)
        for r in res["results"]:
            print(f"\nQuery: {r['query']}")
            if "columns" in r:
                print(format_sql_table(r))
            else:
                print(f"Rows affected: {r.get('rows_affected', 0)}")
        sys.exit(0)

    elif cmd == "regex":
        text = sys.argv[3] if len(sys.argv) > 3 else ""
        replacement = sys.argv[4] if len(sys.argv) > 4 else None
        res = run_regex(arg1, text, replacement)
        print(f"[{res['status']}] Tested in {res['elapsed_ms']}ms — {res['match_count']} match(es)")
        if res["error"]:
            print(f"Error: {res['error']}")
            sys.exit(1)
        for m in res["matches"]:
            print(f"  Match #{m['match_index']}: '{m['full_match']}' at {m['span']} | Groups: {m['groups']} | Named: {m['groupdict']}")
        if res["replaced_text"] is not None:
            print(f"Substituted: {res['replaced_text']}")
        sys.exit(0)

    else:
        print(f"Unknown sandbox mode: '{cmd}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
