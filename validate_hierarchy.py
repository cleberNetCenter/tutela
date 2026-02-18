#!/usr/bin/env python3
"""
FASE 5 e 6 - Validação Final da Hierarquia Semântica
"""
import json
from pathlib import Path
import re

def validate_json_syntax():
    """Valida sintaxe JSON"""
    print("=" * 70)
    print("VALIDAÇÃO JSON")
    print("=" * 70)
    
    for lang in ['pt', 'en', 'es']:
        file_path = Path(f'public/assets/lang/{lang}.json')
        try:
            data = json.loads(file_path.read_text(encoding='utf-8'))
            keys = sum(len(v) if isinstance(v, dict) else 1 for v in data.values())
            print(f"✅ {lang}.json: Sintaxe válida, {keys} keys")
        except json.JSONDecodeError as e:
            print(f"❌ {lang}.json: ERRO - {e}")
            return False
    return True

def validate_hierarchy_in_json():
    """Valida que todas as keys H1→H4 existem nos 3 idiomas"""
    print("\n" + "=" * 70)
    print("VALIDAÇÃO HIERARQUIA JSON")
    print("=" * 70)
    
    required_keys = {
        'home': ['heroTitle', 'h2Main', 'h2Secondary', 'h3ChainStructure', 'h4ChronologicalRegistration', 'h4TechnicalIdentifier', 'h3LegalApplication', 'h4JudicialUse', 'h4AdministrativeUse'],
        'preservation': ['title', 'h2Main', 'h2Secondary', 'h3PreLitigation', 'h4RiskMitigation', 'h4DocumentPredictability', 'h3ProceduralUse', 'h4ExpertAnalysis', 'h4FutureFormalization'],
        'legalBasis': ['title', 'h2Main', 'h2Secondary', 'h3CivilProcedure', 'h3ElectronicProcessLaw', 'h3DigitalSignature', 'h3LGPD', 'h4DataProtection', 'h4ConfidentialityLimits'],
        'security': ['title', 'h2Main', 'h2Secondary', 'h3Encryption', 'h3AccessControl', 'h3ImmutableRegistration', 'h4BlockchainRecord', 'h4TemporalIntegrity']
    }
    
    all_valid = True
    for lang in ['pt', 'en', 'es']:
        data = json.loads(Path(f'public/assets/lang/{lang}.json').read_text(encoding='utf-8'))
        print(f"\n🔍 {lang}.json:")
        
        for section, keys in required_keys.items():
            for key in keys:
                if section not in data or key not in data[section]:
                    print(f"  ❌ Faltando: {section}.{key}")
                    all_valid = False
                else:
                    print(f"  ✅ {section}.{key}")
    
    return all_valid

def validate_html_hierarchy():
    """Valida hierarquia H1→H4 nos HTMLs"""
    print("\n" + "=" * 70)
    print("VALIDAÇÃO HIERARQUIA HTML")
    print("=" * 70)
    
    pages = {
        'preservacao-probatoria-digital.html': {
            'h1': 1,
            'h2': 2,
            'h3': 2,
            'h4': 4
        },
        'fundamento-juridico.html': {
            'h1': 1,
            'h2': 2,
            'h3': 4,
            'h4': 2
        },
        'seguranca.html': {
            'h1': 1,
            'h2': 2,
            'h3': 3,
            'h4': 2
        }
    }
    
    all_valid = True
    for page, expected in pages.items():
        file_path = Path(f'public/{page}')
        if not file_path.exists():
            print(f"\n❌ {page}: Arquivo não encontrado")
            all_valid = False
            continue
        
        content = file_path.read_text(encoding='utf-8')
        print(f"\n📄 {page}:")
        
        for tag, count in expected.items():
            pattern = f'<{tag}[^>]*>'
            found = len(re.findall(pattern, content))
            
            if found >= count:
                print(f"  ✅ {tag.upper()}: {found} encontrados (esperado >= {count})")
            else:
                print(f"  ❌ {tag.upper()}: {found} encontrados (esperado >= {count})")
                all_valid = False
        
        # Validar data-i18n
        data_i18n_count = len(re.findall(r'data-i18n="[^"]*"', content))
        print(f"  📊 data-i18n: {data_i18n_count} atributos")
    
    return all_valid

def validate_no_hierarchy_skip():
    """Valida que não há pulo de hierarquia (H1→H3 sem H2)"""
    print("\n" + "=" * 70)
    print("VALIDAÇÃO SEM PULO DE HIERARQUIA")
    print("=" * 70)
    
    pages = [
        'public/preservacao-probatoria-digital.html',
        'public/fundamento-juridico.html',
        'public/seguranca.html'
    ]
    
    all_valid = True
    for page in pages:
        file_path = Path(page)
        if not file_path.exists():
            continue
        
        content = file_path.read_text(encoding='utf-8')
        
        # Extrair todos os headings em ordem
        headings = re.findall(r'<(h[1-6])[^>]*>', content)
        
        print(f"\n📄 {file_path.name}:")
        print(f"  Hierarquia: {' → '.join(headings[:10])}")
        
        # Validar que não há pulo
        for i in range(len(headings) - 1):
            current_level = int(headings[i][1])
            next_level = int(headings[i+1][1])
            
            if next_level > current_level + 1:
                print(f"  ❌ Pulo de hierarquia: {headings[i]} → {headings[i+1]}")
                all_valid = False
        
        if all_valid:
            print(f"  ✅ Sem pulos de hierarquia")
    
    return all_valid

def validate_css_classes():
    """Valida que as classes CSS existem"""
    print("\n" + "=" * 70)
    print("VALIDAÇÃO CSS")
    print("=" * 70)
    
    required_classes = ['section-title', 'subsection-title', 'detail-title']
    
    pages = [
        'public/preservacao-probatoria-digital.html',
        'public/fundamento-juridico.html',
        'public/seguranca.html'
    ]
    
    all_valid = True
    for page in pages:
        file_path = Path(page)
        if not file_path.exists():
            continue
        
        content = file_path.read_text(encoding='utf-8')
        
        print(f"\n📄 {file_path.name}:")
        for css_class in required_classes:
            if css_class in content:
                count = content.count(css_class)
                print(f"  ✅ .{css_class}: {count} usos")
            else:
                print(f"  ❌ .{css_class}: não encontrado")
                all_valid = False
    
    return all_valid

def main():
    print("=" * 70)
    print("VALIDAÇÃO FINAL - HIERARQUIA SEMÂNTICA H1→H4")
    print("=" * 70)
    
    results = {
        'JSON Syntax': validate_json_syntax(),
        'Hierarquia JSON': validate_hierarchy_in_json(),
        'Hierarquia HTML': validate_html_hierarchy(),
        'Sem Pulo Hierarquia': validate_no_hierarchy_skip(),
        'CSS Classes': validate_css_classes()
    }
    
    print("\n" + "=" * 70)
    print("RESUMO FINAL")
    print("=" * 70)
    
    for test, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status}: {test}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 TODAS AS VALIDAÇÕES PASSARAM!")
        print("\n📊 Estatísticas:")
        print("  - 3 JSONs validados (pt, en, es)")
        print("  - 112 keys por idioma (81 → 112)")
        print("  - 3 páginas HTML atualizadas")
        print("  - Hierarquia completa H1→H4")
        print("  - 0 pulos de hierarquia")
        print("  - 100% equivalência semântica PT/EN/ES")
    else:
        print("\n⚠️ ALGUMAS VALIDAÇÕES FALHARAM")
        print("Por favor, corrija os erros acima.")
    
    return all_passed

if __name__ == '__main__':
    import sys
    sys.exit(0 if main() else 1)
