GRADES_TO_PI_MAP = [
    ("A1", 8),
    ("A2", 7),
    ("B1", 6),
    ("B2", 5),
    ("C1", 4),
    ("C2", 3),
    ("D1", 2),
    ("D2", 1),
    ("E", 0),
]

# Subject Codes Taken From https://freehomedelivery.net/cbse-subject-code/

subject_code_dict_class_12 = {
    "001": "ENGLISH ELECTIVE-N",
    "002": "HINDI ELECTIVE",
    "003": "URDU ELECTIVE",
    "022": "SANSKRIT ELECTIVE",
    "027": "HISTORY",
    "028": "POLITICAL SCIENCE",
    "029": "GEOGRAPHY",
    "030": "ECONOMICS",
    "031": "CARNATIC MUSIC VOC",
    "034": "HIND.MUSIC VOCAL",
    "035": "HIND.MUSIC MEL.INS",
    "036": "HIND MUSIC.INS.PER",
    "037": "PSYCHOLOGY",
    "039": "SOCIOLOGY",
    "040": "PHILOSOPHY",
    "041": "MATHEMATICS",
    "042": "PHYSICS",
    "043": "CHEMISTRY",
    "044": "BIOLOGY",
    "045": "BIOTECHNOLOGY",
    "046": "ENGG. GRAPHICS",
    "048": "PHYSICAL EDUCATION",
    "049": "PAINTING",
    "050": "GRAPHICS",
    "051": "SCULPTURE",
    "052": "APP/COMMERCIAL ART",
    "053": "FASHION STUDIES",
    "054": "BUSINESS STUDIES",
    "055": "ACCOUNTANCY",
    "056": "DANCE-KATHAK",
    "057": "DANCE-BHARATNATYAM",
    "059": "DANCE-ODISSI",
    "061": "DANCE-KATHAKALI",
    "064": "HOME SCIENCE",
    "065": "INFORMATICS PRAC.",
    "066": "ENTREPRENEURSHIP",
    "067": "MULTIMEDIA & WEB T",
    "068": "AGRICULTURE",
    "069": "CR WRTNG TR STUDY",
    "070": "HERITAGE CRAFTS",
    "071": "GRAPHIC DESIGN",
    "072": "MASS MEDIA STUDIES",
    "073": "KNOW TRAD & PRAC.",
    "074": "LEGAL STUDIES",
    "075": "HUMAN RIGHTS & G S",
    "076": "NAT. CADET CORPS",
    "078": "THEATRE STUDIES",
    "079": "LIBRARY & INFO SC.",
    "083": "COMPUTER SCIENCE",
    "101": "ENGLISH ELECTIVE-C",
    "104": "PUNJABI",
    "105": "BENGALI",
    "106": "TAMIL",
    "107": "TELUGU",
    "108": "SINDHI",
    "109": "MARATHI",
    "110": "GUJARATI",
    "111": "MANIPURI",
    "112": "MALAYALAM",
    "113": "ODIA",
    "114": "ASSAMESE",
    "115": "KANNADA",
    "116": "ARABIC",
    "117": "TIBETAN",
    "118": "FRENCH",
    "120": "GERMAN",
    "121": "RUSSIAN",
    "123": "PERSIAN",
    "124": "NEPALI",
    "125": "LIMBOO",
    "126": "LEPCHA",
    "189": "TELUGU – TELANGANA",
    "193": "TANGKHUL",
    "194": "JAPANESE",
    "195": "BHUTIA",
    "196": "SPANISH",
    "198": "MIZO",
    "205": "BENGALI W/O PR.",
    "265": "INFORMATICS PRACTICES (OLD)",
    "283": "COMPUTER SCIENCE (OLD)",
    "301": "ENGLISH CORE",
    "302": "HINDI CORE",
    "303": "URDU CORE",
    "322": "SANSKRIT CORE",
    "604": "OFFCE PROC.& PRAC.",
    "605": "SECY.PRAC & ACCNTG",
    "606": "OFF. COMMUNICATION",
    "607": "TYPOGRAPHY &CA ENG",
    "608": "SHORTHAND ENGLISH",
    "609": "TYPOGRAPHY &CA HIN",
    "610": "SHORTHAND HINDI",
    "622": "ENGINEERING SCI.",
    "625": "APPLIED PHYSICS",
    "626": "MECH. ENGINEERING",
    "627": "AUTO ENGG. – II",
    "628": "AUTOSHOP RPR&PR-II",
    "632": "AC & REFRGTN-III",
    "633": "AC & REFRGTN-IV",
    "657": "BIO-OPTHALMIC – II",
    "658": "OPTICS-II",
    "659": "OPHTHALMIC TECH.",
    "660": "LAB MEDCN-II (MLT)",
    "661": "CLNCL BIOCHEM(MLT)",
    "662": "MICROBIOLOGY (MLT)",
    "666": "RADIATION PHYSICS",
    "667": "RADIOGRAPHY-I (GN)",
    "668": "RADIOGRAPHY-II(SP)",
    "728": "HLT ED,C & PR & PH",
    "729": "B CONCEPT OF HD&MT",
    "730": "FA & EMER MED CARE",
    "731": "CHILD HLTH NURSING",
    "732": "MIDWIFERY",
    "733": "HEALTH CENTRE MGMT",
    "734": "FOOD PROD-III",
    "735": "FOOD PRODUCTION-IV",
    "736": "FOOD SERVICES-II",
    "737": "FOOD BEV CST & CTR",
    "738": "EVOL&FORM OF MM-II",
    "739": "CR&CM PR IN MM-II",
    "740": "GEOSPATIAL TECH",
    "741": "LAB MEDICINE – II",
    "742": "CL BIOCHEM & MB-II",
    "743": "RETAIL OPER – II",
    "744": "RETAIL SERVICES-II",
    "745": "BEAUTY & HAIR – II",
    "746": "HOLISTIC HEALTH-II",
    "747": "LIB SYS & RES MGMT",
    "748": "INFO STORAGE & RET",
    "749": "INTGRTD TRANS OPRN",
    "750": "LOG OP & SCMGMT-II",
    "751": "BAKERY – II",
    "752": "CONFECTIONERY",
    "753": "FRONT OFFICE OPRNS",
    "754": "ADV FRONT OFF OPRN",
    "756": "INTRO TO HOSP MGMT",
    "757": "TR AGN & TOUR OP B",
    "762": "B HORTICULTURE -II",
    "763": "OLERICULTURE – II",
    "765": "FLORICULTURE",
    "766": "BUS.OP & ADMN – II",
    "774": "FABRIC STUDY",
    "775": "BASIC PATTERN DEV.",
    "776": "GARMENT CONST.-II",
    "777": "TRAD IND TEXTILE",
    "778": "PRINTED TEXTILE",
    "779": "TEXTILE CHEM PROC",
    "780": "FIN ACCOUNT – II",
    "781": "COST ACCOUNTING",
    "782": "TAXATION – II",
    "783": "MARKETING-II",
    "784": "SALESMANSHIP-II",
    "785": "BANKING-II",
    "786": "INSURANCE-II",
    "787": "ELECTRICAL MACHINE",
    "788": "ELECTRICAL APPLIAN",
    "789": "OP & MNT OF COM DV",
    "790": "TR SHOOTING & MEE",
    "793": "CAPITAL MKT OPERNS",
    "794": "DERIVATIVE MKT OPR",
    "795": "DATABASE MGMT APP",
    "796": "WEB APPLICATION-II",
    "802": "INFORMATION TECHNOLOGY",
}

subject_code_dict_class_10 = {
    "002": "HINDI COURSE-A",
    "003": "URDU COURSE-A",
    "004": "PUNJABI",
    "005": "BENGALI",
    "006": "TAMIL",
    "007": "TELUGU",
    "008": "SINDHI",
    "009": "MARATHI",
    "010": "GUJARATI",
    "011": "MANIPURI",
    "012": "MALAYALAM",
    "013": "ODIA",
    "014": "ASSAMESE",
    "015": "KANNADA",
    "016": "ARABIC",
    "017": "TIBETAN",
    "018": "FRENCH",
    "020": "GERMAN",
    "021": "RUSSIAN",
    "023": "PERSIAN",
    "024": "NEPALI",
    "025": "LIMBOO",
    "026": "LEPCHA",
    "031": "CARNATIC MUSIC VOC",
    "032": "CAR. MUSIC MEL INS",
    "034": "HIND.MUSIC VOCAL",
    "035": "HIND.MUSIC MEL.INS",
    "036": "HIND MUSIC.PER.INS",
    "041": "MATHEMATICS",
    "049": "PAINTING",
    "064": "HOME SCIENCE",
    "076": "NATIONAL CADET COR",
    "085": "HINDI COURSE-B",
    "086": "SCIENCE-THEORY",
    "087": "SOCIAL SCIENCE",
    "089": "TELUGU – TELANGANA",
    "090": "SCIENCE WITHOUT PR",
    "092": "BODO",
    "093": "TANGKHUL",
    "094": "JAPANESE",
    "095": "BHUTIA",
    "096": "SPANISH",
    "098": "MIZO",
    "099": "BAHASA MELAYU",
    "101": "ENGLISH COMM.",
    "122": "COMM. SANSKRIT",
    "131": "RAI",
    "132": "GURUNG",
    "133": "TAMANG",
    "134": "SHERPA",
    "154": "ELEM. OF BUSINESS",
    "165": "FOUNDATION OF I T",
    "166": "INFO. & COMM. TECH",
    "184": "ENGLISH LNG & LIT.",
    "241": "APPLIED MATHEMATICS",
    "254": "ELEM BOOK-K & ACCY",
    "303": "URDU COURSE-B",
    "354": "e-PUBLISHING -ENG",
    "401": "DYNAMICS OF RET(O)",
    "402": "INFO TECHNOLOGY(O)",
    "403": "SECURITY(O)",
    "404": "AUTOMOBILE TECH(O)",
    "405": "INTR TO FMG (O)",
    "406": "INTR TO TOURISM(O)",
    "407": "BEAUTY & WELLN(O)",
    "454": "e-PUBLISHING -HIN",
    "461": "DYNAMICS OF RET(C)",
    "462": "INFO TECHNOLOGY(C)",
    "463": "SECURITY(C)",
    "464": "AUTOMOBILE TECH(C)",
    "465": "INTR TO FMG (C)",
    "466": "INTR TO TOURISM(C)",
    "467": "BEAUTY & WELLN(C)",
}