# Sitemap - Homolog Environment

**Data de Análise:** 2026-04-09  
**Total de Páginas:** 34  
**Páginas Órfãs:** 8  
**Taxa de Cobertura:** ~76%  

---

## 📍 Ponto de Entrada

| URL | Descrição | Status |
|-----|-----------|--------|
| `/` | Homepage | ✓ Entry Point |

---

## 🏛️ Hubs Principais

| URL | Descrição | Status | Referências |
|-----|-----------|--------|-------------|
| `/insights/` | Hub central de conteúdo jurídico | ✓ Linked | 7 |
| `/ativos-digitais/` | Hub de estrutura jurídica de ativos | ✓ Linked | 4 |
| `/prova-digital-validade-juridica/` | Hub de validade jurídica | ❌ Orphan | 6 |

---

## 📚 Pilares - Prova Digital

**Hub:** `/insights/prova-digital/`  
**Status:** ✓ Linked  
**Artigos:** 5

| URL | Tipo |
|-----|------|
| `/insights/prova-digital/cadeia-custodia-prova-digital.html` | Artigo |
| `/insights/prova-digital/hash-criptografico-temporalidade.html` | Artigo |
| `/insights/prova-digital/integridade-tecnica-admissibilidade.html` | Artigo |
| `/insights/prova-digital/producao-antecipada-prova-digital.html` | Artigo |
| `/insights/prova-digital/prova-digital-processo-civil-brasileiro.html` | Artigo |

---

## 📚 Pilares - Ativos Digitais

**Hub:** `/insights/ativos-digitais/`  
**Status:** ✓ Linked  
**Artigos:** 5

| URL | Tipo | Status |
|-----|------|--------|
| `/insights/ativos-digitais/compliance-lgpd.html` | Artigo | ✓ |
| `/insights/ativos-digitais/custodia-ativos-digitais.html` | Artigo | ✓ |
| `/insights/ativos-digitais/marco-regulatorio.html` | Artigo | ✓ |
| `/insights/ativos-digitais/o-que-sao-ativos-digitais.html` | Artigo | ❌ Orphan |
| `/insights/ativos-digitais/sucessao-digital.html` | Artigo | ✓ |

---

## 🏛️ Estrutura - Ativos Digitais

| URL | Descrição | Status | Links |
|-----|-----------|--------|-------|
| `/ativos-digitais/estrutura-juridica/` | Estrutura jurídica | ✓ Linked | - |
| `/ativos-digitais/heranca-digital/` | Herança digital | ❌ Orphan | 5 |
| `/ativos-digitais/protecao-e-riscos/` | Proteção e riscos | ❌ Orphan | - |
| `/ativos-digitais/prova-digital-judicial/` | Prova digital judicial | ❌ Orphan | 7 |

---

## ⚖️ Legal & Institucional

| URL | Descrição | Status |
|-----|-----------|--------|
| `/legal/preservacao-probatoria-digital.html` | Preservação probatória | ✓ Linked |
| `/legal/arquitetura-juridica-prova-digital.html` | Arquitetura jurídica | ✓ Linked |
| `/legal/fundamento-juridico.html` | Fundamento jurídico | ✓ Linked |
| `/legal/institucional.html` | Informações institucionais | ✓ Linked |
| `/legal/politica-de-privacidade.html` | Política de Privacidade | ✓ Linked |
| `/legal/termos-de-custodia.html` | Termos de Custódia | ✓ Linked |
| `/legal/termos-de-uso.html` | Termos de Uso | ❌ Orphan |

---

## 🌐 Páginas de Navegação

| URL | Descrição | Status |
|-----|-----------|--------|
| `/como-funciona.html` | Como Funciona | ✓ Linked |
| `/contato/` | Contato | ❌ Orphan |
| `/diagnostico.html` | Diagnóstico | ✓ Linked |
| `/empresas.html` | Para Empresas | ✓ Linked |
| `/governo.html` | Para Governo | ✓ Linked |
| `/pessoas.html` | Para Pessoas | ✓ Linked |
| `/seguranca.html` | Segurança | ❌ Orphan |

---

## ⚠️ Páginas Órfãs (Não Referenciadas)

### Crítico - Sem Ligações Internas (8 páginas)

1. **`/ativos-digitais/heranca-digital/`**
   - Tipo: Hub Secundário
   - Problema: Página existe e contém 5 links internos, mas não é referenciada por nenhuma outra página
   - Impacto: Inacessível sem navegação direta / URL
   - Recomendação: Adicionar referências em `/ativos-digitais/` ou em `/insights/ativos-digitais/`

2. **`/ativos-digitais/protecao-e-riscos/`**
   - Tipo: Hub Secundário
   - Problema: Página órfã
   - Impacto: Inacessível via navegação
   - Recomendação: Criar links de navegação

3. **`/ativos-digitais/prova-digital-judicial/`**
   - Tipo: Hub Secundário
   - Problema: Página órfã (contém 7 links internos)
   - Impacto: Estrutura interna pronta mas desconectada
   - Recomendação: Integrar com `/insights/prova-digital/`

4. **`/contato/`**
   - Tipo: Página de Navegação
   - Problema: Não referenciada (deveria estar em footer/header)
   - Impacto: Inacessível via navegação estruturada
   - Recomendação: Adicionar em header/footer via partial

5. **`/insights/ativos-digitais/o-que-sao-ativos-digitais.html`**
   - Tipo: Artigo
   - Problema: Não listado no hub de insights de ativos digitais
   - Impacto: Artigo criado mas não descobrível
   - Recomendação: Adicionar ao td-articles section em `/insights/ativos-digitais/`

6. **`/legal/termos-de-uso.html`**
   - Tipo: Legal
   - Problema: Não referenciada (deveria estar em footer legal)
   - Impacto: Página legal inacessível
   - Recomendação: Adicionar em footer via partial

7. **`/prova-digital-validade-juridica/`**
   - Tipo: Hub Secundário
   - Problema: Página existe com 6 links internos, mas não é referenciada
   - Impacto: Hub conceitual desconectado
   - Recomendação: Integrar como subcategoria de `/insights/prova-digital/` ou criar link desde homepage

8. **`/seguranca.html`**
   - Tipo: Página de Navegação
   - Problema: Não referenciada por nenhuma página principal
   - Impacto: Conteúdo de segurança inacessível
   - Recomendação: Adicionar link em header/footer ou homepage

---

## 📊 Análise de Topologia

### Páginas com Maior Número de Links Internos

| URL | Contagem | Categoria |
|-----|----------|-----------|
| `/legal/arquitetura-juridica-prova-digital.html` | 10 | Legal/Núcleo |
| `/legal/preservacao-probatoria-digital.html` | 9 | Legal/Núcleo |
| `/legal/fundamento-juridico.html` | 8 | Legal/Núcleo |
| `/legal/termos-de-custodia.html` | 7 | Legal/Núcleo |
| `/prova-digital-validade-juridica/` | 6 | Hub Órfão |
| `/ativos-digitais/prova-digital-judicial/` | 7 | Hub Órfão |

### Observações

- **Páginas Legais são Hubs:** As páginas em `/legal/` funcionam como centros de distribuição de links (8-10 cada)
- **Hubs Órfãos de Ativos:** Tanto `/ativos-digitais/heranca-digital/` quanto `/ativos-digitais/prova-digital-judicial/` possuem estruturas de links mas não são descobríveis
- **Ausência de Footer/Header Dinâmico:** Páginas importantes como `/contato/`, `/seguranca.html`, `/legal/termos-de-uso.html` deveriam estar em partials compartilhados

---

## 🔴 Problemas Identificados

### Alta Prioridade

1. **Desestruturação de Ativos Digitais**
   - `/ativos-digitais/heranca-digital/`, `/ativos-digitais/protecao-e-riscos/`, `/ativos-digitais/prova-digital-judicial/` existem mas não são ligadas
   - Solução: Mapear estas páginas em `/ativos-digitais/index.html`

2. **Artigo Órfão em Insights**
   - `/insights/ativos-digitais/o-que-sao-ativos-digitais.html` não aparece no hub
   - Solução: Adicionar ao grid de artigos em `/insights/ativos-digitais/index.html`

3. **Hub Desconectado**
   - `/prova-digital-validade-juridica/` existe mas não é referenciado de nenhuma página principal
   - Solução: Converter em subcategoria de `/insights/prova-digital/` ou adicionar ao menu principal

### Média Prioridade

4. **Páginas de Navegação Órfãs**
   - `/contato/`, `/seguranca.html` e `/legal/termos-de-uso.html` deveriam estar acessíveis via footer/header
   - Solução: Adicionar links em `partials/footer.html` e `partials/header.html`

5. **Inconsistência de Navegação**
   - Algumas páginas do tipo "hub" têm links internos mas não são descobríveis
   - Solução: Revisar partials e criar mapa de navegação global

---

## ✅ Recomendações de Ação

### Curto Prazo (Imediato)

- [ ] Adicionar `/ativos-digitais/heranca-digital/`, `/protecao-e-riscos/`, `/prova-digital-judicial/` ao menu de `/ativos-digitais/index.html`
- [ ] Adicionar [`/insights/ativos-digitais/o-que-sao-ativos-digitais.html`] ao grid de artigos em `/insights/ativos-digitais/index.html`
- [ ] Incluir `/legal/termos-de-uso.html` e `/contato/` em `partials/footer.html`
- [ ] Gerar links para `/seguranca.html` em header ou dentro de páginas legais relevantes

### Médio Prazo

- [ ] Revisar estratégia de `/prova-digital-validade-juridica/` - integrar ou manter como hub autônomo com links apropriados
- [ ] Consolidar estrutura de Ativos Digitais: definir hierarquia clara entre pilares e artigos
- [ ] Implementar mapa do site XML para cobertura completa

### Longo Prazo

- [ ] Auditar links depois de cada alteração estrutural
- [ ] Implementar teste automatizado de cobertura de links
- [ ] Documentar estrutura esperada de navegação

---

## 📋 Resumo Executivo

A estrutura do homolog contenha **34 páginas** organizadas em **4 camadas**:

1. **Camada 1 (Homepage):** `/` - Linked ✓
2. **Camada 2 (Hubs):** `/insights/`, `/ativos-digitais/`, `/prova-digital-validade-juridica/` (Orphan)
3. **Camada 3 (Pilares):** Prova Digital e Ativos Digitais com artigos secundários
4. **Camada 4 (Legal):** Páginas de conformidade, termos e política; mostly linked mas 1 orphan

**Taxa de Connectividade:** ~76% (26/34 páginas referenciadas)

**Problema Principal:** 8 páginas órfãs (24%) não são descobríveis via navegação estruturada. Destas, 3 são hubs secundários com estrutura interna completa mas desconectadas do mapa de navegação principal.

**Estado Geral:** Estrutura de conteúdo robusta mas com falhas críticas de navegação interna. Recomenda-se mapear todos os hubs órfãos antes de publicação em produção.

---

*Gerado automaticamente em 2026-04-09 via análise estrutural do repositório*
