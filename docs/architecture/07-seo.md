# 07 — SEO

## Índice
- [Resumo](#resumo)
- [Metadata por página](#metadata-por-página)
- [Open Graph e Twitter Cards](#open-graph-e-twitter-cards)
- [Schema.org (dados estruturados)](#schemaorg-dados-estruturados)
- [robots.txt](#robotstxt)
- [Sitemap](#sitemap)
- [Canonical e hreflang](#canonical-e-hreflang)
- [Hierarquia de headings](#hierarquia-de-headings)
- [Breadcrumbs](#breadcrumbs)
- [Busca interna e SEO](#busca-interna-e-seo)
- [Lacunas identificadas](#lacunas-identificadas)

## Resumo

O site tem uma estratégia de SEO **deliberada e relativamente sofisticada** para um site estático: meta tags completas por página, dados estruturados ricos (7+ tipos de Schema.org), sitemap gerado automaticamente a cada push, e robots.txt que explicitamente libera bots de LLM (GPTBot, ClaudeBot, OAI-SearchBot). Isso é coerente com o comentário em `public/robots.txt:2`: `# MPA Architecture - SEO Jurídico Nacional`.

## Metadata por página

Cada página inclui, tipicamente (referência: `public/index.html:4-29`):
- `<meta charset>`, `<meta viewport>`, `<meta name="robots" content="index, follow">`
- `<title>` e `<meta name="description">`, ambos com atributo `data-i18n` quando a página participa do i18n client-side (permitindo que o índice de busca e o crawler vejam a versão PT, enquanto o usuário vê a versão traduzida em runtime)
- `<link rel="canonical">` absoluto
- `<link rel="alternate" hreflang="...">` (ver seção dedicada)
- Favicon SVG (`/assets/illustrations/favicon.svg`)

## Open Graph e Twitter Cards

Presentes de forma consistente nas páginas principais (`public/index.html:15-28`, `public/diagnostico.html:13-24`):
- `og:type`, `og:site_name`, `og:locale`, `og:title`, `og:description`, `og:url`, `og:image`
- `twitter:card=summary_large_image`, `twitter:site=@tuteladigitalbr`, `twitter:title`, `twitter:description`, `twitter:image`

**Achado crítico**: todas as páginas referenciam `https://tuteladigital.com.br/assets/images/og-image.jpg` como imagem de compartilhamento, mas **esse arquivo não existe no repositório** — `public/assets/images/` contém apenas 3 SVGs de bandeiras (`flags/br.svg`, `us.svg`, `es.svg`); não há nenhum `.jpg` em `public/assets/images/` nem em `public/assets/illustrations/`. Isso significa que **qualquer compartilhamento do site no WhatsApp, LinkedIn, Twitter/X ou Facebook não exibe imagem de preview**, a menos que o arquivo exista apenas no servidor de produção fora do controle de versão (necessita validação). Ver [12-technical-debt.md](12-technical-debt.md).

## Schema.org (dados estruturados)

Levantamento de todos os valores `@type` usados em blocos `application/ld+json` em todo o site:

| Tipo | Ocorrências | Onde |
| --- | --- | --- |
| `ListItem` | 58 | Dentro de `BreadcrumbList` |
| `Organization` | 34 | Rodapé (todas as páginas) + reforço em algumas páginas |
| `BreadcrumbList` | 20 | Artigos de insights e páginas internas |
| `Article` | 11 | Artigos do blog |
| `WebPage` / `CollectionPage` / `AboutPage` | 10+2+1 | Páginas institucionais e de listagem |
| `Question` / `Answer` (dentro de `FAQPage`) | 9+9 | Artigos com seção de perguntas frequentes |
| `FAQPage` | 4 | Artigos selecionados |
| `ImageObject` | 7 | Ilustração de artigos |
| `TechArticle` | 3 | Artigos técnicos (ex.: cadeia de custódia) |
| `TermsOfService` / `PrivacyPolicy` | 2+1 | Páginas legais |
| `LegalService` | 2 | Home e artigos-chave |
| `PostalAddress`, `Country`, `Thing` | 1 cada | Complementos de endereço/área de atuação |

A organização (`Organization`, `@id: https://tuteladigital.com.br/#organization`) é definida uma única vez no rodapé (`public/partials/footer.html:66-89`) e referenciada por `@id` em outros blocos (ex.: `LegalService.provider` em `public/index.html:83`) — um padrão correto de reuso de entidade JSON-LD.

O sistema de i18n também atualiza esse dado estruturado em runtime: `i18n.js:206-214` (`updateSchemaLanguage`) reescreve o campo `inLanguage` de todo `script[type="application/ld+json"]` da página ao trocar de idioma.

## robots.txt

```
User-agent: *
Allow: /
User-agent: GPTBot / OAI-SearchBot / ChatGPT-User / ClaudeBot / Claude-SearchBot / Claude-User
Allow: /
Sitemap: https://tuteladigital.com.br/sitemap.xml
```

Não há `Disallow` para nenhum caminho — nenhuma área do site é bloqueada de indexação, incluindo páginas de redirecionamento e partials (embora partials não sejam acessíveis via URL própria de qualquer forma).

## Sitemap

`public/sitemap.xml` é **gerado automaticamente**, não editado manualmente — `.github/workflows/sitemap.yml` reconstrói o arquivo do zero a cada push em `main`, `homolog` ou `feature/legal-structure`, iterando sobre `git ls-files` (ou seja, o sitemap reflete o que está commitado, não o que está no disco local). Regras de prioridade/frequência (`sitemap.yml:56-66`):

| Página | `priority` | `changefreq` |
| --- | --- | --- |
| Home (`/`) | 1.0 | weekly |
| `/insights/` (índice) | 0.8 | weekly |
| Artigos de `/insights/*` | 0.7 | monthly (padrão) |
| `/legal/*` | 0.5 | yearly |
| Demais páginas | 0.8 | monthly |

`<lastmod>` vem de `git log -1 --format=%cd` do próprio arquivo — reflete a data do último commit que tocou aquele HTML, não uma data de "revisão editorial" manual.

## Canonical e hreflang

Ver detalhamento em [04-routing.md](04-routing.md#internacionalização-de-url). Resumo do achado principal: o cluster de 4 páginas do pillar de Ativos Digitais (`/ativos-digitais/`, `/pt/ativos-digitais/`, `/en/digital-assets/`, `/es/activos-digitales/`) implementa hreflang recíproco em 3 das 4 páginas — a página apontada como `x-default` (`/ativos-digitais/index.html`) **não** declara, ela mesma, o bloco `hreflang` que a aponta de volta para as outras 3 variantes (confirmado por busca `grep hreflang` sem resultado nesse arquivo). Isso quebra a reciprocidade que o Google recomenda para clusters de hreflang.

## Hierarquia de headings

Cada página analisada usa um único `<h1>` (ex.: `public/index.html:106`, `public/diagnostico.html`), seguido de `<h2>` por seção e `<h3>` para subitens de card — hierarquia consistente e sem saltos observados nas páginas analisadas. Os elementos `<h1>`-`<h4>` herdam a família `--font-display` globalmente (`foundation/base.css:24-53`).

## Breadcrumbs

Existe um dado estruturado `BreadcrumbList` em 20 páginas, mas o breadcrumb **visual correspondente é intencionalmente ocultado da tela para todos os usuários**, não apenas de leitores de tela. O CSS documenta essa decisão explicitamente:

```css
/* =====================================
   BREADCRUMB VISUAL HIDDEN (SEO ONLY)
===================================== */
.breadcrumb,
nav[aria-label="breadcrumb"] {
  position: absolute;
  left: -9999px;
  top: auto;
  width: 1px;
  height: 1px;
  overflow: hidden;
}
```
(`public/assets/css/layout/layout.css:38-51`)

Esse padrão CSS (`width:1px; height:1px; overflow:hidden` combinado com posicionamento fora da tela) é a técnica clássica de "visually-hidden": o elemento continua no DOM e é acessível a leitores de tela e crawlers, mas nenhum usuário sighted vê uma trilha de navegação (breadcrumb) na interface. Ou seja, o breadcrumb existe apenas para SEO (rich snippet do Google) e acessibilidade assistiva — não como recurso de navegação visual.

## Busca interna e SEO

O índice de busca (`assets/search-index.json`) é gerado a partir do HTML rastreado, e explicitamente **exclui páginas de redirecionamento** (detecção de `meta http-equiv="refresh"` ou `window.location.replace`, `.github/ci/build_search_index.py:124-133`) para não expor ao usuário um resultado que só empurra para outro lugar. Esse mesmo índice também extrai o texto de `header.html`/`footer.html` separadamente (já que o HTML bruto de cada página nunca contém esse conteúdo, resolvido apenas em runtime via SSI) para permitir busca por termos que só aparecem no menu ou rodapé.

## Lacunas identificadas

| Lacuna | Severidade | Detalhe |
| --- | --- | --- |
| `og-image.jpg` referenciado mas ausente do repositório | Alta | Ver acima; afeta preview de compartilhamento em todas as 35 páginas |
| Página `x-default` sem cluster `hreflang` recíproco | Média | Ver [04-routing.md](04-routing.md) |
| `lastmod` do sitemap reflete commit, não revisão editorial | Baixa | Pode subestimar ou superestimar "frescor" percebido pelo Google |
| Ausência de `sitemap` de imagens ou de vídeo | Baixa | Não identificado no projeto — não há necessidade aparente, dado o baixo volume de mídia rica |

## Documentos relacionados
- [04-routing.md](04-routing.md) — URLs, canonical, redirecionamentos.
- [12-technical-debt.md](12-technical-debt.md) — priorização dos achados acima.
