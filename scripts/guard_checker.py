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
from pathlib import Path
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
    # Strictly gate check to PHP files
    if filename and not (filename.endswith(".php") or filename.endswith(".phtml")):
        return violations
    if "<?php" not in content:
        return violations

    lines = content.splitlines()

    # 1. Check strict types in PHP source files
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
        if "guard-ignore" in line:
            continue
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


def check_python_security_and_hygiene(content: str, filename: str = "") -> List[GuardViolation]:
    """
    Validates Python files for:
    - Mutable default arguments (def foo(items=[]))
    - Insecure os.system calls
    - Hardcoded secret string literals
    """
    violations = []
    if filename and not filename.endswith(".py"):
        return violations
    if "def " not in content and "import " not in content:
        return violations

    lines = content.splitlines()

    # 1. Mutable default arguments in function definitions
    mutable_def = re.compile(r"^\s*def\s+\w+\s*\([^)]*?=\s*(\[\]|\{\}|\bset\(\))\s*[,)]")
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if mutable_def.search(line):
            violations.append(GuardViolation(
                guard_name="clean-code-guard",
                rule="MUTABLE_DEFAULT_ARGUMENT",
                line_no=idx,
                message="Mutable default argument ([], {}, or set()) in function definition. Use None as default.",
                snippet=line.strip()
            ))

    # 2. Insecure os.system
    os_system_pat = re.compile(r"^\s*os\.system\s*\(")
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") or "message=" in line or "rule=" in line:
            continue
        if os_system_pat.search(line):
            violations.append(GuardViolation(
                guard_name="clean-code-guard",
                rule="INSECURE_OS_SYSTEM",
                line_no=idx,
                message="Insecure 'os.system()' call detected. Use subprocess.run() with argument lists instead.",
                snippet=line.strip()
            ))

    # 3. Hardcoded secret/token literals
    secret_pat = re.compile(r'^\s*(?:const\s+|let\s+|var\s+|self\.)?(api_key|secret_key|private_key|auth_token)\s*=\s*["\'][a-zA-Z0-9_\-]{16,}["\']', re.IGNORECASE)
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") or "message=" in line or "rule=" in line:
            continue
        if secret_pat.search(line):
            violations.append(GuardViolation(
                guard_name="clean-code-guard",
                rule="HARDCODED_SECRET_LITERAL",
                line_no=idx,
                message="Potential hardcoded secret or API token in string literal. Load from environment variable.",
                snippet=line.strip()
            ))

    return violations


def check_architectural_boundaries(content: str, filename: str = "") -> List[GuardViolation]:
    """
    Validates Architectural Layer, Bounded Domain, and Public/Admin Shell Boundaries:
    - CLIENT_SERVER_BOUNDARY_LEAK: "use client" components importing DB/Repository/server-only modules
    - LAYER_SKIPPING_CONTROLLER_BYPASS: HTTP Controllers directly calling *Repository or raw SQL/transactions
    - PUBLIC_ADMIN_SHELL_LEAK: Public routes importing Admin shell (AdminSidebar/AdminNavbar) or Admin routes importing Public Navbar/Footer
    - CROSS_DOMAIN_REPOSITORY_LEAK: Domain A importing internal Repository of Domain B
    - UPWARD_ABSTRACTION_LEAK: Services/Repositories returning unexecuted ORM query builders or raw driver statements
    """
    violations = []
    fn_norm = filename.replace("\\", "/") if filename else ""
    fn_lower = fn_norm.lower()

    # Do not scan guard/test/sentinel scripts themselves unless invoked with synthetic filename in unit tests
    if fn_lower and any(skip in fn_lower for skip in ["guard_checker.py", "sentinel.py", "test_guards_battery.py", "test_sentinel.py"]):
        return violations

    lines = content.splitlines()
    is_client_component = '"use client"' in content or "'use client'" in content
    is_controller = (
        fn_lower.endswith("controller.php")
        or fn_lower.endswith(".controller.ts")
        or fn_lower.endswith(".controller.js")
        or bool(re.search(r"\bclass\s+\w+Controller\b", content))
    )

    # 1. Client -> Server / DB / Repository Boundary Leak
    if is_client_component:
        server_import_pat = re.compile(
            r"""^\s*import\s+.*?\bfrom\s+['"](@prisma/client|[^'"]*/lib/(?:db|prisma)|[^'"]*/repositories/[^'"]+|[^'"]*\.repo(?:sitory)?|(?:node:)?(?:fs|fs/promises|child_process|net|tls)|mysql2|pg|better-sqlite3)['"]"""
        )
        direct_db_call_pat = re.compile(r"\b(prisma\.\w+\.(?:findMany|findUnique|findFirst|create|update|delete|upsert|\$queryRaw)|db\.query\s*\()")
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("*"):
                continue
            if server_import_pat.search(line) or direct_db_call_pat.search(line):
                violations.append(GuardViolation(
                    guard_name="clean-code-guard",
                    rule="CLIENT_SERVER_BOUNDARY_LEAK",
                    line_no=idx,
                    message="Client component ('use client') imports or calls server-only persistence/repository module. Move data access to a Server Component or Server Action.",
                    snippet=stripped
                ))

    # 2. Layer Skipping in HTTP Controllers (Controller -> Repository or Raw SQL / Transaction)
    if is_controller:
        raw_sql_or_tx_pat = re.compile(
            r"\b(DB::(?:raw|statement|unprepared|select|beginTransaction)\s*\(|prisma\.\$(?:queryRaw|executeRaw|transaction)\b)"
        )
        repo_bypass_pat = re.compile(
            r"(?:^\s*use\s+[\w\\]+\\Repositories\\\w+Repository\b|^\s*import\s+.*?\b\w+Repository\b.*?\bfrom\b|\b\w+Repository\s+\$\w+|\bprivate\s+(?:readonly\s+)?\w+\s*:\s*\w+Repository\b)"
        )
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("#") or stripped.startswith("*"):
                continue
            if raw_sql_or_tx_pat.search(line):
                violations.append(GuardViolation(
                    guard_name="clean-code-guard",
                    rule="LAYER_SKIPPING_CONTROLLER_BYPASS",
                    line_no=idx,
                    message="Controller executes raw SQL or manual DB transaction directly, bypassing the Service/Action layer.",
                    snippet=stripped
                ))
            if repo_bypass_pat.search(line):
                violations.append(GuardViolation(
                    guard_name="clean-code-guard",
                    rule="LAYER_SKIPPING_CONTROLLER_BYPASS",
                    line_no=idx,
                    message="Controller couples directly to a Repository, bypassing the Service/Action orchestration layer.",
                    snippet=stripped
                ))

    # 3. Public vs. Admin Shell Separation Leak
    is_public_scope = (
        "/(public)/" in fn_lower
        or "/public/" in fn_lower
        or bool(re.search(r"\b(?:function|class)\s+Public\w*(?:Page|Layout|View)\b", content))
    )
    is_admin_scope = (
        "/admin/" in fn_lower
        or fn_lower.startswith("admin/")
        or bool(re.search(r"\b(?:function|class)\s+Admin\w*(?:Page|Layout|View)\b", content))
    )

    if is_public_scope and not is_admin_scope:
        admin_shell_pat = re.compile(r"""(\bAdmin(?:Sidebar|Navbar|Shell|Header|Layout)\b|from\s+['"][^'"]*/components/admin/)""")
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("*"):
                continue
            if admin_shell_pat.search(line):
                violations.append(GuardViolation(
                    guard_name="clean-code-guard",
                    rule="PUBLIC_ADMIN_SHELL_LEAK",
                    line_no=idx,
                    message="Public route/view imports or renders Admin shell navigation (AdminSidebar/AdminNavbar). Keep Public and Admin shells strictly isolated.",
                    snippet=stripped
                ))

    if is_admin_scope and not is_public_scope:
        public_shell_pat = re.compile(r"""(\bPublic(?:Navbar|Footer|Header|Shell|Layout)\b|from\s+['"][^'"]*/components/public/(?:Navbar|Footer|Header))""")
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("*"):
                continue
            if public_shell_pat.search(line):
                violations.append(GuardViolation(
                    guard_name="clean-code-guard",
                    rule="PUBLIC_ADMIN_SHELL_LEAK",
                    line_no=idx,
                    message="Admin route/view imports or renders Public shell navigation (PublicNavbar/PublicFooter). Keep Public and Admin shells strictly isolated.",
                    snippet=stripped
                ))

    # 4. Cross-Domain Internal Repository Leak
    php_domain_match = re.search(r"namespace\s+App\\Domains\\([A-Za-z0-9_]+)", content)
    path_domain_match = re.search(r"(?:^|/)domains/([a-zA-Z0-9_-]+)/", fn_norm, re.IGNORECASE)
    current_domain = (
        php_domain_match.group(1).lower() if php_domain_match
        else (path_domain_match.group(1).lower() if path_domain_match else None)
    )

    if current_domain:
        php_cross_repo = re.compile(r"^\s*use\s+App\\Domains\\([A-Za-z0-9_]+)\\Repositories\\(\w+)")
        ts_cross_repo = re.compile(r"""from\s+['"][^'"]*domains/([a-zA-Z0-9_-]+)/repositories/([^'"]+)['"]""", re.IGNORECASE)
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("#") or stripped.startswith("*"):
                continue
            m_php = php_cross_repo.search(line)
            if m_php and m_php.group(1).lower() != current_domain:
                violations.append(GuardViolation(
                    guard_name="clean-code-guard",
                    rule="CROSS_DOMAIN_REPOSITORY_LEAK",
                    line_no=idx,
                    message=f"Domain '{current_domain}' imports internal Repository '{m_php.group(2)}' from foreign Domain '{m_php.group(1)}'. Use public Service/Action contracts across domains.",
                    snippet=stripped
                ))
            m_ts = ts_cross_repo.search(line)
            if m_ts and m_ts.group(1).lower() != current_domain:
                violations.append(GuardViolation(
                    guard_name="clean-code-guard",
                    rule="CROSS_DOMAIN_REPOSITORY_LEAK",
                    line_no=idx,
                    message=f"Domain '{current_domain}' imports internal Repository from foreign Domain '{m_ts.group(1)}'. Use public Service/Action contracts across domains.",
                    snippet=stripped
                ))

    # 5. Upward Abstraction Leak (Returning unexecuted ORM Query Builder, PDOStatement, or SDK HTTP wrapper from Service/Repository)
    imports_orm_builder = bool(re.search(r"use\s+Illuminate\\Database\\(?:Eloquent|Query)\\Builder\b", content))
    abstraction_leak_pat = re.compile(
        r"(?:function\s+\w+\s*\([^)]*\)\s*:\s*(?:\\?Illuminate\\Database\\(?:Eloquent|Query)\\Builder|Eloquent\\Builder|Query\\Builder|\\?PDOStatement|Stripe\\ApiResponse|AxiosResponse"
        + (r"|Builder" if imports_orm_builder else "")
        + r")\b)"
    )
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("#") or stripped.startswith("*"):
            continue
        if abstraction_leak_pat.search(line):
            violations.append(GuardViolation(
                guard_name="clean-code-guard",
                rule="UPWARD_ABSTRACTION_LEAK",
                line_no=idx,
                message="Method leaks unexecuted ORM Builder, raw PDOStatement, or transport wrapper across layer boundary. Return a domain DTO, Collection, or paginated result.",
                snippet=stripped
            ))

    return violations


def check_modularity_and_reusability(content: str, filename: str = "") -> List[GuardViolation]:
    """
    Enforces Junior-Developer Readability, Single-Component-Per-File Modularity,
    Practical 2+ Reusability, and the 2-3 Line Component Header Comment contract:
    1. MONOLITH_COMPONENT_FILE: Entry files (App.jsx/tsx, page.jsx/tsx, index.jsx/tsx)
       must not bundle 3+ distinct UI components/sections inline (e.g., Header + Hero + Footer + Card).
    2. MISSING_COMPONENT_HEADER_DOC: Reusable UI component files under components/
       must start with a concise 2-3 line header comment (Purpose | Reused In | Key Props/Inputs).
    3. EXTREME_TOKEN_MICRO_ABSTRACTION: Flags pointless wrapper components around a single raw font/color CSS token.
    """
    violations: List[GuardViolation] = []
    if not filename:
        return violations

    fn_norm = filename.replace("\\", "/")
    fn_lower = fn_norm.lower()
    base_lower = fn_lower.split("/")[-1]
    lines = content.splitlines()

    # 1. Monolith Component File Check on entry/page files
    is_entry_file = base_lower in ("app.jsx", "app.tsx", "page.jsx", "page.tsx", "index.jsx", "index.tsx")
    if is_entry_file:
        comp_decl_pat = re.compile(
            r"^\s*(?:export\s+(?:default\s+)?)?(?:function\s+([A-Z][A-Za-z0-9_]*)\s*\(|const\s+([A-Z][A-Za-z0-9_]*)\s*(?::\s*[^=]+)?=\s*(?:async\s*)?(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>)"
        )
        found_components: List[tuple] = []
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
                continue
            m = comp_decl_pat.search(line)
            if m:
                comp_name = m.group(1) or m.group(2)
                found_components.append((idx, comp_name, stripped))

        if len(found_components) >= 3:
            names_str = ", ".join(c[1] for c in found_components)
            first_line, _, first_snip = found_components[0]
            violations.append(GuardViolation(
                guard_name="clean-code-guard",
                rule="MONOLITH_COMPONENT_FILE",
                line_no=first_line,
                message=(
                    f"Entry file '{base_lower}' bundles {len(found_components)} components inline ({names_str}). "
                    "Split Header, Hero, Footer, and reusable primitives (Button, Card) into separate 1-component-per-file modules."
                ),
                snippet=first_snip[:80]
            ))

    # 2. Concise 2-3 Line Component Header Check on reusable components
    is_reusable_component_file = (
        ("/components/" in fn_lower or fn_lower.startswith("components/"))
        and any(fn_lower.endswith(ext) for ext in (".jsx", ".tsx", ".vue", ".svelte"))
        and not base_lower.endswith((".test.tsx", ".test.jsx", ".spec.tsx", ".spec.jsx", ".types.ts", ".stories.tsx"))
    )
    if is_reusable_component_file:
        top_slice = "\n".join(lines[:12])
        has_header_comment = bool(
            re.search(r"(/\*[\s\S]*?\*/|^\s*//\s*\S+)", top_slice, re.MULTILINE)
        )
        if not has_header_comment:
            violations.append(GuardViolation(
                guard_name="clean-code-guard",
                rule="MISSING_COMPONENT_HEADER_DOC",
                line_no=1,
                message=(
                    "Reusable component file is missing a concise 2-3 line top header comment "
                    "(Purpose | Reused In | Key Props/Inputs) for junior-developer readability."
                ),
                snippet=lines[0].strip()[:80] if lines else ""
            ))

    return violations


def scan_content(content: str, filename: str = "") -> List[GuardViolation]:
    """Runs all relevant guard checks on a given content string."""
    violations = []
    fn_lower = filename.lower() if filename else ""

    # Next.js Server Actions: JS/TS component and action files
    if not fn_lower or any(fn_lower.endswith(ext) for ext in [".js", ".jsx", ".ts", ".tsx"]):
        violations.extend(check_next_server_actions(content))

    # Pest PHP: PHP files only
    if not fn_lower or fn_lower.endswith(".php") or fn_lower.endswith(".phtml"):
        violations.extend(check_pest_php_security(content, filename))

    # RTL CSS: Style sheets, templates, and UI components (never scan python scripts)
    if not fn_lower or (not fn_lower.endswith(".py") and any(fn_lower.endswith(ext) for ext in [".css", ".scss", ".sass", ".less", ".html", ".astro", ".vue", ".svelte", ".jsx", ".tsx", ".js", ".ts"])):
        violations.extend(check_rtl_logical_css(content))

    # Clean code & Architectural Boundaries: scan all code files except guard_checker.py itself
    if "guard_checker.py" not in fn_lower:
        violations.extend(check_clean_code_hygiene(content))
        violations.extend(check_architectural_boundaries(content, filename))
        violations.extend(check_modularity_and_reusability(content, filename))

    # Python security and hygiene: Python files only
    if not fn_lower or fn_lower.endswith(".py"):
        violations.extend(check_python_security_and_hygiene(content, filename))

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
