# Documentação de Arquitetura — Tutela Digital®

Esta pasta documenta, com base exclusivamente em evidências encontradas no repositório `cleberNetCenter/tutela` (branch `homolog`, snapshot de 2026-07-23), a arquitetura técnica, o design system, o SEO, a performance, a segurança e a dívida técnica do site institucional da Tutela Digital®.

Este trabalho é **somente leitura**: nenhum arquivo de aplicação foi alterado. A única mudança produzida é a criação desta pasta.

## Como ler esta documentação

Se você é novo no projeto, siga esta ordem:

1. [01-overview.md](01-overview.md) — o que é o projeto, em uma página.
2. [02-stack.md](02-stack.md) — tecnologias usadas (e as que não são usadas).
3. [03-folder-structure.md](03-folder-structure.md) — inventário completo de diretórios e arquivos.
4. [04-routing.md](04-routing.md) — como uma URL vira uma página.
5. [05-components.md](05-components.md) — partials, componentes de UI e árvore de composição.
6. [06-design-system.md](06-design-system.md) — tokens, cores, tipografia, espaçamento.
7. [07-seo.md](07-seo.md) — metadata, Schema.org, sitemap, robots.
8. [08-performance.md](08-performance.md) — carregamento de assets, cache, fontes.
9. [09-security.md](09-security.md) — headers, formulários, dados sensíveis.
10. [10-dependencies.md](10-dependencies.md) — dependências internas e de terceiros.
11. [11-build-deploy.md](11-build-deploy.md) — CI/CD, ambientes, Nginx, Docker.
12. [12-technical-debt.md](12-technical-debt.md) — dívida técnica observada, classificada por severidade.
13. [13-development-workflow.md](13-development-workflow.md) — fluxo de trabalho de desenvolvimento e publicação.
14. [14-glossary.md](14-glossary.md) — glossário jurídico e técnico do projeto.

O [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) traz uma síntese executiva (visão geral, pontos fortes, riscos, maturidade) para quem precisa de uma leitura rápida antes de decisões.

## Índice de documentos

| # | Documento | Conteúdo |
| --- | --- | --- |
| 00 | [README.md](README.md) | Este índice |
| 01 | [01-overview.md](01-overview.md) | Visão geral do produto e da arquitetura |
| 02 | [02-stack.md](02-stack.md) | Stack tecnológica |
| 03 | [03-folder-structure.md](03-folder-structure.md) | Estrutura de diretórios e inventário de arquivos |
| 04 | [04-routing.md](04-routing.md) | Rotas, URLs, redirecionamentos, i18n de URL |
| 05 | [05-components.md](05-components.md) | Componentes, partials, árvore de composição |
| 06 | [06-design-system.md](06-design-system.md) | Design tokens, cores, tipografia, espaçamento, breakpoints |
| 07 | [07-seo.md](07-seo.md) | Metadata, Open Graph, Twitter Cards, Schema.org, sitemap, robots |
| 08 | [08-performance.md](08-performance.md) | Carregamento de assets, fontes, imagens, cache |
| 09 | [09-security.md](09-security.md) | Headers, formulários, CAPTCHA, dados sensíveis, CORS |
| 10 | [10-dependencies.md](10-dependencies.md) | Dependências internas e serviços de terceiros |
| 11 | [11-build-deploy.md](11-build-deploy.md) | Pipeline de CI/CD, ambientes, Docker, Nginx |
| 12 | [12-technical-debt.md](12-technical-debt.md) | Dívida técnica classificada (Alta/Média/Baixa) |
| 13 | [13-development-workflow.md](13-development-workflow.md) | Workflow de desenvolvimento e publicação |
| 14 | [14-glossary.md](14-glossary.md) | Glossário de termos jurídicos e técnicos |
| — | [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) | Síntese executiva |

## Convenções usadas nestes documentos

- **"Não identificado no projeto."** — significa que uma busca ativa foi feita no repositório e nada foi encontrado (ex.: arquivo de configuração, teste, header de segurança).
- **"Necessita validação."** — significa que a informação depende de um sistema externo ao repositório (ex.: configuração real do Nginx no servidor, que segundo [docs/ambientes-e-deploy.md](../ambientes-e-deploy.md) não é mais versionada em Git) e não pode ser confirmada apenas lendo o código.
- Todas as referências a arquivos usam caminhos relativos à raiz do repositório (ex.: `public/index.html:12`).
- Este material reflete o estado do repositório no momento da análise. Trechos de código evoluem; trate esta documentação como uma fotografia, não como fonte viva — para o estado atual, sempre confira o arquivo citado.
