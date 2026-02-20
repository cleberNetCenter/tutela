#!/bin/bash

echo "🔧 Corrigindo navegação MPA em EN/ES..."

# ============================================================================
# CORRIGIR public/en/index.html
# ============================================================================

echo "  📝 Corrigindo: public/en/index.html"

sed -i 's|<a class="nav-link" href="#" data-i18n="nav_home">|<a class="nav-link" href="/en/index.html" data-i18n="nav_home">|g' public/en/index.html
sed -i 's|<a class="nav-link" href="#" data-i18n="nav_governo">|<a class="nav-link" href="/en/governo.html" data-i18n="nav_governo">|g' public/en/index.html
sed -i 's|<a class="nav-link" href="#" data-i18n="nav_empresas">|<a class="nav-link" href="/en/empresas.html" data-i18n="nav_empresas">|g' public/en/index.html
sed -i 's|<a class="nav-link" href="#" data-i18n="nav_pessoas">|<a class="nav-link" href="/en/pessoas.html" data-i18n="nav_pessoas">|g' public/en/index.html
sed -i 's|<a class="nav-link" href="#" data-i18n="nav_como_funciona">|<a class="nav-link" href="/como-funciona.html" data-i18n="nav_como_funciona">|g' public/en/index.html
sed -i 's|<a class="nav-link" href="#" data-i18n="nav_seguranca">|<a class="nav-link" href="/seguranca.html" data-i18n="nav_seguranca">|g' public/en/index.html

# ============================================================================
# CORRIGIR public/es/index.html
# ============================================================================

echo "  📝 Corrigindo: public/es/index.html"

sed -i 's|<a class="nav-link" href="#" data-i18n="nav_home">|<a class="nav-link" href="/es/index.html" data-i18n="nav_home">|g' public/es/index.html
sed -i 's|<a class="nav-link" href="#" data-i18n="nav_governo">|<a class="nav-link" href="/es/governo.html" data-i18n="nav_governo">|g' public/es/index.html
sed -i 's|<a class="nav-link" href="#" data-i18n="nav_empresas">|<a class="nav-link" href="/es/empresas.html" data-i18n="nav_empresas">|g' public/es/index.html
sed -i 's|<a class="nav-link" href="#" data-i18n="nav_pessoas">|<a class="nav-link" href="/es/pessoas.html" data-i18n="nav_pessoas">|g' public/es/index.html
sed -i 's|<a class="nav-link" href="#" data-i18n="nav_como_funciona">|<a class="nav-link" href="/como-funciona.html" data-i18n="nav_como_funciona">|g' public/es/index.html
sed -i 's|<a class="nav-link" href="#" data-i18n="nav_seguranca">|<a class="nav-link" href="/seguranca.html" data-i18n="nav_seguranca">|g' public/es/index.html

echo ""
echo "✅ Navegação MPA corrigida em EN/ES"

# ============================================================================
# REMOVER QUALQUER OCORRÊNCIA DE navigateTo RESTANTE
# ============================================================================

echo ""
echo "🗑️  Removendo todas as ocorrências de navigateTo..."

# Buscar e remover linhas com navigateTo
for file in public/en/index.html public/es/index.html; do
  if [ -f "$file" ]; then
    echo "  🔧 Processando: $file"
    # Remover qualquer linha que contenha navigateTo
    sed -i '/navigateTo/d' "$file"
  fi
done

echo ""
echo "✅ Todas as ocorrências de navigateTo removidas"

# ============================================================================
# VALIDAÇÃO
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "VALIDAÇÃO FINAL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

NAVIGATE_COUNT=$(grep -r "navigateTo" public/*.html public/*/*.html 2>/dev/null | grep -v test | wc -l)
DATA_PAGE_COUNT=$(grep -r "data-page=" public/*.html public/*/*.html 2>/dev/null | grep -v test | wc -l)
HREF_HASH_COUNT=$(grep -r 'href="#"' public/en/*.html public/es/*.html 2>/dev/null | wc -l)

echo "  • navigateTo() encontrados: $NAVIGATE_COUNT"
echo "  • data-page= encontrados: $DATA_PAGE_COUNT"
echo "  • href=\"#\" em EN/ES: $HREF_HASH_COUNT"

if [ $NAVIGATE_COUNT -eq 0 ] && [ $DATA_PAGE_COUNT -eq 0 ]; then
  echo ""
  echo "✅ ARQUITETURA MPA PURA - SEM RESQUÍCIOS SPA"
else
  echo ""
  echo "⚠️  Alguns resquícios SPA ainda existem"
fi

echo ""

