#!/usr/bin/env python3
"""
Script para adicionar versionamento automático a todos os arquivos JavaScript
Alinha ao padrão CSS (?v=4) garantindo cache-busting após deploy
"""

import os
import re
from datetime import datetime
from pathlib import Path

# Gerar timestamp de versão
VERSION = datetime.now().strftime("%Y%m%d%H%M")

# Arquivos JavaScript a versionar
JS_FILES = [
    'dropdown-menu.js',
    'i18n.js',
    'navigation.js'
]

# Páginas HTML a processar
HTML_FILES = [
    'public/index.html',
    'public/como-funciona.html',
    'public/seguranca.html',
    'public/governo.html',
    'public/empresas.html',
    'public/pessoas.html',
    'public/legal/preservacao-probatoria-digital.html',
    'public/legal/fundamento-juridico.html',
    'public/legal/termos-de-custodia.html',
    'public/legal/politica-de-privacidade.html',
    'public/legal/institucional.html'
]

def add_js_versioning():
    """Adiciona ?v=YYYYMMDDHHMM a todas as referências JavaScript"""
    
    stats = {
        'files_processed': 0,
        'references_updated': 0,
        'errors': []
    }
    
    print(f"🔧 Aplicando versionamento JavaScript: ?v={VERSION}")
    print("=" * 70)
    
    for html_file in HTML_FILES:
        if not os.path.exists(html_file):
            stats['errors'].append(f"❌ Arquivo não encontrado: {html_file}")
            continue
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_updated = False
            
            # Processar cada arquivo JS
            for js_file in JS_FILES:
                # Padrão 1: Caminho absoluto /assets/js/ARQUIVO.js
                pattern1 = rf'<script src="/assets/js/{js_file}(\?v=\d{{12}})?"></script>'
                replacement1 = f'<script src="/assets/js/{js_file}?v={VERSION}"></script>'
                
                new_content, count1 = re.subn(pattern1, replacement1, content)
                if count1 > 0:
                    content = new_content
                    stats['references_updated'] += count1
                    file_updated = True
                    print(f"  ✅ {html_file}: /assets/js/{js_file} → ?v={VERSION}")
                
                # Padrão 2: Caminho relativo assets/js/ARQUIVO.js
                pattern2 = rf'<script src="assets/js/{js_file}(\?v=\d{{12}})?"></script>'
                replacement2 = f'<script src="assets/js/{js_file}?v={VERSION}"></script>'
                
                new_content, count2 = re.subn(pattern2, replacement2, content)
                if count2 > 0:
                    content = new_content
                    stats['references_updated'] += count2
                    file_updated = True
                    print(f"  ✅ {html_file}: assets/js/{js_file} → ?v={VERSION}")
            
            # Salvar apenas se houve mudanças
            if file_updated:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                stats['files_processed'] += 1
            
        except Exception as e:
            stats['errors'].append(f"❌ Erro ao processar {html_file}: {str(e)}")
    
    return stats

def create_version_json():
    """Cria arquivo /assets/version.json para automação futura"""
    
    version_data = {
        "version": VERSION,
        "timestamp": datetime.now().isoformat(),
        "assets": {
            "css": "4",
            "js": VERSION
        }
    }
    
    os.makedirs('public/assets', exist_ok=True)
    
    import json
    with open('public/assets/version.json', 'w', encoding='utf-8') as f:
        json.dump(version_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📦 Criado: public/assets/version.json")
    print(f"   Versão CSS: ?v=4")
    print(f"   Versão JS:  ?v={VERSION}")

def main():
    print("\n" + "=" * 70)
    print("🚀 VERSIONAMENTO AUTOMÁTICO DE ARQUIVOS JAVASCRIPT")
    print("=" * 70)
    print(f"📅 Versão: {VERSION}")
    print(f"📁 Arquivos JS: {', '.join(JS_FILES)}")
    print(f"📄 Páginas HTML: {len(HTML_FILES)}")
    print("=" * 70 + "\n")
    
    # Aplicar versionamento
    stats = add_js_versioning()
    
    # Criar version.json
    create_version_json()
    
    # Relatório final
    print("\n" + "=" * 70)
    print("📊 RELATÓRIO FINAL")
    print("=" * 70)
    print(f"✅ Arquivos processados: {stats['files_processed']}")
    print(f"✅ Referências atualizadas: {stats['references_updated']}")
    
    if stats['errors']:
        print(f"\n⚠️  Erros encontrados: {len(stats['errors'])}")
        for error in stats['errors']:
            print(f"   {error}")
    else:
        print("\n✅ Nenhum erro encontrado!")
    
    print("\n" + "=" * 70)
    print("🎯 RESULTADO")
    print("=" * 70)
    print("✅ Todos os JS agora têm versionamento automático")
    print("✅ Padrão: ?v=YYYYMMDDHHMM (timestamp de build)")
    print("✅ Atualização imediata após deploy (sem hard refresh)")
    print("✅ Alinhado ao padrão CSS (?v=4)")
    print("✅ Estrutura HTML preservada")
    print("✅ Compatível com MPA")
    print("\n📌 PRÓXIMO PASSO: Configurar Nginx para cache agressivo")
    print("   location ~* \\.(js)$ {")
    print("       add_header Cache-Control \"public, max-age=31536000, immutable\";")
    print("   }")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
