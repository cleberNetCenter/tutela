# ADRs — Registros de Decisão Arquitetural

Formaliza, em formato leve, decisões técnicas relevantes já tomadas durante a execução de `16-architecture-backlog.md` — uma escolha entre alternativas reais, com trade-offs, que uma pessoa futura poderia questionar ou reverter sem saber por que foi feita daquela forma (critério de `../../governance/18-engineering-principles.md`, linha "Quando criar um ADR").

Um ADR não reabre nem reinvestiga a decisão — só formaliza o "porquê" já registrado no campo Observações do item de backlog correspondente.

Use [template.md](template.md) para novos ADRs. Numeração sequencial (`0001`, `0002`, ...), nunca reatribuída.

## Índice

| ADR | Decisão | Sprint / ARQ |
|---|---|---|
| [0001](0001-nomenclatura-ad-pillar.md) | Nomenclatura `--ad-pillar-*` para tokens sem equivalente em `--ad-*` | Sprint 11 / `ARQ-301` |
| [0002](0002-breakpoint-tokens-fora-de-media.md) | Tokens `--breakpoint-*` como constantes documentadas, não `var()` em `@media` | Sprint 12 / `ARQ-302` |
| [0003](0003-convencao-cache-busting.md) | Cache-busting por contador incremental + guard-test de hash | Sprint 19 / `ARQ-502` |
