// PayerCompanyDTO.js
export class PayerCompanyDTO {
  constructor({
    matched_candidate = {},
    alternative_options = []
  } = {}) {
    this.matchedCandidate = new MatchedCandidate(matched_candidate);
    this.alternativeOptions = alternative_options.map(option => new MatchedCandidate(option));
  }

  getMatchedCandidate() {
    return this.matchedCandidate;
  }

  setMatchedCandidate(value) {
    this.matchedCandidate = new MatchedCandidate(value);
  }

  getAlternativeOptions() {
    return this.alternativeOptions;
  }

  setAlternativeOptions(value) {
    this.alternativeOptions = value.map(option => new MatchedCandidate(option));
  }
}

// MatchedCandidate.js
export class MatchedCandidate {
  constructor({
    matched_phrase = '',
    matched_master_data = {},
    similarity = 0,
    match_type = ''
  } = {}) {
    this.matchedPhrase = matched_phrase;
    this.matchedMasterData = new MatchedMasterData(matched_master_data);
    this.similarity = similarity;
    this.matchType = match_type;
  }

  getMatchedPhrase() {
    return this.matchedPhrase;
  }

  setMatchedPhrase(value) {
    this.matchedPhrase = value;
  }

  getMatchedMasterData() {
    return this.matchedMasterData;
  }

  setMatchedMasterData(value) {
    this.matchedMasterData = new MatchedMasterData(value);
  }

  getSimilarity() {
    return this.similarity;
  }

  setSimilarity(value) {
    this.similarity = value;
  }

  getMatchType() {
    return this.matchType;
  }

  setMatchType(value) {
    this.matchType = value;
  }
}

// MatchedMasterData.js
export class MatchedMasterData {
  constructor({
    code = '',
    short_name = '',
    name = '',
    currency = ''
  } = {}) {
    this.code = code;
    this.shortName = short_name;
    this.name = name;
    this.currency = currency;
  }

  getCode() {
    return this.code;
  }

  setCode(value) {
    this.code = value;
  }

  getShortName() {
    return this.shortName;
  }

  setShortName(value) {
    this.shortName = value;
  }

  getName() {
    return this.name;
  }

  setName(value) {
    this.name = value;
  }

  getCurrency() {
    return this.currency;
  }

  setCurrency(value) {
    this.currency = value;
  }
}
