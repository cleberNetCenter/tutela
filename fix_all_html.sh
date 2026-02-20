#!/bin/bash

# Lista de arquivos HTML a processar
HTML_FILES=(
  "public/index.html"
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

echo "🔧 Limpando ${#HTML_FILES[@]} arquivos HTML..."

for file in "${HTML_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "⚠️ Arquivo não existe: $file (pulando)"
    continue
  fi
  
  echo "📄 Processando: $file"
  
  # 1. Remove scripts legados (navigation.js, mobile-menu.js, dropdown-menu.js)
  sed -i '/<script[^>]*navigation\.js/d' "$file"
  sed -i '/<script[^>]*mobile-menu\.js/d' "$file"
  sed -i '/<script[^>]*dropdown-menu\.js/d' "$file"
  
  # 2. Converte caminhos CSS relativos para absolutos
  sed -i 's|href="assets/css/|href="/assets/css/|g' "$file"
  sed -i 's|href="\.\.\/assets/css/|href="/assets/css/|g' "$file"
  sed -i 's|href="\.\.\/\.\.\/assets/css/|href="/assets/css/|g' "$file"
  
  # 3. Converte caminhos JS relativos para absolutos
  sed -i 's|src="assets/js/|src="/assets/js/|g' "$file"
  sed -i 's|src="\.\.\/assets/js/|src="/assets/js/|g' "$file"
  sed -i 's|src="\.\.\/\.\.\/assets/js/|src="/assets/js/|g' "$file"
  
  # 4. Converte caminhos de imagens para absolutos
  sed -i 's|src="assets/|src="/assets/|g' "$file"
  sed -i 's|src="\.\.\/assets/|src="/assets/|g' "$file"
  sed -i 's|src="\.\.\/\.\.\/assets/|src="/assets/|g' "$file"
  
  # 5. Converte caminhos de lang JSON para absolutos
  sed -i 's|/assets/lang/|/assets/lang/|g' "$file"
  
done

echo "✅ Limpeza concluída!"
echo ""
echo "Verificando se ainda existem scripts legados..."
grep -rn "navigation\.js\|mobile-menu\.js\|dropdown-menu\.js" public/*.html public/en/*.html public/es/*.html public/legal/*.html 2>/dev/null || echo "✅ Nenhum script legado encontrado!"

