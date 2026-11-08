# 📘 The `.agents` Beginner Handbook | دليل استخدام `.agents` المبسط

> **You do NOT need to be a senior developer—or even a junior developer—to build professional, secure, bug-free apps with this system.**
> **لا تحتاج أن تكون مبرمجاً خبيراً (أو حتى مبتدئاً) لتبني تطبيقات ولوحات تحكم احترافية وآمنة وخالية من الأخطاء باستخدام هذا النظام.**

---

## 🔥 1. Why You Need This (Once You See This, You Can't Unsee It)
### لماذا تحتاج `.agents`؟ (الفرق بين العمل بدونه والعمل معه)

### ❌ Without `.agents`: Your AI is a "Fast Intern"
If you open a normal AI chat and say *"build a users page,"* it acts like an impatient intern: it **guesses** what you want, writes messy code, forgets security, breaks the sidebar and Arabic layout, and wastes your internet data.

### ✅ With `.agents`: Your AI Becomes a "Full Senior Tech Team"
With `.agents` installed, your AI turns into a **coordinated Senior Engineering Team** (**UI Designer + Frontend Architect + Backend Engineer + Database Expert + Security Guard + QA Tester**) that **interviews you first**, plans before writing code, enforces CMS layout & security standards, and checks its own work automatically.

> **ما هو `.agents` باختصار؟**
> * **بدون `.agents`:** الذكاء الاصطناعي يتصرف كمتدرب متسرع—يخمن طلبك، يكتب كود عشوائي، ينسى الأمان والصلاحيات، يكسر القوائم الجانبية واللغة العربية (RTL)، ويستهلك باقة الإنترنت.
> * **مع `.agents`:** يتحول المساعد إلى **فريق برمجي خبير كامل** (مصمم واجهات + مبرمج باك-إند + خبير قواعد بيانات + حارس أمان) يسألك أولاً، يخطط، يكتب كود نظيف بأي تقنية تختارها، ويراجع أخطاءه بنفسه قبل أن يسلمك النتيجة.

### ⚡ Side-by-Side: How Your AI Performs Without vs. With `.agents`

| Area (المجال) | ❌ WITHOUT `.agents` (Fast Intern) | ✅ WITH `.agents` (Senior Tech Team) |
| :--- | :--- | :--- |
| **Clarifying Your Idea**<br>*(فهم فكرتك)* | Guesses everything and builds the wrong screen.<br>*(يخمن كل شيء ويبني صفحة مختلفة عما في بالك)* | **Interviews you first** (`/grill-me` + `/muaz-skill`) with `(Recommended)` choices before writing code.<br>*(يسألك خطوة بخطوة مع خيارات مقترحة قبل كتابة أي كود)* |
| **Tech Stack**<br>*(التقنيات واللغات)* | Forces random libraries you didn't ask for.<br>*(يفرض عليك مكتبات عشوائية)* | **100% Your Choice** (React, Next.js, Vue, Laravel, Blade, WordPress, Node, Python, MySQL, Postgres, etc.).<br>*(يكتشف تقنيات مشروعك تلقائياً أو يلتزم بالتقنية التي تختارها)* |
| **CMS Navbar & Sidebar**<br>*(الشريط العلوي والجانبي)* | Navbar and Sidebar scroll away or break on mobile.<br>*(تختفي القائمة عند التمرير وتنكسر على الجوال)* | **Sticky Top Nav (`sticky top-0`) + Sticky Sidebar (`h-dvh`)** + Mobile Drawer automatically.<br>*(شريط علوي وجانبي ثابت دائماً + قائمة منسدلة للجوال)* |
| **CMS Data Tables & Forms**<br>*(الجداول والنماذج)* | Wide tables push the page off-screen; forms have no validation or loading states.<br>*(الجداول العريضة تكسر الشاشة والنماذج بدون تحقق)* | **`flex-1 min-w-0` + Horizontal Scroll Tables**, Sticky Headers, Pagination, 5 UI States, and Sticky Form Save Bar.<br>*(جداول متجاوبة مع بحث وترقيم صفحات + نماذج احترافية)* |
| **Arabic & English (RTL/LTR)**<br>*(دعم العربية والإنجليزية)* | Uses `left`/`right` CSS so Arabic layouts look backwards.<br>*(يستخدم اتجاهات ثابتة فتظهر العربية بشكل معكوس)* | Enforces **CSS Logical Properties** (`/rtl-logical-guard`) so Arabic & English both work 100%.<br>*(يدعم العربية والإنجليزية تلقائياً بدون كسر التصميم)* |
| **Backend & Security**<br>*(الباك-إند والأمان)* | Anyone can call APIs or delete records; file uploads are unsafe.<br>*(ثغرات أمنية وغياب صلاحيات المستخدمين)* | Mandatory **RBAC Roles (Admin/Editor/User)**, Server Validation, Pagination, and Safe File Uploads.<br>*(حماية الصلاحيات، التحقق من البيانات، ورفع الملفات بأمان)* |
| **Database Integrity**<br>*(قواعد البيانات)* | Missing indexes, slow N+1 queries, accidental permanent deletes.<br>*(قاعدة بيانات بطيئة وحذف نهائي للبيانات بالخطأ)* | Mandatory **Foreign Keys, Indexes, Soft Deletes (`deleted_at`), and Transactions**.<br>*(علاقات وفهارس سريعة وحذف آمن قابل للاسترجاع)* |
| **Internet Data Usage**<br>*(استهلاك الإنترنت)* | Downloads background updates and re-downloads packages every time.<br>*(يستهلك الإنترنت في الخلفية ويعيد تحميل الحزم)* | **`/save-data` cuts background internet usage by 75–85%** and uses offline package caches.<br>*(يوفر 75–85% من استهلاك الإنترنت ويستخدم الكاش المحلي)* |

> [!TIP]
> **Live Proof — We Used `.agents` to Build This Handbook!**
> Even this Handbook and its 11 shortcut commands were built using the exact tools inside this repo:
> 1. **Pre-Coding Architecture (`/web-precode`):** Audited at **100% Clearance** in [`docs/precode/handbook/`](file:///d:/Skills/.agents/docs/precode/handbook/01-PRD.md).
> 2. **Specification-Driven Implementation (`/spec-kit`):** Specified, planned, and executed step-by-step in [`specs/001-beginner-handbook/`](file:///d:/Skills/.agents/specs/001-beginner-handbook/spec.md).

---

## 🚦 2. How It Works: The "1-2-3 Traffic Light" Rule
### كيف يعمل النظام؟ (قاعدة إشارة المرور 1-2-3)

You never need to memorize 60 skills. Every task follows **3 simple steps**:

1. 🔴 **Step 1: Paste ONE Command + Your Idea (in Arabic or English)**
   Pick your situation below, copy the prompt into the **AI Chat Box**, and describe what you want in plain words.
2. 🟡 **Step 2: Answer the AI's Questions (Click `(Recommended)` When Unsure!)**
   Before writing code, the AI will interview you step-by-step (`/grill-me` + `/muaz-skill`). **Beginner secret:** The best answer is always marked `(Recommended)` as the first choice—if you don't know a technical detail, just pick `(Recommended)`!
3. 🟢 **Step 3: It Builds, Checks Itself & Gives You a "How to Test It" Card**
   Once you say `"yes"` to the summary, the AI writes the code, runs its own UI/Security/Test checks automatically, fixes any bugs, and gives you a simple **"How to Test It"** box telling you exactly what to click.

---

### ⚠️ Crucial Beginner Note: Where Do I Type This?
### ملاحظة هامة للمبتدئين: أين أكتب هذه الأوامر؟

In every guide box below, look at the icon:
* 💬 **Paste in AI Chat (الصق في شات الذكاء الاصطناعي):** Type or paste this directly where you chat with the AI assistant. **(99% of everything in this book is pasted in AI Chat!)**
* 💻 **Paste in Terminal (الصق في التيرمينال / سطر الأوامر):** Only used if you prefer running setup manually in PowerShell/CMD.

---

## 🛠️ 3. One-Time Setup (Takes 60 Seconds)
### التثبيت لأول مرة (خلال دقيقة واحدة فقط)

You don't even need to touch the Terminal. Just copy and paste this box into your **AI Chat**:

> 💬 **Paste in AI Chat (الصق هذا النص في شات الذكاء الاصطناعي):**
> ```text
> Please set up Agent OS for me:
> 1. Run `python scripts/agent_os.py sync --apply` to install all skills and rules globally.
> 2. Run `python scripts/agent_os.py install-hooks` to enable local git safety checks.
> 3. Run `python scripts/agent_os.py data-saver apply` to enable low-bandwidth mode and offline package caching.
> Tell me in simple words when everything is 100% ready.
> ```

*(After running setup the very first time, close and reopen Antigravity IDE once so all `/commands` appear in your chat menu.)*

---

## ⚡ 4. Start Here in 30 Seconds: The Top 4 Magic Commands
### ابدأ هنا في 30 ثانية: أهم 4 أوامر يومية

If you only remember **4 commands**, you can build and fix almost anything:

| What do you want to do? (ماذا تريد أن تفعل؟) | 💬 Paste This in AI Chat (الصق هذا في شات الذكاء الاصطناعي) |
| :--- | :--- |
| **1. Save Internet Data & Get Fast Replies**<br>*(توفير باقة الإنترنت وتسريع الردود)* | `/save-data` |
| **2. Start a Brand New Project from Zero**<br>*(بداية مشروع جديد من الصفر بأي تقنية)* | `/start-project [write your app idea in Arabic or English]` |
| **3. Add ANY New Feature (Auto-Picks Skills)**<br>*(إضافة أي ميزة جديدة — يختار المهارات تلقائياً)* | `/smart-feature [describe your feature in Arabic or English]` |
| **4. Fix UI Violations, Broken Sidebar, or Tables**<br>*(إصلاح مشاكل الواجهة أو القائمة الجانبية أو الجداول)* | `/fix-ui` |

---

## 🧩 5. All 11 Situation Cards (Short `/Command` + Full Copy-Paste Prompts)
### دليل الحالات الـ 11 الكامل (الأمر المختصر + النص الكامل الجاهز للنسخ)

Find your exact situation below. You can either use **Option A (The 1-Word Shortcut)** or **Option B (The Full Copy-Paste Prompt)**.
> 💡 **Note:** In every `[ ... ]` placeholder below, you can write your description in **Arabic or English**, and you can specify **any tech stack you want** (or let the AI auto-detect it from your project).

---

### 🖼️ Situation 1: You Have UI Violations, Broken Sticky Nav/Sidebar, Tables, or Forms
#### الحالة 1: لديك مشاكل في الواجهة، أو القائمة العلوية/الجانبية غير ثابتة، أو الجداول والنماذج مكسورة

* **What it does (ماذا يفعل؟):** Automatically scans your UI with `/ui-audit`, generates fix prompts for every violation, fixes Sticky Navbars, Sticky Sidebars, overflowing CMS Tables (`min-w-0`), Forms, Mobile/Tablet/Desktop responsiveness, and Arabic/English RTL issues, then verifies the result with `/ui-review-loop`.

**Option A — 1-Word Shortcut (💬 Paste in AI Chat):**
```text
/fix-ui [optional: mention the page or folder, or leave blank to scan the whole UI]
```

**Option B — Full Copy-Paste Prompt (💬 Paste in AI Chat):**
```text
Use /fix-ui (/ui-audit, /muaz-skill, /rtl-logical-guard, /ui-review-loop, and /clean-code-guard) to scan my UI, automatically generate the fix prompts for all violations, and fix them now.
Specifically check and fix:
1. Top Navbar must stay sticky (sticky top-0 z-40) and Sidebar must stay sticky with independent scroll on desktop (lg:sticky lg:top-0 lg:h-dvh lg:overflow-y-auto) plus a working mobile drawer on <1024px.
2. Main content wrapper must have flex-1 min-w-0 so wide tables never push or break the page layout.
3. Data tables must scroll horizontally inside their card (overflow-x-auto), have sticky headers, and include Idle, Loading, Empty, and Error states.
4. Forms must be aligned in a responsive grid with field validation states and a sticky bottom Save/Cancel bar.
5. Full responsiveness across Mobile, Tablet, and Desktop in both LTR (English) and RTL (Arabic).
```

---

### 🎨 Situation 2: Starting a New Frontend / CMS UI Feature (Any Tech Stack)
#### الحالة 2: بناء ميزة واجهة أمامية جديدة (صفحة، لوحة تحكم، جدول، أو نموذج — بأي تقنية)

* **Works with ANY Frontend stack:** React, Next.js, Vue, Nuxt, Laravel Blade/Livewire/Filament, Angular, Svelte, Astro, HTML/Tailwind, or WordPress.
* **What it does (ماذا يفعل؟):** Interviews you first via `/grill-me` + `/muaz-skill` Smart Intake, designs the UI blueprint, enforces CMS Sticky Nav/Sidebar/Tables/Forms + RTL rules, builds the code, and auto-checks it.

**Option A — 1-Word Shortcut (💬 Paste in AI Chat):**
```text
/feature-fe Stack: [your stack or "auto-detect"] | Feature: [describe your page, table, or form in Arabic or English]
```

**Option B — Full Copy-Paste Prompt (💬 Paste in AI Chat):**
```text
I am starting a new frontend feature.
Preferred Frontend Stack: [write your stack, e.g., React / Next.js / Vue / Blade / HTML-Tailwind, or "auto-detect from project"]
Feature Description: [describe what you want to build in Arabic or English]

Follow the /feature-fe workflow:
1. First, auto-detect my project files and interview me step-by-step using /grill-me and the Smart Intake questions in /muaz-skill (references/intake-template.md) with (Recommended) defaults. Show the Confirmation Summary and wait for my "yes" before writing code.
2. Activate /muaz-skill, /rtl-logical-guard, /ui-review-loop, /clean-code-guard, and /test-guard (plus /nextjs-fullstack if Next.js or /wp-guard if WordPress).
3. Enforce CMS Frontend Armor: sticky top navbar (sticky top-0 z-40), sticky desktop sidebar (lg:sticky lg:top-0 lg:h-dvh lg:overflow-y-auto) with mobile drawer, flex-1 min-w-0 main column, responsive overflow-x-auto tables with sticky headers/pagination and all 5 UI states (Idle/Loading/Success/Error/Empty), responsive forms with sticky Save/Cancel bar, and 100% responsiveness across Mobile/Tablet/Desktop in both LTR and RTL.
4. After coding, run the UI review loop automatically, fix any issues, and show me a simple "How to Test It" card.
```

---

### ⚙️ Situation 3: Starting a New Frontend + Backend Feature (Any Tech Stack)
#### الحالة 3: بناء ميزة تشمل الواجهة الأمامية + الباك-إند (APIs، صلاحيات، تحقق، رفع ملفات)

* **Works with ANY Frontend + Backend stack:** Next.js/React, Vue/Laravel, Blade/Livewire, Node/Express/NestJS, Python/FastAPI/Django, Go, etc.
* **What it does (ماذا يفعل؟):** Runs the full `/grill-me` + `/muaz-skill` intake, builds the CMS Frontend **PLUS** Backend APIs, RBAC Role/Permission checks (Admin/Editor/User), Server-Side Pagination/Search/Sort for tables, Server-Side Form Validation, and Safe File/Image Uploads.

**Option A — 1-Word Shortcut (💬 Paste in AI Chat):**
```text
/feature-febe Stack: [your FE + BE stack or "auto-detect"] | Feature: [describe your feature in Arabic or English]
```

**Option B — Full Copy-Paste Prompt (💬 Paste in AI Chat):**
```text
I am starting a new Frontend + Backend feature.
Preferred Tech Stack: [write your Frontend + Backend stack, or "auto-detect from project"]
Feature Description: [describe your feature in Arabic or English]

Follow the /feature-febe workflow:
1. First, auto-detect my project files and interview me step-by-step using /grill-me and /muaz-skill Smart Intake (references/intake-template.md) with (Recommended) defaults. Show the Confirmation Summary and wait for my "yes" before coding.
2. Activate Frontend skills (/muaz-skill, /rtl-logical-guard, /ui-review-loop) AND Backend skills (/backend-api, /backend-http, /backend-identity, /backend-ops, /clean-code-guard, /test-guard, plus /laravel-mastery & /pest-security-guard if Laravel, or /nextjs-fullstack & /next-server-action-guard if Next.js).
3. Enforce CMS Frontend Armor (sticky nav, sticky sidebar + mobile drawer, flex-1 min-w-0 main wrapper, responsive tables with 5 UI states, responsive forms, all-media LTR/RTL).
4. Enforce CMS Backend Armor:
   - Role & Permission Guards (RBAC: Admin/Editor/User) on both UI buttons and backend endpoints + anti-IDOR ownership checks.
   - Server-side Pagination, Search, Filtering, and Sorting wired to the frontend table.
   - Server-side Form Validation returning clear field-by-field errors (422) to the frontend form.
   - Safe File & Image Uploads (MIME/size validation, preview URLs, and deleting old files on update/delete).
5. Auto-verify UI, security, and tests, then show me a plain-language "How to Test It" card.
```

---

### 🗄️ Situation 4: Starting a Full Feature: Frontend + Backend + Database (Any Stack)
#### الحالة 4: بناء ميزة كاملة من الألف إلى الياء: واجهة أمامية + باك-إند + قاعدة بيانات

* **Works with ANY Frontend, Backend & Database:** MySQL, PostgreSQL, SQLite, MongoDB, Firebase/Firestore, Supabase, Prisma, Drizzle, Laravel Eloquent, etc.
* **What it does (ماذا يفعل؟):** Everything in `/feature-febe` **PLUS** Database Schema design, Migrations, Foreign Keys (`ON DELETE RESTRICT`/`CASCADE`), Indexes for fast search/filtering, Soft Deletes (`deleted_at`), N+1 query prevention, and atomic Transactions.

**Option A — 1-Word Shortcut (💬 Paste in AI Chat):**
```text
/feature-full Stack: [your FE + BE + DB stack or "auto-detect"] | Feature: [describe your feature in Arabic or English]
```

**Option B — Full Copy-Paste Prompt (💬 Paste in AI Chat):**
```text
I am starting a complete Frontend + Backend + Database feature.
Preferred Tech Stack: [write your Frontend, Backend, and Database stack, or "auto-detect from project"]
Feature Description: [describe your feature in Arabic or English]

Follow the /feature-full workflow:
1. First, auto-detect my project files and interview me step-by-step using /grill-me and /muaz-skill Smart Intake (references/intake-template.md) with (Recommended) defaults. Show the Confirmation Summary and wait for my "yes" before coding.
2. Activate Database skills (/database, /backend-data), Backend skills (/backend-api, /backend-http, /backend-identity, /backend-ops + stack security guards), and Frontend skills (/muaz-skill, /rtl-logical-guard, /ui-review-loop) + /clean-code-guard and /test-guard.
3. Enforce CMS Database Armor:
   - Explicit Foreign Keys (ON DELETE RESTRICT/CASCADE), Indexes on all foreign keys and search/filter columns, Soft Deletes (deleted_at) so CMS records aren't lost by mistake, zero N+1 queries (eager loading), and database transactions for multi-table writes.
4. Enforce CMS Backend Armor:
   - RBAC Role & Permission Guards (Admin/Editor/User), Server-Side Pagination/Search/Filter/Sort, Field-Level Form Validation, and Safe File/Image Uploads with old-file cleanup.
5. Enforce CMS Frontend Armor:
   - Sticky Top Navbar, Sticky Sidebar (h-dvh) + mobile drawer, flex-1 min-w-0 main column, responsive overflow-x-auto Data Tables with 5 UI states, responsive Forms with sticky Save/Cancel bar, and full LTR/RTL responsiveness across Mobile, Tablet, and Desktop.
6. Run automatic UI, security, and test checks, fix any issues, and finish with a plain-language "How to Test It" card.
```

---

### 🚀 Situation 5: Starting a Brand New Project from Zero (Any Tech Stack)
#### الحالة 5: بدء مشروع جديد بالكامل من الصفر (مقابلة التخطيط + التوثيق المعماري + البناء)

* **What it does (ماذا يفعل؟):** Interviews you with `/grill-me` + the 28 Smart Intake questions in `/muaz-skill`, generates the 6 Pre-Coding architecture documents (`/web-precode`), breaks the build into ordered tasks (`/spec-kit`), and builds the entire foundation in your chosen stack.

**Option A — 1-Word Shortcut (💬 Paste in AI Chat):**
```text
/start-project [describe your project idea in Arabic or English]
```

**Option B — Full Copy-Paste Prompt (💬 Paste in AI Chat):**
```text
I want to start a brand new project from zero: [describe your project idea in Arabic or English].

Follow the /start-project workflow:
1. Interview me first using /grill-me and the Smart Intake grill questions from /muaz-skill (references/intake-template.md, Q1–Q28 in Frontier Rounds) with (Recommended) options. Ask me about Purpose, Design Tone, Pages, Sticky Nav/Sidebar layout, my preferred Frontend, Backend, and Database stack, Auth/Roles, and Arabic/English RTL support. Show me the Phase 1E Confirmation Summary and wait for my "yes" before writing code.
2. Once I confirm, create and audit the 6 Pre-Coding Architecture Pillars using /web-precode (01-PRD through 06-IMPLEMENTATION_PLAN) and generate the Spec-Kit plan and task list using /spec-kit (/speckit-specify, /speckit-plan, /speckit-tasks).
3. Build the project using my chosen stack with full CMS Frontend Armor (sticky nav/sidebar, responsive tables/forms, RTL/LTR), Backend Armor (RBAC, validation, pagination, safe uploads), and Database Armor (foreign keys, indexes, soft deletes).
4. Auto-verify everything and finish with a beginner-friendly "How to Test It" card.
```

---

### 🧠 Situation 6: "I Only Have a Feature Description — Pick the Best Skills for Me!"
#### الحالة 6: لدي وصف للميزة فقط — دع النظام يختار أفضل المهارات تلقائياً ويبنيها!

* **When to use it (متى تستخدمه؟):** When you don't know whether your feature needs Frontend only, Backend, or Database changes. Just describe what you want in plain words!

**Option A — 1-Word Shortcut (💬 Paste in AI Chat):**
```text
/smart-feature [describe your feature in plain Arabic or English]
```

**Option B — Full Copy-Paste Prompt (💬 Paste in AI Chat):**
```text
Here is the feature I want to build: [describe your feature in Arabic or English].
Use /smart-feature:
1. Inspect my project files and automatically select the best targeted Frontend, CMS, Backend, Database, and Security skills for this description. Tell me briefly which stack and skills you activated.
2. Run the full /grill-me + /muaz-skill Smart Intake interview (with (Recommended) defaults) and wait for my "yes" on the Confirmation Summary before writing code.
3. Build the feature enforcing all CMS Frontend, Backend, and Database protections that apply to this feature.
4. Auto-run UI, security, and test checks, fix any issues, and show me a simple "How to Test It" card.
```

---

### 🛒 Situation 7: Building a WordPress or WooCommerce Feature / Theme / Plugin
#### الحالة 7: بناء ميزة أو قالب أو إضافة ووردبريس / ووكومرس (WordPress / WooCommerce)

* **What it does (ماذا يفعل؟):** Chains `/grill-me` + `/muaz-skill` + `/wp-guard` + `/woo-guard` + `/rtl-logical-guard` + `/database` so your plugin/theme is 100% secure (nonces, capabilities, prepared SQL) and WooCommerce HPOS-compatible.

**Option A — 1-Word Shortcut (💬 Paste in AI Chat):**
```text
/feature-wp [describe your WordPress or WooCommerce feature in Arabic or English]
```

**Option B — Full Copy-Paste Prompt (💬 Paste in AI Chat):**
```text
I want to build a WordPress / WooCommerce feature: [describe feature in Arabic or English].
Use /feature-wp:
1. Run /grill-me + /muaz-skill Smart Intake first and wait for my "yes" on the Confirmation Summary.
2. Activate /wp-guard, /woo-guard, /muaz-skill, /rtl-logical-guard, /database, and /clean-code-guard.
3. Enforce WordPress nonces, capability checks (current_user_can), input sanitization, output escaping, $wpdb->prepare(), WooCommerce HPOS CRUD methods, and responsive RTL/LTR layouts.
4. Auto-check all modified files and show me a simple "How to Test It in wp-admin / Storefront" card.
```

---

### 🐛 Situation 8: Fixing a Backend, API, Login/Permission, Validation, or Database Bug
#### الحالة 8: إصلاح خطأ في الباك-إند، أو الـ API، أو الصلاحيات، أو بطء/مشكلة في قاعدة البيانات

**Option A — 1-Word Shortcut (💬 Paste in AI Chat):**
```text
/fix-backend [paste the error message or describe what is not working]
```

**Option B — Full Copy-Paste Prompt (💬 Paste in AI Chat):**
```text
Something is broken in my backend/database: [paste error or describe what happens in Arabic or English].
Use /fix-backend (/backend-api, /backend-data, /database, /backend-identity, /test-guard, and my stack's security guards):
1. Trace the exact bug from the frontend request to the API controller, validation, RBAC permissions, and database query.
2. Explain why it broke in 2 simple sentences, then fix it safely (checking RBAC, 422 validation errors, pagination/N+1 queries, file uploads, and DB foreign keys/soft deletes).
3. Write or run a test to make sure the bug stays fixed, and show me a simple "How to Test It" card.
```

---

### 🛡️ Situation 9: Checking Code, Security & Deleting Bloat Before Pushing to GitHub
#### الحالة 9: فحص الكود والأمان وحذف التعقيد الزائد قبل رفع التعديلات (Push / PR)

**Option A — 1-Word Shortcut (💬 Paste in AI Chat):**
```text
/check-all
```

**Option B — Full Copy-Paste Prompt (💬 Paste in AI Chat):**
```text
Use /check-all (/clean-code-guard, /test-guard, /rtl-logical-guard, /next-server-action-guard, /pest-security-guard, /ponytail-review, and /debate-review) to review my recent changes.
Check for security holes, missing RBAC permissions, broken CMS layout/RTL rules, missing tests, and unnecessary code bloat. Fix safe issues automatically and give me a clear READY TO PUSH or FIX NEEDED summary.
```

---

### 📄 Situation 10: Documenting an Existing or Messy Project for Other Developers
#### الحالة 10: كتابة أو تحديث توثيق شامل للمشروع (`README` و `ARCHITECTURE` و `API`)

**Option A — 1-Word Shortcut (💬 Paste in AI Chat):**
```text
/doc-project
```

**Option B — Full Copy-Paste Prompt (💬 Paste in AI Chat):**
```text
Use /doc-project (/project-documentation and /docs-guard) to scan this codebase and generate or update a beginner-friendly README.md (with exact step-by-step setup commands), docs/ARCHITECTURE.md, and docs/API.md. Verify that every command and file path mentioned actually exists in the project.
```

---

### 📶 Situation 11: Limited Internet / Mobile Data Mode (Save 75–85% Bandwidth & Tokens)
#### الحالة 11: وضع توفير الإنترنت والبيانات (يقلل استهلاك الإنترنت بنسبة 75–85% ويسرع الردود)

* **Important FAQ:** *Does `/save-data` stop the AI from downloading a new package if a new feature needs one?*
  **No!** When you use `--prefer-offline`, it checks your computer's local cache first (0 MB used if you already installed that package before), and **only connects to the internet to download brand-new packages**.

**Option A — 1-Word Shortcut (💬 Paste in AI Chat):**
```text
/save-data
```

**Option B — Full Copy-Paste Prompt (💬 Paste in AI Chat):**
```text
Use /save-data (/data-saver and /caveman lite):
1. Run `python scripts/agent_os.py data-saver apply` to ensure my IDE is not wasting internet bandwidth in the background.
2. Use offline-first flags (`npm install --prefer-offline --no-audit --no-fund`, `composer install --prefer-dist`, `pip install --prefer-binary`) whenever installing packages.
3. Keep chat replies concise and high-signal so responses load fast on mobile data.
```

---

## 🏰 6. What `.agents` Protects Automatically (Behind the Scenes)
### ما الذي يحميه النظام تلقائياً في الخلفية دون تدخل منك؟

Even when you don't type a single guard name, these protections are **built into the combo commands**:

### A. CMS Frontend Armor (درع الواجهة الأمامية ولوحات التحكم)
1. **Sticky Top Navbar:** `sticky top-0 z-40` — never disappears when scrolling down.
2. **Sticky Sidebar Panel:** `lg:sticky lg:top-0 lg:h-dvh lg:w-64 lg:shrink-0 lg:overflow-y-auto` on desktop + slide-out mobile drawer on `<1024px`.
3. **Main Column Overflow Lock (`flex-1 min-w-0`):** Stops wide tables from pushing the sidebar or breaking mobile screens.
4. **CMS Data Tables:** Wrapped in `overflow-x-auto`, sticky table headers, server-wired search/filter/sort/pagination, and all **5 UI States** (`Idle`, `Loading` skeletons, `Success`, `Error`, `Empty`).
5. **CMS Forms:** Responsive multi-column grids, field-by-field validation error text, loading state on submit, and a sticky bottom `Save / Cancel` bar.
6. **All-Media + Arabic/English RTL:** Tested at Mobile (`375px`), Tablet (`768px`), Laptop (`1024px`), and Desktop (`1280px+`) using CSS Logical Properties (`ms-`, `me-`, `ps-`, `pe-`, `start-`, `end-`).

### B. CMS Backend & Database Armor (درع الباك-إند وقاعدة البيانات)
1. **RBAC Role & Permission Guards:** Admin vs. Editor vs. User permissions enforced on **both** UI buttons and backend API routes + anti-IDOR ownership checks.
2. **Server-Side Pagination, Search & Sort:** Large CMS tables never freeze or crash the browser.
3. **Field-Level Server Validation:** Returns clean `422` errors mapped to each form input instead of `500` server crashes.
4. **Safe File & Image Uploads:** Checks file type & max size, generates safe filenames, returns preview URLs, and deletes old files when updated/deleted.
5. **Database Integrity:** Explicit Foreign Keys (`ON DELETE RESTRICT`/`CASCADE`), Indexes on foreign keys and search columns, Soft Deletes (`deleted_at`), zero N+1 queries, and atomic database transactions.

---

## 📚 7. Complete All-Commands Copy-Paste Directory (All 85 Skills + 28 CLI Tools)
### الدليل الكامل لجميع الأوامر الـ 85 وأدوات سطر الأوامر الـ 28 (متى وكيف تستخدمها + الوصف + أمر جاهز للنسخ)

Below is every single command in `.agents`, organized by domain so your team knows **when to use it**, **what it does**, and has a **ready copy-paste command** for AI Chat or Terminal.

---

### A. Core Architecture, Intake, Critique & Daily Planning (7 Skills)

| Command | When & How to Use | Description | 💬 Ready Copy-Paste Command |
| :--- | :--- | :--- | :--- |
| **`/engineering-workflow`** | Use on any engineering task, bug fix, refactoring, or architecture decision when you want full senior discipline. | Enforces Stage 0 Read-Only Intake, Independent Critical Thinking & Debate, Karpathy's 4 Coding Laws, backward root-cause tracing, and Goal-Driven Verification. | `/engineering-workflow Evaluate the best architecture for [feature/bug], surface trade-offs, and implement with verification.` |
| **`/intake`** | Use on any new feature request, multi-part UI edit, or ambiguous prompt before writing code. | Inspects the repo in Read-Only mode first, builds the 3-Layer Impact Map (`UI -> Backend API -> Database Schema`), locks a `Do-Not-Remove` list of existing UI elements, and opens the `ask_question` dialog. | `/intake Map the 3-layer impact (UI, API, DB) and Do-Not-Remove lock list for adding [feature].` |
| **`/critique`** | Use after drafting a complex plan or specification (before writing code) to catch blind spots. | Audits the draft plan against codebase truth, hidden Backend/DB impact, accidental UI removals, missing 6-state matrix coverage, and over-engineering. | `/critique Audit our proposed implementation plan against codebase truth, missing DB persistence, and UI regressions.` |
| **`/plan-daily`** | Use at the start of a work session to triage today's focus, or when creating/upgrading an Agent OS skill. | Inspects `git status` and `SESSION_SNAPSHOT.md` to propose 1 Primary Focus + 2 Secondary tasks, or scaffolds and syncs new skills/CLI tools. | `/plan-daily Inspect current git status and SESSION_SNAPSHOT.md and propose today's primary engineering focus.` |
| **`/find-skills`** | Use when you ask *"is there a skill for X?"* or want the agent to recommend the right slash commands. | Searches the installed 85-skill catalog and matches your plain-language goal to the exact skill chain. | `/find-skills Which skills and commands should I use to build and audit [your task]?` |
| **`/delegate-setup`** | Use once when configuring which local AI CLI (`opencode`, `claude`, `codex`) handles delegated tasks. | Discovers installed implementer CLIs and configures delegation fleet lanes after your approval. | `/delegate-setup Discover installed AI CLIs and propose a delegation lane configuration.` |
| **`/opencode-delegate`** | Use when you explicitly want to dispatch a bounded coding task to the OpenCode CLI in the background. | Packages a bounded task brief, runs OpenCode CLI (`--owner-approved`), and reviews the resulting git diff before landing. | `/opencode-delegate Delegate implementing [module] to OpenCode CLI and review the diff when finished.` |

---

### B. Pre-Coding Architecture & Specification-Driven Development (12 Skills)

| Command | When & How to Use | Description | 💬 Ready Copy-Paste Command |
| :--- | :--- | :--- | :--- |
| **`/web-precode`** | Use before coding a new app or major module to author all 6 architecture documents. | Authors and validates `01-PRD.md`, `02-TRD.md`, `03-APP_FLOW.md` (with 5-State UI Matrix), `04-DESIGN_BRIEF.md`, `05-BACKEND_SCHEMA.md` (ERD), and `06-IMPLEMENTATION_PLAN.md`. | `/web-precode Author all 6 Pre-Coding architecture documents in docs/precode/ for [feature] and run precode audit.` |
| **`/spec-kit`** | Use to run the full GitHub Spec-Kit Specification-Driven Development (SDD) lifecycle. | Guides a feature from constitution and specification through clarification, planning, task breakdown, analysis, and implementation. | `/spec-kit Initialize the Specification-Driven Development workflow for [feature].` |
| **`/speckit-constitution`** | Use to establish or update your project's non-negotiable architectural and security rules. | Creates or updates the project constitution (`MASTER.md` / `.specify/memory/constitution.md`). | `/speckit-constitution Create or update the project constitution with our stack and security invariants.` |
| **`/speckit-specify`** | Use to turn a plain-language feature description into a structured `spec.md`. | Authors user stories, functional requirements, edge cases, and measurable acceptance criteria in `spec.md`. | `/speckit-specify Write a formal feature specification (spec.md) for [feature] with acceptance criteria.` |
| **`/speckit-clarify`** | Use right after `/speckit-specify` to resolve any underspecified requirements. | Identifies up to 5 high-impact ambiguities in `spec.md`, asks targeted multiple-choice questions, and writes your answers back into `spec.md`. | `/speckit-clarify Audit spec.md for underspecified business rules and ask up to 5 targeted clarification questions.` |
| **`/speckit-plan`** | Use after `spec.md` is clear to generate the technical architecture plan (`plan.md`). | Produces data models, API contracts, component hierarchy, and step-by-step architecture in `plan.md`. | `/speckit-plan Generate the technical implementation plan (plan.md) and API contracts from spec.md.` |
| **`/speckit-checklist`** | Use to generate a custom requirement, security, and UX checklist for the active spec. | Creates a verification checklist in the spec folder so no acceptance criterion is missed during coding. | `/speckit-checklist Generate a pre-implementation verification checklist for the active feature spec.` |
| **`/speckit-tasks`** | Use after `plan.md` is ready to generate a dependency-ordered `tasks.md`. | Breaks the plan into small, testable, dependency-ordered tasks with exact file paths and verification commands. | `/speckit-tasks Generate an actionable, dependency-ordered tasks.md from spec.md and plan.md.` |
| **`/speckit-analyze`** | Use after `tasks.md` is generated (before coding) to verify cross-artifact consistency. | Audits `spec.md`, `plan.md`, and `tasks.md` to ensure every requirement maps to a task and zero schema conflicts exist. | `/speckit-analyze Run a cross-artifact consistency analysis across spec.md, plan.md, and tasks.md.` |
| **`/speckit-implement`** | Use to execute all tasks in `tasks.md` step-by-step with verification gates. | Processes each task in `tasks.md` in dependency order, running build/test verification before marking tasks complete. | `/speckit-implement Execute the pending tasks in tasks.md with goal-driven verification after each step.` |
| **`/speckit-converge`** | Use when a feature is partially built and you want to find and finish what is still missing. | Compares the live codebase against `spec.md`, `plan.md`, and `tasks.md`, then appends remaining unbuilt items to `tasks.md`. | `/speckit-converge Compare the current codebase against spec.md and append any unbuilt requirements to tasks.md.` |
| **`/speckit-taskstoissues`** | Use when you want to export `tasks.md` into GitHub Issues for team tracking. | Converts dependency-ordered tasks in `tasks.md` into structured GitHub Issues via the GitHub MCP server. | `/speckit-taskstoissues Convert the tasks in tasks.md into dependency-ordered GitHub issues.` |

---

### C. All-in-One Situation Combos (11 Skills)

| Command | When & How to Use | Description | 💬 Ready Copy-Paste Command |
| :--- | :--- | :--- | :--- |
| **`/start-project`** | Starting a brand new application from scratch in any tech stack. | Interviews you (`Q1-Q28`), generates the 6 Pre-Coding docs (`/web-precode`), creates Spec-Kit tasks (`/spec-kit`), and builds the full-stack foundation. | `/start-project Build a bilingual SaaS dashboard with authentication, role permissions, and analytics.` |
| **`/smart-feature`** | Adding any feature when you want `.agents` to auto-detect the right Frontend, Backend, DB, and Security skills. | Inspects your repo, announces the selected skill chain, runs Smart Intake, builds the feature, and verifies UI/security/tests. | `/smart-feature Add a customer invoices page where admins can filter by status and export to CSV.` |
| **`/feature-fe`** | Building a Frontend / CMS UI page, table, modal, or form in any frontend stack. | Runs Smart Intake and builds the UI enforcing Sticky Navbar, Sticky Sidebar (`h-dvh`), responsive Data Tables (`overflow-x-auto`), Forms, and RTL/LTR parity. | `/feature-fe Build a responsive products management table with status filter, search, and edit modal.` |
| **`/feature-febe`** | Building a feature that requires both Frontend UI and Backend API endpoints/validation/auth. | Chains `/feature-fe` with `/backend-api`, `/backend-identity`, RBAC role guards, `422` validation, server pagination, and safe uploads. | `/feature-febe Build a team members management screen wired to REST endpoints with Admin-only RBAC and validation.` |
| **`/feature-full`** | Building a complete end-to-end feature across Frontend UI + Backend API + Database migrations. | Chains `/feature-febe` with `/database` and `/backend-data` (foreign keys, compound indexes, soft deletes, eager loading, and ACID transactions). | `/feature-full Create a coupons module with database migration, CRUD endpoints, validation, and admin DataTable.` |
| **`/feature-wp`** | Building or customizing a WordPress theme, plugin, block, or WooCommerce store feature. | Chains `/wp-guard`, `/woo-guard`, `/rtl-logical-guard`, and `/database` to enforce nonces, capability checks, `$wpdb->prepare()`, and HPOS CRUD. | `/feature-wp Build a custom WooCommerce wholesale discount plugin with an admin settings table and HPOS compatibility.` |
| **`/fix-ui`** | Fixing broken Sticky Navbars, Sidebars, overflowing tables, unaligned forms, or broken Arabic RTL layouts. | Scans your frontend with `/ui-audit`, generates structured fix prompts, repairs layout/RTL violations, and verifies via `/ui-review-loop`. | `/fix-ui Scan the admin dashboard and fix the horizontal table overflow, sticky sidebar, and RTL icon padding.` |
| **`/fix-backend`** | Fixing a `500`/`422`/`403`/`401` API error, broken auth/permission check, upload failure, or slow DB query. | Traces the bug from Frontend request to DB query, fixes the root cause safely, and writes a regression test. | `/fix-backend Fix the 500 error on order creation, prevent duplicate submissions, and add a regression test.` |
| **`/check-all`** | Auditing all modified code before `git commit`, `git push`, or opening a Pull Request. | Chains `/clean-code-guard`, `/test-guard`, `/rtl-logical-guard`, stack security guards, `/ponytail-review`, and `/debate-review` for a `READY TO PUSH` verdict. | `/check-all Audit all modified files for security, RTL logical properties, test quality, and code simplicity before pushing.` |
| **`/doc-project`** | Generating or updating beginner-friendly `README.md`, `docs/ARCHITECTURE.md`, and `docs/API.md`. | Scans real routes, schemas, and `.env` keys with `/project-documentation` and verifies zero drift with `/docs-guard`. | `/doc-project Scan the repository and update README.md, docs/ARCHITECTURE.md, and docs/API.md.` |
| **`/save-data`** | Working on mobile hotspot or metered internet to cut bandwidth by 75–85% and get concise replies. | Applies `data-saver` IDE rules, enforces `--prefer-offline` package flags, and activates `/caveman lite` concise output. | `/save-data Activate low-bandwidth mode, configure offline package caching, and use concise responses.` |

---

### D. Frontend, UI Design, Google Stitch & Browser Verification (22 Skills)

| Command | When & How to Use | Description | 💬 Ready Copy-Paste Command |
| :--- | :--- | :--- | :--- |
| **`/muaz-skill`** | Designing or building any frontend website, landing page, or CMS dashboard. | Powered by 91 UI styles, 169 color palettes, and 72 font pairings; outputs a calibrated design blueprint (`60-30-10` tokens) before writing production code. | `/muaz-skill Design and build a high-craft analytics dashboard with 60-30-10 tokens and responsive cards.` |
| **`/nextjs-fullstack`** | Building Next.js 15+ / React 19 App Router pages, layouts, Server Components, and Server Actions. | Enforces Server vs. Client Component boundaries, Suspense streaming, Partial Prerendering (PPR), and Tailwind CSS v4 best practices. | `/nextjs-fullstack Build the orders route using Next.js App Router Server Components and validated Server Actions.` |
| **`/shadcn-ui`** | Installing, customizing, or composing accessible `shadcn/ui` + Radix + Tailwind components. | Enforces accessible Dialogs, DataTables, Forms, keyboard navigation, focus rings, and semantic token theming. | `/shadcn-ui Add an accessible DataTable with filter toolbar, status pills, and CRUD modal using shadcn/ui.` |
| **`/rtl-logical-guard`** | Building or auditing bilingual Arabic/English (`RTL`/`LTR`) components and stylesheets. | Replaces physical CSS classes (`ml-*`, `mr-*`, `pl-*`, `pr-*`, `left-*`, `right-*`, `text-left`) with logical properties (`ms-*`, `me-*`, `ps-*`, `pe-*`, `start-*`, `end-*`, `text-start`). | `/rtl-logical-guard Audit all frontend components for physical directional CSS classes and convert them to logical properties.` |
| **`/ui-audit`** | Running a full read-only frontend UI audit across routes, layouts, responsiveness, and accessibility. | Discovers all frontend routes, audits the 6-state matrix, mobile 375px layout, and RTL parity, and writes isolated fix prompts to `docs/ui-audits/`. | `/ui-audit Run a comprehensive read-only frontend UI audit and generate structured fix prompts.` |
| **`/ui-review-loop`** | Verifying UI changes in a real headless/recorded browser (`video + DOM timeline + network`). | Records browser verification rounds and exercises interactive UI states across desktop and mobile viewports. | `/ui-review-loop Record and verify the updated UI flows across desktop and mobile viewports.` |
| **`/generate-design`** | Generating new UI screens or editing existing screens in Google Stitch via `StitchMCP`. | Enhances prompts with UI/UX tokens and calls Stitch MCP to generate or refine high-craft screens. | `/generate-design Generate a responsive admin analytics screen in Stitch matching our DESIGN.md tokens.` |
| **`/enhance-prompt`** | Turning a rough UI idea into a polished, token-rich Google Stitch generation prompt. | Injects layout structure, typography scale, color tokens, and component states into your UI prompt. | `/enhance-prompt Turn this rough idea into a detailed Stitch design prompt: [your UI idea].` |
| **`/design-md`** | Analyzing an existing Google Stitch project to synthesize a semantic `DESIGN.md` file. | Extracts colors, typography, spacing, and surface hierarchy from Stitch screens into `DESIGN.md`. | `/design-md Analyze our Stitch project and synthesize a complete DESIGN.md file.` |
| **`/taste-design`** | Generating an anti-generic `DESIGN.md` with calibrated typography, color tokens, and micro-motion. | Enforces high-craft visual standards and bans generic AI gradients and overused fonts. | `/taste-design Generate a DESIGN.md specification for a modern fintech dashboard.` |
| **`/extract-design-md`** | Reverse-engineering a `DESIGN.md` design system directly from existing frontend source code. | Scans Tailwind configs, CSS variables, and React/Vue/Astro components to document the project's visual language. | `/extract-design-md Analyze our frontend stylesheets and components and generate a complete DESIGN.md.` |
| **`/manage-design-system`** | Creating, updating, or applying design systems across screens in Google Stitch. | Synchronizes local `DESIGN.md` tokens with your Stitch project's active design system. | `/manage-design-system Sync our local DESIGN.md tokens into our Google Stitch project.` |
| **`/extract-static-html`** | Extracting self-contained static HTML (with inlined CSS and assets) from a built web app or component. | Captures a live view as a standalone HTML snapshot ready for sharing or uploading to Google Stitch. | `/extract-static-html Extract a self-contained static HTML snapshot of our dashboard page.` |
| **`/upload-to-stitch`** | Uploading local HTML pages, mockups, or `DESIGN.md` files into a Google Stitch project. | Handles safe asset packaging and uploads local files to Stitch MCP without base64 truncation. | `/upload-to-stitch Upload our extracted static HTML and DESIGN.md to our Stitch project.` |
| **`/code-to-design`** | Migrating an existing React/Vue/Vite/Astro frontend into Google Stitch as editable screens. | Chains `/extract-static-html`, `/extract-design-md`, and `/upload-to-stitch` in one workflow. | `/code-to-design Extract our current frontend view and design system and upload it to Google Stitch.` |
| **`/site-md`** | Creating a `SITE.md` project constitution for autonomous multi-screen Stitch generation. | Synthesizes site map, page roles, navigation links, and brand rules into `SITE.md`. | `/site-md Create a SITE.md blueprint for our multi-page marketing and dashboard site.` |
| **`/stitch-loop`** | Iteratively generating and refining multi-page websites in Google Stitch using a baton-passing loop. | Reads `SITE.md` and `DESIGN.md` to generate, review, and refine screens sequentially. | `/stitch-loop Run the iterative Stitch build loop for the screens defined in SITE.md.` |
| **`/react-components`** | Converting Google Stitch screens into modular Vite + React components with AST validation. | Downloads Stitch screen markup, splits it into reusable React components with clean props, and validates syntax. | `/react-components Convert our Stitch screen into modular React components with clean props and Tailwind tokens.` |
| **`/react-vite-dashboard`** | Converting Google Stitch dashboard designs into a production React + Vite + TanStack Query app. | Scaffolds a responsive dashboard shell with accessible tokens from `DESIGN.md` and typed data hooks. | `/react-vite-dashboard Convert our Stitch dashboard screens into a React + Vite + TanStack Query application.` |
| **`/react-native`** | Converting Google Stitch mobile screens into React Native components using `StyleSheet`. | Translates Stitch layouts and tokens into clean, cross-platform React Native screens. | `/react-native Convert our mobile Stitch screens into React Native components with StyleSheet.` |
| **`/remotion`** | Generating animated walkthrough videos of your UI or Stitch screens using Remotion. | Builds smooth camera pans, zooms, and caption overlays to showcase your product screens. | `/remotion Create a 30-second Remotion walkthrough video showcasing our new dashboard screens.` |
| **`/webmcp`** | Exposing in-page JavaScript tools and forms to browser AI agents via the W3C `document.modelContext` standard. | Registers, validates, and secures `document.modelContext.registerTool` handlers for agentic web apps. | `/webmcp Register in-page WebMCP tools on our dashboard so browser agents can query and filter records.` |

---

### E. Backend, API, Auth, Database & DevOps (11 Skills)

| Command | When & How to Use | Description | 💬 Ready Copy-Paste Command |
| :--- | :--- | :--- | :--- |
| **`/laravel-mastery`** | Building or refactoring Laravel 11+ / PHP 8.3+ controllers, FormRequests, Eloquent models, jobs, and Pest tests. | Enforces `declare(strict_types=1)`, FormRequest validation, eager loading (zero N+1), pessimistic locking (`lockForUpdate`), and idempotent jobs. | `/laravel-mastery Implement the orders controller, FormRequest, service action, and Pest tests in Laravel.` |
| **`/backend-api`** | Designing or building REST/GraphQL APIs, controllers, middleware, and service layers in Node, Python, PHP, or Go. | Enforces clean controller-service-repository separation, consistent error envelopes, and auth/validation boundaries. | `/backend-api Design and implement the REST endpoints for [resource] with 422 validation, pagination, and RBAC.` |
| **`/backend-http`** | Implementing HTTP routing conventions, status codes, cursor/offset pagination, webhooks, SSE, or WebSockets. | Enforces RFC-compliant status codes (`200`, `201`, `400`, `401`, `403`, `404`, `422`, `429`), rate limiting, and webhook signature verification. | `/backend-http Add cursor pagination, rate limiting, and idempotent webhook verification to our API routes.` |
| **`/backend-identity`** | Implementing login, registration, JWT, OAuth2/OIDC, session cookies, RBAC/ABAC roles, or MFA. | Enforces server-side session derivation, `HttpOnly`/`SameSite`/`Secure` cookies, role guards, and anti-IDOR ownership checks. | `/backend-identity Implement server-side RBAC middleware and ownership guards for [resource].` |
| **`/backend-data`** | Writing complex relational/NoSQL queries, caching layers, full-text search, or multi-step transactions. | Prevents N+1 queries, enforces atomic database transactions, and configures safe cache invalidation. | `/backend-data Optimize our reporting queries to eliminate N+1 loads and wrap writes in a transaction.` |
| **`/database`** | Designing database schemas, ERDs, migrations, foreign keys, compound indexes, and soft deletes. | Enforces 3NF normalization, explicit `ON DELETE` rules, compound indexes matching `WHERE`/`ORDER BY`, and expand-and-contract migrations. | `/database Design the migration and indexes for [table] with foreign keys, soft deletes, and zero N+1 queries.` |
| **`/backend-ops`** | Setting up background queues, cron workers, S3/R2 object storage uploads, `/health` probes, and structured logs. | Enforces retry/dead-letter queues, MIME/size-validated uploads, readiness endpoints, and correlation-ID JSON logging. | `/backend-ops Configure idempotent background queue workers and retry handling for [job].` |
| **`/devops-deploy`** | Setting up Dockerfiles, `docker-compose`, GitHub Actions CI/CD, Nginx, Vercel/Netlify/VPS deployment, and `.env.example`. | Produces multi-stage production Dockerfiles, zero-downtime deployment pipelines, and copy-pasteable `KEY = VALUE` cloud configs. | `/devops-deploy Create a production Dockerfile and GitHub Actions CI/CD pipeline with health checks.` |
| **`/next-server-action-guard`** | Creating, editing, or auditing Next.js App Router Server Actions (`actions.ts`) and Route Handlers. | Enforces server-side `auth()` session checks, Anti-IDOR resource ownership verification, Zod schema validation, and safe error returns. | `/next-server-action-guard Audit all Server Actions in src/app/ for session derivation, Anti-IDOR ownership, and Zod validation.` |
| **`/pest-security-guard`** | Writing or auditing PHP/Laravel code and running Pest 3 architectural security tests. | Enforces `arch()->preset()->security()`, `declare(strict_types=1)`, and bans `eval()`, `exec()`, `dd()`, and raw unparameterized SQL. | `/pest-security-guard Audit our Laravel codebase and run Pest architectural security tests.` |
| **`/firebase-security-rules-auditor`** | Auditing or hardening Firebase Firestore (`firestore.rules`) and Cloud Storage (`storage.rules`) security rules. | Checks for privilege escalation, role bypasses, `create` vs. `update` gaps, missing `hasOnly` field locks, and resource exhaustion. | `/firebase-security-rules-auditor Audit firestore.rules and storage.rules for privilege escalation and missing ownership checks.` |

---

### F. Security, Bug Hunting, Pentesting, WordPress/WooCommerce & QA (12 Skills)

| Command | When & How to Use | Description | 💬 Ready Copy-Paste Command |
| :--- | :--- | :--- | :--- |
| **`/bug-hunter`** | Investigating a feature, workflow, or PR in read-only mode to find hidden functional bugs and race conditions. | Traces frontend-to-backend state transitions and reports evidence-backed bugs with exact file/line triggers and reproduction steps. | `/bug-hunter Investigate the checkout and order state flow in read-only mode for functional bugs and race conditions.` |
| **`/security-audit`** | Running a comprehensive security vulnerability review across your codebase, APIs, and dependencies. | Audits auth boundaries, secret exposure, SQLi/XSS/CSRF/SSRF vectors, and insecure cryptography. | `/security-audit Run a security vulnerability review across our authentication and payment modules.` |
| **`/pentest`** | Probing a live local or staging web application you own for BOLA/IDOR, BFLA, RLS bypass, and injection flaws. | Executes authorized WSTG-anchored HTTP/API probes (`curl`) using test credentials and outputs reproducible PoC + remediation recipes. | `/pentest Run an authorized WSTG security assessment against http://localhost:3000 with our test credentials.` |
| **`/cookie-debugging`** | Diagnosing `401`/`403` login loops, dropped sessions, `Cookie`/`Set-Cookie` headers, or `SameSite`/CORS issues. | Uses Chrome DevTools MCP to inspect live network cookie headers, domain/path scopes, and redirect chains. | `/cookie-debugging Diagnose why session cookies are dropping on redirect between login and dashboard.` |
| **`/wp-guard`** | Reviewing WordPress plugin, theme, Gutenberg block, REST route, or AJAX handler code before shipping. | Enforces `wp_verify_nonce`, `current_user_can`, input sanitization, late output escaping (`esc_html`, `esc_url`), and `$wpdb->prepare()`. | `/wp-guard Review our custom WordPress plugin endpoints and admin metaboxes for security and escaping.` |
| **`/woo-guard`** | Reviewing WooCommerce extensions, checkout fields, payment gateways, or order/product hooks. | Enforces HPOS-compatible `wc_get_order()` CRUD (never raw `get_post_meta`), server-side checkout validation, and decimal money accuracy. | `/woo-guard Audit our WooCommerce checkout and order hooks for HPOS compatibility and payment safety.` |
| **`/clean-code-guard`** | Reviewing modified production code for Clean Code, SOLID, DRY, KISS, YAGNI, and layer boundaries. | Catches bloated functions, cross-layer leaks, magic numbers, hardcoded URLs/secrets, and dead code before commit. | `/clean-code-guard Review all modified production files for Clean Code, SOLID boundaries, and simplicity.` |
| **`/testing-qa`** | Writing unit, integration, or E2E tests (`Vitest`, `Jest`, `Playwright`, `Pytest`, `Pest`, `PHPUnit`). | Builds deterministic tests covering happy paths, negative/422 validation, 403 unauthorized access, and edge cases. | `/testing-qa Write unit and integration tests for [module] covering happy path, validation errors, and unauthorized access.` |
| **`/test-guard`** | Reviewing generated or modified test files to prevent brittle, over-mocked, or fake tests. | Ensures tests assert real behavior and state transitions rather than mocking the system under test. | `/test-guard Review our new test files to ensure real behavior assertions, negative cases, and zero over-mocking.` |
| **`/debate-review`** | Running a two-perspective adversarial code review on a local git diff or GitHub/GitLab Pull Request. | Runs a proposer-vs-challenger debate across changed lines to catch subtle logic and security regressions. | `/debate-review Run a two-perspective adversarial code review on our current git diff.` |
| **`/reverse-engineer-anything`** | Analyzing compiled binaries, Electron apps, minified bundles, or undocumented network protocols. | Uses static and runtime evidence to map internal APIs, state machines, and data structures for clean-room reconstruction. | `/reverse-engineer-anything Analyze the target bundle and document its internal API protocol and state machine.` |
| **`/agentic-workflows`** | Orchestrating multi-agent parallel research, consensus voting, build-verify QA loops, or dual-axis security audits. | Coordinates isolated subagent passes and synthesizes verified findings without polluting your main context window. | `/agentic-workflows Run a build-and-verify QA loop across our modified modules.` |

---

### G. Code Simplicity (`Ponytail`), Low-Bandwidth (`Data-Saver`) & Documentation (10 Skills)

| Command | When & How to Use | Description | 💬 Ready Copy-Paste Command |
| :--- | :--- | :--- | :--- |
| **`/ponytail`** | Activating simplicity-first coding mode (`YAGNI`) so the agent writes the shortest, cleanest stdlib-first solution. | Bans speculative abstractions, single-use wrappers, and unnecessary third-party libraries (`lite`, `full`, or `ultra`). | `/ponytail Implement [feature] using the simplest, shortest standard-library solution with zero bloat.` |
| **`/ponytail-review`** | Reviewing a git diff or PR specifically to find and delete over-engineered code. | Outputs a concise list of unnecessary abstractions, dead config flags, and dependencies that can be replaced with native code. | `/ponytail-review Review our current changes and list every over-engineered abstraction we can delete or simplify.` |
| **`/ponytail-audit`** | Scanning the entire repository for over-engineering, dead files, and redundant dependencies. | Produces a ranked whole-repo simplification report showing what to delete or inline. | `/ponytail-audit Scan the repository and rank the top over-engineered modules and dependencies we can simplify.` |
| **`/ponytail-debt`** | Harvesting all `// ponytail:` deferred-shortcut comments across the codebase into a tracked ledger. | Ensures deliberate MVP shortcuts are tracked in one place instead of forgotten. | `/ponytail-debt List all ponytail deferred-work comments across the codebase.` |
| **`/ponytail-gain`** | Displaying the measured code-size, token, and speed savings scoreboard from Ponytail mode. | Shows a compact benchmark summary of complexity reduction. | `/ponytail-gain Show the ponytail simplicity impact scoreboard.` |
| **`/ponytail-help`** | Displaying the quick-reference card for all `/ponytail*` commands and intensity levels. | Prints a 1-screen cheat sheet of Ponytail modes (`lite`, `full`, `ultra`) and audit commands. | `/ponytail-help Show the quick-reference guide for all ponytail commands.` |
| **`/caveman`** | Switching chat responses to ultra-concise, low-token mode (`lite`, `full`, `ultra`) while keeping 100% code accuracy. | Cuts prose filler by 60–80% so responses stream faster and consume fewer context tokens. | `/caveman lite Keep all technical explanations concise and high-signal.` |
| **`/data-saver`** | Auditing or activating the low-bandwidth Antigravity IDE profile (saves 75–85% daily internet data). | Disables background IDE auto-updates, telemetry, and git auto-fetch while preserving full AI chat and MCP tools. | `/data-saver Audit my IDE bandwidth settings and apply the low-bandwidth profile.` |
| **`/project-documentation`** | Generating or updating `README.md`, `docs/ARCHITECTURE.md`, and `docs/API.md` from actual codebase files. | Performs deterministic local AST/route/schema analysis to author complete onboarding and architecture docs. | `/project-documentation Generate comprehensive README.md, docs/ARCHITECTURE.md, and docs/API.md files.` |
| **`/docs-guard`** | Auditing documentation files against the actual codebase to catch outdated flags, broken paths, or filler. | Verifies every CLI command, env variable, file path, and endpoint documented in `.md` files against source truth. | `/docs-guard Audit README.md and docs/ against the codebase to verify every command, path, and endpoint.` |

---

### H. All 28 Unified Agent OS CLI Commands (`python scripts/agent_os.py <cmd>`)

You can either paste these in your **Terminal** or ask the **AI Chat** to run them for you:

| CLI Command | When & How to Use | Description | 💻 Ready Copy-Paste Terminal Command |
| :--- | :--- | :--- | :--- |
| **`status`** | Check workspace git SHA, installed skill count (85), active rules (5), and safety locks. | Prints active workspace root, git branch/commit, danger-zone locks, and installed skill/rule/test counts. | `python scripts/agent_os.py status` |
| **`route`** | Auto-recommend the best skills and workflow for any plain-language feature description. | Analyzes your prompt and repository stack to output the exact skill chain to activate. | `python scripts/agent_os.py route "build a responsive orders table with status filter and CSV export"` |
| **`skill-find`** | Search the 85-skill registry by keyword, domain, or stack from the terminal. | Queries `SKILL_INDEX.json` and returns matching slash commands and file paths. | `python scripts/agent_os.py skill-find "security"` |
| **`plan-daily`** | Generate today's prioritized engineering focus from `git status` and `SESSION_SNAPSHOT.md`. | Inspects uncommitted work, recent commits, and snapshots to recommend 1 Primary Focus + 2 Secondary tasks. | `python scripts/agent_os.py plan-daily` |
| **`precode`** | Scaffold or audit the 6 Pre-Coding Architecture Documents (`01-PRD` to `06-IMPLEMENTATION_PLAN`). | Verifies that all 6 pre-coding documents exist and pass the 100% architecture clearance gate. | `python scripts/agent_os.py precode audit docs/precode` |
| **`symbol`** | Find the exact `file:line` definition of a class, function, or component without reading whole files. | Uses AST/regex indexing to jump directly to symbol definitions (`97%` token savings). | `python scripts/agent_os.py symbol build_registry_payload` |
| **`outline`** | View a compact structural outline of functions/classes inside a file before reading it. | Lists all classes, methods, and functions with line numbers for any source file. | `python scripts/agent_os.py outline scripts/sync_handbook.py` |
| **`trace`** | Trace all callers, callees, and import references of a function or component across the repo. | Maps the upstream/downstream blast radius of a symbol before refactoring or fixing a bug. | `python scripts/agent_os.py trace check_rtl_logical_css` |
| **`scan`** | Scan a file or directory for hardcoded secrets, security flaws, AI slop, and RTL CSS violations. | Runs `guard_checker.py` across target files and exits non-zero if any violation is found. | `python scripts/agent_os.py scan learning-platform/src/pages/index.astro` |
| **`ui-audit`** | Run the automated frontend UI & responsive layout scanner from the CLI. | Checks components for sticky nav/sidebar patterns, `overflow-x-auto` tables, and logical RTL classes. | `python scripts/agent_os.py ui-audit learning-platform/src` |
| **`sentinel`** | Run the Proactive Full-Stack Sentinel audit across Frontend, Backend, Security, and Git state. | Executes multi-layer static analysis and outputs a prioritized health report. | `python scripts/agent_os.py sentinel .` |
| **`review`** | Review uncommitted git changes (`git diff`) for code quality, security, and layer violations. | Audits staged/unstaged diffs before you commit or push. | `python scripts/agent_os.py review` |
| **`chaos-audit`** | Audit backend/API code for missing timeouts, non-idempotent retries, and race conditions. | Scans async handlers, webhooks, and DB writes for resilience under network/concurrency failures. | `python scripts/agent_os.py chaos-audit scripts` |
| **`snapshot`** | Freeze or restore cognitive session state (`SESSION_SNAPSHOT.md`) at 60%–70% context capacity. | Checkpoints locked decisions, touched files, and next steps so zero context is lost across sessions. | `python scripts/agent_os.py snapshot freeze "milestone-complete"` |
| **`sync`** | Synchronize all 85 skills, 5 rules, scripts, and `GEMINI.md` across Workspace, Antigravity, and OpenCode. | Copies updated skills/rules to `~/.gemini/config` and `~/.config/opencode` (`--team` installs `GEMINI.team.md`). | `python scripts/agent_os.py sync --apply` |
| **`handbook-sync`** | Rebuild the bilingual W3Schools Learning Platform, update `handbook.html`, and deploy to GitHub Pages. | Syncs `SKILL_INDEX.json` -> `skills-registry.json`, builds `dist/index.html`, copies to `handbook.html`, and deploys with `--deploy`. | `python scripts/agent_os.py handbook-sync --build --deploy` |
| **`index-skills`** | Rebuild `SKILL_INDEX.json` and `SKILLS_DIRECTORY.md` after adding or editing a skill. | Scans `skills/` and global plugins to update the master skill index. | `python scripts/agent_os.py index-skills` |
| **`data-saver`** | Check, apply, or restore the low-bandwidth Data-Saver IDE profile (`75–85%` bandwidth reduction). | Configures IDE settings and offline package manager caches (`npm`, `pnpm`, `composer`, `pip`). | `python scripts/agent_os.py data-saver status` |
| **`test`** | Run the complete Agent OS automated unit test suite (`tests/`). | Executes all unit tests verifying CLI tools, security guards, sync parity, and handbook compilation. | `python scripts/agent_os.py test` |
| **`audit`** | Verify parity and SHA-256 integrity across Workspace, Antigravity, and OpenCode installations. | Checks that all rules, skills, and scripts are in sync without modifying files. | `python scripts/agent_os.py audit` |
| **`doctor`** | Run a complete environment diagnostic (Python, Node, Git, paths, and permissions). | Verifies that your machine has all required runtimes and valid configuration files. | `python scripts/agent_os.py doctor` |
| **`scope`** | Check modified files in `git status` against an allowed scope boundary. | Alerts if any file outside the authorized feature directory was accidentally modified. | `python scripts/agent_os.py scope` |
| **`adr-check`** | Verify that Architectural Decision Records (`docs/adr/`) exist and follow the required template. | Audits ADR files so major architectural choices remain documented for the team. | `python scripts/agent_os.py adr-check` |
| **`antipattern`** | Scan code for known framework anti-patterns (N+1 loops, raw SQL, `window.alert`, physical CSS). | Detects common structural mistakes across JS/TS, PHP, Python, and CSS files. | `python scripts/agent_os.py antipattern learning-platform/src` |
| **`eval` / `sql` / `regex`** | Safely test Python expressions, inspect SQLite/SQL queries, or test regex patterns from the CLI. | Provides a deterministic sandbox for verifying expressions, SQL syntax, and regular expressions. | `python scripts/agent_os.py regex "ms-[0-9]+" "class='ms-4 text-start'"` |
| **`probe` / `logs`** | Probe a local HTTP endpoint's status/headers or tail recent application log files. | Verifies live server readiness (`200 OK`) and inspects runtime error logs without opening a browser. | `python scripts/agent_os.py probe http://localhost:4321` |
| **`telemetry`** | View local execution telemetry (tool pass rates, context usage, and guard statistics). | Summarizes local `.agent_telemetry.json` metrics with zero external network calls. | `python scripts/agent_os.py telemetry` |
| **`codemod`** | Preview and apply safe structural search-and-replace transformations across multiple files. | Runs dry-run or applied multi-file refactors with diff previews. | `python scripts/agent_os.py codemod --help` |
