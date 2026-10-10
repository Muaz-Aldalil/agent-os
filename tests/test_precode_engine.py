#!/usr/bin/env python3
"""
tests/test_precode_engine.py
Unit tests for the Agent OS 6 Pre-Coding Pillars Engine (scripts/precode_engine.py).
"""

import unittest
import tempfile
import shutil
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from precode_engine import init_precode, audit_precode, CANONICAL_DOCS
from skill_router import resolve_task_routing


class TestPrecodeEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="agent_os_precode_test_"))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_creates_all_6_documents(self):
        result = init_precode(self.temp_dir, "NovaStore")
        self.assertTrue(result["success"])
        self.assertEqual(len(result["created_files"]), 6)
        
        for doc in CANONICAL_DOCS:
            doc_path = self.temp_dir / doc
            self.assertTrue(doc_path.is_file(), f"Missing canonical doc: {doc}")
            content = doc_path.read_text(encoding="utf-8")
            self.assertIn("NovaStore", content)

    def test_audit_missing_directory(self):
        non_existent = self.temp_dir / "does_not_exist"
        result = audit_precode(non_existent)
        self.assertFalse(result["passed"])
        self.assertEqual(result["score"], 0.0)

    def test_audit_missing_files(self):
        init_precode(self.temp_dir, "TestApp")
        # Remove two files
        (self.temp_dir / "03-APP_FLOW.md").unlink()
        (self.temp_dir / "05-BACKEND_SCHEMA.md").unlink()

        result = audit_precode(self.temp_dir)
        self.assertFalse(result["passed"])
        self.assertLess(result["score"], 100.0)
        self.assertTrue(any("Missing: 03-APP_FLOW.md" in c["message"] for c in result["checks"]))

    def test_audit_flags_unfilled_placeholders(self):
        init_precode(self.temp_dir, "TestApp")
        # Template initially has placeholder HTML comments
        result = audit_precode(self.temp_dir)
        # Check 2 should detect unfilled comments
        check2 = next(c for c in result["checks"] if "Placeholder Markers" in c["name"])
        self.assertFalse(check2["passed"])

    def test_audit_requires_5_ui_states_in_app_flow(self):
        init_precode(self.temp_dir, "TestApp")
        # Overwrite APP_FLOW with flowchart but missing Empty and Loading states
        flow_path = self.temp_dir / "03-APP_FLOW.md"
        flow_path.write_text("""# App Flow
```mermaid
flowchart TD
    A --> B
```
Idle and Success states are here, but others missing.
""", encoding="utf-8")
        result = audit_precode(self.temp_dir)
        check5 = next(c for c in result["checks"] if "App Flow" in c["name"])
        self.assertFalse(check5["passed"])

    def test_audit_100_percent_clearance_when_fully_populated(self):
        init_precode(self.temp_dir, "AcmePortal")
        
        # Populate 01-PRD.md cleanly
        (self.temp_dir / "01-PRD.md").write_text("""# Product Requirements Document: AcmePortal
## 1. Executive Summary
AcmePortal is an autonomous customer portal.
## 2. Target Personas & User Journeys
Primary Persona: Alice the Operations Manager.
## 3. Functional Requirements
### P0 (Must Have)
- [ ] FR-001: Customer Auth
- [ ] FR-002: Document Upload
## 4. Formal User Stories & Acceptance Criteria
### User Story US-01: Login
**As a** customer, **I want to** log in, **so that** I see my account.
**Acceptance Criteria (Given / When / Then)**:
- Given an active user
- When valid credentials entered
- Then redirect to dashboard
## 5. Explicitly Out of Scope
- International wire payments
## 6. Non-Functional Requirements
- WCAG AA accessibility.
""", encoding="utf-8")

        # Populate 02-TRD.md cleanly
        (self.temp_dir / "02-TRD.md").write_text("""# Technical Requirements Document: AcmePortal
## 1. System Architecture
Next.js 15 App Router with Server Components.
## 2. Technology Stack Selection
Frontend: Next.js 15, Tailwind CSS v4.
Backend: Next.js Server Actions.
Database: PostgreSQL 16 with Prisma ORM.
Security: Anti-IDOR server-side derivation, Zod input sanitization.
## 3. Third-Party Integrations
Stripe, Resend.
## 4. Security Architecture & Boundary Invariants
Authentication derivation from verified session; CSP headers.
## 5. Performance Budgets
LCP <= 2.5s, INP <= 200ms.
""", encoding="utf-8")

        # Populate 03-APP_FLOW.md cleanly
        (self.temp_dir / "03-APP_FLOW.md").write_text("""# App Flow: AcmePortal
## 1. Route Map
/ -> /dashboard
## 2. Primary User Journey Flowcharts
```mermaid
flowchart TD
    A[Start] --> B[Dashboard]
```
## 3. The 5-State UI Matrix
Every view handles Idle, Loading, Success, Error, and Empty states.
| View | Idle | Loading | Success | Error | Empty |
| Dashboard | Ready | Skeleton | Rendered | Alert 422 | No items yet |
## 4. Session & Auth Flow
Tokens refreshed automatically.
## 5. Edge Handling
Optimistic UI rollback.
""", encoding="utf-8")

        # Populate 04-DESIGN_BRIEF.md cleanly
        (self.temp_dir / "04-DESIGN_BRIEF.md").write_text("""# Design Brief: AcmePortal
## 1. Brand Identity & Visual Aesthetic
Minimalist Modern enterprise dashboard.
## 2. Color Palette & The 60-30-10 Rule
60% Dominant Background: #0f172a (Dark)
30% Structural Surface: #1e293b
10% Accent CTA: #3b82f6
Semantic tokens: Success emerald, Error rose.
## 3. Typography Hierarchy
Font family: Inter for display and body, JetBrains Mono for code.
Scale: Display H1 36px, Page H2 24px, Body 16px.
## 4. Spacing, Elevation & Component Tokens
rounded-lg (8px), shadow-sm, focus rings, minimum 44x44px tap target.
## 5. Bi-directional (LTR / RTL) Layout Integrity
Mandatory CSS Logical Properties: ms-4, pe-6, text-start, start-0.
""", encoding="utf-8")

        # Populate 05-BACKEND_SCHEMA.md cleanly
        (self.temp_dir / "05-BACKEND_SCHEMA.md").write_text("""# Backend Schema: AcmePortal
## 1. Storage Architecture
PostgreSQL 16 relational database.
## 2. Entity Relationship Diagram (ERD)
```mermaid
erDiagram
    ORGANIZATION ||--o{ USER : "employs"
    ORGANIZATION {
        uuid id PK
        string name
    }
    USER {
        uuid id PK
        uuid organization_id FK
        string email UK
    }
```
## 3. Schema DDL
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    email VARCHAR(255) NOT NULL UNIQUE
);
```
## 4. Indexing Strategy
Index on organization_id and email.
## 5. Data Integrity
ON DELETE CASCADE for parent organization deletion.
""", encoding="utf-8")

        # Populate 06-IMPLEMENTATION_PLAN.md cleanly
        (self.temp_dir / "06-IMPLEMENTATION_PLAN.md").write_text("""# Implementation Plan: AcmePortal
## 1. Execution Dependency Graph
Foundations -> Domain -> UI -> Feature -> Verification
## 2. Phase 1 — Foundations
- [ ] Task 1.1: Run schema migrations
- [ ] Task 1.2: Environment configuration
## 3. Phase 2 — Core Domain
- [ ] Task 2.1: Server-side authentication
- [ ] Task 2.2: Zod validation schemas
## 4. Phase 3 — UI Shell
- [ ] Task 3.1: Tailwind tokens and RTL logical properties
- [ ] Task 3.2: Reusable components
## 5. Phase 4 — Feature Workflows
- [ ] Task 4.1: User journey with 5 UI states
## 6. Phase 5 — Quality Gates
- [ ] Task 5.1: Run full unit test battery
""", encoding="utf-8")

        # Run audit
        result = audit_precode(self.temp_dir)
        self.assertTrue(result["passed"], f"Audit failed: {result['findings']}")
        self.assertEqual(result["score"], 100.0)
        self.assertEqual(result["passed_checks"], 8)
        self.assertEqual(result["total_checks"], 8)

    def test_skill_router_routes_precode_tasks(self):
        routing = resolve_task_routing("Write the PRD, TRD, and app flow for our new dashboard")
        self.assertIn("WEB_PRECODE", routing["domains"])
        self.assertIn("web-precode", routing["implementation_skills"])
        self.assertIn("agent_os precode audit", routing["completion_guards"])


if __name__ == "__main__":
    unittest.main()
