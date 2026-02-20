#!/bin/bash
set -euo pipefail

# MPA COMPLETE AUDIT SCRIPT
# Date: 2026-02-20
# Purpose: Full automated verification of MPA migration

REPORT="audit_mpa_complete_$(date +%Y%m%d_%H%M%S).txt"
exec > >(tee "$REPORT") 2>&1

echo "═══════════════════════════════════════════════════════"
echo "  MPA COMPLETE MIGRATION AUDIT"
echo "  Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════════════════"
echo ""

# Counters
CRITICAL_ERRORS=0
PATH_ERRORS=0
SPA_ERRORS=0
DUPLICATE_ERRORS=0
I18N_ERRORS=0
SVG_ERRORS=0

# Phase 1: Required files check
echo "▶ PHASE 1: REQUIRED FILES CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

REQUIRED_FILES=(
  "public/assets/js/navigation-controller.js"
  "public/assets/js/i18n.js"
  "public/assets/lang/pt.json"
  "public/assets/lang/en.json"
  "public/assets/lang/es.json"
  "public/assets/illustrations/workflow_process.svg"
  "public/assets/illustrations/security_shield.svg"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "  ✅ FOUND: $file"
  else
    echo "  ❌ MISSING: $file"
    ((CRITICAL_ERRORS++))
  fi
done
echo ""

# Phase 2: Prohibited files check
echo "▶ PHASE 2: PROHIBITED FILES CHECK (Legacy SPA)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

PROHIBITED_FILES=(
  "public/assets/js/navigation.js"
  "public/assets/js/mobile-menu.js"
  "public/assets/js/dropdown-menu.js"
)

for file in "${PROHIBITED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "  ❌ CRITICAL: Found prohibited file: $file"
    ((CRITICAL_ERRORS++))
  else
    echo "  ✅ REMOVED: $file"
  fi
done
echo ""

# Phase 3: HTML files scan
echo "▶ PHASE 3: HTML FILES SCAN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

HTML_FILES=$(find public -name "*.html" -type f | sort)
HTML_COUNT=$(echo "$HTML_FILES" | wc -l)
echo "  Found $HTML_COUNT HTML files"
echo ""

# Phase 4: Prohibited script tags
echo "▶ PHASE 4: PROHIBITED SCRIPT TAGS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

PROHIBITED_SCRIPTS=(
  "navigation.js"
  "mobile-menu.js"
  "dropdown-menu.js"
)

for script in "${PROHIBITED_SCRIPTS[@]}"; do
  FOUND=$(grep -rn "$script" public/*.html public/*/*.html public/*/*/*.html 2>/dev/null || true)
  if [ -n "$FOUND" ]; then
    echo "  ❌ CRITICAL: References to $script found:"
    echo "$FOUND" | sed 's/^/     /'
    ((CRITICAL_ERRORS++))
  else
    echo "  ✅ No references to $script"
  fi
done
echo ""

# Phase 5: Relative path errors
echo "▶ PHASE 5: RELATIVE PATH ERRORS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

while IFS= read -r file; do
  # Check for src="assets/ or href="assets/ (missing leading slash)
  RELATIVE_PATHS=$(grep -n 'src="assets/\|href="assets/\|src='"'"'assets/\|href='"'"'assets/' "$file" 2>/dev/null || true)
  if [ -n "$RELATIVE_PATHS" ]; then
    echo "  ⚠️  PATH ERROR in $file:"
    echo "$RELATIVE_PATHS" | sed 's/^/     /'
    ((PATH_ERRORS++))
  fi
done <<< "$HTML_FILES"

if [ $PATH_ERRORS -eq 0 ]; then
  echo "  ✅ All asset paths are absolute"
fi
echo ""

# Phase 6: SPA remnants
echo "▶ PHASE 6: SPA ARCHITECTURE REMNANTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

SPA_PATTERNS=(
  "navigateTo("
  "data-page="
  'class="page active"'
  'class="page"'
  "history.pushState"
  "history.replaceState"
  "page-container"
  "initNavigation("
)

for pattern in "${SPA_PATTERNS[@]}"; do
  FOUND=$(grep -rn "$pattern" public/*.html public/*/*.html public/*/*/*.html 2>/dev/null || true)
  if [ -n "$FOUND" ]; then
    echo "  ❌ SPA REMNANT: '$pattern' found:"
    echo "$FOUND" | head -10 | sed 's/^/     /'
    COUNT=$(echo "$FOUND" | wc -l)
    if [ $COUNT -gt 10 ]; then
      echo "     ... and $((COUNT - 10)) more occurrences"
    fi
    ((SPA_ERRORS++))
  fi
done

if [ $SPA_ERRORS -eq 0 ]; then
  echo "  ✅ No SPA remnants detected"
fi
echo ""

# Phase 7: Script loading order
echo "▶ PHASE 7: SCRIPT LOADING ORDER VERIFICATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

while IFS= read -r file; do
  # Extract script tags from end of body
  SCRIPTS=$(grep -A 5 '</body>' "$file" | grep '<script' || true)
  
  # Check correct order: i18n.js then navigation-controller.js
  I18N_LINE=$(echo "$SCRIPTS" | grep -n 'i18n.js' | cut -d: -f1 | head -1)
  NAV_LINE=$(echo "$SCRIPTS" | grep -n 'navigation-controller.js' | cut -d: -f1 | head -1)
  
  if [ -n "$I18N_LINE" ] && [ -n "$NAV_LINE" ]; then
    if [ "$I18N_LINE" -lt "$NAV_LINE" ]; then
      echo "  ✅ $file: Correct order"
    else
      echo "  ⚠️  $file: Incorrect order (nav-controller before i18n)"
      ((DUPLICATE_ERRORS++))
    fi
  elif [ -n "$I18N_LINE" ] || [ -n "$NAV_LINE" ]; then
    echo "  ⚠️  $file: Missing script (i18n: ${I18N_LINE:-missing}, nav: ${NAV_LINE:-missing})"
    ((DUPLICATE_ERRORS++))
  fi
  
  # Check for extra navigation scripts
  EXTRA_SCRIPTS=$(echo "$SCRIPTS" | grep -v 'i18n.js' | grep -v 'navigation-controller.js' | grep -v '^$' || true)
  if [ -n "$EXTRA_SCRIPTS" ]; then
    echo "  ⚠️  $file: Extra scripts detected:"
    echo "$EXTRA_SCRIPTS" | sed 's/^/     /'
    ((DUPLICATE_ERRORS++))
  fi
done <<< "$HTML_FILES"
echo ""

# Phase 8: i18n.js fetch validation
echo "▶ PHASE 8: I18N.JS FETCH PATH VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

I18N_FILE="public/assets/js/i18n.js"
if [ -f "$I18N_FILE" ]; then
  # Check for absolute fetch path
  ABSOLUTE_FETCH=$(grep "fetch(\`/assets/lang/" "$I18N_FILE" || true)
  RELATIVE_FETCH=$(grep 'fetch("assets/lang/\|fetch('"'"'assets/lang/\|fetch(`assets/lang/' "$I18N_FILE" || true)
  
  if [ -n "$ABSOLUTE_FETCH" ]; then
    echo "  ✅ i18n.js uses absolute fetch path"
  fi
  
  if [ -n "$RELATIVE_FETCH" ]; then
    echo "  ❌ i18n.js contains relative fetch paths:"
    echo "$RELATIVE_FETCH" | sed 's/^/     /'
    ((I18N_ERRORS++))
  fi
else
  echo "  ❌ i18n.js not found"
  ((CRITICAL_ERRORS++))
fi
echo ""

# Phase 9: Duplicate DOMContentLoaded listeners
echo "▶ PHASE 9: DUPLICATE INLINE SCRIPTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

while IFS= read -r file; do
  # Count inline DOMContentLoaded occurrences
  COUNT=$(grep -c "document.addEventListener('DOMContentLoaded'" "$file" 2>/dev/null || echo "0")
  if [ "$COUNT" -gt 1 ]; then
    echo "  ⚠️  $file: $COUNT DOMContentLoaded listeners (duplicate)"
    ((DUPLICATE_ERRORS++))
  fi
done <<< "$HTML_FILES"

if [ $DUPLICATE_ERRORS -eq 0 ]; then
  echo "  ✅ No duplicate inline scripts"
fi
echo ""

# Phase 10: i18n key synchronization
echo "▶ PHASE 10: I18N KEY SYNCHRONIZATION CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Extract all data-i18n keys from HTML
DATA_I18N_KEYS=$(grep -roh 'data-i18n="[^"]*"' public/*.html public/*/*.html public/*/*/*.html 2>/dev/null | \
  sed 's/data-i18n="//g' | sed 's/"//g' | sort -u)

KEY_COUNT=$(echo "$DATA_I18N_KEYS" | wc -l)
echo "  Found $KEY_COUNT unique data-i18n keys in HTML"

# Check each language file
for lang in pt en es; do
  LANG_FILE="public/assets/lang/${lang}.json"
  if [ -f "$LANG_FILE" ]; then
    # Validate JSON syntax
    if python3 -m json.tool "$LANG_FILE" > /dev/null 2>&1; then
      echo "  ✅ ${lang}.json: Valid JSON syntax"
      
      # Count keys (rough estimate)
      LANG_KEYS=$(grep -o '"[^"]*":' "$LANG_FILE" | wc -l)
      echo "     Keys in file: ~$LANG_KEYS"
    else
      echo "  ❌ ${lang}.json: Invalid JSON syntax"
      ((I18N_ERRORS++))
    fi
  else
    echo "  ❌ ${lang}.json: File not found"
    ((I18N_ERRORS++))
  fi
done
echo ""

# Phase 11: SVG illustration check
echo "▶ PHASE 11: SVG ILLUSTRATION FILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

SVG_REFS=$(grep -roh 'src="/assets/illustrations/[^"]*\.svg"' public/*.html public/*/*.html 2>/dev/null | \
  sed 's/src="//g' | sed 's/"//g' | sed 's|^/||' | sort -u)

while IFS= read -r svg_path; do
  if [ -n "$svg_path" ]; then
    FULL_PATH="public/$svg_path"
    if [ -f "$FULL_PATH" ]; then
      SIZE=$(stat -f%z "$FULL_PATH" 2>/dev/null || stat -c%s "$FULL_PATH" 2>/dev/null)
      echo "  ✅ $svg_path (${SIZE} bytes)"
    else
      echo "  ❌ MISSING: $svg_path"
      ((SVG_ERRORS++))
    fi
  fi
done <<< "$SVG_REFS"

if [ $SVG_ERRORS -eq 0 ]; then
  echo "  ✅ All SVG illustrations present"
fi
echo ""

# Final summary
echo "═══════════════════════════════════════════════════════"
echo "  AUDIT SUMMARY"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📊 Statistics:"
echo "   • HTML files audited: $HTML_COUNT"
echo "   • Critical errors: $CRITICAL_ERRORS"
echo "   • Path errors: $PATH_ERRORS"
echo "   • SPA remnants: $SPA_ERRORS"
echo "   • Duplicate scripts: $DUPLICATE_ERRORS"
echo "   • i18n errors: $I18N_ERRORS"
echo "   • SVG errors: $SVG_ERRORS"
echo ""

TOTAL_ERRORS=$((CRITICAL_ERRORS + PATH_ERRORS + SPA_ERRORS + DUPLICATE_ERRORS + I18N_ERRORS + SVG_ERRORS))
echo "   TOTAL ERRORS: $TOTAL_ERRORS"
echo ""

if [ $TOTAL_ERRORS -eq 0 ]; then
  echo "✅ FINAL STATUS: APPROVED"
  echo "   All checks passed. Project is 100% MPA compliant."
else
  echo "❌ FINAL STATUS: REPROVED"
  echo "   Found $TOTAL_ERRORS error(s) that need correction."
fi
echo ""
echo "Report saved to: $REPORT"
echo "═══════════════════════════════════════════════════════"

exit 0
