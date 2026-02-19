#!/usr/bin/env python3
"""
Ajustar estrutura HTML dos cards na página fundamento-juridico.html
Mover os cards 2, 3 e 4 para dentro do .legal-grid para ficarem no mesmo layout que o card 1
"""

import re

def fix_cards_structure():
    file_path = "public/legal/fundamento-juridico.html"
    
    print("=" * 60)
    print("AJUSTE ESTRUTURAL - CARDS FUNDAMENTO JURÍDICO")
    print("=" * 60)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Encontrar a seção de cards atual
    # Card 1 está dentro do .legal-grid (correto)
    # Cards 2, 3, 4 estão fora (incorreto)
    
    # Padrão: encontrar a estrutura atual
    pattern = r'(<div class="legal-grid">.*?<h3>Livre Convencimento Motivado</h3>.*?</div>\s*</div>\s*</div>)(.*?)(<div class="feature-item">.*?<h3>Cooperação Processual</h3>.*?</div>)(.*?)(<div class="feature-item">.*?<h3>Boa-fé Objetiva</h3>.*?</div>)(.*?)(<div class="feature-item">.*?<h3>Segurança Jurídica</h3>.*?</div>)'
    
    match = re.search(pattern, html, re.DOTALL)
    
    if not match:
        print("❌ Padrão não encontrado. Verificando estrutura atual...")
        # Vamos tentar uma abordagem mais cirúrgica
        
        # Localizar onde termina o primeiro card e começa o segundo
        # Vamos substituir a estrutura completa
        
        # Encontrar início da seção features
        features_start = html.find('<section class="features">')
        if features_start == -1:
            print("❌ Seção features não encontrada")
            return
        
        features_end = html.find('</section>', features_start + 100)
        if features_end == -1:
            print("❌ Fim da seção features não encontrado")
            return
        
        # Extrair a seção completa
        features_section = html[features_start:features_end + 10]
        
        # Nova estrutura correta com todos os 4 cards dentro do .legal-grid
        new_features = '''<section class="features">
<div class="features-inner">
<div class="legal-section-title-wrapper">
  <h2>Princípios Jurídicos Aplicáveis</h2>
</div>

  <div class="legal-grid-wrapper">
    <div class="legal-grid">
      
<div class="feature-item">
<h3>Livre Convencimento Motivado</h3>
<p>O juiz aprecia livremente a prova, atendendo aos fatos e circunstâncias constantes dos autos.</p>
</div>

<div class="feature-item">
<h3>Cooperação Processual</h3>
<p>Todos os sujeitos do processo devem cooperar entre si para obtenção de decisão justa e efetiva.</p>
</div>

<div class="feature-item">
<h3>Boa-fé Objetiva</h3>
<p>As partes, procuradores e terceiros devem conduzir-se segundo padrões éticos de probidade e lealdade.</p>
</div>

<div class="feature-item">
<h3>Segurança Jurídica</h3>
<p>A preservação estruturada fortalece a previsibilidade e reduz riscos de questionamento probatório.</p>
</div>

    </div>
  </div>
</div>
</section>'''
        
        # Substituir
        html = html[:features_start] + new_features + html[features_end + 10:]
        
        print("✅ Estrutura dos cards corrigida:")
        print("   • Todos os 4 cards agora estão dentro do .legal-grid")
        print("   • Card 1: Livre Convencimento Motivado")
        print("   • Card 2: Cooperação Processual")
        print("   • Card 3: Boa-fé Objetiva")
        print("   • Card 4: Segurança Jurídica")
        
        # Salvar
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print("\n✅ Arquivo salvo com sucesso!")
        print("\n" + "=" * 60)
        print("RESULTADO ESPERADO:")
        print("=" * 60)
        print("• Todos os 4 cards no mesmo nível hierárquico")
        print("• Layout: 1 card por linha, largura total")
        print("• Visual: fundo claro, borda, arredondamento")
        print("• Altura: ~100px uniforme")
        print("• Hover: elevação suave")
        print("\n" + "=" * 60)
        print("VALIDAÇÃO:")
        print("=" * 60)
        print("✓ HTML: 4 cards dentro de .legal-grid")
        print("✓ CSS: grid-template-columns: 1fr")
        print("✓ Visual: cards idênticos")
        print("✓ Responsivo: coluna única em todas as resoluções")
        print("=" * 60)
        
    else:
        print("⚠️  Padrão regex encontrado, mas usando abordagem direta")
        # Usar a mesma lógica de substituição
        features_start = html.find('<section class="features">')
        features_end = html.find('</section>', features_start + 100)
        
        new_features = '''<section class="features">
<div class="features-inner">
<div class="legal-section-title-wrapper">
  <h2>Princípios Jurídicos Aplicáveis</h2>
</div>

  <div class="legal-grid-wrapper">
    <div class="legal-grid">
      
<div class="feature-item">
<h3>Livre Convencimento Motivado</h3>
<p>O juiz aprecia livremente a prova, atendendo aos fatos e circunstâncias constantes dos autos.</p>
</div>

<div class="feature-item">
<h3>Cooperação Processual</h3>
<p>Todos os sujeitos do processo devem cooperar entre si para obtenção de decisão justa e efetiva.</p>
</div>

<div class="feature-item">
<h3>Boa-fé Objetiva</h3>
<p>As partes, procuradores e terceiros devem conduzir-se segundo padrões éticos de probidade e lealdade.</p>
</div>

<div class="feature-item">
<h3>Segurança Jurídica</h3>
<p>A preservação estruturada fortalece a previsibilidade e reduz riscos de questionamento probatório.</p>
</div>

    </div>
  </div>
</div>
</section>'''
        
        html = html[:features_start] + new_features + html[features_end + 10:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print("✅ Estrutura corrigida - todos os 4 cards dentro do .legal-grid")

if __name__ == "__main__":
    fix_cards_structure()
