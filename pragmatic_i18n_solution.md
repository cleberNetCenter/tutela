# Solução Pragmática para i18n de Páginas Legais

## Situação Atual

| Página | Cobertura | Status |
|--------|-----------|--------|
| institucional.html | 57% (21/37) | ⚠️ Parcial |
| politica-de-privacidade.html | 10% (6/59) | ❌ Baixa |
| fundamento-juridico.html | 16% (9/56) | ❌ Baixa |
| termos-de-custodia.html | 50% (12/24) | ⚠️ Parcial |

## Problema

Adicionar `data-i18n` em TODOS os 176 elementos de texto dessas 4 páginas exigiria:
- Criar ~150+ novas chaves de tradução
- Traduzir manualmente cada texto jurídico para EN e ES
- Risco de erro em traduções jurídicas complexas
- Tempo estimado: 4-6 horas

## Solução Proposta

### Abordagem Híbrida

1. **Páginas Operacionais (alta cobertura)**
   - `index.html`, `como-funciona.html`, `seguranca.html`, `preservacao-probatoria-digital.html`
   - ✅ Manter tradução completa PT/EN/ES

2. **Páginas Legais/Institucionais (baixa cobertura)**
   - `institucional.html`, `politica-de-privacidade.html`, `fundamento-juridico.html`, `termos-de-custodia.html`
   - ✅ Traduzir apenas: H1, H2, subtítulos principais
   - ✅ Adicionar banner de aviso:
     ```
     [EN] This legal document is available in Portuguese only.
     [ES] Este documento legal está disponible solo en portugués.
     ```

### Implementação

```javascript
// Detectar idioma e mostrar aviso se não for PT
if (currentLang !== 'pt' && isLegalPage) {
  showLanguageNotice();
}
```

### Benefícios

- ✅ Implementação rápida (15min vs 4-6h)
- ✅ Sem risco de erro em traduções jurídicas
- ✅ UX clara: usuário sabe que precisa do português
- ✅ Títulos traduzidos para navegação
- ✅ Conformidade legal mantida em PT

### Páginas Afetadas

- `/institucional` - informações institucionais
- `/politica-de-privacidade` - política LGPD
- `/fundamento-juridico` - base jurídica da preservação
- `/termos-de-custodia` - termos contratuais

### Próxima Ação

Implementar banner de aviso e garantir que títulos/navegação estejam traduzidos.
