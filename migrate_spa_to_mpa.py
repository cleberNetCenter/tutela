#!/usr/bin/env python3
"""
Migração SPA → MPA - Tutela Digital®
Autor: GenSpark AI Developer
Data: 2026-02-18

OBJETIVO: Migrar de SPA para MPA com foco em SEO jurídico nacional
"""

import os
import re
import shutil
from pathlib import Path

# Diretórios
PUBLIC_DIR = Path('public')
EN_DIR = PUBLIC_DIR / 'en'
ES_DIR = PUBLIC_DIR / 'es'
LEGAL_DIR = PUBLIC_DIR / 'legal'

print("="*60)
print("MIGRAÇÃO SPA → MPA - TUTELA DIGITAL®")
print("="*60)

# =========================================
# ETAPA 1: Criar estrutura de diretórios
# =========================================
print("\n[1] Criando estrutura /en/ e /es/...")

EN_DIR.mkdir(exist_ok=True)
ES_DIR.mkdir(exist_ok=True)

print(f"✅ Criado: {EN_DIR}")
print(f"✅ Criado: {ES_DIR}")

# =========================================
# ETAPA 2: Mover páginas EN/ES
# =========================================
print("\n[2] Movendo páginas multilíngue...")

# Mover index-en.html para /en/index.html
if (PUBLIC_DIR / 'index-en.html').exists():
    shutil.move(str(PUBLIC_DIR / 'index-en.html'), str(EN_DIR / 'index.html'))
    print(f"✅ Movido: index-en.html → /en/index.html")

# Mover index-es.html para /es/index.html
if (PUBLIC_DIR / 'index-es.html').exists():
    shutil.move(str(PUBLIC_DIR / 'index-es.html'), str(ES_DIR / 'index.html'))
    print(f"✅ Movido: index-es.html → /es/index.html")

# =========================================
# ETAPA 3: Criar páginas físicas MPA
# =========================================
print("\n[3] Criando páginas físicas MPA...")

# Template base para páginas PT
mpa_pages_pt = {
    'governo.html': {
        'title': 'Governo | Tutela Digital®',
        'h1': 'Soluções para Governo',
        'content': '''
        <p>Custódia jurídica de documentos e ativos digitais para órgãos públicos.</p>
        <ul>
            <li>Conformidade com LGPD</li>
            <li>Segurança de dados</li>
            <li>Auditoria completa</li>
        </ul>
        '''
    },
    'empresas.html': {
        'title': 'Empresas | Tutela Digital®',
        'h1': 'Soluções para Empresas',
        'content': '''
        <p>Proteção jurídica de ativos digitais corporativos.</p>
        <ul>
            <li>Contratos digitais</li>
            <li>Propriedade intelectual</li>
            <li>Compliance</li>
        </ul>
        '''
    },
    'pessoas.html': {
        'title': 'Pessoas Físicas | Tutela Digital®',
        'h1': 'Soluções para Pessoas',
        'content': '''
        <p>Custódia de documentos pessoais e ativos digitais.</p>
        <ul>
            <li>Herança digital</li>
            <li>Documentos pessoais</li>
            <li>Proteção de dados</li>
        </ul>
        '''
    }
}

# Template base HTML
def create_mpa_page(filename, title, h1, content, lang='pt'):
    noindex = ''
    if lang != 'pt':
        noindex = '''
    <meta name="robots" content="noindex,follow">
    <meta name="googlebot" content="noindex,follow">'''
    
    hreflang = ''
    if filename == 'index.html' and lang == 'pt':
        hreflang = '''
    <link rel="alternate" hreflang="pt-br" href="https://tuteladigital.com.br/" />
    <link rel="alternate" hreflang="x-default" href="https://tuteladigital.com.br/" />'''
    
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>{noindex}{hreflang}
    <link rel="stylesheet" href="/assets/css/styles-clean.css">
    <link rel="stylesheet" href="/assets/css/styles-header-final.css">
    <link rel="stylesheet" href="/assets/css/dropdown-menu.css">
</head>
<body>
    <header class="header">
        <nav class="nav">
            <a href="/" class="nav-link">Início</a>
            <a href="/como-funciona.html" class="nav-link">Como Funciona</a>
            <a href="/seguranca.html" class="nav-link">Segurança</a>
            <li class="nav-dropdown">
                <a href="#">Soluções</a>
                <ul class="dropdown-menu">
                    <li><a href="/governo.html">Governo</a></li>
                    <li><a href="/empresas.html">Empresas</a></li>
                    <li><a href="/pessoas.html">Pessoas</a></li>
                </ul>
            </li>
            <li class="nav-dropdown">
                <a href="#">Base Jurídica</a>
                <ul class="dropdown-menu">
                    <li><a href="/legal/preservacao-probatoria-digital.html">Preservação Probatória</a></li>
                    <li><a href="/legal/fundamento-juridico.html">Fundamento Jurídico</a></li>
                    <li><a href="/legal/termos-de-custodia.html">Termos de Custódia</a></li>
                    <li><a href="/legal/politica-de-privacidade.html">Política de Privacidade</a></li>
                    <li><a href="/legal/institucional.html">Institucional</a></li>
                </ul>
            </li>
        </nav>
    </header>
    
    <main>
        <section>
            <h1>{h1}</h1>
            {content}
        </section>
    </main>
    
    <script src="/assets/js/dropdown-menu.js"></script>
</body>
</html>'''

# Criar páginas PT
for filename, data in mpa_pages_pt.items():
    filepath = PUBLIC_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(create_mpa_page(filename, data['title'], data['h1'], data['content'], 'pt'))
    print(f"✅ Criado: {filename}")

# Criar páginas EN
mpa_pages_en = {
    'governo.html': ('Government | Tutela Digital®', 'Government Solutions', '<p>Legal custody of documents and digital assets for public agencies.</p>'),
    'empresas.html': ('Companies | Tutela Digital®', 'Business Solutions', '<p>Legal protection of corporate digital assets.</p>'),
    'pessoas.html': ('Individuals | Tutela Digital®', 'Individual Solutions', '<p>Custody of personal documents and digital assets.</p>')
}

for filename, (title, h1, content) in mpa_pages_en.items():
    filepath = EN_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(create_mpa_page(filename, title, h1, content, 'en'))
    print(f"✅ Criado: /en/{filename}")

# Criar páginas ES
mpa_pages_es = {
    'governo.html': ('Gobierno | Tutela Digital®', 'Soluciones para Gobierno', '<p>Custodia legal de documentos y activos digitales para organismos públicos.</p>'),
    'empresas.html': ('Empresas | Tutela Digital®', 'Soluciones para Empresas', '<p>Protección legal de activos digitales corporativos.</p>'),
    'pessoas.html': ('Individuos | Tutela Digital®', 'Soluciones para Personas', '<p>Custodia de documentos personales y activos digitales.</p>')
}

for filename, (title, h1, content) in mpa_pages_es.items():
    filepath = ES_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(create_mpa_page(filename, title, h1, content, 'es'))
    print(f"✅ Criado: /es/{filename}")

print("\n✅ ETAPA 3 concluída: Páginas físicas MPA criadas")

# =========================================
# ETAPA 4: Backup navigation.js
# =========================================
print("\n[4] Fazendo backup de navigation.js...")

nav_file = PUBLIC_DIR / 'assets' / 'js' / 'navigation.js'
if nav_file.exists():
    backup_file = nav_file.with_suffix('.js.backup')
    shutil.copy(str(nav_file), str(backup_file))
    print(f"✅ Backup criado: navigation.js.backup")

print("\n" + "="*60)
print("MIGRAÇÃO BÁSICA CONCLUÍDA")
print("="*60)
print("\nPRÓXIMOS PASSOS MANUAIS:")
print("1. Remover navigation.js do <head> dos HTMLs")
print("2. Converter onclick='navigateTo()' para href=''")
print("3. Adicionar noindex em /en/ e /es/")
print("4. Atualizar sitemap.xml")
print("5. Implementar breadcrumb")
print("="*60)
