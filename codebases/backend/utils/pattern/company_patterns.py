COMPANY_PATTERNS = {
    "10101": {  # L O U I S · P Ö H L A U · L O H R E N T Z
        "name": "L O U I S · P Ö H L A U · L O H R E N T Z",
        "invoice_number": {
            "keywords": ["Invoice No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Invoice No"],
            "line_offset": 1,
            "extract_type": "line"
        },
        "amount": {
            "keywords": ["Total Sum", "USD"],
            "line_offset": 1,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
    "10201": {  # WTA Patents
        "name": "WTA Patents",
        "invoice_number": {
            "keywords": ["Invoice"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Invoice"],
            "line_offset": 1,
            "extract_type": "line"
        },
        "amount": {
            "keywords": ["Please Pay This Amount"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
    "248": {  # DANIEL
        "name": "DANIEL",
        "invoice_number": {
            "keywords": ["INVOICE Nº"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["INVOICE Nº"],
            "line_offset": 1,  # 키워드 다음 줄
            "extract_type": "line"
        },
        "amount": {
            "keywords": ["TOTAL AMOUNT DUE"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
    "10": {  # OLIFF
        "name": "OLIFF",
        "invoice_number": {
            "keywords": ["Debit Note Number"],
            "line_offset": 1,
            "extract_type": "line"
        },
        "date": {
            "keywords": ["Date"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["TOTAL"],
            "line_offset": 0,
            "extract_type": "line"  # 같은 줄 어딘가에 금액이 있음
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
    # Dinsmore and Shohl LLP (410)
    "410": {
        "name": "Dinsmore",
        "invoice_number": {
            "keywords": ["Invoice #"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Date"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "amount": {
            "keywords": ["Total Due for Professional Services"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
    
    },

# Winter Brandl (184)
    "184": {
        "name": "WINTER",
        "invoice_number": {
            "keywords": ["INVOICE NUMBER"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["INVOICE DATE"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["INVOICE TOTAL"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },

# KINGSOUND & PARTNERS (352)
    "352": {
        "name": "金信(KINGSOUND)",
        "invoice_number": {
            "keywords": ["D/N No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Date"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["TOTAL USD"],
            "line_offset": 1,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Y/ Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
    "446": {  # SoraIP
        "name": "SoraIP",
        "invoice_number": {
            "keywords": ["D/N No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["D/N No"],
            "line_offset": -1,
            "extract_type": "line"
        },
        "amount": {
            "keywords": ["TOTAL AMOUNT"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Docket No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
    "436": {  # 青和特許法律事務所
        "name": "青和特許法律事務所",
        "invoice_number": {
            "keywords": ["請求No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["請求No"],
            "line_offset": 1,
            "extract_type": "line"
        },
        "amount": {
            "keywords": ["合計金額"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["貴社整理番号"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
    "73": {  # TBK
        "name": "TBK",
        "invoice_number": {
            "keywords": ["INVOICE"],  # 코드에서 "INVOICE:", "Invoice:" 등 처리
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Date of the Service", "INVOICE"],  # "Date of Service:" 등 처리
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["Total gross", "Total Amount"],  # "Total (gross):", "Total Amount:" 등 처리
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your ref"],  # "Your ref.", "Your Ref:", "Your reference" 등 처리
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
        "401": {  # HENRY GOH
        "name": "Henry Goh",
        "invoice_number": {
            "keywords": ["No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Date"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["Total (Inclusive of Tax)"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
        "432": {  # Beyond Attorneys at Law
        "name": "BEYOND ATTORNEYS AT LAW",
        "invoice_number": {
            "keywords": ["No"],  # "No.:", "No:" 등 처리
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Dated"],  # "Dated:", "Date:" 등 처리
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["TOTAL"],  # USD 뒤에 오는 숫자 형식의 금액
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your Ref"],  # "Your Ref:", "Your Ref." 등 처리
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },

     "330": {  # Unitalen
        "name": "UNITALEN",
        "invoice_number": {
            "keywords": ["DATE"],  # "NO.", "No." 등 처리
            "line_offset": -4,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["DATE"],  # "DATE:", "Date:" 등 처리
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["Equivalent to"],  # 금액 형식 (\d{1,3}(,\d{3})*\.\d{2})
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "case_number": {
            "keywords": ["Your Ref"],  # "Your Ref.", "Your reference" 등 처리
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
        "84": {  # SAIDMAN DESIGNLAW GROUP
        "name": "SAIDMAN",
        "invoice_number": {
            "keywords": ["Debit Note No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Debit Note No"],  # 키워드 바로 아래 줄의 날짜
            "line_offset": 1,
            "extract_type": "line"
        },
        "amount": {
            "keywords": ["This Invoice Total"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your refs"],  # "Your refs.", "Your reference" 등 처리
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
        "61": {  # FINNEGAN
        "name": "FINNEGAN, HENDERSON, FARABOW, GARRETT & DUNNER, L.L.P.",
        "invoice_number": {
            "keywords": ["Invoice Number"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Invoice Date"],
            "line_offset": 0,
            "extract_type": "after_keyword",
            "date_format": "MM/DD/YY"  # 특정 날짜 형식 지정
        },
        "amount": {
            "keywords": ["AMOUNT DUE THIS INVOICE"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Client Ref No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },

        "27": {  # CHINA SINDA
        "name": "中原(CHINA SINDA)",
        "invoice_number": {
            "keywords": ["No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["DEBIT NOTE"],  # 키워드 다음 줄에 위치한 날짜
            "line_offset": 1,
            "extract_type": "line",
            "date_format": "MMM DD, YYYY"
        },
        "amount": {
            "keywords": ["Grand Total"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }},

            "67": {  # LAW OFFICES (ADVANCE CHINA I.P.LAW OFFICE)
        "name": "ADVANCE CHINA I.P.LAW OFFICE",
        "invoice_number": {
            "keywords": ["D/N No",],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["D/N No"],  # 송장 번호 바로 아래 줄에 날짜가 있음
            "line_offset": 1,
            "extract_type": "line",
            "date_format": "MMM DD, YYYY"
        },
        "amount": {
            "keywords": ["Total Current Charges"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your Reference"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }},
            "38": {  # ANAND AND ANAND
        "name": "ANAND",
        "invoice_number": {
            "keywords": ["Invoice Number"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Invoice Date"],
            "line_offset": 0,
            "extract_type": "after_keyword",
            "date_format": "DD-MMM-YYYY"  # 특정 날짜 형식
        },
        "amount": {
            "keywords": ["Total Invoice Value"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },

        "49": {  # KIM & CHANG
        "name": "金&張(KIM&CHANG)",
        "invoice_number": {
            "keywords": ["No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["INVOICE"],  # 키워드 바로 아래 날짜 형식
            "line_offset": 1,
            "extract_type": "line",
            "date_format": "MMM DD, YYYY"
        },
        "amount": {
            "keywords": ["総金額"],  # 일본어로된 총액 키워드
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    }

    ,    "180": {  # Tilleke & Gibbins
        "name": "Tilleke",
        "invoice_number": {
            "keywords": ["Invoice"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Date"],
            "line_offset": 0,
            "extract_type": "after_keyword",
            "date_format": "DD MMM YYYY"  # 특정 날짜 형식
        },
        "amount": {
            "keywords": ["Total Amount Due"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
        "325": {  # Sughrue Mion
        "name": "Sughrue",
        "invoice_number": {
            "keywords": ["INVOICE NO"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["DATE"],
            "line_offset": 0,
            "extract_type": "after_keyword",
            "date_format": "MMM DD, YYYY"
        },
        "amount": {
            "keywords": ["Total for Services and Disbursements"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["YOUR REF"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },

        "164": {  # CPA Global Limited
        "name": "CPA Global",
        "invoice_number": {
            "keywords": ["INVOICE NO"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["INVOICE DATE"],
            "line_offset": 0,
            "extract_type": "after_keyword",
            "date_format": "MMM DD, YYYY"
        },
        "amount": {
            "keywords": ["TOTAL CURRENT INVOICE"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["TTDC REF"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
        "260": {  # D YOUNG & CO LLP
        "name": "D YOUNG",
        "invoice_number": {
            "keywords": ["Invoice No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Tax Point"],
            "line_offset": 0,
            "extract_type": "after_keyword",
            "date_format": "DD MMM YYYY"
        },
        "amount": {
            "keywords": ["Total"],
            "line_offset": 0,
            "extract_type": "line",
            "last_occurrence": True  # 가장 마지막에 위치한 금액만 추출
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },

        "401": {  # Henry Goh & Co
        "name": "Henry Goh",
        "invoice_number": {
            "keywords": ["No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Date"],
            "line_offset": 0,
            "extract_type": "after_keyword",
            "date_format": "DD/MM/YYYY"
        },
        "amount": {
            "keywords": ["Total (Inclusive of Tax)"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },

        "76": {  # ABU-GHAZALEH LEGAL SERVICES
        "name": "ABU-GHAZALEH LEGAL SERVICES",
        "invoice_number": {
            "keywords": ["INVOICE NO"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["INVOICE NO"],  # 같은 줄에서 날짜 형식을 탐색
            "line_offset": 0,
            "extract_type": "line"
        },
        "amount": {
            "keywords": ["Rounded TOTAL(USD)"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
    "96": {  # Clarke Mexico
        "name": "Clarke Mexico",
        "invoice_number": {
            "keywords": ["Invoice Number"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Invoice Date"],
            "line_offset": 0,
            "extract_type": "line",
            "date_format": "DD/MM/YYYY"  # "18/12/2024" 형식
        },
        "amount": {
            "keywords": ["Total"],
            "line_offset": 0,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["S.Ref/Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
    "gorodissky": {  # Gorodissky
        "name": "Gorodissky",
        "invoice_number": {
            "keywords": ["Invoice No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Invoice No"],
            "line_offset": 1,  # 키워드 아래 줄에서 날짜 찾기
            "extract_type": "line"
        },
        "amount": {
            "keywords": ["Due for payment USD"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },

        "289": {  # SD PETOSEVIC
        "name": "SD PETOSEVIC",
        "invoice_number": {
            "keywords": ["Invoice No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Invoice No"],
            "line_offset": 1,  # 키워드 섹션 바로 아래에 위치한 날짜
            "extract_type": "line"
        },
        "amount": {
            "keywords": ["TOTAL Amount in EUR"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },


    "258": {  # J.A.KEMP
        "name": "J.A.KEMP",
        "invoice_number": {
            "keywords": ["Invoice No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Date"],
            "line_offset": 0,
            "extract_type": "after_keyword",
            "date_format": "DD/MM/YYYY"
        },
        "amount": {
            "keywords": ["Total Due"],
            "line_offset": 0,
            "extract_type": "after_keyword",
            "currency": "GBP"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "company_name": {
            "keywords": ["J A Kemp LLP"],
            "location": "footer",  # 문서 하단에서 회사 정보 찾기
            "extract_type": "exact_match"
        }
    },    "465": {  # JUPITER LAW PARTNERS의 ID
        "invoice_number": {
            "keywords": ["Invoice No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Date"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["Grand Total"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "case_number": {
            "keywords": ["Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },
        "185": {
        "invoice_number": {
            "keywords": ["DEBIT NOTE No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Date", "Invoice Date"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["Total"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "case_number": {
            "keywords": ["Your Reference"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },

        "43": {
        "invoice_number": {
            "keywords": ["Invoice No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Jakarta"],
            "line_offset": 0,
            "extract_type": "after_keyword",
            "note": "비표준 패턴, 추가 검증 필요"
        },
        "amount": {
            "keywords": ["Invoice Amount"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    }
,
    "80": {
        "invoice_number": {
            "keywords": ["Invoice Date"],
            "line_offset": 1,
            "extract_type": "line"
        },
        "date": {
            "keywords": ["Invoice Date"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["Grand Total"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "case_number": {
            "keywords": ["Your Reference"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },

        "365": {
        "invoice_number": {
            "keywords": ["Tax Invoice No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Tax Invoice Date"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["Balance Due"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "case_number": {
            "keywords": ["Your ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },

        "81": {
        "invoice_number": {
            "keywords": ["Invoice"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Date"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["TOTAL US$"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "case_number": {
            "keywords": ["Your ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },

        "131": {
        "invoice_number": {
            "keywords": ["Invoice No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Date"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["Total"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    }
,
        "204": {
        "invoice_number": {
            "keywords": ["Invoice No"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "date": {
            "keywords": ["Date"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "amount": {
            "keywords": ["TOTAL (US$)"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        },
        "case_number": {
            "keywords": ["Your Ref"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    },

        "46": {
        "invoice_number": {
            "keywords": ["Invoice Number"],
            "line_offset": 1,
            "extract_type": "line"
        },
        "date": {
            "keywords": ["Invoice Date"],
            "line_offset": 1,
            "extract_type": "line"
        },
        "amount": {
            "keywords": ["Total Amount"],
            "line_offset": 1,
            "extract_type": "line"
        },
        "case_number": {
            "keywords": ["Your Reference"],
            "line_offset": 0,
            "extract_type": "after_keyword"
        }
    }
}