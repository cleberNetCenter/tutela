#!/bin/bash

# Arquivos HTML principais (exceto index.html - já corrigido)
FILES=(
  "public/governo.html"
  "public/empresas.html"
  "public/pessoas.html"
  "public/como-funciona.html"
  "public/seguranca.html"
  "public/en/index.html"
  "public/en/governo.html"
  "public/en/empresas.html"
  "public/en/pessoas.html"
  "public/es/index.html"
  "public/es/governo.html"
  "public/es/empresas.html"
  "public/es/pessoas.html"
  "public/legal/fundamento-juridico.html"
  "public/legal/institucional.html"
  "public/legal/politica-de-privacidade.html"
  "public/legal/preservacao-probatoria-digital.html"
  "public/legal/termos-de-custodia.html"
)

echo "🔧 Corrigindo ordem dos scripts em ${#FILES[@]} arquivos..."

for file in "${FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "⚠️ $file não existe (pulando)"
    continue
  fi
  
  echo "📄 Processando: $file"
  
  # Remove versões antigas dos scripts (se existirem)
  sed -i '/<script src="\/assets\/js\/i18n\.js/d' "$file"
  sed -i '/<script src="\/assets\/js\/navigation-controller\.js/d' "$file"
  
  # Adiciona os scripts na ordem correta ANTES do </body>
  sed -i 's|</body>|<script src="/assets/js/i18n.js"></script>\n<script src="/assets/js/navigation-controller.js"></script>\n</body>|' "$file"
  
done

echo "✅ Ordem de scripts corrigida!"
echo ""
echo "Verificando ordem final..."
for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "📄 $file:"
    grep -A1 "i18n.js\|navigation-controller.js" "$file" | head -4
    echo ""
  fi
done

