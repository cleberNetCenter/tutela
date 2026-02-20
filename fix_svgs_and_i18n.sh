#!/bin/bash

set -e

echo "════════════════════════════════════════════════════════════════════════════"
echo "  🔧 CORREÇÃO ESTRUTURAL: SVGs + Sincronização i18n"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""

# ============================================================================
# PARTE 1 — CRIAÇÃO DOS SVGs FALTANTES
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PARTE 1 — CRIAÇÃO DOS SVGs FALTANTES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

SVG_DIR="public/assets/illustrations"
mkdir -p "$SVG_DIR"

# 1.1 - Criar workflow_process.svg
WORKFLOW_SVG="$SVG_DIR/workflow_process.svg"

if [ ! -f "$WORKFLOW_SVG" ]; then
  echo "  🎨 Criando: workflow_process.svg"
  cat > "$WORKFLOW_SVG" << 'SVGEOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" fill="none">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4A90E2;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#357ABD;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="400" height="300" fill="#F8F9FA" rx="10"/>
  
  <!-- Process Steps -->
  <!-- Step 1 -->
  <circle cx="100" cy="80" r="30" fill="url(#grad1)"/>
  <text x="100" y="88" text-anchor="middle" fill="white" font-size="24" font-weight="bold">1</text>
  <text x="100" y="130" text-anchor="middle" fill="#2C3E50" font-size="12">Coleta</text>
  
  <!-- Arrow 1 -->
  <path d="M 130 80 L 170 80" stroke="#4A90E2" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>
  
  <!-- Step 2 -->
  <circle cx="200" cy="80" r="30" fill="url(#grad1)"/>
  <text x="200" y="88" text-anchor="middle" fill="white" font-size="24" font-weight="bold">2</text>
  <text x="200" y="130" text-anchor="middle" fill="#2C3E50" font-size="12">Validação</text>
  
  <!-- Arrow 2 -->
  <path d="M 230 80 L 270 80" stroke="#4A90E2" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>
  
  <!-- Step 3 -->
  <circle cx="300" cy="80" r="30" fill="url(#grad1)"/>
  <text x="300" y="88" text-anchor="middle" fill="white" font-size="24" font-weight="bold">3</text>
  <text x="300" y="130" text-anchor="middle" fill="#2C3E50" font-size="12">Custódia</text>
  
  <!-- Process Flow Lines -->
  <path d="M 100 120 Q 150 180 200 180 Q 250 180 300 120" stroke="#E0E0E0" stroke-width="2" fill="none" stroke-dasharray="5,5"/>
  
  <!-- Bottom Process Bar -->
  <rect x="50" y="220" width="300" height="40" rx="20" fill="#E8F4F8" stroke="#4A90E2" stroke-width="2"/>
  <text x="200" y="245" text-anchor="middle" fill="#357ABD" font-size="14" font-weight="600">Fluxo de Preservação Digital</text>
  
  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#4A90E2" />
    </marker>
  </defs>
</svg>
SVGEOF
  echo "  ✅ workflow_process.svg criado"
else
  echo "  ✅ workflow_process.svg já existe"
fi

# 1.2 - Criar security_shield.svg
SHIELD_SVG="$SVG_DIR/security_shield.svg"

if [ ! -f "$SHIELD_SVG" ]; then
  echo "  🎨 Criando: security_shield.svg"
  cat > "$SHIELD_SVG" << 'SVGEOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" fill="none">
  <defs>
    <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#2ECC71;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#27AE60;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.2"/>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="400" height="400" fill="#F0F8FF" rx="10"/>
  
  <!-- Main Shield -->
  <path d="M 200 50 L 320 100 Q 330 110 330 130 L 330 250 Q 330 280 310 300 L 200 360 L 90 300 Q 70 280 70 250 L 70 130 Q 70 110 80 100 Z" 
        fill="url(#shieldGrad)" 
        stroke="#1E8449" 
        stroke-width="4"
        filter="url(#shadow)"/>
  
  <!-- Inner Shield Detail -->
  <path d="M 200 80 L 300 120 Q 305 125 305 140 L 305 240 Q 305 260 290 275 L 200 320 L 110 275 Q 95 260 95 240 L 95 140 Q 95 125 100 120 Z" 
        fill="#F8F9FA" 
        opacity="0.3"/>
  
  <!-- Checkmark -->
  <path d="M 160 200 L 185 230 L 245 160" 
        stroke="white" 
        stroke-width="16" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        fill="none"/>
  
  <!-- Lock Icon (top) -->
  <rect x="185" y="110" width="30" height="35" rx="5" fill="white" opacity="0.9"/>
  <path d="M 195 110 Q 195 95 200 95 Q 205 95 205 110" 
        stroke="white" 
        stroke-width="3" 
        fill="none" 
        opacity="0.9"/>
  
  <!-- Security Badge -->
  <circle cx="200" cy="340" r="25" fill="#1E8449" stroke="white" stroke-width="3"/>
  <text x="200" y="350" text-anchor="middle" fill="white" font-size="20" font-weight="bold">✓</text>
  
  <!-- Text Label -->
  <text x="200" y="385" text-anchor="middle" fill="#2C3E50" font-size="14" font-weight="600">Segurança Garantida</text>
</svg>
SVGEOF
  echo "  ✅ security_shield.svg criado"
else
  echo "  ✅ security_shield.svg já existe"
fi

echo ""
echo "✅ PARTE 1 COMPLETA - SVGs criados/validados"
echo ""

# ============================================================================
# PARTE 2 — SINCRONIZAÇÃO AUTOMÁTICA DAS CHAVES I18N
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PARTE 2 — SINCRONIZAÇÃO AUTOMÁTICA DAS CHAVES I18N"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 2.1 - Extrair TODAS as chaves usadas
echo "  🔍 Extraindo chaves i18n dos arquivos HTML..."

# Extrair todas as chaves data-i18n de arquivos HTML (exceto testes)
I18N_KEYS=$(grep -roh 'data-i18n="[^"]*"' public/*.html public/*/*.html 2>/dev/null | \
            grep -v test | \
            sed 's/data-i18n="//g' | \
            sed 's/"//g' | \
            sort -u)

KEYS_COUNT=$(echo "$I18N_KEYS" | wc -l)
echo "  📊 Total de chaves únicas encontradas: $KEYS_COUNT"
echo ""

# 2.2 - Verificar arquivos de idioma
PT_FILE="public/assets/lang/pt.json"
EN_FILE="public/assets/lang/en.json"
ES_FILE="public/assets/lang/es.json"

if [ ! -f "$PT_FILE" ]; then
  echo "  ❌ ERRO: $PT_FILE não encontrado"
  exit 1
fi

echo "  ✅ Arquivos de idioma encontrados"
echo "     • $PT_FILE"
echo "     • $EN_FILE"
echo "     • $ES_FILE"
echo ""

# 2.3 - Script Python para sincronização (mais robusto que bash para JSON)
echo "  🔧 Executando sincronização de chaves..."

python3 << 'PYSCRIPT'
import json
import sys
from pathlib import Path

# Carregar arquivos JSON
pt_path = Path("public/assets/lang/pt.json")
en_path = Path("public/assets/lang/en.json")
es_path = Path("public/assets/lang/es.json")

# Carregar JSONs
with open(pt_path, 'r', encoding='utf-8') as f:
    pt_data = json.load(f)

with open(en_path, 'r', encoding='utf-8') as f:
    en_data = json.load(f)

with open(es_path, 'r', encoding='utf-8') as f:
    es_data = json.load(f)

def get_nested_value(data, key_path):
    """Obter valor aninhado de um dict usando chave.com.ponto"""
    keys = key_path.split('.')
    value = data
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None
    return value

def set_nested_value(data, key_path, value):
    """Definir valor aninhado em um dict usando chave.com.ponto"""
    keys = key_path.split('.')
    current = data
    
    for i, key in enumerate(keys[:-1]):
        if key not in current:
            current[key] = {}
        elif not isinstance(current[key], dict):
            # Se não for dict, converter para dict
            current[key] = {}
        current = current[key]
    
    # Definir o valor final apenas se não existir
    if keys[-1] not in current:
        current[keys[-1]] = value

# Obter todas as chaves do PT (fonte de verdade)
def get_all_keys(data, prefix=''):
    """Extrair recursivamente todas as chaves aninhadas"""
    keys = []
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.extend(get_all_keys(value, full_key))
        else:
            keys.append(full_key)
    return keys

pt_keys = get_all_keys(pt_data)

print(f"  📊 Chaves encontradas em pt.json: {len(pt_keys)}")

# Sincronizar EN
missing_en = 0
for key in pt_keys:
    en_value = get_nested_value(en_data, key)
    if en_value is None:
        pt_value = get_nested_value(pt_data, key)
        set_nested_value(en_data, key, pt_value)
        missing_en += 1

# Sincronizar ES
missing_es = 0
for key in pt_keys:
    es_value = get_nested_value(es_data, key)
    if es_value is None:
        pt_value = get_nested_value(pt_data, key)
        set_nested_value(es_data, key, pt_value)
        missing_es += 1

print(f"  ✅ Chaves adicionadas em EN: {missing_en}")
print(f"  ✅ Chaves adicionadas em ES: {missing_es}")

# Salvar arquivos sincronizados
with open(en_path, 'w', encoding='utf-8') as f:
    json.dump(en_data, f, ensure_ascii=False, indent=2)

with open(es_path, 'w', encoding='utf-8') as f:
    json.dump(es_data, f, ensure_ascii=False, indent=2)

print("  ✅ Arquivos JSON sincronizados e salvos")

PYSCRIPT

echo ""
echo "✅ PARTE 2 COMPLETA - Chaves i18n sincronizadas"
echo ""

# ============================================================================
# VALIDAÇÃO FINAL
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "VALIDAÇÃO FINAL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "  📊 Verificando arquivos criados/atualizados:"
echo ""

if [ -f "$WORKFLOW_SVG" ]; then
  SIZE=$(stat -f%z "$WORKFLOW_SVG" 2>/dev/null || stat -c%s "$WORKFLOW_SVG" 2>/dev/null)
  echo "  ✅ workflow_process.svg ($SIZE bytes)"
else
  echo "  ❌ workflow_process.svg NÃO ENCONTRADO"
fi

if [ -f "$SHIELD_SVG" ]; then
  SIZE=$(stat -f%z "$SHIELD_SVG" 2>/dev/null || stat -c%s "$SHIELD_SVG" 2>/dev/null)
  echo "  ✅ security_shield.svg ($SIZE bytes)"
else
  echo "  ❌ security_shield.svg NÃO ENCONTRADO"
fi

echo ""
echo "  📊 Validando arquivos JSON:"

for lang_file in "$PT_FILE" "$EN_FILE" "$ES_FILE"; do
  if python3 -c "import json; json.load(open('$lang_file'))" 2>/dev/null; then
    echo "  ✅ $(basename $lang_file) - JSON válido"
  else
    echo "  ❌ $(basename $lang_file) - JSON INVÁLIDO"
  fi
done

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "  ✅ CORREÇÃO ESTRUTURAL COMPLETA"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""

