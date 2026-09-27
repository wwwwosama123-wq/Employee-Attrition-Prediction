import pandas as pd
import numpy as np
import joblib
import warnings

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV,
    StratifiedKFold,
)
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    confusion_matrix,
    accuracy_score,
    f1_score,
)

from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.combine import SMOTETomek

from config import (
    DROP_COLS,
    TARGET_COL,
    NUMERIC_COLS,
    CATEGORICAL_COLS,
    CATEGORY_OPTIONS,
)

warnings.filterwarnings("ignore")


# 1) تحميل البيانات وتنظيفها

def load_and_clean_data(path="WA_Fn-UseC_-HR-Employee-Attrition.csv"):
    print("\n[1] تحميل البيانات...")
    df = pd.read_csv(path)

    df = df.drop(columns=DROP_COLS, errors="ignore")

    df[TARGET_COL] = df[TARGET_COL].map({"No": 0, "Yes": 1})

    print(f"    عدد الموظفين       : {len(df)}")
    print(f"    عدد المستقيلين     : {df[TARGET_COL].sum()}")
    print(f"    نسبة الاستقالة     : {df[TARGET_COL].mean() * 100:.2f}%")
    print(f"    عدد الاعمدة المتبقية: {df.shape[1] - 1}")
    return df


# 2) تجهيز الميزات والهدف

def prepare_features(df):
    print("\n[2] تجهيز الميزات...")
    X = df.drop(columns=TARGET_COL)
    y = df[TARGET_COL]

    # التأكد من تطابق الأعمدة مع القوائم
    assert set(X.columns) == set(NUMERIC_COLS + CATEGORICAL_COLS), \
        "الأعمدة لا تتطابق مع config.py"

    X = pd.get_dummies(
        X,
        columns=CATEGORICAL_COLS,
        drop_first=True,
    )
    X = X.astype(float)

    feature_names = X.columns.tolist()
    print(f"    عدد الميزات بعد الترميز: {len(feature_names)}")
    return X, y, feature_names


# 3) تقسيم البيانات

def split_data(X, y):
    print("\n[3] تقسيم البيانات (75% تدريب / 25% اختبار)...")
    return train_test_split(
        X, y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )


# 4) تحجيم الأعمدة الرقمية

def fit_scaler(X_train, X_test):
    print("\n[4] تحجيم الأعمدة الرقمية...")
    scaler = StandardScaler()

    X_train = X_train.copy()
    X_test = X_test.copy()

    X_train[NUMERIC_COLS] = scaler.fit_transform(X_train[NUMERIC_COLS])
    X_test[NUMERIC_COLS] = scaler.transform(X_test[NUMERIC_COLS])

    return X_train, X_test, scaler


# 5) بناء Pipeline

def build_pipeline():
    print("\n[5] بناء Pipeline (SMOTETomek + RandomForest)...")
    return ImbPipeline(steps=[
        ("smote", SMOTETomek(random_state=42)),
        ("clf", RandomForestClassifier(
            random_state=42,
            n_jobs=-1,
            class_weight="balanced",
        )),
    ])


# 6) البحث عن أفضل الإعدادات

def tune_model(pipeline, X_train, y_train):
    print("\n[6] البحث عن أفضل الإعدادات...")

    params = {
        "clf__n_estimators": [200, 300],
        "clf__max_depth": [10, 15, None],
        "clf__min_samples_split": [2, 5],
        "clf__min_samples_leaf": [1, 2],
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    search = GridSearchCV(
        pipeline, params,
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1,
        verbose=1,
    )
    search.fit(X_train, y_train)

    print(f"\n    أفضل الإعدادات: {search.best_params_}")
    print(f"    أفضل ROC-AUC في CV: {search.best_score_:.4f}")
    return search.best_estimator_


# 7) تقييم النموذج

def evaluate_model(model, X_test, y_test):
    print("\n[7] تقييم النموذج على بيانات الاختبار...")

    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]

    print("\nتقرير التصنيف:")
    print(classification_report(y_test, pred, digits=3))

    print(f"Accuracy : {accuracy_score(y_test, pred):.4f}")
    print(f"F1-Score : {f1_score(y_test, pred):.4f}")
    print(f"ROC-AUC  : {roc_auc_score(y_test, prob):.4f}")

    print("\nمصفوفة الارتباك:")
    print(confusion_matrix(y_test, pred))


# 8) حفظ النموذج مع كل ما يحتاجه التطبيق

def save_artifacts(model, scaler, feature_names):
    print("\n[8] حفظ النموذج...")

    artifacts = {
        # النموذج والمعالج
        "model": model,
        "scaler": scaler,

        # أسماء الميزات النهائية بعد الترميز
        "feature_names": feature_names,

        # أعمدة التحجيم
        "num_cols": NUMERIC_COLS,

        # القيم الممكنة للفئات 
        "category_options": CATEGORY_OPTIONS,

        # القيم الافتراضية والحدود
        "defaults": None,  
    }

    joblib.dump(artifacts, "hr_attrition_model.joblib")
    print("     تم الحفظ في: hr_attrition_model.joblib")



def main():
    print("=" * 60)
    print(" تدريب نموذج التنبؤ باستقالة الموظفين")
    print("=" * 60)

    # 1. تحميل وتنظيف
    df = load_and_clean_data()

    # 2. تجهيز الميزات
    X, y, feature_names = prepare_features(df)

    # 3. تقسيم
    X_train, X_test, y_train, y_test = split_data(X, y)

    # 4. تحجيم
    X_train, X_test, scaler = fit_scaler(X_train, X_test)

    # 5. بناء Pipeline
    pipeline = build_pipeline()

    # 6. ضبط المعاملات
    model = tune_model(pipeline, X_train, y_train)

    # 7. تقييم
    evaluate_model(model, X_test, y_test)

    # 8. حفظ
    save_artifacts(model, scaler, feature_names)

    print("\n" + "=" * 60)
    print("  اكتمل التدريب بنجاح")
    print("=" * 60)


if __name__ == "__main__":
    main()