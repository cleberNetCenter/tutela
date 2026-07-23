# 14 — Glossário

## Índice
- [Termos jurídicos e de negócio](#termos-jurídicos-e-de-negócio)
- [Termos técnicos do projeto](#termos-técnicos-do-projeto)
- [Siglas](#siglas)

## Termos jurídicos e de negócio

| Termo | Significado no contexto do projeto |
| --- | --- |
| **Ativos digitais** | Bens ou direitos existentes em formato digital (documentos, contratos, credenciais, dados) que são objeto de custódia, proteção e planejamento sucessório pela Tutela Digital®. Cluster de conteúdo principal do site (`/ativos-digitais/`). |
| **Prova digital** | Evidência eletrônica usada para demonstrar fatos em processos judiciais, administrativos ou arbitrais. Segundo tema principal do site (`/insights/prova-digital/`, `/legal/*`). |
| **Cadeia de custódia** | Registro documentado e ininterrupto de todas as operações realizadas sobre uma evidência digital, com identificação temporal e autoral de cada evento — usado para sustentar a admissibilidade da prova em juízo. Citado como um dos "selos de confiança" no rodapé (`footer.html:57`). |
| **Custódia probatória / preservação probatória** | Ato técnico-jurídico de preservar um ativo/evidência digital de forma estruturada, com integridade verificável, antes ou durante um litígio. |
| **Fase pré-litigiosa** | Momento anterior à existência formal de um litígio, em que a Tutela Digital® afirma atuar prioritariamente, preservando prova antes que ela seja necessária em juízo (`public/index.html:169-171`). |
| **e-Notariado** | Plataforma nacional de atos notariais eletrônicos (tabelionatos brasileiros), citada como parceiro de integração para "formalização notarial" e "fé pública" (`public/index.html:191-193`). |
| **Fé pública** | Atributo jurídico conferido por agente público (ex.: tabelião) que confere presunção de veracidade a um ato ou documento. |
| **Admissibilidade jurídica / probatória** | Capacidade de uma evidência ser aceita e considerada válida por um juízo, tribunal administrativo ou câmara arbitral. |
| **Produção antecipada de prova** | Instituto processual que permite produzir e assegurar uma prova antes do momento processual ordinário, tema de um dos artigos do blog. |
| **Herança digital / sucessão digital** | Planejamento e regras jurídicas para transmissão de ativos digitais após o falecimento do titular — tema de página dedicada (`/ativos-digitais/heranca-digital/`). |
| **Art. 369 do CPC** | Dispositivo do Código de Processo Civil brasileiro citado no site (`public/index.html:352`) como fundamento legal de que "as partes têm o direito de empregar todos os meios legais... para provar a verdade dos fatos". |
| **LGPD** | Lei Geral de Proteção de Dados (Lei 13.709/2018) — citada como referência de conformidade regulatória (`public/index.html:211`). |
| **ICP-Brasil** | Infraestrutura de Chaves Públicas Brasileira — sistema nacional de certificação digital, citado como um dos "selos de confiança" no rodapé. |
| **PCT/IB2026/055458** | Número de um Pedido Internacional de Patente (Patent Cooperation Treaty) citado no rodapé como "patent pending" da tecnologia da empresa (`footer.html:60`). |

## Termos técnicos do projeto

| Termo | Significado |
| --- | --- |
| **MPA (Multi-Page Application)** | Arquitetura em que cada URL corresponde a um documento HTML completo, entregue pelo servidor — o padrão adotado por este site, em oposição a uma SPA. Citado explicitamente em `public/robots.txt:2` e `public/assets/js/navigation.js:2`. |
| **SSI (Server Side Includes)** | Diretiva processada pelo servidor web (`<!--#include virtual="..." -->`) que injeta o conteúdo de um arquivo dentro de outro no momento da requisição. Usado para compartilhar header, footer e scripts entre as 35 páginas do site sem duplicar HTML. |
| **Pillar page** | Página "guarda-chuva" de um tema amplo (aqui, Ativos Digitais), que se ramifica em subpáginas mais específicas — termo usado nos próprios nomes de arquivo (`ativos-digitais-pillar-main.html`). |
| **Design tokens** | Variáveis de design (cor, espaçamento, tipografia) centralizadas como custom properties CSS (`--color-*`, `--space-*`) em `foundation/tokens.css`. |
| **`--ad-*` / `--ux-*`** | Dois namespaces de tokens específicos do cluster de páginas de Ativos Digitais — ver [06-design-system.md](06-design-system.md) para a distinção (e a fragmentação) entre eles. |
| **`data-i18n`** | Atributo HTML customizado usado pelo motor de internacionalização (`i18n.js`) para marcar qual chave de tradução um elemento deve exibir. Variantes: `data-i18n-html`, `data-i18n-aria`, `data-i18n-placeholder`, `data-i18n-alt`, `data-i18n-title`. |
| **Search index (`search-index.json`)** | Arquivo JSON gerado por CI (`build_search_index.py`) contendo título, descrição e corpo de texto de cada página, consumido pelo widget de busca client-side. |
| **`#buscar=`** | Fragmento de URL usado pelo widget de busca para indicar, na página de destino, qual termo deve ser destacado e rolado até a visão (`search.js`). |
| **Legal page (`body.legal-page`)** | Classe aplicada ao `<body>` das páginas do cluster `/legal/*`, usada por `i18n.js` (para restringir tradução apenas à interface) e por `legal-animations.js` (para ativar scroll-reveal). |
| **Reveal (`.reveal`)** | Classe usada em seções que devem animar de opacidade 0 para 1 ao entrarem na viewport, via `IntersectionObserver`. |
| **Cache-busting** | Técnica de adicionar uma query string (`?v=7`) à URL de um asset para forçar o navegador a buscar uma nova versão em vez de usar o cache. |

## Siglas

| Sigla | Significado |
| --- | --- |
| CPC | Código de Processo Civil |
| LGPD | Lei Geral de Proteção de Dados |
| ICP-Brasil | Infraestrutura de Chaves Públicas Brasileira |
| PCT | Patent Cooperation Treaty (Tratado de Cooperação em Matéria de Patentes) |
| MPA | Multi-Page Application |
| SPA | Single Page Application |
| SSI | Server Side Includes |
| SEO | Search Engine Optimization |
| CI/CD | Continuous Integration / Continuous Deployment |
| TLS | Transport Layer Security |
| CSP | Content Security Policy |
| CORS | Cross-Origin Resource Sharing |
| WCAG | Web Content Accessibility Guidelines |
| i18n | Internationalization (Internacionalização) |
| GA4 | Google Analytics 4 |
| GTM | Google Tag Manager |

## Documentos relacionados
- [01-overview.md](01-overview.md) — contexto de negócio completo.
- [06-design-system.md](06-design-system.md) — detalhamento dos tokens citados aqui.
