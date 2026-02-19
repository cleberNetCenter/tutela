#!/usr/bin/env python3
"""
CORREÇÃO CRÍTICA: Restaurar CSS Principal + Adicionar Footer/WhatsApp
O script anterior DELETOU o CSS principal. Este script ADICIONA sem deletar.
"""

from pathlib import Path

BASE_DIR = Path("public")

# CSS do Footer (para adicionar ao final)
FOOTER_CSS = '''

/* =======================================================
   FOOTER INSTITUCIONAL (4 COLUNAS)
   ======================================================= */

.footer {
  background: linear-gradient(180deg, #052e24, #031f18);
  color: #d9efe7;
  padding: 60px 40px 30px;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
}

.footer-col h3 {
  font-weight: 600;
  margin-bottom: 20px;
  font-size: 20px;
  letter-spacing: 0.5px;
  color: #ffffff;
}

.footer-col h4 {
  font-weight: 600;
  margin-bottom: 15px;
  font-size: 16px;
  letter-spacing: 0.5px;
  color: #ffffff;
  text-transform: none;
}

.footer-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-col ul li {
  margin-bottom: 10px;
}

.footer-col a {
  text-decoration: none;
  color: #b5d6c8;
  transition: color 0.3s ease;
  font-size: 14px;
  display: inline-block;
}

.footer-col a:hover {
  color: #ffffff;
}

.footer-brand-col p {
  margin: 8px 0;
  font-size: 14px;
}

.footer-brand-col a {
  color: #b5d6c8;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-brand-col a:hover {
  color: #ffffff;
}

.footer-social-icon {
  width: 18px;
  height: 18px;
  vertical-align: middle;
  margin-right: 5px;
}

.footer-bottom {
  text-align: center;
  margin-top: 50px;
  padding-top: 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 14px;
  opacity: 0.7;
}

/* Responsividade Footer */
@media (max-width: 992px) {
  .footer-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 35px;
  }
}

@media (max-width: 768px) {
  .footer {
    padding: 40px 20px 20px;
  }
  
  .footer-container {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .footer-bottom {
    margin-top: 35px;
    padding-top: 25px;
  }
}

/* Remove estilos antigos do footer */
.footer-inner {
  display: none;
}

.footer-links {
  display: none;
}

.footer-copy {
  display: none;
}
'''

# CSS do WhatsApp (para adicionar ao final)
WHATSAPP_CSS = '''

/* =======================================================
   WHATSAPP FLOATING BUTTON
   ======================================================= */

.whatsapp-float {
  position: fixed;
  bottom: 25px;
  right: 25px;
  background: #25D366;
  color: #fff;
  width: 58px;
  height: 58px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(0,0,0,0.25);
  z-index: 9999;
  transition: transform 0.3s ease;
  text-decoration: none;
}

.whatsapp-float:hover {
  transform: scale(1.08);
  background: #20ba5a;
}

.whatsapp-icon {
  width: 32px;
  height: 32px;
}

.whatsapp-tooltip {
  position: absolute;
  right: 70px;
  background: #0b3d2e;
  color: #fff;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 13px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.whatsapp-float:hover .whatsapp-tooltip {
  opacity: 1;
}

@media (max-width: 768px) {
  .whatsapp-float {
    bottom: 20px;
    right: 20px;
    width: 54px;
    height: 54px;
  }
  
  .whatsapp-icon {
    width: 28px;
    height: 28px;
  }
  
  .whatsapp-tooltip {
    display: none;
  }
}
'''

def fix_css_file():
    """
    Adiciona CSS do footer e WhatsApp SEM deletar o CSS existente
    """
    
    css_file = BASE_DIR / "assets/css/styles-clean.css"
    
    print("\n" + "="*60)
    print("  CORREÇÃO CRÍTICA: CSS Principal")
    print("="*60)
    
    print(f"\n📄 Corrigindo: {css_file.relative_to(BASE_DIR)}")
    
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    print(f"  • Tamanho atual: {len(css_content)} caracteres")
    print(f"  • Linhas atuais: {len(css_content.splitlines())} linhas")
    
    # Verifica se já tem o CSS do footer
    if '/* FOOTER INSTITUCIONAL (4 COLUNAS) */' not in css_content:
        print(f"  • Adicionando CSS do footer...")
        css_content += FOOTER_CSS
    else:
        print(f"  ✓ CSS do footer já existe")
    
    # Verifica se já tem o CSS do WhatsApp
    if '/* WHATSAPP FLOATING BUTTON */' not in css_content:
        print(f"  • Adicionando CSS do WhatsApp...")
        css_content += WHATSAPP_CSS
    else:
        print(f"  ✓ CSS do WhatsApp já existe")
    
    # Salva CSS atualizado
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print(f"\n✅ CSS corrigido!")
    print(f"  • Tamanho final: {len(css_content)} caracteres")
    print(f"  • Linhas finais: {len(css_content.splitlines())} linhas")

def main():
    print("\n" + "="*60)
    print("  CORREÇÃO CRÍTICA: Restaurar CSS Principal")
    print("="*60)
    
    print("\n🐛 PROBLEMA:")
    print("  • Script anterior DELETOU o CSS principal")
    print("  • Só restou CSS do footer e WhatsApp")
    print("  • Todas as páginas perderam formatação")
    
    print("\n✅ SOLUÇÃO:")
    print("  • CSS principal foi restaurado do commit anterior")
    print("  • Agora vamos ADICIONAR (não substituir) CSS do footer/WhatsApp")
    
    fix_css_file()
    
    print("\n" + "="*60)
    print("✅ CORREÇÃO CONCLUÍDA!")
    print("="*60)
    
    print("\n📊 RESULTADO:")
    print("  ✅ CSS principal mantido")
    print("  ✅ CSS do footer adicionado")
    print("  ✅ CSS do WhatsApp adicionado")
    print("  ✅ Todas as páginas devem estar formatadas corretamente")
    
    print("\n🧪 TESTES:")
    print("  1. Abrir https://tuteladigital.com.br/")
    print("  2. Verificar se a página está formatada corretamente")
    print("  3. Verificar se o footer está correto (4 colunas)")
    print("  4. Verificar se o botão WhatsApp está visível")
    print("  5. Testar em todas as páginas")

if __name__ == '__main__':
    main()
