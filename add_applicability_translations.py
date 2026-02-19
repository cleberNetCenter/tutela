#!/usr/bin/env python3
"""
Script para adicionar traduções da seção "Aplicabilidade Jurídica" 
na página principal (index.html) para EN e ES
"""

import json

def add_translations():
    """Adiciona as traduções faltantes nos arquivos de idioma"""
    
    # Traduções para adicionar
    translations = {
        'pt': {
            'home_applicability_title': 'Aplicabilidade Jurídica',
            'home_applicability_desc': 'A preservação probatória digital pode ser utilizada para instrução de processos judiciais, defesas administrativas, procedimentos arbitrais, investigações internas e formalizações notariais, conforme avaliação da autoridade competente.'
        },
        'en': {
            'home_applicability_title': 'Legal Applicability',
            'home_applicability_desc': 'Digital evidentiary preservation can be used for judicial proceedings, administrative defenses, arbitration procedures, internal investigations and notarial formalizations, subject to evaluation by the competent authority.'
        },
        'es': {
            'home_applicability_title': 'Aplicabilidad Jurídica',
            'home_applicability_desc': 'La preservación probatoria digital puede utilizarse para instruir procesos judiciales, defensas administrativas, procedimientos arbitrales, investigaciones internas y formalizaciones notariales, conforme a la evaluación de la autoridad competente.'
        }
    }
    
    files_updated = []
    
    for lang, keys in translations.items():
        file_path = f'public/assets/lang/{lang}.json'
        
        try:
            # Ler arquivo JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verificar se a seção "home" existe
            if 'home' not in data:
                data['home'] = {}
                print(f"⚠️  Seção 'home' não existia em {lang}.json, criando...")
            
            # Verificar se as chaves já existem
            keys_added = []
            for key, value in keys.items():
                if key not in data['home']:
                    data['home'][key] = value
                    keys_added.append(key)
                else:
                    print(f"⏭️  Chave '{key}' já existe em {lang}.json")
            
            if keys_added:
                # Salvar arquivo JSON
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                files_updated.append(lang)
                print(f"✅ {file_path} atualizado com {len(keys_added)} chaves: {', '.join(keys_added)}")
            else:
                print(f"⏭️  {file_path} já contém todas as chaves necessárias")
        
        except FileNotFoundError:
            print(f"❌ Arquivo {file_path} não encontrado")
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao parsear JSON em {file_path}: {e}")
        except Exception as e:
            print(f"❌ Erro ao processar {file_path}: {e}")
    
    return files_updated

if __name__ == "__main__":
    print("🌐 Adicionando traduções da seção 'Aplicabilidade Jurídica'...\n")
    
    files_updated = add_translations()
    
    print(f"\n✅ Script concluído!")
    print(f"📊 Arquivos atualizados: {len(files_updated)}")
    
    if files_updated:
        print(f"🔤 Idiomas: {', '.join(files_updated).upper()}")
        print("\n📋 Próximos passos:")
        print("  1. Verificar as traduções nos arquivos JSON")
        print("  2. Testar a página em EN e ES")
        print("  3. Fazer commit das mudanças")
        print("  4. Criar pull request")
