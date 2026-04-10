#!/bin/bash

BASE_DIR="../public/insights/ativos-digitais"

echo "🚀 Migrando ativos-digitais..."

for file in "$BASE_DIR"/*.html; do
  filename=$(basename -- "$file")

  # ignorar index
  if [[ "$filename" == "index.html" ]]; then
    continue
  fi

  name="${filename%.html}"

  # evitar sobrescrever estrutura existente
  if [ -d "$BASE_DIR/$name" ]; then
    echo "⚠️ Já existe pasta: $name — pulando"
    continue
  fi

  echo "➡️ Movendo: $filename"

  mkdir -p "$BASE_DIR/$name"
  mv "$file" "$BASE_DIR/$name/index.html"

done

echo "✅ Concluído!"
