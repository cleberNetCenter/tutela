#!/usr/bin/env python3
"""
Script para corrigir páginas com conteúdo hard-coded em português
Adiciona i18n.js, data-i18n attributes e converte dropdowns para botões
"""
import json
import re
from pathlib import Path
from datetime import datetime

def add_i18n_keys():
    """Adiciona chaves faltantes aos arquivos de tradução"""
    
    # Chaves para a página institucional
    institucional_keys = {
        "pt": {
            "title": "Estrutura Institucional",
            "subtitle": "Informações jurídicas e estruturais da entidade responsável pela preservação probatória digital.",
            "legalIdTitle": "Identificação Jurídica",
            "legalIdText": "Razão Social: Novaes & Coelho Ltda - NetCenter\nCNPJ: 00.810.662/0001-27\nSede: Av. Raja Gabaglia, 1710 - Sala 408 - Gutierrez - Belo Horizonte - MG - 30441-194",
            "legalIdDescription": "A Tutela Digital® é infraestrutura privada de preservação probatória digital desenvolvida no Brasil, com atuação nacional.",
            "activityNatureTitle": "Natureza da Atividade",
            "activityNatureP1": "A Tutela Digital® não exerce função cartorial e não substitui tabelionato.",
            "activityNatureP2": "Sua atuação consiste na preservação técnica estruturada de ativos digitais com cadeia de custódia verificável, integridade criptográfica e registro temporal imutável.",
            "activityNatureP3": "Quando solicitado, os ativos podem ser submetidos à formalização cartorial por meio de ata notarial junto a tabelionato competente.",
            "purposeTitle": "Finalidade da Infraestrutura",
            "legalBasisTitle": "Base Jurídica Aplicável",
            "legalBasisP1": "A admissibilidade da prova digital fundamenta-se no Código de Processo Civil, na Lei nº 11.419/2006, na Medida Provisória nº 2.200-2/2001 e na Lei nº 13.709/2018 (LGPD).",
            "legalBasisP2": "A integridade e autenticidade podem ser demonstradas por mecanismos técnicos idôneos e cadeia de custódia verificável.",
            "interopTitle": "Interoperabilidade Cartorial",
            "interopP1": "A infraestrutura permite interoperabilidade com tabelionatos para eventual emissão de ata notarial, mediante solicitação do titular.",
            "interopP2": "A formalização notarial ocorre exclusivamente pelo tabelionato competente.",
            "govTitle": "Desenvolvimento e Governança",
            "govP1": "A plataforma foi desenvolvida pela NetCenter, empresa com mais de 30 anos de atuação em tecnologia da informação.",
            "govP2": "O produto Tutela Digital® opera como unidade especializada com foco exclusivo em preservação probatória digital.",
            "govP3": "Detalhes técnicos proprietários não são divulgados publicamente para preservação de segurança e propriedade intelectual.",
            "ctaTitle": "Transparência Institucional e Confiabilidade Jurídica",
            "ctaText": "Conheça também os fundamentos jurídicos e termos de custódia."
        },
        "en": {
            "title": "Institutional Structure",
            "subtitle": "Legal and structural information about the entity responsible for digital evidentiary preservation.",
            "legalIdTitle": "Legal Identification",
            "legalIdText": "Corporate Name: Novaes & Coelho Ltda - NetCenter\nTax ID: 00.810.662/0001-27\nHeadquarters: Av. Raja Gabaglia, 1710 - Suite 408 - Gutierrez - Belo Horizonte - MG - Brazil - 30441-194",
            "legalIdDescription": "Tutela Digital® is a private digital evidentiary preservation infrastructure developed in Brazil, operating nationwide.",
            "activityNatureTitle": "Nature of Activity",
            "activityNatureP1": "Tutela Digital® does not perform notarial functions and does not replace notary services.",
            "activityNatureP2": "Its activity consists of structured technical preservation of digital assets with verifiable chain of custody, cryptographic integrity, and immutable temporal registration.",
            "activityNatureP3": "When requested, assets can be submitted for notarial formalization through notarial act at a competent notary office.",
            "purposeTitle": "Infrastructure Purpose",
            "legalBasisTitle": "Applicable Legal Basis",
            "legalBasisP1": "Admissibility of digital evidence is based on the Code of Civil Procedure, Law No. 11.419/2006, Provisional Measure No. 2.200-2/2001, and Law No. 13.709/2018 (LGPD).",
            "legalBasisP2": "Integrity and authenticity can be demonstrated by suitable technical mechanisms and verifiable chain of custody.",
            "interopTitle": "Notarial Interoperability",
            "interopP1": "The infrastructure allows interoperability with notary offices for possible issuance of notarial act, upon request by the holder.",
            "interopP2": "Notarial formalization occurs exclusively through competent notary office.",
            "govTitle": "Development and Governance",
            "govP1": "The platform was developed by NetCenter, a company with over 30 years of experience in information technology.",
            "govP2": "Tutela Digital® product operates as a specialized unit focused exclusively on digital evidentiary preservation.",
            "govP3": "Proprietary technical details are not publicly disclosed for security and intellectual property preservation.",
            "ctaTitle": "Institutional Transparency and Legal Reliability",
            "ctaText": "Also learn about the legal foundations and custody terms."
        },
        "es": {
            "title": "Estructura Institucional",
            "subtitle": "Información jurídica y estructural de la entidad responsable de la preservación probatoria digital.",
            "legalIdTitle": "Identificación Jurídica",
            "legalIdText": "Razón Social: Novaes & Coelho Ltda - NetCenter\nCNPJ: 00.810.662/0001-27\nSede: Av. Raja Gabaglia, 1710 - Sala 408 - Gutierrez - Belo Horizonte - MG - Brasil - 30441-194",
            "legalIdDescription": "Tutela Digital® es una infraestructura privada de preservación probatoria digital desarrollada en Brasil, con actuación nacional.",
            "activityNatureTitle": "Naturaleza de la Actividad",
            "activityNatureP1": "Tutela Digital® no ejerce función notarial y no sustituye servicios notariales.",
            "activityNatureP2": "Su actuación consiste en la preservación técnica estructurada de activos digitales con cadena de custodia verificable, integridad criptográfica y registro temporal inmutable.",
            "activityNatureP3": "Cuando se solicita, los activos pueden someterse a formalización notarial mediante acta notarial en notaría competente.",
            "purposeTitle": "Finalidad de la Infraestructura",
            "legalBasisTitle": "Base Jurídica Aplicable",
            "legalBasisP1": "La admisibilidad de la prueba digital se fundamenta en el Código de Proceso Civil, la Ley nº 11.419/2006, la Medida Provisional nº 2.200-2/2001 y la Ley nº 13.709/2018 (LGPD).",
            "legalBasisP2": "La integridad y autenticidad pueden demostrarse mediante mecanismos técnicos idóneos y cadena de custodia verificable.",
            "interopTitle": "Interoperabilidad Notarial",
            "interopP1": "La infraestructura permite interoperabilidad con notarías para eventual emisión de acta notarial, mediante solicitud del titular.",
            "interopP2": "La formalización notarial ocurre exclusivamente por la notaría competente.",
            "govTitle": "Desarrollo y Gobernanza",
            "govP1": "La plataforma fue desarrollada por NetCenter, empresa con más de 30 años de actuación en tecnología de la información.",
            "govP2": "El producto Tutela Digital® opera como unidad especializada con foco exclusivo en preservación probatoria digital.",
            "govP3": "Detalles técnicos propietarios no son divulgados públicamente para preservación de seguridad y propiedad intelectual.",
            "ctaTitle": "Transparencia Institucional y Confiabilidad Jurídica",
            "ctaText": "Conozca también los fundamentos jurídicos y términos de custodia."
        }
    }
    
    # Chaves adicionais para política de privacidade
    privacy_additional = {
        "pt": {
            "title": "Política de Privacidade e Proteção de Dados",
            "subtitle": "Diretrizes aplicáveis ao tratamento de dados pessoais no contexto da custódia probatória digital.",
            "scope_title": "1. Escopo",
            "scope_text": "A presente Política de Privacidade descreve como a Tutela Digital® realiza o tratamento de dados pessoais em conformidade com a Lei nº 13.709/2018 (Lei Geral de Proteção de Dados - LGPD).",
            "controller_title": "2. Controlador de Dados",
            "controller_text": "Novaes & Coelho Ltda - NetCenter\nCNPJ: 00.810.662/0001-27\nE-mail: contato@tuteladigital.com.br",
            "data_collected_title": "3. Dados Coletados",
            "data_collected_text": "São coletados apenas os dados necessários à identificação do titular, autenticação, registro da custódia e emissão de relatórios periciais. Incluem: nome completo, CPF/CNPJ, e-mail, telefone e endereço.",
            "purpose_title": "4. Finalidade do Tratamento",
            "purpose_text": "Execução de serviço de custódia probatória digital\nIdentificação do depositante\nCumprimento de obrigação legal ou regulatória\nExercício regular de direitos em processo judicial",
            "security_title": "5. Medidas de Segurança",
            "security_text": "A Tutela Digital® adota controles técnicos de segurança, incluindo criptografia, controle de acesso, registro de auditoria e armazenamento segregado.",
            "retention_title": "6. Período de Retenção",
            "retention_text": "Os dados são mantidos pelo período contratado ou pelo prazo legal aplicável, o que for maior.",
            "rights_title": "7. Direitos do Titular",
            "rights_text": "Confirmação de existência de tratamento\nAcesso aos dados\nCorreção de dados incompletos ou inexatos\nAnonimização, bloqueio ou eliminação\nPortabilidade\nInformação sobre compartilhamento\nRevogação do consentimento",
            "contact_title": "8. Contato",
            "contact_text": "Para exercer seus direitos ou esclarecer dúvidas sobre esta política, entre em contato através do e-mail: contato@tuteladigital.com.br",
            "changes_title": "9. Alterações",
            "changes_text": "Esta Política de Privacidade pode ser atualizada. A versão vigente estará sempre disponível neste endereço.",
            "cta_title": "Consulte também nossos Termos de Custódia",
            "cta_text": "Para entender os termos técnicos e jurídicos da custódia probatória."
        },
        "en": {
            "title": "Privacy Policy and Data Protection",
            "subtitle": "Guidelines applicable to the processing of personal data in the context of digital evidentiary custody.",
            "scope_title": "1. Scope",
            "scope_text": "This Privacy Policy describes how Tutela Digital® processes personal data in compliance with Law No. 13.709/2018 (General Data Protection Law - LGPD).",
            "controller_title": "2. Data Controller",
            "controller_text": "Novaes & Coelho Ltda - NetCenter\nTax ID: 00.810.662/0001-27\nEmail: contato@tuteladigital.com.br",
            "data_collected_title": "3. Data Collected",
            "data_collected_text": "Only data necessary for holder identification, authentication, custody registration, and expert report issuance are collected. Includes: full name, CPF/CNPJ, email, phone, and address.",
            "purpose_title": "4. Purpose of Processing",
            "purpose_text": "Execution of digital evidentiary custody service\nDepositor identification\nCompliance with legal or regulatory obligation\nRegular exercise of rights in judicial proceedings",
            "security_title": "5. Security Measures",
            "security_text": "Tutela Digital® adopts technical security controls, including encryption, access control, audit logging, and segregated storage.",
            "retention_title": "6. Retention Period",
            "retention_text": "Data is retained for the contracted period or the applicable legal term, whichever is longer.",
            "rights_title": "7. Data Subject Rights",
            "rights_text": "Confirmation of processing existence\nAccess to data\nCorrection of incomplete or inaccurate data\nAnonymization, blocking, or deletion\nPortability\nInformation about sharing\nConsent withdrawal",
            "contact_title": "8. Contact",
            "contact_text": "To exercise your rights or clarify doubts about this policy, contact us via email: contato@tuteladigital.com.br",
            "changes_title": "9. Changes",
            "changes_text": "This Privacy Policy may be updated. The current version will always be available at this address.",
            "cta_title": "Also consult our Custody Terms",
            "cta_text": "To understand the technical and legal terms of evidentiary custody."
        },
        "es": {
            "title": "Política de Privacidad y Protección de Datos",
            "subtitle": "Directrices aplicables al tratamiento de datos personales en el contexto de la custodia probatoria digital.",
            "scope_title": "1. Alcance",
            "scope_text": "La presente Política de Privacidad describe cómo Tutela Digital® realiza el tratamiento de datos personales en conformidad con la Ley nº 13.709/2018 (Ley General de Protección de Datos - LGPD).",
            "controller_title": "2. Controlador de Datos",
            "controller_text": "Novaes & Coelho Ltda - NetCenter\nCNPJ: 00.810.662/0001-27\nCorreo electrónico: contato@tuteladigital.com.br",
            "data_collected_title": "3. Datos Recopilados",
            "data_collected_text": "Se recopilan solo los datos necesarios para la identificación del titular, autenticación, registro de custodia y emisión de informes periciales. Incluyen: nombre completo, CPF/CNPJ, correo electrónico, teléfono y dirección.",
            "purpose_title": "4. Finalidad del Tratamiento",
            "purpose_text": "Ejecución del servicio de custodia probatoria digital\nIdentificación del depositante\nCumplimiento de obligación legal o regulatoria\nEjercicio regular de derechos en proceso judicial",
            "security_title": "5. Medidas de Seguridad",
            "security_text": "Tutela Digital® adopta controles técnicos de seguridad, incluyendo encriptación, control de acceso, registro de auditoría y almacenamiento segregado.",
            "retention_title": "6. Período de Retención",
            "retention_text": "Los datos se mantienen por el período contratado o por el plazo legal aplicable, lo que sea mayor.",
            "rights_title": "7. Derechos del Titular",
            "rights_text": "Confirmación de existencia de tratamiento\nAcceso a los datos\nCorrección de datos incompletos o inexactos\nAnonimización, bloqueo o eliminación\nPortabilidad\nInformación sobre compartición\nRevocación del consentimiento",
            "contact_title": "8. Contacto",
            "contact_text": "Para ejercer sus derechos o aclarar dudas sobre esta política, contacte a través del correo electrónico: contato@tuteladigital.com.br",
            "changes_title": "9. Alteraciones",
            "changes_text": "Esta Política de Privacidad puede ser actualizada. La versión vigente estará siempre disponible en esta dirección.",
            "cta_title": "Consulte también nuestros Términos de Custodia",
            "cta_text": "Para entender los términos técnicos y jurídicos de la custodia probatoria."
        }
    }
    
    # Atualizar arquivos JSON
    for lang in ['pt', 'en', 'es']:
        file_path = Path(f'public/assets/lang/{lang}.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Adicionar chaves institucional
        if 'institucional' not in data:
            data['institucional'] = institucional_keys[lang]
            print(f"✅ Adicionadas chaves 'institucional' ao {lang}.json")
        
        # Atualizar chaves privacy
        if 'privacy' in data:
            data['privacy'].update(privacy_additional[lang])
            print(f"✅ Atualizadas chaves 'privacy' no {lang}.json")
        else:
            data['privacy'] = privacy_additional[lang]
            print(f"✅ Criadas chaves 'privacy' no {lang}.json")
        
        # Salvar arquivo
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Todos os arquivos JSON atualizados!")

def fix_lang_dropdown(content):
    """Converte dropdown de idiomas de links para botões"""
    # Padrão antigo
    old_pattern = r'<div class="lang-menu">\s*<a href="index\.html">Português</a>\s*<a href="index-en\.html">English</a>\s*<a href="index-es\.html">Español</a>\s*</div>'
    
    # Novo padrão com botões
    new_dropdown = '''<div class="lang-menu">
    <button class="lang-option" data-lang="pt">🇧🇷 Português</button>
    <button class="lang-option" data-lang="en">🇺🇸 English</button>
    <button class="lang-option" data-lang="es">🇪🇸 Español</button>
  </div>'''
    
    content = re.sub(old_pattern, new_dropdown, content)
    return content

def add_i18n_script(content):
    """Adiciona script i18n.js antes do navigation.js"""
    # Verificar se já existe
    if 'i18n.js' in content:
        return content
    
    # Adicionar antes do navigation.js
    pattern = r'(<script src="assets/js/navigation\.js"></script>)'
    replacement = r'<script src="assets/js/i18n.js"></script>\n\1'
    
    content = re.sub(pattern, replacement, content)
    return content

def process_institucional():
    """Processa institucional.html"""
    file_path = Path('public/institucional.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adicionar data-i18n attributes
    replacements = [
        (r'<h1>Estrutura Institucional</h1>', 
         r'<h1 data-i18n="institucional.title">Estrutura Institucional</h1>'),
        (r'<p>Informações jurídicas e estruturais da entidade responsável pela preservação probatória digital\.</p>',
         r'<p data-i18n="institucional.subtitle">Informações jurídicas e estruturais da entidade responsável pela preservação probatória digital.</p>'),
        (r'<h2>Identificação Jurídica</h2>',
         r'<h2 data-i18n="institucional.legalIdTitle">Identificação Jurídica</h2>'),
        (r'<h2>Natureza da Atividade</h2>',
         r'<h2 data-i18n="institucional.activityNatureTitle">Natureza da Atividade</h2>'),
        (r'<h2>Finalidade da Infraestrutura</h2>',
         r'<h2 data-i18n="institucional.purposeTitle">Finalidade da Infraestrutura</h2>'),
        (r'<h2>Base Jurídica Aplicável</h2>',
         r'<h2 data-i18n="institucional.legalBasisTitle">Base Jurídica Aplicável</h2>'),
        (r'<h2>Interoperabilidade Cartorial</h2>',
         r'<h2 data-i18n="institucional.interopTitle">Interoperabilidade Cartorial</h2>'),
        (r'<h2>Desenvolvimento e Governança</h2>',
         r'<h2 data-i18n="institucional.govTitle">Desenvolvimento e Governança</h2>'),
        (r'<h2>Transparência Institucional e Confiabilidade Jurídica</h2>',
         r'<h2 data-i18n="institucional.ctaTitle">Transparência Institucional e Confiabilidade Jurídica</h2>'),
    ]
    
    for old, new in replacements:
        content = re.sub(old, new, content)
    
    # Fix dropdown
    content = fix_lang_dropdown(content)
    
    # Add i18n script
    content = add_i18n_script(content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ institucional.html processado")

def process_privacy():
    """Processa politica-de-privacidade.html"""
    file_path = Path('public/politica-de-privacidade.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adicionar data-i18n attributes
    replacements = [
        (r'<h1>Política de Privacidade e Proteção de Dados</h1>',
         r'<h1 data-i18n="privacy.title">Política de Privacidade e Proteção de Dados</h1>'),
        (r'<p>Diretrizes aplicáveis ao tratamento de dados pessoais no contexto da custódia probatória digital\.</p>',
         r'<p data-i18n="privacy.subtitle">Diretrizes aplicáveis ao tratamento de dados pessoais no contexto da custódia probatória digital.</p>'),
        (r'<h2>1\. Escopo</h2>',
         r'<h2 data-i18n="privacy.scope_title">1. Escopo</h2>'),
        (r'<h2>2\. Controlador de Dados</h2>',
         r'<h2 data-i18n="privacy.controller_title">2. Controlador de Dados</h2>'),
        (r'<h2>3\. Dados Coletados</h2>',
         r'<h2 data-i18n="privacy.data_collected_title">3. Dados Coletados</h2>'),
        (r'<h2>4\. Finalidade do Tratamento</h2>',
         r'<h2 data-i18n="privacy.purpose_title">4. Finalidade do Tratamento</h2>'),
        (r'<h2>5\. Medidas de Segurança</h2>',
         r'<h2 data-i18n="privacy.security_title">5. Medidas de Segurança</h2>'),
        (r'<h2>6\. Período de Retenção</h2>',
         r'<h2 data-i18n="privacy.retention_title">6. Período de Retenção</h2>'),
        (r'<h2>7\. Direitos do Titular</h2>',
         r'<h2 data-i18n="privacy.rights_title">7. Direitos do Titular</h2>'),
        (r'<h2>8\. Contato</h2>',
         r'<h2 data-i18n="privacy.contact_title">8. Contato</h2>'),
        (r'<h2>9\. Alterações</h2>',
         r'<h2 data-i18n="privacy.changes_title">9. Alterações</h2>'),
        (r'<h2>Consulte também nossos Termos de Custódia</h2>',
         r'<h2 data-i18n="privacy.cta_title">Consulte também nossos Termos de Custódia</h2>'),
    ]
    
    for old, new in replacements:
        content = re.sub(old, new, content)
    
    # Fix dropdown
    content = fix_lang_dropdown(content)
    
    # Add i18n script
    content = add_i18n_script(content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ politica-de-privacidade.html processado")

def process_fundamento():
    """Processa fundamento-juridico.html"""
    file_path = Path('public/fundamento-juridico.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix dropdown
    content = fix_lang_dropdown(content)
    
    # Add i18n script
    content = add_i18n_script(content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ fundamento-juridico.html processado")

def main():
    print("=" * 80)
    print("🔧 CORREÇÃO DE PÁGINAS COM CONTEÚDO HARD-CODED")
    print("=" * 80)
    print()
    
    print("📝 FASE 1: Atualizando arquivos JSON...")
    add_i18n_keys()
    print()
    
    print("📝 FASE 2: Processando arquivos HTML...")
    process_institucional()
    process_privacy()
    process_fundamento()
    print()
    
    print("=" * 80)
    print("✅ CORREÇÃO COMPLETA!")
    print("=" * 80)
    print()
    print("Arquivos modificados:")
    print("  - public/assets/lang/pt.json")
    print("  - public/assets/lang/en.json")
    print("  - public/assets/lang/es.json")
    print("  - public/institucional.html")
    print("  - public/politica-de-privacidade.html")
    print("  - public/fundamento-juridico.html")
    print()

if __name__ == "__main__":
    main()
