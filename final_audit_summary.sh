#!/bin/bash

echo "═══════════════════════════════════════════════════════"
echo "  FINAL MPA AUDIT SUMMARY"
echo "  Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════════════════"
echo ""

# Production files (exclude test files)
PROD_HTML=$(find public -name "*.html" -not -name "test*" -type f)
PROD_COUNT=$(echo "$PROD_HTML" | wc -l | tr -d ' ')
TEST_COUNT=$(ls public/test*.html 2>/dev/null | wc -l | tr -d ' ')

echo "📊 FILE STATISTICS:"
echo "   • Production HTML files: $PROD_COUNT"
echo "   • Test HTML files: $TEST_COUNT (should be removed)"
echo ""

echo "✅ REQUIRED FILES:"
for file in public/assets/js/navigation-controller.js public/assets/js/i18n.js public/assets/lang/pt.json public/assets/lang/en.json public/assets/lang/es.json public/assets/illustrations/workflow_process.svg public/assets/illustrations/security_shield.svg; do
  if [ -f "$file" ]; then
    SIZE=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
    echo "   ✓ $file ($SIZE bytes)"
  else
    echo "   ✗ MISSING: $file"
  fi
done
echo ""

echo "🚫 PROHIBITED FILES (Legacy SPA):"
for file in public/assets/js/navigation.js public/assets/js/mobile-menu.js public/assets/js/dropdown-menu.js; do
  if [ -f "$file" ]; then
    echo "   ✗ FOUND: $file (CRITICAL ERROR)"
  else
    echo "   ✓ Removed: $file"
  fi
done
echo ""

echo "🔍 PRODUCTION FILES VALIDATION:"
echo "   Checking for SPA remnants in production files..."
SPA_COUNT=0
for pattern in "navigateTo(" "data-page=" "onclick=.*navigateTo" "class=\"page active\""; do
  FOUND=$(echo "$PROD_HTML" | xargs grep -l "$pattern" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$FOUND" -gt 0 ]; then
    echo "   ✗ Found '$pattern' in $FOUND production file(s)"
    SPA_COUNT=$((SPA_COUNT + FOUND))
  fi
done
if [ $SPA_COUNT -eq 0 ]; then
  echo "   ✓ No SPA remnants in production files"
fi
echo ""

echo "📝 I18N VALIDATION:"
if grep -q 'fetch(`/assets/lang/' public/assets/js/i18n.js; then
  echo "   ✓ i18n.js uses absolute fetch path"
else
  echo "   ✗ i18n.js fetch path incorrect"
fi

for lang in pt en es; do
  FILE="public/assets/lang/${lang}.json"
  if python3 -m json.tool "$FILE" > /dev/null 2>&1; then
    KEYS=$(grep -o '"[^"]*":' "$FILE" | wc -l | tr -d ' ')
    echo "   ✓ ${lang}.json: Valid JSON ($KEYS keys)"
  else
    echo "   ✗ ${lang}.json: Invalid JSON"
  fi
done
echo ""

echo "🎯 SCRIPT LOADING ORDER:"
SAMPLE_FILES="public/index.html public/governo.html public/legal/institucional.html"
for file in $SAMPLE_FILES; do
  if [ -f "$file" ]; then
    ORDER=$(grep -A 3 '</body>' "$file" | grep '<script' | grep -o '[^/]*\.js' | tr '\n' ' ')
    if echo "$ORDER" | grep -q "i18n.js.*navigation-controller.js"; then
      echo "   ✓ $file: Correct order"
    else
      echo "   ⚠ $file: Order = $ORDER"
    fi
  fi
done
echo ""

echo "⚠️  TEST FILES STATUS:"
if [ $TEST_COUNT -gt 0 ]; then
  echo "   Found $TEST_COUNT test files (should be removed for production):"
  ls public/test*.html 2>/dev/null | sed 's/^/      • /'
else
  echo "   ✓ No test files found"
fi
echo ""

echo "═══════════════════════════════════════════════════════"
if [ $SPA_COUNT -eq 0 ] && [ -f "public/assets/js/i18n.js" ] && [ -f "public/assets/js/navigation-controller.js" ]; then
  echo "  ✅ FINAL STATUS: APPROVED FOR PRODUCTION"
  echo "     (Note: Remove test files before deployment)"
else
  echo "  ❌ FINAL STATUS: ISSUES FOUND"
  echo "     Requires correction before deployment"
fi
echo "═══════════════════════════════════════════════════════"
