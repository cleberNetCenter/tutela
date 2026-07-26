# ADR-0003 — Cache-busting por contador incremental + guard-test de hash

| Campo | Valor |
|---|---|
| Status | Aceito |
| Data | 2026-07-25 |
| Sprint / ARQ | Sprint 19, `ARQ-502` |

## Contexto

Três esquemas de cache-busting conviviam no repositório: contador simples (`main.css?v=7`), data `AAAAMMDDNN` (`i18n.js?v=2026041001`) e contador por arquivo (`lang/pt.json?v=10`). O levantamento (grep completo antes de qualquer mudança) encontrou 113 ocorrências de `?v=` em 40 arquivos, mapeadas a 22 assets fisicamente distintos, incluindo dois casos reais de inconsistência (mesmo asset com `?v=` divergente entre páginas — `assets-digital.css` e `insights-pilar.css`) que já causavam risco real de cache desatualizado, não só inconsistência cosmética.

O risco central do item era o cenário "esquecer de incrementar o `?v=` ao editar o arquivo" — nenhum dos três esquemas, sozinho, detecta esse erro automaticamente.

## Decisão

Contador incremental único por arquivo, mantido manualmente, com um manifesto (`tests/support/asset-versions.json`) registrando `{versão, hash de conteúdo}` de cada asset. Um guard-test (`tests/cache-busting.spec.ts`) falha se o hash do arquivo no disco divergir do hash registrado no manifesto — captura exatamente o cenário de risco do item (editar o arquivo sem incrementar `?v=`), sem depender de um passo novo no pipeline de deploy. `tests/support/generate-asset-versions.js` regenera o manifesto após um bump manual, recalculando hashes e falhando se encontrar versões divergentes para o mesmo arquivo antes de escrever.

## Alternativas consideradas

- **Hash de conteúdo calculado automaticamente por script, embutido direto na URL do asset** — mais robusto (elimina o passo manual por completo), mas exigiria um passo novo no pipeline de deploy que hoje não existe (`11-build-deploy.md` confirma "não há build") — fora de escopo desta sprint, mesma disciplina de arquitetura sem build step de `ARQ-302`/ADR-0002.
- **Data única `AAAAMMDDNN` como formato padronizado** — padroniza a sintaxe mas não previne cache stale sozinha (nada impede esquecer de atualizar a data ao editar o arquivo); exigiria o mesmo guard-test de hash por cima mesmo assim, então não simplifica a solução real.

## Consequências

21 assets versionados, todos com contador inteiro simples (1-4 dígitos), 1 único valor por arquivo em todo o site, verificado automaticamente. O processo de bump de versão continua manual (não há geração automática de hash na URL), mas o guard-test elimina o risco silencioso de esquecimento — a proteção real do item vem do teste, não da convenção de formato em si. Um achado incidental fora de escopo desta decisão (`legal/termos-de-uso.html` referenciando `pages/termos-de-uso.css`, nunca existente no histórico do repositório) foi catalogado como `KNOWN_DEAD_ASSETS` no manifesto, não corrigido aqui — candidato a item novo de backlog, não uma reabertura desta decisão.
