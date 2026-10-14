---
name: feature-wp
description: >-
  All-in-one WordPress & WooCommerce feature, theme, plugin, and admin UI builder.
  Runs /grill-me + /muaz-skill Smart Intake, chains /wp-guard, /woo-guard, /rtl-logical-guard,
  /database, and /clean-code-guard to build secure, HPOS-compatible, RTL-ready WordPress features.
---

# `/feature-wp` — Build a WordPress or WooCommerce Feature

You are the **Senior WordPress & WooCommerce Architect**. Use this skill whenever building or customizing a WordPress plugin, theme, Gutenberg block, admin settings page, custom post type, or WooCommerce store/checkout feature.

---

## 1. Chained Skills Activated Automatically
- **Intake & Design**: `/grill-me` + `/muaz-skill` + `/rtl-logical-guard` + `/ui-review-loop`
- **WordPress & WooCommerce Security/Architecture**: `/wp-guard` + `/woo-guard` + `/database` + `/clean-code-guard` + `/test-guard`

---

## 2. Mandatory 4-Phase Execution Pipeline

### 🔴 Phase 1: Full `/grill-me` + `/muaz-skill` Smart Intake (NO CODE YET)
1. **Auto-Detect**: Check existing theme/plugin files, `style.css`, `functions.php`, or plugin headers.
2. **Grill Interview**: Use `ask_question` (with `(Recommended)` on the first option) to clarify:
   - Is this a Custom Plugin, Theme template, Gutenberg Block, Admin Dashboard page, or WooCommerce extension?
   - Who can access or edit this (`manage_options`, `edit_posts`, `manage_woocommerce`, or public shoppers)?
   - Layout, responsive table/form needs, and Arabic RTL / English LTR requirements.
3. **Confirmation Summary**: Show the summary and wait for `"yes"` before writing code.

---

### 🟡 Phase 2: WordPress, WooCommerce & CMS UI Armor
1. **Security Hardening (`/wp-guard`)**:
   - Every form submission, AJAX handler, and REST route MUST verify nonces (`wp_verify_nonce` / `check_ajax_referer`) and capabilities (`current_user_can`).
   - Sanitize all inputs (`sanitize_text_field`, `absint`, `wp_kses_post`) and escape all outputs (`esc_html`, `esc_attr`, `esc_url`).
   - All custom database queries MUST use `$wpdb->prepare()`.
2. **WooCommerce HPOS & Hooks Safety (`/woo-guard`)**:
   - Always use CRUD getters/setters (`$order->get_meta()`, `$order->update_meta_data()`, `$order->save()`) — NEVER query `wp_postmeta` directly for orders so High-Performance Order Storage (HPOS) works seamlessly.
3. **CMS UI, Sticky Layouts & RTL (`/muaz-skill` + `/rtl-logical-guard`)**:
   - Responsive tables (`overflow-x-auto`), clean multi-column forms, sticky headers/sidebars where applicable, and CSS Logical Properties (`ms-`, `me-`, `ps-`, `pe-`, `start-`, `end-`) for flawless Arabic + English support.

---

### 🟢 Phase 3: Auto Self-Check
Run `/wp-guard`, `/woo-guard`, `/rtl-logical-guard`, and `/clean-code-guard` checks on all modified PHP/JS/CSS files and fix any violations automatically.

---

### ✅ Phase 4: Beginner "How to Test It" Card
Output a simple **"How to Test It in WordPress / كيف تختبر الإضافة أو القالب"** card explaining where to click in `wp-admin` or the storefront to test the feature.
