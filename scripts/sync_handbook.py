#!/usr/bin/env python3
"""
Agent OS Learning Platform & Handbook Sync Engine (`sync_handbook.py`).
Synchronizes `SKILL_INDEX.json` (85 custom skills + 19 MCP servers + 36 plugin skills)
and the 28 Unified CLI Tools into `learning-platform/src/data/skills-registry.json`
with bilingual EN/AR User Request Domains, explanations, ready copy-paste commands,
and 2-4 word truncated table summaries, then syncs compiled Astro static output
(`learning-platform/dist/index.html`) to root `handbook.html` and GitHub Pages.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SKILL_INDEX_PATH = WORKSPACE_ROOT / "SKILL_INDEX.json"
PLATFORM_DIR = WORKSPACE_ROOT / "learning-platform"
REGISTRY_OUT_PATH = PLATFORM_DIR / "src" / "data" / "skills-registry.json"
DIST_HTML_PATH = PLATFORM_DIR / "dist" / "index.html"
ROOT_HANDBOOK_PATH = WORKSPACE_ROOT / "handbook.html"

CATEGORY_AR_MAP: Dict[str, str] = {
    "Beginner Situation Combos (All-in-One)": "حزم المهام الشاملة (أمر واحد)",
    "Core Architecture & Workflow": "الهندسة الأساسية وسير العمل",
    "Specification-Driven Development (Spec-Kit)": "التطوير الموجه بالمواصفات (Spec-Kit)",
    "Frontend & User Experience": "الواجهة الأمامية وتجربة المستخدم",
    "Backend & Data Systems": "الواجهة الخلفية وقواعد البيانات",
    "Simplicity & Anti-Bloat (Ponytail)": "البساطة ومنع التعقيد (Ponytail)",
    "Quality & Security Guards": "حراس الجودة والأمان",
    "WordPress & WooCommerce": "ووردبريس وووكرومرس",
    "Testing & QA Automation": "الاختبارات وضمان الجودة",
    "DevOps, Delegation & Utilities": "النشر والتفويض والأدوات",
    "Google Stitch Design & UI Suite": "جناح تصميم Google Stitch والواجهات",
}

ROLE_AR_MAP: Dict[str, str] = {
    "master-command": "أمر شامل",
    "orchestrator": "منسق رئيسي",
    "domain-skill": "مهارة تخصصية",
    "guard": "حارس جودة وأمان",
    "phase-skill": "مرحلة مواصفات",
    "sub-module": "وحدة فرعية",
    "utility": "أداة مساندة",
}

PHASE_AR_MAP: Dict[str, str] = {
    "THINK": "تفكير واستجواب",
    "PLAN": "تخطيط ومواصفات",
    "BUILD": "بناء وتنفيذ",
    "VERIFY": "فحص ومراجعة",
}

# Comprehensive Domain + Arabic Summary + Ready Copy-Paste Prompts for all 85 Skills
SKILL_CATALOG_ENRICHMENT: Dict[str, Dict[str, str]] = {
    "start-project": {
        "short": "بناء مشروع جديد...",
        "full": "الأمر الشامل لبدء مشروع جديد من الصفر لأي تقنية: يشغل استجواب المتطلبات الذكي، ويكتب الوثائق الهندسية الست، وينفذ الواجهة والخلفية وقاعدة البيانات مع الحراس.",
        "domainEn": "Starting a brand-new web app, SaaS, or CMS platform from zero in any stack",
        "domainAr": "بدء مشروع تطبيق ويب أو منصة أو لوحة تحكم جديدة من الصفر بأي تقنية",
        "promptEn": "/start-project Build a bilingual (AR/EN) clinic appointment & billing SaaS with Admin, Doctor, and Receptionist roles.",
        "promptAr": "/start-project ابن منصة ثنائية اللغة (عربي/إنجليزي) لإدارة مواعيد وفواتير العيادات بصلاحيات مدير وطبيب وموظف استقبال."
    },
    "plan-daily": {
        "short": "تخطيط عمل اليوم...",
        "full": "مخطط الجلسة اليومي ومصنع تطوير المهارات: يفحص حالة المشروع ويحدد مهمة أساسية واحدة لليوم أو يبني مهارة وأداة جديدة بالكامل.",
        "domainEn": "Morning session triage, picking today's #1 task, or creating a new Agent OS skill",
        "domainAr": "فرز مهام الصباح، تحديد الأولوية رقم 1 لليوم، أو بناء مهارة جديدة للنظام",
        "promptEn": "/plan-daily Inspect git status, PROGRESS.md, and test health, then recommend today's #1 primary engineering focus.",
        "promptAr": "/plan-daily افحص حالة المشروع وسجل التقدم والاختبارات واقترح المهمة الهندسية الأساسية لليوم."
    },
    "smart-feature": {
        "short": "موجه الميزات الذكي...",
        "full": "يقرأ وصف الميزة بالعربية أو الإنجليزية ويختار تلقائياً أفضل مهارات الواجهة والخلفية وقاعدة البيانات والحراس ويبنيها.",
        "domainEn": "Adding any new feature when you want Agent OS to auto-detect stack and layers",
        "domainAr": "إضافة أي ميزة جديدة مع ترك النظام يكتشف التقنية والطبقات المطلوبة تلقائياً",
        "promptEn": "/smart-feature Add a customer support ticket drawer with priority tags, agent assignment, and email notifications.",
        "promptAr": "/smart-feature أضف نافذة تذاكر دعم فني مع تصنيف الأولوية وتعيين الموظف المسؤول وإشعارات البريد."
    },
    "feature-full": {
        "short": "بناء ميزة كاملة...",
        "full": "يبني ميزة متكاملة تشمل الواجهة الأمامية ولوحة التحكم والواجهة الخلفية وقاعدة البيانات مع الفحص التلقائي.",
        "domainEn": "New end-to-end feature touching Frontend UI + Backend API + Database migrations",
        "domainAr": "بناء ميزة متكاملة تشمل الواجهة الأمامية + الـ API الخلفي + جداول قاعدة البيانات",
        "promptEn": "/feature-full Create a discount coupons module with usage limits, expiry dates, admin CRUD table, and atomic checkout redemption.",
        "promptAr": "/feature-full أنشئ وحدة كوبونات خصم مع حد استخدام وتاريخ انتهاء وجدول إدارة وعملية خصم ذرية عند الدفع."
    },
    "feature-febe": {
        "short": "بناء واجهة وخلفية...",
        "full": "يبني واجهة أمامية مع نقاط النهاية الخلفية والتحقق من الصلاحيات والبيانات بدون تغييرات في هيكل قاعدة البيانات.",
        "domainEn": "New UI + Backend API, RBAC permissions, form validation, or file uploads (no new DB tables)",
        "domainAr": "بناء واجهة أمامية مع نقاط API خلفية وفحص صلاحيات أو رفع ملفات بدون جداول جديدة",
        "promptEn": "/feature-febe Add a bulk order status update action bar and RBAC-protected API endpoint with 422 validation.",
        "promptAr": "/feature-febe أضف شريط تحديث جماعي لحالة الطلبات مع نقطة نهاية API محمية بالصلاحيات والتحقق."
    },
    "feature-fe": {
        "short": "بناء واجهة أمامية...",
        "full": "يبني صفحات ومكونات الواجهة الأمامية ولوحات التحكم المتجاوبة مع دعم كامل للعربية والإنجليزية.",
        "domainEn": "New Frontend/CMS page, dashboard, responsive data table, modal, or form in any UI framework",
        "domainAr": "بناء صفحة واجهة أمامية أو لوحة تحكم أو جدول متجاوب أو نموذج بأي إطار عمل",
        "promptEn": "/feature-fe Build a vendor analytics dashboard with 3 KPI cards, collapsible category grid, and truncated payout table.",
        "promptAr": "/feature-fe ابن لوحة إحصائيات للتجار تضم 3 بطاقات مؤشرات وشبكة قابلة للطي وجدول دفعات متجاوب."
    },
    "feature-wp": {
        "short": "بناء ميزة ووردبريس...",
        "full": "يبني إضافات وقوالب وميزات ووردبريس وووكرومرس متوافقة مع HPOS ومعايير الأمان.",
        "domainEn": "Building a WordPress plugin, theme, block, or WooCommerce HPOS checkout/order feature",
        "domainAr": "بناء إضافة أو قالب ووردبريس أو ميزة متجر ووكرومرس متوافقة مع نظام HPOS",
        "promptEn": "/feature-wp Add a custom delivery time-slot selector on WooCommerce checkout saved via HPOS CRUD with nonce verification.",
        "promptAr": "/feature-wp أضف حقل اختيار وقت التوصيل في صفحة دفع ووكرومرس محفوظاً عبر دوال HPOS القياسية."
    },
    "fix-ui": {
        "short": "إصلاح مشاكل الواجهة...",
        "full": "يفحص الواجهة الأمامية بالكامل ويصلح مشاكل الجداول والأشرطة الثابتة والنماذج واتجاه النص تلقائياً.",
        "domainEn": "Fixing broken sticky navbars/sidebars, overflowing mobile tables, messy forms, or RTL alignment bugs",
        "domainAr": "إصلاح مشاكل الواجهة والأشرطة الثابتة وخروج الجداول عن شاشة الجوال وأخطاء اتجاه العربية",
        "promptEn": "/fix-ui Scan my frontend and fix the non-sticky navbar, mobile horizontal table overflow, and overlapping RTL search icon.",
        "promptAr": "/fix-ui افحص الواجهة الأمامية وأصلح ثبات الشريط العلوي وخروج الجدول على الجوال وتداخل أيقونة البحث بالعربية."
    },
    "fix-backend": {
        "short": "إصلاح أعطال الخلفية...",
        "full": "يشخص ويصلح أخطاء الواجهة الخلفية والصلاحيات ورفع الملفات واستعلامات قواعد البيانات.",
        "domainEn": "Fixing 500/422/403 API errors, broken auth/RBAC, race conditions, upload bugs, or slow N+1 queries",
        "domainAr": "إصلاح أخطاء الخادم 500/422/403 ومشاكل الصلاحيات وتضارب العمليات واستعلامات N+1 البطيئة",
        "promptEn": "/fix-backend Trace and fix the duplicate order creation race condition when a user double-clicks checkout.",
        "promptAr": "/fix-backend تتبع وأصلح مشكلة تكرار إنشاء الطلب عند ضغط المستخدم مرتين بسرعة على زر الدفع."
    },
    "check-all": {
        "short": "الفحص الشامل قبل...",
        "full": "يشغل جميع حراس الكود النظيف والاختبارات والأمان واتجاه الواجهة ومنع التعقيد في أمر واحد قبل الرفع.",
        "domainEn": "Pre-push / pre-PR quality, security, RTL, test, and anti-bloat review across all modified files",
        "domainAr": "الفحص الشامل لجودة الكود والأمان والاختبارات والعربية ومنع التعقيد قبل الرفع أو الدمج",
        "promptEn": "/check-all Audit all modified files in my working tree for security, RTL, clean code, and test quality before git push.",
        "promptAr": "/check-all افحص جميع الملفات المعدلة للتحقق من الأمان والعربية وجودة الكود والاختبارات قبل الرفع."
    },
    "save-data": {
        "short": "توفير باقة الإنترنت...",
        "full": "يقلل استهلاك بيانات الإنترنت بنسبة 75-85% عبر إيقاف التحديثات الصامتة وتفعيل التخزين المحلي والردود المختصرة.",
        "domainEn": "Working on mobile hotspot or metered internet; cutting IDE bandwidth by 75-85% and saving tokens",
        "domainAr": "العمل عبر نقطة اتصال الجوال وتقليل استهلاك الإنترنت بنسبة 75-85% مع ردود سريعة ومختصرة",
        "promptEn": "/save-data Activate low-bandwidth profile, offline package manager caching, and concise caveman lite replies.",
        "promptAr": "/save-data فعل وضع توفير بيانات الإنترنت والتخزين المحلي للحزم والردود المختصرة."
    },
    "doc-project": {
        "short": "توثيق المشروع تلقائياً...",
        "full": "يفحص الكود المصدري ويولد ملفات README والهندسة المعمارية وتوثيق الـ API بدقة وبدون حشو.",
        "domainEn": "Generating or updating verified README.md, docs/ARCHITECTURE.md, and docs/API.md from real code",
        "domainAr": "توليد أو تحديث ملفات README والهندسة المعمارية وتوثيق الـ API من الكود الفعلي",
        "promptEn": "/doc-project Scan our repository and update README.md, docs/ARCHITECTURE.md, and docs/API.md with verified paths.",
        "promptAr": "/doc-project افحص المشروع وحدث ملفات README.md وdocs/ARCHITECTURE.md وdocs/API.md بمسارات موثقة."
    },
    "intake": {
        "short": "بوابة الاستجواب الذكي...",
        "full": "بوابة الاستجواب الأولي: تفحص الكود بوضع القراءة فقط، وتبني جدول التأثير الثلاثي وقائمة عدم الحذف، وتطرح الأسئلة التفاعلية.",
        "domainEn": "Clarifying ambiguous requirements on Turn 1 with a 3-Layer Impact Map (UI + API + DB) and Do-Not-Remove lock list",
        "domainAr": "توضيح المتطلبات في بداية المهمة مع جدول التأثير الثلاثي (واجهة + خلفية + بيانات) وقائمة عناصر عدم الحذف",
        "promptEn": "/intake Inspect our checkout flow in read-only mode, map the 3-layer impact (UI/API/DB), lock existing nav links, and ask clarifying questions.",
        "promptAr": "/intake افحص مسار الدفع بوضع القراءة فقط، واعرض جدول التأثير الثلاثي وقائمة عدم الحذف، واطرح أسئلة التوضيح."
    },
    "critique": {
        "short": "المراجعة النقدية الذاتية...",
        "full": "المراجع النقدي الذاتي: يفحص مسودة الخطة أو التصميم لاكتشاف الافتراضات غير الموثقة أو حذف عناصر الواجهة بالخطأ أو المبالغة الهندسية.",
        "domainEn": "Adversarial self-review of an architecture plan, spec, or draft to catch blind spots and hidden DB/UI blast radius",
        "domainAr": "مراجعة نقدية صارمة لخطة أو مواصفات لاكتشاف الثغرات وتأثيرات قاعدة البيانات أو حذف عناصر الواجهة بالخطأ",
        "promptEn": "/critique Audit the proposed architecture plan against codebase truth, IDOR risks, 6-state UI coverage, and accidental nav removals.",
        "promptAr": "/critique راجع الخطة المقترحة نقدياً مقابل الكود الفعلي ومخاطر الصلاحيات وحالات الواجهة الست ومنع الحذف الخاطئ."
    },
    "engineering-workflow": {
        "short": "سير العمل الهندسي...",
        "full": "البروتوكول الهندسي المتكامل: التفكير النقدي، قوانين Karpathy الأربعة، تتبع السبب الجذري، والتحقق التجريبي.",
        "domainEn": "Enforcing Senior Staff Engineer discipline, critical debate, root-cause tracing, and 60-70% context handover",
        "domainAr": "تطبيق انضباط المهندس الرئيسي والتفكير النقدي وتتبع السبب الجذري وبروتوكول حفظ الجلسة",
        "promptEn": "/engineering-workflow Hold in Read-Only mode while I share 3 bug reports, challenge any risky assumptions, and wait for 'proceed'.",
        "promptAr": "/engineering-workflow ابق في وضع القراءة فقط بينما أشارك 3 ملاحظات، وناقش أي افتراضات خطرة، وانتظر كلمة proceed."
    },
    "muaz-skill": {
        "short": "مهندس التصميم والواجهات...",
        "full": "محرك هندسة التصميم والواجهات الأمامية مع 91 نمطاً بصرياً و169 لوحة ألوان وفحص التباين ومنع التصميم العشوائي.",
        "domainEn": "Designing a cohesive UI system, 60-30-10 color palette, typography hierarchy, and anti-slop frontend blueprint",
        "domainAr": "تصميم نظام واجهة متكامل ولوحة ألوان متوازنة وتسلسل خطوط ومخطط واجهة خالٍ من العشوائية",
        "promptEn": "/muaz-skill Design a fintech dashboard blueprint with WCAG AA contrast tokens, sticky shell, and bilingual AR/EN typography.",
        "promptAr": "/muaz-skill صمم مخطط لوحة تحكم مالية برموز ألوان متوافقة مع WCAG AA وهيكل ثابت وخطوط عربية وإنجليزية."
    },
    "clean-code-guard": {
        "short": "حارس الكود النظيف...",
        "full": "يراجع الكود الإنتاجي وفق مبادئ SOLID وDRY وKISS وYAGNI ويكتشف أخطاء الذكاء الاصطناعي الشائعة.",
        "domainEn": "Auditing production code for SOLID, DRY, KISS, layer boundaries, and 2+ component reusability",
        "domainAr": "فحص الكود الإنتاجي وفق مبادئ الكود النظيف وفصل الطبقات وإعادة استخدام المكونات",
        "promptEn": "/clean-code-guard Review src/components/ and src/services/ for SOLID violations, duplicated logic, and layer boundary leaks.",
        "promptAr": "/clean-code-guard راجع مجلدات المكونات والخدمات لاكتشاف تكرار الكود أو كسر حدود الطبقات المعمارية."
    },
    "test-guard": {
        "short": "حارس جودة الاختبارات...",
        "full": "يراجع كود الاختبارات لمنع الاختبارات الوهمية أو المكررة ويضمن اختبار السلوك الحقيقي.",
        "domainEn": "Reviewing unit/integration tests to eliminate tautological mocks and enforce real behavior & negative assertions",
        "domainAr": "مراجعة كود الاختبارات لمنع الاختبارات الوهمية وضمان فحص السلوك الفعلي والحالات السلبية",
        "promptEn": "/test-guard Audit our test suite in tests/ to remove over-mocked tautologies and add boundary/negative assertions.",
        "promptAr": "/test-guard راجع حزمة الاختبارات لإزالة المحاكاة الوهمية وإضافة اختبارات الحدود والحالات السلبية."
    },
    "docs-guard": {
        "short": "حارس دقة التوثيق...",
        "full": "يتحقق من تطابق كل مسار ملف ودالة ومتغير بيئة ومثال كود في ملفات التوثيق مع الكود الفعلي.",
        "domainEn": "Verifying README and API documentation against real source files to eliminate docs-vs-code drift and buzzwords",
        "domainAr": "التحقق من تطابق ملفات README وتوثيق الـ API مع الكود المصدري الفعلي وإزالة الحشو التسويقي",
        "promptEn": "/docs-guard Verify every CLI flag, endpoint, and file path in README.md and docs/API.md against the actual codebase.",
        "promptAr": "/docs-guard تحقق من وجود وصحة كل أمر ومسار ملف ونقطة نهاية مذكورة في README.md وdocs/API.md."
    },
    "rtl-logical-guard": {
        "short": "حارس العربية والاتجاه...",
        "full": "يفرض استخدام خصائص CSS المنطقية ويمنع كسر التصميم في الواجهات الثنائية اللغة.",
        "domainEn": "Eliminating physical left/right Tailwind classes and enforcing bidirectional AR/EN logical CSS properties",
        "domainAr": "استبدال كلاسات الاتجاه الفيزيائية بخصائص CSS المنطقية لضمان عمل الواجهة بالعربية والإنجليزية",
        "promptEn": "/rtl-logical-guard Scan all frontend components and replace physical ml-*/pl-*/text-left/left-* classes with logical equivalents.",
        "promptAr": "/rtl-logical-guard افحص جميع مكونات الواجهة واستبدل كلاسات الاتجاه الفيزيائية بالخصائص المنطقية."
    },
    "next-server-action-guard": {
        "short": "حارس أمان Next.js...",
        "full": "يفرض التحقق من الهوية في الخادم ومنع ثغرات IDOR وفحص البيانات بـ Zod داخل Next.js Server Actions.",
        "domainEn": "Securing Next.js App Router Server Actions and Route Handlers against IDOR, unvalidated inputs, and auth bypass",
        "domainAr": "تأمين دوال الخادم في Next.js ضد ثغرات الصلاحيات (IDOR) والبيانات غير المفحوصة وتجاوز الهوية",
        "promptEn": "/next-server-action-guard Audit all Server Actions in src/app/ for session derivation, Zod validation, and tenant ownership scoping.",
        "promptAr": "/next-server-action-guard راجع جميع دوال الخادم في Next.js للتحقق من الجلسة وفحص Zod وملكية السجلات."
    },
    "pest-security-guard": {
        "short": "حارس أمان لارافيل...",
        "full": "يفرض معايير أمان Pest 3 والأنواع الصارمة ويمنع الدوال الخطرة في تطبيقات PHP وLaravel.",
        "domainEn": "Enforcing Pest 3 architectural security presets, strict types, and RBAC checks in PHP/Laravel apps",
        "domainAr": "تطبيق فحوصات الأمان المعمارية في Pest 3 والأنواع الصارمة وفحص الصلاحيات في تطبيقات Laravel",
        "promptEn": "/pest-security-guard Audit our Laravel controllers, models, and Pest architecture tests for mass-assignment and RBAC safety.",
        "promptAr": "/pest-security-guard افحص متحكمات ونماذج لارافيل واختبارات Pest للتأكد من حماية التعيين الجماعي والصلاحيات."
    },
    "wp-guard": {
        "short": "حارس أمان ووردبريس...",
        "full": "يفرض فحص Nonce والصلاحيات والاستعلامات المحضرة وتعقيم المخرجات في قوالب وإضافات ووردبريس.",
        "domainEn": "Auditing WordPress plugins/themes for nonces, current_user_can, $wpdb->prepare, and late output escaping",
        "domainAr": "مراجعة إضافات وقوالب ووردبريس للتحقق من Nonce والصلاحيات واستعلامات SQL المحضرة وتعقيم المخرجات",
        "promptEn": "/wp-guard Review our WordPress AJAX and REST handlers for nonce checks, capability gates, and SQL injection safety.",
        "promptAr": "/wp-guard راجع معالجات AJAX وREST في ووردبريس للتحقق من Nonce والصلاحيات وحماية استعلامات SQL."
    },
    "woo-guard": {
        "short": "حارس متاجر ووكرومرس...",
        "full": "يفرض دوال CRUD المتوافقة مع HPOS وسلامة العمليات المالية والتحقق من الدفع في ووكرومرس.",
        "domainEn": "Reviewing WooCommerce extensions for HPOS compatibility, wc_get_order CRUD, and checkout money safety",
        "domainAr": "فحص إضافات ووكرومرس للتأكد من توافق HPOS واستخدام دوال الطلبات الرسمية وسلامة عمليات الدفع",
        "promptEn": "/woo-guard Audit our WooCommerce order hooks and replace any direct wp_postmeta queries with HPOS-safe CRUD methods.",
        "promptAr": "/woo-guard افحص خطافات الطلبات في ووكرومرس واستبدل أي استعلامات مباشرة بدوال HPOS القياسية."
    },
    "firebase-security-rules-auditor": {
        "short": "مدقق قواعد Firebase...",
        "full": "يفحص قواعد أمان Firestore وStorage لاكتشاف ثغرات تصعيد الصلاحيات وتجاوز الملكية وفحص الأنواع.",
        "domainEn": "Red-team auditing of Cloud Firestore & Storage security rules (firestore.rules) against privilege escalation",
        "domainAr": "فحص قواعد أمان Firestore وStorage لاكتشاف ثغرات تصعيد الصلاحيات وتجاوز ملكية البيانات",
        "promptEn": "/firebase-security-rules-auditor Audit firestore.rules for role-escalation bypasses, missing hasOnly checks, and unbounded writes.",
        "promptAr": "/firebase-security-rules-auditor افحص ملف firestore.rules لاكتشاف ثغرات تصعيد الصلاحيات أو الكتابة غير المقيدة."
    },
    "bug-hunter": {
        "short": "صائد الأعطال والثغرات...",
        "full": "وكيل استقصاء بوضع القراءة فقط يكتشف الأعطال الوظيفية والثغرات الأمنية عبر الواجهة والخلفية وحدود الاتصال.",
        "domainEn": "Deep read-only investigation to uncover hidden functional bugs, race conditions, and boundary vulnerabilities",
        "domainAr": "فحص استقصائي عميق بوضع القراءة فقط لاكتشاف الأعطال الخفية وتضارب العمليات والثغرات الأمنية",
        "promptEn": "/bug-hunter Investigate the checkout and webhook modules in read-only mode and report any functional or security defects with evidence.",
        "promptAr": "/bug-hunter افحص وحدتي الدفع والإشعارات بوضع القراءة فقط وقدم تقريراً بالأعطال أو الثغرات المدعومة بالأدلة."
    },
    "pentest": {
        "short": "اختبار الاختراق المصرح...",
        "full": "وكيل فحص أمني يختبر حدود الواجهة والـ API وقاعدة البيانات لاكتشاف ثغرات BOLA/BFLA والحقن وتجاوز الصلاحيات.",
        "domainEn": "Authorized 3-layer web penetration testing (Frontend, API, DB/RLS) for BOLA/IDOR, auth bypass, and injection",
        "domainAr": "اختبار اختراق مصرح به عبر الطبقات الثلاث (الواجهة، الـ API، قاعدة البيانات) لاكتشاف ثغرات الصلاحيات والحقن",
        "promptEn": "/pentest Run an authorized security assessment against http://localhost:3000 targeting BOLA/IDOR and role boundaries.",
        "promptAr": "/pentest نفذ فحص اختراق مصرحاً به على البيئة المحلية لاختبار حدود الصلاحيات وحماية السجلات."
    },
    "security-audit": {
        "short": "التدقيق الأمني الشامل...",
        "full": "مراجعة أمنية شاملة للكود المصدري والـ API والخدمات لاكتشاف الثغرات وتقديم خطط المعالجة.",
        "domainEn": "Comprehensive source-code security audit and threat modeling across auth, payments, secrets, and APIs",
        "domainAr": "تدقيق أمني شامل للكود المصدري ونمذجة التهديدات عبر المصادقة والمدفوعات والأسرار ونقاط الـ API",
        "promptEn": "/security-audit Perform a security review of our authentication, file upload, and payment webhook handlers.",
        "promptAr": "/security-audit أجرِ مراجعة أمنية شاملة لمعالجات تسجيل الدخول ورفع الملفات وإشعارات الدفع."
    },
    "cookie-debugging": {
        "short": "تشخيص الكوكيز والجلسات...",
        "full": "يفحص ويعالج مشاكل الكوكيز وانتهاء الجلسات وأخطاء 401/403 وإعدادات SameSite عبر أدوات المتصفح.",
        "domainEn": "Diagnosing 401/403 session drops, Set-Cookie headers, SameSite/Secure flags, and auth redirect loops",
        "domainAr": "تشخيص انقطاع الجلسات وأخطاء 401/403 وإعدادات الكوكيز وحلقات إعادة التوجيه في تسجيل الدخول",
        "promptEn": "/cookie-debugging Diagnose why the session cookie is dropped after login redirect and verify SameSite/HttpOnly flags.",
        "promptAr": "/cookie-debugging شخص سبب فقدان كوكي الجلسة بعد تسجيل الدخول وتحقق من إعدادات SameSite وHttpOnly."
    },
    "reverse-engineer-anything": {
        "short": "الهندسة العكسية المتقدمة...",
        "full": "يحلل الحزم المترجمة وتطبيقات Electron والملفات التنفيذية لفهم آلية عملها أو إعادة بنائها.",
        "domainEn": "Reverse engineering compiled bundles, Electron apps, binaries, or legacy artifacts from runtime evidence",
        "domainAr": "تحليل وهندسة عكسية للحزم المترجمة أو تطبيقات Electron أو الأنظمة القديمة لفهم آلية عملها",
        "promptEn": "/reverse-engineer-anything Analyze the packaged bundle in dist/ to reconstruct its API contract and state machine.",
        "promptAr": "/reverse-engineer-anything حلل الحزمة المترجمة في مجلد dist لاستخراج عقود الـ API وآلة الحالة الخاصة بها."
    },
    "ui-audit": {
        "short": "مدقق الواجهة الشامل...",
        "full": "يمسح الواجهة الأمامية عبر 8 أبعاد (التخطيط، الألوان، التجاوب، إمكانية الوصول، التفاعل، العربية) ويولد تقارير دقيقة.",
        "domainEn": "Running an 8-dimension static UI audit across routes, layouts, tokens, responsiveness, a11y, and RTL",
        "domainAr": "إجراء تدقيق شامل للواجهة الأمامية من 8 أبعاد (التخطيط، الألوان، التجاوب، الوصول، التفاعل، العربية)",
        "promptEn": "/ui-audit Audit all frontend pages in src/ and generate a structured report of layout, contrast, and RTL issues.",
        "promptAr": "/ui-audit افحص جميع صفحات الواجهة في مجلد src وولد تقريراً منظماً بمشاكل التخطيط والتباين والعربية."
    },
    "ui-review-loop": {
        "short": "حلقة الفحص البصري...",
        "full": "يوثق ويختبر سلوك الواجهة الأمامية والتفاعلات في المتصفح عبر جولات مسجلة بالصوت والصورة وخط زمني للـ DOM.",
        "domainEn": "Verifying live browser UI interactions, responsive viewports, and DOM states with recorded evidence",
        "domainAr": "التحقق من تفاعلات الواجهة الحية وتجاوب الشاشات وحالات العناصر بأدلة مسجلة",
        "promptEn": "/ui-review-loop Verify all 5 UI states and mobile drawer interactions across 375px, 768px, and 1440px viewports.",
        "promptAr": "/ui-review-loop تحقق من حالات الواجهة الخمس وتفاعلات القائمة على مقاسات الجوال والتابلت والحاسوب."
    },
    "nextjs-fullstack": {
        "short": "هندسة Next.js 15+...",
        "full": "يفرض حدود مكونات الخادم والعميل، وأمان Server Actions، وتدفق Suspense، وقواعد Tailwind v4 في Next.js.",
        "domainEn": "Building or refactoring Next.js 15+ & React 19 App Router apps with strict RSC/Client boundaries",
        "domainAr": "بناء أو تطوير تطبيقات Next.js 15+ وReact 19 مع فصل صارم بين مكونات الخادم والعميل",
        "promptEn": "/nextjs-fullstack Refactor src/app/dashboard/ to keep data fetching in Server Components and isolate interactivity in minimal Client islands.",
        "promptAr": "/nextjs-fullstack طور لوحة التحكم في Next.js لإبقاء جلب البيانات في مكونات الخادم وعزل التفاعل في مكونات عميل صغيرة."
    },
    "laravel-mastery": {
        "short": "هندسة لارافيل المتقدمة...",
        "full": "يفرض الأنواع الصارمة وفصل طلبات التحقق FormRequest ومنع استعلامات N+1 والقفل المتشائم في Laravel 11+.",
        "domainEn": "Building enterprise Laravel 11+ & PHP 8.3/8.4 features with FormRequests, Action classes, and lockForUpdate()",
        "domainAr": "بناء ميزات احترافية في Laravel 11+ مع فصل التحقق ومنع N+1 واستخدام القفل الآمن للمعاملات",
        "promptEn": "/laravel-mastery Build an idempotent wallet withdrawal service using FormRequest validation, DB::transaction, and lockForUpdate().",
        "promptAr": "/laravel-mastery ابن خدمة سحب رصيد آمنة في لارافيل باستخدام FormRequest ومعاملات قاعدة البيانات وقفل الصفوف."
    },
    "backend-api": {
        "short": "تصميم وبناء الـ API...",
        "full": "يبني ويصمم أنظمة الخلفية ونقاط النهاية REST/GraphQL والمصادقة ومنطق الخادم عبر Node وPython وPHP.",
        "domainEn": "Designing or building backend services, controllers, middleware, and business logic layers",
        "domainAr": "تصميم وبناء خدمات الواجهة الخلفية والمتحكمات والوسطاء ومنطق العمل في الخادم",
        "promptEn": "/backend-api Design and implement a paginated REST API for vendor payouts with role middleware and structured error envelopes.",
        "promptAr": "/backend-api صمم ونفذ واجهة برمجية REST لمدفوعات التجار مع ترقيم الصفحات وفحص الصلاحيات وتوحيد رسائل الخطأ."
    },
    "backend-data": {
        "short": "نمذجة وأداء البيانات...",
        "full": "إجراءات البيانات الخلفية: النمذجة العلائقية، التخزين المؤقت، المعاملات، الترحيل، الفهرسة، وتحسين الاستعلامات.",
        "domainEn": "Optimizing ORM queries, eager loading, Redis caching, batch backfills, and transactional data integrity",
        "domainAr": "تحسين استعلامات قواعد البيانات والتخزين المؤقت والمعاملات وترحيل البيانات بأمان",
        "promptEn": "/backend-data Eliminate the N+1 queries on the orders index endpoint and add cursor pagination with compound indexing.",
        "promptAr": "/backend-data تخلص من استعلامات N+1 في نقطة نهاية الطلبات وأضف ترقيم صفحات سريعاً مع فهرس مركب."
    },
    "backend-http": {
        "short": "بروتوكولات HTTP والويبهوك...",
        "full": "معايير REST وGraphQL وWebSockets وSSE والويبهوك والتحقق من المدخلات وإصدارات الـ API.",
        "domainEn": "Implementing REST status codes, idempotent webhooks, SSE streaming, rate limiting, and boundary validation",
        "domainAr": "تنفيذ معايير HTTP وإشعارات الويبهوك الآمنة وتدفق البيانات وتحديد معدل الطلبات",
        "promptEn": "/backend-http Implement a Stripe webhook receiver with timing-safe signature verification and idempotency key deduplication.",
        "promptAr": "/backend-http نفذ مستقبل إشعارات ويبهوك للدفع مع التحقق الآمن من التوقيع ومنع تكرار تنفيذ العملية."
    },
    "backend-identity": {
        "short": "المصادقة والصلاحيات RBAC...",
        "full": "إدارة الجلسات وJWT وOAuth2 ومفاتيح الـ API وصلاحيات RBAC/ABAC والمصادقة الثنائية في الخادم.",
        "domainEn": "Implementing authentication, JWT/session lifecycle, RBAC/ABAC permissions, MFA, and tenant isolation",
        "domainAr": "تنفيذ تسجيل الدخول وإدارة الجلسات وصلاحيات الأدوار وعزل بيانات المشتركين في الخادم",
        "promptEn": "/backend-identity Add multi-tenant RBAC middleware ensuring users can only access records matching their server-session tenant_id.",
        "promptAr": "/backend-identity أضف وسيط صلاحيات متعدد المستأجرين يضمن وصول المستخدم لسجلات مؤسسته فقط من جلسة الخادم."
    },
    "backend-ops": {
        "short": "الطوابير والمراقبة الخلفية...",
        "full": "إدارة المهام الخلفية والطوابير وتخزين الملفات السحابي والسجلات المنظمة وفحوصات جاهزية الخادم.",
        "domainEn": "Setting up background job queues, retry/dead-letter policies, S3 object storage, and health checks",
        "domainAr": "إعداد طوابير المهام الخلفية وسياسات إعادة المحاولة والتخزين السحابي وفحوصات صحة الخادم",
        "promptEn": "/backend-ops Move PDF invoice generation and email dispatch into an idempotent background queue job with exponential backoff.",
        "promptAr": "/backend-ops انقل توليد فواتير PDF وإرسال البريد إلى مهمة خلفية في الطابور قابلة لإعادة المحاولة بأمان."
    },
    "database": {
        "short": "مخططات وفهارس البيانات...",
        "full": "تصميم جداول قواعد البيانات والترحيل والفهارس والعلاقات عبر PostgreSQL وMySQL وSQLite وFirestore.",
        "domainEn": "Designing normalized database schemas, zero-downtime Expand-and-Contract migrations, foreign keys, and indexes",
        "domainAr": "تصميم مخططات قواعد البيانات والترحيل الآمن بدون توقف والمفاتيح الخارجية والفهارس",
        "promptEn": "/database Design a zero-downtime Expand-and-Contract migration to add multi-currency integer minor-unit columns to invoices.",
        "promptAr": "/database صمم ترحيل قاعدة بيانات بدون توقف لإضافة أعمدة العملات المتعددة بالوحدات الصغرى الصحيحة للفواتير."
    },
    "devops-deploy": {
        "short": "النشر وخطوط CI/CD...",
        "full": "إعداد حاويات Docker وخطوط GitHub Actions والنشر على Vercel وNetlify وAWS وإدارة متغيرات البيئة.",
        "domainEn": "Configuring Docker, GitHub Actions CI/CD pipelines, Nginx, Vercel/Netlify deploys, and env secrets",
        "domainAr": "إعداد حاويات Docker وخطوط النشر التلقائي GitHub Actions واستضافة المواقع ومتغيرات البيئة",
        "promptEn": "/devops-deploy Create a GitHub Actions CI workflow that runs unit tests, guard scans, and builds the production bundle on PRs.",
        "promptAr": "/devops-deploy أنشئ مسار GitHub Actions يشغل الاختبارات وفحوصات الحراس ويبني النسخة الإنتاجية عند كل طلب دمج."
    },
    "testing-qa": {
        "short": "هندسة الاختبارات الشاملة...",
        "full": "كتابة اختبارات الوحدات والتكامل وE2E عبر Vitest وJest وPlaywright وPytest وPest بتغطية حقيقية.",
        "domainEn": "Writing deterministic unit, integration, and Playwright E2E tests covering happy, edge, and failure paths",
        "domainAr": "كتابة اختبارات الوحدات والتكامل واختبارات المتصفح الشاملة للحالات الطبيعية والحدية والأخطاء",
        "promptEn": "/testing-qa Write integration tests for the coupon redemption flow covering valid codes, expired codes, and concurrent double-submits.",
        "promptAr": "/testing-qa اكتب اختبارات تكامل لمسار استخدام الكوبونات تغطي الأكواد الصالحة والمنتهية ومحاولات الاستخدام المتزامنة."
    },
    "web-precode": {
        "short": "الركائز الست ما قبل الكود...",
        "full": "تأليف وفحص الوثائق الهندسية الست (PRD، TRD، تدفق الشاشات، التصميم، قاعدة البيانات، خطة التنفيذ) قبل البرمجة.",
        "domainEn": "Authoring and auditing the 6 Pre-Coding Architecture Pillar documents before writing application code",
        "domainAr": "تأليف وفحص الوثائق الهندسية الست (المتطلبات، التقنية، الشاشات، التصميم، البيانات، الخطة) قبل كتابة الكود",
        "promptEn": "/web-precode Generate and audit all 6 Pre-Coding documents in docs/precode/ for our new B2B ordering portal.",
        "promptAr": "/web-precode أنشئ وافحص الوثائق الهندسية الست في مجلد docs/precode لبوابة طلبات الجملة الجديدة."
    },
    "spec-kit": {
        "short": "نظام المواصفات Spec-Kit...",
        "full": "سير العمل الرسمي للتطوير الموجه بالمواصفات (SDD) عبر مراحل الدستور والمواصفات والتخطيط والمهام والتنفيذ.",
        "domainEn": "Orchestrating Specification-Driven Development (SDD) with hard-stop gates between spec, plan, and tasks",
        "domainAr": "إدارة التطوير الموجه بالمواصفات مع بوابات توقف صارمة بين كتابة المواصفات والخطة والمهام",
        "promptEn": "/spec-kit Initialize a new Spec-Kit feature specification for our automated vendor settlement workflow.",
        "promptAr": "/spec-kit ابدأ مواصفات ميزة جديدة بنظام Spec-Kit لمسار تسوية مستحقات التجار التلقائي."
    },
    "speckit-constitution": {
        "short": "دستور المشروع Spec-Kit...",
        "full": "إنشاء أو تحديث دستور المشروع الهندسي والمبادئ غير القابلة للتفاوض في نظام Spec-Kit.",
        "domainEn": "Creating or updating the project's non-negotiable architectural principles in .specify/memory/constitution.md",
        "domainAr": "إنشاء أو تحديث المبادئ الهندسية غير القابلة للتفاوض للمشروع في ملف دستور Spec-Kit",
        "promptEn": "/speckit-constitution Update the project constitution to enforce integer currency math, RTL parity, and server-side RBAC.",
        "promptAr": "/speckit-constitution حدث دستور المشروع لفرض الحسابات المالية الصحيحة ودعم العربية وفحص الصلاحيات بالخادم."
    },
    "speckit-specify": {
        "short": "كتابة مواصفات الميزة...",
        "full": "تحويل وصف الميزة إلى وثيقة مواصفات دقيقة (spec.md) تشمل قصص المستخدمين ومعايير القبول.",
        "domainEn": "Authoring a structured feature specification (spec.md) with user stories and acceptance criteria",
        "domainAr": "كتابة وثيقة مواصفات دقيقة للميزة (spec.md) تشمل قصص المستخدمين ومعايير القبول",
        "promptEn": "/speckit-specify Write the feature spec for real-time order tracking with status timeline and SMS/email alerts.",
        "promptAr": "/speckit-specify اكتب مواصفات ميزة تتبع الطلبات الفوري مع الخط الزمني للحالة وإشعارات الرسائل والبريد."
    },
    "speckit-clarify": {
        "short": "توضيح فجوات المواصفات...",
        "full": "تحديد النقاط الغامضة في وثيقة المواصفات وطرح حتى 5 أسئلة مركزة لتوثيق الإجابات داخل spec.md.",
        "domainEn": "Resolving underspecified edge cases in spec.md via up to 5 targeted clarification questions",
        "domainAr": "حسم النقاط الغامضة والحالات الحدية في المواصفات عبر طرح حتى 5 أسئلة توضيحية مركزة",
        "promptEn": "/speckit-clarify Scan the current spec.md for ambiguous permissions or failure states and ask clarifying questions.",
        "promptAr": "/speckit-clarify افحص ملف المواصفات الحالي لاكتشاف أي غموض في الصلاحيات أو حالات الفشل واطرح أسئلة التوضيح."
    },
    "speckit-plan": {
        "short": "خطة التنفيذ المعمارية...",
        "full": "توليد خطة التنفيذ التقنية (plan.md) ومخطط البيانات وعقود الـ API انطلاقاً من المواصفات المعتمدة.",
        "domainEn": "Generating the technical implementation plan (plan.md), data model, and API contracts from spec.md",
        "domainAr": "توليد خطة التنفيذ التقنية (plan.md) ونموذج البيانات وعقود الـ API من وثيقة المواصفات",
        "promptEn": "/speckit-plan Generate the technical implementation plan and data contracts for the approved feature spec.",
        "promptAr": "/speckit-plan ولد خطة التنفيذ التقنية وعقود البيانات للمواصفات المعتمدة."
    },
    "speckit-checklist": {
        "short": "قائمة فحص المتطلبات...",
        "full": "توليد قائمة تحقق مخصصة للميزة لضمان تغطية جميع متطلبات الأمان والأداء وتجربة المستخدم.",
        "domainEn": "Generating a requirement quality checklist (UX, security, data integrity) for the active feature spec",
        "domainAr": "توليد قائمة تحقق شاملة لجودة المتطلبات (الأمان، البيانات، تجربة المستخدم) للميزة الحالية",
        "promptEn": "/speckit-checklist Generate a security, RTL, and 6-state UI verification checklist for the current feature.",
        "promptAr": "/speckit-checklist ولد قائمة تحقق للأمان والعربية وحالات الواجهة الست للميزة الحالية."
    },
    "speckit-tasks": {
        "short": "توليد قائمة المهام...",
        "full": "تحويل الخطة التقنية إلى قائمة مهام قابلة للتنفيذ ومرتبة حسب الاعتمادية في ملف tasks.md.",
        "domainEn": "Breaking down plan.md into dependency-ordered, verifiable engineering tasks in tasks.md",
        "domainAr": "تقسيم الخطة التقنية إلى مهام برمجية مرتبة حسب الأولوية والاعتمادية في ملف tasks.md",
        "promptEn": "/speckit-tasks Generate a dependency-ordered tasks.md with exact file paths and verification commands for each step.",
        "promptAr": "/speckit-tasks ولد ملف tasks.md مرتباً حسب الاعتمادية مع مسارات الملفات وأوامر التحقق لكل خطوة."
    },
    "speckit-analyze": {
        "short": "تحليل تطابق الوثائق...",
        "full": "فحص التناسق والجودة بين ملفات spec.md وplan.md وtasks.md قبل بدء كتابة الكود.",
        "domainEn": "Running a non-destructive consistency audit across spec.md, plan.md, and tasks.md before implementation",
        "domainAr": "إجراء فحص تناسق شامل بين ملفات المواصفات والخطة والمهام قبل بدء كتابة الكود",
        "promptEn": "/speckit-analyze Check spec.md, plan.md, and tasks.md for unmapped requirements or conflicting schema definitions.",
        "promptAr": "/speckit-analyze افحص ملفات المواصفات والخطة والمهام لاكتشاف أي متطلبات غير مغطاة أو تعارض في البيانات."
    },
    "speckit-implement": {
        "short": "تنفيذ مهام Spec-Kit...",
        "full": "تنفيذ جميع المهام المحددة في ملف tasks.md بالترتيب مع التحقق التجريبي من كل خطوة.",
        "domainEn": "Executing the approved tasks in tasks.md step-by-step with verification gates",
        "domainAr": "تنفيذ المهام المعتمدة في ملف tasks.md خطوة بخطوة مع تشغيل فحوصات التحقق",
        "promptEn": "/speckit-implement Execute Phase 1 and Phase 2 tasks from tasks.md and verify each task with its test command.",
        "promptAr": "/speckit-implement نفذ مهام المرحلة الأولى والثانية من ملف tasks.md وتحقق من كل مهمة بأمر الاختبار الخاص بها."
    },
    "speckit-converge": {
        "short": "مطابقة الكود مع المهام...",
        "full": "مقارنة الكود الفعلي في المشروع مع ملفات المواصفات والمهام لإضافة أي عمل متبقٍ لم يكتمل.",
        "domainEn": "Auditing the live codebase against spec.md and tasks.md to identify and append any unbuilt gaps",
        "domainAr": "مقارنة الكود الفعلي مع المواصفات وقائمة المهام لاكتشاف أي أجزاء متبقية وإضافتها للتنفيذ",
        "promptEn": "/speckit-converge Compare our current codebase against spec.md and tasks.md and list any remaining unbuilt tasks.",
        "promptAr": "/speckit-converge قارن الكود الحالي بملفي المواصفات والمهام وحدد أي مهام متبقية لم تكتمل بعد."
    },
    "speckit-taskstoissues": {
        "short": "تحويل المهام إلى GitHub...",
        "full": "تحويل المهام الموجودة في ملف tasks.md إلى تذاكر عمل (GitHub Issues) مرتبة ومنظمة.",
        "domainEn": "Converting dependency-ordered tasks in tasks.md into tracked GitHub Issues",
        "domainAr": "تحويل قائمة المهام في tasks.md إلى تذاكر عمل منظمة على منصة GitHub Issues",
        "promptEn": "/speckit-taskstoissues Export the uncompleted tasks in tasks.md into structured GitHub Issues with acceptance criteria.",
        "promptAr": "/speckit-taskstoissues حول المهام غير المكتملة في tasks.md إلى تذاكر GitHub Issues مع معايير القبول."
    },
    "ponytail": {
        "short": "وضع البساطة القصوى...",
        "full": "يفرض أبسط وأقصر حل برمجي يعمل بكفاءة: يستخدم المكتبة القياسية قبل الإضافات الخارجية ويمنع المبالغة الهندسية.",
        "domainEn": "Writing the simplest, shortest, zero-bloat implementation using stdlib/native features (YAGNI)",
        "domainAr": "كتابة أبسط وأقصر كود برمجي يحل المشكلة باستخدام إمكانيات اللغة القياسية وبدون تعقيد",
        "promptEn": "/ponytail Implement a lightweight rate limiter for our API using native in-memory Map without adding external packages.",
        "promptAr": "/ponytail نفذ محدد طلبات خفيفاً للـ API باستخدام إمكانيات اللغة القياسية بدون إضافة مكتبات خارجية."
    },
    "ponytail-review": {
        "short": "مراجعة حذف التعقيد...",
        "full": "مراجعة كود تركز حصرياً على اكتشاف التعقيد الزائد والمكتبات غير الضرورية والتجريد المبالغ فيه لحذفه.",
        "domainEn": "Reviewing a PR or diff exclusively to cut over-engineering, dead wrappers, and unnecessary dependencies",
        "domainAr": "مراجعة التعديلات البرمجية حصرياً لحذف التعقيد الزائد والطبقات الوهمية والمكتبات غير الضرورية",
        "promptEn": "/ponytail-review Review my current git diff and list every over-engineered wrapper or dependency we can delete.",
        "promptAr": "/ponytail-review راجع التعديلات الحالية وحدد كل غلاف معقد أو مكتبة زائدة يمكننا حذفها وتبسيطها."
    },
    "ponytail-audit": {
        "short": "فحص المشروع من التضخم...",
        "full": "يمسح المستودع بالكامل لاكتشاف الكود الميت والمكتبات الزائدة التي يمكن حذفها أو استبدالها ببدائل قياسية.",
        "domainEn": "Scanning the entire repository to produce a ranked list of bloat, dead abstractions, and packages to delete",
        "domainAr": "مسح المشروع بالكامل لإنتاج قائمة مرتبة بالكود الزائد والمكتبات التي يمكن حذفها أو تبسيطها",
        "promptEn": "/ponytail-audit Scan our codebase for over-engineering and rank the top 10 abstractions or dependencies to simplify.",
        "promptAr": "/ponytail-audit افحص المشروع لاكتشاف التضخم الهندسي ورتب أهم 10 أجزاء أو مكتبات يمكن تبسيطها."
    },
    "ponytail-debt": {
        "short": "سجل الاختصارات المؤجلة...",
        "full": "يجمع كل تعليقات ponytail: في الكود داخل سجل موحد لتتبع الاختصارات المتعمدة ومنع نسيانها.",
        "domainEn": "Harvesting all `ponytail:` shortcut comments across the repo into a tracked technical debt ledger",
        "domainAr": "جمع كافة تعليقات الاختصارات المؤجلة (ponytail:) في الكود داخل سجل واضح لمتابعتها",
        "promptEn": "/ponytail-debt Scan the repository for all ponytail: comments and compile our deferred shortcuts ledger.",
        "promptAr": "/ponytail-debt امسح المشروع لجمع كل تعليقات الاختصارات المؤجلة في جدول متابعة موحد."
    },
    "ponytail-gain": {
        "short": "لوحة توفير الكود...",
        "full": "يعرض إحصائيات التوفير في حجم الكود والتكلفة والسرعة التي يحققها نظام البساطة Ponytail.",
        "domainEn": "Viewing the benchmarked code-size, token, and speed savings scoreboard of Ponytail simplicity mode",
        "domainAr": "عرض لوحة نتائج التوفير في حجم الكود والتكلفة والسرعة لوضع البساطة Ponytail",
        "promptEn": "/ponytail-gain Show the Ponytail simplicity impact scoreboard.",
        "promptAr": "/ponytail-gain اعرض لوحة إحصائيات التوفير والأثر لوضع البساطة."
    },
    "ponytail-help": {
        "short": "دليل أوامر البساطة...",
        "full": "بطاقة مرجعية سريعة لجميع أوضاع وأوامر ومهارات عائلة Ponytail لمنع التعقيد.",
        "domainEn": "Quick reference card for all Ponytail simplicity modes (lite, full, ultra) and commands",
        "domainAr": "البطاقة المرجعية السريعة لجميع أوامرومستويات وضع البساطة Ponytail",
        "promptEn": "/ponytail-help Show all Ponytail modes and slash commands.",
        "promptAr": "/ponytail-help اعرض دليل أوامر ومستويات وضع البساطة Ponytail."
    },
    "caveman": {
        "short": "وضع الردود المضغوطة...",
        "full": "وضع تواصل فائق الاختصار يقلل استهلاك التوكنز بنسبة كبيرة مع الحفاظ التام على الدقة التقنية.",
        "domainEn": "Switching chat responses to ultra-brief, low-token technical answers (lite, full, ultra)",
        "domainAr": "تحويل ردود المحادثة إلى إجابات تقنية مختصرة جداً لتوفير التوكنز والوقت",
        "promptEn": "/caveman lite Keep all responses ultra-concise and high-signal for this session.",
        "promptAr": "/caveman lite اجعل جميع الردود في هذه الجلسة مختصرة ومباشرة جداً."
    },
    "data-saver": {
        "short": "درع حماية باقة الإنترنت...",
        "full": "يفحص ويفعل ملف توفير البيانات لبيئة التطوير لإيقاف التحديثات الصامتة والجلب التلقائي وتوفير 75-85% من الإنترنت.",
        "domainEn": "Auditing, applying, or restoring Antigravity IDE low-bandwidth settings via bandwidth_guard.py",
        "domainAr": "فحص أو تفعيل أو استعادة إعدادات توفير الإنترنت في بيئة العمل لتقليل الاستهلاك بنسبة 85%",
        "promptEn": "/data-saver Check current IDE bandwidth drain and apply the low-bandwidth Data-Saver profile.",
        "promptAr": "/data-saver افحص استهلاك الإنترنت في بيئة العمل وفعل ملف توفير البيانات."
    },
    "agentic-workflows": {
        "short": "تنسيق الوكلاء المتعددين...",
        "full": "ينسق سير العمل المتقدم: البحث المتوازي، الإجماع الإحصائي، المناظرة المهيكلة، وحلقات التحسين الذاتي.",
        "domainEn": "Orchestrating parallel research fan-out, dual-model debate, build-verify QA loops, or model-outage fallback",
        "domainAr": "تنسيق مهام البحث المتوازي أو المناظرة المزدوجة أو حلقات الفحص والتحسين المستمر",
        "promptEn": "/agentic-workflows Run a dual-axis security and performance review loop on our checkout service.",
        "promptAr": "/agentic-workflows شغل حلقة مراجعة مزدوجة للأمان والأداء على خدمة إتمام الدفع."
    },
    "debate-review": {
        "short": "مراجعة المناظرة المزدوجة...",
        "full": "مراجعة كود أو طلب دمج (PR) عبر مناظرة بين نموذجين مستقلين لاكتشاف الثغرات والأخطاء العميقة.",
        "domainEn": "Two-perspective adversarial code review of a GitHub PR, GitLab MR, or local git working tree",
        "domainAr": "مراجعة كود معمقة لطلب دمج أو تعديلات محلية عبر مناظرة نقدية لكشف الأخطاء الخفية",
        "promptEn": "/debate-review Run an adversarial review on our current branch diff before opening a Pull Request.",
        "promptAr": "/debate-review أجرِ مراجعة نقدية مزدوجة لتعديلات الفرع الحالي قبل فتح طلب الدمج."
    },
    "opencode-delegate": {
        "short": "تفويض التنفيذ لـ OpenCode...",
        "full": "يفوض مهمة برمجية محددة إلى أداة OpenCode CLI في الخلفية ثم يراجع التعديلات ويدمجها بعد الفحص.",
        "domainEn": "Delegating an isolated coding task or PDF report compilation to the OpenCode background CLI implementer",
        "domainAr": "تفويض مهمة برمجية معزولة أو توليد تقرير PDF إلى أداة OpenCode في الخلفية ومراجعة نتيجتها",
        "promptEn": "/opencode-delegate Delegate compiling the printable architecture summary PDF report to OpenCode and review the output.",
        "promptAr": "/opencode-delegate فوض مهمة تجميع تقرير الهندسة المعمارية بصيغة PDF إلى OpenCode وراجع النتيجة."
    },
    "delegate-setup": {
        "short": "إعداد مسارات التفويض...",
        "full": "يكتشف أدوات CLI المثبتة ويضبط مسارات تفويض المهام البرمجية والاختبارات بعد موافقة المالك.",
        "domainEn": "Configuring which CLI implementer lane handles feature, test, or UI delegation tasks",
        "domainAr": "إعداد وتخصيص مسارات أدوات التنفيذ المساندة لمهام الميزات أو الاختبارات أو الواجهات",
        "promptEn": "/delegate-setup Discover installed CLI implementers and propose a delegation lane configuration.",
        "promptAr": "/delegate-setup اكتشف أدوات سطر الأوامر المثبتة واقترح إعدادات مسارات التفويض."
    },
    "find-skills": {
        "short": "مستكشف المهارات الذكي...",
        "full": "يساعدك في البحث عن المهارة أو الأداة المناسبة لأي مهمة داخل فهرس المهارات أو المتجر.",
        "domainEn": "Discovering which installed Agent OS skill or marketplace plugin best fits a specialized task",
        "domainAr": "البحث عن المهارة أو الإضافة الأنسب لإنجاز مهمة معينة داخل النظام",
        "promptEn": "/find-skills Which skills and CLI tools should I use to audit WooCommerce HPOS and Arabic RTL layout?",
        "promptAr": "/find-skills ما هي المهارات والأدوات المناسبة لفحص توافق ووكرومرس HPOS واتجاه اللغة العربية؟"
    },
    "project-documentation": {
        "short": "مولد وثائق الكود...",
        "full": "يحلل بنية الكود المصدري والمسارات ليولد ملفات README وARCHITECTURE وAPI موثقة بالكامل.",
        "domainEn": "Scanning repository structure and routes to author comprehensive README.md, ARCHITECTURE.md, and API.md",
        "domainAr": "تحليل بنية المستودع والمسارات لكتابة ملفات توثيق شاملة للمشروع والهندسة والـ API",
        "promptEn": "/project-documentation Analyze our repo structure and generate docs/ARCHITECTURE.md with Mermaid flow diagrams.",
        "promptAr": "/project-documentation حلل بنية المشروع وولد ملف docs/ARCHITECTURE.md مع مخططات توضيحية."
    },
    "generate-design": {
        "short": "توليد وتعديل شاشات...",
        "full": "يولد ويعدل شاشات الواجهة الأمامية بصرياً عبر خادم Google Stitch MCP استناداً إلى ملفات التصميم.",
        "domainEn": "Generating new UI screens or design variants visually via Google Stitch MCP from text prompts",
        "domainAr": "توليد شاشات واجهة جديدة أو نسخ تصميمية بصرياً عبر خادم Google Stitch MCP",
        "promptEn": "/generate-design Generate a mobile-first bilingual order tracking screen in Stitch using our DESIGN.md tokens.",
        "promptAr": "/generate-design ولد شاشة تتبع طلبات متجاوبة وثنائية اللغة عبر Stitch باستخدام رموز ملف DESIGN.md."
    },
    "design-md": {
        "short": "توثيق نظام التصميم...",
        "full": "يحلل مشاريع Stitch ويولد ملف DESIGN.md المتكامل للألوان والخطوط والمكونات.",
        "domainEn": "Synthesizing a semantic DESIGN.md file (tokens, typography, surfaces, components) from a Stitch project",
        "domainAr": "تحليل مشروع تصميم في Stitch وتوليد ملف DESIGN.md القياسي للألوان والخطوط والمكونات",
        "promptEn": "/design-md Analyze our Stitch project screens and synthesize a complete root DESIGN.md specification.",
        "promptAr": "/design-md حلل شاشات مشروعنا في Stitch وولد ملف DESIGN.md المرجعي الكامل في جذر المشروع."
    },
    "extract-design-md": {
        "short": "استخراج التصميم من الكود...",
        "full": "يستخرج نظام التصميم (DESIGN.md) مباشرة من كود الواجهة الأمامية وملفات Tailwind وCSS الحالية.",
        "domainEn": "Reverse-engineering a complete DESIGN.md design system directly from existing React/Vue/Astro/Tailwind code",
        "domainAr": "استخراج وثيقة نظام التصميم DESIGN.md مباشرة من كود الواجهة وملفات الأنماط الحالية",
        "promptEn": "/extract-design-md Scan our Tailwind config and UI components to extract a root DESIGN.md token catalog.",
        "promptAr": "/extract-design-md افحص إعدادات Tailwind ومكونات الواجهة لاستخراج ملف DESIGN.md شامل للمشروع."
    },
    "taste-design": {
        "short": "ضبط الذائقة البصرية...",
        "full": "يعاير مؤشرات التباين البصري والحركة وكثافة العناصر في ملفات DESIGN.md لمنع التصميم الرتيب.",
        "domainEn": "Calibrating DESIGN.md for high-craft typography, calibrated contrast, and anti-generic visual hierarchy",
        "domainAr": "ضبط ملف DESIGN.md لرفع جودة الخطوط والتباين البصري ومنع التصاميم القالبية المكررة",
        "promptEn": "/taste-design Refine our DESIGN.md to enforce crisp editorial typography, WCAG AA contrast, and subtle micro-motion.",
        "promptAr": "/taste-design طور ملف DESIGN.md لفرض خطوط واضحة وتباين قياسي وحركات تفاعلية خفيفة."
    },
    "manage-design-system": {
        "short": "إدارة أنظمة التصميم...",
        "full": "ينشئ ويحدث ويطبق أنظمة التصميم عبر خادم StitchMCP لضمان تناسق الشاشات.",
        "domainEn": "Creating, updating, and applying shared design systems across screens in Google Stitch MCP",
        "domainAr": "إنشاء وتحديث وتطبيق نظام التصميم الموحد على جميع الشاشات عبر Google Stitch MCP",
        "promptEn": "/manage-design-system Sync our local DESIGN.md tokens to the active Stitch project design system and apply to all screens.",
        "promptAr": "/manage-design-system زامن رموز ملف DESIGN.md المحلي مع نظام التصميم في Stitch وطبقه على جميع الشاشات."
    },
    "enhance-prompt": {
        "short": "تحسين أوصاف التصميم...",
        "full": "يحول الأفكار البسيطة إلى أوصاف تصميمية دقيقة وغنية بمصطلحات UI/UX ورموز نظام التصميم لـ Stitch.",
        "domainEn": "Upgrading a rough UI idea into a Stitch-optimized design prompt with layout, token, and state details",
        "domainAr": "تحويل فكرة واجهة بسيطة إلى وصف تصميمي احترافي مفصل جاهز للتوليد في Stitch",
        "promptEn": "/enhance-prompt Enhance this UI idea for Stitch: 'A vendor payout settings page with bank account verification'.",
        "promptAr": "/enhance-prompt طور فكرة الواجهة هذه لـ Stitch: 'صفحة إعدادات دفعات التجار مع توثيق الحساب البنكي'."
    },
    "code-to-design": {
        "short": "تحويل الكود إلى تصميم...",
        "full": "يحول كود الواجهة الأمامية (React/Vue/Vite/HTML) إلى تصميم قابل للتعديل في Stitch عبر استخراج HTML ونظام التصميم.",
        "domainEn": "Migrating or uploading an existing coded React/Vue/Astro web app into Google Stitch as editable screens",
        "domainAr": "تحويل ورفع صفحات تطبيق ويب مبرمج حالياً إلى منصة Google Stitch كشاشات قابلة للتعديل",
        "promptEn": "/code-to-design Extract our main dashboard view and design tokens and upload them to our Stitch project.",
        "promptAr": "/code-to-design استخرج شاشة لوحة التحكم الرئيسية ورموز التصميم وارفعها إلى مشروعنا في Stitch."
    },
    "extract-static-html": {
        "short": "استخراج HTML مستقل...",
        "full": "يستخرج ملف HTML ثابت ومستقل بذاته مع دمج CSS والصور لمعاينة حالة الواجهة أو رفعها إلى Stitch.",
        "domainEn": "Extracting a self-contained static HTML snapshot (with inlined CSS/assets) from a built app or component",
        "domainAr": "استخراج ملف HTML ثابت ومستقل بذاته مع دمج الأنماط والصور لمعاينة الواجهة أو مشاركتها",
        "promptEn": "/extract-static-html Capture a self-contained static HTML snapshot of our landing page into stitch-preview/.",
        "promptAr": "/extract-static-html استخرج نسخة HTML ثابتة ومستقلة لصفحة الهبوط داخل مجلد المعاينة."
    },
    "upload-to-stitch": {
        "short": "رفع الملفات إلى Stitch...",
        "full": "يرفع ملفات HTML المستخرجة والصور وملفات DESIGN.md المحلية بأمان إلى مشاريع Google Stitch.",
        "domainEn": "Uploading local HTML snapshots, mockups, or DESIGN.md files to a Google Stitch project without token truncation",
        "domainAr": "رفع ملفات HTML الثابتة أو الصور أو ملفات DESIGN.md المحلية بأمان إلى مشروع Google Stitch",
        "promptEn": "/upload-to-stitch Upload DESIGN.md and stitch-preview/index.html to our active Stitch project.",
        "promptAr": "/upload-to-stitch ارفع ملف DESIGN.md وملف المعاينة الثابت إلى مشروعنا النشط في Stitch."
    },
    "react-components": {
        "short": "تحويل التصميم لـ React...",
        "full": "يحول شاشات Google Stitch إلى مكونات React وVite معيارية نظيفة أو يزامن المكونات الحالية مع أحدث تصميم.",
        "domainEn": "Converting Google Stitch screens into modular, reusable React + Tailwind components (1 component per file)",
        "domainAr": "تحويل شاشات Google Stitch إلى مكونات React معيارية قابلة لإعادة الاستخدام (مكون واحد لكل ملف)",
        "promptEn": "/react-components Convert the approved Stitch checkout screen into modular React components with 2-3 line header comments.",
        "promptAr": "/react-components حول شاشة الدفع المعتمدة في Stitch إلى مكونات React معيارية منفصلة وموثقة."
    },
    "react-vite-dashboard": {
        "short": "لوحات تحكم React + Vite...",
        "full": "يحول تصاميم Stitch إلى لوحات تحكم React + Vite إنتاجية مع TanStack Query ورموز DESIGN.md.",
        "domainEn": "Building production React + Vite admin dashboards with TanStack Query and DESIGN.md tokens",
        "domainAr": "بناء لوحات تحكم إنتاجية بـ React وVite مع إدارة الحالة بـ TanStack Query ورموز التصميم",
        "promptEn": "/react-vite-dashboard Scaffold a React + Vite admin dashboard with sticky sidebar, TanStack Query hooks, and truncated tables.",
        "promptAr": "/react-vite-dashboard ابن لوحة تحكم بـ React وVite تضم قائمة جانبية ثابتة وجلب بيانات بـ TanStack Query وجداول متجاوبة."
    },
    "react-native": {
        "short": "تحويل التصميم لـ React Native...",
        "full": "يحول شاشات وتصاميم Stitch إلى مكونات تطبيقات جوال React Native باستخدام StyleSheet القياسي.",
        "domainEn": "Converting Stitch UI designs into native iOS/Android React Native components using StyleSheet",
        "domainAr": "تحويل تصاميم الواجهات في Stitch إلى مكونات تطبيقات جوال React Native متوافقة",
        "promptEn": "/react-native Convert the Stitch order history screen into a React Native FlatList screen with RTL support.",
        "promptAr": "/react-native حول شاشة سجل الطلبات من Stitch إلى شاشة React Native متجاوبة تدعم العربية."
    },
    "shadcn-ui": {
        "short": "مكونات shadcn/ui...",
        "full": "دليل متخصص لدمج وتخصيص وبناء الواجهات باستخدام مكتبة مكونات shadcn/ui وRadix UI بأفضل الممارسات.",
        "domainEn": "Installing, customizing, and composing accessible shadcn/ui (Radix + Tailwind) dialogs, tables, and forms",
        "domainAr": "تثبيت وتخصيص وبناء النوافذ والجداول والنماذج المتوافقة مع معايير الوصول باستخدام shadcn/ui",
        "promptEn": "/shadcn-ui Build an accessible command palette and data-table filter bar using shadcn/ui Dialog and Popover primitives.",
        "promptAr": "/shadcn-ui ابن شريط تصفية جداول ونافذة أوامر متوافقة مع إمكانية الوصول باستخدام مكونات shadcn/ui."
    },
    "site-md": {
        "short": "دستور الموقع SITE.md...",
        "full": "يحلل متطلبات الموقع ويولد ملف SITE.md المرجعي لتوجيه حلقة بناء الصفحات المتتالية في Stitch.",
        "domainEn": "Synthesizing a SITE.md sitemap and page-generation constitution for the Stitch autonomous build loop",
        "domainAr": "توليد ملف SITE.md لخريطة الموقع ودستور بناء الصفحات المتتالي في منصة Stitch",
        "promptEn": "/site-md Generate a SITE.md blueprint defining all public and admin routes for our Stitch build loop.",
        "promptAr": "/site-md ولد ملف SITE.md يحدد جميع مسارات الصفحات العامة ولوحة التحكم لحلقة البناء."
    },
    "stitch-loop": {
        "short": "حلقة البناء التلقائي Stitch...",
        "full": "يبني صفحات الموقع تباعاً عبر Stitch بنمط تسليم الراية المستمر استناداً إلى ملفي SITE.md وDESIGN.md.",
        "domainEn": "Iteratively generating and syncing multi-page websites through Google Stitch using SITE.md and DESIGN.md",
        "domainAr": "توليد ومزامنة صفحات موقع متعدد الصفحات بالتتابع عبر Google Stitch استناداً إلى SITE.md وDESIGN.md",
        "promptEn": "/stitch-loop Run the Stitch build loop to generate the next unbuilt page in SITE.md using our DESIGN.md system.",
        "promptAr": "/stitch-loop شغل حلقة البناء لتوليد الصفحة التالية من ملف SITE.md باستخدام نظام التصميم المعتمد."
    },
    "remotion": {
        "short": "فيديوهات العرض بـ Remotion...",
        "full": "يولد فيديوهات استعراضية احترافية للمنتج والشاشات باستخدام إطار Remotion مع انتقالات سلسة.",
        "domainEn": "Creating programmatic product walkthrough videos and animated UI demos from Stitch screens using Remotion",
        "domainAr": "إنشاء فيديوهات استعراضية تفاعلية لشاشات المنتج والواجهة برمجياً باستخدام إطار Remotion",
        "promptEn": "/remotion Create a 30-second Remotion product walkthrough video showcasing our new dashboard and mobile view.",
        "promptAr": "/remotion أنشئ فيديو استعراضي مدته 30 ثانية بـ Remotion يعرض لوحة التحكم الجديدة وتجاوب الجوال."
    },
    "webmcp": {
        "short": "بروتوكول المتصفح WebMCP...",
        "full": "الدليل القياسي لتعريض أدوات JavaScript والنماذج داخل صفحات الويب للوكلاء الأذكياء عبر document.modelContext.",
        "domainEn": "Registering in-browser WebMCP tools (document.modelContext.registerTool) so AI agents can actuate web apps safely",
        "domainAr": "تسجيل أدوات WebMCP داخل صفحات الويب لتمكين الوكلاء الأذكياء من التفاعل الآمن مع التطبيق",
        "promptEn": "/webmcp Register an in-page WebMCP tool via document.modelContext.registerTool to let agents filter the orders table.",
        "promptAr": "/webmcp سجل أداة WebMCP داخل الصفحة لتمكين المساعد الذكي من تصفية جدول الطلبات مباشرة."
    },
}

# All 28 Unified Agent OS CLI Tools (`python scripts/agent_os.py <cmd>`)
CLI_TOOLS_CATALOG: List[Dict[str, str]] = [
    {
        "name": "status",
        "command": "python scripts/agent_os.py status",
        "phase": "THINK",
        "phaseAr": "تفكير واستجواب",
        "domainEn": "Checking workspace git SHA, installed skill count (85), active rules (5), and safety hooks",
        "domainAr": "فحص حالة المستودع وعدد المهارات المثبتة (85) والقواعد النشطة (5) وحراس الأمان",
        "shortEn": "Inspect OS status...",
        "shortAr": "فحص حالة النظام...",
        "descriptionEn": "Prints active workspace root, git branch/commit, danger-zone sandbox locks, and installed skill/rule/test counts.",
        "descriptionAr": "يعرض مسار العمل الحالي وحالة Git وأقفال الأمان وعدد المهارات والقواعد وحزم الاختبارات المثبتة.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py status",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py status"
    },
    {
        "name": "route",
        "command": "python scripts/agent_os.py route \"<task>\"",
        "phase": "THINK",
        "phaseAr": "تفكير واستجواب",
        "domainEn": "Auto-selecting the exact Frontend, Backend, Database, and Security skills for any plain-text task",
        "domainAr": "التوجيه التلقائي لاختيار مهارات الواجهة والخلفية والبيانات والأمان لأي مهمة نصية",
        "shortEn": "Auto-route task skills...",
        "shortAr": "توجيه المهارات تلقائياً...",
        "descriptionEn": "Analyzes a task description or file path and returns the prioritized list of skills and guards to activate.",
        "descriptionAr": "يحلل وصف المهمة أو مسار الملف ويعيد قائمة المهارات والحراس التي يجب تفعيلها بالترتيب.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py route \"build responsive orders table with Laravel API\"",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py route \"build responsive orders table with Laravel API\""
    },
    {
        "name": "skill-find",
        "command": "python scripts/agent_os.py skill-find \"<query>\"",
        "phase": "THINK",
        "phaseAr": "تفكير واستجواب",
        "domainEn": "Searching the 85-skill catalog by keyword, framework, or security domain from the terminal",
        "domainAr": "البحث في دليل الـ 85 مهارة بالكلمات المفتاحية أو اسم الإطار أو مجال الأمان",
        "shortEn": "Search skill catalog...",
        "shortAr": "البحث في سجل المهارات...",
        "descriptionEn": "Searches SKILL_INDEX.json for the top 5 matching skills by keyword, category, and trigger description.",
        "descriptionAr": "يبحث في فهرس المهارات ويعرض أفضل 5 مهارات مطابقة للكلمة المفتاحية مع مساراتها.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py skill-find \"woocommerce hpos security\"",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py skill-find \"woocommerce hpos security\""
    },
    {
        "name": "plan-daily",
        "command": "python scripts/agent_os.py plan-daily",
        "phase": "PLAN",
        "phaseAr": "تخطيط ومواصفات",
        "domainEn": "Running morning session triage or scaffolding a brand-new skill (--skill <name>)",
        "domainAr": "تشغيل الفرز اليومي للمهام في الصباح أو توليد مهارة جديدة في النظام",
        "shortEn": "Daily triage & factory...",
        "shortAr": "مخطط اليوم ومصنع المهارات...",
        "descriptionEn": "Scans git status, PROGRESS.md, and DECISIONS.md to select one primary focus or scaffold a new skill.",
        "descriptionAr": "يفحص حالة Git وسجل التقدم والقرارات لتحديد أولوية اليوم أو إنشاء مهارة جديدة متكاملة.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py plan-daily",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py plan-daily"
    },
    {
        "name": "precode",
        "command": "python scripts/agent_os.py precode <init|audit|status>",
        "phase": "PLAN",
        "phaseAr": "تخطيط ومواصفات",
        "domainEn": "Initializing or auditing the 6 Pre-Coding Architecture Pillar documents (01-PRD to 06-PLAN)",
        "domainAr": "تهيئة أو تدقيق الوثائق الهندسية الست ما قبل البرمجة (من PRD إلى خطة التنفيذ)",
        "shortEn": "Audit 6 Pre-Code docs...",
        "shortAr": "فحص الوثائق الهندسية الست...",
        "descriptionEn": "Verifies all 6 Pre-Coding documents exist with zero TBD placeholders and complete 5-State UI matrices.",
        "descriptionAr": "يتحقق من اكتمال الوثائق الهندسية الست وخلوها من النواقص وتغطية حالات الواجهة الخمس.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py precode status",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py precode status"
    },
    {
        "name": "symbol",
        "command": "python scripts/agent_os.py symbol <Name>",
        "phase": "THINK",
        "phaseAr": "تفكير واستجواب",
        "domainEn": "Finding exact AST class/function definitions and line numbers without reading whole files",
        "domainAr": "البحث الدقيق عن تعريف دالة أو كلاس ورقم السطر عبر شجرة الكود AST دون قراءة الملفات كاملة",
        "shortEn": "Find AST symbol...",
        "shortAr": "البحث عن رمز برمجي...",
        "descriptionEn": "Uses AST code_graph.py to locate exact symbol definitions and callers across the repository.",
        "descriptionAr": "يستخدم محلل AST لتحديد موقع تعريف الدوال والكلاسات وأماكن استدعائها بدقة.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py symbol sync_registry",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py symbol sync_registry"
    },
    {
        "name": "outline",
        "command": "python scripts/agent_os.py outline <file>",
        "phase": "THINK",
        "phaseAr": "تفكير واستجواب",
        "domainEn": "Viewing a structural AST outline of classes, functions, and signatures in a file",
        "domainAr": "عرض الهيكل التلخيصي للكلاسات والدوال داخل ملف برمجي بسرعة",
        "shortEn": "AST file outline...",
        "shortAr": "ملخص هيكل الملف...",
        "descriptionEn": "Prints a compact structural outline of all classes, methods, and functions inside a source file.",
        "descriptionAr": "يطبع ملخصاً منظماً لجميع الكلاسات والدوال وأرقام الأسطر داخل الملف المستهدف.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py outline scripts/sync_handbook.py",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py outline scripts/sync_handbook.py"
    },
    {
        "name": "trace",
        "command": "python scripts/agent_os.py trace <args>",
        "phase": "VERIFY",
        "phaseAr": "فحص ومراجعة",
        "domainEn": "Recording and verifying backward root-cause hypotheses during bug investigations",
        "domainAr": "تسجيل وتتبع فرضيات السبب الجذري أثناء تشخيص الأعطال البرمجية",
        "shortEn": "Root-cause bug tracer...",
        "shortAr": "متتبع السبب الجذري...",
        "descriptionEn": "Manages structured root-cause tracing cycles (start, hypothesis, confirm/refute, status) in .agent_trace.json.",
        "descriptionAr": "يدير خطوات تتبع السبب الجذري للأعطال وتوثيق الفرضيات المؤكدة أو المستبعدة.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py trace status",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py trace status"
    },
    {
        "name": "scan",
        "command": "python scripts/agent_os.py scan <file>",
        "phase": "VERIFY",
        "phaseAr": "فحص ومراجعة",
        "domainEn": "Scanning any file for RTL physical CSS violations, missing auth guards, or dangerous calls",
        "domainAr": "فحص أي ملف برمجي لاكتشاف أخطاء كلاسات العربية أو نقص فحص الصلاحيات أو الدوال الخطرة",
        "shortEn": "Static guard file scan...",
        "shortAr": "فحص الملف بالحراس...",
        "descriptionEn": "Runs guard_checker.py on the target file to verify RTL logical CSS, Next.js server actions, and PHP/WP security.",
        "descriptionAr": "يشغل محرك الحراس على الملف المستهدف لفحص خصائص CSS المنطقية وأمان الخادم.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py scan learning-platform/src/pages/index.astro",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py scan learning-platform/src/pages/index.astro"
    },
    {
        "name": "ui-audit",
        "command": "python scripts/agent_os.py ui-audit scan --dir <path>",
        "phase": "VERIFY",
        "phaseAr": "فحص ومراجعة",
        "domainEn": "Running the 100X 8-dimension static frontend UI audit across .astro, .tsx, .vue, .blade.php, and .html",
        "domainAr": "تشغيل محرك فحص الواجهة الأمامية من 8 أبعاد عبر جميع ملفات القوالب والمكونات",
        "shortEn": "8-dimension UI scanner...",
        "shortAr": "فاحص الواجهة بـ 8 أبعاد...",
        "descriptionEn": "Scans frontend directories for sticky shell issues, table overflow, arbitrary hexes, missing a11y labels, and RTL bugs.",
        "descriptionAr": "يمسح مجلدات الواجهة لاكتشاف مشاكل التثبيت وخروج الجداول والألوان العشوائية ونقص وسوم الوصول.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py ui-audit scan --dir learning-platform",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py ui-audit scan --dir learning-platform"
    },
    {
        "name": "sentinel",
        "command": "python scripts/agent_os.py sentinel [path]",
        "phase": "VERIFY",
        "phaseAr": "فحص ومراجعة",
        "domainEn": "Proactive audit for N+1 queries, float money math, missing pagination, and security boundary leaks",
        "domainAr": "الفحص الاستباقي لاكتشاف استعلامات N+1 والحسابات العشرية الخاطئة للمال ونقص الترقيم",
        "shortEn": "Proactive sentinel audit...",
        "shortAr": "الحارس الاستباقي للأداء...",
        "descriptionEn": "Scans code for scalability hazards, float currency risks, unbounded queries, and UX state gaps.",
        "descriptionAr": "يفحص الكود لاكتشاف مخاطر الأداء والتوسع والحسابات المالية والاستعلامات غير المقيدة.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py sentinel .",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py sentinel ."
    },
    {
        "name": "review",
        "command": "python scripts/agent_os.py review",
        "phase": "VERIFY",
        "phaseAr": "فحص ومراجعة",
        "domainEn": "Reviewing uncommitted git diffs for debug leftovers, secret leaks, and quality violations",
        "domainAr": "مراجعة التعديلات الحالية في Git لاكتشاف بقايا الطباعة أو تسرب الأسرار أو مخالفات الجودة",
        "shortEn": "Git diff quality review...",
        "shortAr": "مراجعة تعديلات Git...",
        "descriptionEn": "Runs diff_reviewer.py on the working tree diff to catch console.log/dd(), hardcoded secrets, and missing tests.",
        "descriptionAr": "يفحص التعديلات غير المرفوعة في Git لمنع تسرب الأسرار أو عبارات التشخيص المؤقتة.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py review",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py review"
    },
    {
        "name": "chaos-audit",
        "command": "python scripts/agent_os.py chaos-audit [file]",
        "phase": "VERIFY",
        "phaseAr": "فحص ومراجعة",
        "domainEn": "Auditing resilience against network timeouts, null payloads, and unhandled promise/exception crashes",
        "domainAr": "فحص صمود الكود أمام انقطاع الشبكة والبيانات الفارغة والأخطاء غير المعالجة",
        "shortEn": "Resilience & chaos audit...",
        "shortAr": "فحص الصمود والأخطاء...",
        "descriptionEn": "Checks async calls, webhooks, and external integrations for timeout guards and clean error handling.",
        "descriptionAr": "يفحص استدعاءات الشبكة والويبهوك للتأكد من وجود مهلة زمنية ومعالجة آمنة للأخطاء.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py chaos-audit",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py chaos-audit"
    },
    {
        "name": "snapshot",
        "command": "python scripts/agent_os.py snapshot <freeze|resume> \"<label>\"",
        "phase": "THINK",
        "phaseAr": "تفكير واستجواب",
        "domainEn": "Freezing or resuming SESSION_SNAPSHOT.md at 60-70% context capacity for zero-loss chat handover",
        "domainAr": "تجميد أو استعادة لقطة الجلسة عند امتلاء 60-70% من السياق للانتقال لمحادثة جديدة بدون فقدان الذاكرة",
        "shortEn": "60-70% context handover...",
        "shortAr": "حفظ واستعادة سياق الجلسة...",
        "descriptionEn": "Writes or restores SESSION_SNAPSHOT.md capturing Objective, Locked Decisions, Rejected Ideas, and Next Step.",
        "descriptionAr": "يحفظ أو يستعيد ملف SESSION_SNAPSHOT.md شاملاً الهدف والقرارات المعتمدة والأفكار المرفوضة والخطوة التالية.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py snapshot freeze \"Milestone Complete\"",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py snapshot freeze \"Milestone Complete\""
    },
    {
        "name": "sync",
        "command": "python scripts/agent_os.py sync [--apply] [--team]",
        "phase": "BUILD",
        "phaseAr": "بناء وتنفيذ",
        "domainEn": "Synchronizing all 85 skills, 5 rules, scripts, and GEMINI.md across Workspace, Antigravity, and OpenCode",
        "domainAr": "مزامنة جميع المهارات الـ 85 والقواعد والسكربتات بين المستودع وبيئة Antigravity وOpenCode",
        "shortEn": "Tri-target config sync...",
        "shortAr": "مزامنة الإعدادات الشاملة...",
        "descriptionEn": "Synchronizes skills, rules, scripts, and slash commands across Workspace, ~/.gemini/config, and ~/.config/opencode.",
        "descriptionAr": "يزامن المهارات والقواعد والأوامر المختصرة عبر المستودع والإعدادات العامة للنظام.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py sync --apply --team",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py sync --apply --team"
    },
    {
        "name": "handbook-sync",
        "command": "python scripts/agent_os.py handbook-sync --build [--deploy]",
        "phase": "BUILD",
        "phaseAr": "بناء وتنفيذ",
        "domainEn": "Rebuilding the bilingual W3Schools Learning Platform, syncing root handbook.html, and deploying to GitHub Pages",
        "domainAr": "تحديث سجل المهارات وبناء منصة التعلم التفاعلية ومزامنة handbook.html والنشر على GitHub Pages",
        "shortEn": "Build & deploy handbook...",
        "shortAr": "بناء ونشر منصة التعلم...",
        "descriptionEn": "Syncs SKILL_INDEX.json into skills-registry.json, compiles Astro dist/index.html, updates handbook.html, and deploys to GitHub Pages.",
        "descriptionAr": "يزامن فهرس المهارات مع منصة التعلم، ويبني الواجهة الثابتة، ويحدث handbook.html، وينشر التحديثات على GitHub Pages.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py handbook-sync --build --deploy",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py handbook-sync --build --deploy"
    },
    {
        "name": "index-skills",
        "command": "python scripts/agent_os.py index-skills",
        "phase": "BUILD",
        "phaseAr": "بناء وتنفيذ",
        "domainEn": "Re-indexing all skills, plugin skills, and MCP servers into SKILL_INDEX.json and SKILLS_DIRECTORY.md",
        "domainAr": "إعادة فهرسة جميع المهارات والإضافات وخوادم MCP داخل SKILL_INDEX.json وSKILLS_DIRECTORY.md",
        "shortEn": "Rebuild skill index...",
        "shortAr": "إعادة فهرسة المهارات...",
        "descriptionEn": "Scans skills/ and global plugins to regenerate SKILL_INDEX.json and SKILLS_DIRECTORY.md.",
        "descriptionAr": "يمسح مجلدات المهارات والإضافات لتوليد ملفات الفهرس والدليل المحدثة.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py index-skills",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py index-skills"
    },
    {
        "name": "data-saver",
        "command": "python scripts/agent_os.py data-saver <status|apply|restore>",
        "phase": "THINK",
        "phaseAr": "تفكير واستجواب",
        "domainEn": "Cutting Antigravity IDE background internet bandwidth consumption by 75-85%",
        "domainAr": "تقليل استهلاك الإنترنت الخلفي في بيئة التطوير بنسبة 75-85% عبر إيقاف التحديثات الصامتة",
        "shortEn": "Low-bandwidth IDE guard...",
        "shortAr": "أداة توفير بيانات الإنترنت...",
        "descriptionEn": "Audits or applies low-bandwidth settings in Antigravity IDE and configures offline package manager caches.",
        "descriptionAr": "يفحص أو يطبق إعدادات توفير باقة الإنترنت في بيئة التطوير ويفعل الكاش المحلي للحزم.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py data-saver status",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py data-saver status"
    },
    {
        "name": "test",
        "command": "python scripts/agent_os.py test",
        "phase": "VERIFY",
        "phaseAr": "فحص ومراجعة",
        "domainEn": "Running the complete Agent OS unit test and security guard verification battery",
        "domainAr": "تشغيل حزمة اختبارات الوحدات وفحوصات حراس الأمان الكاملة للنظام",
        "shortEn": "Run all unit tests...",
        "shortAr": "تشغيل جميع الاختبارات...",
        "descriptionEn": "Executes all unit tests in tests/ to verify CLI engines, guards, sync parity, and handbook compilation.",
        "descriptionAr": "ينفذ جميع الاختبارات البرمجية في مجلد tests للتحقق من سلامة الأدوات والحراس والمزامنة.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py test",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py test"
    },
    {
        "name": "audit",
        "command": "python scripts/agent_os.py audit",
        "phase": "VERIFY",
        "phaseAr": "فحص ومراجعة",
        "domainEn": "Auditing all SKILL.md frontmatter, broken file links, and rule integrity across Agent OS",
        "domainAr": "فحص سلامة ترويسات جميع ملفات المهارات والروابط والقواعد داخل النظام",
        "shortEn": "Audit skill integrity...",
        "shortAr": "فحص سلامة بنية النظام...",
        "descriptionEn": "Runs audit_agent_os.py to validate YAML frontmatter, markdown links, and directory structure.",
        "descriptionAr": "يفحص صحة بيانات YAML والروابط الداخلية وهيكلة المجلدات لجميع المهارات والقواعد.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py audit",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py audit"
    },
    {
        "name": "doctor",
        "command": "python scripts/agent_os.py doctor [--fix]",
        "phase": "VERIFY",
        "phaseAr": "فحص ومراجعة",
        "domainEn": "Diagnosing environment health, Python/Node tools, and auto-fixing config drift",
        "domainAr": "تشخيص جاهزية بيئة العمل وأدوات Python/Node وإصلاح عدم تطابق الإعدادات تلقائياً",
        "shortEn": "Environment health check...",
        "shortAr": "فحص جاهزية بيئة العمل...",
        "descriptionEn": "Checks required runtimes, hooks, and global sync state, automatically repairing drift when --fix is passed.",
        "descriptionAr": "يتحقق من توفر بيئات التشغيل والخطافات وحالة المزامنة مع إمكانية الإصلاح التلقائي.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py doctor",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py doctor"
    },
    {
        "name": "scope",
        "command": "python scripts/agent_os.py scope <set|check|clear|status>",
        "phase": "PLAN",
        "phaseAr": "تخطيط ومواصفات",
        "domainEn": "Locking allowed file/directory edit boundaries so narrow fixes never touch unrelated files",
        "domainAr": "قفل حدود الملفات المسموح بتعديلها لضمان عدم المساس بأي ملفات خارج نطاق المهمة",
        "shortEn": "Lock file edit scope...",
        "shortAr": "قفل نطاق تعديل الملفات...",
        "descriptionEn": "Enforces surgical change boundaries by restricting edits to explicitly approved paths.",
        "descriptionAr": "يفرض حدود التعديل الجراحي عبر حصر التغييرات في المسارات المعتمدة فقط.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py scope status",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py scope status"
    },
    {
        "name": "adr-check",
        "command": "python scripts/agent_os.py adr-check [list]",
        "phase": "VERIFY",
        "phaseAr": "فحص ومراجعة",
        "domainEn": "Verifying code compliance against locked Architectural Decision Records in DECISIONS.md",
        "domainAr": "التحقق من التزام الكود بالقرارات المعمارية المعتمدة والموثقة في ملف DECISIONS.md",
        "shortEn": "Enforce ADR decisions...",
        "shortAr": "فحص الالتزام بالقرارات...",
        "descriptionEn": "Checks the repository against architectural invariants locked in DECISIONS.md.",
        "descriptionAr": "يفحص التزام المشروع بالقواعد والقرارات المعمارية الموثقة في سجل القرارات.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py adr-check list",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py adr-check list"
    },
    {
        "name": "antipattern",
        "command": "python scripts/agent_os.py antipattern <list|scan|audit>",
        "phase": "VERIFY",
        "phaseAr": "فحص ومراجعة",
        "domainEn": "Scanning code against the recurring bug & anti-pattern ledger (.agent_antipatterns.json)",
        "domainAr": "فحص الكود مقابل سجل الأخطاء المتكررة والأنماط الممنوعة لمنع تكرارها",
        "shortEn": "Scan known anti-patterns...",
        "shortAr": "فحص الأخطاء المتكررة...",
        "descriptionEn": "Prevents regression of historical bugs by scanning files against recorded anti-pattern signatures.",
        "descriptionAr": "يمنع عودة الأخطاء السابقة عبر فحص الملفات مقابل بصمات الأخطاء المسجلة.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py antipattern list",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py antipattern list"
    },
    {
        "name": "eval / sql / regex",
        "command": "python scripts/agent_os.py <eval|sql|regex> [args]",
        "phase": "VERIFY",
        "phaseAr": "فحص ومراجعة",
        "domainEn": "Testing Python expressions, SQLite queries, or regular expressions deterministically in a sandbox",
        "domainAr": "اختبار تعبيرات Python أو استعلامات SQL أو التعبيرات النمطية Regex في بيئة معزولة",
        "shortEn": "Deterministic REPL sandbox...",
        "shortAr": "بيئة اختبار SQL وRegex...",
        "descriptionEn": "Executes isolated Python math, SQL schema queries, or regex pattern checks instead of guessing in prose.",
        "descriptionAr": "ينفذ حسابات بايثون واستعلامات SQL وفحوصات Regex بشكل حتمي بدلاً من التخمين النظري.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py regex \"^/[a-z-]+$\" \"/feature-full\"",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py regex \"^/[a-z-]+$\" \"/feature-full\""
    },
    {
        "name": "probe / logs",
        "command": "python scripts/agent_os.py <probe|logs> [args]",
        "phase": "VERIFY",
        "phaseAr": "فحص ومراجعة",
        "domainEn": "Probing local HTTP endpoints or tailing application log files without opening a browser",
        "domainAr": "فحص استجابة نقاط النهاية المحلية أو قراءة سجلات الأخطاء بدون فتح المتصفح",
        "shortEn": "HTTP probe & log tail...",
        "shortAr": "فحص الروابط والسجلات...",
        "descriptionEn": "Checks HTTP status/latency of local dev servers and extracts recent error stack traces from logs.",
        "descriptionAr": "يتحقق من حالة وسرعة استجابة الخوادم المحلية ويستخرج أحدث رسائل الخطأ من السجلات.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py probe http://localhost:3000",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py probe http://localhost:3000"
    },
    {
        "name": "telemetry",
        "command": "python scripts/agent_os.py telemetry [status|stats|today]",
        "phase": "THINK",
        "phaseAr": "تفكير واستجواب",
        "domainEn": "Inspecting live conversation context percentage (60-70% threshold) and token cost analytics",
        "domainAr": "فحص نسبة استهلاك سياق المحادثة الحالي وإحصائيات استهلاك التوكنز",
        "shortEn": "Context & token telemetry...",
        "shortAr": "قياس السياق والتوكنز...",
        "descriptionEn": "Reports active conversation context usage against the 60-70% handover threshold and token dashboard stats.",
        "descriptionAr": "يعرض نسبة امتلاء سياق المحادثة مقارنة بحد الـ 60-70% وإحصائيات التوكنز.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py telemetry status",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py telemetry status"
    },
    {
        "name": "codemod",
        "command": "python scripts/agent_os.py codemod <args>",
        "phase": "BUILD",
        "phaseAr": "بناء وتنفيذ",
        "domainEn": "Performing safe, deterministic regex/AST multi-file refactoring with dry-run diff preview",
        "domainAr": "تنفيذ تعديلات هيكلية آمنة عبر عدة ملفات مع معاينة الفروق قبل التطبيق",
        "shortEn": "Safe multi-file codemod...",
        "shortAr": "تعديل متعدد الملفات آمن...",
        "descriptionEn": "Runs codemod.py to preview and apply safe structural replacements across a directory.",
        "descriptionAr": "يتيح معاينة وتطبيق التعديلات البرمجية المتكررة عبر ملفات المشروع بأمان.",
        "samplePromptEn": "python D:\\Skills\\.agents\\scripts\\agent_os.py codemod --help",
        "samplePromptAr": "python D:\\Skills\\.agents\\scripts\\agent_os.py codemod --help"
    },
]


def sanitize_copy(text: str) -> str:
    """Remove forbidden buzzwords so synced JSON never triggers anti_slop checks."""
    replacements = {
        r"\bseamless(ly)?\b": "smooth",
        r"\bleverage\b": "use",
        r"\bcutting-edge\b": "modern",
        r"\bgame-changer\b": "practical tool",
        r"\brevolutionize\b": "improve",
        r"\bparadigm-shift\b": "structural shift",
        r"\bempower(s|ing)?\b": "enable",
        r"\bharness\b": "apply",
        r"\bunlock(s|ing)?\b": "enable",
        r"\bsupercharge\b": "accelerate",
        r"\belevate\b": "improve",
        r"\bunleash\b": "run",
        r"\bdelve\b": "inspect",
        r"\beffortless(ly)?\b": "direct",
        r"\bstreamline(s|d)?\b": "simplify",
        r"\bstate-of-the-art\b": "verified",
        r"\bbest-in-class\b": "reliable",
        r"\bworld-class\b": "production-ready",
        r"\bnext-gen\b": "modern",
        r"\bholistic\b": "complete",
        r"\bsynergy\b": "coordination",
        r"\bdisrupt\b": "change",
        r"\bdive into\b": "examine",
    }
    cleaned = text
    for pattern, repl in replacements.items():
        cleaned = re.sub(pattern, repl, cleaned, flags=re.IGNORECASE)
    return cleaned


def truncate_words(text: str, max_words: int = 3) -> str:
    """Truncate text to 2-4 words + '...' for responsive data table cells."""
    words = [w for w in re.split(r"\s+", text.strip()) if w]
    if len(words) <= max_words:
        return " ".join(words)
    return " ".join(words[:max_words]) + "..."


def build_registry_payload(index_data: Dict[str, Any]) -> Dict[str, Any]:
    skills_raw: List[Dict[str, Any]] = index_data.get("skills", [])
    mcp_raw: List[Dict[str, Any]] = index_data.get("mcp_servers", [])
    plugin_raw: List[Dict[str, Any]] = index_data.get("plugin_skills", [])

    skills_out: List[Dict[str, Any]] = []
    for item in skills_raw:
        name = item.get("name", "")
        cat_en = item.get("category", "Core Architecture & Workflow")
        cat_ar = CATEGORY_AR_MAP.get(cat_en, "الهندسة الأساسية وسير العمل")
        role_en = item.get("role", "domain-skill")
        role_ar = ROLE_AR_MAP.get(role_en, "مهارة تخصصية")
        phase_en = item.get("phase", "BUILD")
        phase_ar = PHASE_AR_MAP.get(phase_en, "بناء وتنفيذ")

        desc_en = sanitize_copy(item.get("description", ""))
        short_en = truncate_words(desc_en, 3)

        enriched = SKILL_CATALOG_ENRICHMENT.get(name, {})
        short_ar = enriched.get("short", f"مهارة {cat_ar.split()[0]}...")
        desc_ar = enriched.get(
            "full",
            f"مهارة /{name} ضمن فئة ({cat_ar}) في مرحلة ({phase_ar}): {desc_en}",
        )
        domain_en = enriched.get("domainEn", f"{cat_en} tasks requiring /{name}")
        domain_ar = enriched.get("domainAr", f"مهام {cat_ar} عبر أمر /{name}")
        domain_short_en = truncate_words(domain_en, 4)
        domain_short_ar = truncate_words(domain_ar, 4)
        prompt_en = enriched.get(
            "promptEn",
            f"/{name} Inspect my current project context and execute the {name} workflow.",
        )
        prompt_ar = enriched.get(
            "promptAr",
            f"/{name} افحص سياق المشروع الحالي ونفذ مسار عمل {name} بدقة.",
        )

        skills_out.append({
            "name": name,
            "command": f"/{name}",
            "categoryEn": cat_en,
            "categoryAr": cat_ar,
            "phase": phase_en,
            "phaseAr": phase_ar,
            "role": role_en,
            "roleAr": role_ar,
            "domainEn": domain_en,
            "domainAr": domain_ar,
            "domainShortEn": domain_short_en,
            "domainShortAr": domain_short_ar,
            "shortEn": short_en,
            "shortAr": short_ar,
            "descriptionEn": desc_en,
            "descriptionAr": desc_ar,
            "samplePromptEn": prompt_en,
            "samplePromptAr": prompt_ar,
            "file": item.get("file", f"skills/{name}/SKILL.md"),
        })

    mcp_out: List[Dict[str, Any]] = []
    for srv in mcp_raw:
        srv_name = srv.get("name", "")
        domain_en = sanitize_copy(srv.get("domain", ""))
        phase_en = srv.get("phase", "BUILD")
        mcp_out.append({
            "name": srv_name,
            "phase": phase_en,
            "phaseAr": PHASE_AR_MAP.get(phase_en, "بناء وتنفيذ"),
            "domainEn": domain_en,
            "domainAr": f"خادم MCP ({srv_name}): {domain_en}",
            "shortEn": truncate_words(domain_en, 3),
            "shortAr": f"خادم {srv_name}...",
            "samplePromptEn": f"Use MCP server {srv_name} to inspect live runtime state or official documentation for this task.",
            "samplePromptAr": f"استخدم خادم MCP ({srv_name}) لفحص الحالة الحية أو التوثيق الرسمي لهذه المهمة.",
        })

    cli_out: List[Dict[str, Any]] = []
    for tool in CLI_TOOLS_CATALOG:
        t_copy = dict(tool)
        t_copy.setdefault("categoryEn", "Unified CLI Engine (agent_os.py)")
        t_copy.setdefault("categoryAr", "محرك سطر الأوامر الموحد (agent_os.py)")
        t_copy.setdefault("domainShortEn", truncate_words(t_copy.get("domainEn", ""), 4))
        t_copy.setdefault("domainShortAr", truncate_words(t_copy.get("domainAr", ""), 4))
        cli_out.append(t_copy)

    return {
        "version": "2.1.0",
        "totalSkills": len(skills_out),
        "totalPluginSkills": len(plugin_raw),
        "totalMcpServers": len(mcp_out),
        "totalCliTools": len(cli_out),
        "skills": skills_out,
        "cliTools": cli_out,
        "mcpServers": mcp_out,
    }


def sync_registry() -> Dict[str, Any]:
    if not SKILL_INDEX_PATH.exists():
        raise FileNotFoundError(f"Missing SKILL_INDEX.json at {SKILL_INDEX_PATH}")
    raw = json.loads(SKILL_INDEX_PATH.read_text(encoding="utf-8"))
    payload = build_registry_payload(raw)
    REGISTRY_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_OUT_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return payload


def sync_built_html(run_build: bool = False) -> bool:
    if run_build and (PLATFORM_DIR / "package.json").exists():
        npm_cmd = "npm.cmd" if sys.platform.startswith("win") else "npm"
        res = subprocess.run([npm_cmd, "run", "build"], cwd=PLATFORM_DIR)
        if res.returncode != 0:
            return False

    if DIST_HTML_PATH.exists():
        shutil.copyfile(DIST_HTML_PATH, ROOT_HANDBOOK_PATH)
        return True
    return False


GITHUB_PAGES_REPO = "https://github.com/Muaz-Aldalil/agent-os-learning-platform.git"
GITHUB_PAGES_LIVE_URL = "https://muaz-aldalil.github.io/agent-os-learning-platform/"


def deploy_github_pages(repo_url: str = GITHUB_PAGES_REPO, force_gh_pages: bool = False) -> bool:
    """Push learning-platform source (main, non-force) and compiled dist/ (gh-pages) to GitHub Pages."""
    if not DIST_HTML_PATH.exists():
        print("[ERROR] dist/index.html does not exist. Run with --build first.")
        return False

    with tempfile.TemporaryDirectory(prefix="agent_os_pages_") as tmp_root:
        stage_main = Path(tmp_root) / "main"
        stage_pages = Path(tmp_root) / "gh-pages"

        # Clone existing main branch so history is preserved without --force
        clone_res = subprocess.run(
            ["git", "clone", "--branch", "main", "--single-branch", repo_url, str(stage_main)],
            capture_output=True,
            text=True,
        )
        if clone_res.returncode != 0:
            stage_main.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "init", "-b", "main"], cwd=stage_main, capture_output=True, text=True)
            subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=stage_main, capture_output=True, text=True)

        shutil.copytree(
            PLATFORM_DIR,
            stage_main,
            ignore=shutil.ignore_patterns(".git", ".netlify", "node_modules", ".astro"),
            dirs_exist_ok=True,
        )

        # Clone existing gh-pages branch if present so fast-forward works without --force
        clone_pages_res = subprocess.run(
            ["git", "clone", "--branch", "gh-pages", "--single-branch", repo_url, str(stage_pages)],
            capture_output=True,
            text=True,
        )
        if clone_pages_res.returncode != 0:
            stage_pages.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "init", "-b", "gh-pages"], cwd=stage_pages, capture_output=True, text=True)
            subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=stage_pages, capture_output=True, text=True)

        shutil.copytree(
            PLATFORM_DIR / "dist",
            stage_pages,
            ignore=shutil.ignore_patterns(".git", ".netlify"),
            dirs_exist_ok=True,
        )

        subprocess.run(["git", "add", "-A"], cwd=stage_main, capture_output=True, text=True)
        status_main = subprocess.run(
            ["git", "status", "--porcelain"], cwd=stage_main, capture_output=True, text=True
        )
        if status_main.stdout.strip():
            cmds_main = [
                ["git", "commit", "-m", "chore: sync Agent OS learning platform (85 skills + 28 CLI tools + domain prompts)"],
                ["git", "push", "-u", "origin", "main"],
            ]
            for cmd in cmds_main:
                res = subprocess.run(cmd, cwd=stage_main, capture_output=True, text=True)
                if res.returncode != 0:
                    print(f"[ERROR] Failed main push command {' '.join(cmd)}: {res.stderr}")
                    return False

        subprocess.run(["git", "add", "-A"], cwd=stage_pages, capture_output=True, text=True)
        status_pages = subprocess.run(
            ["git", "status", "--porcelain"], cwd=stage_pages, capture_output=True, text=True
        )
        if status_pages.stdout.strip():
            push_pages_cmd = ["git", "push", "-u", "origin", "gh-pages"]
            if force_gh_pages:
                push_pages_cmd.append("--force")

            cmds_pages = [
                ["git", "commit", "-m", "deploy: sync static build for GitHub Pages (85 skills + 28 CLI tools)"],
                push_pages_cmd,
            ]
            for cmd in cmds_pages:
                res = subprocess.run(cmd, cwd=stage_pages, capture_output=True, text=True)
                if res.returncode != 0:
                    print(f"[ERROR] Failed gh-pages push command {' '.join(cmd)}: {res.stderr}")
                    return False

    print(f"[OK] Deployed live to GitHub Pages -> {GITHUB_PAGES_LIVE_URL}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Agent OS Skills Registry & Handbook HTML")
    parser.add_argument("--build", action="store_true", help="Run Astro build before syncing root handbook.html")
    parser.add_argument("--deploy", action="store_true", help="Deploy compiled platform to GitHub Pages")
    parser.add_argument("--force-gh-pages", action="store_true", help="Allow force-pushing static build to gh-pages branch only")
    parser.add_argument("--registry-only", action="store_true", help="Only generate skills-registry.json")
    args = parser.parse_args()

    payload = sync_registry()
    print(
        f"[OK] Synced {payload['totalSkills']} core skills, {payload['totalCliTools']} CLI tools & {payload['totalMcpServers']} MCP servers "
        f"-> {REGISTRY_OUT_PATH.relative_to(WORKSPACE_ROOT)}"
    )

    if not args.registry_only:
        copied = sync_built_html(run_build=args.build or args.deploy)
        if copied:
            print(f"[OK] Synced Astro build -> {ROOT_HANDBOOK_PATH.relative_to(WORKSPACE_ROOT)}")
        else:
            print("[INFO] Astro dist/index.html not yet built; skipped root handbook.html copy.")

        if args.deploy:
            if not deploy_github_pages(force_gh_pages=args.force_gh_pages):
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
