#!/bin/bash

BASE_DIR="../public/insights/prova-digital"

echo "🚀 Iniciando migração para URLs limpas..."

for file in "$BASE_DIR"/*.html; do
  filename=$(basename -- "$file")

  # ignorar index.html
  if [[ "$filename" == "index.html" ]]; then
    continue
  fi

  name="${filename%.html}"

  echo "➡️ Processando: $filename"

  mkdir -p "$BASE_DIR/$name"
  mv "$file" "$BASE_DIR/$name/index.html"

done

echo "✅ Migração concluída!"
