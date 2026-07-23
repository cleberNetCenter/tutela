# 19 — Definition of Done

# Objetivo

Definir o que significa dizer que um item de trabalho está **concluído**. Não explica conceitos, não justifica regras — para o porquê de cada critério, ver [17-architectural-manifesto.md](../architecture/17-architectural-manifesto.md) e [18-engineering-principles.md](18-engineering-principles.md). Este documento só declara o critério de aceite objetivo, aplicável a qualquer item de [16-architecture-backlog.md](../architecture/16-architecture-backlog.md).

# Regra Geral

Nenhum item do backlog é considerado concluído enquanto todos os critérios obrigatórios da tabela abaixo não forem atendidos. Um item parcialmente atendido é **em andamento** ou **bloqueado**, nunca **concluído**.

# Checklist de Conclusão

| Critério | Obrigatório | Observação |
|---|---|---|
| ☐ Escopo implementado | Sim | Corresponde exatamente ao escopo do item no backlog — nem menos, nem mais. |
| ☐ Critérios de aceite atendidos | Sim | Os declarados no item correspondente do backlog. |
| ☐ Critérios de regressão atendidos | Sim | Os declarados no item correspondente do backlog. |
| ☐ Código revisado | Sim | Por alguém que não implementou a mudança. |
| ☐ Código simples | Sim | Ver EP-01 em 18-engineering-principles.md. |
| ☐ Sem duplicação desnecessária | Sim | Ver EP-04 e EP-15. |
| ☐ Sem código morto introduzido | Sim | Ver EP-05. |
| ☐ Testes executados | Condicional | Obrigatório para fluxos críticos; ver regras de teste em 18-engineering-principles.md. |
| ☐ Documentação atualizada | Sim | Ver EP-10; inclui qualquer documento cuja afirmação a mudança tornou desatualizada. |
| ☐ Backlog atualizado | Sim | Status do item refletido em 16-architecture-backlog.md. |
| ☐ Dívida técnica registrada (quando existir) | Condicional | Obrigatório sempre que a entrega introduzir alguma; ver EP-17. |
| ☐ Dependências justificadas | Condicional | Obrigatório sempre que a entrega introduzir dependência nova; ver EP-13. |
| ☐ Sem erros conhecidos | Sim | Nenhum erro identificado e não resolvido no escopo entregue. |
| ☐ Sem TODOs permanentes | Sim | Um `TODO` só é aceitável se corresponder a um item já aberto no backlog, referenciado explicitamente. |
| ☐ Build válida | Sim | O resultado publicável carrega e funciona sem erro observável, pelo mecanismo de verificação vigente no momento da entrega. |

15 critérios no total: 11 obrigatórios em toda entrega, 4 condicionais (aplicam-se conforme a natureza da entrega, mas quando aplicáveis são igualmente obrigatórios).

# Exceções

Um item pode ser entregue parcialmente apenas quando:

1. A parte entregue é, por si só, funcional e não deixa o projeto em estado inconsistente.
2. A parte não entregue é registrada explicitamente como um novo item no backlog, com seu próprio critério de aceite.
3. O item original é marcado como concluído somente para o escopo efetivamente entregue — nunca como "concluído" para o escopo original inteiro.

Sem os três pontos acima documentados no backlog, uma entrega parcial não é uma exceção válida — é um item incompleto.

# Responsabilidade

Quem revisa a entrega declara o item como concluído, com base nesta checklist — nunca quem a implementou, sozinho. Na ausência de um segundo revisor disponível, quem implementou confirma cada critério explicitamente antes de declarar conclusão, e essa autoavaliação fica registrada junto ao item.

# O que este documento NÃO é

- Não é o Review Checklist. Não define o que verificar durante a revisão de uma mudança específica — define apenas o resultado que essa revisão confirma no final.
- Não é o Manifesto. Não justifica nenhum critério — apenas os aplica.
- Não é o Engineering Principles. Não explica as práticas — apenas exige que já tenham sido seguidas.
- Não é um ADR. Não registra decisão alguma.
