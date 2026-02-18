#!/usr/bin/env python3
"""
Gera sitemap.xml e robots.txt corretos para MPA
"""

from pathlib import Path
from datetime import date

PUBLIC_DIR = Path('public')

print("\n" + "="*60)
print("GERANDO SITEMAP.XML E ROBOTS.TXT")
print("="*60)

# URLs para o sitemap (apenas PT)
sitemap_urls = [
    ('https://tuteladigital.com.br/', '2026-02-18', 'weekly', '1.0'),
    ('https://tuteladigital.com.br/como-funciona.html', '2026-02-18', 'monthly', '0.9'),
    ('https://tuteladigital.com.br/seguranca.html', '2026-02-18', 'monthly', '0.9'),
    ('https://tuteladigital.com.br/governo.html', '2026-02-18', 'monthly', '0.8'),
    ('https://tuteladigital.com.br/empresas.html', '2026-02-18', 'monthly', '0.8'),
    ('https://tuteladigital.com.br/pessoas.html', '2026-02-18', 'monthly', '0.8'),
    ('https://tuteladigital.com.br/legal/preservacao-probatoria-digital.html', '2026-02-18', 'monthly', '0.7'),
    ('https://tuteladigital.com.br/legal/fundamento-juridico.html', '2026-02-18', 'monthly', '0.6'),
    ('https://tuteladigital.com.br/legal/institucional.html', '2026-02-18', 'monthly', '0.6'),
    ('https://tuteladigital.com.br/legal/termos-de-custodia.html', '2026-02-18', 'monthly', '0.6'),
    ('https://tuteladigital.com.br/legal/politica-de-privacidade.html', '2026-02-18', 'monthly', '0.6'),
]

# Gerar sitemap.xml
sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''

for url, lastmod, changefreq, priority in sitemap_urls:
    sitemap_content += f'''  <url>
    <loc>{url}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
'''

sitemap_content += '</urlset>'

# Salvar sitemap.xml
sitemap_file = PUBLIC_DIR / 'sitemap.xml'
with open(sitemap_file, 'w', encoding='utf-8') as f:
    f.write(sitemap_content)

print(f"\n✅ Sitemap gerado: {sitemap_file}")
print(f"   - {len(sitemap_urls)} URLs (apenas PT)")
print("   - SEM páginas /en/ ou /es/")

# Gerar robots.txt
robots_content = '''# Tutela Digital® - Robots.txt
# MPA Architecture - SEO Jurídico Nacional

User-agent: *

# Permitir páginas PT
Allow: /
Allow: /como-funciona.html
Allow: /seguranca.html
Allow: /governo.html
Allow: /empresas.html
Allow: /pessoas.html
Allow: /legal/

# Bloquear páginas EN/ES (noindex já aplicado)
Disallow: /en/
Disallow: /es/

# Assets
Allow: /assets/

# Sitemap
Sitemap: https://tuteladigital.com.br/sitemap.xml
'''

robots_file = PUBLIC_DIR / 'robots.txt'
with open(robots_file, 'w', encoding='utf-8') as f:
    f.write(robots_content)

print(f"\n✅ Robots.txt gerado: {robots_file}")
print("   - Bloqueado: /en/ e /es/")
print("   - Sitemap: https://tuteladigital.com.br/sitemap.xml")

print("\n✅ SITEMAP E ROBOTS.TXT GERADOS")
print("="*60)
