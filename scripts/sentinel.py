#!/usr/bin/env python3
"""
scripts/sentinel.py
Proactive Architectural Sentinel & Scalability Guard for Agent OS.

Performs proactive, deep architectural auditing across three foundational pillars:
1. Scalability & Latency Invariants (Unbounded queries, N+1 patterns, unindexed columns)
2. Generative Bloat & Parsimony (Speculative single-method classes, stdlib duplication)
3. Product Empathy & UX Soundness (Hostile/leaking error strings, inaccessible controls)
"""

import sys
import os
import re
import ast
from pathlib import Path
from typing import List, Dict, Any, Optional

# UTF-8 terminal encoding configuration
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

# Severity Levels
P0 = "P0"  # Critical Scalability / Sensitive Leak
P1 = "P1"  # Architectural Violation / N+1 Risk / Bloat
P2 = "P2"  # Hygiene / Micro-UX Notice

class SentinelFinding:
    def __init__(self, severity: str, category: str, file_path: str, line_num: int, snippet: str, message: str, suggestion: str):
        self.severity = severity
        self.category = category
        self.file_path = file_path
        self.line_num = line_num
        self.snippet = snippet.strip()
        self.message = message
        self.suggestion = suggestion

    def to_dict(self) -> Dict[str, Any]:
        return {
            "severity": self.severity,
            "category": self.category,
            "file": self.file_path,
            "line": self.line_num,
            "snippet": self.snippet,
            "message": self.message,
            "suggestion": self.suggestion
        }

class ArchitecturalSentinel:
    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = root_dir or WORKSPACE_ROOT
        self.findings: List[SentinelFinding] = []

    def clear(self):
        self.findings = []

    # -------------------------------------------------------------------------
    # 1. SCALABILITY & LATENCY AUDIT
    # -------------------------------------------------------------------------
    def audit_scalability(self, code: str, file_path: str) -> List[SentinelFinding]:
        findings = []
        # Exclude unit test files from unbounded query flagging
        if "test" in file_path.lower():
            return findings

        lines = code.splitlines()

        # Check A: Unbounded SQL queries without LIMIT (excluding aggregate functions)
        sql_pattern = re.compile(r'\b(select\s+.+?\s+from\s+[a-zA-Z0-9_]+)\b', re.IGNORECASE)
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith(("#", "//", "/*", "*")) or "print(" in line:
                continue
            if sql_pattern.search(line):
                lower_line = line.lower()
                is_aggregate = any(agg in lower_line for agg in ["count(", "sum(", "avg(", "max(", "min("])
                has_limit = "limit " in lower_line or "take(" in lower_line or "paginate(" in lower_line
                if not is_aggregate and not has_limit and ("select " in lower_line or "from " in lower_line):
                    findings.append(SentinelFinding(
                        severity=P1,
                        category="SCALABILITY",
                        file_path=file_path,
                        line_num=idx,
                        snippet=line,
                        message="Potential unbounded query detected without explicit LIMIT or pagination.",
                        suggestion="Add explicit LIMIT clause or apply server-side cursor/pagination."
                    ))

        # Check B: ORM Unbounded Bulk Fetch (e.g. Model.all(), User::all())
        unbounded_orm = re.compile(r'(\b[A-Z][a-zA-Z0-9_]*::all\(\)|\b[a-zA-Z0-9_]+\.find_all\(\)|\bprisma\.[a-zA-Z0-9_]+\.findMany\(\s*\))')
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith(("#", "//", "/*", "*")) or "print(" in line:
                continue
            if unbounded_orm.search(line):
                findings.append(SentinelFinding(
                    severity=P1,
                    category="SCALABILITY",
                    file_path=file_path,
                    line_num=idx,
                    snippet=line,
                    message="ORM unconstrained bulk fetch detected. Will exhaust memory under production volume.",
                    suggestion="Replace with chunked streaming (chunk/cursor) or paginated query."
                ))

        # Check C: N+1 Query Patterns (Query calls nested directly inside loop constructs)
        in_loop = False
        loop_depth = 0
        query_call = re.compile(r'\b(find_by|findById|select|query|findUnique|findFirst)\s*\(', re.IGNORECASE)
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith(("#", "//", "/*", "*")):
                continue
            if re.match(r'^(for\s|while\s|foreach\s*\(|\.forEach\(|\.map\()', stripped):
                in_loop = True
                loop_depth += 1
            if in_loop and query_call.search(stripped):
                findings.append(SentinelFinding(
                    severity=P0,
                    category="SCALABILITY",
                    file_path=file_path,
                    line_num=idx,
                    snippet=line,
                    message="N+1 query pattern detected: database fetch inside iterative loop construct.",
                    suggestion="Batch IDs with IN clause, use eager loading (with/include), or join tables."
                ))
            if in_loop and ("}" in stripped or (stripped == "" and loop_depth > 0)):
                loop_depth = max(0, loop_depth - 1)
                if loop_depth == 0:
                    in_loop = False

        # Check D: Missing Index Predicates in Migrations/DDL
        if "migration" in file_path.lower() or "schema" in file_path.lower() or file_path.endswith(".sql"):
            fk_or_timestamp = re.compile(r'(foreignId\([\'"][^\'"]+[\'"]\)|unsignedBigInteger\([\'"].*_id[\'"]\)|timestamp\([\'"](expires_at|deleted_at)[\'"]\))')
            for idx, line in enumerate(lines, start=1):
                stripped = line.strip()
                if stripped.startswith(("#", "//", "/*", "*")):
                    continue
                if fk_or_timestamp.search(line) and "index" not in line.lower() and "primary" not in line.lower():
                    findings.append(SentinelFinding(
                        severity=P1,
                        category="SCALABILITY",
                        file_path=file_path,
                        line_num=idx,
                        snippet=line,
                        message="Foreign key or indexed lifecycle timestamp declared without explicit database index.",
                        suggestion="Append ->index() or add CREATE INDEX to prevent table scans on joins and expirations."
                    ))

        return findings

    # -------------------------------------------------------------------------
    # 2. GENERATIVE BLOAT & PARSIMONY AUDIT
    # -------------------------------------------------------------------------
    def audit_parsimony(self, code: str, file_path: str) -> List[SentinelFinding]:
        findings = []
        if not file_path.endswith(".py") or "test" in file_path.lower():
            return findings

        # Check Python AST for single-method class bloat
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Exclude test classes, data containers, and protocols
                    if node.name.startswith("Test") or node.name.endswith("Test"):
                        continue
                    methods = [m for m in node.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
                    is_special = any(b.id in ["BaseModel", "Exception", "TestCase", "Protocol"] for b in node.bases if isinstance(b, ast.Name))
                    if len(methods) == 1 and not is_special:
                        method_name = methods[0].name
                        if method_name not in ["__init__", "__call__"]:
                            findings.append(SentinelFinding(
                                severity=P2,
                                category="PARSIMONY",
                                file_path=file_path,
                                line_num=node.lineno,
                                snippet=f"class {node.name}: def {method_name}(...)",
                                message="Speculative single-method class detected (Generative Bloat).",
                                suggestion="Replace class with a standalone top-level pure function (Surgical Parsimony)."
                            ))
        except SyntaxError as err:
            # Record non-fatal syntax error for unparsed templates
            findings.append(SentinelFinding(
                severity=P2,
                category="PARSIMONY",
                file_path=file_path,
                line_num=getattr(err, "lineno", 1) or 1,
                snippet=str(err),
                message=f"SyntaxError parsing AST: {err}",
                suggestion="Verify file syntax to enable deep AST parsimony analysis."
            ))

        return findings

    # -------------------------------------------------------------------------
    # 3. PRODUCT EMPATHY & UX SOUNDNESS AUDIT
    # -------------------------------------------------------------------------
    def audit_product_empathy(self, code: str, file_path: str) -> List[SentinelFinding]:
        findings = []
        if "test" in file_path.lower():
            return findings

        lines = code.splitlines()

        # Check A: Hostile or leaking raw error responses
        hostile_err = re.compile(r'(\bres\.(?:status\(\d+\)\.)?(?:send|json|status)\(.*?(something went wrong|internal server error|error 500|err\.message|error\.stack|stack:\s*err).*?\))', re.IGNORECASE)
        for idx, line in enumerate(lines, start=1):
            if hostile_err.search(line):
                findings.append(SentinelFinding(
                    severity=P1,
                    category="PRODUCT_EMPATHY",
                    file_path=file_path,
                    line_num=idx,
                    snippet=line,
                    message="Hostile or raw exception leak in HTTP response (fails Product Empathy & Security).",
                    suggestion="Return sanitized, user-friendly diagnostic guidance with an actionable recovery option."
                ))

        # Check B: Inaccessible interactive controls (buttons/links with generic text)
        generic_control = re.compile(r'(<button[^>]*>\s*(click here|submit|more)\s*</button>|<a\s+[^>]*>\s*(click here|here|more)\s*</a>)', re.IGNORECASE)
        for idx, line in enumerate(lines, start=1):
            if generic_control.search(line) and "aria-label" not in line:
                findings.append(SentinelFinding(
                    severity=P2,
                    category="PRODUCT_EMPATHY",
                    file_path=file_path,
                    line_num=idx,
                    snippet=line,
                    message="Generic interactive button/link label without accessible aria-label.",
                    suggestion="Provide descriptive label (e.g. 'View order details') or supply aria-label."
                ))

        return findings

    # -------------------------------------------------------------------------
    # SCANNER RUNNER
    # -------------------------------------------------------------------------
    def scan_file(self, file_path: Path) -> List[SentinelFinding]:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []

        rel_path = str(file_path.relative_to(self.root_dir)) if self.root_dir in file_path.parents else str(file_path)
        f1 = self.audit_scalability(content, rel_path)
        f2 = self.audit_parsimony(content, rel_path)
        f3 = self.audit_product_empathy(content, rel_path)
        
        all_f = f1 + f2 + f3
        self.findings.extend(all_f)
        return all_f

    def scan_path(self, target_path: Optional[Path] = None) -> List[SentinelFinding]:
        target = target_path or self.root_dir
        self.clear()
        
        if target.is_file():
            self.scan_file(target)
            return self.findings

        valid_extensions = {".py", ".ts", ".tsx", ".js", ".jsx", ".php", ".sql"}
        ignore_dirs = {".git", "__pycache__", "node_modules", "vendor", ".specify"}

        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                p = Path(root) / file
                if p.suffix in valid_extensions:
                    self.scan_file(p)

        return self.findings

    def format_report(self) -> str:
        out = []
        out.append("=" * 65)
        out.append("       ANTIGRAVITY AGENT OS - ARCHITECTURAL SENTINEL REPORT    ")
        out.append("=" * 65)

        p0_count = sum(1 for f in self.findings if f.severity == P0)
        p1_count = sum(1 for f in self.findings if f.severity == P1)
        p2_count = sum(1 for f in self.findings if f.severity == P2)

        out.append(f"Findings: P0 (Critical Scalability): {p0_count} | P1 (Architectural/N+1): {p1_count} | P2 (UX/Parsimony): {p2_count}")
        out.append("-" * 65)

        if not self.findings:
            out.append("  [PASS] Zero architectural or scalability regressions detected.")
            out.append("  [HEALTHY] Proactive Sentinel confirms high-scalability & parsimonious design.")
            out.append("=" * 65)
            return "\n".join(out)

        # Sort findings: P0 first, then P1, then P2
        order = {P0: 0, P1: 1, P2: 2}
        sorted_findings = sorted(self.findings, key=lambda f: order.get(f.severity, 99))

        for f in sorted_findings:
            sev_tag = f"[{f.severity}]".ljust(5)
            out.append(f"{sev_tag} {f.category} in {f.file_path}:{f.line_num}")
            out.append(f"       Message:    {f.message}")
            out.append(f"       Snippet:    {f.snippet}")
            out.append(f"       Remedy:     {f.suggestion}")
            out.append("")

        out.append("=" * 65)
        return "\n".join(out)

def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else WORKSPACE_ROOT
    sentinel = ArchitecturalSentinel(WORKSPACE_ROOT)
    sentinel.scan_path(target)
    print(sentinel.format_report())
    
    # Block if P0 or P1 findings exist
    has_blockers = any(f.severity in [P0, P1] for f in sentinel.findings)
    sys.exit(1 if has_blockers else 0)

if __name__ == "__main__":
    main()
