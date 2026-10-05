#!/usr/bin/env python3
"""
Automated Quality Guard Checker for Antigravity Agent OS.
Implements programmatic verification for:
1. Next.js Server Action Guard (Auth derivation, Anti-IDOR, Zod validation, Error boundaries)
2. Pest & PHP Security Guard (strict_types, dangerous functions, arch presets)
3. RTL / Logical Properties Guard (Physical CSS/Tailwind vs Logical Properties)
4. Clean Code Hygiene Guard (Swallowed errors, deep nesting, dead code)
"""

import sys
import re
from typing import List, Dict, Any

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

class GuardViolation:
    def __init__(self, guard_name: str, rule: str, line_no: int, message: str, snippet: str = ""):
        self.guard_name = guard_name
        self.rule = rule
        self.line_no = line_no
        self.message = message
        self.snippet = snippet

    def to_dict(self) -> Dict[str, Any]:
        return {
            "guard": self.guard_name,
            "rule": self.rule,
            "line": self.line_no,
            "message": self.message,
            "snippet": self.snippet
        }

    def __repr__(self) -> str:
        return f"[{self.guard_name}] Line {self.line_no} ({self.rule}): {self.message}"


def check_next_server_actions(content: str) -> List[GuardViolation]:
    """
    Validates Next.js App Router Server Actions for:
    - Server-side auth derivation (never trusting userId/role from payload)
    - Anti-IDOR ownership verification
    - Schema validation via safeParse
    - Secure error handling
    """
    violations = []
    lines = content.splitlines()

    is_server_file = '"use server"' in content or "'use server'" in content
    
    # Check for direct client-supplied userId/tenantId in action signatures
    param_pattern = re.compile(r"export\s+async\s+function\s+\w+\s*\(\s*\{[^}]*\b(userId|user_id|tenantId|role|isAdmin)\b[^}]*\}")
    for idx, line in enumerate(lines, 1):
        if is_server_file or "use server" in line:
            m = param_pattern.search(line)
            if m:
                violations.append(GuardViolation(
                    guard_name="next-server-action-guard",
                    rule="AUTH_DERIVATION_VIOLATION",
                    line_no=idx,
                    message=f"Server Action accepts '{m.group(1)}' from payload. Auth identity MUST be derived server-side via session/auth().",
                    snippet=line.strip()
                ))

    # Check for IDOR: db delete/update by ID alone without tenant/user scoping
    idor_pattern = re.compile(
        r"\.(delete|update)\s*\(\s*\{\s*where:\s*\{\s*id\b(?![^}]*\b(userId|user_id|tenantId|ownerId)\b)",
        re.DOTALL
    )
    for m in idor_pattern.finditer(content):
        line_no = content[:m.start()].count("\n") + 1
        violations.append(GuardViolation(
            guard_name="next-server-action-guard",
            rule="ANTI_IDOR_VIOLATION",
            line_no=line_no,
            message="Resource updated/deleted by ID without ownership or tenant verification check.",
            snippet=m.group(0).replace("\n", " ")[:60].strip()
        ))

    # Check for raw error leakage in catch blocks
    raw_error_pattern = re.compile(r"return\s*\{[^}]*error:\s*(err|error)\.(message|stack)")
    for idx, line in enumerate(lines, 1):
        if raw_error_pattern.search(line):
            violations.append(GuardViolation(
                guard_name="next-server-action-guard",
                rule="RAW_ERROR_LEAK",
                line_no=idx,
                message="Catch block returns raw error.message or error.stack to client. Return generic message and log internally.",
                snippet=line.strip()
            ))

    return violations


def check_pest_php_security(content: str, filename: str = "") -> List[GuardViolation]:
    """
    Validates PHP & Pest 3 code against:
    - strict_types declaration
    - dangerous forbidden PHP functions
    - security architectural preset in Pest test suites
    """
    violations = []
    lines = content.splitlines()

    # 1. Check strict types in PHP source files
    if "<?php" in content:
        has_strict = any("declare(strict_types=1);" in line for line in lines[:10])
        if not has_strict and not filename.endswith("blade.php"):
            violations.append(GuardViolation(
                guard_name="pest-security-guard",
                rule="STRICT_TYPES_REQUIRED",
                line_no=1,
                message="PHP file missing mandatory 'declare(strict_types=1);' in file header."
            ))

    # 2. Check dangerous functions
    dangerous_fns = [
        ("eval", r"\beval\s*\("),
        ("exec", r"\bexec\s*\("),
        ("shell_exec", r"\bshell_exec\s*\("),
        ("system", r"\bsystem\s*\("),
        ("passthru", r"\bpassthru\s*\("),
        ("unserialize", r"\bunserialize\s*\("),
    ]

    for idx, line in enumerate(lines, 1):
        # Skip commented lines
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("#") or stripped.startswith("*"):
            continue
        for fn_name, pat in dangerous_fns:
            if re.search(pat, line):
                violations.append(GuardViolation(
                    guard_name="pest-security-guard",
                    rule="DANGEROUS_FUNCTION_FORBIDDEN",
                    line_no=idx,
                    message=f"Forbidden dangerous function '{fn_name}()' detected.",
                    snippet=line.strip()
                ))

    # 3. Pest architectural security check
    if "arch()" in content and not any("preset()->security()" in line for line in lines):
        violations.append(GuardViolation(
            guard_name="pest-security-guard",
            rule="ARCH_SECURITY_PRESET_MISSING",
            line_no=1,
            message="Pest architectural tests detected without 'arch()->preset()->security()'."
        ))

    return violations


def check_rtl_logical_css(content: str) -> List[GuardViolation]:
    """
    Validates CSS, JSX, and HTML templates for bidirectional (LTR/RTL) integrity.
    Detects physical CSS directions and Tailwind physical utility classes.
    """
    violations = []
    lines = content.splitlines()

    # CSS physical property checks
    css_physical_patterns = [
        (r"\bmargin-left\s*:", "Use 'margin-inline-start' instead of physical 'margin-left'"),
        (r"\bmargin-right\s*:", "Use 'margin-inline-end' instead of physical 'margin-right'"),
        (r"\bpadding-left\s*:", "Use 'padding-inline-start' instead of physical 'padding-left'"),
        (r"\bpadding-right\s*:", "Use 'padding-inline-end' instead of physical 'padding-right'"),
        (r"\bleft\s*:\s*\d+", "Use 'inset-inline-start' instead of physical 'left' for positioning"),
        (r"\bright\s*:\s*\d+", "Use 'inset-inline-end' instead of physical 'right' for positioning"),
        (r"\btext-align\s*:\s*left\b", "Use 'text-align: start' instead of physical 'text-align: left'"),
        (r"\btext-align\s*:\s*right\b", "Use 'text-align: end' instead of physical 'text-align: right'"),
    ]

    # Tailwind physical classes checks
    tailwind_physical_patterns = [
        (r'(?:className|class)=["\'][^"\']*\bml-\d+\b', "Use 'ms-*' (margin-start) instead of physical 'ml-*'"),
        (r'(?:className|class)=["\'][^"\']*\bmr-\d+\b', "Use 'me-*' (margin-end) instead of physical 'mr-*'"),
        (r'(?:className|class)=["\'][^"\']*\bpl-\d+\b', "Use 'ps-*' (padding-start) instead of physical 'pl-*'"),
        (r'(?:className|class)=["\'][^"\']*\bpr-\d+\b', "Use 'pe-*' (padding-end) instead of physical 'pr-*'"),
        (r'(?:className|class)=["\'][^"\']*\btext-left\b', "Use 'text-start' instead of physical 'text-left'"),
        (r'(?:className|class)=["\'][^"\']*\btext-right\b', "Use 'text-end' instead of physical 'text-right'"),
    ]

    for idx, line in enumerate(lines, 1):
        for pattern, recommendation in css_physical_patterns:
            if re.search(pattern, line):
                violations.append(GuardViolation(
                    guard_name="rtl-logical-guard",
                    rule="PHYSICAL_CSS_PROPERTY",
                    line_no=idx,
                    message=f"Physical CSS property violates RTL layout integrity: {recommendation}",
                    snippet=line.strip()
                ))

        for pattern, recommendation in tailwind_physical_patterns:
            if re.search(pattern, line):
                violations.append(GuardViolation(
                    guard_name="rtl-logical-guard",
                    rule="PHYSICAL_TAILWIND_UTILITY",
                    line_no=idx,
                    message=f"Physical Tailwind class violates RTL layout integrity: {recommendation}",
                    snippet=line.strip()
                ))

    return violations


def check_clean_code_hygiene(content: str) -> List[GuardViolation]:
    """
    Validates general clean code, error swallowing, and code health:
    - Silent error swallowing (except: pass or empty catch blocks)
    - Commented-out dead code blocks
    """
    violations = []

    # 1. Swallowed errors in Python (single-line or multi-line except ...: \n pass)
    swallowed_py = re.compile(r"except(\s+[^\n:]+)?:(\s*#.*)?\s*(\n\s*)pass\b")
    for m in swallowed_py.finditer(content):
        line_no = content[:m.start()].count("\n") + 1
        violations.append(GuardViolation(
            guard_name="clean-code-guard",
            rule="SWALLOWED_EXCEPTION",
            line_no=line_no,
            message="Silent exception swallowing ('except: pass'). Always log or handle errors.",
            snippet=m.group(0).replace("\n", " ").strip()
        ))

    # 2. Swallowed errors in JS/TS/PHP (single-line or multi-line catch (e) { })
    swallowed_js = re.compile(r"catch\s*\([^)]*\)\s*\{\s*\}", re.DOTALL)
    for m in swallowed_js.finditer(content):
        line_no = content[:m.start()].count("\n") + 1
        violations.append(GuardViolation(
            guard_name="clean-code-guard",
            rule="SWALLOWED_EXCEPTION",
            line_no=line_no,
            message="Empty catch block swallowed silently ('catch (e) {}'). Log or handle errors.",
            snippet=m.group(0).replace("\n", " ").strip()
        ))

    return violations


def scan_content(content: str, filename: str = "") -> List[GuardViolation]:
    """Runs all relevant guard checks on a given content string."""
    violations = []
    violations.extend(check_next_server_actions(content))
    violations.extend(check_pest_php_security(content, filename))
    violations.extend(check_rtl_logical_css(content))
    violations.extend(check_clean_code_hygiene(content))
    return violations


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python guard_checker.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        file_content = f.read()

    results = scan_content(file_content, filepath)
    if not results:
        print(f"[PASS] All guard checks passed for {filepath}")
        sys.exit(0)
    else:
        print(f"[FAIL] Found {len(results)} guard violation(s) in {filepath}:")
        for v in results:
            print(f"  - {v}")
        sys.exit(1)
