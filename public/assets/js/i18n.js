// =======================================================
// SISTEMA DE INTERNACIONALIZAÇÃO — Tutela Digital®
// PT (pt-BR) | EN (en) | ES (es)
// =======================================================

const I18N = {
  currentLang: 'pt',
  translations: {},
  fallbackLang: 'pt',

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
      const response = await fetch(`assets/lang/${lang}.json?v=1`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      this.translations = await response.json();
      console.log(`[i18n] Traduções carregadas: ${lang}.json`);
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
      const translation = this.translations[key];
      
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
      const translation = this.translations[key];
      if (translation) {
        el.placeholder = translation;
      }
    });

    // Traduz atributos alt de imagens
    document.querySelectorAll('[data-i18n-alt]').forEach(el => {
      const key = el.dataset.i18nAlt;
      const translation = this.translations[key];
      if (translation) {
        el.alt = translation;
      }
    });

    // Traduz atributos title
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const key = el.dataset.i18nTitle;
      const translation = this.translations[key];
      if (translation) {
        el.title = translation;
      }
    });
  },

  /**
   * Troca de idioma
   */
  async switchLanguage(lang) {
    if (this.currentLang === lang) return;
    
    this.currentLang = lang;
    localStorage.setItem('tutela_lang', lang);
    
    await this.loadTranslations(lang);
    this.applyTranslations();
    this.updateLanguageSelector();
    
    // Atualiza atributo lang do HTML
    document.documentElement.lang = this.getLangCode(lang);
    
    // Atualiza schemas JSON-LD (se existirem)
    this.updateSchemaLanguage(lang);
    
    console.log('[i18n] Idioma alterado para:', lang);
  },

  /**
   * Atualiza UI do seletor de idioma
   */
  updateLanguageSelector() {
    const toggle = document.querySelector('.lang-toggle');
    if (toggle) {
      toggle.textContent = this.currentLang.toUpperCase();
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
   */
  t(key) {
    return this.translations[key] || key;
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
