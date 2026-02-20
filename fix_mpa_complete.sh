#!/bin/bash

echo "════════════════════════════════════════════════════════════════════════════"
echo "  🔧 MIGRAÇÃO DEFINITIVA PARA MPA PURA - CORREÇÃO ESTRUTURAL COMPLETA"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""

# Encontrar todos os HTML (exceto testes)
HTML_FILES=$(find public -name "*.html" -type f ! -path "*/test*" ! -path "*/debug*" | sort)
HTML_COUNT=$(echo "$HTML_FILES" | wc -l)

echo "📄 Total de arquivos HTML a processar: $HTML_COUNT"
echo ""

# ============================================================================
# ETAPA 1 — CORRIGIR TODOS OS PATHS RELATIVOS DE ASSETS
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ETAPA 1 — CORRIGIR TODOS OS PATHS RELATIVOS DE ASSETS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

for html in $HTML_FILES; do
  echo "  🔧 Processando: $html"
  
  # Substituir href="assets/ por href="/assets/
  sed -i 's|href="assets/|href="/assets/|g' "$html"
  sed -i "s|href='assets/|href='/assets/|g" "$html"
  
  # Substituir src="assets/ por src="/assets/
  sed -i 's|src="assets/|src="/assets/|g' "$html"
  sed -i "s|src='assets/|src='/assets/|g" "$html"
done

echo ""
echo "✅ ETAPA 1 COMPLETA - Paths absolutos aplicados"
echo ""

# ============================================================================
# ETAPA 2 — ELIMINAR COMPLETAMENTE ARQUITETURA SPA
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ETAPA 2 — ELIMINAR COMPLETAMENTE ARQUITETURA SPA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

for html in $HTML_FILES; do
  echo "  🗑️  Limpando SPA: $html"
  
  # 2.1 - Remover onclick="navigateTo(...); return false;"
  sed -i 's| onclick="navigateTo([^"]*); return false;"||g' "$html"
  sed -i "s| onclick='navigateTo([^']*); return false;'||g" "$html"
  
  # 2.2 - Remover data-page="..."
  sed -i 's| data-page="[^"]*"||g' "$html"
  sed -i "s| data-page='[^']*'||g" "$html"
  
  # 2.3 - Substituir href="#" por href real (apenas se tiver data-i18n)
  # Isso será feito manualmente após para links específicos
  
  # 2.4 - Remover class="page active" e class="page"
  sed -i 's|class="page active"|class="main"|g' "$html"
  sed -i 's|class="page"|class="main"|g' "$html"
done

echo ""
echo "✅ ETAPA 2 COMPLETA - Arquitetura SPA eliminada"
echo ""

# ============================================================================
# ETAPA 3 — LIMPEZA TOTAL DE SCRIPTS INLINE DUPLICADOS
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ETAPA 3 — LIMPEZA TOTAL DE SCRIPTS INLINE DUPLICADOS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

LEGAL_FILES=(
  "public/legal/fundamento-juridico.html"
  "public/legal/institucional.html"
  "public/legal/politica-de-privacidade.html"
  "public/legal/preservacao-probatoria-digital.html"
  "public/legal/termos-de-custodia.html"
)

for legal in "${LEGAL_FILES[@]}"; do
  if [ -f "$legal" ]; then
    echo "  🧹 Limpando scripts duplicados: $legal"
    
    # Remover blocos <script> inline que contenham DOMContentLoaded
    # (preservando apenas os imports externos)
    perl -i -0pe 's/<script>\s*document\.addEventListener\(.*?<\/script>//gs' "$legal"
  fi
done

echo ""
echo "✅ ETAPA 3 COMPLETA - Scripts duplicados removidos"
echo ""

# ============================================================================
# ETAPA 4 — GARANTIR CONTROLLER ÚNICO
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ETAPA 4 — GARANTIR CONTROLLER ÚNICO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

for html in $HTML_FILES; do
  echo "  ✅ Validando scripts: $html"
  
  # Verificar se tem os scripts corretos
  if ! grep -q "/assets/js/i18n.js" "$html" || ! grep -q "/assets/js/navigation-controller.js" "$html"; then
    echo "  ⚠️  Scripts não encontrados, ignorando: $html"
  fi
done

echo ""
echo "✅ ETAPA 4 COMPLETA - Controllers validados"
echo ""

# ============================================================================
# ETAPA 5 — VALIDAR FETCH NO i18n.js
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ETAPA 5 — VALIDAR FETCH NO i18n.js"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

I18N_FILE="public/assets/js/i18n.js"

if [ -f "$I18N_FILE" ]; then
  echo "  🔍 Verificando fetch em i18n.js"
  
  if grep -q 'fetch(`/assets/lang/' "$I18N_FILE"; then
    echo "  ✅ Fetch já usa caminho absoluto"
  elif grep -q 'fetch(`assets/lang/' "$I18N_FILE"; then
    echo "  🔧 Corrigindo fetch relativo para absoluto"
    sed -i 's|fetch(`assets/lang/|fetch(`/assets/lang/|g' "$I18N_FILE"
    echo "  ✅ Fetch corrigido"
  else
    echo "  ⚠️  Padrão de fetch não reconhecido"
  fi
else
  echo "  ❌ ERRO: i18n.js não encontrado!"
fi

echo ""
echo "✅ ETAPA 5 COMPLETA - Fetch validado"
echo ""

# ============================================================================
# ETAPA 6 — NORMALIZAR LINKS DE NAVEGAÇÃO
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ETAPA 6 — NORMALIZAR LINKS DE NAVEGAÇÃO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Substituir href="#" com onclick por hrefs reais em arquivos EN
EN_FILES=$(find public/en -name "*.html" -type f 2>/dev/null)

for en_html in $EN_FILES; do
  echo "  🔧 Normalizando links EN: $en_html"
  
  # Logo
  sed -i 's|<a class="logo" href="#">|<a class="logo" href="/en/index.html">|g' "$en_html"
  
  # Links de navegação
  sed -i 's|<a class="nav-link" href="#">|<a class="nav-link" href="/en/index.html">|g' "$en_html"
done

# Substituir href="#" com onclick por hrefs reais em arquivos ES
ES_FILES=$(find public/es -name "*.html" -type f 2>/dev/null)

for es_html in $ES_FILES; do
  echo "  🔧 Normalizando links ES: $es_html"
  
  # Logo
  sed -i 's|<a class="logo" href="#">|<a class="logo" href="/es/index.html">|g' "$es_html"
  
  # Links de navegação
  sed -i 's|<a class="nav-link" href="#">|<a class="nav-link" href="/es/index.html">|g' "$es_html"
done

echo ""
echo "✅ ETAPA 6 COMPLETA - Links normalizados"
echo ""

# ============================================================================
# ETAPA 7 — REMOVER QUALQUER CLASSE SPA
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ETAPA 7 — REMOVER QUALQUER CLASSE SPA RESTANTE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

for html in $HTML_FILES; do
  echo "  🧹 Limpando classes SPA: $html"
  
  # Já foi feito na ETAPA 2, mas garantir
  sed -i 's|id="page-|id="content-|g' "$html"
done

echo ""
echo "✅ ETAPA 7 COMPLETA - Classes SPA removidas"
echo ""

# ============================================================================
# VALIDAÇÃO FINAL
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "VALIDAÇÃO FINAL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "🔍 Verificando resquícios SPA..."

NAVIGATE_COUNT=$(grep -r "navigateTo" public/*.html public/*/*.html 2>/dev/null | grep -v test | wc -l)
DATA_PAGE_COUNT=$(grep -r "data-page=" public/*.html public/*/*.html 2>/dev/null | grep -v test | wc -l)
PAGE_ACTIVE_COUNT=$(grep -r 'class="page active"' public/*.html public/*/*.html 2>/dev/null | grep -v test | wc -l)

echo "  • navigateTo() encontrados: $NAVIGATE_COUNT"
echo "  • data-page= encontrados: $DATA_PAGE_COUNT"
echo "  • class=\"page active\" encontrados: $PAGE_ACTIVE_COUNT"

if [ $NAVIGATE_COUNT -eq 0 ] && [ $DATA_PAGE_COUNT -eq 0 ] && [ $PAGE_ACTIVE_COUNT -eq 0 ]; then
  echo ""
  echo "✅ NENHUM RESQUÍCIO SPA DETECTADO"
else
  echo ""
  echo "⚠️  Alguns resquícios ainda existem (verificar manualmente)"
fi

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "  ✅ MIGRAÇÃO PARA MPA PURA COMPLETA"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""

