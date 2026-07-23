# Resumo Executivo — Arquitetura Tutela Digital®

## Índice
- [Visão geral](#visão-geral)
- [Pontos fortes](#pontos-fortes)
- [Riscos](#riscos)
- [Complexidade](#complexidade)
- [Maturidade da arquitetura](#maturidade-da-arquitetura)
- [Oportunidades futuras](#oportunidades-futuras)

## Visão geral

O site da Tutela Digital® é uma **aplicação web multi-página (MPA) inteiramente estática** — HTML, CSS e JavaScript vanilla, sem framework, sem build, sem backend próprio versionado — que serve 35 páginas de conteúdo institucional e jurídico sobre custódia probatória de ativos digitais. A composição de página depende de Server Side Includes (SSI) resolvidos pelo Nginx em produção. O deploy é feito via GitHub Actions em runners self-hosted, com `git reset --hard` + Docker Compose em dois ambientes (homologação e produção), seguindo um fluxo de branches `feature → homolog → main` reforçado por um gate de CI que impede promoção direta a `main`.

Esta é uma arquitetura **deliberadamente simples e de baixo custo operacional** para o problema que resolve: divulgar um serviço jurídico-técnico, capturar leads via um formulário de diagnóstico, e ranquear bem em buscadores (incluindo bots de LLM, explicitamente liberados no `robots.txt`) para um nicho jurídico específico no Brasil.

## Pontos fortes

- **SEO tecnicamente maduro para um site estático**: metadata completa por página, mais de 15 tipos de Schema.org em uso (Organization, LegalService, TechArticle, Article, FAQPage, BreadcrumbList, entre outros), sitemap regenerado automaticamente a cada push a partir do estado real do Git, e um índice de busca client-side desenhado com cuidado (exclui páginas de redirecionamento, resolve conteúdo de header/footer via SSI, prioriza matches em título/descrição).
- **Design system central bem organizado**: `foundation/tokens.css` segue uma hierarquia clara (paleta primitiva → tokens semânticos → extensão de produto), com comentários explicando a intenção de cada camada — incomum em projetos CSS sem ferramenta de design tokens.
- **Pipeline de deploy com salvaguardas reais de processo**: o workflow "Guard - main requer homolog" implementa como *gate* técnico de CI algo que, em muitos times, fica só como convenção verbal — impossibilita, na prática, pular a etapa de homologação.
- **Runbook operacional já existente e detalhado** (`docs/ambientes-e-deploy.md`), escrito com honestidade sobre o que está confirmado versus o que precisa validação no servidor — uma postura de documentação madura, adotada também nesta nova documentação de arquitetura.
- **i18n bem pensado para o caso de uso**: tradução client-side para a maioria do site (custo zero de manutenção de conteúdo duplicado) combinada com páginas físicas totalmente traduzidas apenas onde há retorno de SEO internacional (o pillar de Ativos Digitais).
- **Superfície de ataque pequena por construção**: sem dependências de runtime, sem gerenciamento de sessão/autenticação neste repositório, sem segredos versionados.

## Riscos

Classificados em detalhe, com evidência e severidade, em [12-technical-debt.md](12-technical-debt.md). Os três de maior impacto potencial:

1. **Compartilhamento social quebrado em todo o site**: a imagem de Open Graph referenciada em todas as 35 páginas (`og-image.jpg`) não existe no repositório.
2. **Endpoint de coleta de dados pessoais (`/api/diagnostico`) sem implementação auditável** neste repositório — impede verificar tratamento adequado de dados sob a LGPD, ironicamente para uma empresa cujo produto é conformidade e integridade probatória.
3. **Postura de segurança HTTP não verificável a partir do código**: CSP, HSTS e X-Frame-Options não são declarados em nenhum lugar do repositório; dependem inteiramente de uma configuração de Nginx que não é versionada, criando um ponto cego de auditoria.

Riscos adicionais de menor severidade, mas relevantes para manutenção contínua: fragmentação de design tokens (três namespaces de cor de marca), ausência de skip-link de acessibilidade, e uma regra de sincronização de branches (main → homolog) que o próprio time já identificou como potencialmente invertida.

## Complexidade

**Baixa a moderada**, e majoritariamente **acidental, não essencial** — ou seja, boa parte da complexidade encontrada (três esquemas de cache-busting, três sistemas de tokens, nomenclatura de scripts que não corresponde à função) vem de evolução incremental sem consolidação, não da natureza do problema em si. Um site estático institucional com 35 páginas é, em princípio, um domínio de baixa complexidade estrutural; a maior fonte de complexidade real é a coordenação entre camadas manuais (i18n JSON, versionamento de assets, geração de sitemap/índice de busca por CI) que, em uma stack com ferramentas de build, seriam automatizadas.

## Maturidade da arquitetura

A arquitetura está em um estágio de **maturidade operacional média-alta com maturidade de engenharia de frontend média-baixa**: o pipeline de deploy, o runbook e a estratégia de SEO revelam um time que pensa sobre processo e sobre buscadores com cuidado (evidenciado pelos comentários explicativos ao longo do código e dos workflows). Já a camada de frontend (CSS/JS) mostra sinais claros de **crescimento orgânico sem refatoração periódica**: arquivos "descontinuados" mantidos como tombstones em vez de removidos, uma migração de SPA para MPA cujos vestígios (`navigation.js` desativado, IDs de `i18n-config.json` que não existem mais no DOM) não foram completamente limpos, e ausência total de testes automatizados apesar de uma tentativa iniciada (Playwright instalado, não configurado).

## Oportunidades futuras

Sem prescrever implementação (fora do escopo desta análise, que é somente leitura), os documentos temáticos desta pasta sinalizam onde investigação e decisão futura têm mais retorno:

- Consolidar os três sistemas de tokens de cor (`--color-*`, `--ad-*`, `--ux-*`) em uma única fonte de verdade — ver [06-design-system.md](06-design-system.md).
- Confirmar e documentar formalmente a configuração real de Nginx (headers de segurança, redirects, SSI) como parte do runbook — ver [09-security.md](09-security.md) e [11-build-deploy.md](11-build-deploy.md).
- Esclarecer o ciclo de vida de `/api/diagnostico` e dos dados coletados pelo formulário — ver [09-security.md](09-security.md).
- Revisitar a decisão de sincronização automática `main → homolog` no workflow de sitemap junto à equipe — ver [11-build-deploy.md](11-build-deploy.md).
- Decidir explicitamente se `vercel.json`/`public/_redirects` seguem necessários dado que o deploy real não usa essas plataformas — ver [04-routing.md](04-routing.md).

## Documentos relacionados

Este resumo é a porta de entrada. Para qualquer afirmação acima, o documento temático correspondente traz a evidência completa, o arquivo e a linha exata de origem. Comece por [README.md](README.md) para navegar pelo conjunto completo.
