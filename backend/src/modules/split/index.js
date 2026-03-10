const paymentSplitService = require('../payments/splitService');

function createSplitContext(input) {
  return {
    scenario: input.scenario || 'marketplace',
    recipients: paymentSplitService.calculate(input),
  };
}

module.exports = { createSplitContext };
