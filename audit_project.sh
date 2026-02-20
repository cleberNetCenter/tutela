#!/bin/bash

# ============================================================
# AUDITORIA ESTRUTURAL COMPLETA - ARQUITETURA MPA
# ============================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

REPORT_FILE="audit_report_$(date +%Y%m%d_%H%M%S).txt"

# Contadores
CRITICAL_ERRORS=0
PATH_ERRORS=0
SPA_RESIDUES=0
DUPLICATE_SCRIPTS=0
TOTAL_ERRORS=0

echo "============================================================" | tee -a "$REPORT_FILE"
echo "  AUDITORIA ESTRUTURAL COMPLETA - ARQUITETURA MPA" | tee -a "$REPORT_FILE"
echo "  Data: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$REPORT_FILE"
echo "============================================================" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# ============================================================
# ETAPA 1 — VALIDAR ESTRUTURA DE ARQUIVOS
# ============================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT_FILE"
echo "ETAPA 1 — VALIDAÇÃO DA ESTRUTURA DE ARQUIVOS" | tee -a "$REPORT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

echo "1.1 — Verificando arquivos OBRIGATÓRIOS:" | tee -a "$REPORT_FILE"

REQUIRED_FILES=(
  "public/assets/js/navigation-controller.js"
  "public/assets/js/i18n.js"
  "public/assets/lang/pt.json"
  "public/assets/lang/en.json"
  "public/assets/lang/es.json"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "  ✅ $file" | tee -a "$REPORT_FILE"
  else
    echo -e "  ${RED}❌ ERRO CRÍTICO: $file NÃO ENCONTRADO${NC}" | tee -a "$REPORT_FILE"
    ((CRITICAL_ERRORS++))
  fi
done

echo "" | tee -a "$REPORT_FILE"
echo "1.2 — Verificando arquivos PROIBIDOS (legado SPA):" | tee -a "$REPORT_FILE"

FORBIDDEN_FILES=(
  "public/assets/js/navigation.js"
  "public/assets/js/mobile-menu.js"
  "public/assets/js/dropdown-menu.js"
)

for file in "${FORBIDDEN_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo -e "  ${RED}❌ ERRO CRÍTICO: $file AINDA EXISTE (DEVE SER REMOVIDO)${NC}" | tee -a "$REPORT_FILE"
    ((CRITICAL_ERRORS++))
  else
    echo "  ✅ $file (corretamente removido)" | tee -a "$REPORT_FILE"
  fi
done

echo "" | tee -a "$REPORT_FILE"

# ============================================================
# ETAPA 2 — VARREDURA EM TODOS OS HTML
# ============================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT_FILE"
echo "ETAPA 2 — VARREDURA EM TODOS OS ARQUIVOS HTML" | tee -a "$REPORT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# Encontrar todos os HTML (exceto testes)
HTML_FILES=$(find public -name "*.html" -type f ! -path "*/test*" ! -path "*/debug*" | sort)
HTML_COUNT=$(echo "$HTML_FILES" | wc -l)

echo "📄 Total de arquivos HTML a auditar: $HTML_COUNT" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

echo "2.1 — Verificando SCRIPTS PROIBIDOS:" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

FORBIDDEN_SCRIPTS_FOUND=0

for html in $HTML_FILES; do
  # Verificar navigation.js
  if grep -q "navigation\.js" "$html" 2>/dev/null; then
    echo -e "  ${RED}❌ ERRO: $html contém referência a 'navigation.js'${NC}" | tee -a "$REPORT_FILE"
    grep -n "navigation\.js" "$html" | head -3 | tee -a "$REPORT_FILE"
    ((CRITICAL_ERRORS++))
    ((FORBIDDEN_SCRIPTS_FOUND++))
  fi
  
  # Verificar mobile-menu.js
  if grep -q "mobile-menu\.js" "$html" 2>/dev/null; then
    echo -e "  ${RED}❌ ERRO: $html contém referência a 'mobile-menu.js'${NC}" | tee -a "$REPORT_FILE"
    grep -n "mobile-menu\.js" "$html" | head -3 | tee -a "$REPORT_FILE"
    ((CRITICAL_ERRORS++))
    ((FORBIDDEN_SCRIPTS_FOUND++))
  fi
  
  # Verificar dropdown-menu.js
  if grep -q "dropdown-menu\.js" "$html" 2>/dev/null; then
    echo -e "  ${RED}❌ ERRO: $html contém referência a 'dropdown-menu.js'${NC}" | tee -a "$REPORT_FILE"
    grep -n "dropdown-menu\.js" "$html" | head -3 | tee -a "$REPORT_FILE"
    ((CRITICAL_ERRORS++))
    ((FORBIDDEN_SCRIPTS_FOUND++))
  fi
done

if [ $FORBIDDEN_SCRIPTS_FOUND -eq 0 ]; then
  echo "  ✅ Nenhum script proibido encontrado" | tee -a "$REPORT_FILE"
fi

echo "" | tee -a "$REPORT_FILE"

# 2.2 — CAMINHOS RELATIVOS INCORRETOS
echo "2.2 — Verificando CAMINHOS RELATIVOS INCORRETOS:" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

RELATIVE_PATH_ERRORS=0

for html in $HTML_FILES; do
  # Verificar src="assets/ (sem barra inicial)
  if grep -q 'src="assets/' "$html" 2>/dev/null; then
    echo -e "  ${YELLOW}⚠️  ERRO DE PATH: $html contém src=\"assets/\" (falta \"/\")${NC}" | tee -a "$REPORT_FILE"
    grep -n 'src="assets/' "$html" | head -3 | tee -a "$REPORT_FILE"
    ((PATH_ERRORS++))
    ((RELATIVE_PATH_ERRORS++))
  fi
  
  # Verificar href="assets/ (sem barra inicial)
  if grep -q 'href="assets/' "$html" 2>/dev/null; then
    echo -e "  ${YELLOW}⚠️  ERRO DE PATH: $html contém href=\"assets/\" (falta \"/\")${NC}" | tee -a "$REPORT_FILE"
    grep -n 'href="assets/' "$html" | head -3 | tee -a "$REPORT_FILE"
    ((PATH_ERRORS++))
    ((RELATIVE_PATH_ERRORS++))
  fi
  
  # Verificar ../assets/ (path relativo com ..)
  if grep -q '\.\./assets/' "$html" 2>/dev/null; then
    echo -e "  ${YELLOW}⚠️  ERRO DE PATH: $html contém \"../assets/\" (deve ser \"/assets/\")${NC}" | tee -a "$REPORT_FILE"
    grep -n '\.\./assets/' "$html" | head -3 | tee -a "$REPORT_FILE"
    ((PATH_ERRORS++))
    ((RELATIVE_PATH_ERRORS++))
  fi
done

if [ $RELATIVE_PATH_ERRORS -eq 0 ]; then
  echo "  ✅ Nenhum caminho relativo incorreto encontrado" | tee -a "$REPORT_FILE"
fi

echo "" | tee -a "$REPORT_FILE"

# 2.3 — SCRIPTS DUPLICADOS
echo "2.3 — Verificando SCRIPTS DUPLICADOS DE NAVEGAÇÃO:" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

DUPLICATE_FOUND=0

for html in $HTML_FILES; do
  # Contar quantas vezes document.addEventListener('click' aparece
  CLICK_COUNT=$(grep -c "document\.addEventListener('click'" "$html" 2>/dev/null || echo 0)
  
  if [ "$CLICK_COUNT" -gt 1 ]; then
    echo -e "  ${YELLOW}⚠️  DUPLICAÇÃO: $html tem $CLICK_COUNT listeners 'click'${NC}" | tee -a "$REPORT_FILE"
    ((DUPLICATE_SCRIPTS++))
    ((DUPLICATE_FOUND++))
  fi
  
  # Contar quantas vezes DOMContentLoaded aparece
  DOM_COUNT=$(grep -c "DOMContentLoaded" "$html" 2>/dev/null || echo 0)
  
  if [ "$DOM_COUNT" -gt 2 ]; then  # Permitir 2 (i18n.js + navigation-controller.js)
    echo -e "  ${YELLOW}⚠️  DUPLICAÇÃO: $html tem $DOM_COUNT listeners 'DOMContentLoaded' (esperado: 2)${NC}" | tee -a "$REPORT_FILE"
    ((DUPLICATE_SCRIPTS++))
    ((DUPLICATE_FOUND++))
  fi
done

if [ $DUPLICATE_FOUND -eq 0 ]; then
  echo "  ✅ Nenhuma duplicação de scripts detectada" | tee -a "$REPORT_FILE"
fi

echo "" | tee -a "$REPORT_FILE"

# 2.4 — ORDEM DE CARREGAMENTO CORRETA
echo "2.4 — Verificando ORDEM DE CARREGAMENTO DOS SCRIPTS:" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

SCRIPT_ORDER_ERRORS=0

for html in $HTML_FILES; do
  # Extrair últimas linhas antes do </body>
  SCRIPT_SECTION=$(grep -B5 "</body>" "$html" | grep -E "i18n\.js|navigation-controller\.js")
  
  # Verificar se i18n.js vem ANTES de navigation-controller.js
  I18N_LINE=$(grep -n "i18n\.js" "$html" | tail -1 | cut -d: -f1)
  NAV_CONTROLLER_LINE=$(grep -n "navigation-controller\.js" "$html" | tail -1 | cut -d: -f1)
  
  if [ -n "$I18N_LINE" ] && [ -n "$NAV_CONTROLLER_LINE" ]; then
    if [ "$I18N_LINE" -gt "$NAV_CONTROLLER_LINE" ]; then
      echo -e "  ${RED}❌ ERRO DE ORDEM: $html - navigation-controller.js (linha $NAV_CONTROLLER_LINE) ANTES de i18n.js (linha $I18N_LINE)${NC}" | tee -a "$REPORT_FILE"
      ((CRITICAL_ERRORS++))
      ((SCRIPT_ORDER_ERRORS++))
    else
      echo "  ✅ $html - ordem correta (i18n.js → navigation-controller.js)" | tee -a "$REPORT_FILE"
    fi
  elif [ -z "$I18N_LINE" ]; then
    echo -e "  ${RED}❌ ERRO: $html - i18n.js NÃO ENCONTRADO${NC}" | tee -a "$REPORT_FILE"
    ((CRITICAL_ERRORS++))
  elif [ -z "$NAV_CONTROLLER_LINE" ]; then
    echo -e "  ${RED}❌ ERRO: $html - navigation-controller.js NÃO ENCONTRADO${NC}" | tee -a "$REPORT_FILE"
    ((CRITICAL_ERRORS++))
  fi
done

echo "" | tee -a "$REPORT_FILE"

# ============================================================
# ETAPA 3 — AUDITORIA DO i18n.js
# ============================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT_FILE"
echo "ETAPA 3 — AUDITORIA DO i18n.js (FETCH ABSOLUTO)" | tee -a "$REPORT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

I18N_FILE="public/assets/js/i18n.js"

if [ -f "$I18N_FILE" ]; then
  # Verificar fetch relativo incorreto
  if grep -q 'fetch(`assets/lang/' "$I18N_FILE" 2>/dev/null; then
    echo -e "  ${RED}❌ ERRO CRÍTICO: $I18N_FILE usa fetch RELATIVO 'assets/lang/'${NC}" | tee -a "$REPORT_FILE"
    grep -n 'fetch(`assets/lang/' "$I18N_FILE" | tee -a "$REPORT_FILE"
    ((CRITICAL_ERRORS++))
  elif grep -q 'fetch("/assets/lang/' "$I18N_FILE" 2>/dev/null || grep -q "fetch(\`/assets/lang/" "$I18N_FILE" 2>/dev/null; then
    echo "  ✅ i18n.js usa fetch ABSOLUTO '/assets/lang/'" | tee -a "$REPORT_FILE"
    grep -n 'fetch(' "$I18N_FILE" | grep lang | head -2 | tee -a "$REPORT_FILE"
  else
    echo -e "  ${YELLOW}⚠️  AVISO: Não foi possível detectar fetch em i18n.js${NC}" | tee -a "$REPORT_FILE"
  fi
else
  echo -e "  ${RED}❌ ERRO CRÍTICO: $I18N_FILE NÃO ENCONTRADO${NC}" | tee -a "$REPORT_FILE"
  ((CRITICAL_ERRORS++))
fi

echo "" | tee -a "$REPORT_FILE"

# ============================================================
# ETAPA 4 — DETECTAR RESQUÍCIOS SPA
# ============================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT_FILE"
echo "ETAPA 4 — DETECTAR RESQUÍCIOS DE ARQUITETURA SPA" | tee -a "$REPORT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

SPA_PATTERNS=(
  "navigateTo("
  ".page.active"
  "history.pushState"
  "history.replaceState"
  "data-page="
  "page-container"
  "initNavigation("
)

SPA_RESIDUE_FOUND=0

for pattern in "${SPA_PATTERNS[@]}"; do
  echo "🔍 Procurando por: $pattern" | tee -a "$REPORT_FILE"
  
  MATCHES=$(grep -rn "$pattern" public/*.html public/*/*.html 2>/dev/null | grep -v test | grep -v debug || true)
  
  if [ -n "$MATCHES" ]; then
    echo -e "  ${RED}❌ RESQUÍCIO SPA DETECTADO:${NC}" | tee -a "$REPORT_FILE"
    echo "$MATCHES" | head -5 | tee -a "$REPORT_FILE"
    ((SPA_RESIDUES++))
    ((SPA_RESIDUE_FOUND++))
  else
    echo "  ✅ Nenhum resquício detectado" | tee -a "$REPORT_FILE"
  fi
  echo "" | tee -a "$REPORT_FILE"
done

if [ $SPA_RESIDUE_FOUND -eq 0 ]; then
  echo "✅ ARQUITETURA MPA PURA - Sem resquícios SPA" | tee -a "$REPORT_FILE"
fi

echo "" | tee -a "$REPORT_FILE"

# ============================================================
# ETAPA 5 — DETECTAR PATHS INCORRETOS EM /legal/
# ============================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT_FILE"
echo "ETAPA 5 — DETECTAR PATHS INCORRETOS EM /legal/" | tee -a "$REPORT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

LEGAL_HTML_FILES=$(find public/legal -name "*.html" -type f 2>/dev/null || true)
LEGAL_PATH_ERRORS=0

if [ -z "$LEGAL_HTML_FILES" ]; then
  echo "⚠️  Nenhum arquivo HTML encontrado em public/legal/" | tee -a "$REPORT_FILE"
else
  for legal_html in $LEGAL_HTML_FILES; do
    # Verificar se tenta carregar /legal/assets/
    if grep -q '/legal/assets/' "$legal_html" 2>/dev/null; then
      echo -e "  ${RED}❌ ERRO DE PATH: $legal_html tenta carregar '/legal/assets/' (INCORRETO)${NC}" | tee -a "$REPORT_FILE"
      grep -n '/legal/assets/' "$legal_html" | head -3 | tee -a "$REPORT_FILE"
      ((PATH_ERRORS++))
      ((LEGAL_PATH_ERRORS++))
    fi
    
    # Verificar se usa caminho relativo correto (/assets/)
    if grep -q '"/assets/' "$legal_html" 2>/dev/null || grep -q "'/assets/" "$legal_html" 2>/dev/null; then
      echo "  ✅ $legal_html usa '/assets/' (correto)" | tee -a "$REPORT_FILE"
    fi
  done
  
  if [ $LEGAL_PATH_ERRORS -eq 0 ]; then
    echo "✅ Nenhum path incorreto em /legal/" | tee -a "$REPORT_FILE"
  fi
fi

echo "" | tee -a "$REPORT_FILE"

# ============================================================
# ETAPA 6 — RELATÓRIO FINAL
# ============================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT_FILE"
echo "RELATÓRIO FINAL - RESUMO DA AUDITORIA" | tee -a "$REPORT_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

TOTAL_ERRORS=$((CRITICAL_ERRORS + PATH_ERRORS + SPA_RESIDUES + DUPLICATE_SCRIPTS))

echo "📊 ESTATÍSTICAS:" | tee -a "$REPORT_FILE"
echo "  • Arquivos HTML auditados: $HTML_COUNT" | tee -a "$REPORT_FILE"
echo "  • Erros críticos: $CRITICAL_ERRORS" | tee -a "$REPORT_FILE"
echo "  • Erros de path: $PATH_ERRORS" | tee -a "$REPORT_FILE"
echo "  • Resquícios SPA: $SPA_RESIDUES" | tee -a "$REPORT_FILE"
echo "  • Scripts duplicados: $DUPLICATE_SCRIPTS" | tee -a "$REPORT_FILE"
echo "  ────────────────────────────" | tee -a "$REPORT_FILE"
echo "  • TOTAL DE ERROS: $TOTAL_ERRORS" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

if [ $TOTAL_ERRORS -eq 0 ]; then
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}" | tee -a "$REPORT_FILE"
  echo -e "${GREEN}   ✅ APROVADO — ARQUITETURA CONSISTENTE${NC}" | tee -a "$REPORT_FILE"
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}" | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
  echo "✅ Nenhum 404 esperado" | tee -a "$REPORT_FILE"
  echo "✅ Nenhum caminho relativo incorreto" | tee -a "$REPORT_FILE"
  echo "✅ Nenhum SPA legado" | tee -a "$REPORT_FILE"
  echo "✅ Nenhum script duplicado" | tee -a "$REPORT_FILE"
  echo "✅ Estrutura MPA pura" | tee -a "$REPORT_FILE"
  echo "✅ Controller único" | tee -a "$REPORT_FILE"
else
  echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}" | tee -a "$REPORT_FILE"
  echo -e "${RED}   ❌ REPROVADO — NECESSITA CORREÇÃO${NC}" | tee -a "$REPORT_FILE"
  echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}" | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
  echo "⚠️  Foram detectados $TOTAL_ERRORS erros que precisam ser corrigidos." | tee -a "$REPORT_FILE"
fi

echo "" | tee -a "$REPORT_FILE"
echo "📄 Relatório salvo em: $REPORT_FILE" | tee -a "$REPORT_FILE"
echo "============================================================" | tee -a "$REPORT_FILE"

# Retornar código de saída baseado no resultado
if [ $TOTAL_ERRORS -eq 0 ]; then
  exit 0
else
  exit 1
fi

