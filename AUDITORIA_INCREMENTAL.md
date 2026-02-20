# Auditoria Incremental de Arquitetura

- Data: 2026-02-20 21:11 UTC
- Escopo: `public/assets/lang/*.json`, `validate_hierarchy.py`, scripts de auditoria Node.

## Resultado

⚠️ 6 regressão(ões) detectada(s).

## Achados

1. **[HIGH] i18n-schema**
   - Resumo: en.json perdeu seções de arquitetura presentes em pt.json
   - Evidência: Seções ausentes: institucional, institutional, legalBasis, preservation, privacy, terms

2. **[HIGH] i18n-coverage**
   - Resumo: Cobertura de chaves de en.json abaixo do limite mínimo (80%)
   - Evidência: Cobertura atual: 63.2% (146/231)

3. **[HIGH] i18n-schema**
   - Resumo: es.json perdeu seções de arquitetura presentes em pt.json
   - Evidência: Seções ausentes: institucional, institutional, legalBasis, preservation, privacy, terms

4. **[HIGH] i18n-coverage**
   - Resumo: Cobertura de chaves de es.json abaixo do limite mínimo (80%)
   - Evidência: Cobertura atual: 63.2% (146/231)

5. **[MEDIUM] validation-tooling**
   - Resumo: Validador aponta para página inexistente
   - Evidência: public/fundamento-juridico.html

6. **[MEDIUM] validation-tooling**
   - Resumo: Validador aponta para página inexistente
   - Evidência: public/preservacao-probatoria-digital.html
