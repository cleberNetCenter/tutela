# CLAUDE.md — Tutela Digital™

Resumo operacional para uma sessão de Claude Code neste repositório. Não duplica os documentos de arquitetura — para o "porquê" das decisões, ver as referências abaixo.

## Comandos-chave

```bash
npm install
npm run dev     # servidor SSI local, http://localhost:8081/ — NUNCA python3 -m http.server (não resolve <!--#include-->)
npm test        # suíte Playwright completa (servidor próprio, porta 8080)
node tests/support/generate-asset-versions.js   # regenera tests/support/asset-versions.json após bump manual de ?v=
```

## Regras permanentes de processo

- **Servidor local obrigatório**: `npm run dev` (porta 8081) para inspeção manual; `npm test` sobe seu próprio servidor SSI (porta 8080). `python3 -m http.server` não implementa SSI e quebra header/footer/scripts silenciosamente — só aceitável para um arquivo isolado sem includes.
- **Regressão visual**: qualquer mudança em CSS/layout precisa rodar a suíte de regressão visual (`visual-contrast.spec.ts`, `visual-design-tokens.spec.ts`, `visual-radius-shadow.spec.ts`) antes de considerar o trabalho concluído.
- **Disciplina de escopo**: bugs encontrados fora do escopo da tarefa atual vão para commit separado e sinalizado — nunca misturados no mesmo diff.
- **Publicação**: commitar localmente é normal; `git push` só depois de confirmar com quem pediu a tarefa.
- **Fluxo de branches**: feature/fix → `homolog` (deploy automático de homologação) → validação manual → PR `homolog → main` (bloqueado por CI se o commit ainda não for ancestral de `homolog`) → deploy de produção automático. Ver [docs/architecture/13-development-workflow.md](docs/architecture/13-development-workflow.md).
- **Sem build step**: não há bundler, pré-processador CSS, nem lint configurado (`docs/architecture/02-stack.md`). Não introduzir um sem decisão arquitetural explícita (ADR).

## Estrutura essencial

```text
public/            # raiz do site servido (HTML, assets/css, assets/js, assets/lang)
public/partials/   # includes SSI (header, footer, scripts) — resolvidos por npm run dev e pelo Nginx
tests/              # Playwright: smoke, contraste, regressão visual, guard-tests de convenção
tests/support/      # servidor SSI de teste, gerador/manifesto de cache-busting
docs/architecture/  # documentação arquitetural — fonte de verdade, não reescrever sem necessidade
docs/architecture/adr/  # Registros de Decisão Arquitetural (ADRs) — ver README.md da pasta
docs/governance/    # Engineering Principles, Definition of Done, Review Checklist
```

## Fonte de verdade

- **O que falta fazer**: [docs/architecture/16-architecture-backlog.md](docs/architecture/16-architecture-backlog.md) — todo item rastreável (`ARQ-NNN`) com critérios de aceite, status e observações da sprint que o resolveu. Nenhum desenvolvimento deve começar sem estar representado ali.
- **Por que decisões específicas foram tomadas**: [docs/architecture/adr/](docs/architecture/adr/).
- **Princípios de evolução e convenções de engenharia**: [docs/architecture/17-architectural-manifesto.md](docs/architecture/17-architectural-manifesto.md), [docs/governance/18-engineering-principles.md](docs/governance/18-engineering-principles.md).
- **Definição de pronto / checklist de revisão**: [docs/governance/19-definition-of-done.md](docs/governance/19-definition-of-done.md), [docs/governance/20-review-checklist.md](docs/governance/20-review-checklist.md).
