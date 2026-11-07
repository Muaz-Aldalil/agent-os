/**
 * Agent OS W3Schools x Social Learning Platform Curriculum & Interactive Data.
 * Complete bilingual (EN LTR + AR RTL) content for all 4 Tracks, 15 Lessons,
 * 6 Tap-Through Story Reels, 11 Situation Combos, and 6 Tech Stack Simulator Presets.
 */

export const TECH_STACKS = [
  {
    id: 'astro',
    labelEn: 'Astro + HTML + Tailwind',
    labelAr: 'أسترو + HTML + تايلويند',
    badge: 'Astro 4',
    stackSkills: ['/feature-fe', '/muaz-skill', '/rtl-logical-guard', '/ui-audit'],
    filesEn: [
      'src/layouts/W3Layout.astro (Sticky Topbar + Dark Ribbon + RTL/LTR Shell)',
      'src/pages/index.astro (Mobile-First W3Schools Reader + Social Feed)',
      'src/data/skills-registry.json (Auto-synced from SKILL_INDEX.json)',
      'tailwind.config.mjs (Semantic W3Schools Design Tokens)'
    ],
    filesAr: [
      'src/layouts/W3Layout.astro (شريط علوي ثابت + غلاف ثنائي اللغة)',
      'src/pages/index.astro (قارئ الدروس المتجاوب + موجز التعلم التفاعلي)',
      'src/data/skills-registry.json (سجل المهارات المتزامن تلقائياً)',
      'tailwind.config.mjs (رموز ألوان W3Schools القياسية)'
    ]
  },
  {
    id: 'nextjs',
    labelEn: 'Next.js 15 + Prisma + MySQL',
    labelAr: 'نكست 15 + بريزما + MySQL',
    badge: 'Next.js 15',
    stackSkills: ['/nextjs-fullstack', '/next-server-action-guard', '/database', '/rtl-logical-guard'],
    filesEn: [
      'prisma/schema.prisma (Foreign Keys + Compound Indexes + Soft Deletes)',
      'src/app/actions.ts (Server Auth + Anti-IDOR + Zod Validation)',
      'src/app/admin/page.tsx (Sticky Admin Shell + Truncated Responsive Table)',
      'tests/feature.spec.ts (Real Integration & Boundary Verification)'
    ],
    filesAr: [
      'prisma/schema.prisma (مفاتيح خارجية + فهارس مركبة + حذف ناعم)',
      'src/app/actions.ts (تحقق الهوية بالخادم + حماية IDOR + فحص Zod)',
      'src/app/admin/page.tsx (غلاف إدارة ثابت + جدول متجاوب مختصر)',
      'tests/feature.spec.ts (اختبارات تكامل حقيقية للحدود)'
    ]
  },
  {
    id: 'laravel',
    labelEn: 'Laravel 11 + Blade / Livewire',
    labelAr: 'لارافيل 11 + بليد / لايفواير',
    badge: 'Laravel 11',
    stackSkills: ['/laravel-mastery', '/pest-security-guard', '/database', '/rtl-logical-guard'],
    filesEn: [
      'database/migrations/create_table.php (Strict FK + Indexes)',
      'app/Http/Requests/StoreRequest.php (authorize() + Server Rules)',
      'resources/views/admin/index.blade.php (Responsive Table + Floating Save)',
      'tests/Feature/SecurityTest.php (Pest 3 Arch + RBAC Verification)'
    ],
    filesAr: [
      'database/migrations/create_table.php (مفاتيح خارجية وفهارس دقيقة)',
      'app/Http/Requests/StoreRequest.php (فحص الصلاحيات وقواعد التحقق)',
      'resources/views/admin/index.blade.php (جدول متجاوب + زر حفظ عائم)',
      'tests/Feature/SecurityTest.php (اختبارات أمان وصلاحيات Pest 3)'
    ]
  },
  {
    id: 'vue',
    labelEn: 'Vue 3 / Nuxt 3 + Tailwind',
    labelAr: 'فيو 3 / نكست 3 + تايلويند',
    badge: 'Nuxt 3',
    stackSkills: ['/feature-fe', '/muaz-skill', '/rtl-logical-guard', '/clean-code-guard'],
    filesEn: [
      'layouts/admin.vue (h-dvh Sticky Sidebar + Independent Scroll Main)',
      'components/DataTable.vue (2-4 Word Cell Truncate + Details Modal)',
      'server/api/items.post.ts (Server Session + Payload Validation)',
      'tests/table.test.ts (Component & Responsive State Suite)'
    ],
    filesAr: [
      'layouts/admin.vue (قائمة جانبية ثابتة بكامل الارتفاع + تمرير مستقل)',
      'components/DataTable.vue (اختصار خلايا الجدول + نافذة التفاصيل)',
      'server/api/items.post.ts (فحص الجلسة والبيانات في الخادم)',
      'tests/table.test.ts (اختبارات المكونات والتجاوب)'
    ]
  },
  {
    id: 'html',
    labelEn: 'HTML5 + Tailwind CSS Static',
    labelAr: 'HTML5 + تايلويند ثابت',
    badge: 'HTML + TW',
    stackSkills: ['/feature-fe', '/muaz-skill', '/rtl-logical-guard', '/ui-audit'],
    filesEn: [
      'index.html (100dvh Hero + Sticky Top-0 Navbar + overflow-x-clip)',
      'tokens.json (WCAG 2.2 AA Verified 60-30-10 Design Tokens)',
      '.design-lock.md (Locked Typography & Surface Palette Blueprint)',
      'docs/ui-audits/report.md (8-Dimension Static UI Audit Report)'
    ],
    filesAr: [
      'index.html (واجهة رئيسية 100dvh + شريط علوي ثابت + منع التمرير الأفقي)',
      'tokens.json (رموز تصميم متوافقة مع تباين WCAG 2.2 AA)',
      '.design-lock.md (مخطط الخطوط والألوان المعتمد)',
      'docs/ui-audits/report.md (تقرير فحص الواجهة من 8 أبعاد)'
    ]
  },
  {
    id: 'wp',
    labelEn: 'WordPress + WooCommerce HPOS',
    labelAr: 'ووردبريس + ووكرومرس HPOS',
    badge: 'WP / Woo',
    stackSkills: ['/feature-wp', '/wp-guard', '/woo-guard', '/rtl-logical-guard'],
    filesEn: [
      'includes/class-order-handler.php (wc_get_order CRUD + HPOS Declaration)',
      'includes/class-rest-controller.php (check_ajax_referer + current_user_can)',
      'templates/admin-table.php (esc_html__ + Logical RTL Classes)',
      'tests/OrderSecurityTest.php (Nonce, Capability & SQL Prepare Checks)'
    ],
    filesAr: [
      'includes/class-order-handler.php (دوال CRUD متوافقة مع HPOS)',
      'includes/class-rest-controller.php (فحص Nonce والصلاحيات بالخادم)',
      'templates/admin-table.php (تعقيم المخرجات ودعم اتجاه العربية)',
      'tests/OrderSecurityTest.php (اختبارات الحماية واستعلامات SQL الآمنة)'
    ]
  }
];

export const STORY_REELS = [
  {
    id: 'story-intern',
    badgeEn: '60s Intro',
    badgeAr: 'مقدمة 60ث',
    titleEn: 'Intern vs Senior Team',
    titleAr: 'متدرب مقابل فريق خبراء',
    authorEn: 'Agent OS Core',
    authorAr: 'نواة النظام',
    color: 'w3-green',
    slides: [
      {
        stepLabelEn: 'Slide 1 of 3: The Raw AI Problem',
        stepLabelAr: 'شريحة 1 من 3: مشكلة الذكاء الاصطناعي الخام',
        headingEn: 'Without Agent OS: A Fast Intern Guessing Your App',
        headingAr: 'بدون النظام: متدرب سريع يخمن تفاصيل تطبيقك',
        bodyEn: 'When you ask raw AI to "build an orders page", it starts writing code immediately without asking about roles, mobile layout, or database indexes. Result: broken mobile tables, English mixed with Arabic, and missing server security.',
        bodyAr: 'عندما تطلب من ذكاء اصطناعي عادي "بناء صفحة طلبات"، يبدأ بكتابة الكود فوراً دون السؤال عن الصلاحيات أو الجوال أو فهارس قاعدة البيانات. النتيجة: جداول مكسورة على الجوال، نصوص مختلطة، وثغرات أمنية.',
        code: '// Raw AI Output (No Guards):\n// 1. Guessed schema without indexes\n// 2. Overflowing 12-column desktop table on 375px mobile\n// 3. Physical pl-4 / text-left breaking Arabic RTL'
      },
      {
        stepLabelEn: 'Slide 2 of 3: The 6-Specialist Pipeline',
        stepLabelAr: 'شريحة 2 من 3: خط عمل من 6 متخصصين',
        headingEn: 'With Agent OS: 1 Slash Command Awakens 6 Specialists',
        headingAr: 'مع النظام: أمر واحد يفعل 6 مهندسين متخصصين',
        bodyEn: 'Typing a single Situation Combo like /feature-full automatically chains a Product Interviewer, UI Architect, Frontend Builder, Backend Engineer, Database Architect, and Security Auditor.',
        bodyAr: 'كتابة أمر شامل واحد مثل /feature-full يقوم تلقائياً بتشغيل مستجوب المتطلبات، ومهندس التصميم، ومطور الواجهة، ومطور الخلفية، ومهندس البيانات، ومدقق الأمان.',
        code: '/feature-full Add a vendor payout approval table with status filter and receipt modal'
      },
      {
        stepLabelEn: 'Slide 3 of 3: You Stay the Boss',
        stepLabelAr: 'شريحة 3 من 3: أنت صاحب القرار دائماً',
        headingEn: 'You Own Business Intent. Agent OS Owns Engineering.',
        headingAr: 'أنت تملك قرار العمل، والنظام يملك التنفيذ الهندسي.',
        bodyEn: 'You never need to memorize 60 individual skill names. Pick 1 of the 11 Situation Combos, answer plain-language questions, and reply "proceed" when the blueprint matches your vision.',
        bodyAr: 'لا تحتاج لحفظ 60 مهارة منفصلة. اختر أمراً واحداً من الأوامر الشاملة الـ 11، وأجب عن أسئلة واضحة، ثم اكتب "proceed" عندما يطابق المخطط رؤيتك.'
      }
    ]
  },
  {
    id: 'story-traffic',
    badgeEn: 'Core Rule',
    badgeAr: 'القاعدة الذهبية',
    titleEn: '1-2-3 Traffic Light',
    titleAr: 'قاعدة الإشارة 1-2-3',
    authorEn: 'Workflow Guard',
    authorAr: 'حارس سير العمل',
    color: 'w3-yellow',
    slides: [
      {
        stepLabelEn: 'Step 1: RED LIGHT (Stop & Grill)',
        stepLabelAr: 'الخطوة 1: الإشارة الحمراء (توقف واستجوب)',
        headingEn: 'Zero Code Written Until Questions Are Answered',
        headingAr: 'لا يكتب أي سطر كود قبل الإجابة عن الأسئلة',
        bodyEn: 'In Stage 1, Agent OS pauses in Read-Only Hold Mode and asks targeted multiple-choice questions with a (Suggested) default option first.',
        bodyAr: 'في المرحلة الأولى، يتوقف النظام في وضع القراءة فقط ويطرح أسئلة محددة متعددة الخيارات مع وضع الخيار المقترح في المقدمة.',
        code: '[Stage 1: RED LIGHT]\nQ1: Who can approve payouts? -> (Suggested) Admin & Finance Manager only\nQ2: What happens on rejection? -> (Suggested) Log reason + notify vendor'
      },
      {
        stepLabelEn: 'Step 2: YELLOW LIGHT (Blueprint)',
        stepLabelAr: 'الخطوة 2: الإشارة الصفراء (المخطط)',
        headingEn: 'Review the Architecture & UI Blueprint Before Building',
        headingAr: 'راجع مخطط الواجهة وقاعدة البيانات قبل البناء',
        bodyEn: 'Agent OS shows you the exact files, database columns, 5 UI states (Loading, Empty, Error, Success, Populated), and design tokens before touching production files.',
        bodyAr: 'يعرض لك النظام الملفات الدقيقة وأعمدة قاعدة البيانات وحالات الواجهة الخمس ورموز الألوان قبل تعديل أي ملف في المشروع.'
      },
      {
        stepLabelEn: 'Step 3: GREEN LIGHT ("proceed")',
        stepLabelAr: 'الخطوة 3: الإشارة الخضراء ("proceed")',
        headingEn: 'Say "proceed" to Build & Auto-Verify',
        headingAr: 'اكتب "proceed" لبدء البناء والفحص التلقائي',
        bodyEn: 'Once you say "proceed", Agent OS writes the code, runs clean-code-guard, test-guard, rtl-logical-guard, and anti_slop.py, and hands you a verified manifest.',
        bodyAr: 'بمجرد كتابة "proceed"، يكتب النظام الكود ويشغل حراس الجودة والاختبارات واتجاه اللغة ويسلمك تقريراً موثقاً بالملفات.'
      }
    ]
  },
  {
    id: 'story-sudan',
    badgeEn: '-85% Data',
    badgeAr: 'توفير 85%',
    titleEn: 'Sudan /save-data Mode',
    titleAr: 'وضع توفير البيانات /save-data',
    authorEn: 'Bandwidth Guard',
    authorAr: 'حارس البيانات',
    color: 'w3-mint',
    slides: [
      {
        stepLabelEn: 'Slide 1 of 2: Mobile Hotspot Protection',
        stepLabelAr: 'شريحة 1 من 2: حماية باقات الجوال ونقاط الاتصال',
        headingEn: 'Stop Silent Background Downloads From Draining GBs',
        headingAr: 'أوقف التحديثات الصامتة التي تستهلك باقة الإنترنت',
        bodyEn: 'IDEs silently burn 500MB to 2GB daily on background extension updates, git autofetch every 3 minutes, telemetry, and unrequested ghost-text completions.',
        bodyAr: 'تستهلك بيئات التطوير ما بين 500 ميجابايت إلى 2 جيجابايت يومياً في تحديثات الإضافات الصامتة والجلب التلقائي لـ Git والإكمال التلقائي المستمر.'
      },
      {
        stepLabelEn: 'Slide 2 of 2: One Command Activation',
        stepLabelAr: 'شريحة 2 من 2: التفعيل بأمر واحد',
        headingEn: 'Run /save-data at the Start of Mobile Sessions',
        headingAr: 'شغل /save-data عند العمل عبر نقطة اتصال الجوال',
        bodyEn: 'Chains bandwidth_guard.py with /caveman lite and offline package caches (npm --prefer-offline, pnpm, composer, pip) to cut daily data usage by 75-85%.',
        bodyAr: 'يدمج أداة حماية النطاق مع الردود المختصرة والتخزين المحلي للحزم لتقليل استهلاك الإنترنت اليومي بنسبة 75-85%.',
        code: '/save-data\n# Or via CLI:\npython D:\\Skills\\.agents\\scripts\\agent_os.py data-saver apply'
      }
    ]
  },
  {
    id: 'story-cms',
    badgeEn: 'Mobile First',
    badgeAr: 'الجوال أولاً',
    titleEn: 'CMS & Table Armor',
    titleAr: 'درع الجداول ولوحات التحكم',
    authorEn: 'Muaz UI Engine',
    authorAr: 'محرك معاذ للواجهات',
    color: 'w3-pink',
    slides: [
      {
        stepLabelEn: 'Slide 1 of 2: Responsive Data Tables',
        stepLabelAr: 'شريحة 1 من 2: جداول البيانات المتجاوبة',
        headingEn: 'No More Horizontal Page Scroll on 375px Phones',
        headingAr: 'وداعاً للتمرير الأفقي المزعج على شاشات الجوال',
        bodyEn: 'Every Admin and User table wraps in overflow-x-auto and truncates long cell descriptions to the first 2-4 words + "..." with a click-to-expand Details modal.',
        bodyAr: 'كل جدول في لوحة التحكم أو واجهة المستخدم يغلف بتمرير داخلي ويختصر النصوص الطويلة إلى أول 2-4 كلمات مع زر عرض التفاصيل في نافذة منبثقة.',
        code: '<td class="max-w-xs truncate">First three words...</td>\n<button type="button" data-detail-id="row-1">Details</button>'
      },
      {
        stepLabelEn: 'Slide 2 of 2: Sticky Shell & Floating Save',
        stepLabelAr: 'شريحة 2 من 2: القوائم الثابتة وزر الحفظ العائم',
        headingEn: 'Sticky Navbar, h-dvh Sidebar, & Zero window.alert()',
        headingAr: 'شريط علوي ثابت، قائمة جانبية كاملة، ومنع التنبيهات البدائية',
        bodyEn: 'Public navbars stay sticky (top-0) using overflow-x-clip. Admin sidebars lock to h-dvh with independent main scroll, and long CMS forms use one Floating Save bar + custom Toasts.',
        bodyAr: 'يبقى الشريط العلوي ثابتاً دائماً، وتثبت القائمة الجانبية بكامل ارتفاع الشاشة مع تمرير مستقل للمحتوى، وتستخدم النماذج الطويلة شريط حفظ عائماً وإشعارات أنيقة.'
      }
    ]
  },
  {
    id: 'story-fixui',
    badgeEn: 'Auto Fixer',
    badgeAr: 'مصلح الواجهات',
    titleEn: 'Fix Broken UI with /fix-ui',
    titleAr: 'إصلاح الواجهات بأمر /fix-ui',
    authorEn: 'UI Audit Engine',
    authorAr: 'محرك فحص الواجهة',
    color: 'w3-green',
    slides: [
      {
        stepLabelEn: 'Slide 1 of 2: 8-Dimension Static Audit',
        stepLabelAr: 'شريحة 1 من 2: فحص شامل من 8 أبعاد',
        headingEn: 'Finds Arbitrary Hexes, Missing Labels, & RTL Bugs Instantly',
        headingAr: 'يكتشف الألوان العشوائية ونقص الوسوم وأخطاء العربية فوراً',
        bodyEn: 'The /fix-ui combo runs ui_audit_engine.py across all .astro, .tsx, .vue, .blade.php, and .html files to locate layout, accessibility, and RTL violations.',
        bodyAr: 'يقوم أمر /fix-ui بتشغيل محرك الفحص عبر جميع ملفات الواجهة لاكتشاف أخطاء التخطيط وإمكانية الوصول واتجاه اللغة العربية.',
        code: '/fix-ui Fix the overlapping search icon, non-sticky navbar, and overflowing table on mobile'
      },
      {
        stepLabelEn: 'Slide 2 of 2: Automated Verification Loop',
        stepLabelAr: 'شريحة 2 من 2: حلقة التحقق التلقائي',
        headingEn: 'Verifies Zero Slop & 0 Audit Warnings Before Handoff',
        headingAr: 'يتحقق من صفر أخطاء تصميم قبل تسليم النتيجة',
        bodyEn: 'Every UI fix is checked against anti_slop.py (36 checks), quality_gate.py, and rtl-logical-guard so broken layouts never return.',
        bodyAr: 'يتم فحص كل تعديل عبر محرك منع العشوائية (36 فحصاً) وبوابة الجودة وحارس الاتجاه المنطقي لضمان عدم عودة المشكلة.'
      }
    ]
  },
  {
    id: 'story-v115',
    badgeEn: 'v1.15.0',
    badgeAr: 'إصدار 1.15',
    titleEn: 'Astro + Handbook Sync',
    titleAr: 'دعم Astro والمزامنة التلقائية',
    authorEn: 'Release Notes',
    authorAr: 'سجل التحديثات',
    color: 'w3-yellow',
    slides: [
      {
        stepLabelEn: 'Slide 1 of 2: Automated Registry Sync',
        stepLabelAr: 'شريحة 1 من 2: مزامنة سجل المهارات تلقائياً',
        headingEn: 'Update Skills Once, Deploy Everywhere',
        headingAr: 'حدث المهارات مرة واحدة، وانشرها في كل مكان',
        bodyEn: 'Running python scripts/agent_os.py handbook-sync --build reads SKILL_INDEX.json, updates learning-platform/src/data/skills-registry.json, builds the Astro app, and updates root handbook.html.',
        bodyAr: 'تشغيل أمر المزامنة يقرأ فهرس المهارات، ويحدث بيانات منصة التعلم، ويبني تطبيق Astro، ويحدث ملف الدليل الرئيسي تلقائياً.',
        code: 'python scripts/agent_os.py handbook-sync --build'
      },
      {
        stepLabelEn: 'Slide 2 of 2: Astro + TSX + Vue + Blade Support',
        stepLabelAr: 'شريحة 2 من 2: دعم كامل لملفات Astro',
        headingEn: 'All Static Guards Now Audit .astro Files Natively',
        headingAr: 'جميع أدوات الفحص تدعم الآن ملفات .astro مباشرة',
        bodyEn: 'ui_audit_engine.py, anti_slop.py, and guard_checker.py now inspect .astro components alongside React, Next.js, Vue, Blade, and HTML.',
        bodyAr: 'أصبحت محركات فحص الواجهة ومنع العشوائية وحارس الاتجاه المنطقي تفحص ملفات .astro جنباً إلى جنب مع React وVue وBlade وHTML.'
      }
    ]
  }
];

export const CURRICULUM_TRACKS = [
  {
    id: 'track-start',
    titleEn: 'Track 1: Start Here & 1-2-3 Rule',
    titleAr: 'المسار 1: البداية وقاعدة 1-2-3',
    lessons: [
      {
        id: 'ch-intro',
        trackId: 'track-start',
        feedCategory: 'start',
        badgeEn: 'Lesson 1.1',
        badgeAr: 'درس 1.1',
        xp: 25,
        readTimeEn: '2 min read',
        readTimeAr: 'قراءة دقيقتين',
        authorEn: 'Agent OS Core Team',
        authorAr: 'فريق نواة النظام',
        roleEn: 'Principal Systems Architect',
        roleAr: 'مهندس الأنظمة الرئيسي',
        titleEn: 'Agent OS Introduction: Your 6-Specialist AI Engineering Team',
        titleAr: 'مقدمة النظام: فريقك الهندسي المكون من 6 خبراء',
        summaryEn: 'Learn how Agent OS transforms a single plain-language slash command into a coordinated Frontend, Backend, Database, and Security engineering pipeline.',
        summaryAr: 'تعرف كيف يحول النظام أمراً نصياً بسيطاً إلى خط عمل متكامل يشمل الواجهة الأمامية والخلفية وقاعدة البيانات والأمان.',
        bulletsEn: [
          'Without Agent OS: Raw AI behaves like an eager intern who guesses requirements and skips mobile responsiveness and server auth.',
          'With Agent OS: 60 specialized skills and 24 CLI tools work under one constitution where you own business decisions and Agent OS owns technical execution.',
          'You only need 11 Situation Combos (/start-project, /feature-full, /fix-ui, etc.) for 95% of daily engineering work.'
        ],
        bulletsAr: [
          'بدون النظام: يتصرف الذكاء الاصطناعي العادي كمتدرب متسرع يخمن المتطلبات ويتجاهل تجاوب الجوال وحماية الخادم.',
          'مع النظام: تعمل 60 مهارة متخصصة و24 أداة برمجية تحت دستور هندسي موحد حيث تملك أنت قرار العمل ويملك النظام التنفيذ التقني.',
          'تحتاج فقط إلى 11 أمراً شاملاً (/start-project و/feature-full و/fix-ui وغيرها) لإنجاز 95% من مهامك اليومية.'
        ],
        beforeEn: 'User: "Build me a customer dashboard"\nRaw AI: Immediately dumps 400 lines of unstyled code with hardcoded fake data, broken mobile tables, and zero auth checks.',
        beforeAr: 'المستخدم: "ابن لي لوحة تحكم للعملاء"\nالذكاء الخام: يكتب فوراً 400 سطر ببيانات وهمية وجداول مكسورة على الجوال وبدون أي فحص للصلاحيات.',
        afterEn: 'User: "/feature-full Build a customer orders dashboard with status filtering"\nAgent OS: Interviews you on 3 key rules -> Locks design tokens & schema -> Builds responsive UI + API + DB + Tests.',
        afterAr: 'المستخدم: "/feature-full ابن لوحة طلبات العملاء مع تصفية الحالة"\nالنظام: يسألك 3 أسئلة مركزة -> يعتمد المخطط ورموز التصميم -> يبني الواجهة والخلفية وقاعدة البيانات والاختبارات.',
        exampleTitleEn: 'Example: Starting Any Task With Plain Language',
        exampleTitleAr: 'مثال: بدء أي مهمة بلغة واضحة ومباشرة',
        command: '/smart-feature',
        promptEn: '/smart-feature I want to add a team member invitation modal with role selection (Admin, Editor, Viewer) and email verification.',
        promptAr: '/smart-feature أريد إضافة نافذة دعوة أعضاء الفريق مع اختيار الصلاحية (مدير، محرر، مشاهد) وتأكيد البريد الإلكتروني.',
        chainedSkills: ['/grill-me', '/muaz-skill', '/feature-febe', '/backend-identity', '/rtl-logical-guard', '/clean-code-guard'],
        simQuestionsEn: [
          'Q1 (Scope & Expiration): How long should invitation links remain valid? -> (Suggested) 48 hours with one-click resend',
          'Q2 (Duplicate Handling): What if the invited email already belongs to an active member? -> (Suggested) Show inline warning and prevent duplicate invite'
        ],
        simQuestionsAr: [
          'س1 (الصلاحية والمدة): كم تبلغ مدة صلاحية رابط الدعوة؟ -> (المقترح) 48 ساعة مع زر إعادة إرسال بضغطة واحدة',
          'س2 (منع التكرار): ماذا يحدث إذا كان البريد مسجلاً بالفعل؟ -> (المقترح) إظهار تنبيه فوري في الحقل ومنع تكرار الدعوة'
        ],
        quiz: {
          questionEn: 'How many Situation Combo commands do you need to know for 95% of daily tasks in Agent OS?',
          questionAr: 'كم أمراً شاملاً تحتاج لمعرفته لإنجاز 95% من مهامك اليومية في النظام؟',
          optionsEn: [
            '11 Situation Combo commands (which automatically chain the 60 underlying skills)',
            'All 60 skills must be typed manually in every prompt',
            'You must write custom Python scripts before every prompt'
          ],
          optionsAr: [
            '11 أمراً شاملاً (تقوم بتشغيل المهارات الـ 60 الفرعية تلقائياً)',
            'يجب كتابة جميع المهارات الـ 60 يدوياً في كل طلب',
            'يجب كتابة سكربت بايثون مخصص قبل كل طلب'
          ],
          correctIndex: 0,
          explanationEn: 'Correct! The 11 Situation Combos act as smart routers that chain the right underlying skills automatically.',
          explanationAr: 'إجابة صحيحة! الأوامر الشاملة الـ 11 تعمل كموجهات ذكية تشغل المهارات الفرعية المناسبة تلقائياً.'
        }
      },
      {
        id: 'ch-traffic',
        trackId: 'track-start',
        feedCategory: 'start',
        badgeEn: 'Lesson 1.2',
        badgeAr: 'درس 1.2',
        xp: 25,
        readTimeEn: '3 min read',
        readTimeAr: 'قراءة 3 دقائق',
        authorEn: 'Engineering Workflow',
        authorAr: 'سير العمل الهندسي',
        roleEn: 'Gate & Hold-Mode Controller',
        roleAr: 'مراقب البوابات ووضع التوقف',
        titleEn: 'The 1-2-3 Traffic Light Rule & Batch Hold Mode',
        titleAr: 'قاعدة الإشارة الضوئية 1-2-3 ووضع تجميع الملاحظات',
        summaryEn: 'Understand how Red Light (Questions), Yellow Light (Blueprint), and Green Light ("proceed") prevent wasted tokens and unwanted code edits.',
        summaryAr: 'افهم كيف تمنع الإشارة الحمراء (الأسئلة) والصفراء (المخطط) والخضراء ("proceed") إهدار الوقت والتعديلات غير المطلوبة.',
        bulletsEn: [
          'RED LIGHT (Hold & Grill): Agent OS resolves upstream business rules (actors, permissions, failure policy) before asking about UI colors or columns.',
          'YELLOW LIGHT (Blueprint): For new apps or features, Agent OS presents the file plan, schema, and design tokens and waits for your approval.',
          'BATCH HOLD MODE: Tell Agent OS "I will give you a lot of things to fix, do not proceed until I tell you" to queue multiple fixes in Read-Only mode.'
        ],
        bulletsAr: [
          'الإشارة الحمراء (توقف واستجوب): يحسم النظام قواعد العمل الأساسية (المستخدمون، الصلاحيات، سياسة الأخطاء) قبل تفاصيل الألوان والأعمدة.',
          'الإشارة الصفراء (المخطط): يعرض النظام خطة الملفات وقاعدة البيانات ورموز التصميم وينتظر موافقتك.',
          'وضع تجميع الملاحظات: قل للنظام "سأعطيك عدة تعديلات، لا تبدأ حتى أخبرك" لتجميع كل ملاحظاتك في وضع القراءة فقط.'
        ],
        beforeEn: 'Sending 5 separate bug notes one by one while the AI edits half-baked files after every single message.',
        beforeAr: 'إرسال 5 ملاحظات متفرقة بينما يقوم الذكاء الاصطناعي بتعديل الملفات بشكل ناقص بعد كل رسالة.',
        afterEn: 'Activating Read-Only Hold Mode, listing all 5 fixes clearly, verifying the exact target lines, and saying "proceed" once.',
        afterAr: 'تفعيل وضع التوقف للقراءة فقط، وسرد الملاحظات الخمس بالكامل، وتأكيد أماكنها في الكود، ثم كتابة "proceed" مرة واحدة.',
        exampleTitleEn: 'Example: Using Batch Feedback Hold Mode',
        exampleTitleAr: 'مثال: استخدام وضع تجميع الملاحظات قبل التنفيذ',
        command: '/engineering-workflow',
        promptEn: '/engineering-workflow I will give you 4 UI and API fixes. Hold in Read-Only mode and do not edit files until I say proceed.',
        promptAr: '/engineering-workflow سأعطيك 4 تعديلات في الواجهة والـ API. ابق في وضع القراءة فقط ولا تعدل أي ملف حتى أقول proceed.',
        chainedSkills: ['/engineering-workflow', '/grill-me', '/clean-code-guard', '/test-guard'],
        simQuestionsEn: [
          'Hold Mode Active: Logged Item #1 (Navbar sticky top-0) and Item #2 (Table cell truncate). Waiting for remaining items or "proceed".',
          'Pre-Flight Check: Confirmed target files exist with 0 conflicting background processes.'
        ],
        simQuestionsAr: [
          'وضع التوقف مفعل: تم تسجيل الملاحظة #1 (تثبيت الشريط العلوي) والملاحظة #2 (اختصار خلايا الجدول). بانتظار بقية الملاحظات أو كلمة "proceed".',
          'فحص الجاهزية: تم التأكد من وجود الملفات المستهدفة بدون أي تعارض.'
        ],
        quiz: {
          questionEn: 'What magic word unlocks Stage 5 (Code Execution) after you review the blueprint or finish giving batch feedback?',
          questionAr: 'ما هي الكلمة التي تفتح مرحلة التنفيذ وكتابة الكود بعد مراجعة المخطط أو الانتهاء من سرد الملاحظات؟',
          optionsEn: [
            '"proceed" (or "start")',
            'It starts editing files automatically without waiting',
            'You must restart the IDE'
          ],
          optionsAr: [
            'كلمة "proceed" (أو "ابدأ" / "اعتمد")',
            'يبدأ بتعديل الملفات تلقائياً دون انتظار',
            'يجب إعادة تشغيل بيئة العمل'
          ],
          correctIndex: 0,
          explanationEn: 'Right! Agent OS respects hard-stop gates and only transitions to execution when you give the explicit "proceed" signal.',
          explanationAr: 'صحيح! يحترم النظام بوابات التوقف ولا ينتقل للتنفيذ إلا عندما تعطيه إشارة "proceed" الصريحة.'
        }
      },
      {
        id: 'ch-daily',
        trackId: 'track-start',
        feedCategory: 'ops',
        badgeEn: 'Lesson 1.3',
        badgeAr: 'درس 1.3',
        xp: 25,
        readTimeEn: '2 min read',
        readTimeAr: 'قراءة دقيقتين',
        authorEn: 'Daily Planner Engine',
        authorAr: 'محرك التخطيط اليومي',
        roleEn: 'Session Triage & Continuity',
        roleAr: 'فرز الجلسة واستمرارية العمل',
        titleEn: 'Daily Triage (`/plan-daily`) & Session Continuity (`PROGRESS.md`)',
        titleAr: 'التخطيط اليومي (`/plan-daily`) واستمرارية الجلسات (`PROGRESS.md`)',
        summaryEn: 'Never waste morning energy wondering what to do next or re-explaining yesterday\'s architecture to a fresh chat session.',
        summaryAr: 'لا تضيع طاقة الصباح في التفكير من أين تبدأ أو إعادة شرح ما أنجزته بالأمس في محادثة جديدة.',
        bulletsEn: [
          'Run /plan-daily at the start of any session: it inspects git status, PROGRESS.md, DECISIONS.md, and test health, then recommends ONE primary focus.',
          'At the end of every task, Agent OS updates PROGRESS.md and DECISIONS.md automatically so the next chat session resumes with 100% context.',
          'Want to create a brand-new skill or CLI tool in Agent OS? Run /plan-daily --skill <name> to scaffold, wire, and test it end-to-end.'
        ],
        bulletsAr: [
          'شغل /plan-daily في بداية أي جلسة: يفحص حالة Git وملفي PROGRESS.md وDECISIONS.md وصحة الاختبارات، ثم يقترح مهمة أساسية واحدة لليوم.',
          'في نهاية كل مهمة، يحدث النظام ملفي PROGRESS.md وDECISIONS.md تلقائياً لتبدأ المحادثة القادمة بكامل السياق.',
          'هل تريد إضافة مهارة أو أداة جديدة للنظام؟ استخدم /plan-daily --skill <name> لبنائها وربطها واختبارها بالكامل.'
        ],
        beforeEn: 'Opening a new chat and spending 20 minutes pasting old files so the AI remembers what was built yesterday.',
        beforeAr: 'فتح محادثة جديدة وقضاء 20 دقيقة في نسخ الملفات القديمة ليتذكر الذكاء الاصطناعي ما تم بناؤه بالأمس.',
        afterEn: 'Typing /plan-daily — Agent OS reads PROGRESS.md & DECISIONS.md in 2 seconds and presents today\'s #1 priority.',
        afterAr: 'كتابة /plan-daily — يقرأ النظام سجل التقدم والقرارات في ثانيتين ويعرض لك الأولوية رقم 1 لليوم.',
        exampleTitleEn: 'Example: Running Autonomous Morning Triage',
        exampleTitleAr: 'مثال: تشغيل الفرز الصباحي التلقائي للمهام',
        command: '/plan-daily',
        promptEn: '/plan-daily Check current repo health and recommend today\'s primary engineering focus.',
        promptAr: '/plan-daily افحص حالة المشروع الحالية واقترح المهمة الهندسية الأساسية لليوم.',
        chainedSkills: ['/plan-daily', '/engineering-workflow', '/clean-code-guard'],
        simQuestionsEn: [
          'Session Triage: Scanned git working tree + PROGRESS.md + 35 unit tests (100% passing).',
          'Primary Focus Selected: Complete payment webhook idempotency guard -> Reply "proceed" to begin.'
        ],
        simQuestionsAr: [
          'فرز الجلسة: تم فحص شجرة Git وسجل التقدم و35 اختباراً برمجياً (جميعها ناجحة).',
          'المهمة المقترحة لليوم: استكمال حارس عدم تكرار إشعارات الدفع -> اكتب "proceed" للبدء.'
        ],
        quiz: {
          questionEn: 'Which two files does Agent OS maintain automatically so new chat sessions remember your project state and architectural rules?',
          questionAr: 'ما هما الملفان اللذان يحدثهما النظام تلقائياً لتتذكر المحادثات الجديدة حالة المشروع وقراراته المعمارية؟',
          optionsEn: [
            'PROGRESS.md and DECISIONS.md',
            'temp.txt and notes.doc',
            'It does not save anything between sessions'
          ],
          optionsAr: [
            'ملفا PROGRESS.md و DECISIONS.md',
            'ملفا temp.txt و notes.doc',
            'لا يحفظ النظام أي شيء بين الجلسات'
          ],
          correctIndex: 0,
          explanationEn: 'Spot on! PROGRESS.md tracks completed/next tasks and DECISIONS.md locks architectural decisions (ADRs) enforced by adr_enforcer.py.',
          explanationAr: 'ممتاز! يحفظ PROGRESS.md المهام المنجزة والقادمة، ويوثق DECISIONS.md القرارات المعمارية المعتمدة.'
        }
      }
    ]
  },
  {
    id: 'track-combos',
    titleEn: 'Track 2: The 11 Situation Combos',
    titleAr: 'المسار 2: الأوامر الشاملة الـ 11',
    lessons: [
      {
        id: 'ch-start-project',
        trackId: 'track-combos',
        feedCategory: 'features',
        badgeEn: 'Combo 1 & 2',
        badgeAr: 'الأمر 1 و 2',
        xp: 30,
        readTimeEn: '4 min read',
        readTimeAr: 'قراءة 4 دقائق',
        authorEn: 'Start-Project Architect',
        authorAr: 'مهندس المشاريع الجديدة',
        roleEn: 'Full-Stack App Scaffolder',
        roleAr: 'مؤسس المشاريع المتكاملة',
        titleEn: '`/start-project`: Build a Brand-New App From Zero in Any Stack',
        titleAr: '`/start-project`: بناء مشروع جديد من الصفر بأي تقنية',
        summaryEn: 'The master command for new projects: runs the Frontier Smart Intake interview, authors the 6 Pre-Coding architecture docs, and scaffolds Frontend, Backend, and Database.',
        summaryAr: 'الأمر الرئيسي للمشاريع الجديدة: يجري مقابلة المتطلبات الذكية، ويكتب الوثائق الهندسية الست، ويبني الواجهة والخلفية وقاعدة البيانات.',
        bulletsEn: [
          'Runs Q1-Q28 in short Frontier Rounds (3-5 questions at a time) so you never face a wall of text.',
          'Generates docs/specs/ (01-PRD, 02-TRD, 03-App-Flow 5-State UI Matrix, 04-Design-Brief, 05-Backend-Schema, 06-Implementation-Plan).',
          'Locks tokens.json and .design-lock.md before scaffolding your chosen stack (Astro, Next.js, Laravel, Nuxt, or HTML/Tailwind).'
        ],
        bulletsAr: [
          'يطرح الأسئلة في جولات قصيرة (3-5 أسئلة في كل جولة) لتجنب الإرهاق أو النصوص الطويلة.',
          'ينشئ الوثائق الهندسية الست في مجلد docs/specs/ شاملة المتطلبات وتدفق الشاشات ومخطط قاعدة البيانات.',
          'يعتمد ملفات tokens.json و.design-lock.md قبل بناء الكود بالتقنية التي اخترتها.'
        ],
        beforeEn: 'Scaffolding a new project without a PRD, schema, or design tokens — resulting in mismatched colors and database rewrites a week later.',
        beforeAr: 'بناء مشروع جديد بدون وثيقة متطلبات أو مخطط قاعدة بيانات أو رموز ألوان — مما يؤدي لإعادة كتابة المشروع بعد أسبوع.',
        afterEn: 'Running /start-project once to lock all 6 Pre-Coding documents, WCAG-verified tokens, and a clean initial codebase.',
        afterAr: 'تشغيل /start-project مرة واحدة لاعتماد الوثائق الست ورموز التصميم المتوافقة وبنية الكود النظيفة.',
        exampleTitleEn: 'Example: Launching a Bilingual SaaS Platform From Scratch',
        exampleTitleAr: 'مثال: إطلاق منصة سحابية ثنائية اللغة من الصفر',
        command: '/start-project',
        promptEn: '/start-project Build a bilingual (AR/EN) clinic appointment and billing management platform with Admin, Doctor, and Receptionist roles.',
        promptAr: '/start-project ابن منصة ثنائية اللغة (عربي/إنجليزي) لإدارة مواعيد وفواتير العيادات بصلاحيات مدير وطبيب وموظف استقبال.',
        chainedSkills: ['/start-project', '/grill-me', '/muaz-skill', '/web-precode', '/spec-kit', '/feature-full'],
        simQuestionsEn: [
          'Round 1 (Actors & Auth): Confirm role hierarchy -> (Suggested) Super Admin > Clinic Doctor > Receptionist > Patient Portal',
          'Round 2 (Billing & Currency): Primary invoice currency and tax rule? -> (Suggested) Multi-currency ledger with immutable paid receipts'
        ],
        simQuestionsAr: [
          'الجولة 1 (المستخدمون والصلاحيات): تأكيد تسلسل الأدوار -> (المقترح) مدير عام > طبيب > موظف استقبال > بوابة المريض',
          'الجولة 2 (الفوترة والعملة): العملة الأساسية وقواعد الإيصالات؟ -> (المقترح) سجل مالي غير قابل للتعديل بعد الدفع'
        ],
        quiz: {
          questionEn: 'What does /start-project generate in docs/specs/ before writing production application code?',
          questionAr: 'ماذا ينشئ أمر /start-project داخل مجلد docs/specs/ قبل كتابة الكود الإنتاجي؟',
          optionsEn: [
            'The 6 Pre-Coding Pillar documents (PRD, TRD, App Flow, Design Brief, Schema, Plan)',
            'Only a README file',
            'Nothing, it skips planning completely'
          ],
          optionsAr: [
            'الوثائق الهندسية الست (PRD, TRD, App Flow, Design Brief, Schema, Plan)',
            'ملف README فقط',
            'لا ينشئ أي شيء ويتخطى التخطيط'
          ],
          correctIndex: 0,
          explanationEn: 'Correct! The 6 Pre-Coding Pillars ensure every route, table, and UI state is designed before coding begins.',
          explanationAr: 'صحيح! تضمن الوثائق الهندسية الست تصميم كل مسار وجدول وحالة واجهة قبل بدء البرمجة.'
        }
      },
      {
        id: 'ch-smart-feature',
        trackId: 'track-combos',
        feedCategory: 'features',
        badgeEn: 'Combo 3',
        badgeAr: 'الأمر 3',
        xp: 25,
        readTimeEn: '3 min read',
        readTimeAr: 'قراءة 3 دقائق',
        authorEn: 'Smart Feature Router',
        authorAr: 'موجه الميزات الذكي',
        roleEn: 'Auto-Skill Dispatcher',
        roleAr: 'موزع المهارات التلقائي',
        titleEn: '`/smart-feature`: Describe What You Want, It Picks the Skills',
        titleAr: '`/smart-feature`: اشرح ما تريد بلغة عادية وهو يختار المهارات',
        summaryEn: 'Not sure whether your task needs database migrations, backend APIs, or only frontend UI? Type /smart-feature and let Agent OS inspect your repo and route automatically.',
        summaryAr: 'لست متأكداً هل تحتاج المهمة إلى تعديل قاعدة البيانات أم الخلفية أم الواجهة فقط؟ اكتب /smart-feature ليقوم النظام بفحص مشروعك واختيار المهارات تلقائياً.',
        bulletsEn: [
          'Scans package.json, composer.json, or astro.config.mjs to detect your exact tech stack.',
          'Determines whether the feature touches UI only (/feature-fe), UI + API (/feature-febe), or UI + API + DB (/feature-full).',
          'Runs the short Smart Intake interview and executes all matching security and RTL guards automatically.'
        ],
        bulletsAr: [
          'يفحص ملفات المشروع لاكتشاف التقنية المستخدمة بدقة (Astro أو Next.js أو Laravel أو Vue أو WordPress).',
          'يحدد تلقائياً هل تتطلب الميزة واجهة فقط أم واجهة وخلفية أم واجهة وخلفية وقاعدة بيانات.',
          'يجري مقابلة المتطلبات القصيرة ويشغل جميع حراس الأمان واللغة العربية تلقائياً.'
        ],
        beforeEn: 'Guessing which internal skill to call and forgetting to include database indexing or server-side authorization.',
        beforeAr: 'تخمين اسم المهارة الداخلية ونسيان تضمين فهارس قاعدة البيانات أو فحص الصلاحيات في الخادم.',
        afterEn: 'Using /smart-feature with a plain Arabic or English sentence — routing, building, and auditing happen in one workflow.',
        afterAr: 'استخدام /smart-feature بجملة عربية أو إنجليزية بسيطة — ليتم التوجيه والبناء والفحص في مسار واحد.',
        exampleTitleEn: 'Example: Letting `/smart-feature` Route a Multi-Layer Task',
        exampleTitleAr: 'مثال: ترك `/smart-feature` يوجه مهمة متعددة الطبقات',
        command: '/smart-feature',
        promptEn: '/smart-feature Add an export-to-CSV button and date-range filter on the admin transactions table.',
        promptAr: '/smart-feature أضف زر تصدير CSV وتصفية حسب التاريخ في جدول المعاملات بلوحة التحكم.',
        chainedSkills: ['/smart-feature', '/feature-febe', '/backend-http', '/backend-identity', '/rtl-logical-guard'],
        simQuestionsEn: [
          'Stack Detected: Astro / TypeScript + REST endpoint -> Routed to /feature-febe (UI + API validation).',
          'Q1 (Export Limit): Maximum rows per CSV export? -> (Suggested) Stream up to 10,000 rows with server RBAC check'
        ],
        simQuestionsAr: [
          'التقنية المكتشفة: Astro / TypeScript مع نقطة نهاية API -> تم التوجيه إلى /feature-febe.',
          'س1 (حد التصدير): الحد الأقصى للصفوف في ملف CSV؟ -> (المقترح) حتى 10,000 صف مع فحص صلاحية المدير بالخادم'
        ],
        quiz: {
          questionEn: 'When should you use /smart-feature?',
          questionAr: 'متى يفضل استخدام أمر /smart-feature؟',
          optionsEn: [
            'Whenever you want to describe a feature in plain language and let Agent OS auto-select UI, API, and DB skills',
            'Only when editing README files',
            'Only for deleting old git branches'
          ],
          optionsAr: [
            'عندما تريد وصف ميزة بلغة عادية وترك النظام يختار مهارات الواجهة والخلفية وقاعدة البيانات تلقائياً',
            'فقط عند تعديل ملفات التوثيق',
            'فقط عند حذف فروع Git القديمة'
          ],
          correctIndex: 0,
          explanationEn: 'Exactly! /smart-feature is your universal entry point whenever you do not want to think about which layer a feature touches.',
          explanationAr: 'بالضبط! أمر /smart-feature هو نقطة الدخول الموحدة عندما لا ترغب في التفكير أي طبقة برمجية ستتأثر بالميزة.'
        }
      },
      {
        id: 'ch-feature-full',
        trackId: 'track-combos',
        feedCategory: 'features',
        badgeEn: 'Combo 4 & 5',
        badgeAr: 'الأمر 4 و 5',
        xp: 30,
        readTimeEn: '4 min read',
        readTimeAr: 'قراءة 4 دقائق',
        authorEn: 'Full-Stack Builder',
        authorAr: 'باني الميزات المتكاملة',
        roleEn: 'UI + API + DB Orchestrator',
        roleAr: 'منسق الواجهة والخلفية والبيانات',
        titleEn: '`/feature-full` vs `/feature-febe`: Full-Stack DB Features vs UI+API',
        titleAr: 'الفرق بين `/feature-full` و`/feature-febe`: متى تشمل قاعدة البيانات؟',
        summaryEn: 'Use /feature-full when your feature adds or alters database tables/columns; use /feature-febe when connecting new UI and backend endpoints to existing tables.',
        summaryAr: 'استخدم /feature-full عندما تضيف الميزة جداول أو أعمدة جديدة في قاعدة البيانات، واستخدم /feature-febe عند بناء واجهة وخلفية على جداول موجودة مسبقاً.',
        bulletsEn: [
          '/feature-full chains /feature-febe + /database + /backend-data: enforces foreign keys, compound indexes, soft deletes, N+1 prevention, and ACID transactions.',
          '/feature-febe chains /feature-fe + /backend-api + /backend-identity: enforces server-side session derivation, anti-IDOR ownership checks, and strict payload validation.',
          'Both commands automatically enforce responsive CMS tables, sticky navigation, and RTL logical properties.'
        ],
        bulletsAr: [
          'يدمج /feature-full مهارات الواجهة والخلفية مع هندسة قواعد البيانات: يفرض المفاتيح الخارجية والفهارس المركبة ومنع استعلامات N+1 والمعاملات الآمنة.',
          'يدمج /feature-febe مهارات الواجهة مع الـ API والصلاحيات: يفرض اشتقاق الجلسة من الخادم وفحص ملكية السجل (Anti-IDOR) والتحقق من المدخلات.',
          'كلا الأمرين يفرضان تلقائياً الجداول المتجاوبة والأشرطة الثابتة وخصائص CSS المنطقية للعربية.'
        ],
        beforeEn: 'Creating a new "Coupons" feature where the frontend works in mock state, the API lacks ownership checks, and the DB table has no index on coupon_code.',
        beforeAr: 'إنشاء ميزة "كوبونات خصم" تعمل في الواجهة ببيانات وهمية، وبدون فحص صلاحيات في الخلفية، وبدون فهرس سريع لكود الكوبون في قاعدة البيانات.',
        afterEn: 'Running /feature-full to build the indexed coupons migration, atomic redemption transaction, admin CRUD table, and security tests together.',
        afterAr: 'تشغيل /feature-full لبناء جدول الكوبونات المفهرس، ومعاملة الاستخدام الذرية، وجدول الإدارة المتجاوب، واختبارات الأمان معاً.',
        exampleTitleEn: 'Example: Building a Complete Database-Backed Feature',
        exampleTitleAr: 'مثال: بناء ميزة متكاملة مرتبطة بقاعدة البيانات',
        command: '/feature-full',
        promptEn: '/feature-full Create a discount coupons module with usage limits, expiry dates, admin CRUD table, and atomic checkout redemption.',
        promptAr: '/feature-full أنشئ وحدة كوبونات خصم مع حد أقصى للاستخدام وتاريخ انتهاء وجدول إدارة كامل وعملية خصم ذرية عند الدفع.',
        chainedSkills: ['/feature-full', '/database', '/backend-data', '/backend-identity', '/next-server-action-guard', '/pest-security-guard'],
        simQuestionsEn: [
          'Q1 (Concurrency): How should simultaneous redemptions of the last coupon be handled? -> (Suggested) Pessimistic row lock (SELECT FOR UPDATE) inside DB transaction',
          'Q2 (Admin UI): How should expired coupons appear in the admin table? -> (Suggested) Semantic status dot + filter tab without deleting historical order links'
        ],
        simQuestionsAr: [
          'س1 (التزامن): كيف نعالج محاولة استخدام آخر كوبون في نفس اللحظة؟ -> (المقترح) قفل الصف داخل معاملة قاعدة البيانات لمنع السحب المزدوج',
          'س2 (واجهة الإدارة): كيف تظهر الكوبونات المنتهية في الجدول؟ -> (المقترح) نقطة حالة دلالية مع تبويب تصفية دون حذف ارتباطات الطلبات السابقة'
        ],
        quiz: {
          questionEn: 'Which command should you choose when adding a new database table, backend API endpoint, and Admin CMS table all together?',
          questionAr: 'أي أمر تختار عندما تريد إضافة جدول جديد في قاعدة البيانات مع نقطة نهاية API وجدول في لوحة التحكم معاً؟',
          optionsEn: [
            '/feature-full',
            '/fix-ui',
            '/save-data'
          ],
          optionsAr: [
            '/feature-full',
            '/fix-ui',
            '/save-data'
          ],
          correctIndex: 0,
          explanationEn: 'Correct! /feature-full covers Frontend UI + Backend API + Database Schema & Migrations.',
          explanationAr: 'صحيح! يغطي أمر /feature-full الواجهة الأمامية والخلفية ومخطط قاعدة البيانات معاً.'
        }
      },
      {
        id: 'ch-feature-fe-wp',
        trackId: 'track-combos',
        feedCategory: 'cms',
        badgeEn: 'Combo 6 & 7',
        badgeAr: 'الأمر 6 و 7',
        xp: 25,
        readTimeEn: '3 min read',
        readTimeAr: 'قراءة 3 دقائق',
        authorEn: 'Frontend & WP Specialist',
        authorAr: 'خبير الواجهات وووردبريس',
        roleEn: 'UI & WooCommerce Architect',
        roleAr: 'مهندس الواجهات وووكرومرس',
        titleEn: '`/feature-fe` (Frontend/CMS UI) & `/feature-wp` (WordPress/WooCommerce)',
        titleAr: '`/feature-fe` (الواجهات ولوحات التحكم) و`/feature-wp` (ووردبريس وووكرومرس)',
        summaryEn: 'Build pixel-accurate, mobile-first Frontend/CMS screens with /feature-fe, or HPOS-compliant WordPress & WooCommerce plugins/themes with /feature-wp.',
        summaryAr: 'ابن واجهات أمامية ولوحات تحكم متجاوبة عبر /feature-fe، أو قوالب وإضافات ووردبريس وووكرومرس متوافقة مع HPOS عبر /feature-wp.',
        bulletsEn: [
          '/feature-fe works across Astro, React, Next.js, Vue, Nuxt, Blade, and HTML/Tailwind: enforces 100dvh Hero math, sticky navbars, 3-card grids with Show More, and RTL logical properties.',
          '/feature-wp chains /wp-guard + /woo-guard: enforces wp_verify_nonce, current_user_can, $wpdb->prepare, and wc_get_order() CRUD (never direct wp_postmeta queries).',
          'Both reject AI-slop patterns (no emojis as icons, no translucent blur overlays, no arbitrary hexes).'
        ],
        bulletsAr: [
          'يعمل /feature-fe مع Astro وReact وNext.js وVue وBlade وHTML/Tailwind: يفرض حساب ارتفاع الواجهة الرئيسية والأشرطة الثابتة وشبكة الـ 3 بطاقات ودعم العربية.',
          'يدمج /feature-wp حارسي ووردبريس وووكرومرس: يفرض فحص Nonce والصلاحيات والاستعلامات المحضرة ودوال الطلبات المتوافقة مع HPOS.',
          'كلاهما يمنع أنماط التصميم العشوائي مثل الإيموجي كأيقونات أو التمويه الزجاجي أو الألوان العشوائية.'
        ],
        beforeEn: 'Writing a WooCommerce plugin that queries wp_postmeta directly — breaking stores that have High-Performance Order Storage (HPOS) enabled.',
        beforeAr: 'كتابة إضافة ووكرومرس تستعلم من جدول wp_postmeta مباشرة — مما يعطل المتاجر التي تفعل تخزين الطلبات عالي الأداء (HPOS).',
        afterEn: 'Running /feature-wp so every order read/write uses wc_get_order() CRUD methods and declares HPOS compatibility.',
        afterAr: 'تشغيل /feature-wp بحيث تستخدم جميع عمليات الطلبات دوال wc_get_order() القياسية وتعلن التوافق الرسمي مع HPOS.',
        exampleTitleEn: 'Example: Building a Mobile-First CMS Analytics Screen',
        exampleTitleAr: 'مثال: بناء شاشة إحصائيات متجاوبة في لوحة التحكم',
        command: '/feature-fe',
        promptEn: '/feature-fe Build a vendor analytics page with 3 KPI cards, a collapsible category grid, and a responsive payout history table.',
        promptAr: '/feature-fe ابن صفحة إحصائيات للتجار تضم 3 بطاقات مؤشرات وشبكة تصنيفات قابلة للطي وجدول سجل دفعات متجاوب.',
        chainedSkills: ['/feature-fe', '/muaz-skill', '/rtl-logical-guard', '/ui-audit', '/clean-code-guard'],
        simQuestionsEn: [
          'Q1 (Card Grid Overflow): When a vendor has more than 3 category cards, how should they render? -> (Suggested) 3 cards per row on desktop (1 on mobile) with "Show More / Collapse All" toggle',
          'Q2 (Table Cell Truncation): How should long payout notes render on mobile? -> (Suggested) Truncate to 2-4 words + "..." with Details modal'
        ],
        simQuestionsAr: [
          'س1 (شبكة البطاقات): عند وجود أكثر من 3 بطاقات في القسم، كيف تعرض؟ -> (المقترح) 3 بطاقات في الصف على الحاسوب (وواحدة على الجوال) مع زر عرض المزيد / طي الكل',
          'س2 (اختصار الجدول): كيف تعرض الملاحظات الطويلة في الجدول؟ -> (المقترح) اختصار إلى 2-4 كلمات مع زر عرض التفاصيل في نافذة منبثقة'
        ],
        quiz: {
          questionEn: 'In /feature-wp, how must WooCommerce order data be accessed to remain HPOS-compatible?',
          questionAr: 'في أمر /feature-wp، كيف يجب الوصول لبيانات طلبات ووكرومرس لضمان التوافق مع نظام HPOS؟',
          optionsEn: [
            'Using wc_get_order() and WooCommerce CRUD methods ($order->get_meta / update_meta_data)',
            'Writing raw SQL against wp_posts and wp_postmeta',
            'Storing order totals in browser cookies'
          ],
          optionsAr: [
            'باستخدام دالة wc_get_order() ودوال CRUD الرسمية في ووكرومرس',
            'كتابة استعلام SQL مباشر على جدول wp_postmeta',
            'تخزين إجمالي الطلب في ملفات تعريف الارتباط بالمتصفح'
          ],
          correctIndex: 0,
          explanationEn: 'Correct! Direct wp_postmeta access breaks HPOS stores; wc_get_order() CRUD works across all WooCommerce storage engines.',
          explanationAr: 'إجابة صحيحة! الاستعلام المباشر من wp_postmeta يكسر متاجر HPOS، بينما تعمل دوال wc_get_order() مع جميع محركات التخزين.'
        }
      },
      {
        id: 'ch-fixers',
        trackId: 'track-combos',
        feedCategory: 'bugs',
        badgeEn: 'Combo 8 & 9',
        badgeAr: 'الأمر 8 و 9',
        xp: 30,
        readTimeEn: '3 min read',
        readTimeAr: 'قراءة 3 دقائق',
        authorEn: 'Diagnostic & Repair Lead',
        authorAr: 'قائد التشخيص والإصلاح',
        roleEn: 'UI & Backend Bug Hunter',
        roleAr: 'صائد أعطال الواجهة والخلفية',
        titleEn: '`/fix-ui` & `/fix-backend`: Surgical Bug Fixing Without Regressions',
        titleAr: '`/fix-ui` و`/fix-backend`: إصلاح الأعطال بدقة وبدون آثار جانبية',
        summaryEn: 'When a table overflows on mobile, an Arabic layout is flipped, or an API throws a 500 error, use /fix-ui or /fix-backend for root-cause repair.',
        summaryAr: 'عندما يخرج جدول عن شاشة الجوال، أو ينقلب اتجاه العربية، أو يظهر خطأ 500 في الخادم، استخدم /fix-ui أو /fix-backend للإصلاح الجذري.',
        bulletsEn: [
          '/fix-ui runs ui_audit_engine.py first to pinpoint broken sticky bars, overflowing flex children (missing min-w-0), overlapping input icons, and physical CSS classes.',
          '/fix-backend traces the authority chain (Route -> Middleware -> Controller/Action -> DB Query) to fix N+1 queries, missing auth checks, broken file uploads, and race conditions.',
          'Both preserve 100% of your existing brand colors, fonts, navbar, footer, and unrelated routes.'
        ],
        bulletsAr: [
          'يشغل /fix-ui محرك فحص الواجهة أولاً لتحديد الأشرطة غير الثابتة، والعناصر الخارجة عن الحاوية، وتداخل أيقونات البحث، والكلاسات الفيزيائية الخاطئة.',
          'يتتبع /fix-backend سلسلة الصلاحيات والبيانات لإصلاح استعلامات N+1، ونقص فحص الهوية، وأعطال رفع الملفات، وتضارب العمليات المتزامنة.',
          'يحافظ كلا الأمرين بنسبة 100% على ألوان الهوية والخطوط والشريط العلوي والتذييل والمسارات الأخرى.'
        ],
        beforeEn: 'Asking raw AI to "fix the mobile table" and watching it delete half the columns and change your website\'s primary brand color.',
        beforeAr: 'الطلب من ذكاء اصطناعي عادي "إصلاح الجدول على الجوال" ومشاهدته يحذف نصف الأعمدة ويغير اللون الأساسي للموقع.',
        afterEn: 'Running /fix-ui to add overflow-x-auto, min-w-0, and 3-word cell truncation while keeping 100% of existing data and brand tokens intact.',
        afterAr: 'تشغيل /fix-ui لإضافة التمرير الداخلي واختصار الخلايا مع الحفاظ الكامل على جميع البيانات وألوان الهوية.',
        exampleTitleEn: 'Example: Fixing Mobile Overflow & RTL Icon Collision',
        exampleTitleAr: 'مثال: إصلاح خروج الجدول عن الشاشة وتداخل أيقونة البحث بالعربية',
        command: '/fix-ui',
        promptEn: '/fix-ui The search icon overlaps placeholder text in Arabic RTL, and the users table overflows horizontally on 375px mobile screens.',
        promptAr: '/fix-ui أيقونة البحث تتداخل مع النص الإرشادي في الواجهة العربية، وجدول المستخدمين يخرج أفقياً عن شاشة الجوال مقاس 375px.',
        chainedSkills: ['/fix-ui', '/ui-audit', '/rtl-logical-guard', '/muaz-skill', '/clean-code-guard'],
        simQuestionsEn: [
          'Audit Finding 1: Search input used physical pl-10 left-3 -> Converting to logical ps-10 start-3 pointer-events-none.',
          'Audit Finding 2: Table wrapper lacked overflow-x-auto and cell truncation -> Wrapping table and adding Details modal.'
        ],
        simQuestionsAr: [
          'نتيجة الفحص 1: حقل البحث يستخدم pl-10 left-3 الفيزيائية -> سيتم التحويل إلى ps-10 start-3 المنطقية.',
          'نتيجة الفحص 2: حاوية الجدول تفتقر إلى overflow-x-auto واختصار الخلايا -> سيتم تغليف الجدول وإضافة نافذة التفاصيل.'
        ],
        quiz: {
          questionEn: 'Why do search icons often overlap placeholder text when switching from English (LTR) to Arabic (RTL)?',
          questionAr: 'لماذا تتداخل أيقونات البحث غالباً مع النص الإرشادي عند التحويل من الإنجليزية إلى العربية؟',
          optionsEn: [
            'Because physical classes like left-3 and pl-10 were used instead of logical start-3 and ps-10',
            'Because Arabic fonts cannot be used inside input elements',
            'Because HTML inputs do not support SVG icons'
          ],
          optionsAr: [
            'بسبب استخدام كلاسات فيزيائية مثل left-3 و pl-10 بدلاً من الكلاسات المنطقية start-3 و ps-10',
            'لأن الخطوط العربية لا تعمل داخل حقول الإدخال',
            'لأن حقول HTML لا تدعم أيقونات SVG'
          ],
          correctIndex: 0,
          explanationEn: 'Exact! Logical properties (start-3 + ps-10) automatically flip sides when dir="rtl" is active.',
          explanationAr: 'صحيح تماماً! الخصائص المنطقية (start-3 مع ps-10) تعكس اتجاهها تلقائياً عند تفعيل dir="rtl".'
        }
      },
      {
        id: 'ch-ops-combos',
        trackId: 'track-combos',
        feedCategory: 'ops',
        badgeEn: 'Combo 10, 11 & 12',
        badgeAr: 'الأمر 10 و11 و12',
        xp: 30,
        readTimeEn: '3 min read',
        readTimeAr: 'قراءة 3 دقائق',
        authorEn: 'Quality & Ops Guard',
        authorAr: 'حارس الجودة والتشغيل',
        roleEn: 'Pre-Push & Bandwidth Lead',
        roleAr: 'مسؤول الفحص وتوفير البيانات',
        titleEn: '`/check-all`, `/save-data`, & `/doc-project`: Audit, Save Bandwidth, & Document',
        titleAr: '`/check-all` و`/save-data` و`/doc-project`: الفحص الشامل وتوفير الإنترنت والتوثيق',
        summaryEn: 'Run a 7-guard pre-push audit with /check-all, slash mobile hotspot usage by 85% with /save-data, and generate verified project docs with /doc-project.',
        summaryAr: 'شغل 7 حراس فحص قبل الرفع بأمر /check-all، ووفر 85% من باقة الإنترنت بأمر /save-data، ووثق مشروعك بدقة بأمر /doc-project.',
        bulletsEn: [
          '/check-all chains /clean-code-guard, /test-guard, /rtl-logical-guard, /next-server-action-guard, /pest-security-guard, /ponytail-review, and /debate-review.',
          '/save-data chains bandwidth_guard.py + /caveman lite + offline npm/pnpm/composer/pip caches.',
          '/doc-project scans real source files to generate or update README.md, docs/ARCHITECTURE.md, and docs/API.md, then verifies every symbol via /docs-guard.'
        ],
        bulletsAr: [
          'يشغل /check-all سبعة حراس متتاليين للكود النظيف والاختبارات والعربية وأمان الخادم ومنع التعقيد والمراجعة المزدوجة.',
          'يفعل /save-data حماية النطاق الترددي والردود المختصرة والتخزين المحلي لمديري الحزم.',
          'يمسح /doc-project ملفات الكود الحقيقية لتوليد وتحديث ملفات README والهندسة المعمارية والـ API ثم يدققها عبر حارس التوثيق.'
        ],
        beforeEn: 'Pushing unreviewed code that fails CI, or shipping a README whose installation commands no longer match package.json.',
        beforeAr: 'رفع كود غير مفحوص يفشل في الاختبارات، أو تسليم ملف README تحتوي أوامره على أسماء سكربتات قديمة غير موجودة.',
        afterEn: 'Running /check-all and /doc-project before release so every guard passes and every documented command is verified against source.',
        afterAr: 'تشغيل /check-all و/doc-project قبل الإطلاق لضمان نجاح جميع الحراس ومطابقة التوثيق للكود الفعلي.',
        exampleTitleEn: 'Example: Running Full Pre-Release Verification',
        exampleTitleAr: 'مثال: تشغيل الفحص الشامل قبل تسليم المشروع',
        command: '/check-all',
        promptEn: '/check-all Audit my current working tree changes before we prepare the release.',
        promptAr: '/check-all افحص جميع التعديلات الحالية في المشروع قبل التحضير للإطلاق.',
        chainedSkills: ['/check-all', '/clean-code-guard', '/test-guard', '/rtl-logical-guard', '/ponytail-review', '/debate-review'],
        simQuestionsEn: [
          'Guard 1-4: clean-code-guard (PASS), test-guard (PASS), rtl-logical-guard (0 physical classes), security-guard (PASS).',
          'Guard 5-7: ponytail-review (0 bloat dependencies), anti_slop.py (0 violations).'
        ],
        simQuestionsAr: [
          'الحراس 1-4: الكود النظيف (ناجح)، الاختبارات (ناجح)، اتجاه العربية (0 أخطاء)، أمان الخادم (ناجح).',
          'الحراس 5-7: فحص البساطة (0 مكتبات زائدة)، فحص منع العشوائية (0 مخالفات).'
        ],
        quiz: {
          questionEn: 'Which command chains 7 quality, security, RTL, test, and anti-bloat guards in one shot before you push code?',
          questionAr: 'أي أمر يقوم بتشغيل 7 حراس للجودة والأمان والعربية والاختبارات ومنع التعقيد في خطوة واحدة قبل رفع الكود؟',
          optionsEn: [
            '/check-all',
            '/start-project',
            '/feature-wp'
          ],
          optionsAr: [
            '/check-all',
            '/start-project',
            '/feature-wp'
          ],
          correctIndex: 0,
          explanationEn: 'Correct! /check-all is your single pre-push gate across code, tests, UI, RTL, and security.',
          explanationAr: 'صحيح! أمر /check-all هو بوابة الفحص الشاملة قبل الرفع.'
        }
      }
    ]
  },
  {
    id: 'track-cms',
    titleEn: 'Track 3: CMS, Mobile & Spec-Kit Armor',
    titleAr: 'المسار 3: درع الجوال ولوحات التحكم والمواصفات',
    lessons: [
      {
        id: 'ch-cms-shell',
        trackId: 'track-cms',
        feedCategory: 'cms',
        badgeEn: 'Lesson 3.1',
        badgeAr: 'درس 3.1',
        xp: 25,
        readTimeEn: '3 min read',
        readTimeAr: 'قراءة 3 دقائق',
        authorEn: 'CMS Shell Architect',
        authorAr: 'مهندس هيكل لوحات التحكم',
        roleEn: 'Layout & Navigation Guard',
        roleAr: 'حارس التخطيط والتنقل',
        titleEn: 'Public vs. Admin Shell Separation & Sticky Navigation Rules',
        titleAr: 'فصل واجهة الموقع عن لوحة التحكم وقواعد التثبيت القياسية',
        summaryEn: 'Master the non-negotiable shell rules: 100dvh Hero math, sticky top-0 navbars without overflow-hidden traps, and h-dvh admin sidebars.',
        summaryAr: 'أتقن القواعد الأساسية لهيكل التطبيقات: حساب ارتفاع الواجهة الرئيسية، وتثبيت الشريط العلوي، والقائمة الجانبية المستقلة في لوحة التحكم.',
        bulletsEn: [
          'Public vs Admin Separation: Public pages and /admin/* share design tokens, but never render the public navbar inside /admin/* or the admin sidebar on public pages.',
          'Hero 100dvh Rule: Always subtract navbar height using min-h-[calc(100dvh-var(--navbar-height))] so the fold fits mobile, tablet, and desktop with zero vertical overflow.',
          'Sticky Ancestor Rule: Never put overflow-hidden on body or layout wrappers (which breaks position: sticky); use overflow-x-clip instead.'
        ],
        bulletsAr: [
          'فصل الواجهة العامة عن الإدارة: تشترك الصفحات العامة ولوحة التحكم في رموز الألوان، لكن لا يظهر شريط الموقع العام داخل الإدارة ولا القائمة الجانبية في الصفحات العامة.',
          'قاعدة ارتفاع الواجهة 100dvh: اطرح دائماً ارتفاع الشريط العلوي لضمان ظهور القسم الأول بالكامل بدون تمرير رأسي زائد.',
          'قاعدة التثبيت: لا تضع overflow-hidden على الحاويات الأب لأنها تعطل خاصية sticky؛ استخدم overflow-x-clip بدلاً منها.'
        ],
        beforeEn: 'Putting overflow-hidden on the page wrapper — causing the sticky navbar and admin sidebar to scroll away off-screen.',
        beforeAr: 'وضع overflow-hidden على الحاوية الرئيسية للصفحة — مما يؤدي لاختفاء الشريط العلوي والقائمة الجانبية عند التمرير.',
        afterEn: 'Using overflow-x-clip on the root shell, sticky top-0 z-40 on the navbar, and h-dvh sticky sidebar with flex-1 min-w-0 overflow-y-auto main content.',
        afterAr: 'استخدام overflow-x-clip على الغلاف الرئيسي، وتثبيت الشريط العلوي بـ top-0، وتثبيت القائمة الجانبية بارتفاع الشاشة مع تمرير مستقل للمحتوى.',
        exampleTitleEn: 'Example: Inspecting CMS Shell Layout Compliance',
        exampleTitleAr: 'مثال: فحص التزام هيكل لوحة التحكم بالقواعد القياسية',
        command: '/fix-ui',
        promptEn: '/fix-ui Verify our Admin Layout has a sticky h-dvh sidebar, independent content scroll, and one Floating Save button for long forms.',
        promptAr: '/fix-ui تحقق من أن تخطيط لوحة التحكم يضم قائمة جانبية ثابتة بارتفاع الشاشة وتمرير محتوى مستقل وزر حفظ عائم للنماذج الطويلة.',
        chainedSkills: ['/fix-ui', '/ui-audit', '/muaz-skill', '/rtl-logical-guard'],
        simQuestionsEn: [
          'Shell Check 1: Root container uses overflow-x-clip (sticky top-0 preserved).',
          'Shell Check 2: Long CMS editor uses single Floating Save bar + custom Toast notification (0 window.alert calls).'
        ],
        simQuestionsAr: [
          'فحص الهيكل 1: الحاوية الجذرية تستخدم overflow-x-clip (تم الحفاظ على ثبات الشريط العلوي).',
          'فحص الهيكل 2: المحرر الطويل يستخدم شريط حفظ عائماً موحداً وإشعارات مخصصة (صفر استخدام لـ window.alert).'
        ],
        quiz: {
          questionEn: 'Which CSS property should you use on root containers to prevent horizontal scroll WITHOUT breaking sticky navbars?',
          questionAr: 'ما هي خاصية CSS التي يجب استخدامها لمنع التمرير الأفقي دون تعطيل ثبات الشريط العلوي (sticky)؟',
          optionsEn: [
            'overflow-x-clip',
            'overflow-hidden on every div',
            'display: none'
          ],
          optionsAr: [
            'خاصية overflow-x-clip',
            'خاصية overflow-hidden على كل عنصر',
            'خاصية display: none'
          ],
          correctIndex: 0,
          explanationEn: 'Correct! overflow-x-clip clips horizontal overflow without creating a scroll container that traps position: sticky.',
          explanationAr: 'صحيح! تمنع overflow-x-clip التمرير الأفقي دون إنشاء حاوية تمرير تعطل خاصية sticky.'
        }
      },
      {
        id: 'ch-tables-cards',
        trackId: 'track-cms',
        feedCategory: 'cms',
        badgeEn: 'Lesson 3.2',
        badgeAr: 'درس 3.2',
        xp: 25,
        readTimeEn: '3 min read',
        readTimeAr: 'قراءة 3 دقائق',
        authorEn: 'Mobile-First UI Guard',
        authorAr: 'حارس تصميم الجوال أولاً',
        roleEn: 'Data Table & Grid Engineer',
        roleAr: 'مهندس الجداول والشبكات المتجاوبة',
        titleEn: 'Mobile-First Data Tables (2-4 Word Truncation) & 3-Card Grids',
        titleAr: 'جداول البيانات المتجاوبة (اختصار 2-4 كلمات) وشبكات البطاقات الثلاثية',
        summaryEn: 'Keep mobile screens clean at 375px: truncate long table cells to 2-4 words + "..." with a Details modal, and cap card sections at 3 per row with Show More.',
        summaryAr: 'حافظ على نظافة شاشات الجوال مقاس 375px: اختصر خلايا الجداول الطويلة إلى 2-4 كلمات مع نافذة تفاصيل، واعرض 3 بطاقات في الصف مع زر عرض المزيد.',
        bulletsEn: [
          'Responsive Table Wrapper: Always wrap tables in a w-full overflow-x-auto container inside a flex-1 min-w-0 parent.',
          'Cell Truncation Rule: Truncate long descriptions or payloads to the first 2-4 words + "..." and provide a "Details" button that opens a clean modal.',
          '3-Card Grid Rule: Render 1 card per row on mobile and 3 cards per row on desktop (lg:grid-cols-[repeat(3,minmax(0,1fr))]) with a "Show More / Collapse All" button when items > 3.'
        ],
        bulletsAr: [
          'حاوية الجدول المتجاوبة: غلف دائماً الجداول داخل حاوية w-full overflow-x-auto ضمن أب يحمل flex-1 min-w-0.',
          'قاعدة اختصار الخلايا: اختصر الأوصاف الطويلة إلى أول 2-4 كلمات + "..." مع زر "التفاصيل" لفتح نافذة منبثقة واضحة.',
          'قاعدة شبكة البطاقات: اعرض بطاقة واحدة في الصف على الجوال و3 بطاقات على الحاسوب مع زر "عرض المزيد / طي الكل" عند زيادة البطاقات عن 3.'
        ],
        beforeEn: 'Rendering a 60-word description inside a table cell — stretching the row to 300px tall on mobile and squishing all other columns.',
        beforeAr: 'عرض وصف من 60 كلمة داخل خلية جدول — مما يمدد ارتفاع الصف إلى 300 بكسل على الجوال ويضغط بقية الأعمدة.',
        afterEn: 'Displaying "All-in-one master command..." in the cell and opening the full bilingual breakdown inside a modal on click.',
        afterAr: 'عرض "الأمر الشامل لبناء..." داخل الخلية وفتح التفاصيل الكاملة في نافذة منبثقة عند الضغط.',
        exampleTitleEn: 'Example: Auditing Responsive Tables & Card Grids via CLI',
        exampleTitleAr: 'مثال: فحص الجداول المتجاوبة وشبكات البطاقات عبر سطر الأوامر',
        command: '/ui-audit',
        promptEn: 'python D:\\Skills\\.agents\\scripts\\agent_os.py ui-audit scan --dir D:\\Skills\\.agents\\learning-platform',
        promptAr: 'python D:\\Skills\\.agents\\scripts\\agent_os.py ui-audit scan --dir D:\\Skills\\.agents\\learning-platform',
        chainedSkills: ['/ui-audit', '/muaz-skill', '/rtl-logical-guard', '/clean-code-guard'],
        simQuestionsEn: [
          'Dim 5 (Responsive): Verified flex-1 min-w-0 on main column and overflow-x-auto on all data tables.',
          'Dim 4 (Interactions): Verified all buttons include explicit type="button" and focus-visible rings.'
        ],
        simQuestionsAr: [
          'البعد 5 (التجاوب): تم التحقق من وجود flex-1 min-w-0 على العمود الرئيسي وoverflow-x-auto على جميع الجداول.',
          'البعد 4 (التفاعل): تم التحقق من وجود type="button" وحلقات التركيز المرئية على جميع الأزرار.'
        ],
        quiz: {
          questionEn: 'How should long text inside a Data Table cell be displayed on mobile and desktop?',
          questionAr: 'كيف يجب عرض النصوص الطويلة داخل خلايا جدول البيانات على الجوال والحاسوب؟',
          optionsEn: [
            'Truncated to the first 2-4 words + "..." with a click-to-open Details modal for the full content',
            'Left unwrapped so the table becomes 4,000px wide',
            'Deleted permanently from the database'
          ],
          optionsAr: [
            'تختصر إلى أول 2-4 كلمات + "..." مع زر يفتح نافذة منبثقة لعرض التفاصيل الكاملة',
            'تترك بدون التفاف ليصبح عرض الجدول 4000 بكسل',
            'تحذف نهائياً من قاعدة البيانات'
          ],
          correctIndex: 0,
          explanationEn: 'Right! Truncating to 2-4 words + "..." keeps every row scannable while preserving full details in the modal.',
          explanationAr: 'صحيح! اختصار النص إلى 2-4 كلمات يحافظ على تناسق الصفوف مع إتاحة التفاصيل الكاملة في النافذة المنبثقة.'
        }
      },
      {
        id: 'ch-rtl-bilingual',
        trackId: 'track-cms',
        feedCategory: 'cms',
        badgeEn: 'Lesson 3.3',
        badgeAr: 'درس 3.3',
        xp: 25,
        readTimeEn: '3 min read',
        readTimeAr: 'قراءة 3 دقائق',
        authorEn: 'RTL Logical Guard',
        authorAr: 'حارس الاتجاه المنطقي واللغة',
        roleEn: 'Bilingual Layout Enforcer',
        roleAr: 'مدقق الواجهات الثنائية اللغة',
        titleEn: 'Bilingual AR/EN Isolation & CSS Logical Properties (`rtl-logical-guard`)',
        titleAr: 'العزل اللغوي التام (عربي/إنجليزي) وخصائص CSS المنطقية',
        summaryEn: 'Eliminate broken Arabic layouts and mixed-language text leakage by enforcing CSS Logical Properties and strict locale dictionaries.',
        summaryAr: 'تخلص من انكسار الواجهات العربية أو اختلاط النصوص الإنجليزية بالعربية عبر تطبيق خصائص CSS المنطقية وفصل القواميس اللغوية.',
        bulletsEn: [
          'Replace physical margins/paddings (ml-*, mr-*, pl-*, pr-*) with logical equivalents (ms-*, me-*, ps-*, pe-*).',
          'Replace physical positioning and alignment (left-*, right-*, text-left, text-right, border-l-*) with start-*, end-*, text-start, text-end, border-s-*.',
          'Zero Language Leakage: When Arabic (dir="rtl" lang="ar") is active, all UI headings, buttons, badges, and explanations must render in Arabic.'
        ],
        bulletsAr: [
          'استبدل الهوامش والحشوات الفيزيائية (ml-* وmr-* وpl-* وpr-*) بالخصائص المنطقية (ms-* وme-* وps-* وpe-*).',
          'استبدل التموضع والمحاذاة الفيزيائية (left-* وright-* وtext-left وborder-l-*) بـ start-* وend-* وtext-start وborder-s-*.',
          'منع تسرب اللغات: عند تفعيل العربية (dir="rtl" lang="ar")، يجب أن تظهر جميع العناوين والأزرار والشارات والشروحات باللغة العربية.'
        ],
        beforeEn: '<div class="border-l-4 pl-4 text-left ml-2"> — Looks fine in English, but in Arabic the border stays on the left and collides with right-aligned text.', // rtl-guard-ignore: intentional bad example
        beforeAr: '<div class="border-l-4 pl-4 text-left ml-2"> — يبدو جيداً بالإنجليزية، لكن بالعربية يبقى الإطار يساراً ويتصادم مع النص المحاذى لليمين.', // rtl-guard-ignore: intentional bad example
        afterEn: '<div class="border-s-4 ps-4 text-start ms-2"> — Automatically places the accent border on the left in English and on the right in Arabic.',
        afterAr: '<div class="border-s-4 ps-4 text-start ms-2"> — يضع الإطار الجانبي تلقائياً على اليسار في الإنجليزية وعلى اليمين في العربية.',
        exampleTitleEn: 'Example: Scanning a File With `rtl-logical-guard`',
        exampleTitleAr: 'مثال: فحص ملف للتأكد من خلوه من الكلاسات الفيزيائية',
        command: '/rtl-logical-guard',
        promptEn: 'python D:\\Skills\\.agents\\scripts\\agent_os.py scan D:\\Skills\\.agents\\learning-platform\\src\\pages\\index.astro',
        promptAr: 'python D:\\Skills\\.agents\\scripts\\agent_os.py scan D:\\Skills\\.agents\\learning-platform\\src\\pages\\index.astro',
        chainedSkills: ['/rtl-logical-guard', '/ui-audit', '/clean-code-guard'],
        simQuestionsEn: [
          'RTL Scan Result: 0 physical directional classes detected across all .astro and .html templates.',
          'Bilingual Check: Verified complete EN (LTR) and AR (RTL) dictionary parity.'
        ],
        simQuestionsAr: [
          'نتيجة فحص الاتجاه: 0 كلاسات اتجاه فيزيائية في جميع قوالب .astro و.html.',
          'فحص ازدواجية اللغة: تم التأكد من تطابق القاموسين العربي والإنجليزي بالكامل.'
        ],
        quiz: {
          questionEn: 'What is the logical Tailwind CSS replacement for `border-l-4 pl-4 text-left`?',
          questionAr: 'ما هو البديل المنطقي الصحيح في Tailwind CSS للكلاسات الفيزيائية `border-l-4 pl-4 text-left`؟',
          optionsEn: [
            'border-s-4 ps-4 text-start',
            'border-r-4 pr-4 text-right',
            'border-t-4 pt-4 text-center'
          ],
          optionsAr: [
            'border-s-4 ps-4 text-start',
            'border-r-4 pr-4 text-right',
            'border-t-4 pt-4 text-center'
          ],
          correctIndex: 0,
          explanationEn: 'Spot on! border-s-4 (inline-start border), ps-4 (inline-start padding), and text-start adapt automatically to both LTR and RTL.',
          explanationAr: 'أحسنت! تتكيف border-s-4 وps-4 وtext-start تلقائياً مع الاتجاهين العربي والإنجليزي.'
        }
      },
      {
        id: 'ch-speckit',
        trackId: 'track-cms',
        feedCategory: 'features',
        badgeEn: 'Lesson 3.4',
        badgeAr: 'درس 3.4',
        xp: 30,
        readTimeEn: '4 min read',
        readTimeAr: 'قراءة 4 دقائق',
        authorEn: 'Spec-Kit & Pre-Code Lead',
        authorAr: 'قائد التطوير الموجه بالمواصفات',
        roleEn: '6-Pillar & SDD Architect',
        roleAr: 'مهندس الوثائق الست وSpec-Kit',
        titleEn: 'The 6 Pre-Coding Pillars (`/web-precode`) & Spec-Kit SDD (`/spec-kit`)',
        titleAr: 'الركائز الست ما قبل البرمجة (`/web-precode`) ونظام المواصفات (`/spec-kit`)',
        summaryEn: 'For complex features or full platforms, use /web-precode and /spec-kit to turn requirements into dependency-ordered, verifiable tasks.',
        summaryAr: 'للميزات المعقدة أو المنصات الكبيرة، استخدم /web-precode و/spec-kit لتحويل المتطلبات إلى مهام مرتبة وقابلة للتحقق.',
        bulletsEn: [
          'Hard-Stop Gate Discipline: Spec-Kit phases (/speckit-specify -> /speckit-clarify -> /speckit-plan -> /speckit-tasks -> /speckit-analyze -> /speckit-implement) never auto-chain without your explicit command.',
          'precode_engine.py audits docs/specs/ to ensure zero placeholders ("TBD", "TODO") and complete 5-State UI Matrices (Loading, Empty, Error, Success, Populated).',
          '/speckit-converge compares your live codebase against tasks.md to identify any remaining unbuilt work.'
        ],
        bulletsAr: [
          'انضباط بوابات التوقف: مراحل Spec-Kit لا تنتقل تلقائياً من مرحلة لأخرى دون أمر صريح منك.',
          'يتحقق محرك الفحص المسبق من خلو وثائق المواصفات من أي عبارات غير مكتملة ومن وجود مصفوفة حالات الواجهة الخمس.',
          'يقارن أمر /speckit-converge الكود الفعلي بملف المهام لاكتشاف أي جزء متبقٍ لم يكتمل بناؤه.'
        ],
        beforeEn: 'Jumping straight into a 20-file refactor without a task list — losing track of edge cases halfway through.',
        beforeAr: 'القفز مباشرة لتعديل 20 ملفاً بدون قائمة مهام مرتبة — مما يؤدي لنسيان الحالات الحدية في منتصف الطريق.',
        afterEn: 'Locking the spec and dependency-ordered tasks.md first, then executing step-by-step with mathematical reconciliation.',
        afterAr: 'اعتماد المواصفات وقائمة المهام المرتبة أولاً، ثم التنفيذ خطوة بخطوة مع مطابقة حسابية دقيقة للملفات والاختبارات.',
        exampleTitleEn: 'Example: Initializing & Auditing the 6 Pre-Coding Pillars',
        exampleTitleAr: 'مثال: تهيئة وفحص الوثائق الهندسية الست قبل البناء',
        command: '/web-precode',
        promptEn: 'python D:\\Skills\\.agents\\scripts\\agent_os.py precode status',
        promptAr: 'python D:\\Skills\\.agents\\scripts\\agent_os.py precode status',
        chainedSkills: ['/web-precode', '/spec-kit', '/speckit-specify', '/speckit-plan', '/speckit-tasks'],
        simQuestionsEn: [
          'Pillar Audit: Checking 01-PRD, 02-TRD, 03-App-Flow, 04-Design-Brief, 05-Backend-Schema, 06-Implementation-Plan.',
          'Gate Rule: Waiting for explicit phase command before moving from /speckit-plan to /speckit-tasks.'
        ],
        simQuestionsAr: [
          'فحص الركائز: التحقق من وجود وثائق المتطلبات والتصميم وتدفق الشاشات وقاعدة البيانات وخطة التنفيذ.',
          'قاعدة البوابة: انتظار الأمر الصريح قبل الانتقال من مرحلة التخطيط إلى توليد المهام.'
        ],
        quiz: {
          questionEn: 'Do Spec-Kit phases (/speckit-specify, /speckit-plan, /speckit-implement) auto-chain on their own without asking you?',
          questionAr: 'هل تنتقل مراحل Spec-Kit تلقائياً من المواصفات إلى التخطيط ثم التنفيذ دون انتظار أمرك؟',
          optionsEn: [
            'No — each Spec-Kit phase has a hard-stop gate and requires your explicit invocation or approval',
            'Yes — it runs everything blindly in one giant step',
            'Spec-Kit is only for Python scripts'
          ],
          optionsAr: [
            'لا — كل مرحلة لها بوابة توقف وتتطلب استدعاءً أو موافقة صريحة منك',
            'نعم — تشغل كل شيء دفعة واحدة دون توقف',
            'نظام Spec-Kit مخصص لسكربتات بايثون فقط'
          ],
          correctIndex: 0,
          explanationEn: 'Correct! Hard-stop gates ensure you review and approve the spec and plan before implementation begins.',
          explanationAr: 'صحيح! تضمن بوابات التوقف مراجعتك وموافقتك على المواصفات والخطة قبل بدء التنفيذ.'
        }
      }
    ]
  },
  {
    id: 'track-ref',
    titleEn: 'Track 4: 60-Skill & CLI Reference',
    titleAr: 'المسار 4: قاموس الـ 60 مهارة وأدوات CLI',
    lessons: [
      {
        id: 'ch-cli-manual',
        trackId: 'track-ref',
        feedCategory: 'ops',
        badgeEn: 'Lesson 4.1',
        badgeAr: 'درس 4.1',
        xp: 25,
        readTimeEn: '3 min read',
        readTimeAr: 'قراءة 3 دقائق',
        authorEn: 'Agent OS CLI Router',
        authorAr: 'موجه أوامر النظام',
        roleEn: '24-Tool Unified CLI',
        roleAr: 'واجهة سطر الأوامر الموحدة',
        titleEn: '`agent_os.py`: The Unified CLI Manual & `handbook-sync` Workflow',
        titleAr: 'دليل أداة `agent_os.py` الموحدة ومزامنة منصة التعلم `handbook-sync`',
        summaryEn: 'Run every audit, router, UI scanner, test suite, and handbook sync from any project directory using python D:\\Skills\\.agents\\scripts\\agent_os.py.',
        summaryAr: 'شغل جميع أدوات الفحص والتوجيه ومسح الواجهة والاختبارات ومزامنة الدليل من أي مشروع عبر أداة agent_os.py الموحدة.',
        bulletsEn: [
          'handbook-sync [--build]: Reads SKILL_INDEX.json, updates learning-platform/src/data/skills-registry.json, runs astro build, and copies dist/index.html to root handbook.html.',
          'ui-audit scan --dir <path>: Runs the 8-dimension static frontend audit across .astro, .tsx, .vue, .blade.php, and .html.',
          'scan <file> & test: Runs security/RTL guard checks on any file and executes the full unit test suite.'
        ],
        bulletsAr: [
          'الأمر handbook-sync [--build]: يقرأ فهرس المهارات، ويحدث سجل منصة التعلم، ويبني مشروع Astro، وينسخ النتيجة إلى handbook.html الرئيسي.',
          'الأمر ui-audit scan --dir <path>: يشغل الفحص الثابت للواجهة من 8 أبعاد عبر ملفات .astro و.tsx و.vue و.blade.php و.html.',
          'الأمران scan <file> وtest: يشغلان حراس الأمان واتجاه العربية على أي ملف وينفذان حزمة الاختبارات الكاملة.'
        ],
        beforeEn: 'Manually editing HTML tables every time you add a new skill to D:\\Skills\\.agents\\skills\\ and sending updated files around.',
        beforeAr: 'تعديل جداول HTML يدوياً في كل مرة تضيف فيها مهارة جديدة وإرسال الملفات المحدثة للفريق يدوياً.',
        afterEn: 'Running python scripts/agent_os.py index-skills && python scripts/agent_os.py handbook-sync --build to update the entire learning platform in seconds.',
        afterAr: 'تشغيل أمر الفهرسة ثم handbook-sync --build لتحديث منصة التعلم بالكامل وملف الدليل في ثوانٍ.',
        exampleTitleEn: 'Example: Updating & Building the Learning Platform After Adding a Skill',
        exampleTitleAr: 'مثال: تحديث وبناء منصة التعلم بعد إضافة مهارة جديدة',
        command: 'handbook-sync',
        promptEn: 'python D:\\Skills\\.agents\\scripts\\agent_os.py handbook-sync --build',
        promptAr: 'python D:\\Skills\\.agents\\scripts\\agent_os.py handbook-sync --build',
        chainedSkills: ['/plan-daily', '/doc-project', '/docs-guard', '/ui-audit'],
        simQuestionsEn: [
          'Step 1: Synced 60 core skills & 18 MCP servers -> learning-platform/src/data/skills-registry.json',
          'Step 2: Built Astro static bundle and synced dist/index.html -> root handbook.html'
        ],
        simQuestionsAr: [
          'الخطوة 1: تمت مزامنة 60 مهارة أساسية و18 خادم MCP إلى ملف skills-registry.json',
          'الخطوة 2: تم بناء حزمة Astro الثابتة ومزامنتها مع ملف handbook.html الرئيسي'
        ],
        quiz: {
          questionEn: 'Which command updates `skills-registry.json`, builds the Astro learning platform, and syncs root `handbook.html` automatically?',
          questionAr: 'ما هو الأمر الذي يحدث سجل المهارات ويبني منصة التعلم بـ Astro ويحدث ملف handbook.html الرئيسي تلقائياً؟',
          optionsEn: [
            'python scripts/agent_os.py handbook-sync --build',
            'git push --force',
            'npm uninstall astro'
          ],
          optionsAr: [
            'python scripts/agent_os.py handbook-sync --build',
            'git push --force',
            'npm uninstall astro'
          ],
          correctIndex: 0,
          explanationEn: 'Correct! handbook-sync --build keeps your Astro platform and standalone handbook.html 100% synchronized.',
          explanationAr: 'صحيح! يحافظ أمر handbook-sync --build على تزامن منصة Astro وملف الدليل المستقل بنسبة 100%.'
        }
      },
      {
        id: 'ch-dictionary',
        trackId: 'track-ref',
        feedCategory: 'ops',
        badgeEn: 'Lesson 4.2',
        badgeAr: 'درس 4.2',
        xp: 25,
        readTimeEn: 'Reference',
        readTimeAr: 'مرجع شامل',
        authorEn: 'Skill Indexer',
        authorAr: 'مفهرس المهارات',
        roleEn: '60-Skill & 18-MCP Catalog',
        roleAr: 'سجل الـ 60 مهارة و18 خادم MCP',
        titleEn: 'Complete 60-Skill & 18-MCP Reference Dictionary (Interactive Table)',
        titleAr: 'القاموس المرجعي الكامل للـ 60 مهارة و18 خادم MCP (جدول تفاعلي)',
        summaryEn: 'Search, filter by category or THINK/PLAN/BUILD/VERIFY phase, inspect full descriptions in the Details Modal, or launch any skill in the Simulator.',
        summaryAr: 'ابحث وصفِّ حسب الفئة أو المرحلة (تفكير/تخطيط/بناء/فحص)، واعرض الوصف الكامل في نافذة التفاصيل، أو جرب أي مهارة في المحاكي.',
        bulletsEn: [
          'Every table row below is auto-synced from SKILL_INDEX.json via scripts/sync_handbook.py.',
          'Long descriptions are truncated to the first 3 words + "..." so the table remains clean on 375px mobile screens.',
          'Click "Details" on any row to view the full bilingual description, file path, and one-click "Try it Yourself" launcher.'
        ],
        bulletsAr: [
          'جميع صفوف الجدول أدناه متزامنة تلقائياً من ملف SKILL_INDEX.json عبر أداة المزامنة.',
          'تم اختصار الأوصاف الطويلة إلى أول 3 كلمات + "..." للحفاظ على نظافة الجدول على شاشات الجوال مقاس 375px.',
          'اضغط على زر "التفاصيل" في أي صف لعرض الشرح الكامل ومسار الملف وزر التجربة الفورية في المحاكي.'
        ],
        beforeEn: 'Scrolling through dozens of folders in D:\\Skills\\.agents\\skills\\ to remember what a specific guard or Spec-Kit skill does.',
        beforeAr: 'التنقل يدوياً بين عشرات المجلدات لمعرفة وظيفة حارس معين أو مهارة فرعية.',
        afterEn: 'Filtering the live 60-skill reference table below by category or keyword and launching it with one click.',
        afterAr: 'تصفية جدول المهارات الـ 60 الحي أدناه حسب الفئة أو الكلمة المفتاحية وتشغيلها بضغطة واحدة.',
        exampleTitleEn: 'Example: Finding Skills via CLI Search',
        exampleTitleAr: 'مثال: البحث عن المهارات عبر سطر الأوامر',
        command: '/check-all',
        promptEn: 'python D:\\Skills\\.agents\\scripts\\agent_os.py skill-find "woocommerce hpos security"',
        promptAr: 'python D:\\Skills\\.agents\\scripts\\agent_os.py skill-find "woocommerce hpos security"',
        chainedSkills: ['/woo-guard', '/wp-guard', '/feature-wp'],
        simQuestionsEn: [
          'Top Match 1: /woo-guard (VERIFY) — Enforces HPOS-safe wc_get_order CRUD and checkout validation.',
          'Top Match 2: /feature-wp (BUILD) — All-in-one WordPress & WooCommerce feature builder.'
        ],
        simQuestionsAr: [
          'النتيجة 1: /woo-guard (فحص) — يفرض دوال الطلبات المتوافقة مع HPOS والتحقق من الدفع.',
          'النتيجة 2: /feature-wp (بناء) — باني ميزات ووردبريس وووكرومرس الشامل.'
        ],
        quiz: {
          questionEn: 'How many core skills are indexed in the Agent OS v1.15.0 catalog?',
          questionAr: 'كم عدد المهارات الأساسية المفهرسة في دليل النظام للإصدار v1.15.0؟',
          optionsEn: [
            '60 core skills (plus 26 plugin skills and 18 MCP servers)',
            'Only 5 skills',
            '1,000 unorganized scripts'
          ],
          optionsAr: [
            '60 مهارة أساسية (بالإضافة إلى 26 مهارة إضافات و18 خادم MCP)',
            '5 مهارات فقط',
            '1000 سكربت غير منظم'
          ],
          correctIndex: 0,
          explanationEn: 'Correct! All 60 core skills, 26 plugin skills, and 18 MCP servers are indexed in SKILL_INDEX.json.',
          explanationAr: 'صحيح! جميع المهارات الـ 60 الأساسية و26 مهارة إضافية و18 خادم MCP مفهرسة في SKILL_INDEX.json.'
        }
      }
    ]
  }
];

export const SITUATION_COMBOS_CARDS = [
  {
    command: '/start-project',
    phase: 'PLAN + BUILD',
    badgeEn: 'New App From Zero',
    badgeAr: 'مشروع جديد من الصفر',
    titleEn: 'Start Brand-New Project',
    titleAr: 'بدء مشروع جديد متكامل',
    shortEn: 'Runs Q1-Q28 intake...',
    shortAr: 'يجري مقابلة المتطلبات...',
    descEn: 'Runs Smart Intake Q1-Q28 in short rounds, authors the 6 Pre-Coding docs, locks design tokens, and builds Frontend, Backend, and Database.',
    descAr: 'يجري مقابلة المتطلبات الذكية في جولات قصيرة، ويكتب الوثائق الهندسية الست، ويعتمد رموز التصميم، ويبني الواجهة والخلفية وقاعدة البيانات.',
    samplePromptEn: '/start-project Build a bilingual (AR/EN) B2B wholesale ordering portal with Admin and Buyer roles.',
    samplePromptAr: '/start-project ابن بوابة طلبات جملة ثنائية اللغة (عربي/إنجليزي) بصلاحيات مدير ومشتري.',
    lessonId: 'ch-start-project'
  },
  {
    command: '/plan-daily',
    phase: 'THINK + PLAN',
    badgeEn: 'Morning Triage',
    badgeAr: 'تخطيط عمل اليوم',
    titleEn: 'Daily Triage & Skill Factory',
    titleAr: 'مخطط اليوم ومصنع المهارات',
    shortEn: 'Picks 1 primary focus...',
    shortAr: 'يحدد أولوية واحدة لليوم...',
    descEn: 'Scans git status, PROGRESS.md, DECISIONS.md, and test health to pick ONE primary focus for today, or scaffolds a new Agent OS skill.',
    descAr: 'يفحص حالة المشروع وسجل التقدم والقرارات والاختبارات ليقترح مهمة أساسية واحدة لليوم، أو يبني مهارة جديدة للنظام.',
    samplePromptEn: '/plan-daily Inspect current project status and propose today\'s primary task.',
    samplePromptAr: '/plan-daily افحص حالة المشروع الحالية واقترح المهمة الأساسية لليوم.',
    lessonId: 'ch-daily'
  },
  {
    command: '/smart-feature',
    phase: 'AUTO-ROUTE',
    badgeEn: 'Auto Skill Router',
    badgeAr: 'الموجه الذكي للميزات',
    titleEn: 'Smart Plain-Language Feature',
    titleAr: 'بناء ميزة بالوصف المباشر',
    shortEn: 'Auto-selects best skills...',
    shortAr: 'يختار المهارات تلقائياً...',
    descEn: 'Reads your plain-language feature description and repo files, automatically selects UI, API, DB, and Security skills, interviews you, and builds it.',
    descAr: 'يقرأ وصف الميزة وملفات المشروع، ويختار تلقائياً مهارات الواجهة والخلفية وقاعدة البيانات والأمان، ثم يبنيها ويفحصها.',
    samplePromptEn: '/smart-feature Add a customer support ticket drawer with priority tags and agent assignment.',
    samplePromptAr: '/smart-feature أضف نافذة تذاكر دعم فني مع تصنيف الأولوية وتعيين الموظف المسؤول.',
    lessonId: 'ch-smart-feature'
  },
  {
    command: '/feature-full',
    phase: 'BUILD + VERIFY',
    badgeEn: 'UI + API + DB',
    badgeAr: 'واجهة + خلفية + بيانات',
    titleEn: 'Complete Full-Stack Feature',
    titleAr: 'ميزة متكاملة مع قاعدة البيانات',
    shortEn: 'Builds UI, API, and DB...',
    shortAr: 'يبني الواجهة والخلفية والبيانات...',
    descEn: 'Chains CMS Frontend + Backend API/RBAC + Database migrations, foreign keys, compound indexes, N+1 prevention, and ACID transactions.',
    descAr: 'يدمج بناء الواجهة الأمامية مع الواجهة الخلفية والصلاحيات وتعديلات قاعدة البيانات والمفاتيح الخارجية والفهارس والمعاملات الآمنة.',
    samplePromptEn: '/feature-full Add an inventory stock transfer module between warehouses with audit log table.',
    samplePromptAr: '/feature-full أضف وحدة نقل مخزون بين المستودعات مع جدول سجل تدقيق متجاوب.',
    lessonId: 'ch-feature-full'
  },
  {
    command: '/feature-febe',
    phase: 'BUILD + VERIFY',
    badgeEn: 'UI + Backend API',
    badgeAr: 'واجهة + خلفية API',
    titleEn: 'Frontend + Backend Feature',
    titleAr: 'ميزة واجهة أمامية وخلفية',
    shortEn: 'Connects UI to secure API...',
    shortAr: 'يربط الواجهة بنقاط API آمنة...',
    descEn: 'Builds responsive CMS UI + Backend endpoints, server-side auth derivation, anti-IDOR ownership checks, and form validation without new DB tables.',
    descAr: 'يبني واجهة متجاوبة مع نقاط النهاية الخلفية وفحص الجلسة بالخادم وحماية ملكية السجلات والتحقق من النماذج بدون جداول جديدة.',
    samplePromptEn: '/feature-febe Add a bulk status update action bar and API endpoint for selected orders.',
    samplePromptAr: '/feature-febe أضف شريط تحديث جماعي لحالة الطلبات المحددة مع نقطة نهاية API محمية.',
    lessonId: 'ch-feature-full'
  },
  {
    command: '/feature-fe',
    phase: 'BUILD + VERIFY',
    badgeEn: 'Frontend & CMS UI',
    badgeAr: 'واجهة أمامية ولوحة تحكم',
    titleEn: 'Frontend & CMS UI Builder',
    titleAr: 'باني الواجهات ولوحات التحكم',
    shortEn: 'Sticky shell & mobile UI...',
    shortAr: 'تخطيط ثابت وواجهة متجاوبة...',
    descEn: 'Stack-agnostic UI builder (Astro, React, Next.js, Vue, Blade, HTML/Tailwind). Enforces sticky navbars, truncated tables, 3-card grids, and RTL.',
    descAr: 'يبني واجهات متجاوبة لأي تقنية مع التزام صارم بالأشرطة الثابتة واختصار الجداول وشبكة الـ 3 بطاقات ودعم العربية.',
    samplePromptEn: '/feature-fe Build a responsive pricing & subscription comparison section with FAQ accordion.',
    samplePromptAr: '/feature-fe ابن قسم مقارنة باقات متجاوب مع قائمة أسئلة شائعة قابلة للطي.',
    lessonId: 'ch-feature-fe-wp'
  },
  {
    command: '/feature-wp',
    phase: 'BUILD + VERIFY',
    badgeEn: 'WordPress & Woo',
    badgeAr: 'ووردبريس وووكرومرس',
    titleEn: 'WordPress & WooCommerce HPOS',
    titleAr: 'ميزات ووردبريس وووكرومرس',
    shortEn: 'HPOS CRUD & nonce guards...',
    shortAr: 'توافق HPOS وحماية Nonce...',
    descEn: 'Chains /wp-guard + /woo-guard + /rtl-logical-guard to build HPOS-compatible plugins, checkout hooks, and admin pages with strict escaping.',
    descAr: 'يدمج حراس ووردبريس وووكرومرس والاتجاه المنطقي لبناء إضافات وقوالب متوافقة مع HPOS ومحمية بالكامل.',
    samplePromptEn: '/feature-wp Add a custom delivery time-slot selector on WooCommerce checkout saved via HPOS CRUD.',
    samplePromptAr: '/feature-wp أضف حقل اختيار وقت التوصيل في صفحة دفع ووكرومرس محفوظاً عبر دوال HPOS القياسية.',
    lessonId: 'ch-feature-fe-wp'
  },
  {
    command: '/fix-ui',
    phase: 'VERIFY + FIX',
    badgeEn: 'UI Auto-Fixer',
    badgeAr: 'مصلح الواجهة التلقائي',
    titleEn: 'Scan & Fix Broken UI / RTL',
    titleAr: 'فحص وإصلاح مشاكل الواجهة والعربية',
    shortEn: 'Fixes tables, navs, RTL...',
    shortAr: 'يصلح الجداول والتنقل والعربية...',
    descEn: 'Scans with /ui-audit, fixes broken sticky navbars, overflowing mobile tables, overlapping input icons, and RTL physical class bugs.',
    descAr: 'يفحص الواجهة بأداة التدقيق، ويصلح الأشرطة غير الثابتة والجداول الخارجة عن شاشة الجوال وتداخل الأيقونات وأخطاء اتجاه العربية.',
    samplePromptEn: '/fix-ui Scan my frontend and fix mobile horizontal overflow and broken RTL alignment.',
    samplePromptAr: '/fix-ui افحص الواجهة الأمامية وأصلح التمرير الأفقي على الجوال ومشاكل محاذاة العربية.',
    lessonId: 'ch-fixers'
  },
  {
    command: '/fix-backend',
    phase: 'VERIFY + FIX',
    badgeEn: 'API & DB Fixer',
    badgeAr: 'مصلح الخلفية والبيانات',
    titleEn: 'Fix API, Auth & DB Bugs',
    titleAr: 'إصلاح أعطال الخلفية والصلاحيات',
    shortEn: 'Fixes 500s, auth, N+1...',
    shortAr: 'يصلح أخطاء 500 والصلاحيات...',
    descEn: 'Diagnoses and repairs server errors, IDOR auth gaps, broken file uploads, N+1 queries, and race conditions across Node, PHP, Python, and Go.',
    descAr: 'يشخص ويصلح أخطاء الخادم وثغرات الصلاحيات ومشاكل رفع الملفات واستعلامات N+1 البطيئة وتضارب العمليات المتزامنة.',
    samplePromptEn: '/fix-backend Fix the duplicate order creation race condition when a user double-clicks checkout.',
    samplePromptAr: '/fix-backend أصلح مشكلة تكرار إنشاء الطلب عند ضغط المستخدم مرتين بسرعة على زر الدفع.',
    lessonId: 'ch-fixers'
  },
  {
    command: '/check-all',
    phase: 'VERIFY',
    badgeEn: '7-Guard Audit',
    badgeAr: 'الفحص الشامل بـ 7 حراس',
    titleEn: 'Pre-Push Quality & Security Gate',
    titleAr: 'بوابة الفحص الشامل قبل الرفع',
    shortEn: 'Runs 7 guards at once...',
    shortAr: 'يشغل 7 حراس في خطوة واحدة...',
    descEn: 'Chains /clean-code-guard, /test-guard, /rtl-logical-guard, server security guards, /ponytail-review, and /debate-review before git push.',
    descAr: 'يشغل حراس الكود النظيف والاختبارات والعربية وأمان الخادم ومنع التعقيد والمراجعة المزدوجة في أمر واحد قبل الرفع.',
    samplePromptEn: '/check-all Review all modified files in my working tree before we merge.',
    samplePromptAr: '/check-all راجع جميع الملفات المعدلة في المشروع قبل الدمج.',
    lessonId: 'ch-ops-combos'
  },
  {
    command: '/save-data',
    phase: 'OPS',
    badgeEn: '-85% Data Saver',
    badgeAr: 'توفير 85% من الإنترنت',
    titleEn: 'Low-Bandwidth & Token Saver',
    titleAr: 'وضع توفير باقة الإنترنت والتوكنز',
    shortEn: 'Cuts mobile data by 85%...',
    shortAr: 'يقلل استهلاك البيانات 85%...',
    descEn: 'Disables silent background downloads, git autofetch, and ghost-text completions, activates offline package caches, and enables /caveman lite.',
    descAr: 'يوقف التحديثات الصامتة والجلب التلقائي لـ Git والإكمال المستمر، ويفعل التخزين المحلي للحزم والردود المختصرة.',
    samplePromptEn: '/save-data Activate low-bandwidth mode for my mobile hotspot session.',
    samplePromptAr: '/save-data فعل وضع توفير البيانات لجلسة العمل عبر نقطة اتصال الجوال.',
    lessonId: 'ch-ops-combos'
  },
  {
    command: '/doc-project',
    phase: 'VERIFY + DOCS',
    badgeEn: 'Verified Auto-Docs',
    badgeAr: 'توثيق المشروع الموثق',
    titleEn: 'Generate & Audit Project Docs',
    titleAr: 'توليد وتدقيق وثائق المشروع',
    shortEn: 'Generates README & API docs...',
    shortAr: 'يولد README وتوثيق الـ API...',
    descEn: 'Scans real codebase structure and routes to generate or update README.md, docs/ARCHITECTURE.md, and docs/API.md, verified by /docs-guard.',
    descAr: 'يمسح هيكل الكود والمسارات الفعلي لتوليد أو تحديث ملفات README والهندسة المعمارية وتوثيق الـ API مع فحصها بحارس التوثيق.',
    samplePromptEn: '/doc-project Update README.md and docs/API.md to reflect our new endpoints.',
    samplePromptAr: '/doc-project حدث ملفي README.md وdocs/API.md ليعكسا نقاط النهاية الجديدة.',
    lessonId: 'ch-ops-combos'
  }
];

export const UI_DICTIONARY = {
  en: {
    brandTitle: 'AgentOS',
    brandSub: 'W3Schools x Social Learning Hub',
    versionBadge: 'v2.1.0 Astro Edition',
    searchPlaceholder: 'Search 85 skills, 28 CLI tools, /commands, or lessons...',
    modeSocial: 'Social Feed',
    modeReader: 'W3Schools Reader',
    modeSimulator: 'Try it Yourself »',
    modeReference: '85-Skill & CLI Dict',
    langToggleLabel: 'العربية (RTL)',
    themeToggleLabel: 'Theme',
    heroEyebrow: 'INTERACTIVE TEAM ONBOARDING & LIVE REFERENCE',
    heroTitle: 'Learn Agent OS the W3Schools Way — Zero Boredom, 100% Interactive',
    heroSubtitle: 'Watch 60-second Story Reels, scroll the Social Learning Feed, tweak live slash commands in the Split-Pane Simulator, and copy ready pre-written commands for all 85 skills & 28 CLI tools.',
    heroCtaPrimary: 'Start Lesson 1.1 »',
    heroCtaSecondary: 'Open Live Simulator »',
    statsSkills: '85 Core Skills',
    statsCombos: '11 Situation Combos',
    statsMcps: '19 MCP Servers',
    statsGuards: '28 CLI Engines',
    storiesHeading: '60-Second Story Reels (Tap Any Ring to Play)',
    feedFilterAll: 'All Posts',
    feedFilterStart: 'Start Here',
    feedFilterFeatures: 'Build Features',
    feedFilterBugs: 'Fix Bugs',
    feedFilterCms: 'CMS & Mobile',
    feedFilterOps: 'Bandwidth & CLI',
    combosSectionTitle: 'The 11 Situation Combos (One Command Does It All)',
    combosSectionSub: 'Mobile-first 3-card grid. Click "Try it Yourself »" on any card to load it in the live simulator.',
    showMoreCombos: 'Show All 12 Combo Cards »',
    collapseCombos: 'Collapse to Top 3 Cards «',
    beforeLabel: 'Without Agent OS (Raw AI)',
    afterLabel: 'With Agent OS (Guarded Pipeline)',
    exampleBoxHeader: 'W3Schools Live Command Example',
    tryItBtn: 'Try it Yourself »',
    readFullLessonBtn: 'Open Full W3Schools Lesson »',
    markCompleteBtn: 'Mark Lesson Completed (+25 XP)',
    completedBadge: 'Completed',
    helpfulBtn: 'Helpful',
    saveToolkitBtn: 'Save to Toolkit',
    savedBadge: 'Saved',
    quizHeader: 'Test Yourself With Exercises (+25 XP)',
    quizSubmitBtn: 'Check Answer »',
    prevLessonBtn: '« Previous',
    nextLessonBtn: 'Next »',
    simHeaderTitle: 'W3Schools Split-Pane "Try it Yourself »" Studio',
    simHeaderSub: 'Select any of the 12 Situation Combos OR any of the 85 Targeted Skills on the start pane, customize your pre-written prompt, and click Run » to inspect the live Agent OS execution pipeline.',
    simSelectCombo: '1. Choose Slash Command or Targeted Skill (85 Skills)',
    simSelectStack: '2. Choose Tech Stack (Includes Astro)',
    simEditPrompt: '3. Edit Your Ready Copy-Paste Prompt',
    simRunBtn: 'Run Command »',
    simCopyPromptBtn: 'Copy Ready Prompt',
    simOutputHeader: 'Simulated Agent OS Execution Pipeline',
    simStage1Title: 'Stage 1 (RED LIGHT): Smart Intake & Domain Target',
    simStage2Title: 'Stage 2 (YELLOW LIGHT): Auto-Chained Skills & Guards',
    simStage3Title: 'Stage 3 (GREEN LIGHT): Target Files & Verification Gate',
    refHeaderTitle: 'Searchable 85-Skill, 28-CLI & 19-MCP Reference Dictionary',
    refHeaderSub: 'Every skill & tool includes its User Request Domain, what it enforces, and a Ready Copy-Paste Command. Click Copy Prompt, Try », or Details.',
    refSearchPlaceholder: 'Filter by user request domain, skill name, /command, category, or phase (THINK, PLAN, BUILD, VERIFY)...',
    refColCommand: 'Targeted Skill / Tool',
    refColDomain: 'User Request Domain',
    refColCategory: 'Category',
    refColPhase: 'Phase',
    refColSummary: 'Summary (2-4 Words)',
    refColAction: 'Ready Command & Details',
    refDetailsBtn: 'Details & Prompt',
    copyPromptShortBtn: 'Copy Prompt',
    refShowMoreRows: 'Show All 85 Skills »',
    refCollapseRows: 'Show First 12 Skills «',
    cliTableTitle: '28 Unified Agent OS CLI Tools (`python scripts/agent_os.py <cmd>`)',
    cliTableSub: 'Deterministic terminal sensors, AST navigators, UI/security auditors, and sync engines with pre-written copy-paste commands.',
    rightRailProgressTitle: 'My Learning Progress & XP Rank',
    rightRailXpLabel: 'Total XP Earned',
    rightRailCompletedLabel: 'Lessons Completed',
    rightRailToolkitTitle: 'My Saved Command Toolkit',
    rightRailToolkitEmpty: 'Click "Save to Toolkit" on any lesson or skill to pin your favorite commands here.',
    rightRailUpdateBoxTitle: 'Team Maintainer Sync Command',
    rightRailUpdateBoxDesc: 'Updated a skill in D:\\Skills\\.agents\\skills? Run this single command to rebuild and sync:',
    modalCloseBtn: 'Close',
    modalDomainLabel: 'User Request Domain (When to Use):',
    modalPromptLabel: 'Ready Copy-Paste Command (Click Copy or Load in Simulator):',
    modalTryInSimBtn: 'Load in "Try it Yourself »" Simulator',
    modalCopyCmdBtn: 'Copy Ready Command',
    rank0: 'New Intern (Level 1)',
    rank1: 'Junior Builder (Level 2)',
    rank2: 'Full-Stack Operator (Level 3)',
    rank3: 'Agent OS Architect (Max Rank)',
    toastCopied: 'Copied ready command to clipboard!',
    toastSaved: 'Updated your Saved Toolkit!',
    toastLessonDone: 'Lesson marked complete! +25 XP awarded.',
    toastQuizRight: 'Correct answer! +25 XP awarded.',
    toastQuizWrong: 'Not quite — review the explanation and try again.',
    mobileNavFeed: 'Feed',
    mobileNavLessons: 'Chapters',
    mobileNavTryIt: 'Try It',
    mobileNavRef: '85 Skills',
    mobileNavProfile: 'My XP'
  },
  ar: {
    brandTitle: 'نظام الوكيل',
    brandSub: 'منصة تعلم تفاعلية بأسلوب W3Schools',
    versionBadge: 'إصدار v2.1.0 يدعم Astro',
    searchPlaceholder: 'ابحث في 85 مهارة أو 28 أداة CLI أو الأوامر أو الدروس...',
    modeSocial: 'موجز التعلم التفاعلي',
    modeReader: 'قارئ دروس W3Schools',
    modeSimulator: 'جربها بنفسك »',
    modeReference: 'قاموس 85 مهارة وCLI',
    langToggleLabel: 'English (LTR)',
    themeToggleLabel: 'المظهر',
    heroEyebrow: 'منصة تدريب الفريق والمرجع التفاعلي الحي',
    heroTitle: 'تعلم نظام Agent OS بأسلوب W3Schools — بدون ملل وبتفاعل كامل 100%',
    heroSubtitle: 'شاهد القصص السريعة في 60 ثانية، وتصفح موجز التعلم التفاعلي، وجرب الأوامر الحية في المحاكي المزدوج، وانسخ الأوامر الجاهزة لجميع المهارات الـ 85 و28 أداة CLI.',
    heroCtaPrimary: 'ابدأ الدرس 1.1 »',
    heroCtaSecondary: 'افتح المحاكي الحي »',
    statsSkills: '85 مهارة أساسية',
    statsCombos: '11 أمراً شاملاً',
    statsMcps: '19 خادم MCP',
    statsGuards: '28 أداة CLI',
    storiesHeading: 'قصص سريعة في 60 ثانية (اضغط على أي حلقة للمشاهدة)',
    feedFilterAll: 'جميع المنشورات',
    feedFilterStart: 'ابدأ من هنا',
    feedFilterFeatures: 'بناء الميزات',
    feedFilterBugs: 'إصلاح الأعطال',
    feedFilterCms: 'لوحات التحكم والجوال',
    feedFilterOps: 'توفير البيانات وCLI',
    combosSectionTitle: 'الأوامر الشاملة الـ 11 (أمر واحد ينجز المهمة بالكامل)',
    combosSectionSub: 'شبكة متجاوبة (3 بطاقات في الصف). اضغط "جربها بنفسك »" على أي بطاقة لتشغيلها في المحاكي الحي.',
    showMoreCombos: 'عرض جميع بطاقات الأوامر الـ 12 »',
    collapseCombos: 'طي القائمة إلى أول 3 بطاقات «',
    beforeLabel: 'بدون النظام (ذكاء اصطناعي خام)',
    afterLabel: 'مع النظام (خط عمل محمي بالحراس)',
    exampleBoxHeader: 'مثال أمر حي بأسلوب W3Schools',
    tryItBtn: 'جربها بنفسك »',
    readFullLessonBtn: 'افتح درس W3Schools الكامل »',
    markCompleteBtn: 'تحديد الدرس كمكتمل (+25 نقطة XP)',
    completedBadge: 'مكتمل',
    helpfulBtn: 'مفيد',
    saveToolkitBtn: 'حفظ في حقيبتي',
    savedBadge: 'محفوظ',
    quizHeader: 'اختبر نفسك بالتمرين (+25 نقطة XP)',
    quizSubmitBtn: 'تحقق من الإجابة »',
    prevLessonBtn: '« السابق',
    nextLessonBtn: 'التالي »',
    simHeaderTitle: 'استوديو "جربها بنفسك »" المزدوج بأسلوب W3Schools',
    simHeaderSub: 'اختر أياً من الأوامر الشاملة الـ 12 أو أي مهارة من المهارات التخصصية الـ 85، وعدل الأمر الجاهز، ثم اضغط تشغيل » لمعاينة خط عمل النظام الحي.',
    simSelectCombo: '1. اختر الأمر الشامل أو المهارة المستهدفة (85 مهارة)',
    simSelectStack: '2. اختر التقنية البرمجية (تشمل Astro)',
    simEditPrompt: '3. عدل نص الأمر الجاهز للنسخ',
    simRunBtn: 'تشغيل الأمر »',
    simCopyPromptBtn: 'نسخ الأمر الجاهز',
    simOutputHeader: 'معاينة خط التنفيذ الحي في النظام',
    simStage1Title: 'المرحلة 1 (الإشارة الحمراء): مجال الطلب وأسئلة المتطلبات',
    simStage2Title: 'المرحلة 2 (الإشارة الصفراء): المهارات والحراس المشغلون تلقائياً',
    simStage3Title: 'المرحلة 3 (الإشارة الخضراء): الملفات المستهدفة وبوابة الفحص',
    refHeaderTitle: 'القاموس المرجعي التفاعلي للـ 85 مهارة و28 أداة CLI و19 خادم MCP',
    refHeaderSub: 'تضم كل مهارة وأداة مجال طلب المستخدم، وشرح ما تفرضه، وأمراً جاهزاً للنسخ واللصق الفوري. اضغط نسخ الأمر أو التفاصيل.',
    refSearchPlaceholder: 'ابحث حسب مجال الطلب أو اسم المهارة أو الأمر أو الفئة أو المرحلة (THINK, PLAN, BUILD, VERIFY)...',
    refColCommand: 'المهارة / الأداة',
    refColDomain: 'مجال طلب المستخدم',
    refColCategory: 'الفئة',
    refColPhase: 'المرحلة',
    refColSummary: 'الملخص (2-4 كلمات)',
    refColAction: 'الأمر الجاهز والتفاصيل',
    refDetailsBtn: 'التفاصيل والأمر',
    copyPromptShortBtn: 'نسخ الأمر',
    refShowMoreRows: 'عرض جميع المهارات الـ 85 »',
    refCollapseRows: 'عرض أول 12 مهارة فقط «',
    cliTableTitle: 'مرجع أدوات سطر الأوامر الـ 28 الموحدة (`python scripts/agent_os.py <cmd>`)',
    cliTableSub: 'أدوات الفحص الحتمي وتحليل شجرة الكود AST وتدقيق الواجهة والأمان والمزامنة مع أوامر جاهزة للنسخ.',
    rightRailProgressTitle: 'تقدمي في التعلم ورتبة الخبرة XP',
    rightRailXpLabel: 'إجمالي نقاط الخبرة XP',
    rightRailCompletedLabel: 'الدروس المكتملة',
    rightRailToolkitTitle: 'حقيبة أوامري المحفوظة',
    rightRailToolkitEmpty: 'اضغط "حفظ في حقيبتي" على أي درس أو مهارة لتثبيت أوامرك المفضلة هنا للوصول السريع.',
    rightRailUpdateBoxTitle: 'أمر المزامنة لمشرف الفريق',
    rightRailUpdateBoxDesc: 'هل عدلت أو أضفت مهارة جديدة؟ شغل هذا الأمر الواحد لتحديث المنصة والدليل:',
    modalCloseBtn: 'إغلاق',
    modalDomainLabel: 'مجال طلب المستخدم (متى تستخدم هذه المهارة/الأداة؟):',
    modalPromptLabel: 'الأمر الجاهز للنسخ واللصق (اضغط نسخ أو تشغيل في المحاكي):',
    modalTryInSimBtn: 'تشغيل في محاكي "جربها بنفسك »"',
    modalCopyCmdBtn: 'نسخ الأمر الجاهز',
    rank0: 'متدرب جديد (المستوى 1)',
    rank1: 'مطور صاعد (المستوى 2)',
    rank2: 'مهندس متكامل (المستوى 3)',
    rank3: 'مهندس أنظمة Agent OS (الرتبة القصوى)',
    toastCopied: 'تم نسخ الأمر الجاهز إلى الحافظة بنجاح!',
    toastSaved: 'تم تحديث حقيبة أوامرك المحفوظة!',
    toastLessonDone: 'تم إكمال الدرس بنجاح! ربحت +25 نقطة XP.',
    toastQuizRight: 'إجابة صحيحة! ربحت +25 نقطة XP.',
    toastQuizWrong: 'إجابة غير دقيقة — راجع التوضيح وحاول مرة أخرى.',
    mobileNavFeed: 'الموجز',
    mobileNavLessons: 'الدروس',
    mobileNavTryIt: 'المحاكي',
    mobileNavRef: '85 مهارة',
    mobileNavProfile: 'تقدمي'
  }
};
