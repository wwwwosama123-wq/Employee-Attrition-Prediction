# 1) الأعمدة التي يجب حذفها من البيانات
CONSTANT_COLS = [
    "EmployeeCount",
    "Over18",
    "StandardHours",
]

# أعمدة لا تحمل معلومة تنبؤية
USELESS_COLS = [
    "EmployeeNumber",   
    "MonthlyRate",    
    "DailyRate",        
    "HourlyRate",      
]

DROP_COLS = CONSTANT_COLS + USELESS_COLS


# 2) العمود الهدف
TARGET_COL = "Attrition"


# 3) الحقول الرقمية 
NUMERIC_COLS = [
    "Age",
    "DistanceFromHome",
    "Education",
    "EnvironmentSatisfaction",
    "JobInvolvement",
    "JobLevel",
    "JobSatisfaction",
    "MonthlyIncome",
    "NumCompaniesWorked",
    "PercentSalaryHike",
    "PerformanceRating",
    "RelationshipSatisfaction",
    "StockOptionLevel",
    "TotalWorkingYears",
    "TrainingTimesLastYear",
    "WorkLifeBalance",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
]


# 4) الحقول النصية 

CATEGORICAL_COLS = [
    "BusinessTravel",
    "Department",
    "EducationField",
    "Gender",
    "JobRole",
    "MaritalStatus",
    "OverTime",
]

# 5) القيم الممكنة لكل حقل نصي
CATEGORY_OPTIONS = {
    "BusinessTravel": [
        "Non-Travel",
        "Travel_Rarely",
        "Travel_Frequently",
    ],
    "Department": [
        "Sales",
        "Research & Development",
        "Human Resources",
    ],
    "EducationField": [
        "Life Sciences",
        "Medical",
        "Marketing",
        "Technical Degree",
        "Human Resources",
        "Other",
    ],
    "Gender": ["Male", "Female"],
    "JobRole": [
        "Sales Executive",
        "Research Scientist",
        "Laboratory Technician",
        "Manufacturing Director",
        "Healthcare Representative",
        "Manager",
        "Sales Representative",
        "Research Director",
        "Human Resources",
    ],
    "MaritalStatus": ["Single", "Married", "Divorced"],
    "OverTime": ["Yes", "No"],
}

# 6) التسميات العربية
LABELS = {
    "Age": "العمر",
    "Gender": "الجنس",
    "MaritalStatus": "الحالة الاجتماعية",
    "DistanceFromHome": "المسافة من المنزل (كم)",
    "Department": "القسم",
    "JobRole": "المسمى الوظيفي",
    "JobLevel": "المستوى الوظيفي",
    "MonthlyIncome": "الدخل الشهري",
    "PercentSalaryHike": "نسبة زيادة الراتب (%)",
    "OverTime": "العمل الإضافي",
    "JobSatisfaction": "الرضا عن العمل",
    "EnvironmentSatisfaction": "الرضا عن البيئة",
    "JobInvolvement": "المشاركة في العمل",
    "PerformanceRating": "تقييم الأداء",
    "RelationshipSatisfaction": "الرضا عن العلاقات",
    "WorkLifeBalance": "التوازن بين العمل والحياة",
    "TotalWorkingYears": "إجمالي سنوات العمل",
    "YearsAtCompany": "سنوات العمل في الشركة",
    "YearsInCurrentRole": "سنوات في الوظيفة الحالية",
    "YearsSinceLastPromotion": "سنوات منذ آخر ترقية",
    "YearsWithCurrManager": "سنوات مع المدير الحالي",
    "NumCompaniesWorked": "عدد الشركات السابقة",
    "TrainingTimesLastYear": "مرات التدريب",
    "StockOptionLevel": "مستوى الأسهم",
    "Education": "مستوى التعليم",
    "EducationField": "مجال التعليم",
    "BusinessTravel": "السفر للعمل",
}


# 7) القيم الافتراضية (للحقول الرقمية)
DEFAULTS = {
    "Age": 30,
    "DistanceFromHome": 5,
    "Education": 3,
    "EnvironmentSatisfaction": 3,
    "JobInvolvement": 3,
    "JobLevel": 2,
    "JobSatisfaction": 3,
    "MonthlyIncome": 5000,
    "NumCompaniesWorked": 2,
    "PercentSalaryHike": 13,
    "PerformanceRating": 3,
    "RelationshipSatisfaction": 3,
    "StockOptionLevel": 0,
    "TotalWorkingYears": 10,
    "TrainingTimesLastYear": 2,
    "WorkLifeBalance": 3,
    "YearsAtCompany": 5,
    "YearsInCurrentRole": 3,
    "YearsSinceLastPromotion": 1,
    "YearsWithCurrManager": 3,
}


# 8) حدود منطقية للحقول الرقمية 
VALID_RANGES = {
    "Age": (18, 60),
    "DistanceFromHome": (1, 29),
    "Education": (1, 5),
    "EnvironmentSatisfaction": (1, 4),
    "JobInvolvement": (1, 4),
    "JobLevel": (1, 5),
    "JobSatisfaction": (1, 4),
    "MonthlyIncome": (1000, 20000),
    "NumCompaniesWorked": (0, 10),
    "PercentSalaryHike": (10, 25),
    "PerformanceRating": (3, 4),
    "RelationshipSatisfaction": (1, 4),
    "StockOptionLevel": (0, 3),
    "TotalWorkingYears": (0, 40),
    "TrainingTimesLastYear": (0, 6),
    "WorkLifeBalance": (1, 4),
    "YearsAtCompany": (0, 40),
    "YearsInCurrentRole": (0, 20),
    "YearsSinceLastPromotion": (0, 15),
    "YearsWithCurrManager": (0, 20),
}


# 9) هيكل الأقسام في الواجهة

FORM_SECTIONS = [
    (
        "① معلومات شخصية",
        [
            ("Age", "entry"),
            ("Gender", "combo"),
            ("MaritalStatus", "combo"),
            ("DistanceFromHome", "entry"),
        ],
    ),
    (
        "② بيانات الوظيفة والراتب",
        [
            ("Department", "combo"),
            ("JobRole", "combo"),
            ("JobLevel", "combo"),
            ("MonthlyIncome", "entry"),
            ("PercentSalaryHike", "entry"),
            ("OverTime", "combo"),
            ("StockOptionLevel", "combo"),
        ],
    ),
    (
        "③ الرضا والأداء",
        [
            ("JobSatisfaction", "combo"),
            ("EnvironmentSatisfaction", "combo"),
            ("JobInvolvement", "combo"),
            ("PerformanceRating", "combo"),
            ("RelationshipSatisfaction", "combo"),
            ("WorkLifeBalance", "combo"),
        ],
    ),
    (
        "④ الخبرة والتطور",
        [
            ("TotalWorkingYears", "entry"),
            ("YearsAtCompany", "entry"),
            ("YearsInCurrentRole", "entry"),
            ("YearsSinceLastPromotion", "entry"),
            ("YearsWithCurrManager", "entry"),
            ("NumCompaniesWorked", "entry"),
            ("TrainingTimesLastYear", "combo"),
        ],
    ),
    (
        "⑤ التعليم",
        [
            ("Education", "combo"),
            ("EducationField", "combo"),
            ("BusinessTravel", "combo"),
        ],
    ),
]