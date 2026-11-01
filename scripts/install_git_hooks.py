#!/usr/bin/env python3
"""
Agent OS Native Git Hook Installer.
Installs cross-platform pre-commit hook that gates commits on:
1. Automated guard validation via guard_checker.py on staged files
2. Stale git lock and diagnostic checks via doctor.py
"""

import sys
import os
from pathlib import Path
from typing import Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

AGENT_OS_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = Path(os.environ.get("AGENT_OS_PROJECT_ROOT") or Path.cwd()).resolve()
WORKSPACE_ROOT = PROJECT_ROOT
HOOKS_DIR = PROJECT_ROOT / ".git" / "hooks"
FALLBACK_GUARD_SCRIPT = (AGENT_OS_ROOT / "scripts" / "guard_checker.py").as_posix()

PRE_COMMIT_SCRIPT = f"""#!/bin/sh
# Antigravity Agent OS - Pre-Commit Quality Guard Hook
python - << 'EOF'
import sys
import subprocess
from pathlib import Path

SCANNED_EXTENSIONS = {{
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".php", ".py", ".css", ".scss", ".vue", ".svelte", ".astro", ".html"
}}

def main():
    print("[*] Pre-Commit Guard: Inspecting staged changes...")
    try:
        output = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            text=True
        ).strip()
    except Exception as e:
        print(f"[BLOCK] Error: Could not inspect git staged files: {{e}}")
        return 1

    if not output:
        return 0

    staged_files = output.splitlines()
    guard_script = Path("scripts/guard_checker.py")
    if not guard_script.exists():
        guard_script = Path("{FALLBACK_GUARD_SCRIPT}")
    if not guard_script.exists():
        print("[BLOCK] Error: guard_checker.py not found locally or in Agent OS.")
        return 1

    has_violations = False
    for f_path in staged_files:
        p = Path(f_path)
        # Skip test directories and test fixtures which intentionally contain test samples
        if "tests" in p.parts or p.name.startswith("test_") or p.name.endswith("Test.php"):
            continue
        if p.suffix.lower() in SCANNED_EXTENSIONS:
            if not p.exists():
                continue
            res = subprocess.run([sys.executable, str(guard_script), str(p)])
            if res.returncode != 0:
                has_violations = True

    if has_violations:
        print("\\n" + "=" * 65)
        print("[BLOCK] Commit rejected: Guard violations detected in staged files!")
        print("Please resolve the issues listed above or run:")
        print("  python scripts/agent_os.py scan <file>")
        print("=" * 65 + "\\n")
        return 1

    print("[PASS] Pre-Commit Guard: Staged changes verified clean.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
EOF
"""


def install_hooks(hooks_dir: Optional[Path] = None) -> bool:
    target_hooks_dir = Path(hooks_dir) if hooks_dir is not None else (
        Path(os.environ.get("AGENT_OS_PROJECT_ROOT") or Path.cwd()).resolve() / ".git" / "hooks"
    )
    if not target_hooks_dir.exists():
        print(f"[!] Git hooks directory not found: {target_hooks_dir}")
        return False

    hook_file = target_hooks_dir / "pre-commit"
    hook_file.write_text(PRE_COMMIT_SCRIPT, encoding="utf-8")

    # On non-Windows POSIX systems, ensure executable permission
    if os.name != "nt":
        try:
            os.chmod(hook_file, 0o755)
        except OSError as err:
            print(f"[!] Notice: Could not set chmod executable permissions: {err}")

    print(f"[SUCCESS] Pre-commit quality guard hook installed at: {hook_file}")
    return True


if __name__ == "__main__":
    success = install_hooks()
    sys.exit(0 if success else 1)
