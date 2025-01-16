- (248, DANIEL, DANIEL ADVOGADOS, USD)

  1. **패턴**:
     - 키워드: `"Beneficiary Name:"`
     - 데이터: 키워드 다음 라인의 텍스트.
  2. **INVOICE DATE (송장 날짜)**:

     **패턴**:

     - 키워드: `"INVOICE Nº:"`
     - 데이터: 키워드 아래에 위치한 날짜 형식 (월, 일, 연도).

  3. **INVOICE № (송장 번호)**:

     **패턴**:

     - 키워드: `"INVOICE Nº:"`
     - 데이터: 키워드 뒤에 나타나는 알파벳과 숫자의 조합.

  4. **AMOUNT BILLED (청구 금액)**:

     **패턴**:

     - 키워드: `"TOTAL AMOUNT DUE:"`
     - 데이터: 키워드 뒤에 나타나는 금액 형식.

  5. **仮案件 № (안건 번호)**:

     **패턴**:

     - 키워드: `"Your Ref:"`
     - 데이터: 키워드 뒤에 나타나는 형식화된 번호 (알파벳+숫자 조합).

- Oliff PLC (10, OLIFF, OLIFF PLC, USD)
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 날짜 형식: `MMM DD, YYYY` (예: "November 27, 2024").
    - PDF 헤더 근처에 위치.
  - **AMOUNT BILLED (청구 금액)**:
    청구 금액은 "TOTAL" 키워드와 **같은 줄에** 있으므로, 패턴 정의 시 이를 명확히 반영하겠습니다.
    - 키워드: `"TOTAL"`
    - 데이터: 키워드와 같은 줄의 금액 형식(예: `$305.00`).
  - **INVOICE № (송장 번호)**:
    송장 번호는 "Debit Note Number" **키워드 바로 아래 줄에** 있으므로, 이 위치를 반영하겠습니다.
    - 키워드: `"Debit Note Number"`
    - 데이터: 키워드 아래 줄에 위치한 숫자.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your Ref."`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합 (예: "TFN220448-US").
- Dinsmore and Shohl LLP (410, Dinsmore, Dinsmore & Shohl LLP, USD)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: `"By Check"` 또는 `"By Wire/ACH"`
    - 데이터: 키워드 아래 라인의 텍스트.
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 날짜 형식: `MMM DD, YYYY` (예: "November 27, 2024").
    - PDF 상단에서 "Invoice #" 근처 위치.
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"Invoice #"`
    - 데이터: 키워드 바로 뒤의 텍스트.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"Total Due for Professional Services"`
    - 데이터: 키워드와 **같은 줄**의 금액 형식(예: `$250.00`).
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your Ref:"`
    - 데이터: 키워드 바로 뒤의 텍스트.
- Winter Brandl – Partnerschaft mbB (184, WINTER, Winter, Brandl & Partner, EUR)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드 없음, 상단에 고정된 위치에 표시된 법인의 이름.
    - 데이터: "WINTER, BRANDL - PARTNERSCHAFT MBB".
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"INVOICE DATE"`
    - 데이터: 키워드 바로 뒤의 날짜 형식.
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"INVOICE NUMBER"`
    - 데이터: 키워드 바로 뒤의 텍스트.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"INVOICE TOTAL"`
    - 데이터: 키워드 뒤에 위치한 금액 형식과 통화 정보.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your Ref"`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- KINGSOUND & PARTNERS (352, 金信(KINGSOUND), KINGSOUND & PARTNERS Intellectual Property Law, USD)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: `"KINGSOUND AND PARTNERS"`
    - 데이터: 문서 상단 또는 은행 정보 섹션에서 반복적으로 나타나는 이름.
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"Date:"`
    - 데이터: 키워드 뒤의 날짜 형식 (예: "December 11, 2024").
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"D/N No:"`
    - 데이터: 키워드 뒤의 텍스트 (알파벳+숫자 조합).
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"TOTAL USD"`
    - 데이터: 키워드 아래 금액 형식과 통화 정보 (예: "249.00 USD").
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Y/ Ref:"`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- SoraIP, Inc. (446, SoraIP, SoraIP, USD)

  ### **데이터 패턴 분석**

  1. **支払先 (지불처)**

     **패턴**:

     - 위치: 문서 상단 고정 위치.
     - 데이터: "SoraIP, Inc." (정확한 이름이 반복적으로 나타나지 않으므로 문서 상단에서 추출).

  2. **INVOICE DATE (송장 날짜)**

     **패턴**:

     - 키워드: 날짜 형식 (`MMM DD, YYYY`).
     - 위치: "D/N No." 키워드 위에 있는 날짜.

  3. **INVOICE № (송장 번호)**

     **패턴**:

     - 키워드: `"D/N No."`
     - 데이터: 키워드 바로 뒤의 텍스트.

  4. **AMOUNT BILLED (청구 금액)**

     **패턴**:

     - 키워드: `"TOTAL AMOUNT"`
     - 데이터: 키워드와 동일한 줄에서 금액 형식과 통화 정보.

  5. **仮案件 № (안건 번호)**

     **패턴**:

     - 키워드: `"Docket No."`
     - 데이터: 키워드 뒤의 알파벳+숫자 조합.

- 青和特許法律事務所 (436, 青和特許法律事務所, 青和特許法律事務所, YEN)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드 없음, 문서 상단 고정 위치.
    - 데이터: "青和特許法律事務所".
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"請求No."`
    - 데이터: 키워드 아래 날짜 형식 (`YYYY年MM月DD日`).
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"請求No."`
    - 데이터: 키워드 뒤의 텍스트.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"合計金額"`
    - 데이터: 키워드와 동일한 줄에 있는 금액 형식 (예: `229,550 円`).
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"貴社整理番号"`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- TBK, Bavariaring 4-6, 80336 München Patentanwälte (73, TBK, TBK, EUR)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드 없음, 문서 상단에 고정된 위치.
    - 데이터: "TBK, Bavariaring 4-6, 80336 München".
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"Date of the Service"` 또는 `"INVOICE:"`.
    - 데이터: 키워드 근처의 날짜 형식 (`MMM DD, YYYY`).
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"INVOICE:"`
    - 데이터: 키워드 뒤의 텍스트.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"Total (gross)"` 또는 `"Total Amount"`.
    - 데이터: 키워드와 동일한 줄에 위치한 금액 형식 (`\d{1,3}(,\d{3})*\.\d{2}\s*€`).
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your ref."`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- HENRY GOH & CO SDN BHD (401, Henry Goh, Henry Goh & Co. Sdn. Bhd., USD)

  1. **支払先 (지불처)**

     **패턴**:

     - 키워드 없음, 문서 상단 고정 위치에서 회사 이름.
     - 데이터: "HENRY GOH & CO SDN BHD".

  2. **INVOICE DATE (송장 날짜)**

     **패턴**:

     - 키워드: `"Date"`
     - 데이터: 키워드 바로 뒤의 날짜 형식 (`DD/MM/YYYY`).

  3. **INVOICE № (송장 번호)**

     **패턴**:

     - 키워드: `"No"`
     - 데이터: 키워드 뒤의 숫자.

  4. **AMOUNT BILLED (청구 금액)**

     **패턴**:

     - 키워드: `"Total (Inclusive of Tax)"`
     - 데이터: 키워드와 동일한 줄에 위치한 금액과 통화 정보.

  5. **仮案件 № (안건 번호)**

     **패턴**:

     - 키워드: `"Your Ref"`
     - 데이터: 키워드 뒤의 알파벳+숫자 조합.

- Beyond Attorneys at Law (432, BEYOND ATTORNEYS AT LAW, BEYOND ATTORNEYS AT LAW, USD)
  - **패턴**:
    - 키워드: `"Beneficiary Account Name:"`
    - 데이터: 키워드 뒤의 회사 이름.
    - 예: `"Beyond International IP Agency Co., Limited"`
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"Dated:"`
    - 데이터: 키워드 뒤의 날짜 형식 (`MMM DD, YYYY`).
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"No.:"`
    - 데이터: 키워드 뒤의 텍스트.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"TOTAL"`
    - 데이터: USD 뒤에 오는 **숫자 형식의 금액**
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your Ref:"`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- Unitalen Attorneys At Law Co LTD (330, UNITALEN, UNITALEN ATTORNEYS AT LAW, USD)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: 없음, 문서 상단 고정 위치 또는 계좌 정보에서 탐색.
    - 데이터: "Unitalen Attorneys At Law Co LTD".
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"DATE:"`
    - 데이터: 키워드 뒤의 날짜 형식 (`MMM DD, YYYY`).
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"NO."`
    - 데이터: 키워드 뒤의 텍스트.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"Equivalent to: US$"`
    - 데이터: 키워드 뒤의 금액 형식 (`\d{1,3}(,\d{3})*\.\d{2}`).
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your Ref."`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- 잘못 매칭됨 : (잘못 매칭된 회사 데이터 : EUR (255, AGENCY TRIA ROBIT(EUR), AGENCY TRIA ROBIT(EUR), EUR))
  - **支払先 (지불처) : 회사 정보가 이미지로 되어 있는 듯함**
    **데이터**: **문서 내 지불처 정보 없음**
    **이유**: 주어진 문서에 지불처 관련 정보가 명시되지 않았습니다. 만약 **파일명**이나 추가 데이터에서 확인 가능하다면 지불처를 보완할 수 있습니다.
  - **INVOICE DATE (송장 날짜)**
    **데이터**: **"December 4, 2024"**
    **이유**: "Date:" 키워드 뒤에 위치하며, 송장이 발행된 날짜를 나타냅니다.
  - **INVOICE № (송장 번호)**
    **데이터**: **"F00014897"**
    **이유**: "Invoice No." 키워드 뒤에 위치하며, 송장 번호 형식을 따릅니다.
  - **AMOUNT BILLED (청구 금액)**
    **데이터**: **"5,944.00 EUR"**
    **이유**: "TOTAL" 섹션에서 금액과 통화 정보가 명시되어 있습니다. VAT 및 기타 비용이 포함된 최종 금액입니다.
  - **仮案件 № (안건 번호)**
    **데이터**: **"TFN231259-EP"**
    **이유**: "Y/Ref." 키워드 뒤에 위치하며, 안건 번호 형식을 따릅니다.
- SAIDMAN DESIGNLAW GROUP, LLC (84, SAIDMAN, SAIDMAN Design Law Group, USD)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: 없음, 문서 상단 고정 위치.
    - 데이터: "SAIDMAN DESIGNLAW GROUP, LLC".
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"Debit Note No:"` 바로 아래 줄의 날짜.
    - 데이터: 날짜 형식 (`MMM DD, YYYY`).
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"Debit Note No:"`
    - 데이터: 키워드 뒤의 텍스트.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"This Invoice Total"`
    - 데이터: 키워드와 동일한 줄의 금액과 통화 정보.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your refs."`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- FINNEGAN, HENDERSON, FARABOW, GARRETT & DUNNER, L.L.P. (61, FINNEGAN, FINNEGAN, HENDERSON, FARABOW, GARRETT & DUNNER, L.L.P., USD)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: 없음, 문서 상단 고정 위치 또는 송금 정보에서 탐색.
    - 데이터: "FINNEGAN, HENDERSON, FARABOW, GARRETT & DUNNER, LLP".
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"Invoice Date:"`
    - 데이터: 키워드 뒤의 날짜 형식 (`MM/DD/YY`).
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"Invoice Number:"`
    - 데이터: 키워드 뒤의 텍스트.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"AMOUNT DUE THIS INVOICE"`
    - 데이터: 키워드와 동일한 줄의 금액과 통화 정보.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Client Ref No."`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- CHINA SINDA (27, 中原(CHINA SINDA), CHINA SINDA INTELLECTUAL PROPERTY LIMITED, USD)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: `"Account Name:"`
    - 데이터: 키워드 뒤의 회사 이름.
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - **"DEBIT NOTE"**
    - 키워드 다음 줄에 위치한 날짜 형식(`MMM DD, YYYY`)을 추출
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"No:"`
    - 데이터: 키워드 뒤의 텍스트.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"Grand Total"`
    - 데이터: 키워드와 동일한 줄의 금액과 통화 정보.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your Ref."`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- LAW OFFICES (67, ADVANCE CHINA, ADVANCE CHINA I.P.LAW OFFICE, USD)

  1. **支払先 (지불처)**

     **패턴**:

     - 키워드: 없음, 문서 상단 고정 위치 또는 송금 정보에서 탐색.
     - 데이터: "Hauptman Ham LLP".

  2. **INVOICE DATE (송장 날짜)**

     **패턴**:

     - 키워드: `"INVOICE NO."` 바로 아래 줄의 날짜.
     - 데이터: 날짜 형식 (`MMM DD, YYYY`).

  3. **INVOICE № (송장 번호)**

     **패턴**:

     - 키워드: `"INVOICE NO."`
     - 데이터: 키워드 뒤의 숫자.

  4. **AMOUNT BILLED (청구 금액)**

     **패턴**:

     - 키워드: `"Total Current Charges"`
     - 데이터: 키워드와 동일한 줄의 금액과 통화 정보.

  5. **仮案件 № (안건 번호)**

     **패턴**:

     - 키워드: `"Your Reference"`
     - 데이터: 키워드 뒤의 알파벳+숫자 조합.

- ANAND AND ANAND (38, ANAND, ANAND AND ANAND, USD)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: 없음, 문서 상단 고정 위치 또는 송금 정보에서 탐색.
    - 데이터: "Anand and Anand".
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"Invoice Date"`
    - 데이터: 키워드 뒤의 날짜 형식 (`DD-MMM-YYYY`).
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"Invoice Number"`
    - 데이터: 키워드 뒤의 텍스트.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"Total Invoice Value"`
    - 데이터: 키워드와 동일한 줄의 금액과 통화 정보.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your Ref"`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합
- KIM & CHANG (49, 金&張(KIM&CHANG), KIM&CHANG, USD)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: `"Name of Account :"`
    - 데이터: 키워드 뒤의 회사 이름.
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"INVOICE"` 바로 아래 날짜 형식 (`MMM DD, YYYY`).
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"No:"`
    - 데이터: 키워드 뒤의 텍스트.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"総金額"`
    - 데이터: 키워드와 동일한 줄의 금액과 통화 정보.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your Ref."`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- (180, Tilleke, Tilleke & Gibbins International Ltd., USD)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: `"Account Name:"`
    - 데이터: 키워드 뒤의 회사 이름.
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"Date:"`
    - 데이터: 키워드 뒤의 날짜 형식 (`DD MMM YYYY`).
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"Invoice:"`
    - 데이터: 키워드 뒤의 텍스트.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"Total Amount Due"`
    - 데이터: 키워드와 동일한 줄의 금액과 통화 정보.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your Ref:"`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합
- (325, Sughrue, Sughrue Mion, PLLC, USD)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: `"Account Name:"`
    - 데이터: 키워드 뒤의 회사 이름.
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"DATE:"`
    - 데이터: 키워드 뒤의 날짜 형식 (`MMM DD, YYYY`).
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"INVOICE NO:"`
    - 데이터: 키워드 뒤의 숫자.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"Total for Services and Disbursements"`
    - 데이터: 키워드와 동일한 줄의 금액과 통화 정보.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"YOUR REF:"`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- (164, CPA, CPA Global Limited, GBP)

  1. **支払先 (지불처)**

     **패턴**:

     - 키워드: `"Mail To:"` 또는 `"Wire Instructions:"`
     - 데이터: 키워드 뒤의 회사 이름.

  2. **INVOICE DATE (송장 날짜)**

     **패턴**:

     - 키워드: `"INVOICE DATE:"`
     - 데이터: 키워드 뒤의 날짜 형식 (`MMM DD, YYYY`).

  3. **INVOICE № (송장 번호)**

     **패턴**:

     - 키워드: `"INVOICE NO.:"`
     - 데이터: 키워드 뒤의 숫자.

  4. **AMOUNT BILLED (청구 금액)**

     **패턴**:

     - 키워드: `"TOTAL CURRENT INVOICE"`
     - 데이터: 키워드와 동일한 줄의 금액과 통화 정보.

  5. **仮案件 № (안건 번호)**

     **패턴**:

     - 키워드: `"TTDC REF."`
     - 데이터: 키워드 뒤의 알파벳+숫자 조합.

- (260, D YOUNG, D YOUNG & CO LLP, GBP)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: `"ACCOUNT ENQUIRIES TO:"`
    - 데이터: 키워드 뒤의 회사 이름.
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"Tax Point:"`
    - 데이터: 키워드 뒤의 날짜 형식 (`DD MMM YYYY`).
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"Invoice No"`
    - 데이터: 키워드 뒤의 숫자.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"Total"`
    - 데이터: 키워드와 동일한 줄의 금액과 통화 정보. ( 가장 마지막에 위치한 금액만 추출)
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your Ref:"`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- (401, Henry Goh, Henry Goh & Co. Sdn. Bhd., USD)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: `"Account Name:"`
    - 데이터: 키워드 뒤의 회사 이름.
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"Date:"`
    - 데이터: 키워드 뒤의 날짜 형식 (`DD/MM/YYYY`).
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"No:"`
    - 데이터: 키워드 뒤의 숫자.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"Total (Inclusive of Tax)"`
    - 데이터: 키워드와 동일한 줄의 금액과 통화 정보.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your Ref:"`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- (76, ABU-GHAZALEH LEGAL SERVICES, ABU-GHAZALEH LEGAL SERVICES LIMITED, USD)
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: `"The name of the account holder"`
    - 데이터: 해당 키워드 뒤에 명시된 값.
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"INVOICE NO."`
    - 데이터: 키워드 같은 줄에서 날짜 형식을 탐색.
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"INVOICE NO."`
    - 데이터: 키워드 뒤에 나오는 문자열.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"Rounded TOTAL(USD)"`
    - 데이터: 키워드와 같은 줄의 금액.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your Ref:"`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- Client Details (55, NTD, NTD PATENT & TRADE MARK AGENCY LIMITED, USD)
- 96Clarke MexicoClarke, Modet & Co., MexicoUSD
  - **支払先 (지불처)**
    **데이터**: **"ClarkeModet y Compañía de México S.A."**
    **이유**: 송금 계좌 정보 섹션의 **"Beneficiary"** 필드에 명시되어 있습니다.
  - **INVOICE DATE (송장 날짜)**
    **데이터**: **"18/12/2024"**
    **이유**: **"Invoice Date"** 키워드와 같은 줄에 표시된 날짜입니다.
  - **INVOICE № (송장 번호)**
    **데이터**: **"ME101546"**
    **이유**: **"Invoice Number"** 키워드 바로 뒤에 위치하며, 송장 번호 형식을 따릅니다.
  - **AMOUNT BILLED (청구 금액)**
    **데이터**: **"372.00 USD"**
    **이유**: **"Total"** 키워드와 같은 줄에 표시된 최종 금액입니다.
  - **仮案件 № (안건 번호)**
    **데이터**: **"MA2022-0180-HN-12"**
    **이유**: **"S.Ref/Your Ref:"** 키워드 뒤에 위치하며, 안건 번호 형식을 따릅니다.
- Gorodissky
  - **支払先 (지불처)**
    **패턴**:
    - 키워드: 문서 상단의 회사명.
    - 데이터: 해당 섹션의 첫 번째 회사 이름.
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - 키워드: `"Invoice No"`
    - 데이터: 키워드 아래에 날짜 형식으로 표시된 값.
  - **INVOICE № (송장 번호)**
    **패턴**:
    - 키워드: `"Invoice No"`
    - 데이터: 키워드 바로 뒤의 숫자.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - 키워드: `"Due for payment USD"`
    - 데이터: 키워드 뒤의 금액.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - 키워드: `"Your Ref"`
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- 289 SD PETOSEVICSD PETOSEVICEUR
  - **支払先 (지불처)**
    **패턴**:
    - **키워드**: 문서 상단의 첫 번째 회사 이름.
    - **데이터**: 해당 섹션의 첫 번째 텍스트.
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - **키워드**: `"Invoice No."`
    - **데이터**: 키워드 섹션 바로 아래에 위치한 날짜.
  - **INVOICE № (송장 번호)**
    **패턴**:
    - **키워드**: `"Invoice No."`
    - **데이터**: 키워드 바로 뒤의 알파벳+숫자 조합.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - **키워드**: `"TOTAL Amount in EUR"`
    - **데이터**: 키워드 뒤의 금액.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - **키워드**: `"Your Ref."`
    - **데이터**: 키워드 뒤의 알파벳+숫자 조합.
- 258J.A.KEMPJ.A.KEMP & Co.GBP
  - **支払先 (지불처)**
    **패턴**:
    - **키워드**: 문서 하단에 회사 정보가 포함된 섹션에서 "J A Kemp LLP".
    - **데이터**: 등록된 회사 이름.
  - **INVOICE DATE (송장 날짜)**
    **패턴**:
    - **키워드**: `"Date:"`
    - **데이터**: 키워드 뒤의 날짜 형식 텍스트.
  - **INVOICE № (송장 번호)**
    **패턴**:
    - **키워드**: `"Invoice No:"`
    - **데이터**: 키워드 뒤의 숫자.
  - **AMOUNT BILLED (청구 금액)**
    **패턴**:
    - **키워드**: `"Total Due"`
    - **데이터**: 키워드 뒤의 금액과 통화 정보.
  - **仮案件 № (안건 번호)**
    **패턴**:
    - **키워드**: `"Your Ref:"`
    - **데이터**: 키워드 뒤의 알파벳+숫자 조합.
- (465, JUPITER LAW PARTNERS, JUPITER LAW PARTNERS, USD)
  - **支払先 (지불처)**
    **데이터:** **"JUPITER LAW PARTNERS"**
    **이유:** 문서 상단에 법무사 이름이 명확히 나와 있으며, 연락처와 이메일이 함께 제공됨.
  - **키워드:** **INVOICE DATE (송장 날짜)**
    **데이터:** **"29 Nov 2024"**
    **이유:** **"Date:"** 키워드 뒤에 위치한 날짜로, 송장 발행일임.
  - **INVOICE № (송장 번호)**
    **데이터:** **"20759/24-25/ST"**
    **이유:** **"Invoice No."** 키워드 뒤에 명시된 고유 번호임.
  - **키워드:** **AMOUNT BILLED (청구 금액)**
    **데이터:** **"90.00 USD"**
    **이유:** **"Grand Total"** 섹션에 해당 금액이 명시되어 있으며, 통화(USD) 정보가 함께 제공됨.
  - **키워드:** **仮案件 № (안건 번호)**
    **데이터:** **"TFN221008-IN"**
    **이유:** **"Ref."** 키워드 뒤에 있는 값으로, 송장과 관련된 프로젝트 번호임.
- (185, KUHNEN, Kuhnen & Wacker Patent and Law Firm P. C., EUR)
  ### **支払先 (지불처)**
  - **패턴:**키워드: 문서 상단 또는 하단의 회사 이름이 포함된 정보 섹션.데이터: "KUHNEN & WACKER Patent- und Rechtsanwaltsbüro" (문서 하단에 기재된 회사명).
  ### **INVOICE DATE (송장 날짜)**
  - **패턴:**키워드: **"Date:"** 또는 **"Invoice Date:"**데이터: **"December 4, 2024"** (문서 상단에서 "Date" 키워드 뒤의 날짜).
  ### **INVOICE № (송장 번호)**
  - **패턴:**키워드: **"DEBIT NOTE No.:"**데이터: **"24-09542"** (키워드 뒤에 기재된 번호).
  ### **AMOUNT BILLED (청구 금액)**
  - **패턴:**키워드: **"Total"**데이터: **"1,428.50 EUR"** (키워드 뒤에 있는 금액과 통화 정보).
  ### **仮案件 № (안건 번호)**
  - **패턴:**키워드: **"Your Reference :"**데이터: **"TFN231627-DE"** (키워드 뒤의 알파벳+숫자 조합).
- (43, BIRO OKTROI, BIRO OKTROI ROOSSENO, USD)
  ### **支払先 (지불처)**
  - **패턴:**키워드: 문서 상단 또는 하단의 회사 이름이 포함된 정보 섹션.데이터: **"PT. BIRO OKTROI ROOSSENO"** (문서 상단에 기재된 회사명).
  ***
  ### **INVOICE DATE (송장 날짜)**
  - **패턴:**키워드: **"Jakarta,"**데이터: **"05 Dec 2024"** (키워드 뒤의 날짜).
  - 흔한 패턴이 아님 다른 방법 고려할 필요 있음
  ***
  ### **INVOICE № (송장 번호)**
  - **패턴:**키워드: **"Invoice No."**데이터: **"PTDN1454/2024"** (키워드 뒤의 번호).
  ***
  ### **AMOUNT BILLED (청구 금액)**
  - **패턴:**키워드: **"Invoice Amount"**데이터: **"1,347.55 USD"** (키워드 뒤의 금액과 통화 정보).
  ***
  ### **仮案件 № (안건 번호)**
  - **패턴:**키워드: **"Your Ref. :"**데이터: **"TFN200244-ID"** (키워드 뒤의 알파벳+숫자 조합).
- (80, Abu_Ghazaleh, Abu-Ghazaleh Intellectual Property, USD)
  **支払先 (지불처)**
  - **패턴**:
    - 키워드: "Beneficiary Name"
    - 데이터: 키워드 뒤의 회사 이름.
  - **결과**:
    - Beneficiary Name: **Abu-Ghazaleh Intellectual Property (AGIP)**
  ***
  **INVOICE DATE (송장 날짜)**
  - **패턴**:
    - 키워드: "Invoice Date :"
    - 데이터: 키워드 뒤의 날짜 형식 텍스트.
  - **결과**:
    - Invoice Date: **17-Dec-2024**
  ***
  **INVOICE № (송장 번호)**
  - **패턴**:
    - 키워드: “Invoice Date"
    - 데이터: 키워드 뒤의 번호.
  ***
  **AMOUNT BILLED (청구 금액)**
  - **패턴**:
    - 키워드: "Grand Total"
    - 데이터: 키워드 뒤의 금액과 통화 정보.
  - **결과**:
    - Grand Total: **385.00 USD**
  ***
  **仮案件 № (안건 번호)**
  - **패턴**:
    - 키워드: "Your Reference"
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
  - **결과**:
    - Your Reference: **MA2022-0180-IQ-12**
- (365, Ashurst, Ashurst, USD)
  ### **支払先 (지불처)**
  - **패턴**:
    - 키워드: **"Account Name:"**
    - 데이터: 키워드 뒤의 회사 이름.
  - **결과**:
    - **Ashurst Australia USD**
  ***
  ### **INVOICE DATE (송장 날짜)**
  - **패턴**:
    - 키워드: **"Tax Invoice Date:"**
    - 데이터: 키워드 뒤의 날짜 형식 텍스트.
  - **결과**:
    - **20 December 2024**
  ***
  ### **INVOICE № (송장 번호)**
  - **패턴**:
    - 키워드: **"Tax Invoice No.:"**
    - 데이터: 키워드 뒤의 숫자 및 문자 조합.
  - **결과**:
    - **290020265**
  ***
  ### **AMOUNT BILLED (청구 금액)**
  - **패턴**:
    - 키워드: **"Balance Due"**
    - 데이터: 키워드 뒤의 금액과 통화 정보.
  - **결과**:
    - **640.29 USD**
  ***
  ### **仮案件 № (안건 번호)**
  - **패턴**:
    - 키워드: **"Your ref:"**
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
  - **결과**:
    - **MA2023-0188-PG-12**
- (81, CAREY, Carey y Cía. Ltda., USD)
  ### **支払先 (지불처)**
  - **패턴**:
    - 키워드: **"Account Name :"**
    - 데이터: 키워드 뒤에 위치한 회사 이름.
  - **결과**:
    - **Estudio Carey Ltda.**
  ***
  ### **INVOICE DATE (송장 날짜)**
  - **패턴**:
    - 키워드: **"Date :"**
    - 데이터: 키워드 뒤에 위치한 날짜 형식 텍스트.
  - **결과**:
    - **11/08/2024**
  ***
  ### **INVOICE № (송장 번호)**
  - **패턴**:
    - 키워드: **"Invoice :"**
    - 데이터: 키워드 뒤의 숫자.
  - **결과**:
    - **719641**
  ***
  ### **AMOUNT BILLED (청구 금액)**
  - **패턴**:
    - 키워드: **"TOTAL US$"**
    - 데이터: 키워드 뒤에 위치한 금액과 통화 정보.
  - **결과**:
    - **520.07 USD**
  ***
  ### **仮案件 № (안건 번호)**
  - **패턴**:
    - 키워드: **"Your ref.:"**
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
  - **결과**:
    - **MA2024-0181-CL-12**
- (131, S. Horowitz & Co., S. Horowitz & Co., USD)
  ### **支払先 (지불처)**
  - **패턴**:
    - 키워드: **"S. Horowitz & Co."**
    - 데이터: 키워드가 위치한 섹션의 회사 이름.
  ***
  ### **INVOICE DATE (송장 날짜)**
  - **패턴**:
    - 키워드: **"Date :"**
    - 데이터: 키워드 뒤의 날짜 형식 텍스트.
  ***
  ### **INVOICE № (송장 번호)**
  - **패턴**:
    - 키워드: **"Invoice No."**
    - 데이터: 키워드 뒤의 숫자.
  ***
  ### **AMOUNT BILLED (청구 금액)**
  - **패턴**:
    - 키워드: **"Total"**
    - 데이터: 키워드 뒤에 위치한 마지막 금액과 통화 정보.
  ***
  ### **仮案件 № (안건 번호)**
  - **패턴**:
    - 키워드: **"Your Ref :"**
    - 데이터: 키워드 뒤의 알파벳+숫자 조합.
- (204, SPRUSON, Spruson & Ferguson Pty Limited., USD)
  **支払先 (지불처)**
  - **패턴:** "INVOICE FROM:" 키워드 뒤에서 회사 정보가 있는 섹션.
    **INVOICE DATE (송장 날짜)**
  - **패턴:** "Date:" 키워드 뒤.
    **INVOICE № (송장 번호)**
  - **패턴:** "Invoice No:" 키워드 뒤.
    **AMOUNT BILLED (청구 금액)**
  - **패턴:** "TOTAL (US$)" 키워드 뒤에서 위치한 금액.
    **仮案件 № (안건 번호)**
  - **패턴:** "Your Ref:" 키워드 뒤에서 알파벳과 숫자의 조합.
- (46, SAPALO, SAPALO VELEZ BUNDANG & BULILAN LAW OFFICES, USD)
  **支払先 (지불처)**
  - **패턴:** "INVOICE FROM:" 키워드 뒤에서 회사 정보가 있는 섹션.
    **INVOICE DATE (송장 날짜)**
  - **패턴:** "Date:" 키워드 근처에 있는 다음줄.
    **INVOICE № (송장 번호)**
  - **패턴:** "Invoice No:" 키워드 근처 에 있는 다음줄.
    **AMOUNT BILLED (청구 금액)**
  - **패턴:** "TOTAL (US$)" 키워드 뒤에서 위치한 금액.
    **仮案件 № (안건 번호)**
  - **패턴:** "Your Ref:" 키워드 뒤에서 알파벳과 숫자의 조합.
