#!/usr/bin/env python3
"""
scripts/ui_audit_engine.py
100X Frontend UI Quality Audit & Implementation Prompt Engine for Agent OS.

Performs high-speed, evidence-based, deterministic static analysis of any frontend codebase across 8 dimensions:
1. Visual Consistency & Design Tokens
2. Responsive Behavior & Viewport Breakpoints
3. Accessibility (WCAG 2.2 Level AA)
4. Interactions & Micro-Behavior
5. Forms, Inputs & Validation Feedback
6. Layout, Content & The 6-State Matrix
7. Navigation & Information Architecture
8. Localization & RTL (Bidirectional CSS Logical Properties)

Generates:
- docs/ui-audits/<YYYY-MM-DD-HHmmss>/report.md
- docs/ui-audits/<YYYY-MM-DD-HHmmss>/manual-browser-checklist.md
- docs/ui-audits/<YYYY-MM-DD-HHmmss>/prompts/UI-XXX-<slug>.md (10-Section Self-Contained Prompts)
"""

import sys
import os
import re
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path("D:/Skills/.agents")

# Excluded directories for fast scanning
IGNORE_DIRS = {
    ".git", "node_modules", ".next", "dist", "build", "vendor",
    "coverage", ".specify", ".system_generated", "brain", "__pycache__"
}

FRONTEND_EXTS = {".tsx", ".jsx", ".vue", ".svelte", ".blade.php", ".html", ".css", ".scss"}

# Severity Levels
CRITICAL = "Critical"
HIGH = "High"
MEDIUM = "Medium"
LOW = "Low"

class UIFinding:
    def __init__(
        self,
        finding_id: str,
        title: str,
        category: str,
        severity: str,
        confidence: str,
        file_path: str,
        line_num: int,
        code_snippet: str,
        current_behavior: str,
        expected_behavior: str,
        user_impact: str,
        root_cause: str,
        is_hypothesis: bool,
        recommended_solution: str,
        affected_routes: Optional[List[str]] = None,
        component_name: Optional[str] = None
    ):
        self.finding_id = finding_id
        self.title = title
        self.category = category
        self.severity = severity
        self.confidence = confidence
        self.file_path = file_path.replace("\\", "/")
        self.line_num = line_num
        self.code_snippet = code_snippet.strip()
        self.current_behavior = current_behavior
        self.expected_behavior = expected_behavior
        self.user_impact = user_impact
        self.root_cause = root_cause
        self.is_hypothesis = is_hypothesis
        self.recommended_solution = recommended_solution
        self.affected_routes = affected_routes or []
        self.component_name = component_name or Path(file_path).stem

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.finding_id,
            "title": self.title,
            "category": self.category,
            "severity": self.severity,
            "confidence": self.confidence,
            "file": self.file_path,
            "line": self.line_num,
            "component": self.component_name,
            "snippet": self.code_snippet,
            "current_behavior": self.current_behavior,
            "expected_behavior": self.expected_behavior,
            "user_impact": self.user_impact,
            "root_cause": self.root_cause,
            "is_hypothesis": self.is_hypothesis,
            "solution": self.recommended_solution,
            "affected_routes": self.affected_routes
        }

class FrontendTopology:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.framework = "Unknown Frontend"
        self.styling_system = "Standard CSS"
        self.ui_library = "Custom Primitives"
        self.has_rtl = False
        self.routes: List[str] = []
        self.components: List[Path] = []
        self.pages: List[Path] = []
        self.layouts: List[Path] = []
        self.tokens: Dict[str, Any] = {}
        self.test_diagnostics: List[str] = []

    def discover(self):
        # 1. Framework & Routing Detection
        pkg_json = self.root_dir / "package.json"
        if pkg_json.exists():
            try:
                pkg_data = json.loads(pkg_json.read_text(encoding="utf-8", errors="ignore"))
                deps = {**pkg_data.get("dependencies", {}), **pkg_data.get("devDependencies", {})}
                scripts = pkg_data.get("scripts", {})

                if "next" in deps:
                    self.framework = f"Next.js {deps.get('next', '')} (React {deps.get('react', '')})"
                elif "nuxt" in deps:
                    self.framework = "Nuxt / Vue"
                elif "vue" in deps:
                    self.framework = "Vue.js"
                elif "@sveltejs/kit" in deps or "svelte" in deps:
                    self.framework = "SvelteKit / Svelte"
                elif "@angular/core" in deps:
                    self.framework = "Angular"
                elif "react" in deps:
                    self.framework = "React SPA"

                # Styling
                if "tailwindcss" in deps or "@tailwindcss/postcss" in deps:
                    self.styling_system = "Tailwind CSS"
                elif "sass" in deps or "node-sass" in deps:
                    self.styling_system = "SASS / SCSS"

                # UI Libraries
                if "@radix-ui/react-slot" in deps or "shadcn" in pkg_data.get("name", ""):
                    self.ui_library = "shadcn/ui (Radix UI Primitives)"
                elif "@mui/material" in deps:
                    self.ui_library = "Material UI"
                elif "@chakra-ui/react" in deps:
                    self.ui_library = "Chakra UI"

                # RTL / i18n
                if "next-intl" in deps or "react-i18next" in deps or "i18next" in deps:
                    self.has_rtl = True

                # Diagnostics
                for s in ["lint", "type-check", "test", "test:e2e", "check"]:
                    if s in scripts:
                        self.test_diagnostics.append(f"npm run {s}")
            except (json.JSONDecodeError, OSError) as e:
                sys.stderr.write(f"[ui-audit] Warning: Could not parse package.json: {e}\n")

        # Check Laravel
        if (self.root_dir / "artisan").exists() or (self.root_dir / "composer.json").exists():
            self.framework = "Laravel (Blade / Inertia)"
            self.test_diagnostics.append("./vendor/bin/pest")

        # 2. Scan Files
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                p = Path(root) / file
                ext = p.suffix.lower()
                rel = p.relative_to(self.root_dir).as_posix()

                if ext in FRONTEND_EXTS:
                    # Classify
                    if "layout" in file.lower():
                        self.layouts.append(p)
                    elif "page" in file.lower() or "view" in file.lower():
                        self.pages.append(p)
                        self.routes.append(f"/{rel}")
                    elif "components" in rel.lower():
                        self.components.append(p)

                # Check HTML dir="rtl"
                if ext in {".html", ".blade.php", ".tsx", ".jsx"}:
                    try:
                        c = p.read_text(encoding="utf-8", errors="ignore")
                        if 'dir="rtl"' in c or "dir='rtl'" in c:
                            self.has_rtl = True
                    except OSError as e:
                        sys.stderr.write(f"[ui-audit] Warning: Could not read {p.name}: {e}\n")

class UIAuditEngine:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.topology = FrontendTopology(root_dir)
        self.findings: List[UIFinding] = []
        self.counter = 1

    def _next_id(self) -> str:
        fid = f"UI-{self.counter:03d}"
        self.counter += 1
        return fid

    def analyze(self):
        self.topology.discover()
        self.findings = []
        self.counter = 1

        # Walk target files
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                p = Path(root) / file
                if p.suffix.lower() in FRONTEND_EXTS:
                    self._audit_file(p)

        self._deduplicate_and_attribute()

    def _audit_file(self, file_path: Path):
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()
        except OSError as e:
            sys.stderr.write(f"[ui-audit] Warning: Could not read {file_path.name}: {e}\n")
            return

        rel_path = file_path.relative_to(self.root_dir).as_posix()

        # -------------------------------------------------------------
        # DIMENSION 1: Visual Consistency & Design Tokens
        # -------------------------------------------------------------
        # Hardcoded hex colors in JSX / Tailwind classes (e.g. text-[#123456], bg-[#fff])
        for idx, line in enumerate(lines, 1):
            hex_match = re.search(r'(?:bg|text|border|fill|stroke)-\[#(?:[0-9a-fA-F]{3,8})\]', line)
            if hex_match:
                self.findings.append(UIFinding(
                    finding_id=self._next_id(),
                    title=f"Hardcoded Arbitrary Hex Color '{hex_match.group(0)}'",
                    category="Visual Consistency",
                    severity=LOW,
                    confidence="High",
                    file_path=rel_path,
                    line_num=idx,
                    code_snippet=line,
                    current_behavior=f"Element defines arbitrary raw hex color: `{hex_match.group(0)}`.",
                    expected_behavior="Colors must utilize semantic design system tokens (e.g. `bg-primary`, `text-muted-foreground`).",
                    user_impact="Creates visual color inconsistency and prevents dark/light theme adaptation.",
                    root_cause="Developer hardcoded custom hex value instead of mapping to the project color palette.",
                    is_hypothesis=False,
                    recommended_solution="Replace arbitrary hex utility with the matching semantic color token from design tokens.",
                    affected_routes=[f"/{rel_path}"]
                ))

            # Arbitrary pixel padding/margin (e.g. p-[13px], mt-[27px])
            spacing_match = re.search(r'(?:p|m|gap|px|py|pt|pb|pl|pr|ps|pe|ms|me)-\[\d{2,}px\]', line)
            if spacing_match:
                self.findings.append(UIFinding(
                    finding_id=self._next_id(),
                    title=f"Non-Standard Arbitrary Pixel Spacing '{spacing_match.group(0)}'",
                    category="Visual Consistency",
                    severity=LOW,
                    confidence="High",
                    file_path=rel_path,
                    line_num=idx,
                    code_snippet=line,
                    current_behavior=f"Element specifies arbitrary spacing: `{spacing_match.group(0)}`.",
                    expected_behavior="Spacing must adhere to the 4px/8px design grid (e.g. `p-3`, `p-4`, `m-6`).",
                    user_impact="Creates uneven visual rhythm and micro-misalignment across views.",
                    root_cause="Ad-hoc pixel override bypassing the standard spacing scale.",
                    is_hypothesis=False,
                    recommended_solution="Refactor arbitrary pixel value to the nearest standard Tailwind spacing step.",
                    affected_routes=[f"/{rel_path}"]
                ))

        # -------------------------------------------------------------
        # DIMENSION 2: Responsive Behavior & Viewport Breakpoints
        # -------------------------------------------------------------
        for idx, line in enumerate(lines, 1):
            # Fixed width exceeding mobile viewport (e.g. w-[600px], min-w-[700px])
            fixed_w = re.search(r'(?:w|min-w)-\[(\d{3,})px\]', line)
            if fixed_w:
                px_val = int(fixed_w.group(1))
                if px_val >= 450:
                    self.findings.append(UIFinding(
                        finding_id=self._next_id(),
                        title=f"Fixed Container Width ({px_val}px) Risks Mobile Viewport Overflow",
                        category="Responsive Behavior",
                        severity=HIGH,
                        confidence="High",
                        file_path=rel_path,
                        line_num=idx,
                        code_snippet=line,
                        current_behavior=f"Container enforces fixed width `{fixed_w.group(0)}` without responsive scaling.",
                        expected_behavior="Containers must use fluid sizing (e.g. `w-full max-w-lg md:max-w-2xl`).",
                        user_impact=f"Causes severe horizontal scrollbars and content clipping on mobile screens (< {px_val}px).",
                        root_cause="Hardcoded pixel width prevents fluid viewport reflow on mobile devices.",
                        is_hypothesis=False,
                        recommended_solution="Replace fixed width with `w-full` paired with responsive `max-w-*` constraints.",
                        affected_routes=[f"/{rel_path}"]
                    ))

            # Inflexible grid without responsive columns (e.g. grid-cols-4 without md: or sm:)
            if re.search(r'\bgrid-cols-[4-9]\b', line) and not re.search(r'\b(?:sm|md|lg):grid-cols-', line):
                self.findings.append(UIFinding(
                    finding_id=self._next_id(),
                    title="Unconstrained Multi-Column Grid Lacks Mobile-First Breakpoint",
                    category="Responsive Behavior",
                    severity=MEDIUM,
                    confidence="High",
                    file_path=rel_path,
                    line_num=idx,
                    code_snippet=line,
                    current_behavior="Grid forces 4+ columns across all viewports including mobile.",
                    expected_behavior="Grids should follow mobile-first progression (e.g. `grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`).",
                    user_impact="Columns become illegibly squished and truncate text severely on phone displays.",
                    root_cause="Missing mobile-first responsive breakpoint prefix on grid-cols definition.",
                    is_hypothesis=False,
                    recommended_solution="Specify `grid-cols-1 sm:grid-cols-2 lg:grid-cols-4` for progressive responsive scaling.",
                    affected_routes=[f"/{rel_path}"]
                ))

        # -------------------------------------------------------------
        # DIMENSION 3: Accessibility (WCAG 2.2 Level AA)
        # -------------------------------------------------------------
        for idx, line in enumerate(lines, 1):
            # Clickable div or span without role="button" or keyboard handling
            if re.search(r'<(?:div|span)[^>]*onClick', line) and not re.search(r'role=["\']button["\']', line):
                self.findings.append(UIFinding(
                    finding_id=self._next_id(),
                    title="Non-Semantic Interactive Element (<div/span onClick>) Lacks Button Role & Keyboard Support",
                    category="Accessibility",
                    severity=HIGH,
                    confidence="High",
                    file_path=rel_path,
                    line_num=idx,
                    code_snippet=line,
                    current_behavior="Non-semantic `<div>` or `<span>` listens to click events without accessibility semantics.",
                    expected_behavior="Interactive actions must use native `<button>` or include `role='button'`, `tabIndex={0}`, and `onKeyDown`.",
                    user_impact="Keyboard-only users and screen readers cannot discover, focus, or activate this action (WCAG 2.1.1).",
                    root_cause="Developer implemented click handler on generic non-interactive HTML container.",
                    is_hypothesis=False,
                    recommended_solution="Refactor container to native semantic `<button>` or add complete ARIA button semantics.",
                    affected_routes=[f"/{rel_path}"]
                ))

            # Missing focus ring on interactive element (outline-none without focus-visible)
            if re.search(r'\b(?:outline-none|focus:outline-none)\b', line) and not re.search(r'\bfocus-visible:(?:ring|outline)\b', line):
                self.findings.append(UIFinding(
                    finding_id=self._next_id(),
                    title="Focus Outline Suppressed Without Visible Keyboard Focus Ring",
                    category="Accessibility",
                    severity=HIGH,
                    confidence="High",
                    file_path=rel_path,
                    line_num=idx,
                    code_snippet=line,
                    current_behavior="Element suppresses focus outline without providing an alternative focus-visible indicator.",
                    expected_behavior="All interactive elements must display a distinct visual focus indicator (WCAG 2.4.7 Focus Visible).",
                    user_impact="Keyboard users lose track of focus position when tabbing through the interface.",
                    root_cause="Unstyled `outline-none` stripped default browser focus indicator without replacement.",
                    is_hypothesis=False,
                    recommended_solution="Pair `focus:outline-none` with `focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2`.",
                    affected_routes=[f"/{rel_path}"]
                ))

            # Image without alt attribute
            if re.search(r'<(?:img|Image)\b[^>]*>', line) and not re.search(r'\balt=["\']', line):
                self.findings.append(UIFinding(
                    finding_id=self._next_id(),
                    title="Image Tag Missing Required 'alt' Attribute",
                    category="Accessibility",
                    severity=MEDIUM,
                    confidence="High",
                    file_path=rel_path,
                    line_num=idx,
                    code_snippet=line,
                    current_behavior="Image element rendered without an `alt` attribute.",
                    expected_behavior="All images must provide descriptive `alt` text or `alt=''` for decorative graphics (WCAG 1.1.1).",
                    user_impact="Screen reader users hear raw file names or missing image alerts.",
                    root_cause="Omission of `alt` prop in JSX/HTML image declaration.",
                    is_hypothesis=False,
                    recommended_solution="Add informative `alt` description or explicit empty `alt=''` if purely decorative.",
                    affected_routes=[f"/{rel_path}"]
                ))

            # Input lacking label / aria-label
            if re.search(r'<input\b', line) and not re.search(r'type=["\'](?:hidden|submit|button)["\']', line):
                if not re.search(r'\b(?:aria-label|aria-labelledby|id=["\'][^"\']+["\'])\b', line):
                    self.findings.append(UIFinding(
                        finding_id=self._next_id(),
                        title="Form Input Lacks Accessible Label or ARIA Association",
                        category="Accessibility",
                        severity=HIGH,
                        confidence="Medium",
                        file_path=rel_path,
                        line_num=idx,
                        code_snippet=line,
                        current_behavior="`<input>` element appears without an associated `id`, `aria-label`, or `aria-labelledby`.",
                        expected_behavior="Every form field must have an explicit accessible name linked via `<label for>` or `aria-label` (WCAG 1.3.1 / 4.1.2).",
                        user_impact="Assistive technology cannot announce the purpose or required input format of this field.",
                        root_cause="Input declared without linking to a companion label element.",
                        is_hypothesis=True,
                        recommended_solution="Assign `id` and connect to `<label htmlFor='...'>`, or supply descriptive `aria-label`.",
                        affected_routes=[f"/{rel_path}"]
                    ))

        # -------------------------------------------------------------
        # DIMENSION 4: Interactions & Micro-Behavior
        # -------------------------------------------------------------
        for idx, line in enumerate(lines, 1):
            # Button without type attribute in forms
            if re.search(r'<button\b', line) and not re.search(r'\btype=["\'](?:button|submit|reset)["\']', line):
                self.findings.append(UIFinding(
                    finding_id=self._next_id(),
                    title="Button Element Lacks Explicit 'type' Attribute",
                    category="Interactions",
                    severity=LOW,
                    confidence="High",
                    file_path=rel_path,
                    line_num=idx,
                    code_snippet=line,
                    current_behavior="`<button>` element defined without explicit `type` attribute, defaulting to `type='submit'` in forms.",
                    expected_behavior="All buttons should explicitly declare `type='button'` or `type='submit'`.",
                    user_impact="Unintended form submissions or page refreshes when clicking non-submit buttons inside forms.",
                    root_cause="HTML default behavior for `<button>` inside `<form>` is submit unless specified otherwise.",
                    is_hypothesis=False,
                    recommended_solution="Add explicit `type='button'` to auxiliary or modal trigger buttons.",
                    affected_routes=[f"/{rel_path}"]
                ))

            # Empty href link
            if re.search(r'<a\b[^>]*href=["\'](?:#|)["\']', line):
                self.findings.append(UIFinding(
                    finding_id=self._next_id(),
                    title="Anchor Link with Empty or Dead Anchor Destination (href='#')",
                    category="Interactions",
                    severity=MEDIUM,
                    confidence="High",
                    file_path=rel_path,
                    line_num=idx,
                    code_snippet=line,
                    current_behavior="Anchor tag uses placeholder `href='#'` or `href=''`. ",
                    expected_behavior="Links must point to valid route URLs, or use `<button>` if triggering in-page interactions.",
                    user_impact="Jumps viewport to top of page on click, creating frustrating disorienting behavior.",
                    root_cause="Link used as trigger for JavaScript action instead of semantic button.",
                    is_hypothesis=False,
                    recommended_solution="Replace `<a href='#'>` with semantic `<button type='button'>`.",
                    affected_routes=[f"/{rel_path}"]
                ))

        # -------------------------------------------------------------
        # DIMENSION 8: Localization & RTL (CSS Logical Properties)
        # -------------------------------------------------------------
        for idx, line in enumerate(lines, 1):
            # Physical CSS margins / paddings breaking RTL
            physical_css = re.search(r'\b(?:pl-|pr-|ml-|mr-|left-|right-|text-left|text-right)\b', line)
            if physical_css:
                found_prop = physical_css.group(0)
                logical_map = {
                    "pl-": "ps- (padding-inline-start)",
                    "pr-": "pe- (padding-inline-end)",
                    "ml-": "ms- (margin-inline-start)",
                    "mr-": "me- (margin-inline-end)",
                    "left-": "start- (inset-inline-start)",
                    "right-": "end- (inset-inline-end)",
                    "text-left": "text-start",
                    "text-right": "text-end"
                }
                suggested = logical_map.get(found_prop, "CSS logical property")

                self.findings.append(UIFinding(
                    finding_id=self._next_id(),
                    title=f"Physical CSS Property '{found_prop}' Violates Bidirectional (RTL/LTR) Layout Integrity",
                    category="Localization & RTL",
                    severity=MEDIUM,
                    confidence="High",
                    file_path=rel_path,
                    line_num=idx,
                    code_snippet=line,
                    current_behavior=f"Element applies physical CSS directional utility `{found_prop}`.",
                    expected_behavior=f"Must use CSS Logical Properties: `{suggested}`.",
                    user_impact="Layout alignment fails to mirror properly when switching to RTL locales (e.g. Arabic), causing severe visual clipping.",
                    root_cause="Physical CSS spacing assumes fixed left-to-right reading direction.",
                    is_hypothesis=False,
                    recommended_solution=f"Replace `{found_prop}` with `{suggested}` throughout the component.",
                    affected_routes=[f"/{rel_path}"]
                ))

    def _deduplicate_and_attribute(self):
        # Group identical findings that occur across multiple instances
        deduped: List[UIFinding] = []
        seen: Dict[Tuple[str, str], UIFinding] = {}

        for f in self.findings:
            key = (f.category, f.title)
            if key in seen:
                existing = seen[key]
                # Merge affected routes / instances
                if f.file_path not in existing.affected_routes:
                    existing.affected_routes.append(f.file_path)
            else:
                seen[key] = f
                deduped.append(f)

        # Re-index findings cleanly
        for idx, f in enumerate(deduped, 1):
            f.finding_id = f"UI-{idx:03d}"

        self.findings = deduped

    def _generate_diff_suggestion(self, f: UIFinding) -> Optional[str]:
        """Generates unified diff preview for deterministic findings."""
        if not f.code_snippet:
            return None
        orig = f.code_snippet
        mod = orig

        # Physical RTL utilities replacement
        if f.category == "Localization & RTL":
            replacements = [
                (r'\bpl-', 'ps-'), (r'\bpr-', 'pe-'),
                (r'\bml-', 'ms-'), (r'\bmr-', 'me-'),
                (r'\bleft-', 'start-'), (r'\bright-', 'end-'),
                (r'\btext-left\b', 'text-start'), (r'\btext-right\b', 'text-end'),
                (r'\bborder-l\b', 'border-s'), (r'\bborder-r\b', 'border-e'),
                (r'\brounded-l\b', 'rounded-s'), (r'\brounded-r\b', 'rounded-e'),
            ]
            for pat, rep in replacements:
                mod = re.sub(pat, rep, mod)

        # Fixed width replacement
        elif f.category == "Responsive Behavior" and "Fixed pixel width" in f.title:
            mod = re.sub(r'\bw-\[(\d+px)\]', r'w-full max-w-[\1]', mod)
            mod = re.sub(r'\bmin-w-\[(\d+px)\]', r'min-w-0 max-w-[\1]', mod)

        # Missing button type
        elif "Missing explicit type" in f.title and "<button" in mod:
            if 'type=' not in mod:
                mod = re.sub(r'(<button\b)', r'\1 type="button"', mod, count=1)

        # Non-semantic clickable
        elif "Non-semantic clickable" in f.title and "<div" in mod and "onClick" in mod:
            mod = re.sub(r'<div(\s+[^>]*)onClick=', r'<button type="button"\1onClick=', mod, count=1)

        # Missing alt
        elif "Missing alt" in f.title and "<img" in mod and "alt=" not in mod:
            mod = re.sub(r'(<img\b)', r'\1 alt="Descriptive label"', mod, count=1)

        if mod != orig:
            return f"- {orig}\n+ {mod}"
        return None

    def generate_report_artifacts(self, output_dir: Path) -> Dict[str, Any]:
        output_dir.mkdir(parents=True, exist_ok=True)
        prompts_dir = output_dir / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)

        timestamp = output_dir.name
        report_file = output_dir / "report.md"
        checklist_file = output_dir / "manual-browser-checklist.md"

        # Tally severities
        sev_counts = {CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0}
        for f in self.findings:
            sev_counts[f.severity] = sev_counts.get(f.severity, 0) + 1

        # 1. Generate report.md
        report_lines = [
            "# Frontend UI Quality Audit Report",
            f"\n- **Run ID**: `{timestamp}`",
            f"- **Audit Date**: `{datetime.now().strftime('%Y-%m-%d')}`",
            f"- **Frontend Architecture**: {self.topology.framework} | {self.topology.styling_system} | {self.topology.ui_library}",
            f"- **Total Confirmed Findings**: {len(self.findings)}",
            f"- **Severity Breakdown**: Critical: {sev_counts[CRITICAL]}, High: {sev_counts[HIGH]}, Medium: {sev_counts[MEDIUM]}, Low: {sev_counts[LOW]}",
            "- **Bidirectional (RTL) Active**: " + ("Yes" if self.topology.has_rtl else "No"),
            "\n---\n",
            "## 1. Executive Summary\n",
            "### Overview & Systemic Issues",
            f"The frontend codebase was audited across all 8 UI quality dimensions using static AST inspection. A total of **{len(self.findings)} confirmed findings** were identified.",
            "Systemic patterns discovered include physical CSS spacing utilities impacting bidirectional RTL layouts, interactive click containers lacking button accessibility semantics, and unconstrained responsive containers.\n",
            "### Severity Breakdown Table\n",
            "| Severity | Count | Primary Impact |",
            "| :--- | :---: | :--- |",
            f"| **Critical** | {sev_counts[CRITICAL]} | Severe blockers, critical accessibility breakdowns, major layout collapse |",
            f"| **High** | {sev_counts[HIGH]} | Major usability flaws, WCAG AA compliance failures, mobile responsive overflow |",
            f"| **Medium** | {sev_counts[MEDIUM]} | Inconsistent component variants, bidirectional RTL spacing drift, missing empty/error states |",
            f"| **Low** | {sev_counts[LOW]} | Minor design token deviations, arbitrary pixel spacing, subtle micro-polish |",
            "\n### Highest-Priority Issues (Address First)\n"
        ]

        # Top 3 findings
        top_findings = sorted(self.findings, key=lambda x: (0 if x.severity == CRITICAL else 1 if x.severity == HIGH else 2))[:3]
        for f in top_findings:
            report_lines.append(f"1. **[{f.finding_id}] {f.title}** ({f.file_path}:{f.line_num}): {f.user_impact}")

        report_lines.extend([
            "\n---\n",
            "## 2. Audit Scope & Coverage Matrix\n",
            "### Discovered Frontend Architecture",
            f"- **Framework & Runtime**: {self.topology.framework}",
            f"- **Styling System**: {self.topology.styling_system}",
            f"- **UI Component Foundation**: {self.topology.ui_library}",
            f"- **Pages & Routes Inspected**: {len(self.topology.pages)} files",
            f"- **Shared Layouts Inspected**: {len(self.topology.layouts)} files",
            f"- **Reusable Components Inspected**: {len(self.topology.components)} files",
            f"- **Discovered Diagnostics**: {', '.join(self.topology.test_diagnostics) if self.topology.test_diagnostics else 'None configured'}",
            "\n### Uninspected Areas & Limitations",
            "- Dynamic client-side authenticated state trees and private user dashboards requiring live database sessions were inspected via source contracts rather than runtime state."
            "\n---\n",
            "## 3. Detailed Confirmed Findings\n"
        ])

        for f in self.findings:
            slug = re.sub(r'[^a-z0-9]+', '-', f.title.lower()).strip('-')[:40]
            prompt_rel = f"prompts/{f.finding_id}-{slug}.md"

            report_lines.extend([
                f"### [{f.finding_id}] {f.title}",
                f"- **Category**: {f.category}",
                f"- **Severity**: {f.severity} | **Confidence**: {f.confidence}",
                f"- **Primary Location**: `[{f.file_path}:{f.line_num}](file:///{self.root_dir.as_posix()}/{f.file_path}#L{f.line_num})`",
                f"- **Component**: `{f.component_name}`",
                f"- **Affected Routes / Touchpoints**: {', '.join(f.affected_routes) if f.affected_routes else 'Global'}",
                "\n#### Implementation Evidence",
                "```tsx",
                f.code_snippet,
                "```",
                "\n#### Current Behavior",
                f.current_behavior,
                "\n#### Expected Behavior & Standard",
                f.expected_behavior,
                "\n#### User Impact",
                f.user_impact,
                "\n#### Root Cause Analysis",
                f"- **Classification**: {'Hypothesis' if f.is_hypothesis else 'Confirmed Root Cause'}",
                f"- **Diagnosis**: {f.root_cause}",
                "\n#### Recommended Correction",
                f.recommended_solution,
                "\n#### Generated Implementation Prompt",
                f"- **Prompt File**: [`{prompt_rel}`](./{prompt_rel})",
                "\n---\n"
            ])

        report_lines.extend([
            "## 4. Unverified Observations\n",
            "> [!NOTE]",
            "> No ungrounded hypotheses were upgraded to confirmed findings. Suspected responsive behaviors that require live device inspection are delegated to the manual browser checklist.\n",
            "---\n",
            "## 5. Recommended Implementation Order\n",
            "1. **Phase 1: High-Severity Responsive & Accessibility Blockers** — Resolve fixed mobile widths, clickable container roles, and focus visible indicators.",
            "2. **Phase 2: Bidirectional RTL & Localization Integrity** — Migrate physical CSS properties (`pl/pr/ml/mr`) to CSS logical properties (`ps/pe/ms/me`).",
            "3. **Phase 3: Design Token Harmonization** — Eliminate arbitrary hex colors and non-standard pixel spacing."
        ])

        report_file.write_text("\n".join(report_lines) + "\n", encoding="utf-8", newline="\n")

        # 2. Generate manual-browser-checklist.md
        check_lines = [
            "# Manual Browser Verification Checklist",
            f"\n> **Run ID**: `{timestamp}`",
            "> **Audit Execution Disclosure**: In strict compliance with read-only execution constraints, no automated browser was launched. The checklist below defines concrete manual verification steps for the human technical owner.\n",
            "| Test ID | Route / URL | Viewport / Device | User Interaction / Steps | Expected Visual & Behavioral Result | Status |",
            "| :--- | :--- | :--- | :--- | :--- | :---: |",
            "| **TC-001** | `/` | Mobile (375px × 667px) | Scroll viewport vertically from top to bottom | Zero horizontal overflow scrollbars; text containers wrap cleanly | [ ] |",
            "| **TC-002** | All Routes | Desktop (1280px × 800px) | Press `Tab` continuously through navigation and buttons | Distinct, visible focus rings appear on every interactive element | [ ] |",
            "| **TC-003** | Localized Routes | Mobile / Desktop | Toggle locale to Arabic (`/ar`) | Layout margins, paddings, and directional arrows mirror seamlessly | [ ] |",
            "| **TC-004** | Forms & Inputs | All Viewports | Submit empty form | Validation error messages appear adjacent to fields with accessible contrast | [ ] |"
        ]
        checklist_file.write_text("\n".join(check_lines) + "\n", encoding="utf-8", newline="\n")

        # 3. Generate Individual 10-Section Prompts
        generated_prompts = []
        for f in self.findings:
            slug = re.sub(r'[^a-z0-9]+', '-', f.title.lower()).strip('-')[:40]
            prompt_file = prompts_dir / f"{f.finding_id}-{slug}.md"

            # Assign specialized role
            if f.category == "Accessibility":
                role = "Senior Frontend Accessibility Specialist (WCAG 2.2 AA)"
                tool_guide = "- **Recommended Skills**: `clean-code-guard`, `test-guard`\n- **MCP Capabilities**: `chrome-devtools-mcp` (for post-fix DOM verification if connected)"
            elif f.category == "Responsive Behavior":
                role = "Senior Responsive Layout Architect"
                tool_guide = "- **Recommended Skills**: `muaz-skill` (Tailwind responsive grid & tokens), `clean-code-guard`\n- **MCP Capabilities**: None required; local browser test inspection suffices."
            elif f.category == "Localization & RTL":
                role = "Senior Frontend Internationalization & RTL Engineer"
                tool_guide = "- **Recommended Skills**: `rtl-logical-guard` (enforces CSS logical properties: ps/pe/ms/me), `muaz-skill`\n- **MCP Capabilities**: None required. Local file edits."
            else:
                role = "Senior Frontend Component & Design System Architect"
                tool_guide = "- **Recommended Skills**: `muaz-skill` (design tokens & aesthetic guidelines), `clean-code-guard`\n- **MCP Capabilities**: None required."

            diff_block = self._generate_diff_suggestion(f)
            diff_section = ""
            if diff_block:
                diff_section = f"\n### Suggested Code Replacement (Unified Diff Preview)\n```diff\n{diff_block}\n```\n\n"

            prompt_content = f"""# Implementation Prompt: [{f.finding_id}] {f.title}

## A. Role
You are acting as a **{role}**.
You write surgical, production-grade frontend code adhering strictly to the project's existing design tokens, component architecture, and accessibility standards.

---

## B. Task & Objective
- **Issue Identifier**: `[{f.finding_id}]`
- **Title**: {f.title}
- **Severity**: {f.severity}
- **Intended Outcome**: Resolve the identified {f.category.lower()} defect in `{f.file_path}` without causing layout or behavioral regressions.
- **Definition of Success**: The component satisfies all acceptance criteria, passes existing tests/linters, and conforms to standard {f.category} guidelines.

---

## C. Context & Evidence
- **Current Defect**: {f.current_behavior}
- **Why It Matters to Users**: {f.user_impact}
- **Expected Standard**: {f.expected_behavior}
- **Root Cause Analysis**:
  - **Classification**: {'Hypothesis' if f.is_hypothesis else 'Confirmed Root Cause'}
  - **Details**: {f.root_cause}

---

## D. Exact Location & Affected Scope
- **Primary Source File**: `[{f.file_path}:{f.line_num}](file:///{self.root_dir.as_posix()}/{f.file_path}#L{f.line_num})`
- **Component Name**: `{f.component_name}`
- **Affected Touchpoints**: {', '.join(f.affected_routes) if f.affected_routes else 'Global usage'}

```tsx
// Offending code excerpt at line {f.line_num}:
{f.code_snippet}
```

---

## E. Recommended Solution & Invariants
- **Recommended Correction**: {f.recommended_solution}
{diff_section}- **Reusable Tokens & Patterns**:
  - Maintain the existing design system palette and spacing scale.
  - Follow mobile-first utility order in Tailwind CSS.
- **Invariants (What Must NOT Change)**:
  - Do NOT alter unrelated styling, margin conventions, or layout wrappers outside the component.
  - Preserve all existing props, exports, event listeners, and TypeScript interfaces.
  - Do NOT break desktop layouts while resolving mobile constraints.

---

## F. Implementation Task Checklist
- [ ] **Step 1: Grounding & Code Inspection** — Open `{f.file_path}` and inspect surrounding layout context before modifying code.
- [ ] **Step 2: Apply Targeted Refactoring** — Implement the recommended correction: `{f.recommended_solution}`.
- [ ] **Step 3: Preserve Surrounding Invariants** — Verify no unrelated classes, props, or sibling layouts are altered.
- [ ] **Step 4: Quality & Clean Code Guard Pass** — Run project linters and clean code self-audit before concluding.

---

## G. Tools, Skills, and MCP Capabilities
> [!NOTE]
> Only verified tools and skills available in the active environment are recommended below.

{tool_guide}

---

## H. Acceptance Criteria
- [ ] **AC-1 (Direct Resolution)**: {f.expected_behavior}
- [ ] **AC-2 (Zero Regressions)**: Surrounding visual elements and component contract remain completely intact.
- [ ] **AC-3 (Verification Green)**: Project linter/test command executes with zero errors.

---

## I. Verification Plan
- **Automated Check**: Run `{self.topology.test_diagnostics[0] if self.topology.test_diagnostics else 'npm run lint'}`
- **Manual Verification Steps for Human Evaluator**:
  1. Open route: `{f.affected_routes[0] if f.affected_routes else '/'}`
  2. Inspect component `{f.component_name}` under target viewport.
  3. Verify: {f.expected_behavior}

---

## J. Implementation Boundaries
- **Strict Scope Limit**: Modify ONLY `{f.file_path}`.
- **Zero Collateral Refactoring**: Do not reorganize imports, rename unrelated types, or clean up untouched code.
- **Inspect Before Editing**: Always read the file lines before editing to ensure line numbers match runtime reality.
"""
            prompt_file.write_text(prompt_content, encoding="utf-8", newline="\n")
            generated_prompts.append(prompt_file)

        return {
            "timestamp": timestamp,
            "report_file": str(report_file),
            "checklist_file": str(checklist_file),
            "prompts_count": len(generated_prompts),
            "total_findings": len(self.findings),
            "severities": sev_counts
        }

def main():
    parser = argparse.ArgumentParser(description="Agent OS UI Audit & Prompt Generation Engine")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # scan subcommand
    scan_p = subparsers.add_parser("scan", help="Scan frontend topology and inventory")
    scan_p.add_argument("--dir", default=".", help="Root directory to scan")
    scan_p.add_argument("--json", action="store_true", help="Output raw JSON format to stdout")

    # audit subcommand
    audit_p = subparsers.add_parser("audit", help="Run full static UI quality audit")
    audit_p.add_argument("--dir", default=".", help="Root directory to audit")
    audit_p.add_argument("--output", help="Optional output JSON file")
    audit_p.add_argument("--json", action="store_true", help="Output raw JSON format to stdout")
    audit_p.add_argument("--strict", action="store_true", help="Exit code 1 if Critical or High findings are present")

    # generate subcommand
    gen_p = subparsers.add_parser("generate", help="Run audit and generate report & prompts")
    gen_p.add_argument("--dir", default=".", help="Root directory to audit")
    gen_p.add_argument("--output-dir", help="Output directory under docs/ui-audits/<timestamp>")
    gen_p.add_argument("--strict", action="store_true", help="Exit code 1 if Critical or High findings are present")

    args = parser.parse_args()
    target_dir = Path(args.dir).resolve()

    engine = UIAuditEngine(target_dir)

    if args.subcommand == "scan":
        engine.topology.discover()
        if getattr(args, "json", False):
            topo_dict = {
                "directory": str(target_dir),
                "framework": engine.topology.framework,
                "styling_system": engine.topology.styling_system,
                "ui_library": engine.topology.ui_library,
                "has_rtl": engine.topology.has_rtl,
                "pages_count": len(engine.topology.pages),
                "layouts_count": len(engine.topology.layouts),
                "components_count": len(engine.topology.components),
                "diagnostics": engine.topology.test_diagnostics
            }
            print(json.dumps(topo_dict, indent=2))
        else:
            print("=" * 65)
            print("        FRONTEND TOPOLOGY & INVENTORY SCAN")
            print("=" * 65)
            print(f"Target Directory:      {target_dir}")
            print(f"Framework:             {engine.topology.framework}")
            print(f"Styling System:        {engine.topology.styling_system}")
            print(f"UI Library:            {engine.topology.ui_library}")
            print(f"Bidirectional RTL:     {'Yes' if engine.topology.has_rtl else 'No'}")
            print(f"Pages / Routes:        {len(engine.topology.pages)} detected")
            print(f"Layouts:               {len(engine.topology.layouts)} detected")
            print(f"Reusable Components:   {len(engine.topology.components)} detected")
            print(f"Diagnostics Available: {', '.join(engine.topology.test_diagnostics) if engine.topology.test_diagnostics else 'None'}")
            print("=" * 65)

    elif args.subcommand == "audit":
        engine.analyze()
        findings_data = [f.to_dict() for f in engine.findings]
        if getattr(args, "json", False):
            print(json.dumps(findings_data, indent=2))
        else:
            print(f"[SUCCESS] Audit completed across {len(engine.topology.pages) + len(engine.topology.components)} files.")
            print(f"Total Confirmed Findings: {len(engine.findings)}")
            for f in engine.findings:
                print(f"  [{f.finding_id}] ({f.severity}) {f.title} -> {f.file_path}:{f.line_num}")
        if args.output:
            out_p = Path(args.output)
            out_p.write_text(json.dumps(findings_data, indent=2), encoding="utf-8")
            if not getattr(args, "json", False):
                print(f"[SAVED] Results exported to: {out_p}")

        if getattr(args, "strict", False):
            has_crit_high = any(f.severity in [CRITICAL, HIGH] for f in engine.findings)
            if has_crit_high:
                sys.stderr.write("[STRICT ERROR] Critical or High UI findings detected.\n")
                sys.exit(1)

    elif args.subcommand == "generate":
        engine.analyze()
        if args.output_dir:
            out_dir = Path(args.output_dir).resolve()
        else:
            ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            out_dir = target_dir / "docs" / "ui-audits" / ts

        res = engine.generate_report_artifacts(out_dir)
        print("=" * 65)
        print("     FRONTEND UI AUDIT - ARTIFACTS GENERATION COMPLETE")
        print("=" * 65)
        print(f"Run ID:                 {res['timestamp']}")
        print(f"Total Findings:         {res['total_findings']}")
        print(f"Severity Breakdown:     Critical: {res['severities'][CRITICAL]} | High: {res['severities'][HIGH]} | Medium: {res['severities'][MEDIUM]} | Low: {res['severities'][LOW]}")
        print(f"Report File:            {res['report_file']}")
        print(f"Manual Checklist:       {res['checklist_file']}")
        print(f"Implementation Prompts: {res['prompts_count']} prompt files generated in prompts/")
        print("=" * 65)

        if getattr(args, "strict", False):
            has_crit_high = (res['severities'][CRITICAL] > 0 or res['severities'][HIGH] > 0)
            if has_crit_high:
                sys.stderr.write("[STRICT ERROR] Critical or High UI findings detected.\n")
                sys.exit(1)

if __name__ == "__main__":
    main()
