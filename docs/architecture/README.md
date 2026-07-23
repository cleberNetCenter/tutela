# Documentação de Arquitetura — Tutela Digital®

Esta pasta documenta, com base exclusivamente em evidências encontradas no repositório `cleberNetCenter/tutela` (branch `homolog`, snapshot de 2026-07-23), a arquitetura técnica, o design system, o SEO, a performance, a segurança e a dívida técnica do site institucional da Tutela Digital®.

Este trabalho é **somente leitura** quanto ao código da aplicação: nenhum arquivo de `public/` foi alterado por esta documentação.

> **Status: fase estrutural encerrada.** A arquitetura, o roadmap, o backlog e a cadeia de governança (documentos 01-20) foram revisados e aprovados como baseline em 2026-07-23 (tag sugerida: `architecture-baseline-2026`). A partir deste ponto, novos documentos estruturais só devem ser criados mediante necessidade excepcional — a evolução do projeto ocorre através do [Backlog](16-architecture-backlog.md), do [Engineering Principles](../governance/18-engineering-principles.md) e de ADRs.

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
15. [15-architecture-roadmap.md](15-architecture-roadmap.md) — plano de evolução arquitetural por épicos (não descreve o estado atual, descreve prioridades futuras).
16. [16-architecture-backlog.md](16-architecture-backlog.md) — backlog rastreável (ARQ-xxx) derivado do roadmap; referência oficial para toda implementação futura.
17. [17-architectural-manifesto.md](17-architectural-manifesto.md) — princípios arquiteturais permanentes; como pensar antes de alterar o projeto, independentemente da tecnologia em uso.

A cadeia de governança de engenharia vive em `docs/governance/`, não nesta pasta:

18. [../governance/18-engineering-principles.md](../governance/18-engineering-principles.md) — como desenvolvemos software neste projeto, dia a dia.
19. [../governance/19-definition-of-done.md](../governance/19-definition-of-done.md) — quando um item do backlog é considerado concluído.
20. [../governance/20-review-checklist.md](../governance/20-review-checklist.md) — checklist final antes de aprovar uma mudança.

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
| 15 | [15-architecture-roadmap.md](15-architecture-roadmap.md) | Roadmap de evolução arquitetural por épicos |
| 16 | [16-architecture-backlog.md](16-architecture-backlog.md) | Backlog arquitetural oficial (ARQ-xxx), rastreável |
| 17 | [17-architectural-manifesto.md](17-architectural-manifesto.md) | Manifesto arquitetural — princípios permanentes |
| — | [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) | Síntese executiva |

## Documentos de governança (`docs/governance/`)

| # | Documento | Conteúdo |
| --- | --- | --- |
| 18 | [18-engineering-principles.md](../governance/18-engineering-principles.md) | Práticas objetivas de engenharia do dia a dia |
| 19 | [19-definition-of-done.md](../governance/19-definition-of-done.md) | Critério objetivo de conclusão de um item de trabalho |
| 20 | [20-review-checklist.md](../governance/20-review-checklist.md) | Checklist de revisão final antes de aprovar uma mudança |

## Convenções usadas nestes documentos

- **"Não identificado no projeto."** — significa que uma busca ativa foi feita no repositório e nada foi encontrado (ex.: arquivo de configuração, teste, header de segurança).
- **"Necessita validação."** — significa que a informação depende de um sistema externo ao repositório (ex.: configuração real do Nginx no servidor, que segundo [docs/ambientes-e-deploy.md](../ambientes-e-deploy.md) não é mais versionada em Git) e não pode ser confirmada apenas lendo o código.
- Todas as referências a arquivos usam caminhos relativos à raiz do repositório (ex.: `public/index.html:12`).
- Este material reflete o estado do repositório no momento da análise. Trechos de código evoluem; trate esta documentação como uma fotografia, não como fonte viva — para o estado atual, sempre confira o arquivo citado.
