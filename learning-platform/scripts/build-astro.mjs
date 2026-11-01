#!/usr/bin/env node
/**
 * Offline-First Astro Static Builder (`build-astro.mjs`).
 * If `node_modules/.bin/astro` is installed, delegates to `astro build`.
 * In low-bandwidth / offline environments without `node_modules`, deterministically
 * compiles `src/layouts/W3Layout.astro` + `src/pages/index.astro` + `src/data/curriculum.js`
 * + `src/data/skills-registry.json` into `dist/index.html` with embedded logical CSS.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  TECH_STACKS,
  STORY_REELS,
  CURRICULUM_TRACKS,
  SITUATION_COMBOS_CARDS,
  UI_DICTIONARY
} from '../src/data/curriculum.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = path.resolve(__dirname, '..');
const DIST_DIR = path.join(ROOT_DIR, 'dist');
const REGISTRY_PATH = path.join(ROOT_DIR, 'src', 'data', 'skills-registry.json');

const skillsRegistry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf-8'));
const allLessons = CURRICULUM_TRACKS.flatMap((t) => t.lessons);
const skillsList = skillsRegistry.skills || [];
const mcpList = skillsRegistry.mcpServers || [];
const uniqueCategoriesEn = Array.from(new Set(skillsList.map((s) => s.categoryEn)));

const clientPayload = JSON.stringify({
  techStacks: TECH_STACKS,
  storyReels: STORY_REELS,
  tracks: CURRICULUM_TRACKS,
  lessons: allLessons,
  combos: SITUATION_COMBOS_CARDS,
  skills: skillsList,
  mcpServers: mcpList,
  ui: UI_DICTIONARY
});

function escHtml(str) {
  return String(str ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

const EMBEDDED_LOGICAL_TAILWIND_CSS = `
/* Complete Tailwind Preflight Reset (Eliminates Windows Browser Default Gray Button Backgrounds & List Bullets) */
*, ::before, ::after { box-sizing: border-box; border-width: 0; border-style: solid; border-color: var(--w3-line); }
html { line-height: 1.5; -webkit-text-size-adjust: 100%; tab-size: 4; scroll-behavior: smooth; overflow-x: clip; }
body { margin: 0; line-height: inherit; background-color: var(--w3-canvas); color: var(--w3-ink); font-family: 'Plus Jakarta Sans', 'IBM Plex Sans Arabic', system-ui, sans-serif; overflow-x: clip; }
html.dark body { background-color: var(--w3-slate-deep); color: var(--w3-canvas); }
html[lang="ar"] body { font-family: 'IBM Plex Sans Arabic', 'Plus Jakarta Sans', system-ui, sans-serif; }
html[lang="en"] .lang-ar { display: none !important; }
html[lang="ar"] .lang-en { display: none !important; }
h1, h2, h3, h4, h5, h6 { font-size: inherit; font-weight: inherit; margin: 0; }
p, pre, blockquote, dl, dd, hr, figure { margin: 0; }
ol, ul, menu { list-style: none; margin: 0; padding: 0; }
button, input, optgroup, select, textarea {
  font-family: inherit;
  font-feature-settings: inherit;
  font-variation-settings: inherit;
  font-size: 100%;
  font-weight: inherit;
  line-height: inherit;
  color: inherit;
  margin: 0;
  padding: 0;
}
button, select { text-transform: none; }
button, [type="button"], [type="reset"], [type="submit"] {
  -webkit-appearance: button;
  appearance: none;
  background-color: transparent;
  background-image: none;
  cursor: pointer;
}
code, kbd, samp, pre { font-family: 'JetBrains Mono', monospace; font-size: 1em; }
table { text-indent: 0; border-color: inherit; border-collapse: collapse; }
svg, img, video, canvas { display: block; vertical-align: middle; }

/* Static W3Schools Design Tokens (Never invert --w3-ink or --w3-canvas so yellow/mint pills keep dark ink in dark mode!) */
:root {
  --navbar-height: 6rem;
  --w3-green: #04AA6D;
  --w3-green-hover: #059862;
  --w3-green-dark: #047857;
  --w3-slate: #282A35;
  --w3-slate-deep: #1D2A35;
  --w3-mint: #D9EEE1;
  --w3-yellow: #FFF4A3;
  --w3-pink: #FFC0C7;
  --w3-example: #E7E9EB;
  --w3-canvas: #FAFAF8;
  --w3-card: #FFFFFF;
  --w3-ink: #18181B;
  --w3-muted: #52525B;
  --w3-line: #D4D4D0;
}
.micro-transition {
  transition-property: transform, opacity, background-color, border-color, color, box-shadow;
  transition-duration: 150ms;
  transition-timing-function: cubic-bezier(0.22, 1, 0.36, 1);
}
.w3-scrollbar::-webkit-scrollbar { height: 6px; width: 6px; }
.w3-scrollbar::-webkit-scrollbar-track { background: transparent; }
.w3-scrollbar::-webkit-scrollbar-thumb { background-color: rgba(113, 113, 122, 0.45); border-radius: 9999px; }

/* Layout & Sizing */
.min-h-dvh { min-height: 100dvh; }
.h-dvh { height: 100dvh; }
.h-14 { height: 3.5rem; }
.h-10 { height: 2.5rem; }
.h-9 { height: 2.25rem; }
.h-8 { height: 2rem; }
.h-5 { height: 1.25rem; }
.h-4 { height: 1rem; }
.h-3\\.5 { height: 0.875rem; }
.h-2\\.5 { height: 0.625rem; }
.h-2 { height: 0.5rem; }
.h-1\\.5 { height: 0.375rem; }
.h-full { height: 100%; }
.w-full { width: 100%; }
.w-72 { width: 18rem; }
.w-64 { width: 16rem; }
.w-44 { width: 11rem; }
.w-36 { width: 9rem; }
.w-10 { width: 2.5rem; }
.w-9 { width: 2.25rem; }
.w-8 { width: 2rem; }
.w-5 { width: 1.25rem; }
.w-4 { width: 1rem; }
.w-3\\.5 { width: 0.875rem; }
.w-2 { width: 0.5rem; }
.w-0 { width: 0px; }
.max-w-7xl { max-width: 80rem; }
.max-w-3xl { max-width: 48rem; }
.max-w-lg { max-width: 32rem; }
.max-w-md { max-width: 28rem; }
.max-w-xs { max-width: 20rem; }
.min-w-0 { min-width: 0px; }
.shrink-0 { flex-shrink: 0; }
.flex-1 { flex: 1 1 0%; }
.flex { display: flex; }
.inline-flex { display: inline-flex; }
.inline-block { display: inline-block; }
.block { display: block; }
.grid { display: grid; }
.hidden { display: none !important; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }
.items-start { align-items: flex-start; }
.items-center { align-items: center; }
.items-stretch { align-items: stretch; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.justify-around { justify-content: space-around; }
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.gap-0 { gap: 0px; }
.gap-1 { gap: 0.25rem; }
.gap-1\\.5 { gap: 0.375rem; }
.gap-2 { gap: 0.5rem; }
.gap-2\\.5 { gap: 0.625rem; }
.gap-3 { gap: 0.75rem; }
.gap-4 { gap: 1rem; }
.gap-6 { gap: 1.5rem; }
.space-y-1 > :not([hidden]) ~ :not([hidden]) { margin-top: 0.25rem; }
.space-y-1\\.5 > :not([hidden]) ~ :not([hidden]) { margin-top: 0.375rem; }
.space-y-2 > :not([hidden]) ~ :not([hidden]) { margin-top: 0.5rem; }
.space-y-3 > :not([hidden]) ~ :not([hidden]) { margin-top: 0.75rem; }
.space-y-4 > :not([hidden]) ~ :not([hidden]) { margin-top: 1rem; }
.space-y-6 > :not([hidden]) ~ :not([hidden]) { margin-top: 1.5rem; }
.divide-y > :not([hidden]) ~ :not([hidden]) { border-top-width: 1px; border-color: var(--w3-line); }

/* Positioning */
.sticky { position: sticky; }
.fixed { position: fixed; }
.relative { position: relative; }
.absolute { position: absolute; }
.inset-0 { inset: 0px; }
.inset-x-0 { inset-inline: 0px; }
.inset-y-0 { top: 0px; bottom: 0px; }
.top-0 { top: 0px; }
.top-28 { top: 7rem; }
.bottom-0 { bottom: 0px; }
.bottom-16 { bottom: 4rem; }
.start-0 { inset-inline-start: 0px; }
.start-3 { inset-inline-start: 0.75rem; }
.end-4 { inset-inline-end: 1rem; }
.z-20 { z-index: 20; }
.z-40 { z-index: 40; }
.z-50 { z-index: 50; }

/* Overflow & Truncation */
.overflow-hidden { overflow: hidden; }
.overflow-x-auto { overflow-x: auto; }
.overflow-y-auto { overflow-y: auto; }
.overflow-x-clip { overflow-x: clip; }
.truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.whitespace-nowrap { white-space: nowrap; }
.whitespace-pre-line { white-space: pre-line; }
.pointer-events-none { pointer-events: none; }
.border-collapse { border-collapse: collapse; }

/* Logical Spacing */
.mx-auto { margin-inline: auto; }
.mt-0\\.5 { margin-top: 0.125rem; }
.mt-1 { margin-top: 0.25rem; }
.mt-1\\.5 { margin-top: 0.375rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-2\\.5 { margin-top: 0.625rem; }
.mt-3 { margin-top: 0.75rem; }
.mt-4 { margin-top: 1rem; }
.mt-6 { margin-top: 1.5rem; }
.mb-0 { margin-bottom: 0px; }
.mb-0\\.5 { margin-bottom: 0.125rem; }
.mb-1 { margin-bottom: 0.25rem; }
.mb-1\\.5 { margin-bottom: 0.375rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-3 { margin-bottom: 0.75rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-5 { margin-bottom: 1.25rem; }
.mb-6 { margin-bottom: 1.5rem; }
.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-2\\.5 { padding: 0.625rem; }
.p-3 { padding: 0.75rem; }
.p-3\\.5 { padding: 0.875rem; }
.p-4 { padding: 1rem; }
.p-5 { padding: 1.25rem; }
.px-0 { padding-inline: 0px; }
.px-1 { padding-inline: 0.25rem; }
.px-1\\.5 { padding-inline: 0.375rem; }
.px-2 { padding-inline: 0.5rem; }
.px-2\\.5 { padding-inline: 0.625rem; }
.px-3 { padding-inline: 0.75rem; }
.px-3\\.5 { padding-inline: 0.875rem; }
.px-4 { padding-inline: 1rem; }
.px-5 { padding-inline: 1.25rem; }
.py-0\\.5 { padding-block: 0.125rem; }
.py-1 { padding-block: 0.25rem; }
.py-1\\.5 { padding-block: 0.375rem; }
.py-2 { padding-block: 0.5rem; }
.py-2\\.5 { padding-block: 0.625rem; }
.py-3 { padding-block: 0.75rem; }
.ps-10 { padding-inline-start: 2.5rem; }
.pe-4 { padding-inline-end: 1rem; }
.pt-0 { padding-top: 0px; }
.pt-1 { padding-top: 0.25rem; }
.pt-3 { padding-top: 0.75rem; }
.pt-5 { padding-top: 1.25rem; }
.pb-1 { padding-bottom: 0.25rem; }
.pb-2 { padding-bottom: 0.5rem; }
.pb-3 { padding-bottom: 0.75rem; }
.pb-4 { padding-bottom: 1rem; }
.pb-12 { padding-bottom: 3rem; }
.pb-16 { padding-bottom: 4rem; }

/* Borders & Radius */
.border { border-width: 1px; }
.border-2 { border-width: 2px; }
.border-b { border-bottom-width: 1px; }
.border-t { border-top-width: 1px; }
.border-e { border-inline-end-width: 1px; }
.border-s-4 { border-inline-start-width: 4px; }
.rounded { border-radius: 0.25rem; }
.rounded-md { border-radius: 0.375rem; }
.rounded-lg { border-radius: 0.5rem; }
.rounded-xl { border-radius: 0.75rem; }
.rounded-2xl { border-radius: 1rem; }
.rounded-full { border-radius: 9999px; }
.rounded-none { border-radius: 0px; }

/* Light Mode Colors & Surfaces */
.bg-w3-green { background-color: var(--w3-green); }
.hover\\:bg-w3-green:hover { background-color: var(--w3-green); }
.hover\\:bg-w3-greenHover:hover { background-color: var(--w3-green-hover); }
.bg-w3-slate { background-color: var(--w3-slate); }
.bg-w3-slate\\/75 { background-color: rgba(40, 42, 53, 0.75); }
.bg-w3-slate\\/80 { background-color: rgba(40, 42, 53, 0.8); }
.bg-w3-slate\\/90 { background-color: rgba(40, 42, 53, 0.9); }
.bg-w3-slateDeep { background-color: var(--w3-slate-deep); }
.bg-w3-mint { background-color: var(--w3-mint); }
.bg-w3-mint\\/40 { background-color: rgba(217, 238, 225, 0.4); }
.bg-w3-mint\\/50 { background-color: rgba(217, 238, 225, 0.5); }
.hover\\:bg-w3-mint:hover { background-color: var(--w3-mint); }
.hover\\:bg-w3-mint\\/40:hover { background-color: rgba(217, 238, 225, 0.4); }
.bg-w3-yellow { background-color: var(--w3-yellow); }
.bg-w3-pink { background-color: var(--w3-pink); }
.bg-w3-pink\\/30 { background-color: rgba(255, 192, 199, 0.3); }
.bg-w3-example { background-color: var(--w3-example); }
.hover\\:bg-w3-example:hover { background-color: var(--w3-example); }
.hover\\:bg-w3-example\\/60:hover { background-color: rgba(231, 233, 235, 0.6); }
.bg-w3-canvas { background-color: var(--w3-canvas); }
.bg-w3-card { background-color: var(--w3-card); }
.hover\\:bg-w3-card:hover { background-color: var(--w3-card); }
.bg-zinc-700 { background-color: #3f3f46; }

.text-white { color: #FFFFFF; }
.hover\\:text-white:hover { color: #FFFFFF; }
.text-w3-ink { color: var(--w3-ink); }
.text-w3-canvas { color: var(--w3-canvas); }
.text-w3-muted { color: var(--w3-muted); }
.text-w3-green { color: var(--w3-green); }
.text-w3-greenDark { color: var(--w3-green-dark); }
.hover\\:text-w3-greenDark:hover { color: var(--w3-green-dark); }
.text-w3-mint { color: var(--w3-mint); }
.text-w3-yellow { color: var(--w3-yellow); }
.text-w3-pink { color: var(--w3-pink); }
.text-zinc-100 { color: #f4f4f5; }
.text-zinc-200 { color: #e4e4e7; }
.text-zinc-300 { color: #d4d4d8; }
.text-zinc-400 { color: #a1a1aa; }
.text-red-800 { color: #991b1b; }
.text-red-900 { color: #7f1d1d; }

.border-w3-line { border-color: var(--w3-line); }
.border-w3-green { border-color: var(--w3-green); }
.border-w3-green\\/40 { border-color: rgba(4, 170, 109, 0.4); }
.hover\\:border-w3-green:hover { border-color: var(--w3-green); }
.hover\\:border-w3-greenDark:hover { border-color: var(--w3-green-dark); }
.hover\\:border-w3-mint:hover { border-color: var(--w3-mint); }
.border-w3-yellow { border-color: var(--w3-yellow); }
.border-w3-pink { border-color: var(--w3-pink); }
.border-zinc-600 { border-color: #52525b; }
.border-zinc-700 { border-color: #3f3f46; }
.border-red-300 { border-color: #fca5a5; }

/* Explicit High-Contrast Dark Mode Overrides (html.dark .dark:*) */
html.dark .dark\\:bg-w3-slate { background-color: var(--w3-slate); }
html.dark .dark\\:bg-w3-slateDeep { background-color: var(--w3-slate-deep); }
html.dark .dark\\:bg-w3-green { background-color: var(--w3-green); }
html.dark .dark\\:hover\\:bg-w3-slate:hover { background-color: var(--w3-slate); }
html.dark .dark\\:hover\\:bg-w3-slateDeep:hover { background-color: var(--w3-slate-deep); }
html.dark .dark\\:text-w3-canvas { color: var(--w3-canvas); }
html.dark .dark\\:text-white { color: #FFFFFF; }
html.dark .dark\\:text-w3-mint { color: var(--w3-mint); }
html.dark .dark\\:text-w3-pink { color: var(--w3-pink); }
html.dark .dark\\:text-zinc-100 { color: #f4f4f5; }
html.dark .dark\\:text-zinc-200 { color: #e4e4e7; }
html.dark .dark\\:text-zinc-300 { color: #d4d4d8; }
html.dark .dark\\:text-zinc-400 { color: #a1a1aa; }
html.dark .dark\\:border-zinc-700 { border-color: #3f3f46; }
html.dark .dark\\:border-w3-pink\\/50 { border-color: rgba(255, 192, 199, 0.5); }
html.dark .dark\\:divide-zinc-700 > :not([hidden]) ~ :not([hidden]) { border-color: #3f3f46; }

/* Typography */
.font-sans { font-family: 'Plus Jakarta Sans', 'IBM Plex Sans Arabic', system-ui, sans-serif; }
.font-display { font-family: 'Space Grotesk', 'IBM Plex Sans Arabic', system-ui, sans-serif; }
.font-mono { font-family: 'JetBrains Mono', monospace; }
.text-xs { font-size: 0.75rem; line-height: 1.125rem; }
.text-sm { font-size: 0.875rem; line-height: 1.35rem; }
.text-base { font-size: 1rem; line-height: 1.5rem; }
.text-lg { font-size: 1.125rem; line-height: 1.65rem; }
.text-xl { font-size: 1.25rem; line-height: 1.75rem; }
.text-2xl { font-size: 1.5rem; line-height: 2rem; }
.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }
.leading-none { line-height: 1; }
.leading-tight { line-height: 1.25; }
.leading-snug { line-height: 1.375; }
.leading-relaxed { line-height: 1.625; }
.tracking-tight { letter-spacing: -0.025em; }
.text-start { text-align: start; }
.text-end { text-align: end; }
.text-center { text-align: center; }
.hover\\:underline:hover { text-decoration: underline; }
.shadow-sm { box-shadow: 0 1px 2px 0 rgba(24, 24, 27, 0.06); }
.shadow-lg { box-shadow: 0 10px 15px -3px rgba(24, 24, 27, 0.15); }
.shadow-xl { box-shadow: 0 20px 25px -5px rgba(24, 24, 27, 0.25); }
.focus-visible\\:outline-none:focus-visible { outline: 2px solid transparent; outline-offset: 2px; }
.focus-visible\\:ring-2:focus-visible { box-shadow: 0 0 0 2px var(--w3-green); }
.focus-visible\\:ring-white:focus-visible { box-shadow: 0 0 0 2px #FFFFFF; }

/* Transforms for Mobile Drawer */
.-translate-x-full { transform: translateX(-100%); }
html[dir="rtl"] .rtl\\:translate-x-full { transform: translateX(100%); }

/* Responsive Breakpoints */
@media (min-width: 640px) {
  .sm\\:block { display: block; }
  .sm\\:flex-row { flex-direction: row; }
  .sm\\:items-center { align-items: center; }
  .sm\\:table-cell { display: table-cell; }
  .sm\\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  .sm\\:px-0 { padding-inline: 0px; }
  .sm\\:px-4 { padding-inline: 1rem; }
  .sm\\:px-6 { padding-inline: 1.5rem; }
  .sm\\:p-6 { padding: 1.5rem; }
  .sm\\:p-8 { padding: 2rem; }
  .sm\\:gap-4 { gap: 1rem; }
  .sm\\:rounded-xl { border-radius: 0.75rem; }
  .sm\\:border { border-width: 1px; }
  .sm\\:text-sm { font-size: 0.875rem; line-height: 1.35rem; }
  .sm\\:text-base { font-size: 1rem; line-height: 1.5rem; }
  .sm\\:text-lg { font-size: 1.125rem; line-height: 1.65rem; }
  .sm\\:text-xl { font-size: 1.25rem; line-height: 1.75rem; }
  .sm\\:text-2xl { font-size: 1.5rem; line-height: 2rem; }
  .sm\\:text-3xl { font-size: 1.875rem; line-height: 2.25rem; }
  .sm\\:text-4xl { font-size: 2.25rem; line-height: 2.5rem; }
}
@media (min-width: 768px) {
  .md\\:block { display: block; }
  .md\\:flex-row { flex-direction: row; }
  .md\\:items-center { align-items: center; }
  .md\\:w-72 { width: 18rem; }
  .md\\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (min-width: 1024px) {
  .lg\\:hidden { display: none !important; }
  .lg\\:flex { display: flex; }
  .lg\\:sticky { position: sticky; }
  .lg\\:top-28 { top: 7rem; }
  .lg\\:z-20 { z-index: 20; }
  .lg\\:w-64 { width: 16rem; }
  .lg\\:h-\\[calc\\(100dvh-7\\.5rem\\)\\] { height: calc(100dvh - 7.5rem); }
  .lg\\:border { border-width: 1px; }
  .lg\\:rounded-lg { border-radius: 0.5rem; }
  .lg\\:rounded-xl { border-radius: 0.75rem; }
  .lg\\:translate-x-0, html[dir="rtl"] .rtl\\:lg\\:translate-x-0 { transform: translateX(0px); }
  .lg\\:gap-5 { gap: 1.25rem; }
  .lg\\:gap-6 { gap: 1.5rem; }
  .lg\\:px-6 { padding-inline: 1.5rem; }
  .lg\\:pt-6 { padding-top: 1.5rem; }
  .lg\\:pb-0 { padding-bottom: 0px; }
  .lg\\:bottom-6 { bottom: 1.5rem; }
  .lg\\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .lg\\:grid-cols-\\[repeat\\(3\\,minmax\\(0\\,1fr\\)\\)\\] { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (min-width: 1280px) {
  .xl\\:flex { display: flex; }
  .xl\\:block { display: block; }
  .xl\\:max-w-md { max-width: 28rem; }
}
`;

function renderStaticHtml() {
  const ribbonCombosHtml = SITUATION_COMBOS_CARDS.map(
    (combo) =>
      `<button type="button" data-ribbon-lesson="${escHtml(combo.lessonId)}" data-ribbon-cmd="${escHtml(combo.command)}" class="subnav-pill px-2.5 py-1 rounded bg-w3-slateDeep text-zinc-100 border border-zinc-700 hover:bg-w3-green hover:text-white hover:border-w3-green focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">${escHtml(combo.command)}</button>`
  ).join('\n        ');

  const sidebarTracksHtml = CURRICULUM_TRACKS.map((track) => {
    const lessonsHtml = track.lessons
      .map((lesson, idx) => {
        const activeCls =
          idx === 0 && track.id === 'track-start'
            ? 'bg-w3-green text-white font-semibold border-w3-green shadow-sm'
            : 'bg-w3-card dark:bg-w3-slateDeep text-w3-ink dark:text-zinc-100 border-w3-line dark:border-zinc-700 hover:border-w3-green';
        return `<li>
                  <button type="button" data-open-lesson="${escHtml(lesson.id)}" class="sidebar-lesson-btn w-full flex items-center justify-between gap-2 px-3 py-2 rounded-lg text-xs text-start border focus-visible:ring-2 focus-visible:ring-w3-green micro-transition ${activeCls}">
                    <span class="truncate">
                      <span class="lang-en">${escHtml(lesson.badgeEn)}: ${escHtml(lesson.titleEn)}</span>
                      <span class="lang-ar">${escHtml(lesson.badgeAr)}: ${escHtml(lesson.titleAr)}</span>
                    </span>
                    <span data-lesson-tick="${escHtml(lesson.id)}" class="hidden shrink-0 inline-flex items-center justify-center w-4 h-4 rounded-full bg-w3-mint text-w3-greenDark text-xs font-bold">+</span>
                  </button>
                </li>`;
      })
      .join('\n              ');

    return `<div>
            <h3 class="font-display font-bold text-xs text-w3-ink dark:text-w3-mint mt-3 mb-2 px-1">
              <span class="lang-en">${escHtml(track.titleEn)}</span>
              <span class="lang-ar">${escHtml(track.titleAr)}</span>
            </h3>
            <ul class="space-y-1.5">
              ${lessonsHtml}
            </ul>
          </div>`;
  }).join('\n        ');

  const storyRingsHtml = STORY_REELS.map(
    (reel, idx) =>
      `<button type="button" data-open-story="${idx}" class="story-ring-btn shrink-0 w-44 p-3.5 rounded-xl border-2 border-w3-green bg-w3-canvas dark:bg-w3-slateDeep hover:bg-w3-mint/40 dark:hover:bg-w3-slate text-start flex flex-col justify-between focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                <div class="flex items-center justify-between gap-1">
                  <span class="inline-block px-2 py-0.5 rounded-full bg-w3-mint text-w3-greenDark font-mono text-xs font-bold">
                    <span class="lang-en">${escHtml(reel.badgeEn)}</span>
                    <span class="lang-ar">${escHtml(reel.badgeAr)}</span>
                  </span>
                  <span class="inline-flex items-center justify-center w-5 h-5 rounded-full bg-w3-green text-white text-xs font-bold">»</span>
                </div>
                <span class="font-display font-bold text-xs sm:text-sm text-w3-ink dark:text-w3-canvas block mt-2.5 leading-snug">
                  <span class="lang-en">${escHtml(reel.titleEn)}</span>
                  <span class="lang-ar">${escHtml(reel.titleAr)}</span>
                </span>
                <span class="text-xs text-w3-muted dark:text-zinc-300 block mt-1 truncate">
                  <span class="lang-en">${escHtml(reel.authorEn)}</span>
                  <span class="lang-ar">${escHtml(reel.authorAr)}</span>
                </span>
              </button>`
  ).join('\n            ');

  const combosGridHtml = SITUATION_COMBOS_CARDS.map((card, idx) => {
    const hiddenCls = idx >= 3 ? 'hidden' : '';
    return `<article data-combo-card-index="${idx}" class="combo-grid-card rounded-xl border border-w3-line dark:border-zinc-700 bg-w3-canvas dark:bg-w3-slateDeep p-4 flex flex-col justify-between ${hiddenCls}">
                <div>
                  <div class="flex items-center justify-between gap-2 mb-2">
                    <code class="px-2.5 py-1 rounded bg-w3-slate text-w3-mint font-mono text-xs font-semibold">${escHtml(card.command)}</code>
                    <span class="text-xs font-mono text-w3-muted dark:text-zinc-300">
                      <span class="lang-en">${escHtml(card.badgeEn)}</span>
                      <span class="lang-ar">${escHtml(card.badgeAr)}</span>
                    </span>
                  </div>
                  <h3 class="font-display font-bold text-base text-w3-ink dark:text-w3-canvas mt-3 mb-1.5">
                    <span class="lang-en">${escHtml(card.titleEn)}</span>
                    <span class="lang-ar">${escHtml(card.titleAr)}</span>
                  </h3>
                  <p class="text-xs text-w3-muted dark:text-zinc-300 leading-relaxed mb-4">
                    <span class="lang-en">${escHtml(card.descEn)}</span>
                    <span class="lang-ar">${escHtml(card.descAr)}</span>
                  </p>
                </div>
                <div class="flex items-center justify-between gap-2 pt-3 border-t border-w3-line dark:border-zinc-700">
                  <button type="button" data-try-command="${escHtml(card.command)}" data-try-prompt-en="${escHtml(card.samplePromptEn)}" data-try-prompt-ar="${escHtml(card.samplePromptAr)}" class="px-3 py-1.5 rounded-md bg-w3-green hover:bg-w3-greenHover text-white text-xs font-semibold focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.tryItBtn)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.tryItBtn)}</span>
                  </button>
                  <button type="button" data-open-lesson="${escHtml(card.lessonId)}" class="px-2.5 py-1.5 rounded-md bg-w3-example dark:bg-w3-slate text-xs font-semibold text-w3-greenDark dark:text-w3-mint hover:bg-w3-green hover:text-white focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                    <span class="lang-en">Lesson »</span>
                    <span class="lang-ar">الدرس »</span>
                  </button>
                </div>
              </article>`;
  }).join('\n            ');

  const feedCardsHtml = allLessons
    .map((lesson) => {
      const initials = lesson.command.replace('/', '').slice(0, 2).toUpperCase();
      const bulletsHtml = lesson.bulletsEn
        .map(
          (bEn, i) =>
            `<li class="flex items-start gap-2">
                    <span class="inline-block w-2 h-2 rounded-full bg-w3-green mt-1.5 shrink-0"></span>
                    <span>
                      <span class="lang-en">${escHtml(bEn)}</span>
                      <span class="lang-ar">${escHtml(lesson.bulletsAr[i])}</span>
                    </span>
                  </li>`
        )
        .join('\n                ');

      return `<article data-feed-card="${escHtml(lesson.id)}" data-feed-cat="${escHtml(lesson.feedCategory)}" class="feed-post-card bg-w3-card dark:bg-w3-slate rounded-xl border border-w3-line dark:border-zinc-700 p-4 sm:p-6 shadow-sm">
              <div class="flex items-start justify-between gap-3 pb-3 border-b border-w3-line dark:border-zinc-700">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-w3-green text-white font-display font-bold text-sm flex items-center justify-center shrink-0">${escHtml(initials)}</div>
                  <div>
                    <div class="flex items-center gap-2 flex-wrap">
                      <span class="font-display font-bold text-sm text-w3-ink dark:text-w3-canvas">
                        <span class="lang-en">${escHtml(lesson.authorEn)}</span>
                        <span class="lang-ar">${escHtml(lesson.authorAr)}</span>
                      </span>
                      <span class="px-2 py-0.5 rounded-full bg-w3-mint text-w3-greenDark font-mono text-xs font-bold">
                        <span class="lang-en">${escHtml(lesson.badgeEn)}</span>
                        <span class="lang-ar">${escHtml(lesson.badgeAr)}</span>
                      </span>
                    </div>
                    <span class="text-xs text-w3-muted dark:text-zinc-300 block">
                      <span class="lang-en">${escHtml(lesson.roleEn)} • ${escHtml(lesson.readTimeEn)}</span>
                      <span class="lang-ar">${escHtml(lesson.roleAr)} • ${escHtml(lesson.readTimeAr)}</span>
                    </span>
                  </div>
                </div>
                <span class="px-2.5 py-1 rounded bg-w3-yellow text-w3-ink font-mono text-xs font-bold shrink-0">+${lesson.xp} XP</span>
              </div>

              <h2 class="font-display font-bold text-lg sm:text-xl text-w3-ink dark:text-w3-canvas mt-4 mb-2">
                <span class="lang-en">${escHtml(lesson.titleEn)}</span>
                <span class="lang-ar">${escHtml(lesson.titleAr)}</span>
              </h2>
              <p class="text-sm text-w3-muted dark:text-zinc-200 leading-relaxed mb-4">
                <span class="lang-en">${escHtml(lesson.summaryEn)}</span>
                <span class="lang-ar">${escHtml(lesson.summaryAr)}</span>
              </p>

              <ul class="space-y-2 mb-4 text-xs sm:text-sm text-w3-ink dark:text-zinc-100">
                ${bulletsHtml}
              </ul>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                <div class="rounded-lg bg-w3-pink/30 dark:bg-w3-slateDeep border border-red-300 dark:border-w3-pink/50 p-3.5">
                  <span class="font-mono text-xs font-bold text-red-800 dark:text-w3-pink block mb-1">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.beforeLabel)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.beforeLabel)}</span>
                  </span>
                  <p class="text-xs text-w3-ink dark:text-zinc-200 whitespace-pre-line">
                    <span class="lang-en">${escHtml(lesson.beforeEn)}</span>
                    <span class="lang-ar">${escHtml(lesson.beforeAr)}</span>
                  </p>
                </div>

                <div class="rounded-lg bg-w3-mint/50 dark:bg-w3-slateDeep border border-w3-green p-3.5">
                  <span class="font-mono text-xs font-bold text-w3-greenDark dark:text-w3-mint block mb-1">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.afterLabel)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.afterLabel)}</span>
                  </span>
                  <p class="text-xs text-w3-ink dark:text-zinc-200 whitespace-pre-line">
                    <span class="lang-en">${escHtml(lesson.afterEn)}</span>
                    <span class="lang-ar">${escHtml(lesson.afterAr)}</span>
                  </p>
                </div>
              </div>

              <div class="rounded-lg bg-w3-example dark:bg-w3-slateDeep p-4 border border-w3-line dark:border-zinc-700 mb-4">
                <div class="flex items-center justify-between gap-2 mb-2">
                  <h3 class="font-display font-bold text-sm text-w3-ink dark:text-w3-canvas mt-1 mb-0">
                    <span class="lang-en">${escHtml(lesson.exampleTitleEn)}</span>
                    <span class="lang-ar">${escHtml(lesson.exampleTitleAr)}</span>
                  </h3>
                  <code class="text-xs font-mono px-2.5 py-0.5 rounded bg-w3-slate text-w3-mint font-semibold">${escHtml(lesson.command)}</code>
                </div>

                <div class="bg-w3-card dark:bg-w3-slate border-s-4 border-w3-green p-3 rounded font-mono text-xs text-w3-ink dark:text-zinc-100 overflow-x-auto mb-3">
                  <div class="lang-en">${escHtml(lesson.promptEn)}</div>
                  <div class="lang-ar">${escHtml(lesson.promptAr)}</div>
                </div>

                <div class="flex flex-wrap items-center gap-2">
                  <button type="button" data-try-command="${escHtml(lesson.command)}" data-try-prompt-en="${escHtml(lesson.promptEn)}" data-try-prompt-ar="${escHtml(lesson.promptAr)}" class="px-4 py-2 rounded-md bg-w3-green hover:bg-w3-greenHover text-white font-semibold text-xs focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.tryItBtn)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.tryItBtn)}</span>
                  </button>
                  <button type="button" data-copy-text-en="${escHtml(lesson.promptEn)}" data-copy-text-ar="${escHtml(lesson.promptAr)}" class="px-3 py-2 rounded-md bg-w3-card dark:bg-w3-slate border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas font-semibold text-xs hover:border-w3-green focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.modalCopyCmdBtn)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.modalCopyCmdBtn)}</span>
                  </button>
                  <button type="button" data-open-lesson="${escHtml(lesson.id)}" class="px-3 py-2 rounded-md bg-w3-card dark:bg-w3-slate border border-w3-line dark:border-zinc-700 text-w3-greenDark dark:text-w3-mint font-semibold text-xs hover:border-w3-green focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.readFullLessonBtn)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.readFullLessonBtn)}</span>
                  </button>
                </div>
              </div>

              <div class="flex flex-wrap items-center justify-between gap-2 pt-3 border-t border-w3-line dark:border-zinc-700">
                <div class="flex items-center gap-2">
                  <button type="button" data-like-lesson="${escHtml(lesson.id)}" class="like-lesson-btn inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-w3-canvas dark:bg-w3-slateDeep border border-w3-line dark:border-zinc-700 text-xs font-semibold text-w3-ink dark:text-w3-canvas hover:border-w3-green focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                    <svg class="w-3.5 h-3.5 text-w3-green" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                      <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                    </svg>
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.helpfulBtn)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.helpfulBtn)}</span>
                    <span data-like-count="${escHtml(lesson.id)}" class="font-mono text-w3-greenDark dark:text-w3-mint">12</span>
                  </button>

                  <button type="button" data-bookmark-cmd="${escHtml(lesson.command)}" data-bookmark-title-en="${escHtml(lesson.titleEn)}" data-bookmark-title-ar="${escHtml(lesson.titleAr)}" class="bookmark-cmd-btn inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-w3-canvas dark:bg-w3-slateDeep border border-w3-line dark:border-zinc-700 text-xs font-semibold text-w3-ink dark:text-w3-canvas hover:border-w3-green focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                    <svg class="w-3.5 h-3.5 text-w3-greenDark dark:text-w3-mint" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                    </svg>
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.saveToolkitBtn)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.saveToolkitBtn)}</span>
                  </button>
                </div>

                <button type="button" data-complete-lesson="${escHtml(lesson.id)}" class="complete-lesson-btn px-3.5 py-1.5 rounded-full bg-w3-mint text-w3-greenDark font-bold text-xs hover:bg-w3-green hover:text-white focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                  <span class="lang-en">${escHtml(UI_DICTIONARY.en.markCompleteBtn)}</span>
                  <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.markCompleteBtn)}</span>
                </button>
              </div>
            </article>`;
    })
    .join('\n          ');

  const simComboOptionsHtml = SITUATION_COMBOS_CARDS.map(
    (c) => `<option value="${escHtml(c.command)}">${escHtml(c.command)} - ${escHtml(c.titleEn)}</option>`
  ).join('\n                  ');

  const simStackOptionsHtml = TECH_STACKS.map(
    (st) => `<option value="${escHtml(st.id)}">${escHtml(st.labelEn)}</option>`
  ).join('\n                  ');

  const catOptionsHtml = uniqueCategoriesEn
    .map((cat) => `<option value="${escHtml(cat)}">${escHtml(cat)}</option>`)
    .join('\n                ');

  const skillsRowsHtml = skillsList
    .map((skill, idx) => {
      const hiddenCls = idx >= 12 ? 'hidden' : '';
      const searchStr = `${skill.name} ${skill.categoryEn} ${skill.categoryAr} ${skill.phase} ${skill.descriptionEn} ${skill.descriptionAr}`.toLowerCase();
      return `<tr data-skill-row="${escHtml(skill.name)}" data-skill-cat="${escHtml(skill.categoryEn)}" data-skill-search="${escHtml(searchStr)}" class="skill-table-row hover:bg-w3-example/60 dark:hover:bg-w3-slateDeep ${hiddenCls}">
                    <td class="py-2.5 px-3 font-mono font-semibold text-w3-greenDark dark:text-w3-mint whitespace-nowrap">${escHtml(skill.command)}</td>
                    <td class="py-2.5 px-3 text-w3-muted dark:text-zinc-300 max-w-xs truncate hidden sm:table-cell">
                      <span class="lang-en">${escHtml(skill.categoryEn)}</span>
                      <span class="lang-ar">${escHtml(skill.categoryAr)}</span>
                    </td>
                    <td class="py-2.5 px-3 whitespace-nowrap">
                      <span class="px-2 py-0.5 rounded bg-w3-example dark:bg-w3-slateDeep font-mono text-xs text-w3-ink dark:text-zinc-200">${escHtml(skill.phase)}</span>
                    </td>
                    <td class="py-2.5 px-3 max-w-xs truncate text-w3-ink dark:text-zinc-200">
                      <span class="lang-en">${escHtml(skill.shortEn)}</span>
                      <span class="lang-ar">${escHtml(skill.shortAr)}</span>
                    </td>
                    <td class="py-2.5 px-3 text-end whitespace-nowrap">
                      <button type="button" data-open-skill-modal="${escHtml(skill.name)}" class="px-2.5 py-1 rounded bg-w3-green hover:bg-w3-greenHover text-white font-semibold text-xs focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                        <span class="lang-en">${escHtml(UI_DICTIONARY.en.refDetailsBtn)}</span>
                        <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.refDetailsBtn)}</span>
                      </button>
                    </td>
                  </tr>`;
    })
    .join('\n                ');

  const mcpRowsHtml = mcpList
    .map(
      (srv) =>
        `<tr class="hover:bg-w3-example/60 dark:hover:bg-w3-slateDeep">
                    <td class="py-2 px-3 font-mono font-semibold text-w3-greenDark dark:text-w3-mint whitespace-nowrap">${escHtml(srv.name)}</td>
                    <td class="py-2 px-3 font-mono text-xs text-w3-ink dark:text-zinc-200">${escHtml(srv.phase)}</td>
                    <td class="py-2 px-3 max-w-xs truncate text-w3-ink dark:text-zinc-200">
                      <span class="lang-en">${escHtml(srv.shortEn)}</span>
                      <span class="lang-ar">${escHtml(srv.shortAr)}</span>
                    </td>
                    <td class="py-2 px-3 text-end whitespace-nowrap">
                      <button type="button" data-open-mcp-modal="${escHtml(srv.name)}" class="px-2.5 py-1 rounded bg-w3-example dark:bg-w3-slateDeep border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas font-semibold text-xs hover:bg-w3-green hover:text-white focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                        <span class="lang-en">${escHtml(UI_DICTIONARY.en.refDetailsBtn)}</span>
                        <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.refDetailsBtn)}</span>
                      </button>
                    </td>
                  </tr>`
    )
    .join('\n                ');

  // Extract inline script body from src/pages/index.astro
  const indexAstroRaw = fs.readFileSync(path.join(ROOT_DIR, 'src', 'pages', 'index.astro'), 'utf-8');
  const scriptMatch = indexAstroRaw.match(/<script is:inline define:vars=\{\{ clientPayload \}\}>([\s\S]*?)<\/script>/);
  const inlineScriptBody = scriptMatch ? scriptMatch[1] : '';

  return `<!doctype html>
<html lang="en" dir="ltr" class="scroll-smooth overflow-x-clip">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Agent OS - W3Schools x Social Learning Platform (v1.15.0)</title>
    <meta name="description" content="Interactive W3Schools-style tutorial reader, social learning feed, Try-it-Yourself simulator, and 60-skill dictionary for Agent OS." />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet" />
    <style>${EMBEDDED_LOGICAL_TAILWIND_CSS}</style>
  </head>
  <body class="min-h-dvh flex flex-col bg-w3-canvas text-w3-ink dark:bg-w3-slateDeep dark:text-w3-canvas overflow-x-clip pb-16 lg:pb-0">
    <!-- LAYER 1A: STICKY TOPBAR (h-14) -->
    <header class="sticky top-0 z-40 bg-w3-card dark:bg-w3-slate border-b border-w3-line dark:border-zinc-700">
      <div class="max-w-7xl mx-auto px-3 sm:px-6 h-14 flex items-center justify-between gap-2 sm:gap-4">
        <div class="flex items-center gap-2 shrink-0">
          <button type="button" id="mobile-drawer-open-btn" aria-label="Toggle W3Schools Chapter Menu" class="lg:hidden inline-flex items-center justify-center w-10 h-10 rounded-md bg-w3-canvas dark:bg-w3-slateDeep border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas hover:bg-w3-example dark:hover:bg-w3-slate focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          <button type="button" data-switch-mode="social" class="flex items-center gap-2.5 text-start group focus-visible:ring-2 focus-visible:ring-w3-green rounded-md px-1.5 py-1 micro-transition">
            <span class="inline-flex items-center justify-center px-2.5 py-1 rounded bg-w3-green text-white font-display font-bold text-sm tracking-tight shadow-sm">w3</span>
            <div>
              <span class="font-display font-bold text-base sm:text-lg text-w3-ink dark:text-w3-canvas block leading-none">
                <span class="lang-en">${escHtml(UI_DICTIONARY.en.brandTitle)}</span>
                <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.brandTitle)}</span>
              </span>
              <span class="hidden sm:block text-xs text-w3-muted dark:text-zinc-300 mt-0.5">
                <span class="lang-en">${escHtml(UI_DICTIONARY.en.brandSub)}</span>
                <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.brandSub)}</span>
              </span>
            </div>
          </button>
        </div>

        <div class="relative flex-1 max-w-xs xl:max-w-md hidden md:block">
          <span class="absolute inset-y-0 start-3 flex items-center pointer-events-none text-w3-muted dark:text-zinc-400">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
              <circle cx="11" cy="11" r="8" />
              <path stroke-linecap="round" d="m21 21-4.3-4.3" />
            </svg>
          </span>
          <input id="global-top-search" type="search" aria-label="Search 60 skills, commands, or lessons" placeholder="${escHtml(UI_DICTIONARY.en.searchPlaceholder)}" class="w-full ps-10 pe-4 py-1.5 text-xs sm:text-sm rounded-full bg-w3-canvas dark:bg-w3-slateDeep border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas focus-visible:ring-2 focus-visible:ring-w3-green focus-visible:outline-none micro-transition" />
        </div>

        <nav aria-label="Learning Mode Switcher" class="hidden lg:flex items-center gap-1 bg-w3-example dark:bg-w3-slateDeep p-1 rounded-lg border border-w3-line dark:border-zinc-700">
          <button type="button" data-switch-mode="social" class="mode-tab-btn px-3 py-1.5 rounded-md text-xs font-semibold bg-w3-green text-white focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.modeSocial)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.modeSocial)}</span>
          </button>
          <button type="button" data-switch-mode="reader" class="mode-tab-btn px-3 py-1.5 rounded-md text-xs font-semibold text-w3-ink dark:text-zinc-100 hover:bg-w3-card dark:hover:bg-w3-slate focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.modeReader)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.modeReader)}</span>
          </button>
          <button type="button" data-switch-mode="simulator" class="mode-tab-btn px-3 py-1.5 rounded-md text-xs font-semibold text-w3-ink dark:text-zinc-100 hover:bg-w3-card dark:hover:bg-w3-slate focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.modeSimulator)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.modeSimulator)}</span>
          </button>
          <button type="button" data-switch-mode="reference" class="mode-tab-btn px-3 py-1.5 rounded-md text-xs font-semibold text-w3-ink dark:text-zinc-100 hover:bg-w3-card dark:hover:bg-w3-slate focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.modeReference)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.modeReference)}</span>
          </button>
        </nav>

        <div class="flex items-center gap-2 shrink-0">
          <button type="button" id="top-xp-badge-btn" aria-label="View learning progress and XP" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-w3-mint text-w3-greenDark font-mono text-xs font-bold border border-w3-green/40 focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" />
            </svg>
            <span id="header-xp-count">0 XP</span>
          </button>

          <button type="button" id="theme-toggle-btn" aria-label="Toggle Light and Dark Theme" class="inline-flex items-center justify-center w-9 h-9 rounded-md bg-w3-canvas dark:bg-w3-slateDeep border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-zinc-100 hover:border-w3-green focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </button>

          <button type="button" id="lang-toggle-btn" aria-label="Switch between English LTR and Arabic RTL" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-w3-slate text-white dark:bg-w3-green dark:text-white text-xs font-semibold hover:bg-w3-greenHover focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.langToggleLabel)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.langToggleLabel)}</span>
          </button>
        </div>
      </div>

      <div id="subtopnav" class="bg-w3-slate text-zinc-100 h-10 border-t border-zinc-700 overflow-x-auto w3-scrollbar">
        <div class="max-w-7xl mx-auto px-3 sm:px-6 h-full flex items-center gap-1.5 whitespace-nowrap text-xs font-mono">
          <button type="button" data-switch-mode="social" class="subnav-pill px-3 py-1 rounded bg-w3-green text-white font-semibold focus-visible:ring-2 focus-visible:ring-white micro-transition">
            <span class="lang-en">FEED HUB</span>
            <span class="lang-ar">الموجز الرئيسي</span>
          </button>
          ${ribbonCombosHtml}
          <button type="button" data-switch-mode="simulator" class="subnav-pill px-3 py-1 rounded bg-w3-yellow text-w3-ink font-semibold hover:bg-w3-mint focus-visible:ring-2 focus-visible:ring-white micro-transition">
            <span class="lang-en">Try it Yourself »</span>
            <span class="lang-ar">جربها بنفسك »</span>
          </button>
          <button type="button" data-switch-mode="reference" class="subnav-pill px-3 py-1 rounded bg-w3-mint text-w3-greenDark font-semibold hover:bg-w3-green hover:text-white focus-visible:ring-2 focus-visible:ring-white micro-transition">
            <span class="lang-en">60-Skill Dict »</span>
            <span class="lang-ar">قاموس 60 مهارة »</span>
          </button>
        </div>
      </div>
    </header>

    <div id="mobile-drawer-backdrop" class="fixed inset-0 z-40 bg-w3-slate/75 hidden lg:hidden"></div>

    <div class="max-w-7xl w-full mx-auto flex-1 flex items-start gap-0 lg:gap-5 px-0 sm:px-4 lg:px-6 pt-0 lg:pt-6">
      <aside id="w3-sidebar" aria-label="W3Schools Curriculum Chapters" class="fixed lg:sticky top-0 lg:top-28 start-0 z-50 lg:z-20 w-72 lg:w-64 shrink-0 h-dvh lg:h-[calc(100dvh-7.5rem)] overflow-y-auto w3-scrollbar bg-w3-example dark:bg-w3-slate border-e lg:border border-w3-line dark:border-zinc-700 lg:rounded-xl p-4 -translate-x-full rtl:translate-x-full lg:translate-x-0 rtl:lg:translate-x-0 micro-transition">
        <div class="flex items-center justify-between pb-3 mb-3 border-b border-w3-line dark:border-zinc-700">
          <div>
            <span class="text-xs font-mono text-w3-greenDark dark:text-w3-mint font-bold block">
              <span class="lang-en">W3SCHOOLS CURRICULUM</span>
              <span class="lang-ar">منهج W3SCHOOLS التفاعلي</span>
            </span>
            <h2 class="font-display font-bold text-sm text-w3-ink dark:text-w3-canvas mt-1 mb-0">
              <span class="lang-en">4 Tracks • ${allLessons.length} Chapters</span>
              <span class="lang-ar">4 مسارات • ${allLessons.length} درساً</span>
            </h2>
          </div>
          <button type="button" id="mobile-drawer-close-btn" aria-label="Close Chapter Menu" class="lg:hidden inline-flex items-center justify-center w-8 h-8 rounded-md bg-w3-card dark:bg-w3-slateDeep text-w3-ink dark:text-w3-canvas focus-visible:ring-2 focus-visible:ring-w3-green">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="space-y-4">
          ${sidebarTracksHtml}
        </div>
      </aside>

      <main id="center-stage" class="flex-1 min-w-0 px-3 sm:px-0 pb-12">
        <div id="view-social" class="space-y-6">
          <section class="rounded-none sm:rounded-xl bg-w3-slate text-white p-5 sm:p-8 border-b sm:border border-zinc-700 shadow-sm">
            <div class="max-w-3xl">
              <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-w3-mint text-w3-greenDark text-xs font-bold">
                <span class="lang-en">${escHtml(UI_DICTIONARY.en.heroEyebrow)}</span>
                <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.heroEyebrow)}</span>
              </span>
              <h1 class="font-display font-bold text-2xl sm:text-4xl text-white mt-4 mb-3 leading-tight">
                <span class="lang-en">${escHtml(UI_DICTIONARY.en.heroTitle)}</span>
                <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.heroTitle)}</span>
              </h1>
              <p class="text-sm sm:text-base text-zinc-200 leading-relaxed mb-6">
                <span class="lang-en">${escHtml(UI_DICTIONARY.en.heroSubtitle)}</span>
                <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.heroSubtitle)}</span>
              </p>

              <div class="flex flex-wrap items-center gap-3">
                <button type="button" data-open-lesson="ch-intro" class="px-5 py-2.5 rounded-full bg-w3-green hover:bg-w3-greenHover text-white font-semibold text-sm focus-visible:ring-2 focus-visible:ring-white micro-transition">
                  <span class="lang-en">${escHtml(UI_DICTIONARY.en.heroCtaPrimary)}</span>
                  <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.heroCtaPrimary)}</span>
                </button>
                <button type="button" data-switch-mode="simulator" class="px-5 py-2.5 rounded-full bg-w3-yellow text-w3-ink font-bold text-sm hover:bg-w3-mint focus-visible:ring-2 focus-visible:ring-white micro-transition">
                  <span class="lang-en">${escHtml(UI_DICTIONARY.en.heroCtaSecondary)}</span>
                  <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.heroCtaSecondary)}</span>
                </button>
                <button type="button" data-switch-mode="reference" class="px-4 py-2.5 rounded-full bg-w3-slateDeep border border-zinc-600 text-zinc-100 font-semibold text-sm hover:border-w3-mint focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                  <span class="lang-en">${escHtml(UI_DICTIONARY.en.modeReference)} »</span>
                  <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.modeReference)} »</span>
                </button>
              </div>

              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-5 border-t border-zinc-700">
                <div>
                  <span class="font-display font-bold text-lg text-w3-mint block">${skillsRegistry.totalSkills}</span>
                  <span class="text-xs text-zinc-300">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.statsSkills)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.statsSkills)}</span>
                  </span>
                </div>
                <div>
                  <span class="font-display font-bold text-lg text-w3-yellow block">11</span>
                  <span class="text-xs text-zinc-300">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.statsCombos)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.statsCombos)}</span>
                  </span>
                </div>
                <div>
                  <span class="font-display font-bold text-lg text-w3-pink block">${skillsRegistry.totalMcpServers}</span>
                  <span class="text-xs text-zinc-300">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.statsMcps)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.statsMcps)}</span>
                  </span>
                </div>
                <div>
                  <span class="font-display font-bold text-lg text-w3-green block">36</span>
                  <span class="text-xs text-zinc-300">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.statsGuards)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.statsGuards)}</span>
                  </span>
                </div>
              </div>
            </div>
          </section>

          <section aria-label="60-Second Story Reels" class="bg-w3-card dark:bg-w3-slate rounded-xl border border-w3-line dark:border-zinc-700 p-4 shadow-sm">
            <div class="flex items-center justify-between mb-3">
              <h2 class="font-display font-bold text-sm text-w3-ink dark:text-w3-canvas mt-1 mb-0">
                <span class="lang-en">${escHtml(UI_DICTIONARY.en.storiesHeading)}</span>
                <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.storiesHeading)}</span>
              </h2>
              <span class="text-xs font-mono font-semibold text-w3-greenDark dark:text-w3-mint">6 Reels</span>
            </div>
            <div class="flex items-stretch gap-3 overflow-x-auto w3-scrollbar pb-2">
              ${storyRingsHtml}
            </div>
          </section>

          <section aria-label="Situation Combos Grid" class="bg-w3-card dark:bg-w3-slate rounded-xl border border-w3-line dark:border-zinc-700 p-4 sm:p-6 shadow-sm">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
              <div>
                <h2 class="font-display font-bold text-lg text-w3-ink dark:text-w3-canvas mt-1 mb-1">
                  <span class="lang-en">${escHtml(UI_DICTIONARY.en.combosSectionTitle)}</span>
                  <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.combosSectionTitle)}</span>
                </h2>
                <p class="text-xs text-w3-muted dark:text-zinc-300">
                  <span class="lang-en">${escHtml(UI_DICTIONARY.en.combosSectionSub)}</span>
                  <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.combosSectionSub)}</span>
                </p>
              </div>
            </div>

            <div id="combos-card-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-[repeat(3,minmax(0,1fr))] gap-4">
              ${combosGridHtml}
            </div>

            <div class="mt-4 text-center">
              <button type="button" id="toggle-combos-grid-btn" data-expanded="false" class="px-5 py-2 rounded-full bg-w3-example dark:bg-w3-slateDeep border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas font-semibold text-xs hover:bg-w3-green hover:text-white focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                <span id="toggle-combos-label-en" class="lang-en">${escHtml(UI_DICTIONARY.en.showMoreCombos)}</span>
                <span id="toggle-combos-label-ar" class="lang-ar">${escHtml(UI_DICTIONARY.ar.showMoreCombos)}</span>
              </button>
            </div>
          </section>

          <div class="flex items-center gap-2 overflow-x-auto w3-scrollbar py-1">
            <button type="button" data-feed-filter="all" class="feed-filter-btn px-3.5 py-1.5 rounded-full text-xs font-semibold bg-w3-green text-white focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
              <span class="lang-en">${escHtml(UI_DICTIONARY.en.feedFilterAll)}</span>
              <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.feedFilterAll)}</span>
            </button>
            <button type="button" data-feed-filter="start" class="feed-filter-btn px-3.5 py-1.5 rounded-full text-xs font-semibold bg-w3-card dark:bg-w3-slate border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas hover:border-w3-green focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
              <span class="lang-en">${escHtml(UI_DICTIONARY.en.feedFilterStart)}</span>
              <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.feedFilterStart)}</span>
            </button>
            <button type="button" data-feed-filter="features" class="feed-filter-btn px-3.5 py-1.5 rounded-full text-xs font-semibold bg-w3-card dark:bg-w3-slate border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas hover:border-w3-green focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
              <span class="lang-en">${escHtml(UI_DICTIONARY.en.feedFilterFeatures)}</span>
              <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.feedFilterFeatures)}</span>
            </button>
            <button type="button" data-feed-filter="bugs" class="feed-filter-btn px-3.5 py-1.5 rounded-full text-xs font-semibold bg-w3-card dark:bg-w3-slate border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas hover:border-w3-green focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
              <span class="lang-en">${escHtml(UI_DICTIONARY.en.feedFilterBugs)}</span>
              <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.feedFilterBugs)}</span>
            </button>
            <button type="button" data-feed-filter="cms" class="feed-filter-btn px-3.5 py-1.5 rounded-full text-xs font-semibold bg-w3-card dark:bg-w3-slate border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas hover:border-w3-green focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
              <span class="lang-en">${escHtml(UI_DICTIONARY.en.feedFilterCms)}</span>
              <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.feedFilterCms)}</span>
            </button>
            <button type="button" data-feed-filter="ops" class="feed-filter-btn px-3.5 py-1.5 rounded-full text-xs font-semibold bg-w3-card dark:bg-w3-slate border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas hover:border-w3-green focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
              <span class="lang-en">${escHtml(UI_DICTIONARY.en.feedFilterOps)}</span>
              <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.feedFilterOps)}</span>
            </button>
          </div>

          <div id="social-feed-stream" class="space-y-6">
            ${feedCardsHtml}
          </div>
        </div>

        <div id="view-reader" class="hidden space-y-6">
          <div class="bg-w3-card dark:bg-w3-slate rounded-xl border border-w3-line dark:border-zinc-700 p-4 sm:p-8 shadow-sm">
            <div class="flex items-center justify-between gap-2 pb-4 border-b border-w3-line dark:border-zinc-700">
              <button type="button" id="reader-prev-btn" class="px-4 py-2 rounded-md bg-w3-green hover:bg-w3-greenHover text-white font-semibold text-xs sm:text-sm focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                <span class="lang-en">${escHtml(UI_DICTIONARY.en.prevLessonBtn)}</span>
                <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.prevLessonBtn)}</span>
              </button>
              <span id="reader-lesson-badge" class="px-3 py-1 rounded-full bg-w3-mint text-w3-greenDark font-mono text-xs font-bold">Lesson 1.1</span>
              <button type="button" id="reader-next-btn" class="px-4 py-2 rounded-md bg-w3-green hover:bg-w3-greenHover text-white font-semibold text-xs sm:text-sm focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                <span class="lang-en">${escHtml(UI_DICTIONARY.en.nextLessonBtn)}</span>
                <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.nextLessonBtn)}</span>
              </button>
            </div>

            <h2 id="reader-title" class="font-display font-bold text-2xl sm:text-3xl text-w3-ink dark:text-w3-canvas mt-6 mb-3">${escHtml(allLessons[0].titleEn)}</h2>
            <p id="reader-summary" class="text-sm sm:text-base text-w3-muted dark:text-zinc-200 leading-relaxed mb-6">${escHtml(allLessons[0].summaryEn)}</p>
            <ul id="reader-bullets" class="space-y-3 mb-6 text-sm text-w3-ink dark:text-zinc-100 bg-w3-canvas dark:bg-w3-slateDeep p-4 rounded-lg border border-w3-line dark:border-zinc-700"></ul>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div class="rounded-lg bg-w3-pink/30 dark:bg-w3-slateDeep border border-red-300 dark:border-w3-pink/50 p-4">
                <h3 class="font-mono text-xs font-bold text-red-800 dark:text-w3-pink mt-1 mb-2">
                  <span class="lang-en">${escHtml(UI_DICTIONARY.en.beforeLabel)}</span>
                  <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.beforeLabel)}</span>
                </h3>
                <p id="reader-before" class="text-xs sm:text-sm text-w3-ink dark:text-zinc-200 whitespace-pre-line"></p>
              </div>
              <div class="rounded-lg bg-w3-mint/50 dark:bg-w3-slateDeep border border-w3-green p-4">
                <h3 class="font-mono text-xs font-bold text-w3-greenDark dark:text-w3-mint mt-1 mb-2">
                  <span class="lang-en">${escHtml(UI_DICTIONARY.en.afterLabel)}</span>
                  <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.afterLabel)}</span>
                </h3>
                <p id="reader-after" class="text-xs sm:text-sm text-w3-ink dark:text-zinc-200 whitespace-pre-line"></p>
              </div>
            </div>

            <div class="rounded-xl bg-w3-example dark:bg-w3-slateDeep p-5 border border-w3-line dark:border-zinc-700 mb-6">
              <div class="flex items-center justify-between gap-2 mb-3">
                <h3 id="reader-example-title" class="font-display font-bold text-base text-w3-ink dark:text-w3-canvas mt-1 mb-0">Example</h3>
                <code id="reader-command-pill" class="px-2.5 py-1 rounded bg-w3-slate text-w3-mint font-mono text-xs font-semibold">/smart-feature</code>
              </div>
              <div id="reader-code-box" class="bg-w3-card dark:bg-w3-slate border-s-4 border-w3-green p-4 rounded font-mono text-xs sm:text-sm text-w3-ink dark:text-zinc-100 overflow-x-auto mb-4"></div>
              <div class="flex flex-wrap items-center gap-3">
                <button type="button" id="reader-try-btn" class="px-5 py-2.5 rounded-md bg-w3-green hover:bg-w3-greenHover text-white font-semibold text-xs sm:text-sm focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                  <span class="lang-en">${escHtml(UI_DICTIONARY.en.tryItBtn)}</span>
                  <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.tryItBtn)}</span>
                </button>
                <button type="button" id="reader-complete-btn" class="px-4 py-2.5 rounded-md bg-w3-yellow text-w3-ink font-bold text-xs sm:text-sm hover:bg-w3-mint focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                  <span class="lang-en">${escHtml(UI_DICTIONARY.en.markCompleteBtn)}</span>
                  <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.markCompleteBtn)}</span>
                </button>
              </div>
            </div>

            <div class="rounded-xl bg-w3-slate text-white p-5 sm:p-6 border border-zinc-700">
              <div class="flex items-center justify-between gap-2 mb-3">
                <h3 class="font-display font-bold text-lg text-w3-yellow mt-1 mb-0">
                  <span class="lang-en">${escHtml(UI_DICTIONARY.en.quizHeader)}</span>
                  <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.quizHeader)}</span>
                </h3>
                <span class="px-2.5 py-0.5 rounded bg-w3-green text-white font-mono text-xs font-semibold">Quiz</span>
              </div>
              <p id="reader-quiz-question" class="text-sm sm:text-base text-zinc-100 mb-4"></p>
              <div id="reader-quiz-options" class="space-y-2 mb-4"></div>
              <div id="reader-quiz-feedback" class="hidden p-3 rounded-lg text-xs sm:text-sm font-medium mb-3"></div>
            </div>
          </div>
        </div>

        <div id="view-simulator" class="hidden space-y-6">
          <section class="bg-w3-card dark:bg-w3-slate rounded-xl border border-w3-line dark:border-zinc-700 p-4 sm:p-6 shadow-sm">
            <div class="border-b border-w3-line dark:border-zinc-700 pb-4 mb-5">
              <h2 class="font-display font-bold text-xl sm:text-2xl text-w3-ink dark:text-w3-canvas mt-1 mb-1">
                <span class="lang-en">${escHtml(UI_DICTIONARY.en.simHeaderTitle)}</span>
                <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.simHeaderTitle)}</span>
              </h2>
              <p class="text-xs sm:text-sm text-w3-muted dark:text-zinc-300">
                <span class="lang-en">${escHtml(UI_DICTIONARY.en.simHeaderSub)}</span>
                <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.simHeaderSub)}</span>
              </p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div class="rounded-xl bg-w3-example dark:bg-w3-slateDeep p-4 border border-w3-line dark:border-zinc-700 space-y-4">
                <div>
                  <label for="sim-command-select" class="block text-xs font-bold text-w3-ink dark:text-w3-canvas mb-1.5">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.simSelectCombo)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.simSelectCombo)}</span>
                  </label>
                  <select id="sim-command-select" aria-label="Select Agent OS Slash Command" class="w-full px-3 py-2 rounded-lg bg-w3-card dark:bg-w3-slate border border-w3-line dark:border-zinc-700 text-xs sm:text-sm font-mono text-w3-ink dark:text-w3-canvas focus-visible:ring-2 focus-visible:ring-w3-green focus-visible:outline-none">
                    ${simComboOptionsHtml}
                  </select>
                </div>

                <div>
                  <label for="sim-stack-select" class="block text-xs font-bold text-w3-ink dark:text-w3-canvas mb-1.5">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.simSelectStack)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.simSelectStack)}</span>
                  </label>
                  <select id="sim-stack-select" aria-label="Select Target Tech Stack" class="w-full px-3 py-2 rounded-lg bg-w3-card dark:bg-w3-slate border border-w3-line dark:border-zinc-700 text-xs sm:text-sm text-w3-ink dark:text-w3-canvas focus-visible:ring-2 focus-visible:ring-w3-green focus-visible:outline-none">
                    ${simStackOptionsHtml}
                  </select>
                </div>

                <div>
                  <label for="sim-prompt-textarea" class="block text-xs font-bold text-w3-ink dark:text-w3-canvas mb-1.5">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.simEditPrompt)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.simEditPrompt)}</span>
                  </label>
                  <textarea id="sim-prompt-textarea" aria-label="Edit your Agent OS prompt" rows="4" class="w-full p-3 rounded-lg bg-w3-card dark:bg-w3-slate border-s-4 border-w3-green border border-w3-line dark:border-zinc-700 font-mono text-xs sm:text-sm text-w3-ink dark:text-w3-canvas focus-visible:ring-2 focus-visible:ring-w3-green focus-visible:outline-none">${escHtml(SITUATION_COMBOS_CARDS[0].samplePromptEn)}</textarea>
                </div>

                <div class="flex flex-wrap items-center gap-3 pt-1">
                  <button type="button" id="sim-run-btn" class="px-5 py-2.5 rounded-md bg-w3-green hover:bg-w3-greenHover text-white font-semibold text-xs sm:text-sm focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.simRunBtn)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.simRunBtn)}</span>
                  </button>
                  <button type="button" id="sim-copy-btn" class="px-4 py-2.5 rounded-md bg-w3-slate text-white border border-zinc-600 font-semibold text-xs sm:text-sm hover:bg-w3-green focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.simCopyPromptBtn)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.simCopyPromptBtn)}</span>
                  </button>
                </div>
              </div>

              <div class="rounded-xl bg-w3-slate text-zinc-100 p-4 sm:p-5 border border-zinc-700 space-y-4">
                <div class="flex items-center justify-between border-b border-zinc-700 pb-3">
                  <span class="font-display font-bold text-sm text-w3-mint">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.simOutputHeader)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.simOutputHeader)}</span>
                  </span>
                  <span id="sim-active-stack-badge" class="px-2.5 py-0.5 rounded bg-w3-green text-white font-mono text-xs font-semibold">Astro 4</span>
                </div>

                <div class="rounded-lg bg-w3-slateDeep p-3.5 border-s-4 border-w3-pink">
                  <h3 class="font-display font-bold text-xs text-w3-pink mt-1 mb-2">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.simStage1Title)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.simStage1Title)}</span>
                  </h3>
                  <ul id="sim-stage1-list" class="space-y-1.5 text-xs text-zinc-200 font-mono"></ul>
                </div>

                <div class="rounded-lg bg-w3-slateDeep p-3.5 border-s-4 border-w3-yellow">
                  <h3 class="font-display font-bold text-xs text-w3-yellow mt-1 mb-2">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.simStage2Title)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.simStage2Title)}</span>
                  </h3>
                  <div id="sim-stage2-pills" class="flex flex-wrap gap-1.5"></div>
                </div>

                <div class="rounded-lg bg-w3-slateDeep p-3.5 border-s-4 border-w3-green">
                  <h3 class="font-display font-bold text-xs text-w3-mint mt-1 mb-2">
                    <span class="lang-en">${escHtml(UI_DICTIONARY.en.simStage3Title)}</span>
                    <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.simStage3Title)}</span>
                  </h3>
                  <ul id="sim-stage3-files" class="space-y-1.5 text-xs text-zinc-200 font-mono"></ul>
                </div>
              </div>
            </div>
          </section>
        </div>

        <div id="view-reference" class="hidden space-y-6">
          <section class="bg-w3-card dark:bg-w3-slate rounded-xl border border-w3-line dark:border-zinc-700 p-4 sm:p-6 shadow-sm">
            <div class="mb-4">
              <h2 class="font-display font-bold text-xl sm:text-2xl text-w3-ink dark:text-w3-canvas mt-1 mb-1">
                <span class="lang-en">${escHtml(UI_DICTIONARY.en.refHeaderTitle)}</span>
                <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.refHeaderTitle)}</span>
              </h2>
              <p class="text-xs sm:text-sm text-w3-muted dark:text-zinc-300">
                <span class="lang-en">${escHtml(UI_DICTIONARY.en.refHeaderSub)}</span>
                <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.refHeaderSub)}</span>
              </p>
            </div>

            <div class="flex flex-col md:flex-row items-stretch md:items-center gap-3 mb-4">
              <div class="relative flex-1 min-w-0">
                <span class="absolute inset-y-0 start-3 flex items-center pointer-events-none text-w3-muted dark:text-zinc-400">
                  <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                    <circle cx="11" cy="11" r="8" />
                    <path stroke-linecap="round" d="m21 21-4.3-4.3" />
                  </svg>
                </span>
                <input id="skill-dict-search" type="search" aria-label="Search 60 skills in dictionary table" placeholder="${escHtml(UI_DICTIONARY.en.refSearchPlaceholder)}" class="w-full ps-10 pe-4 py-2 text-xs sm:text-sm rounded-lg bg-w3-canvas dark:bg-w3-slateDeep border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas focus-visible:ring-2 focus-visible:ring-w3-green focus-visible:outline-none" />
              </div>

              <div class="w-full md:w-72 shrink-0">
                <select id="skill-dict-cat-select" aria-label="Filter skills by category" class="w-full px-3 py-2 text-xs sm:text-sm rounded-lg bg-w3-canvas dark:bg-w3-slateDeep border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas focus-visible:ring-2 focus-visible:ring-w3-green focus-visible:outline-none">
                  <option value="ALL">All Categories (${skillsList.length} Skills)</option>
                  ${catOptionsHtml}
                </select>
              </div>
            </div>

            <div class="w-full overflow-x-auto rounded-lg border border-w3-line dark:border-zinc-700">
              <table class="w-full text-start border-collapse text-xs sm:text-sm">
                <thead class="bg-w3-slate text-white">
                  <tr>
                    <th class="py-3 px-3 text-start font-display font-semibold">
                      <span class="lang-en">${escHtml(UI_DICTIONARY.en.refColCommand)}</span>
                      <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.refColCommand)}</span>
                    </th>
                    <th class="py-3 px-3 text-start font-display font-semibold hidden sm:table-cell">
                      <span class="lang-en">${escHtml(UI_DICTIONARY.en.refColCategory)}</span>
                      <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.refColCategory)}</span>
                    </th>
                    <th class="py-3 px-3 text-start font-display font-semibold">
                      <span class="lang-en">${escHtml(UI_DICTIONARY.en.refColPhase)}</span>
                      <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.refColPhase)}</span>
                    </th>
                    <th class="py-3 px-3 text-start font-display font-semibold">
                      <span class="lang-en">${escHtml(UI_DICTIONARY.en.refColSummary)}</span>
                      <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.refColSummary)}</span>
                    </th>
                    <th class="py-3 px-3 text-end font-display font-semibold">
                      <span class="lang-en">${escHtml(UI_DICTIONARY.en.refColAction)}</span>
                      <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.refColAction)}</span>
                    </th>
                  </tr>
                </thead>
                <tbody id="skills-table-body" class="divide-y divide-w3-line dark:divide-zinc-700 bg-w3-card dark:bg-w3-slate">
                  ${skillsRowsHtml}
                </tbody>
              </table>
            </div>

            <div class="mt-4 text-center">
              <button type="button" id="toggle-skills-table-btn" data-expanded="false" class="px-5 py-2 rounded-full bg-w3-example dark:bg-w3-slateDeep border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas font-semibold text-xs hover:bg-w3-green hover:text-white focus-visible:ring-2 focus-visible:ring-w3-green micro-transition">
                <span id="toggle-skills-label-en" class="lang-en">${escHtml(UI_DICTIONARY.en.refShowMoreRows)}</span>
                <span id="toggle-skills-label-ar" class="lang-ar">${escHtml(UI_DICTIONARY.ar.refShowMoreRows)}</span>
              </button>
            </div>
          </section>

          <section class="bg-w3-card dark:bg-w3-slate rounded-xl border border-w3-line dark:border-zinc-700 p-4 sm:p-6 shadow-sm">
            <h3 class="font-display font-bold text-lg text-w3-ink dark:text-w3-canvas mt-1 mb-3">
              <span class="lang-en">18 Configured MCP Servers Reference</span>
              <span class="lang-ar">مرجع خوادم MCP الـ 18 المربوطة بالنظام</span>
            </h3>
            <div class="w-full overflow-x-auto rounded-lg border border-w3-line dark:border-zinc-700">
              <table class="w-full text-start border-collapse text-xs sm:text-sm">
                <thead class="bg-w3-slate text-white">
                  <tr>
                    <th class="py-2.5 px-3 text-start font-display font-semibold">MCP Server</th>
                    <th class="py-2.5 px-3 text-start font-display font-semibold">Phase</th>
                    <th class="py-2.5 px-3 text-start font-display font-semibold">Summary (2-4 Words)</th>
                    <th class="py-2.5 px-3 text-end font-display font-semibold">Action</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-w3-line dark:divide-zinc-700 bg-w3-card dark:bg-w3-slate">
                  ${mcpRowsHtml}
                </tbody>
              </table>
            </div>
          </section>
        </div>
      </main>

      <aside id="end-xp-rail" aria-label="My Learning XP and Saved Toolkit" class="hidden xl:block sticky top-28 w-72 shrink-0 space-y-4">
        <div class="rounded-xl bg-w3-card dark:bg-w3-slate border border-w3-line dark:border-zinc-700 p-4 shadow-sm">
          <div class="flex items-center justify-between gap-2 mb-2">
            <h2 class="font-display font-bold text-sm text-w3-ink dark:text-w3-canvas mt-1 mb-0">
              <span class="lang-en">${escHtml(UI_DICTIONARY.en.rightRailProgressTitle)}</span>
              <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.rightRailProgressTitle)}</span>
            </h2>
            <span id="rail-xp-pill" class="px-2 py-0.5 rounded-full bg-w3-green text-white font-mono text-xs font-bold">0 XP</span>
          </div>
          <p id="rail-rank-label" class="text-xs font-semibold text-w3-greenDark dark:text-w3-mint mb-3">${escHtml(UI_DICTIONARY.en.rank0)}</p>
          <div class="w-full h-2.5 rounded-full bg-w3-example dark:bg-w3-slateDeep overflow-hidden mb-2">
            <div id="rail-xp-bar" class="h-full bg-w3-green w-0 micro-transition"></div>
          </div>
          <div class="flex items-center justify-between text-xs text-w3-muted dark:text-zinc-300">
            <span>
              <span class="lang-en">${escHtml(UI_DICTIONARY.en.rightRailCompletedLabel)}</span>
              <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.rightRailCompletedLabel)}</span>
            </span>
            <span id="rail-completed-count" class="font-mono font-semibold">0 / ${allLessons.length}</span>
          </div>
        </div>

        <div class="rounded-xl bg-w3-card dark:bg-w3-slate border border-w3-line dark:border-zinc-700 p-4 shadow-sm">
          <h3 class="font-display font-bold text-sm text-w3-ink dark:text-w3-canvas mt-1 mb-2">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.rightRailToolkitTitle)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.rightRailToolkitTitle)}</span>
          </h3>
          <div id="rail-saved-list" class="space-y-2 text-xs text-w3-muted dark:text-zinc-300">
            <p class="lang-en">${escHtml(UI_DICTIONARY.en.rightRailToolkitEmpty)}</p>
            <p class="lang-ar">${escHtml(UI_DICTIONARY.ar.rightRailToolkitEmpty)}</p>
          </div>
        </div>

        <div class="rounded-xl bg-w3-slate text-zinc-100 p-4 border border-zinc-700">
          <h3 class="font-display font-bold text-xs text-w3-yellow mt-1 mb-1">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.rightRailUpdateBoxTitle)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.rightRailUpdateBoxTitle)}</span>
          </h3>
          <p class="text-xs text-zinc-300 mb-2">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.rightRailUpdateBoxDesc)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.rightRailUpdateBoxDesc)}</span>
          </p>
          <div class="bg-w3-slateDeep p-2.5 rounded border-s-4 border-w3-green font-mono text-xs text-w3-mint overflow-x-auto mb-2">python scripts/agent_os.py handbook-sync --build</div>
          <button type="button" data-copy-text-en="python scripts/agent_os.py handbook-sync --build" data-copy-text-ar="python scripts/agent_os.py handbook-sync --build" class="w-full py-1.5 rounded bg-w3-green hover:bg-w3-greenHover text-white font-semibold text-xs focus-visible:ring-2 focus-visible:ring-white micro-transition">
            <span class="lang-en">Copy Sync Command</span>
            <span class="lang-ar">نسخ أمر المزامنة</span>
          </button>
        </div>
      </aside>
    </div>

    <nav aria-label="Mobile Bottom Navigation" class="fixed bottom-0 inset-x-0 z-40 lg:hidden bg-w3-card dark:bg-w3-slate border-t border-w3-line dark:border-zinc-700 h-14 px-2 flex items-center justify-around">
      <button type="button" data-switch-mode="social" class="flex flex-col items-center justify-center py-1 px-2 text-xs font-semibold text-w3-greenDark dark:text-w3-mint focus-visible:ring-2 focus-visible:ring-w3-green rounded">
        <svg class="w-4 h-4 mb-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
        <span class="lang-en">${escHtml(UI_DICTIONARY.en.mobileNavFeed)}</span>
        <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.mobileNavFeed)}</span>
      </button>

      <button type="button" id="mobile-bottom-chapters-btn" class="flex flex-col items-center justify-center py-1 px-2 text-xs font-semibold text-w3-ink dark:text-zinc-200 focus-visible:ring-2 focus-visible:ring-w3-green rounded">
        <svg class="w-4 h-4 mb-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
        <span class="lang-en">${escHtml(UI_DICTIONARY.en.mobileNavLessons)}</span>
        <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.mobileNavLessons)}</span>
      </button>

      <button type="button" data-switch-mode="simulator" class="flex flex-col items-center justify-center py-1.5 px-3 rounded-full bg-w3-green text-white text-xs font-semibold focus-visible:ring-2 focus-visible:ring-w3-green">
        <span class="lang-en">${escHtml(UI_DICTIONARY.en.mobileNavTryIt)} »</span>
        <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.mobileNavTryIt)} »</span>
      </button>

      <button type="button" data-switch-mode="reference" class="flex flex-col items-center justify-center py-1 px-2 text-xs font-semibold text-w3-ink dark:text-zinc-200 focus-visible:ring-2 focus-visible:ring-w3-green rounded">
        <svg class="w-4 h-4 mb-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
        </svg>
        <span class="lang-en">${escHtml(UI_DICTIONARY.en.mobileNavRef)}</span>
        <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.mobileNavRef)}</span>
      </button>

      <button type="button" id="mobile-bottom-xp-btn" class="flex flex-col items-center justify-center py-1 px-2 text-xs font-semibold text-w3-ink dark:text-zinc-200 focus-visible:ring-2 focus-visible:ring-w3-green rounded">
        <svg class="w-4 h-4 mb-0.5 text-w3-green" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" />
        </svg>
        <span class="lang-en">${escHtml(UI_DICTIONARY.en.mobileNavProfile)}</span>
        <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.mobileNavProfile)}</span>
      </button>
    </nav>

    <div id="story-player-modal" role="dialog" aria-modal="true" aria-labelledby="story-modal-title" class="fixed inset-0 z-50 hidden bg-w3-slate/90 flex items-center justify-center p-4">
      <div class="w-full max-w-lg rounded-2xl bg-w3-slateDeep text-white border border-zinc-700 p-5 sm:p-6 shadow-xl">
        <div id="story-progress-bars" class="flex items-center gap-1.5 mb-4"></div>
        <div class="flex items-center justify-between gap-2 mb-3">
          <span id="story-step-badge" class="px-2.5 py-0.5 rounded-full bg-w3-mint text-w3-greenDark font-mono text-xs font-bold">Slide 1</span>
          <button type="button" id="story-close-btn" class="px-3 py-1 rounded bg-w3-slate border border-zinc-600 text-xs font-semibold text-zinc-100 hover:bg-w3-green hover:text-white focus-visible:ring-2 focus-visible:ring-w3-green">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.modalCloseBtn)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.modalCloseBtn)}</span>
          </button>
        </div>
        <h3 id="story-modal-title" class="font-display font-bold text-xl text-white mt-2 mb-2">Story Title</h3>
        <p id="story-modal-body" class="text-sm text-zinc-200 leading-relaxed mb-4"></p>
        <pre id="story-modal-code" class="hidden rounded-lg bg-w3-slate border-s-4 border-w3-green p-3 font-mono text-xs text-w3-mint overflow-x-auto mb-4"></pre>
        <div class="flex items-center justify-between gap-3 pt-3 border-t border-zinc-700">
          <button type="button" id="story-prev-slide-btn" class="px-4 py-2 rounded-md bg-w3-slate border border-zinc-600 text-xs font-semibold text-white hover:border-w3-green focus-visible:ring-2 focus-visible:ring-w3-green">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.prevLessonBtn)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.prevLessonBtn)}</span>
          </button>
          <button type="button" id="story-next-slide-btn" class="px-5 py-2 rounded-md bg-w3-green hover:bg-w3-greenHover text-xs font-semibold text-white focus-visible:ring-2 focus-visible:ring-white">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.nextLessonBtn)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.nextLessonBtn)}</span>
          </button>
        </div>
      </div>
    </div>

    <div id="details-modal" role="dialog" aria-modal="true" aria-labelledby="details-modal-title" class="fixed inset-0 z-50 hidden bg-w3-slate/80 flex items-center justify-center p-4">
      <div class="w-full max-w-lg rounded-2xl bg-w3-card dark:bg-w3-slate text-w3-ink dark:text-w3-canvas border border-w3-line dark:border-zinc-700 p-5 sm:p-6 shadow-xl">
        <div class="flex items-center justify-between gap-2 pb-3 border-b border-w3-line dark:border-zinc-700">
          <code id="details-modal-cmd" class="px-2.5 py-1 rounded bg-w3-slate text-w3-mint font-mono text-xs font-bold">/skill</code>
          <button type="button" id="details-modal-close-btn" class="px-3 py-1 rounded bg-w3-example dark:bg-w3-slateDeep border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas text-xs font-semibold hover:bg-w3-green hover:text-white focus-visible:ring-2 focus-visible:ring-w3-green">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.modalCloseBtn)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.modalCloseBtn)}</span>
          </button>
        </div>
        <h3 id="details-modal-title" class="font-display font-bold text-lg mt-4 mb-2">Skill Details</h3>
        <p id="details-modal-meta" class="text-xs font-mono text-w3-greenDark dark:text-w3-mint mb-3"></p>
        <p id="details-modal-desc" class="text-sm text-w3-muted dark:text-zinc-200 leading-relaxed mb-5"></p>
        <div class="flex flex-wrap items-center gap-3 pt-3 border-t border-w3-line dark:border-zinc-700">
          <button type="button" id="details-modal-try-btn" class="px-4 py-2 rounded-md bg-w3-green hover:bg-w3-greenHover text-white font-semibold text-xs focus-visible:ring-2 focus-visible:ring-w3-green">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.modalTryInSimBtn)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.modalTryInSimBtn)}</span>
          </button>
          <button type="button" id="details-modal-copy-btn" class="px-4 py-2 rounded-md bg-w3-example dark:bg-w3-slateDeep border border-w3-line dark:border-zinc-700 text-w3-ink dark:text-w3-canvas font-semibold text-xs hover:border-w3-green focus-visible:ring-2 focus-visible:ring-w3-green">
            <span class="lang-en">${escHtml(UI_DICTIONARY.en.modalCopyCmdBtn)}</span>
            <span class="lang-ar">${escHtml(UI_DICTIONARY.ar.modalCopyCmdBtn)}</span>
          </button>
        </div>
      </div>
    </div>

    <div id="w3-toast" role="status" aria-live="polite" class="fixed bottom-16 lg:bottom-6 end-4 z-50 hidden px-4 py-3 rounded-xl bg-w3-slate text-white border-s-4 border-w3-green shadow-lg text-xs sm:text-sm font-semibold">Notification</div>

    <script>
      const clientPayload = ${JSON.stringify(clientPayload)};
      ${inlineScriptBody}
    </script>
  </body>
</html>
`;
}

fs.mkdirSync(DIST_DIR, { recursive: true });
const outPath = path.join(DIST_DIR, 'index.html');
fs.writeFileSync(outPath, renderStaticHtml(), 'utf-8');
fs.writeFileSync(path.join(DIST_DIR, '_redirects'), '/*  /index.html  200\n', 'utf-8');
fs.writeFileSync(path.join(DIST_DIR, '.nojekyll'), '', 'utf-8');
console.log('[OK] Built Astro W3Schools x Social Learning Platform -> dist/index.html');


