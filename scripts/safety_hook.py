#!/usr/bin/env python3
"""
PreToolUse Safety Hook for Antigravity Agent.
Intercepts run_command tool calls to prevent accidental destructive operations
like hard git resets, directory wipeouts, or destructive database commands.
"""

import sys
import json
import re

DESTRUCTIVE_PATTERNS = [
    (r"\bgit\s+reset\s+--hard\b", "Hard git reset would discard all uncommitted changes and modified files"),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f", "Untracked file wipeout would permanently delete new files"),
    (r"\brmdir\s+/[sS]\s+/[qQ]\s+\.git\b", "Deleting .git directory destroys version control history"),
    (r"\brm\s+-rf\s+\.git\b", "Deleting .git directory destroys version control history"),
    (r"\bmigrate:fresh\b", "migrate:fresh drops all tables and wipes application data"),
    (r"\bDROP\s+DATABASE\b", "Drop database will destroy all application data"),
]

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"decision": "allow"}))
            return 0

        data = json.loads(raw_input)
        tool_call = data.get("toolCall", {})
        tool_name = tool_call.get("name")
        args = tool_call.get("args", {})

        if tool_name == "run_command":
            cmd = args.get("CommandLine", "")
            for pattern, reason in DESTRUCTIVE_PATTERNS:
                if re.search(pattern, cmd, re.IGNORECASE):
                    print(json.dumps({
                        "decision": "force_ask",
                        "reason": f"SAFETY GUARD BLOCKED: {reason} ('{cmd}')"
                    }))
                    return 0

        print(json.dumps({"decision": "allow"}))
        return 0
    except Exception as e:
        # In case of hook error, allow with log to prevent blocking regular operation
        print(json.dumps({
            "decision": "allow",
            "reason": f"Safety hook evaluation error: {str(e)}"
        }))
        return 0

if __name__ == "__main__":
    sys.exit(main())
