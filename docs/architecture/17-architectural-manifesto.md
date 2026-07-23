# 17 — Manifesto Arquitetural

> Este documento não descreve a arquitetura atual do projeto. Não descreve o backlog. Não descreve tecnologias.
>
> Ele descreve como qualquer pessoa — ou qualquer agente de IA — deve pensar antes de alterar este projeto, hoje ou daqui a dez anos, independentemente de quais tecnologias estiverem em uso naquele momento.

---

## Introdução

Este projeto sustenta um serviço cujo valor central é a confiança de que um fato digital pode ser verificado. Antes de qualquer outra consideração técnica, esse é o problema que a arquitetura existe para resolver: garantir que o que é afirmado possa ser conferido, por qualquer pessoa, a qualquer momento, sem depender da palavra de quem afirma.

Essa exigência não se aplica só ao produto que o projeto entrega — aplica-se à própria arquitetura que o entrega. Um sistema que promete auditabilidade e integridade a seus usuários, mas cuja própria construção é opaca, inconsistente ou não verificável, contradiz a razão de existir do que constrói. Por isso, este manifesto trata a arquitetura não como um meio neutro de entregar conteúdo, mas como uma extensão do compromisso que o projeto assume publicamente.

A arquitetura existe para resolver três tensões permanentes, que nenhuma tecnologia específica resolve sozinha:

- **Entre alcance e integridade** — o projeto precisa ser encontrado, lido e compreendido por muitos tipos de leitor (pessoas, buscadores, tecnologia assistiva, sistemas automatizados), sem que essa busca por alcance comprometa a exatidão do que é dito.
- **Entre evolução e estabilidade** — o projeto precisa poder crescer e se corrigir continuamente, sem que cada mudança se torne um risco para o que já funciona.
- **Entre simplicidade operacional e responsabilidade** — o projeto é mantido por uma operação pequena e deliberadamente enxuta; isso não é desculpa para negligência, é motivo para que cada decisão de arquitetura seja ainda mais criteriosa, já que há menos margem para absorver erros.

Diante de qualquer escolha técnica, os objetivos abaixo importam mais do que qual tecnologia específica os realiza:

1. Que o que é publicado possa ser verificado.
2. Que o que é publicado possa ser encontrado e compreendido por quem precisa dele.
3. Que uma mudança feita hoje não exija reconstruir o entendimento de quem vier depois.
4. Que a complexidade do sistema nunca ultrapasse a complexidade real do problema que ele resolve.

Tecnologias específicas são meios. Este documento não trata de meios — trata dos fins que qualquer meio escolhido precisa servir.

---

## Missão Arquitetural

**A arquitetura existe para que a verdade permaneça verificável, mesmo quando tudo o mais mudar.**

---

## Visão Arquitetural

Nos próximos anos, este projeto deve crescer em conteúdo, alcance e complexidade de negócio sem crescer em complexidade estrutural na mesma proporção. Cada nova capacidade deve poder ser explicada por alguém que nunca a implementou, apenas lendo o que existe.

O sistema deve permanecer, a qualquer momento, inspecionável por inteiro: qualquer pessoa habilitada deve conseguir entender o que o projeto faz, por que faz e como foi decidido, sem depender de conhecimento que exista apenas na memória de quem o construiu.

A confiança que o projeto pede a seus usuários deve ser espelhada internamente: decisões documentadas, mudanças rastreáveis, dívidas reconhecidas e não escondidas. O projeto não deve, em nenhum momento futuro, exigir de quem o mantém uma fé que ele mesmo se recusaria a pedir de seus usuários.

A evolução é bem-vinda; o acúmulo silencioso de atalhos não é. Cada geração de decisões técnicas deve deixar o projeto mais simples de entender do que o encontrou, nunca mais obscuro — mesmo quando o problema que resolve se torna mais complexo.

Nenhuma tecnologia usada hoje é permanente. Os compromissos descritos neste documento são.

---

## Valores Arquiteturais

### Simplicidade Deliberada

| Campo | Conteúdo |
|---|---|
| Descrição | A solução mais simples capaz de cumprir o requisito real é sempre preferível a uma mais sofisticada. |
| Justificativa | Complexidade não examinada se acumula silenciosamente até se tornar risco; simplicidade reduz a superfície onde um erro pode se esconder. |
| Impacto esperado | Menor tempo para qualquer pessoa entender o sistema; menor custo de manutenção; menor probabilidade de regressão ao alterar qualquer parte. |

### Auditabilidade

| Campo | Conteúdo |
|---|---|
| Descrição | Qualquer decisão, comportamento ou dado do sistema deve poder ser explicado e rastreado até sua origem. |
| Justificativa | O serviço que este projeto sustenta depende da ideia de que fatos podem ser verificados — a arquitetura que o entrega precisa sustentar o mesmo padrão sobre si mesma. |
| Impacto esperado | Menos pontos cegos; decisões defensáveis diante de qualquer auditoria externa; confiança institucional sustentada por evidência, não por afirmação. |

### Fonte Única da Verdade

| Campo | Conteúdo |
|---|---|
| Descrição | Toda informação, regra ou definição deve existir em exatamente um lugar; toda duplicação é uma divergência futura ainda não manifesta. |
| Justificativa | Duas fontes para o mesmo fato divergem com o tempo, mesmo com boa intenção — a única defesa estrutural é impedir que a duplicação nasça. |
| Impacto esperado | Consistência automática; correções se propagam sem esforço repetido; menor risco de um lugar dizer uma coisa e outro dizer outra. |

### Legibilidade Universal

| Campo | Conteúdo |
|---|---|
| Descrição | O conteúdo deve ser compreensível por qualquer tipo de leitor — pessoa, buscador, tecnologia assistiva, agente automatizado — sem depender de uma capacidade especial de quem lê. |
| Justificativa | O alcance e a credibilidade do projeto dependem de ser corretamente interpretado por todo tipo de leitor, não apenas pelo público em condições ideais. |
| Impacto esperado | Alcance ampliado; inclusão; resiliência a mudanças em como o conteúdo é consumido no futuro. |

### Confiabilidade Operacional

| Campo | Conteúdo |
|---|---|
| Descrição | Nada chega ao público sem passar antes por um estágio de verificação; mudanças são reversíveis e seu efeito é previsível. |
| Justificativa | Erros expostos diretamente ao público afetam a credibilidade de um serviço cujo produto é, precisamente, confiança. |
| Impacto esperado | Menor frequência e menor impacto de falhas; capacidade de recuperação rápida quando algo dá errado. |

### Evolução Incremental

| Campo | Conteúdo |
|---|---|
| Descrição | Mudanças relevantes acontecem em passos pequenos e verificáveis, nunca em saltos que não podem ser explicados ou revertidos isoladamente. |
| Justificativa | Passos grandes escondem risco dentro de si; passos pequenos tornam cada decisão revisável e reversível por conta própria. |
| Impacto esperado | Histórico compreensível; risco cumulativo menor; capacidade de reverter uma decisão sem reverter todas as outras. |

### Transparência Documental

| Campo | Conteúdo |
|---|---|
| Descrição | O que não está documentado não pode ser considerado conhecido pelo projeto, mesmo que esteja implementado. |
| Justificativa | Conhecimento tácito desaparece quando as pessoas que o carregam saem; documentação é a única forma de conhecimento que sobrevive à equipe que o criou. |
| Impacto esperado | Continuidade independente de quem está presente; decisões que não se perdem com o tempo ou com a rotatividade de pessoas. |

### Responsabilidade sobre Dados

| Campo | Conteúdo |
|---|---|
| Descrição | Dado pessoal só é coletado, transmitido ou armazenado quando existe entendimento claro e documentado de seu ciclo de vida completo. |
| Justificativa | Coerência entre o que o projeto promete a quem confia nele e o que sua própria arquitetura pratica internamente. |
| Impacto esperado | Conformidade legal sustentável ao longo do tempo; menor risco reputacional e jurídico. |

### Performance como Respeito ao Usuário

| Campo | Conteúdo |
|---|---|
| Descrição | O tempo e os recursos de quem acessa o projeto são tratados como finitos e valiosos, não como infinitamente disponíveis. |
| Justificativa | Lentidão é uma forma de atrito que afasta exatamente o público que o projeto tenta servir. |
| Impacto esperado | Melhor experiência percebida; melhor retenção; sinal de cuidado transmitido antes mesmo de o conteúdo ser lido. |

### Acessibilidade como Direito

| Campo | Conteúdo |
|---|---|
| Descrição | A capacidade de usar o projeto não pode depender de uma condição física, sensorial ou cognitiva específica de quem o acessa. |
| Justificativa | Excluir alguém por uma barreira evitável contradiz o propósito de um serviço que se apresenta como confiável e justo. |
| Impacto esperado | Alcance ampliado; conformidade com padrões reconhecidos de acessibilidade; um produto genuinamente utilizável por qualquer pessoa. |

---

## Princípios Arquiteturais

### PA-01 — A Estrutura Publicada é a Fonte da Verdade

| Campo | Conteúdo |
|---|---|
| Descrição | O que é efetivamente entregue a quem lê — sua estrutura e seu conteúdo — é a autoridade final sobre o que o projeto é, não a ferramenta ou processo que o produziu. |
| Motivação | Ferramentas mudam; o que chega a quem lê é o que precisa poder ser auditado diretamente, sem intermediários. |
| Consequências | Nenhuma regra essencial deve existir apenas dentro de uma ferramenta de produção, sem correspondência inspecionável no resultado final. |
| Exemplos | Conteúdo escrito diretamente na forma final, sem uma camada intermediária que precise ser processada para ser lida. |
| Anti-exemplos | Conteúdo que só existe como saída de um processo opaco, sem correspondência auditável no artefato publicado. |

### PA-02 — Composição sobre Duplicação

| Campo | Conteúdo |
|---|---|
| Descrição | Elementos compartilhados entre múltiplas partes do projeto vivem em exatamente um lugar e são reaproveitados por composição, nunca copiados. |
| Motivação | Cópias divergem silenciosamente; composição a partir de uma única origem elimina essa possibilidade pela própria estrutura. |
| Consequências | Uma mudança em um elemento compartilhado se propaga automaticamente para todo lugar onde é usado. |
| Exemplos | Um elemento comum a todas as páginas, definido uma vez e incluído em todas. |
| Anti-exemplos | O mesmo bloco de conteúdo ou regra colado manualmente em vários lugares "só por enquanto". |

### PA-03 — Transparência de Execução

| Campo | Conteúdo |
|---|---|
| Descrição | O comportamento do sistema deve poder ser entendido lendo diretamente seus artefatos, sem depender de ferramentas especializadas ou de conhecimento não escrito. |
| Motivação | Um sistema que só se explica através de uma ferramenta específica cria dependência de quem sabe operar aquela ferramenta. |
| Consequências | Mecanismos diretos e legíveis são preferidos a abstrações que escondem o que de fato acontece. |
| Exemplos | Um comportamento que pode ser seguido passo a passo lendo o próprio código-fonte. |
| Anti-exemplos | Comportamento que só se manifesta em tempo de execução, sem nenhum rastro legível em um artefato. |

### PA-04 — Complexidade é Ganha, Não Herdada

| Campo | Conteúdo |
|---|---|
| Descrição | Nenhuma complexidade nova entra no projeto sem que seu benefício supere claramente seu custo. |
| Motivação | Complexidade acumulada sem crivo é a principal fonte de dívida técnica de longo prazo. |
| Consequências | Toda proposta que aumenta complexidade exige justificativa explícita e comparação com alternativas mais simples. |
| Exemplos | Adotar um mecanismo novo somente depois de demonstrar que o mecanismo atual não resolve o problema real. |
| Anti-exemplos | Introduzir uma camada nova "porque é o padrão do mercado", sem relação com um problema concreto do projeto. |

### PA-05 — Nenhuma Dependência Sem Propósito Declarado

| Campo | Conteúdo |
|---|---|
| Descrição | Toda dependência externa — de código, serviço ou infraestrutura — precisa ter um motivo documentado para existir. |
| Motivação | Cada dependência é um ponto de falha, de manutenção e de risco herdado pelo projeto inteiro. |
| Consequências | Dependências não utilizadas, ou sem justificativa clara, são removidas — não mantidas "por precaução". |
| Exemplos | Um serviço externo adicionado para resolver uma necessidade específica e registrada. |
| Anti-exemplos | Uma ferramenta instalada e nunca conectada a nada, permanecendo indefinidamente sem função nem justificativa revisitada. |

### PA-06 — O Conteúdo Deve Ser Legível por Qualquer Leitor

| Campo | Conteúdo |
|---|---|
| Descrição | Estrutura e conteúdo devem ser compreensíveis tanto por pessoas quanto por sistemas automatizados que os processam. |
| Motivação | O valor do projeto depende de ser corretamente interpretado por todo tipo de leitor, não só pelo modo de acesso mais comum no momento. |
| Consequências | Toda decisão de estrutura considera como o conteúdo será interpretado fora do contexto visual imediato. |
| Exemplos | Hierarquia de conteúdo clara e semântica, independente de qualquer estilo visual aplicado sobre ela. |
| Anti-exemplos | Informação que existe apenas como efeito visual, sem equivalente estrutural legível por quem não a "vê" da forma esperada. |

### PA-07 — Toda Superfície Pública é Superfície de Confiança

| Campo | Conteúdo |
|---|---|
| Descrição | Tudo que é exposto publicamente — incluindo metadados, pré-visualizações e mensagens de erro — é parte do produto e reflete sua credibilidade. |
| Motivação | A primeira impressão de um leitor ou de um sistema automatizado costuma se formar por essas superfícies, antes mesmo do conteúdo principal. |
| Consequências | Metadados e superfícies públicas recebem o mesmo padrão de qualidade e revisão que o conteúdo principal. |
| Exemplos | Uma pré-visualização de compartilhamento correta, verificada e mantida atualizada. |
| Anti-exemplos | Metadados configurados uma única vez e nunca mais verificados, apontando eventualmente para algo que deixou de existir. |

### PA-08 — Segurança é Constitutiva, Não Adicional

| Campo | Conteúdo |
|---|---|
| Descrição | Proteção de dados e integridade do sistema fazem parte do desenho original de qualquer funcionalidade, não uma camada aplicada depois. |
| Motivação | Segurança adicionada tardiamente é sistematicamente incompleta e cria uma falsa sensação de proteção. |
| Consequências | Nenhuma funcionalidade que lida com dado sensível é considerada pronta sem sua dimensão de segurança resolvida. |
| Exemplos | Uma funcionalidade desenhada desde o início considerando como seus dados serão protegidos em trânsito e em repouso. |
| Anti-exemplos | Uma funcionalidade lançada com a intenção declarada de "adicionar segurança depois". |

### PA-09 — Dado Pessoal Exige Rastro Auditável

| Campo | Conteúdo |
|---|---|
| Descrição | Todo dado pessoal coletado precisa ter um caminho documentado, do momento da coleta até seu destino final. |
| Motivação | Sem um rastro documentado, não é possível demonstrar conformidade nem responder a quem pergunte o que aconteceu com seu próprio dado. |
| Consequências | Nenhuma coleta de dado pessoal é aceita sem que seu tratamento completo esteja descrito em algum lugar auditável. |
| Exemplos | Um fluxo de dado pessoal documentado de ponta a ponta, incluindo onde e por quanto tempo é retido. |
| Anti-exemplos | Um dado pessoal enviado a um destino cujo comportamento não pode ser verificado nem descrito por este projeto. |

### PA-10 — Nada Muda Sem Deixar Rastro

| Campo | Conteúdo |
|---|---|
| Descrição | Toda alteração relevante ao projeto é acompanhada de um registro que explica o que mudou e por quê. |
| Motivação | A explicação de uma decisão é tão importante quanto a decisão em si — sem ela, o mesmo debate se repete indefinidamente no futuro. |
| Consequências | Uma mudança sem registro correspondente é tratada como incompleta, independentemente de funcionar tecnicamente. |
| Exemplos | Uma mudança de comportamento acompanhada de sua justificativa, disponível para quem vier depois. |
| Anti-exemplos | Uma mudança relevante cuja única explicação existe na memória de quem a fez. |

### PA-11 — Ambientes de Validação Existem para Ser Usados

| Campo | Conteúdo |
|---|---|
| Descrição | Nenhuma mudança chega ao ambiente público sem antes passar por um estágio de verificação equivalente. |
| Motivação | O custo de um erro já público é sempre maior do que o custo de verificá-lo antes de publicar. |
| Consequências | Atalhos que pulam a etapa de verificação são tratados como incidentes, nunca como conveniência aceitável. |
| Exemplos | Uma mudança validada em um ambiente equivalente ao público antes de ser promovida a ele. |
| Anti-exemplos | Uma alteração aplicada diretamente ao ambiente público "porque é pequena" ou "porque é urgente". |

### PA-12 — Código Morto é Dívida, Não Neutralidade

| Campo | Conteúdo |
|---|---|
| Descrição | Código, configuração ou conteúdo sem função ativa deve ser removido, não deixado "só por garantia". |
| Motivação | Elementos sem função confundem quem lê o projeto depois e podem ser reativados ou copiados por engano. |
| Consequências | A presença de algo no projeto é interpretada como sinal de que está em uso — o que não está em uso não deveria estar presente. |
| Exemplos | Remoção de um mecanismo desativado assim que se confirma que não tem mais função nenhuma. |
| Anti-exemplos | Manter um mecanismo desligado indefinidamente "para não quebrar nada", sem revisão periódica. |

### PA-13 — Consistência Visual é Contrato com o Usuário

| Campo | Conteúdo |
|---|---|
| Descrição | A identidade visual e de comportamento do projeto tem uma única fonte de definição, replicada de forma consistente em todas as suas partes. |
| Motivação | Inconsistência visual comunica descuido, mesmo quando o conteúdo por trás dela está correto. |
| Consequências | Qualquer variação de identidade precisa se justificar contra a fonte única, nunca coexistir como alternativa paralela permanente. |
| Exemplos | Um único conjunto de definições de identidade visual, referenciado por todo o projeto. |
| Anti-exemplos | Dois conjuntos de definição de identidade visual, ligeiramente diferentes, coexistindo sem que ninguém tenha decidido qual prevalece. |

### PA-14 — Acessibilidade é Pré-condição, Não Ajuste Posterior

| Campo | Conteúdo |
|---|---|
| Descrição | A capacidade de uso por pessoas com diferentes capacidades sensoriais, motoras ou cognitivas é parte da definição de "funcionando", não um retoque final. |
| Motivação | Tratar acessibilidade como etapa posterior garante, na prática, que ela nunca receba prioridade suficiente para ser bem feita. |
| Consequências | Uma funcionalidade sem consideração de acessibilidade não é considerada completa. |
| Exemplos | Navegação plenamente operável sem depender de um sentido ou dispositivo específico. |
| Anti-exemplos | Uma interface que funciona apenas de uma forma, com a intenção declarada de "melhorar acessibilidade depois". |

### PA-15 — Automação Substitui Disciplina Manual Onde For Confiável

| Campo | Conteúdo |
|---|---|
| Descrição | Verificações automatizáveis de forma confiável devem ser automatizadas; verificações que ainda dependem de julgamento humano continuam sendo feitas por humanos, deliberadamente. |
| Motivação | Disciplina manual é a forma mais frágil de garantir qualidade — funciona até que alguém esqueça, uma única vez. |
| Consequências | Um processo manual repetido sem variação é candidato natural a automação; uma automação sem confiabilidade comprovada não deve ser tratada como garantia. |
| Exemplos | Uma verificação repetitiva movida de um checklist manual para um mecanismo automatizado equivalente e confiável. |
| Anti-exemplos | Confiar cegamente em uma automação nunca validada, ou insistir manualmente em algo que já poderia ser automatizado com segurança. |

---

## DECISÕES INEGOCIÁVEIS

O que segue nunca deve ser violado, exceto mediante um novo registro formal de decisão que reconheça explicitamente a exceção e sua justificativa.

1. Toda alteração deve preservar a capacidade de o conteúdo ser encontrado e corretamente interpretado por quem o busca.
2. Toda alteração deve preservar — nunca reduzir — a capacidade de uso por pessoas com diferentes capacidades sensoriais, motoras ou cognitivas.
3. Toda alteração deve resultar em complexidade igual ou menor do que a existente, salvo justificativa explícita e registrada do ganho que compensa o aumento.
4. Nenhuma dependência nova é aceita sem propósito declarado e registrado.
5. Toda decisão arquitetural relevante — que afete estrutura, segurança, dado pessoal ou identidade do projeto — deve ter um registro de decisão correspondente.
6. Toda dívida técnica criada deve entrar em um backlog rastreável no momento em que é criada, não depois.
7. Toda alteração relevante deve ser documentada antes de ser considerada concluída.
8. Nenhuma alteração chega ao ambiente público sem passar por um estágio de validação anterior.
9. Nenhum dado pessoal é tratado sem que seu ciclo de vida completo esteja documentado e auditável.
10. Segurança e proteção de dados nunca são tratadas como etapa posterior de uma funcionalidade já lançada.
11. A estrutura pública — conteúdo, metadados, identidade — nunca é sacrificada por conveniência de implementação.

---

## COMO A ARQUITETURA EVOLUI

**Como novas funcionalidades devem nascer.** Toda funcionalidade nova começa por um problema real e documentado, não por uma capacidade técnica disponível. Antes de qualquer construção, a funcionalidade é avaliada contra os valores e princípios deste manifesto — se ela exige violar um deles, essa violação precisa ser reconhecida e justificada explicitamente, não silenciada.

**Como refatorações devem ocorrer.** Uma refatoração é sempre incremental e sempre reversível em cada um de seus passos. Ela não introduz comportamento novo — apenas melhora a forma de um comportamento já existente. Refatoração e mudança de funcionalidade não devem ser misturadas na mesma etapa, para que qualquer uma das duas possa ser revertida sem levar a outra junto.

**Como remover código legado.** Código legado é removido assim que se confirma, com evidência e não com suposição, que ele não tem mais função ativa. A remoção em si é tratada como uma mudança de baixo risco quando a evidência é sólida — o risco real está em manter, indefinidamente, algo cuja função ninguém mais consegue confirmar.

**Como eliminar dívida técnica.** Toda dívida técnica reconhecida entra em um backlog rastreável, com sua origem, seu risco e seu critério de conclusão explícitos. Dívida técnica não é eliminada por urgência ocasional — é eliminada seguindo a prioridade que o próprio projeto define para si, de forma consciente e revisitável.

**Como substituir tecnologias.** A substituição de uma tecnologia por outra é sempre uma decisão sobre meios, nunca sobre fins — o que este manifesto exige do resultado final não muda quando a tecnologia usada para alcançá-lo muda. Uma substituição só é aceitável quando demonstra que preserva, ou melhora, tudo o que os valores e princípios deste documento exigem hoje.

**Como preservar estabilidade.** Estabilidade não é ausência de mudança — é mudança que não surpreende. Toda mudança relevante é verificada em um estágio equivalente ao público antes de alcançá-lo, e toda mudança que altera comportamento existente é acompanhada de uma forma de confirmar, depois de aplicada, que nada além do pretendido mudou.

---

## COMO TOMAMOS DECISÕES

Objetivos legítimos entram em conflito com frequência. Quando isso acontece, a ordem de prioridade abaixo resolve o conflito — não porque os objetivos de prioridade menor não importem, mas porque alguma ordem precisa existir para que a decisão não dependa de quem está na sala no momento em que ela é tomada.

1. **Integridade e confiança** — a exatidão do que é afirmado, a proteção do dado pessoal e a segurança do sistema.
2. **Alcance e legibilidade universal** — a capacidade de ser encontrado e corretamente compreendido por qualquer tipo de leitor, humano ou não.
3. **Simplicidade e auditabilidade estrutural** — a capacidade de o sistema ser entendido e verificado por inteiro.
4. **Consistência** — a coerência visual e comportamental entre todas as partes do projeto.
5. **Desempenho** — a eficiência com que o sistema entrega o que promete.
6. **Conveniência e velocidade de execução** — a facilidade e rapidez de implementar algo.

Aplicando essa ordem aos conflitos citados com frequência:

- **Desempenho x Legibilidade** — legibilidade (posição 2) prevalece sobre desempenho (posição 5). Uma otimização que reduz a capacidade de compreensão do conteúdo por qualquer tipo de leitor não é aceitável, salvo se puder ser resolvida sem esse custo.
- **Alcance/SEO x Conveniência** — o alcance correto do conteúdo (posição 2) prevalece sobre a conveniência de implementação (posição 6). Um atalho que compromete como o conteúdo é encontrado ou interpretado não se justifica pela economia de esforço que proporciona.
- **Dependência nova x Simplicidade** — simplicidade (posição 3) prevalece sobre a conveniência trazida por uma nova dependência (posição 6), a menos que essa dependência sirva diretamente a um objetivo de prioridade mais alta (por exemplo, integridade ou segurança) de um jeito que a simplicidade sozinha não consegue alcançar.
- **Velocidade x Qualidade** — qualidade sustenta diretamente a integridade e a confiabilidade (posição 1) do sistema; velocidade de execução isolada (posição 6) nunca a substitui. Entregar mais rápido nunca é motivo suficiente para reduzir verificação.

Esta ordem não elimina o julgamento — ela dá a esse julgamento um ponto de partida comum, para que decisões tomadas em momentos diferentes, por pessoas diferentes, permaneçam coerentes entre si.

---

## PAPEL DA DOCUMENTAÇÃO

A documentação deste projeto não é um conjunto de artefatos independentes — é uma cadeia, em que cada elo responde a uma pergunta diferente e depende do elo anterior para fazer sentido.

- **O Manifesto** responde "por quê" — os princípios permanentes que não mudam com o tempo nem com a tecnologia. É o elo mais estável da cadeia e a referência final quando qualquer outro documento parecer contraditório.
- **O Roadmap** responde "o quê, em que ordem" — traduz os princípios do Manifesto em prioridades para um determinado ciclo de evolução do projeto. Muda com mais frequência que o Manifesto, mas nunca o contradiz.
- **O Backlog** responde "o quê, especificamente, e com que critério de conclusão" — decompõe o Roadmap em itens rastreáveis, individualmente executáveis e verificáveis.
- **Os Registros de Decisão (ADRs)** respondem "por que decidimos assim, e não de outra forma" — capturam o raciocínio por trás de uma escolha específica, no momento em que ela foi tomada, para que não precise ser reconstruído depois por suposição.
- **O Guia de Engenharia** responde "como, no dia a dia" — convenções práticas de como trabalhar dentro da arquitetura descrita pelos documentos anteriores.
- **A Definição de Pronto** responde "quando algo pode ser considerado concluído" — o critério objetivo, compartilhado, que evita que "pronto" signifique coisas diferentes para pessoas diferentes.
- **O Checklist de Revisão** responde "o que precisa ser conferido antes de aceitar uma mudança" — a última verificação, aplicada de forma consistente independentemente de quem revisa.

Cada um desses documentos é responsabilidade de quem toma decisões arquiteturais no projeto, mas sua atualização é responsabilidade de quem realiza a mudança que o afeta: quem decide algo relevante registra a decisão; quem cria uma dívida técnica a registra no backlog; quem muda uma convenção atualiza o guia correspondente. Documentação desatualizada é tratada como uma forma de dívida técnica, sujeita às mesmas regras de rastreamento das demais.

---

## PAPEL DA IA

Esta seção se aplica a qualquer agente de IA que leia, proponha ou implemente mudanças neste projeto.

Um agente de IA não decide arquitetura. Ele opera dentro da arquitetura definida por este manifesto e pelos documentos que dele derivam — não tem autoridade para estabelecer um novo princípio, um novo padrão estrutural ou uma nova prioridade que os contradiga.

Um agente de IA não cria novos padrões quando um padrão existente já resolve o problema. Antes de introduzir uma forma nova de fazer algo, o padrão já estabelecido no projeto deve ser considerado primeiro — e só ser descartado com justificativa explícita, documentada, para quem revisar a mudança depois.

Um agente de IA consulta a documentação existente antes de implementar. Isso inclui este manifesto, o roadmap vigente, o backlog rastreável e os registros de decisão relevantes ao que está sendo alterado. Implementar sem consultar é tratado como violação deste manifesto, independentemente de o resultado técnico estar correto.

Um agente de IA prefere evolução incremental. Mudanças propostas são as menores possíveis capazes de resolver o problema real, verificáveis isoladamente, nunca agrupadas de forma que dificulte entender o que mudou e por quê.

Um agente de IA preserva consistência. Ao tocar qualquer parte do projeto, segue as convenções já estabelecidas nessa parte, mesmo quando uma alternativa pareceria, isoladamente, melhor — introduzir uma exceção pontual custa mais em consistência do que ganha em otimização local, salvo quando essa exceção for deliberadamente registrada como o início de uma nova convenção.

Um agente de IA justifica mudanças relevantes. Toda alteração que não seja trivial é acompanhada de uma explicação do que mudou, por que mudou e o que foi considerado antes de decidir — na forma esperada pelo papel da documentação descrito acima.

Um agente de IA não substitui o julgamento humano em decisões que este manifesto reserva a pessoas — em particular, nada listado em "Decisões Inegociáveis" é contornado por um agente de IA sob a justificativa de eficiência ou automação.

---

## O QUE ESTE MANIFESTO NÃO É

- Não é um guia de programação. Não ensina como escrever código, nomear variáveis ou estruturar um arquivo — isso é papel do Guia de Engenharia.
- Não é um checklist. Não lista passos a seguir ou caixas a marcar antes de uma entrega — isso é papel da Definição de Pronto e do Checklist de Revisão.
- Não é um registro de decisão (ADR). Não explica por que uma escolha técnica específica foi feita em um momento específico — isso é papel dos ADRs.
- Não é um backlog. Não lista o que falta fazer, com que prioridade ou prazo — isso é papel do Roadmap e do Backlog.
- Não substitui a documentação técnica do projeto. Não descreve como o sistema é construído hoje, quais tecnologias usa ou como seus componentes se relacionam — isso é papel da documentação de arquitetura descritiva já existente.

Este documento responde a uma única pergunta, permanente: o que nunca deve deixar de ser verdade sobre como este projeto é pensado, independentemente de tudo o mais mudar.
