#!/usr/bin/env python3
"""
Script para adicionar atributos data-i18n no HTML
Tutela Digital® - Sistema de Internacionalização
"""

import re
import json

# Mapeamento de textos para chaves i18n
MAPPINGS = [
    # Header & Nav (já feito manualmente)
    # Hero
    (r'<p class="hero-subtitle">(.*?)</p>', '<p class="hero-subtitle" data-i18n="hero_subtitle">\\1</p>'),
    
    # Home - Trust
    (r'<h2>Confiança Institucional</h2>', '<h2 data-i18n="home_trust_title">Confiança Institucional</h2>'),
    
    # Home - Verticals
    (r'<h2>Soluções por Segmento</h2>', '<h2 data-i18n="home_verticals_title">Soluções por Segmento</h2>'),
    (r'<h3>Governo</h3>\s*<p>Custódia probatória', '<h3 data-i18n="home_verticals_gov">Governo</h3>\\n<p data-i18n="home_verticals_gov_desc">Custódia probatória'),
    (r'<h3>Empresas</h3>\s*<p>Proteção de documentos estratégicos', '<h3 data-i18n="home_verticals_corp">Empresas</h3>\\n<p data-i18n="home_verticals_corp_desc">Proteção de documentos estratégicos'),
    (r'<h3>Pessoas Físicas</h3>\s*<p>Proteção patrimonial digital, confidencialidade', '<h3 data-i18n="home_verticals_personal">Pessoas Físicas</h3>\\n<p data-i18n="home_verticals_personal_desc">Proteção patrimonial digital, confidencialidade'),
    
    # Home - Pillars
    (r'<h2>Pilares da Infraestrutura</h2>', '<h2 data-i18n="home_pillars_title">Pilares da Infraestrutura</h2>'),
    (r'<h3>Preservação Probatória Estruturada</h3>', '<h3 data-i18n="home_pillars_preservation">Preservação Probatória Estruturada</h3>'),
    (r'<h3>Integridade Verificável</h3>', '<h3 data-i18n="home_pillars_integrity">Integridade Verificável</h3>'),
    (r'<h3>Cadeia de Custódia Documentada</h3>', '<h3 data-i18n="home_pillars_custody">Cadeia de Custódia Documentada</h3>'),
    (r'<h3>Suporte à Admissibilidade Jurídica</h3>', '<h3 data-i18n="home_pillars_admissibility">Suporte à Admissibilidade Jurídica</h3>'),
    
    # Home - Applicability
    (r'<h2>Aplicabilidade Jurídica</h2>', '<h2 data-i18n="home_applicability_title">Aplicabilidade Jurídica</h2>'),
    
    # Home - CTA
    (r'<h2>Proteja seus ativos digitais com validade jurídica</h2>', '<h2 data-i18n="home_cta_title">Proteja seus ativos digitais com validade jurídica</h2>'),
    (r'<a class="btn btn-primary" href="https://app\.tuteladigital\.com\.br/"([^>]*)>Acessar a Plataforma</a>', '<a class="btn btn-primary" href="https://app.tuteladigital.com.br/"\\1 data-i18n="home_cta_button">Acessar a Plataforma</a>'),
    
    # Footer
    (r'<span class="footer-link" onclick="navigateTo\(\'institucional\'\)">Institucional</span>', '<span class="footer-link" onclick="navigateTo(\'institucional\')" data-i18n="footer_institutional">Institucional</span>'),
    (r'<span class="footer-link" onclick="navigateTo\(\'fundamento-juridico\'\)">Fundamento Jurídico</span>', '<span class="footer-link" onclick="navigateTo(\'fundamento-juridico\')" data-i18n="footer_legal_foundation">Fundamento Jurídico</span>'),
    (r'<span class="footer-link" onclick="navigateTo\(\'termos-de-custodia\'\)">Termos de Custódia</span>', '<span class="footer-link" onclick="navigateTo(\'termos-de-custodia\')" data-i18n="footer_custody_terms">Termos de Custódia</span>'),
    (r'<span class="footer-link" onclick="navigateTo\(\'politica-de-privacidade\'\)">Política de Privacidade</span>', '<span class="footer-link" onclick="navigateTo(\'politica-de-privacidade\')" data-i18n="footer_privacy">Política de Privacidade</span>'),
]

def add_i18n_attributes(html_content):
    """
    Adiciona atributos data-i18n no HTML
    """
    for pattern, replacement in MAPPINGS:
        html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    return html_content

if __name__ == "__main__":
    # Lê o arquivo
    with open('/home/user/webapp/public/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Processa
    modified = add_i18n_attributes(content)
    
    # Salva
    with open('/home/user/webapp/public/index.html', 'w', encoding='utf-8') as f:
        f.write(modified)
    
    print("✅ Atributos data-i18n adicionados com sucesso!")
