// InvoiceNumberDTO.js
export class InvoiceNumberDTO {
  constructor({
    selected_candidate = '',
    alternative_options = []
  } = {}) {
    this.selectedCandidate = selected_candidate;
    this.alternativeOptions = alternative_options;
  }

  getSelectedCandidate() {
    return this.selectedCandidate;
  }

  setSelectedCandidate(value) {
    this.selectedCandidate = value;
  }

  getAlternativeOptions() {
    return this.alternativeOptions;
  }

  setAlternativeOptions(value) {
    this.alternativeOptions = value;
  }
}