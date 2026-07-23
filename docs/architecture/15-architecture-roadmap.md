# 15 — Roadmap de Evolução da Arquitetura

> Status: Planejamento
>
> Baseado na documentação produzida em `docs/architecture`.
>
> Este documento NÃO descreve a arquitetura atual.
>
> Seu objetivo é definir a evolução arquitetural do projeto pelos próximos ciclos de desenvolvimento.

---

# Índice

1. Objetivos Estratégicos
2. Princípios de Evolução
3. Critérios de Priorização
4. Épicos Arquiteturais
5. Ordem de Execução
6. Critérios de Aceite
7. Indicadores de Qualidade
8. Definição de Concluído

---

# 1. Objetivos Estratégicos

A evolução da arquitetura deverá perseguir simultaneamente os seguintes objetivos:

1. Eliminar dívida técnica sem criar novas dívidas.

2. Preservar a simplicidade arquitetural.

3. Manter SEO como requisito funcional.

4. Manter compatibilidade com a arquitetura MPA + SSI.

5. Melhorar segurança.

6. Melhorar consistência visual.

7. Aumentar a automação da engenharia.

8. Tornar o projeto progressivamente auto-documentado.

---

# 2. Princípios de Evolução

Toda alteração futura deverá obedecer aos princípios abaixo.

## P1

Preservar a arquitetura MPA.

## P2

Não introduzir dependências sem justificativa.

## P3

HTML continua sendo a fonte da verdade.

## P4

SEO nunca pode regredir.

## P5

Toda melhoria deve reduzir complexidade.

## P6

Sempre consolidar padrões existentes antes de criar novos.

## P7

Eliminar código morto sempre que uma área for modificada.

---

# 3. Critérios de Priorização

As entregas seguirão esta ordem:

1 Segurança

2 SEO

3 Design System

4 Consolidação Arquitetural

5 Engenharia

6 Acessibilidade

7 Governança

Cada épico só inicia quando o anterior estiver encerrado.

---

# ÉPICO 1

SEGURANÇA

Objetivo

Eliminar riscos de segurança e conformidade.

Itens

- endpoint diagnóstico

- CSP

- HSTS

- X-Frame-Options

- Frame Ancestors

- Referrer Policy

- Permissions Policy

- LGPD

Critérios de aceite

✓ arquitetura auditável

✓ configuração documentada

✓ nenhum item crítico aberto

---

# ÉPICO 2

SEO

Objetivo

Eliminar inconsistências de indexação.

Itens

- Open Graph

- Twitter Cards

- hreflang

- canonical

- sitemap

- metadata

Critérios

100% das páginas consistentes.

---

# ÉPICO 3

DESIGN SYSTEM

Objetivo

Criar uma única fonte de verdade.

Itens

- unificar color

- unificar ad

- unificar ux

- radius

- shadow

- breakpoints

- spacing

Critério

Nenhum token duplicado.

---

# ÉPICO 4

CONSOLIDAÇÃO DA ARQUITETURA

Objetivo

Eliminar completamente vestígios da arquitetura anterior.

Itens

navigation.js

i18n antigo

CSS deprecated

vercel.json

arquivos mortos

Critério

O projeto deve parecer ter sido sempre MPA.

---

# ÉPICO 5

ENGENHARIA

Objetivo

Melhorar produtividade.

Itens

Playwright

Cache Busting

Padronização

Validações

Lint

Critério

Pipeline totalmente automatizado.

---

# ÉPICO 6

ACESSIBILIDADE

Objetivo

Elevar conformidade WCAG.

Itens

Skip Link

ARIA

Landmarks

Keyboard

Focus

Contraste

Critério

WCAG AA.

---

# ÉPICO 7

GOVERNANÇA

Objetivo

Criar documentação permanente.

Itens

Manifesto

Princípios

ADRs

Engineering Guide

CLAUDE.md

Critério

Todo novo desenvolvedor deve compreender a arquitetura lendo apenas a documentação.

---

# 5. Ordem de Execução

Sprint A

Segurança

Sprint B

SEO

Sprint C

Design System

Sprint D

Consolidação

Sprint E

Engenharia

Sprint F

Acessibilidade

Sprint G

Governança

---

# 6. Indicadores

A cada sprint medir:

Número de dívidas eliminadas

Número de arquivos removidos

Duplicações eliminadas

Tokens consolidados

Cobertura Playwright

Performance Lighthouse

SEO

Acessibilidade

---

# 7. Definição de Concluído

Uma dívida técnica só será considerada encerrada quando:

✓ código corrigido

✓ documentação atualizada

✓ arquitetura preservada

✓ testes executados

✓ Playwright executado

✓ nenhuma regressão visual

✓ nenhum impacto de SEO

✓ revisão arquitetural concluída

---

# Resultado Esperado

Ao final deste roadmap o projeto deverá possuir:

• Arquitetura consistente.

• Design System unificado.

• Segurança auditável.

• SEO consolidado.

• Engenharia automatizada.

• Governança documentada.

• Dívida técnica crítica igual a zero.
