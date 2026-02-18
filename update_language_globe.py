#!/usr/bin/env python3
"""Update language selector to use SVG globe icon instead of emoji"""

import re

files_to_update = [
    'public/index.html',
    'public/index-en.html',
    'public/index-es.html',
    'public/como-funciona.html',
    'public/seguranca.html',
    'public/legal/institucional.html',
    'public/legal/fundamento-juridico.html',
    'public/legal/termos-de-custodia.html',
    'public/legal/politica-de-privacidade.html',
    'public/legal/preservacao-probatoria-digital.html'
]

# SVG globe icon (clean, professional)
svg_globe = '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 4px;">
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="2" y1="12" x2="22" y2="12"></line>
      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
    </svg>'''

# Pattern to match emoji globe
pattern = r'🌐\s*<span class="lang-code">'
replacement = f'{svg_globe} <span class="lang-code">'

updated_count = 0

for file_path in files_to_update:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '🌐' in content:
            new_content = re.sub(pattern, replacement, content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            updated_count += 1
            print(f"✅ Updated: {file_path}")
        else:
            print(f"⏭️  Skipped: {file_path} (no emoji found)")
    except FileNotFoundError:
        print(f"⚠️  Not found: {file_path}")
    except Exception as e:
        print(f"❌ Error in {file_path}: {e}")

print(f"\n✅ Total files updated: {updated_count}")
