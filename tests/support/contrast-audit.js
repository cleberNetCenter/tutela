#!/usr/bin/env node
// Auditoria de contraste WCAG AA (ARQ-604) — recalcula a razão de contraste
// de cada par texto/fundo ou UI/fundo listado em PAIRS. Nenhuma dependência
// externa: implementa a fórmula de luminância relativa do próprio WCAG 2.x
// (https://www.w3.org/TR/WCAG21/#dfn-relative-luminance).
//
// Uso: node tests/support/contrast-audit.js
//
// Valores de fg/bg abaixo refletem os tokens JÁ CORRIGIDOS nesta sprint
// (--primitive-neutral-600 e --text-3, ver tokens.css/styles-header-final.css/
// footer.css). Para reproduzir os números PRÉ-correção citados na entrega da
// Sprint 10, usar #4f7c6b (--color-text-muted) e #4a7258 (--text-3).

/** @param {string} hex */
function hexToRgb(hex) {
  const clean = hex.replace("#", "");
  const full =
    clean.length === 3
      ? clean.split("").map((c) => c + c).join("")
      : clean;
  const num = parseInt(full, 16);
  return { r: (num >> 16) & 255, g: (num >> 8) & 255, b: num & 255 };
}

/** Achata rgba sobre um fundo sólido (para texto translúcido sobre gradiente/cor). */
function flatten(fgHex, alpha, bgHex) {
  const fg = hexToRgb(fgHex);
  const bg = hexToRgb(bgHex);
  const blend = (a, b) => Math.round(a * alpha + b * (1 - alpha));
  return { r: blend(fg.r, bg.r), g: blend(fg.g, bg.g), b: blend(fg.b, bg.b) };
}

function relativeLuminance({ r, g, b }) {
  const toLinear = (c) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  };
  const [R, G, B] = [toLinear(r), toLinear(g), toLinear(b)];
  return 0.2126 * R + 0.7152 * G + 0.0722 * B;
}

/** Aceita hex string ("#rrggbb") ou objeto {r,g,b} já resolvido (ex. saída de flatten()). */
function toRgb(color) {
  return typeof color === "string" ? hexToRgb(color) : color;
}

function contrastRatio(colorA, colorB) {
  const lumA = relativeLuminance(toRgb(colorA));
  const lumB = relativeLuminance(toRgb(colorB));
  const lighter = Math.max(lumA, lumB);
  const darker = Math.min(lumA, lumB);
  return (lighter + 0.05) / (darker + 0.05);
}

function verdict(ratio, context) {
  const threshold = context === "large" || context === "ui" ? 3 : 4.5;
  return { ratio: Math.round(ratio * 100) / 100, threshold, pass: ratio >= threshold };
}

// context: "normal" (texto <18pt / <14pt bold, precisa 4.5:1)
//          "large"  (texto >=18pt ou >=14pt bold, precisa 3:1)
//          "ui"     (componente de UI/gráfico, precisa 3:1)
const PAIRS = [
  // ---- Tokens semânticos globais (foundation/tokens.css) ----
  { group: "Global", label: "--color-text-base sobre --color-surface-light", fg: "#0f3a2a", bg: "#f2f7f5", context: "normal" },
  { group: "Global", label: "--color-text-strong sobre --color-surface-light", fg: "#0b241b", bg: "#f2f7f5", context: "normal" },
  { group: "Global", label: "--color-text-muted sobre --color-surface-light", fg: "#4a7464", bg: "#f2f7f5", context: "normal" },
  { group: "Global", label: "--color-text-muted sobre branco (cards.css)", fg: "#4a7464", bg: "#ffffff", context: "normal" },
  { group: "Global", label: "--color-text-inverse sobre --color-surface-brand (botão .btn-secondary / skip-link)", fg: "#e6f0eb", bg: "#0c2418", context: "normal" },
  { group: "Global", label: "botão primário: --color-text-inverse sobre --color-green-900 (buttons.css)", fg: "#e6f0eb", bg: "#0f3a2a", context: "normal" },
  { group: "Global", label: "botão secundário: --color-text-inverse sobre --color-green-950 (buttons.css)", fg: "#e6f0eb", bg: "#0b241b", context: "normal" },

  // ---- Extensão Ativos Digitais (--ad-*, assets-digital.css) ----
  { group: "--ad-*", label: "--ad-text-body sobre --ad-bg-page", fg: "#0f3a2a", bg: "#edf4ed", context: "normal" },
  { group: "--ad-*", label: "--ad-text-heading sobre --ad-bg-page", fg: "#0a2218", bg: "#edf4ed", context: "normal" },
  { group: "--ad-*", label: "--ad-text-muted sobre --ad-bg-page", fg: "#3d6b50", bg: "#edf4ed", context: "normal" },
  { group: "--ad-*", label: "--ad-text-muted sobre --ad-bg-white", fg: "#3d6b50", bg: "#ffffff", context: "normal" },
  { group: "--ad-*", label: "--ad-accent-gold (destaque stat-card) sobre --ad-bg-white — componente UI", fg: "#b08a57", bg: "#ffffff", context: "ui" },
  { group: "--ad-*", label: "branco sobre --ad-brand-dark (CTA/hero escuro)", fg: "#ffffff", bg: "#0d2b1a", context: "large" },

  // ---- Extensão --ad-pillar-* (tokens.css) — consolidada nesta sprint a partir
  // do --ux-* que vivia inline em ativos-digitais-pillar-styles.html (ARQ-301).
  // Valores idênticos aos pré-migração; grupo/labels só refletem os novos nomes.
  { group: "--ad-pillar-*", label: "--ad-pillar-ink sobre --ad-pillar-bg", fg: "#18342b", bg: "#f4f7f2", context: "normal" },
  { group: "--ad-pillar-*", label: "--ad-pillar-ink sobre cartão branco (stat-card/whitepaper)", fg: "#18342b", bg: "#ffffff", context: "normal" },
  { group: "--ad-pillar-*", label: "--ad-pillar-ink-soft (corpo de texto) sobre cartão branco", fg: "#51645d", bg: "#ffffff", context: "normal" },
  { group: "--ad-pillar-*", label: "--ad-pillar-brand-2 (h2/h3/card-icon) sobre cartão branco", fg: "#184d43", bg: "#ffffff", context: "normal" },
  { group: "--ad-pillar-*", label: "--ad-danger (card-danger h3/icon) sobre --ad-danger-bg (quase-branco)", fg: "#9f3627", bg: "#fff2ef", context: "normal" },
  { group: "--ad-pillar-*", label: "--ad-pillar-brand (checklist icon) sobre rgba(15,74,54,0.10) — componente UI", fg: "#0f4a36", bg: flatten("#0f4a36", 0.10, "#ffffff"), context: "ui" },
  { group: "--ad-pillar-*", label: "branco (#eff6f1) sobre header .assets-page (rgba(10,42,33,0.72) sobre gradiente escuro)", fg: "#eff6f1", bg: flatten("#0a2a21", 0.72, "#0d3429"), context: "normal" },
  { group: "--ad-pillar-*", label: "#f4f8f4 (page-header h1) sobre gradiente #163f35→#18453a — pior caso", fg: "#f4f8f4", bg: "#18453a", context: "large" },
  { group: "--ad-pillar-*", label: ".btn-primary #18453a sobre #f4f6f3 (CTA claro)", fg: "#18453a", bg: "#f4f6f3", context: "normal" },

  // ---- Header / Navegação / Dropdowns / Menu mobile (styles-header-final.css) — Sprint 7-9 ----
  { group: "Header/Nav", label: "skip-link: --color-text-inverse sobre --color-surface-brand (ARQ-601)", fg: "#e6f0eb", bg: "#0c2418", context: "normal" },
  { group: "Header/Nav", label: ".nav-link (repouso): --text-2 sobre .header --bg", fg: "#7faa8a", bg: "#0c2418", context: "normal" },
  { group: "Header/Nav", label: ".nav-link:hover / [aria-expanded=true]: --text-1 sobre --bg", fg: "#e8f0ea", bg: "#0c2418", context: "normal" },
  { group: "Header/Nav", label: ".dropdown-menu li a (repouso): --text-2 sobre --bg-drop (ARQ-603)", fg: "#7faa8a", bg: "#0e2c1e", context: "normal" },
  { group: "Header/Nav", label: ".dropdown-menu li a:hover: --text-1 sobre --green-mid (ARQ-603)", fg: "#e8f0ea", bg: "#1a4a2e", context: "normal" },
  { group: "Header/Nav", label: ".mobile-menu-btn span (barras do hamburguer): --text-2 sobre --bg — componente UI (ARQ-603)", fg: "#7faa8a", bg: "#0c2418", context: "ui" },
  { group: "Header/Nav", label: "menu mobile aberto (.nav.open): .dropdown-menu --bg-deep, texto --text-1 (ARQ-603)", fg: "#e8f0ea", bg: "#091d13", context: "normal" },
  { group: "Header/Nav", label: ".header-cta: #071a0e sobre --accent (botão CTA do header)", fg: "#071a0e", bg: "#3ecf72", context: "normal" },
  { group: "Header/Nav", label: ".logo sup (marca ™): --text-3 sobre --bg", fg: "#6e8e79", bg: "#0c2418", context: "normal" },
  { group: "Header/Nav", label: ".nav-toggle::after (seta, repouso): --text-3 sobre --bg — componente UI", fg: "#6e8e79", bg: "#0c2418", context: "ui" },

  // ---- Rodapé (sections/footer.css, mesmos tokens --bg/--text-*) ----
  { group: "Footer", label: "footer --text-3 (copyright/links secundários) sobre --bg", fg: "#6e8e79", bg: "#0c2418", context: "normal" },

  // ---- Páginas legais (legal-shared.css) ----
  // Correção de metodologia (Sprint 15, ARQ-606): texto é translúcido, fundo é opaco —
  // o par correto compara a cor EFETIVA do texto (branco composto sobre o stop via
  // flatten()) contra o próprio stop, não contra branco nominal. A versão anterior
  // fazia contrastRatio("#ffffff", flatten(...)), comparando o branco nominal contra
  // a cor composta — resultado sistematicamente mais pessimista (ex.: reportava 1.64:1
  // e 2.00:1 para alpha 0.68, quando o valor correto era 3.94:1 e 8.18:1). Não altera
  // o veredito (ambos falhavam), mas altera a magnitude usada para calibrar a correção.
  { group: "Legal", label: "hero subtitle rgba(255,255,255,0.78) [ARQ-606] — texto efetivo vs pior stop do gradiente (green-700)", fg: flatten("#ffffff", 0.78, "#1b6b4d"), bg: "#1b6b4d", context: "normal" },
  { group: "Legal", label: "hero subtitle rgba(255,255,255,0.78) [ARQ-606] — texto efetivo vs melhor stop do gradiente (green-950)", fg: flatten("#ffffff", 0.78, "#0b241b"), bg: "#0b241b", context: "normal" },
  { group: "Legal", label: "--color-text-muted sobre --color-surface-muted (seção clara)", fg: "#4a7464", bg: "#e6f0eb", context: "normal" },
  { group: "Legal", label: "--color-text-base sobre --color-surface-muted", fg: "#0f3a2a", bg: "#e6f0eb", context: "normal" },
  { group: "Legal", label: "--primitive-green-700 (link/label) sobre branco", fg: "#1b6b4d", bg: "#ffffff", context: "normal" },
];

let failCount = 0;
console.log(
  "Grupo".padEnd(12),
  "Par".padEnd(78),
  "Contexto".padEnd(9),
  "Razão".padEnd(7),
  "Mínimo",
  "Resultado"
);
for (const p of PAIRS) {
  const ratio = contrastRatio(p.fg, p.bg);
  const v = verdict(ratio, p.context);
  if (!v.pass) failCount++;
  console.log(
    p.group.padEnd(12),
    p.label.padEnd(78),
    p.context.padEnd(9),
    String(v.ratio).padEnd(7),
    `${v.threshold}:1`,
    v.pass ? "PASSA" : "FALHA"
  );
}
console.log(`\n${PAIRS.length} pares avaliados, ${failCount} falha(s).`);

module.exports = { hexToRgb, flatten, relativeLuminance, contrastRatio, verdict };
