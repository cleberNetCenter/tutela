const fs = require('fs');
const path = require('path');

const root = '/home/cleber/tutela-legal';
const publicDir = path.join(root, 'public');
const langDir = path.join(publicDir, 'assets', 'lang');

const locales = {
  pt: {
    path: path.join(publicDir, 'pt', 'ativos-digitais', 'index.html'),
    url: 'https://tuteladigital.com.br/pt/ativos-digitais/',
    lang: 'pt-BR',
    title: 'Gestão de Ativos Digitais no Direito Contemporâneo',
    description: 'Custódia, sucessão e governança de ativos digitais com base jurídica e integridade verificável',
    breadcrumbHome: 'Início',
    breadcrumbCurrent: 'Ativos Digitais'
  },
  en: {
    path: path.join(publicDir, 'en', 'digital-assets', 'index.html'),
    url: 'https://tuteladigital.com.br/en/digital-assets/',
    lang: 'en',
    title: 'Digital Asset Management in Contemporary Law',
    description: 'Custody, succession, and governance of digital assets with legal basis and verifiable integrity',
    breadcrumbHome: 'Home',
    breadcrumbCurrent: 'Digital Assets'
  },
  es: {
    path: path.join(publicDir, 'es', 'activos-digitales', 'index.html'),
    url: 'https://tuteladigital.com.br/es/activos-digitales/',
    lang: 'es',
    title: 'Gestión de Activos Digitales en el Derecho Contemporáneo',
    description: 'Custodia, sucesión y gobernanza de activos digitales con base jurídica e integridad verificable',
    breadcrumbHome: 'Inicio',
    breadcrumbCurrent: 'Activos Digitales'
  }
};

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function paragraphList(items) {
  return items.map((item) => `      <p>\n        ${escapeHtml(item)}\n      </p>`).join('\n');
}

function buildPage(lang, locale, pillar) {
  const preloadedTranslations = JSON.stringify(readJson(path.join(langDir, `${lang}.json`)))
    .replace(/</g, '\\u003c')
    .replace(/>/g, '\\u003e')
    .replace(/&/g, '\\u0026');
  return `<!DOCTYPE html>
<html lang="${locale.lang}">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${escapeHtml(locale.title)}</title>
  <meta name="description" content="${escapeHtml(locale.description)}" />
  <link rel="canonical" href="${locale.url}" />
  <link rel="alternate" hreflang="pt-BR" href="${locales.pt.url}" />
  <link rel="alternate" hreflang="en" href="${locales.en.url}" />
  <link rel="alternate" hreflang="es" href="${locales.es.url}" />
  <link rel="alternate" hreflang="x-default" href="https://tuteladigital.com.br/ativos-digitais/" />
  <link rel="icon" type="image/svg+xml" href="/assets/illustrations/favicon.svg" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="${locale.url}" />
  <meta property="og:title" content="${escapeHtml(locale.title)}" />
  <meta property="og:description" content="${escapeHtml(locale.description)}" />
  <meta property="og:site_name" content="Tutela Digital®" />
  <meta property="twitter:card" content="summary" />
  <meta property="twitter:url" content="${locale.url}" />
  <meta property="twitter:title" content="${escapeHtml(locale.title)}" />
  <meta property="twitter:description" content="${escapeHtml(locale.description)}" />
  <link rel="stylesheet" href="/assets/css/main.css?v=7">
  <link rel="stylesheet" href="/assets/css/styles-header-final.css?v=7">
  <link rel="stylesheet" href="/assets/css/dropdown-menu.css?v=202602190108">
  <script>
    window.__PAGE_LANG__ = '${lang}';
    localStorage.setItem('tutela_lang', '${lang}');
    document.documentElement.lang = '${locale.lang}';
    window.__I18N_PRELOADED_LANG__ = '${lang}';
    window.__I18N_PRELOADED__ = ${preloadedTranslations};
  </script>
</head>

<body class="exec-compact">
  <div class="app">
    <!--#include virtual="/partials/header.html" -->
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <ol>
        <li><a href="/">${escapeHtml(locale.breadcrumbHome)}</a></li>
        <li aria-current="page">${escapeHtml(locale.breadcrumbCurrent)}</li>
      </ol>
    </nav>

    <main class="main main--hero-top legal-page">
      <section class="page-header page-header--legal">
        <div class="page-header-inner">
          <h1>${escapeHtml(pillar.hero.title)}</h1>
          <p class="page-header-subtitle">
            ${escapeHtml(pillar.hero.subtitle)}
          </p>
          <p class="insight-pillar-link">
            ${escapeHtml(pillar.hero.cta)}
          </p>
        </div>
      </section>

      <section class="legal-section-wrapper">
        <div class="whitepaper-container">
          <h2>${escapeHtml(pillar.problem.title)}</h2>
          <p>
            ${escapeHtml(pillar.problem.text)}
          </p>

          <h2>${escapeHtml(pillar.scale.title)}</h2>
${paragraphList(pillar.scale.items)}

          <h2>${escapeHtml(pillar.taxonomy.title)}</h2>
          <h3>${escapeHtml(pillar.taxonomy.categoryLabel)}</h3>
${paragraphList(pillar.taxonomy.items)}
          <h3>${escapeHtml(pillar.taxonomy.criticalLabel)}</h3>
          <p>
            ${escapeHtml(pillar.taxonomy.note)}
          </p>

          <h2>${escapeHtml(pillar.regulatory.title)}</h2>
${paragraphList(pillar.regulatory.items)}

          <h2>${escapeHtml(pillar.risks.title)}</h2>
${paragraphList(pillar.risks.items)}

          <h2>${escapeHtml(pillar.succession.title)}</h2>
          <p>
            ${escapeHtml(pillar.succession.text)}
          </p>
          <h3>${escapeHtml(pillar.succession.recommendedLabel)}</h3>
${paragraphList(pillar.succession.steps)}

          <h2>${escapeHtml(pillar.compliance.title)}</h2>
${paragraphList(pillar.compliance.items)}

          <h2>${escapeHtml(pillar.infrastructure.title)}</h2>
          <p>
            ${escapeHtml(pillar.infrastructure.text)}
          </p>

          <h2>${escapeHtml(pillar.implementation.title)}</h2>
${paragraphList(pillar.implementation.items)}

          <h2>${escapeHtml(pillar.outcomes.title)}</h2>
${paragraphList(pillar.outcomes.items)}

          <h2>${escapeHtml(pillar.usecases.title)}</h2>
${paragraphList(pillar.usecases.items)}

          <h2>${escapeHtml(pillar.context.title)}</h2>
          <p>
            ${escapeHtml(pillar.context.text)}
          </p>
        </div>
      </section>

      <section class="insight-cta-block">
        <div class="insight-cta-inner">
          <h2>${escapeHtml(pillar.ctaFinal.text)}</h2>
          <p>
            ${escapeHtml(pillar.ctaFinal.cta)}
          </p>
        </div>
      </section>
    </main>

    <!--#include virtual="/partials/footer.html" -->
    <!--#include virtual="/partials/scripts.html" -->
  </div>
</body>

</html>
`;
}

function renderPage(lang) {
  const locale = locales[lang];
  if (!locale) {
    throw new Error(`Unsupported language: ${lang}`);
  }

  const data = readJson(path.join(langDir, `${lang}.json`));
  const pillar = data.ativosDigitais.pillar;

  return buildPage(lang, locale, pillar);
}

for (const [lang, locale] of Object.entries(locales)) {
  fs.mkdirSync(path.dirname(locale.path), { recursive: true });
  fs.writeFileSync(locale.path, renderPage(lang), 'utf8');
  console.log(`Generated ${locale.path}`);
}
