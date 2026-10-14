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

## 📚 7. Complete Dictionary of All 60 Skills (Optional Reference)
### القاموس المرجعي لجميع المهارات الـ 60 (مرجع اختياري)

You never need to memorize these—the **11 Situation Commands** above call them for you automatically! They are listed here only in case you are curious what is inside the engine:

| Category (الفئة) | Skills Included (المهارات المتضمنة) |
| :--- | :--- |
| **1. Beginner Situation Combos (11)**<br>*(أوامر الحالات الشاملة)* | `/start-project`, `/smart-feature`, `/feature-fe`, `/feature-febe`, `/feature-full`, `/feature-wp`, `/fix-ui`, `/fix-backend`, `/check-all`, `/doc-project`, `/save-data` |
| **2. Frontend & UI Design (3)**<br>*(تصميم وبناء الواجهات)* | `/muaz-skill` (91 styles, 169 palettes, 28 intake questions), `/nextjs-fullstack`, `/ui-audit` |
| **3. Backend & Data Systems (8)**<br>*(الباك-إند وقواعد البيانات)* | `/laravel-mastery`, `/backend-api`, `/backend-data`, `/backend-http`, `/backend-identity`, `/backend-ops`, `/database`, `/devops-deploy` |
| **4. Automatic Security & Quality Guards (8)**<br>*(حراس الأمان والجودة)* | `/clean-code-guard`, `/test-guard`, `/docs-guard`, `/next-server-action-guard`, `/pest-security-guard`, `/rtl-logical-guard`, `/woo-guard`, `/wp-guard` |
| **5. Pre-Coding & Spec-Kit Planning (13)**<br>*(التخطيط المعماري المسبق)* | `/web-precode`, `/spec-kit`, `/speckit-constitution`, `/speckit-specify`, `/speckit-clarify`, `/speckit-plan`, `/speckit-checklist`, `/speckit-tasks`, `/speckit-implement`, `/speckit-analyze`, `/speckit-converge`, `/speckit-taskstoissues`, `/glopale` |
| **6. Core Workflow & Review (8)**<br>*(سير العمل والمراجعة)* | `/engineering-workflow`, `/data-saver`, `/debate-review`, `/delegate-setup`, `/opencode-delegate`, `/find-skills`, `/project-documentation`, `/ui-review-loop` |
| **7. Simplicity & Anti-Bloat (7)**<br>*(تبسيط الكود وتقليل التوكنز)* | `/caveman`, `/ponytail`, `/ponytail-audit`, `/ponytail-debt`, `/ponytail-gain`, `/ponytail-help`, `/ponytail-review` |
| **8. Testing & Browser Protocol (2)**<br>*(الاختبارات وبروتوكول المتصفح)* | `/testing-qa`, `/webmcp` |
