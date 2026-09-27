import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import joblib

from config import (
    LABELS,
    DEFAULTS,
    VALID_RANGES,
    FORM_SECTIONS,
    NUMERIC_COLS,
    CATEGORICAL_COLS,
    CATEGORY_OPTIONS,
)

# 1) تحميل النموذج

print(" جارٍ تحميل النموذج...")
data = joblib.load("hr_attrition_model.joblib")

model = data["model"]
scaler = data["scaler"]
features = data["feature_names"]
num_cols = data["num_cols"]
model_category_options = data["category_options"]

print(" تم تحميل النموذج بنجاح\n")


# 2) بناء قوائم الخيارات

OPTIONS = {}
for field, values in CATEGORY_OPTIONS.items():
    OPTIONS[field] = {v: v for v in values}  

# ترجمة يدوية للقوائم المنسدلة الخاصة
ARABIC_OPTIONS = {
    "Gender": {"ذكر": "Male", "أنثى": "Female"},
    "MaritalStatus": {"أعزب": "Single", "متزوج": "Married", "مطلق": "Divorced"},
    "OverTime": {"لا": "No", "نعم": "Yes"},
    "BusinessTravel": {
        "لا توجد سفرات": "Non-Travel",
        "سفر نادر": "Travel_Rarely",
        "سفر متكرر": "Travel_Frequently",
    },
    "Department": {
        "المبيعات": "Sales",
        "البحث والتطوير": "Research & Development",
        "الموارد البشرية": "Human Resources",
    },
    "EducationField": {
        "علوم الحياة": "Life Sciences",
        "الطب": "Medical",
        "التسويق": "Marketing",
        "درجة تقنية": "Technical Degree",
        "الموارد البشرية": "Human Resources",
        "أخرى": "Other",
    },
    "JobRole": {
        "تنفيذي مبيعات": "Sales Executive",
        "باحث علمي": "Research Scientist",
        "فني مختبر": "Laboratory Technician",
        "مدير تصنيع": "Manufacturing Director",
        "ممثل رعاية صحية": "Healthcare Representative",
        "مدير": "Manager",
        "ممثل مبيعات": "Sales Representative",
        "مدير أبحاث": "Research Director",
        "موارد بشرية": "Human Resources",
    },
}

# قوائم رقمية بتسميات عربية
NUMERIC_OPTIONS = {
    "JobLevel": {"1 - مبتدئ": 1, "2": 2, "3": 3, "4": 4, "5 - إداري": 5},
    "StockOptionLevel": {"0 (لا يوجد)": 0, "1": 1, "2": 2, "3": 3},
    "Education": {"1": 1, "2": 2, "3 - بكالوريوس": 3, "4 - ماجستير": 4, "5 - دكتوراه": 5},
    "JobSatisfaction": {"1 - منخفض": 1, "2": 2, "3": 3, "4 - مرتفع": 4},
    "EnvironmentSatisfaction": {"1 - منخفض": 1, "2": 2, "3": 3, "4 - مرتفع": 4},
    "JobInvolvement": {"1 - منخفض": 1, "2": 2, "3": 3, "4 - مرتفع": 4},
    "PerformanceRating": {"3 - جيد": 3, "4 - ممتاز": 4},
    "RelationshipSatisfaction": {"1 - منخفض": 1, "2": 2, "3": 3, "4 - مرتفع": 4},
    "WorkLifeBalance": {"1 - ضعيف": 1, "2": 2, "3": 3, "4 - ممتاز": 4},
    "TrainingTimesLastYear": {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6},
}

# دمج كل القواميس
ALL_OPTIONS = {**ARABIC_OPTIONS, **NUMERIC_OPTIONS}


# 3) الكلاس الرئيسي

class AttritionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام التنبؤ باستقالة الموظفين")
        self.root.geometry("1200x800")
        self.root.minsize(1100, 700)
        self.root.configure(bg="#f4f6f8")

        self.fields = {}  

        self._setup_style()
        self._build_header()
        self._build_body()

    # إعداد الأنماط
    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", padding=6, font=("Arial", 11))
        style.configure("TEntry", padding=6, font=("Arial", 11))
        style.configure("Horizontal.TProgressbar", thickness=14)
        style.map("TCombobox", fieldbackground=[("readonly", "white")])

    # الترويسة
    def _build_header(self):
        header = tk.Frame(self.root, bg="#1f4e78", height=85)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="نظام التنبؤ باستقالة الموظفين",
            font=("Arial", 22, "bold"),
            bg="#1f4e78", fg="white",
        ).pack(pady=(15, 2))

        tk.Label(
            header,
            text="أدخل بيانات الموظف ثم اضغط «تنبؤ» للحصول على النتيجة",
            font=("Arial", 11),
            bg="#1f4e78", fg="#dceaf7",
        ).pack()

    # الجسم الرئيسي (عمودان)
    def _build_body(self):
        body = tk.Frame(self.root, bg="#f4f6f8")
        body.pack(fill="both", expand=True, padx=15, pady=12)

        # عمود يسار: النموذج
        left = tk.Frame(body, bg="white", bd=1, relief="solid")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self._build_form(left)

        # عمود يمين: النتيجة
        right = tk.Frame(body, bg="white", bd=1,
                         relief="solid", width=380)
        right.pack(side="right", fill="y", padx=(8, 0))
        right.pack_propagate(False)
        self._build_result(right)

    # نموذج الإدخال
    def _build_form(self, parent):
        tk.Label(
            parent, text="بيانات الموظف",
            font=("Arial", 17, "bold"),
            bg="white", fg="#1f4e78",
        ).pack(anchor="e", padx=20, pady=(14, 6))

        tk.Label(
            parent,
            text="جميع الحقول لها قيم افتراضية — عدّلها حسب الحاجة",
            font=("Arial", 9), bg="white", fg="#888",
        ).pack(anchor="e", padx=20, pady=(0, 8))

        # ---- Canvas للتمرير ----
        container = tk.Frame(parent, bg="white")
        container.pack(fill="both", expand=True, padx=8, pady=6)

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical",
                                  command=canvas.yview)
        inner = tk.Frame(canvas, bg="white")

        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-e.delta / 120), "units"),
        )

        # ---- بناء الأقسام ----
        for title, fields in FORM_SECTIONS:
            self._build_section(inner, title, fields)

        inner.columnconfigure(1, weight=1)

    # قسم واحد
    def _build_section(self, parent, title, fields):
        bar = tk.Frame(parent, bg="#eaf2f8")
        bar.grid(
            row=self._next_row(parent), column=0, columnspan=2,
            sticky="ew", padx=6, pady=(12, 6),
        )

        tk.Label(
            bar, text=title,
            font=("Arial", 12, "bold"),
            bg="#eaf2f8", fg="#1f4e78",
            anchor="e", padx=10, pady=6,
        ).pack(fill="x")

        for key, kind in fields:
            self._build_field(parent, key, kind)

    # --------------------------------------------------------
    # حقل واحد
    # --------------------------------------------------------
    def _build_field(self, parent, key, kind):
        row = self._next_row(parent)

        # التسمية
        tk.Label(
            parent,
            text=LABELS.get(key, key),
            font=("Arial", 11),
            bg="white", fg="#333",
            anchor="e", width=26,
        ).grid(row=row, column=0, padx=(10, 8), pady=5, sticky="e")

        # الحقل
        if kind == "combo" and key in ALL_OPTIONS:
            # قائمة منسدلة (نصية أو رقمية)
            widget = ttk.Combobox(
                parent,
                values=list(ALL_OPTIONS[key].keys()),
                state="readonly",
                width=28,
                font=("Arial", 11),
            )
            widget.current(0)

        else:
            # حقل رقمي
            widget = tk.Entry(
                parent,
                width=30, justify="right",
                relief="solid", bd=1,
                font=("Arial", 11),
                bg="#fdfdfd",
            )
            if key in DEFAULTS:
                widget.insert(0, str(DEFAULTS[key]))

        widget.grid(row=row, column=1, padx=(8, 12),
                    pady=5, sticky="ew")
        self.fields[key] = widget

    # --------------------------------------------------------
    # رقم الصف التالي
    # --------------------------------------------------------
    def _next_row(self, parent):
        return len(parent.grid_slaves())

    # --------------------------------------------------------
    # لوحة النتائج
    # --------------------------------------------------------
    def _build_result(self, parent):
        tk.Label(
            parent, text="نتيجة التنبؤ",
            font=("Arial", 19, "bold"),
            bg="white", fg="#1f4e78",
        ).pack(pady=(40, 20))

        self.result_icon = tk.Label(
            parent, text="📋", font=("Arial", 40), bg="white",
        )
        self.result_icon.pack(pady=(0, 6))

        self.result_text = tk.Label(
            parent, text="بانتظار التنبؤ",
            font=("Arial", 17, "bold"),
            bg="white", fg="#555", justify="center",
        )
        self.result_text.pack(pady=6)

        self.percent = tk.Label(
            parent, text="-- %",
            font=("Arial", 38, "bold"),
            bg="white", fg="#1f4e78",
        )
        self.percent.pack(pady=12)

        tk.Label(
            parent, text="احتمالية الاستقالة",
            font=("Arial", 10), bg="white", fg="#777",
        ).pack()

        self.progress = ttk.Progressbar(
            parent, orient="horizontal", length=300, maximum=100,
        )
        self.progress.pack(pady=18)

        self.risk = tk.Label(
            parent, text="", font=("Arial", 15, "bold"), bg="white",
        )
        self.risk.pack(pady=8)

        tk.Frame(parent, bg="#e0e0e0", height=1).pack(
            fill="x", padx=30, pady=20,
        )

        # ---- أزرار ----
        buttons = tk.Frame(parent, bg="white")
        buttons.pack(pady=5)

        tk.Button(
            buttons, text="🔮 تنبؤ",
            command=self.predict,
            width=14, height=2,
            font=("Arial", 12, "bold"),
            bg="#1f4e78", fg="white",
            activebackground="#163b5c",
            relief="flat", cursor="hand2",
        ).pack(side="left", padx=5)

        tk.Button(
            buttons, text="🔄 مسح",
            command=self.clear,
            width=14, height=2,
            font=("Arial", 12),
            bg="#e9ecef", fg="#333",
            activebackground="#d6d8db",
            relief="flat", cursor="hand2",
        ).pack(side="left", padx=5)

    # ========================================================
    # تجهيز البيانات للتنبؤ
    # ========================================================
    def _prepare_data(self):
        values = {}
        errors = []

        for key, widget in self.fields.items():
            raw = widget.get().strip()

            # 1) التحقق من الفراغ
            if raw == "":
                errors.append(f"• {LABELS.get(key, key)}: فارغ")
                continue

            # 2) القوائم المنسدلة
            if key in ALL_OPTIONS:
                values[key] = ALL_OPTIONS[key][raw]

            # 3) الحقول الرقمية
            else:
                try:
                    val = float(raw)
                except ValueError:
                    errors.append(
                        f"• {LABELS.get(key, key)}: يجب أن يكون رقمًا"
                    )
                    continue

                # التحقق من النطاق
                if key in VALID_RANGES:
                    lo, hi = VALID_RANGES[key]
                    if not (lo <= val <= hi):
                        errors.append(
                            f"• {LABELS.get(key, key)}: "
                            f"يجب أن يكون بين {lo} و {hi}"
                        )
                        continue

                # تحويل لأعداد صحيحة حيث يلزم
                if val.is_integer():
                    val = int(val)
                values[key] = val

        # إذا كانت هناك أخطاء، نرفع استثناء
        if errors:
            raise ValueError("يرجى تصحيح الأخطاء التالية:\n" + "\n".join(errors))

        # ---- بناء DataFrame ----
        df = pd.DataFrame([values])

        # ---- نفس خطوات التدريب تمامًا ----
        df = pd.get_dummies(df, columns=CATEGORICAL_COLS, drop_first=True)
        df = df.astype(float)

        # إضافة أي أعمدة مفقودة (بأصفار)
        for col in features:
            if col not in df.columns:
                df[col] = 0.0

        # ترتيب الأعمدة كما في التدريب
        df = df[features]

        # تحجيم الأعمدة الرقمية
        df[num_cols] = scaler.transform(df[num_cols])

        return df

    # ========================================================
    # التنبؤ
    # ========================================================
    def predict(self):
        try:
            # 1) تجهيز البيانات
            df = self._prepare_data()

            # 2) الحصول على التنبؤ والاحتمال
            prediction = int(model.predict(df)[0])
            probability = float(model.predict_proba(df)[0][1] * 100)

            # 3) عرض النسبة
            self.percent.config(text=f"{probability:.2f}%")
            self.progress["value"] = probability

            # 4) تحديد مستوى الخطورة
            if probability >= 70:
                level = "مرتفع"
                color = "#d32f2f"   # أحمر
            elif probability >= 40:
                level = "متوسط"
                color = "#f57c00"   # برتقالي
            else:
                level = "منخفض"
                color = "#388e3c"   # أخضر

            self.risk.config(text=f"مستوى الخطورة: {level}", fg=color)
            self.percent.config(fg=color)

            # 5) النتيجة النهائية
            if prediction == 1:
                self.result_icon.config(text="⚠️")
                self.result_text.config(
                    text="احتمال استقالة الموظف",
                    fg="#d32f2f",
                )
            else:
                self.result_icon.config(text="✅")
                self.result_text.config(
                    text="احتمال بقاء الموظف",
                    fg="#388e3c",
                )

        except ValueError as e:
            messagebox.showwarning("تحقق من البيانات", str(e))

        except Exception as e:
            messagebox.showerror(
                "خطأ غير متوقع",
                f"حدث خطأ أثناء التنبؤ:\n{e}",
            )

    # ========================================================
    # مسح الحقول
    # ========================================================
    def clear(self):
        for key, widget in self.fields.items():
            if key in ALL_OPTIONS:
                # إعادة القائمة إلى الخيار الأول
                widget.current(0)
            else:
                # إعادة الحقل الرقمي إلى القيمة الافتراضية
                widget.delete(0, tk.END)
                if key in DEFAULTS:
                    widget.insert(0, str(DEFAULTS[key]))

        # إعادة لوحة النتيجة إلى حالتها الأولية
        self.result_icon.config(text="")
        self.result_text.config(text="بانتظار التنبؤ", fg="#555")
        self.percent.config(text="-- %", fg="#1f4e78")
        self.progress["value"] = 0
        self.risk.config(text="")


# تشغيل البرنامج

if __name__ == "__main__":
    root = tk.Tk()
    app = AttritionApp(root)
    root.mainloop()