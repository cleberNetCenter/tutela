# ADR-0001 — Sub-extensão `--ad-pillar-*` para tokens sem equivalente em `--ad-*`

| Campo | Valor |
|---|---|
| Status | Aceito |
| Data | 2026-07-24 |
| Sprint / ARQ | Sprint 11, `ARQ-301` |

## Contexto

`ARQ-301` exigia eliminar `--ux-*` (namespace de cor de marca definido inline em `partials/ativos-digitais-pillar-styles.html`, usado só pelas 3 páginas do cluster de idioma de Ativos Digitais) e migrar tudo para `--ad-*` (fonte única de tokens em `foundation/tokens.css`), sem introduzir mudança visual perceptível não intencional.

Das 21 declarações originais de `--ux-*`, 6 nunca eram consumidas e foram removidas sem substituto. Das 15 restantes, 4 tinham valor numérico idêntico a um token `--ad-*` já existente e foram migradas diretamente (`--ux-accent`→`--ad-accent-gold`, `--ux-danger`→`--ad-danger`, `--ux-danger-bg`→`--ad-danger-bg`, `--ux-shadow-xs`→`--ad-shadow-xs`). As 11 restantes não tinham correspondência numérica em `--ad-*`, confirmado par a par, não presumido — ver tabela completa de valores antes/depois na entrega da Sprint 11.

## Decisão

Trazer as 11 declarações restantes para `tokens.css` com o mesmo valor exato, sob uma sub-extensão nova: `--ad-pillar-*` (`--ad-pillar-bg`, `--ad-pillar-ink`, `--ad-pillar-ink-soft`, `--ad-pillar-line`, `--ad-pillar-brand`, `--ad-pillar-brand-2`, `--ad-pillar-brand-3`, `--ad-pillar-max-width`, `--ad-pillar-radius-xl`, `--ad-pillar-shadow-sm`, `--ad-pillar-shadow-md`).

## Alternativas consideradas

- **Forçar os 11 valores para o token `--ad-*` numericamente mais próximo** — descartada porque introduziria uma mudança de marca perceptível não intencional, proibida pelo critério de regressão do item (diff de screenshot no cluster Ativos Digitais).
- **Inventar um valor novo de compromisso entre `--ux-*` e o `--ad-*` mais próximo** — descartada pelo mesmo motivo: não é uma migração, é uma mudança de design não solicitada nesta sprint.
- **Manter os 11 tokens como namespace `--ux-*` isolado** — descartada por não satisfazer o critério de aceite do item (nenhum token `--ux-*` remanescente; fonte única `--ad-*`).

## Consequências

`--ad-*` passa a ter uma sub-extensão nomeada por contexto de uso (`pillar`) em vez de ser uma escala plana — precedente para casos futuros em que um cluster de páginas precisa de tokens de marca sem equivalente no restante do site: estender `--ad-*` com um sufixo de contexto, não criar um namespace paralelo. `--ux-*` foi eliminado por completo (0 declarações, 0 usos), satisfazendo o critério de aceite de `ARQ-301` sem regressão visual (0 diff em `tests/visual-design-tokens.spec.ts`, 24 baselines granulares).
