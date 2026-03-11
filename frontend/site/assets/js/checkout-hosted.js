(function () {
  const form = document.querySelector('[data-checkout-form]');
  if (!form) {
    return;
  }

  const planSelect = form.querySelector('[name="plan"]');
  const summaryName = document.querySelector('[data-plan-name]');
  const summaryPrice = document.querySelector('[data-plan-price]');
  const statusBox = document.querySelector('[data-checkout-status]');
  const submitButton = form.querySelector('[type="submit"]');

  const planCatalog = {
    essentials: {
      amount: 4990,
      itemName: 'Plano Essencial Tutela',
      itemDescription: 'Contratacao inicial com checkout hospedado pela Cielo.',
      displayPrice: 'R$ 49,90',
    },
    business: {
      amount: 14990,
      itemName: 'Plano Corporativo Tutela',
      itemDescription: 'Contratacao corporativa com checkout hospedado pela Cielo.',
      displayPrice: 'R$ 149,90',
    },
  };

  function digitsOnly(value) {
    return String(value || '').replace(/\D/g, '');
  }

  function inferIdentityType(documentNumber) {
    const digits = digitsOnly(documentNumber);
    if (digits.length === 14) {
      return 'CNPJ';
    }

    return 'CPF';
  }

  function renderPlanSummary() {
    const selectedPlan = planCatalog[planSelect.value] || planCatalog.essentials;
    summaryName.textContent = selectedPlan.itemName;
    summaryPrice.textContent = selectedPlan.displayPrice;
  }

  function renderStatus(state, message) {
    statusBox.dataset.state = state || '';
    statusBox.textContent = message || '';
  }

  function formatDetails(details) {
    if (!details) {
      return 'Nao foi possivel iniciar o checkout agora.';
    }

    if (typeof details === 'string') {
      return details;
    }

    if (details.data && typeof details.data === 'object') {
      if (details.data.error_description) {
        return details.data.error_description;
      }

      if (details.data.message) {
        return details.data.message;
      }
    }

    return JSON.stringify(details);
  }

  planSelect.addEventListener('change', renderPlanSummary);
  renderPlanSummary();

  form.addEventListener('submit', async function (event) {
    event.preventDefault();

    const selectedPlan = planCatalog[planSelect.value] || planCatalog.essentials;
    const formData = new FormData(form);
    const payload = {
      amount: selectedPlan.amount,
      itemName: selectedPlan.itemName,
      itemDescription: selectedPlan.itemDescription,
      customerName: formData.get('customerName'),
      customerEmail: formData.get('customerEmail'),
      customerIdentity: digitsOnly(formData.get('customerIdentity')),
      customerIdentityType: inferIdentityType(formData.get('customerIdentity')),
      customerPhone: digitsOnly(formData.get('customerPhone')),
    };

    submitButton.disabled = true;
    renderStatus('loading', 'Preparando seu checkout seguro na Cielo...');

    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(formatDetails(result.details || result.message));
      }

      if (!result.checkoutUrl) {
        throw new Error('A Cielo nao retornou a URL de checkout.');
      }

      renderStatus('loading', 'Redirecionando para a pagina segura da Cielo...');
      window.location.href = result.checkoutUrl;
    } catch (error) {
      renderStatus('error', error.message || 'Nao foi possivel iniciar o checkout.');
      submitButton.disabled = false;
    }
  });
})();
