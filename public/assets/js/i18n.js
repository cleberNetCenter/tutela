// =======================================================
// SISTEMA DE INTERNACIONALIZAÇÃO — Tutela Digital®
// PT (pt-BR) | EN (en) | ES (es)
// =======================================================

const I18N = {
  currentLang: 'pt',
  translations: {},
  fallbackLang: 'pt',

  // Mapa de compatibilidade: chaves antigas → novas
  keyMap: {
    // Meta & Global
    'site_title': 'global.brand',
    'site_description': 'home.heroSubtitle',
    
    // Navigation
    'nav_home': 'navigation.home',
    'nav_governo': 'navigation.government',
    'nav_empresas': 'navigation.companies',
    'nav_pessoas': 'navigation.individuals',
    'nav_como_funciona': 'navigation.howItWorks',
    'nav_seguranca': 'navigation.security',
    'nav_preservacao': 'navigation.preservation',
    'nav_fundamento': 'navigation.legalBasis',
    'nav_termos': 'navigation.terms',
    'nav_privacy': 'navigation.privacy',
    'nav_cta': 'global.accessPlatform',
    
    // Home Hero
    'hero_subtitle': 'home.heroSubtitle',
    'home_verticals_title': 'home.heroTitle',
    
    // Home Intro (Trust)
    'home_trust_title': 'home.introTitle',
    'home_trust_p1': 'home.introP1',
    'home_trust_p2': 'home.introP2',
    'home_trust_p3': 'home.introP3',
    
    // Home Verticals (Soluções por Segmento)
    'home_verticals_gov': 'navigation.government',
    'home_verticals_gov_desc': 'government.heroTitle',
    'home_verticals_corp': 'navigation.companies',
    'home_verticals_corp_desc': 'companies.heroTitle',
    'home_verticals_personal': 'navigation.individuals',
    'home_verticals_personal_desc': 'individuals.heroTitle',
    
    // Home Pillars
    'home_pillars_title': 'home.pillarsTitle',
    'home_pillars_preservation': 'home.pillar1Title',
    'home_pillars_preservation_desc': 'home.pillar1Desc',
    'home_pillars_integrity': 'home.pillar2Title',
    'home_pillars_integrity_desc': 'home.pillar2Desc',
    'home_pillars_custody': 'home.pillar3Title',
    'home_pillars_custody_desc': 'home.pillar3Desc',
    'home_pillars_admissibility': 'home.pillar3Title',
    'home_pillars_admissibility_desc': 'home.pillar3Desc',
    
    // Home Applicability
    'home_applicability_title': 'preservation.title',
    'home_applicability_desc': 'preservation.p1',
    
    // Home CTA
    'home_cta_title': 'global.ctaPrimary',
    'home_cta_desc': 'global.ctaInstitutional',
    'home_cta_button': 'global.accessPlatform'
  },

  /**
   * Inicializa o sistema i18n
   */
  async init() {
    // Detecta idioma salvo ou do navegador
    const savedLang = localStorage.getItem('tutela_lang');
    const browserLang = navigator.language.split('-')[0];
    const supportedLangs = ['pt', 'en', 'es'];
    
    this.currentLang = savedLang || 
      (supportedLangs.includes(browserLang) ? browserLang : 'pt');

    // Carrega traduções
    await this.loadTranslations(this.currentLang);
    
    // Aplica traduções
    this.applyTranslations();
    
    // Atualiza UI do seletor de idioma
    this.updateLanguageSelector();
    
    // Atualiza atributo lang do HTML
    document.documentElement.lang = this.getLangCode(this.currentLang);
    
    console.log('[i18n] Sistema inicializado:', this.currentLang);
  },

  /**
   * Carrega arquivo JSON de traduções
   */
  async loadTranslations(lang) {
    try {
      const response = await fetch(`assets/lang/${lang}.json?v=8`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      this.translations = await response.json();
      console.log(`[i18n] Traduções carregadas: ${lang}.json (${Object.keys(this.translations).length} seções)`);
    } catch (error) {
      console.error(`[i18n] Erro ao carregar ${lang}.json:`, error);
      if (lang !== this.fallbackLang) {
        console.warn('[i18n] Carregando fallback (pt)...');
        await this.loadTranslations(this.fallbackLang);
      }
    }
  },

  /**
   * Aplica traduções em todos os elementos com data-i18n
   */
  applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.dataset.i18n;
      const translation = this.t(key);
      
      if (translation) {
        // Suporta texto simples ou HTML
        if (el.dataset.i18nHtml === 'true') {
          el.innerHTML = translation;
        } else {
          el.textContent = translation;
        }
      } else {
        console.warn(`[i18n] Chave não encontrada: "${key}"`);
      }
    });

    // Traduz placeholders de inputs
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.dataset.i18nPlaceholder;
      const translation = this.t(key);
      if (translation) {
        el.placeholder = translation;
      }
    });

    // Traduz atributos alt de imagens
    document.querySelectorAll('[data-i18n-alt]').forEach(el => {
      const key = el.dataset.i18nAlt;
      const translation = this.t(key);
      if (translation) {
        el.alt = translation;
      }
    });

    // Traduz atributos title
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const key = el.dataset.i18nTitle;
      const translation = this.t(key);
      if (translation) {
        el.title = translation;
      }
    });

    // Mostra aviso para páginas legais em idioma não-PT
    this.showLegalPageNoticeIfNeeded();
  },

  /**
   * Mostra banner de aviso em páginas legais quando idioma não é PT
   */
  showLegalPageNoticeIfNeeded() {
    // Lista de páginas legais (apenas texto em PT)
    const legalPages = [
      'page-institucional',
      'page-politica-de-privacidade',
      'page-fundamento-juridico',
      'page-termos-de-custodia'
    ];

    // Verifica se estamos em uma página legal
    const isLegalPage = legalPages.some(pageId => 
      document.getElementById(pageId)?.classList.contains('active')
    );

    // Se não for página legal ou idioma for PT, remove aviso (se existir)
    if (!isLegalPage || this.currentLang === 'pt') {
      const existingNotice = document.getElementById('legal-lang-notice');
      if (existingNotice) {
        existingNotice.remove();
      }
      return;
    }

    // Se já existe aviso, não cria outro
    if (document.getElementById('legal-lang-notice')) {
      return;
    }

    // Mensagens de aviso por idioma
    const messages = {
      'en': '⚠️ Legal Information: This document is available in Portuguese only. For complete understanding, please switch to Portuguese (PT).',
      'es': '⚠️ Información Legal: Este documento está disponible solo en portugués. Para una comprensión completa, cambie a portugués (PT).'
    };

    // Cria banner de aviso
    const notice = document.createElement('div');
    notice.id = 'legal-lang-notice';
    notice.style.cssText = `
      position: sticky;
      top: 0;
      z-index: 9999;
      background: #fff3cd;
      color: #856404;
      padding: 16px 24px;
      text-align: center;
      font-size: 14px;
      line-height: 1.6;
      border-bottom: 2px solid #ffc107;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    `;
    notice.innerHTML = `
      <strong style="display: block; margin-bottom: 8px;">⚠️ ${this.currentLang === 'en' ? 'Language Notice' : 'Aviso de Idioma'}</strong>
      <p style="margin: 0;">${messages[this.currentLang]}</p>
      <button onclick="I18N.switchLanguage('pt')" style="
        margin-top: 12px;
        padding: 8px 16px;
        background: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-weight: 600;
      ">
        Switch to Portuguese (PT) / Cambiar a Portugués (PT)
      </button>
    `;

    // Insere no topo da página
    const main = document.querySelector('.main');
    if (main) {
      main.insertBefore(notice, main.firstChild);
    }
  },

  /**
   * Troca de idioma
   */
  async switchLanguage(lang) {
    if (this.currentLang === lang) return;
    
    // Salva idioma no localStorage
    localStorage.setItem('tutela_lang', lang);
    
    // Fecha o menu dropdown
    const dropdown = document.querySelector('.lang-dropdown');
    if (dropdown) {
      dropdown.classList.remove('active');
    }
    
    // Recarrega a página para aplicar traduções completas
    console.log('[i18n] Idioma alterado para:', lang, '- Recarregando página...');
    window.location.reload();
  },

  /**
   * Atualiza UI do seletor de idioma
   */
  updateLanguageSelector() {
    const langCode = document.querySelector('.lang-code');
    if (langCode) {
      langCode.textContent = this.currentLang.toUpperCase();
    }

    // Marca idioma ativo no menu
    document.querySelectorAll('.lang-option').forEach(option => {
      option.classList.toggle('active', option.dataset.lang === this.currentLang);
    });
  },

  /**
   * Retorna código de idioma completo
   */
  getLangCode(lang) {
    const codes = {
      'pt': 'pt-BR',
      'en': 'en',
      'es': 'es'
    };
    return codes[lang] || 'pt-BR';
  },

  /**
   * Atualiza inLanguage nos schemas JSON-LD
   */
  updateSchemaLanguage(lang) {
    document.querySelectorAll('script[type="application/ld+json"]').forEach(script => {
      try {
        const schema = JSON.parse(script.textContent);
        const langCode = this.getLangCode(lang);
        
        if (schema.inLanguage) {
          schema.inLanguage = langCode;
        }
        
        // Atualiza script
        script.textContent = JSON.stringify(schema, null, 2);
      } catch (e) {
        console.warn('[i18n] Erro ao atualizar schema:', e);
      }
    });
  },

  /**
   * Retorna tradução por chave (uso programático)
   * Suporta chaves aninhadas: "global.brand" ou "navigation.home"
   * Suporta chaves antigas com underscore via keyMap
   */
  t(key) {
    if (!key) return '';
    
    // Converte chave antiga para nova (se existir no mapa)
    const mappedKey = this.keyMap[key] || key;
    
    // Se a chave contém ponto, navega pelo objeto
    if (mappedKey.includes('.')) {
      const keys = mappedKey.split('.');
      let value = this.translations;
      
      for (const k of keys) {
        value = value?.[k];
        if (value === undefined) {
          console.warn(`[i18n] Chave aninhada não encontrada: "${mappedKey}" (original: "${key}")`);
          return key;
        }
      }
      
      return value || key;
    }
    
    // Chave simples
    return this.translations[mappedKey] || key;
  }
};

// =======================================================
// INICIALIZAÇÃO AUTOMÁTICA
// =======================================================

document.addEventListener('DOMContentLoaded', () => {
  I18N.init();
});

// =======================================================
// EVENT LISTENERS PARA SELETOR DE IDIOMA
// =======================================================

document.addEventListener('click', (e) => {
  // Troca de idioma
  if (e.target.matches('.lang-option')) {
    const lang = e.target.dataset.lang;
    if (lang) {
      I18N.switchLanguage(lang);
    }
  }

  // Toggle dropdown
  if (e.target.matches('.lang-toggle')) {
    const dropdown = document.querySelector('.lang-dropdown');
    if (dropdown) {
      dropdown.classList.toggle('active');
    }
  }

  // Fecha dropdown ao clicar fora
  if (!e.target.closest('.lang-dropdown')) {
    document.querySelectorAll('.lang-dropdown').forEach(d => {
      d.classList.remove('active');
    });
  }
});

// Exporta para uso global
window.I18N = I18N;

// =======================================================
// RE-APLICAR TRADUÇÕES APÓS NAVEGAÇÃO (SPA)
// =======================================================

// Observa mudanças de classe .active nas páginas
const pageObserver = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
      const target = mutation.target;
      if (target.classList.contains('page') && target.classList.contains('active')) {
        // Página foi ativada, re-aplicar traduções
        console.log('[i18n] Página ativada, aplicando traduções:', target.id);
        I18N.applyTranslations();
      }
    }
  });
});

// Observar todas as páginas
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.page').forEach(page => {
    pageObserver.observe(page, { attributes: true, attributeFilter: ['class'] });
  });
});
