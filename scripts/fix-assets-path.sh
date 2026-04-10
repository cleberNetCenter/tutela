#!/bin/bash

BASE_DIR="/home/cleber/tutela-legal/public"

echo "🔍 Iniciando correção de paths em: $BASE_DIR"
echo ""

find "$BASE_DIR" -type f -name "*.html" | while read -r file; do
  echo "➡️  Processando: $file"

  # Corrige href="assets/..."
  sed -i 's|\(href=\)"assets/|\1"/assets/|g' "$file"

  # Corrige src="assets/..."
  sed -i 's|\(src=\)"assets/|\1"/assets/|g' "$file"

done

echo ""
echo "✅ Correção finalizada."
