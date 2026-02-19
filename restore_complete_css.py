#!/usr/bin/env python3
"""
Restauração COMPLETA do CSS Principal
======================================
Problema: styles-clean.css está com apenas footer/WhatsApp (391 linhas)
          Faltam ~255 linhas de CSS essencial (reset, layout, tipografia, etc.)

Solução: Restaurar CSS completo do commit fca74e4 (646 linhas) + adicionar footer/WhatsApp
"""

import subprocess
import os

def main():
    print("🔧 RESTAURAÇÃO COMPLETA DO CSS\n")
    
    # 1. Extrair CSS original do commit estável
    print("1️⃣ Extraindo CSS original do commit fca74e4...")
    result = subprocess.run(
        ["git", "show", "fca74e4:public/assets/css/styles-clean.css"],
        cwd="/home/user/webapp",
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Erro ao extrair CSS: {result.stderr}")
        return
    
    original_css = result.stdout
    original_lines = len(original_css.split('\n'))
    print(f"   ✅ CSS original: {original_lines} linhas extraídas")
    
    # 2. Adicionar CSS do Footer Institucional (4 colunas)
    print("\n2️⃣ Adicionando CSS do Footer Institucional...")
    footer_css = """

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
"""
    footer_lines = len(footer_css.split('\n'))
    print(f"   ✅ Footer CSS: {footer_lines} linhas preparadas")
    
    # 3. Adicionar CSS do WhatsApp Float
    print("\n3️⃣ Adicionando CSS do WhatsApp Float...")
    whatsapp_css = """

/* =======================================================
   WHATSAPP FLOATING BUTTON
   ======================================================= */

.whatsapp-float {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 58px;
  height: 58px;
  background-color: #20ba5a;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 9999;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none;
  cursor: pointer;
}

.whatsapp-float:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.whatsapp-float .whatsapp-icon {
  width: 32px;
  height: 32px;
  fill: #ffffff;
}

.whatsapp-tooltip {
  position: absolute;
  right: 70px;
  background: #0b3d2e;
  color: #ffffff;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 13px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.whatsapp-float:hover .whatsapp-tooltip {
  opacity: 1;
}

/* Mobile: esconder tooltip e reduzir botão */
@media (max-width: 768px) {
  .whatsapp-float {
    width: 54px;
    height: 54px;
    bottom: 20px;
    right: 20px;
  }
  
  .whatsapp-float .whatsapp-icon {
    width: 28px;
    height: 28px;
  }
  
  .whatsapp-tooltip {
    display: none;
  }
}
"""
    whatsapp_lines = len(whatsapp_css.split('\n'))
    print(f"   ✅ WhatsApp CSS: {whatsapp_lines} linhas preparadas")
    
    # 4. Combinar tudo
    print("\n4️⃣ Combinando CSS completo...")
    complete_css = original_css + footer_css + whatsapp_css
    total_lines = len(complete_css.split('\n'))
    
    # 5. Escrever arquivo final
    css_path = "/home/user/webapp/public/assets/css/styles-clean.css"
    print(f"\n5️⃣ Escrevendo CSS completo em {css_path}...")
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(complete_css)
    
    print(f"   ✅ Arquivo escrito com sucesso!")
    
    # 6. Verificar resultado
    print("\n📊 RESULTADO FINAL:")
    print(f"   • CSS Original: {original_lines} linhas")
    print(f"   • Footer CSS: {footer_lines} linhas")
    print(f"   • WhatsApp CSS: {whatsapp_lines} linhas")
    print(f"   • TOTAL: {total_lines} linhas")
    print(f"   • Tamanho: {len(complete_css):,} caracteres")
    
    print("\n✅ RESTAURAÇÃO COMPLETA CONCLUÍDA!")
    print("\n📋 Validação:")
    print("   1. CSS principal restaurado (reset, layout, tipografia)")
    print("   2. Footer institucional (4 colunas) adicionado")
    print("   3. WhatsApp float multilíngue adicionado")
    print("   4. Todas as páginas devem ter formatação completa")

if __name__ == "__main__":
    main()
