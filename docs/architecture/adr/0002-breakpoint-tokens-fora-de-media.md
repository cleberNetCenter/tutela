# ADR-0002 — Tokens `--breakpoint-*` como constantes documentadas, não `var()` dentro de `@media`

| Campo | Valor |
|---|---|
| Status | Aceito |
| Data | 2026-07-24 |
| Sprint / ARQ | Sprint 12, `ARQ-302` |

## Contexto

`ARQ-302` exigia eliminar 13 valores de `max-width` usados como números mágicos em `@media`, substituindo-os por uma escala de tokens compartilhada. O levantamento (grep completo antes de qualquer mudança) confirmou 47 ocorrências reais desses 13 valores em 17 arquivos.

A limitação técnica real: CSS não permite `var()` dentro da condição de `@media` — `@media (max-width: var(--breakpoint-768))` é sintaxe inválida pela própria especificação CSS, não uma questão de compatibilidade de navegador. `02-stack.md` confirma que o projeto não usa pré-processador (sem Sass/Less/Stylus) nem build step para CSS (sem PostCSS/Tailwind), então qualquer solução que dependesse de um passo de build estava fora de escopo por decisão de arquitetura já estabelecida, não por limitação de execução desta sprint.

## Decisão

Declarar os 13 valores reais como tokens `--breakpoint-<valor>` em `foundation/tokens.css`, nomeados pelo valor literal (ex. `--breakpoint-768: 768px`), utilizáveis via `var()` em qualquer contexto que não seja a condição de `@media` (ex. `max-width` de container). Dentro de `@media`, os valores continuam literais — a "tokenização" real é garantida por um guard-test (`tests/breakpoint-tokens.spec.ts`) que lê `tokens.css` como fonte única de verdade e falha se um valor não aprovado aparecer em qualquer `@media (max-width: ...)` do repositório, ou se a formatação divergir do padrão.

## Alternativas consideradas

- **Adotar um pré-processador (Sass/Less) só para resolver `var()` em `@media`** — descartada: introduziria um build step novo no projeto, uma mudança de arquitetura muito maior que o escopo do item, e contradiz a decisão já documentada em `02-stack.md` de não ter build step.
- **`@custom-media` (PostCSS)** — descartada pelo mesmo motivo: exige build step (PostCSS), inexistente no projeto.
- **Consolidar os 13 valores em 5-6 níveis semânticos (`xs/sm/md/lg/xl`)** — descartada: comprimiria valores distintos sob o mesmo nome sem justificativa de design, e não havia convenção de nomenclatura por escala pré-existente a reaproveitar.

## Consequências

O critério de aceite original ("todo `max-width` referenciando um token `--breakpoint-*` via `var()`") foi reinterpretado, com essa reinterpretação registrada explicitamente no próprio backlog: "toda ocorrência usa um valor da lista aprovada em `--breakpoint-*`, verificado automaticamente" — a garantia é por guard-test, não por referência sintática direta. Isso é uma limitação aceita da stack sem build step, não uma solução parcial a ser revisitada; qualquer decisão futura de adotar build step para CSS reabriria esta decisão, mas isso é uma mudança de stack maior, fora do escopo de qualquer ARQ individual do Épico 3.
