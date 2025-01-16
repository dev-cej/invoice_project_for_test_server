// AmountBilledDTO.js
export class AmountBilledDTO {
  constructor({
    selected_candidate = [],
    alternative_options = []
  } = {}) {
    this.selectedCandidate = selected_candidate.map(item => new AmountDetail(item));
    this.alternativeOptions = alternative_options.map(option => new AmountDetail(option));
  }

  getSelectedCandidate() {
    return this.selectedCandidate;
  }

  setSelectedCandidate(value) {
    this.selectedCandidate = value.map(item => new AmountDetail(item));
  }

  getAlternativeOptions() {
    return this.alternativeOptions;
  }

  setAlternativeOptions(value) {
    this.alternativeOptions = value.map(option => new AmountDetail(option));
  }
}

// AmountDetail.js
export class AmountDetail {
  constructor({
    amount = '',
    currency = ''
  } = {}) {
    this.amount = amount;
    this.currency = currency;
  }

  getAmount() {
    return this.amount;
  }

  setAmount(value) {
    this.amount = value;
  }

  getCurrency() {
    return this.currency;
  }

  setCurrency(value) {
    this.currency = value;
  }
}