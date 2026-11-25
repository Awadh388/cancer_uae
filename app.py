from pathlib import Path
import json

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models/outcome_status_model.joblib"
METRICS_PATH = ROOT / "reports/model_metrics.json"
DATA_PATH = ROOT / "data/processed/cleaned_dataset.csv"

st.set_page_config(page_title="UAE Cancer Data Explorer", page_icon="📊", layout="wide")

AR = {
    "Language / اللغة": "اللغة / Language",
    "English (UK)": "الإنجليزية (بريطانيا)",
    "British English": "الإنجليزية البريطانية",
    "UAE Cancer Data Explorer": "مستكشف بيانات السرطان في الإمارات",
    "Educational analysis of recorded dataset labels. Not for diagnosis, treatment, or clinical decisions.": "تحليل تعليمي للتصنيفات المسجلة في مجموعة البيانات. لا يُستخدم للتشخيص أو العلاج أو القرارات السريرية.",
    "This dataset has no documented source or license, and its real-world provenance is unverified. Model outputs are exploratory associations only.": "لا يوجد مصدر أو ترخيص موثّق لمجموعة البيانات، ولم يتم التحقق من أنها تمثل بيانات واقعية. نتائج النموذج استكشافية فقط.",
    "Model artifacts are missing. Add the workbook at data/raw/uae_cancer_dataset_200k.xlsx (or set CANCER_DATA_PATH), then run `python train.py`.": "ملفات النموذج غير موجودة. أضف ملف Excel إلى data/raw/uae_cancer_dataset_200k.xlsx (أو عيّن CANCER_DATA_PATH)، ثم شغّل `python train.py`.",
    "Cleaned data is missing. Run `python train.py` to generate it.": "البيانات المنظّفة غير موجودة. شغّل `python train.py` لإنشائها.",
    "Interactive dashboard": "لوحة تفاعلية",
    "Try a prediction": "جرّب التنبؤ",
    "Model details": "تفاصيل النموذج",
    "Explore the records": "استكشف السجلات",
    "Dashboard filters": "عوامل تصفية اللوحة",
    "Cancer type": "نوع السرطان",
    "Emirate": "الإمارة",
    "Gender": "الجنس",
    "Recorded outcome": "النتيجة المسجلة",
    "Diagnosis year": "سنة التشخيص",
    "Age": "العمر",
    "No records match these filters. Broaden one or more selections.": "لا توجد سجلات تطابق عوامل التصفية. وسّع خياراً واحداً أو أكثر.",
    "Matching records": "السجلات المطابقة",
    "of dataset": "من مجموعة البيانات",
    "Median age": "العمر الوسيط",
    "Cancer types": "أنواع السرطان",
    "Emirates": "الإمارات",
    "Recorded outcome counts": "عدد النتائج المسجلة",
    "Outcome mix by cancer stage": "توزيع النتائج حسب مرحلة السرطان",
    "Diagnosis volume over time": "عدد التشخيصات عبر الزمن",
    "Explore a breakdown": "استكشف التفصيل",
    "Group records by": "جمّع السجلات حسب",
    "View matching records": "عرض السجلات المطابقة",
    "Showing up to 1,000 of {n:,} matching records.": "يعرض حتى 1,000 من أصل {n:,} سجل مطابق.",
    "Download filtered records as CSV": "تنزيل السجلات المصفّاة بصيغة CSV",
    "Adjust diagnosis-time attributes and submit to compare the model's class scores. Treatment and follow-up fields are intentionally excluded.": "أدخل خصائص وقت التشخيص ثم احسب درجات الفئات التي يتوقعها النموذج. تم استبعاد معلومات العلاج والمتابعة عمداً.",
    "BMI (derived from weight and height)": "مؤشر كتلة الجسم (محسوب من الوزن والطول)",
    "Nationality": "الجنسية",
    "Cancer stage": "مرحلة السرطان",
    "Smoking status": "حالة التدخين",
    "Recorded comorbidity": "الأمراض المصاحبة المسجلة",
    "Ethnicity": "الأصل العرقي",
    "Calculate class scores": "احسب درجات الفئات",
    "Most likely recorded class": "الفئة المسجلة الأرجح",
    "{score:.1%} model score": "درجة النموذج {score:.1%}",
    "Recorded class": "الفئة المسجلة",
    "Model score": "درجة النموذج",
    "Scores are model probabilities for dataset labels, not calibrated patient risks or clinical outcomes.": "هذه الدرجات احتمالات لفئات مجموعة البيانات، وليست تقديراً معايراً لمخاطر المرضى أو نتائج سريرية.",
    "How the model performed": "أداء النموذج",
    "Rows modeled": "السجلات المستخدمة في التدريب",
    "Held-out accuracy": "الدقة على بيانات الاختبار",
    "Held-out macro F1": "مقياس F1 الكلي على بيانات الاختبار",
    "Model comparison": "مقارنة النماذج",
    "Tuning selection:": "إعدادات الضبط المختارة:",
    "The target is a recorded label at an unspecified observation time, not survival or treatment effectiveness.": "الهدف هو تصنيف نتيجة مسجلة بوقت رصد غير محدد، وليس التنبؤ بالبقاء أو بفعالية العلاج.",
    "Held-out confusion matrix": "مصفوفة الالتباس لبيانات الاختبار",
    "Outcome": "النتيجة",
    "Records": "السجلات",
    "Diagnoses": "التشخيصات",
    "Cancer_Type": "نوع السرطان",
    "Cancer_Stage": "مرحلة السرطان",
    "Smoking_Status": "حالة التدخين",
    "Nationality": "الجنسية",
    "Patient_ID": "معرّف المريض",
    "Diagnosis_Date": "تاريخ التشخيص",
    "Under Treatment": "قيد العلاج",
    "Recovered": "متعافٍ",
    "Deceased": "متوفى",
    "Female": "أنثى", "Male": "ذكر",
    "Abu Dhabi": "أبوظبي", "Dubai": "دبي", "Sharjah": "الشارقة",
    "Ajman": "عجمان", "Fujairah": "الفجيرة", "Ras Al Khaimah": "رأس الخيمة",
    "Umm Al Quwain": "أم القيوين",
    "Emirati": "إماراتي", "Expatriate": "مقيم",
    "Breast": "الثدي", "Colorectal": "القولون والمستقيم", "Leukemia": "اللوكيميا",
    "Liver": "الكبد", "Lung": "الرئة", "Ovarian": "المبيض", "Pancreatic": "البنكرياس", "Prostate": "البروستاتا",
    "Non-Smoker": "غير مدخن", "Smoker": "مدخن", "Unknown": "غير معروف",
    "Cardiovascular Disease": "أمراض القلب والأوعية الدموية", "Diabetes": "السكري", "Hypertension": "ارتفاع ضغط الدم",
    "African": "أفريقي", "East Asian": "شرق آسيوي", "European": "أوروبي", "South Asian": "جنوب آسيوي", "Arab": "عربي",
}
UK = {
    "Rows modeled": "Rows modelled",
    "This dataset has no documented source or license, and its real-world provenance is unverified. Model outputs are exploratory associations only.": "This dataset has no documented source or licence, and its real-world provenance is unverified. Model outputs are exploratory associations only.",
}

with st.sidebar:
    language_choice = st.selectbox("Language / اللغة", ["English (UK)", "العربية"], index=0, key="language")
is_arabic = language_choice == "العربية"

def tr(text: str) -> str:
    return AR.get(text, text) if is_arabic else UK.get(text, text)

direction_css = "direction: rtl;" if is_arabic else "direction: ltr;"
text_align = "right" if is_arabic else "left"
st.markdown(f"""
<style>
.stApp {{ {direction_css} }}
.stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3,
[data-testid="stSidebar"] {{ text-align: {text_align}; }}
</style>
""", unsafe_allow_html=True)

st.title(tr("UAE Cancer Data Explorer"))
st.caption(tr("Educational analysis of recorded dataset labels. Not for diagnosis, treatment, or clinical decisions."))
st.warning(tr("This dataset has no documented source or license, and its real-world provenance is unverified. Model outputs are exploratory associations only."))

if not MODEL_PATH.exists() or not METRICS_PATH.exists():
    st.error(tr("Model artifacts are missing. Add the workbook at data/raw/uae_cancer_dataset_200k.xlsx (or set CANCER_DATA_PATH), then run `python train.py`."))
    st.stop()

@st.cache_resource
def load_artifacts():
    return joblib.load(MODEL_PATH), json.loads(METRICS_PATH.read_text(encoding="utf-8"))

@st.cache_data(show_spinner=False)
def load_data():
    data = pd.read_csv(DATA_PATH, parse_dates=["Diagnosis_Date"])
    data["Diagnosis_Year"] = data["Diagnosis_Date"].dt.year
    return data

model, metrics = load_artifacts()
if not DATA_PATH.exists():
    st.error(tr("Cleaned data is missing. Run `python train.py` to generate it."))
    st.stop()
data = load_data()

tab1, tab2, tab3 = st.tabs([tr("Interactive dashboard"), tr("Try a prediction"), tr("Model details")])
with tab1:
    st.subheader(tr("Explore the records"))
    with st.sidebar:
        st.header(tr("Dashboard filters"))
        cancer_options = sorted(data["Cancer_Type"].dropna().unique())
        cancer_filter = st.multiselect(tr("Cancer type"), cancer_options, default=cancer_options, format_func=tr)
        emirate_options = sorted(data["Emirate"].dropna().unique())
        emirate_filter = st.multiselect(tr("Emirate"), emirate_options, default=emirate_options, format_func=tr)
        gender_options = sorted(data["Gender"].dropna().unique())
        gender_filter = st.multiselect(tr("Gender"), gender_options, default=gender_options, format_func=tr)
        outcome_options = sorted(data["Outcome"].dropna().unique())
        outcome_filter = st.multiselect(tr("Recorded outcome"), outcome_options, default=outcome_options,
                                        format_func=lambda x: tr(x))
        years = data["Diagnosis_Year"].dropna().astype(int)
        selected_years = st.slider(tr("Diagnosis year"), int(years.min()), int(years.max()),
                                   (int(years.min()), int(years.max())))
        ages = data["Age"].dropna().astype(int)
        selected_ages = st.slider(tr("Age"), int(ages.min()), int(ages.max()),
                                  (int(ages.min()), int(ages.max())))

    filtered = data[
        data["Cancer_Type"].isin(cancer_filter)
        & data["Emirate"].isin(emirate_filter)
        & data["Gender"].isin(gender_filter)
        & data["Outcome"].isin(outcome_filter)
        & data["Diagnosis_Year"].between(*selected_years)
        & data["Age"].between(*selected_ages)
    ]
    if filtered.empty:
        st.info(tr("No records match these filters. Broaden one or more selections."))
    else:
        first, second, third, fourth = st.columns(4)
        first.metric(tr("Matching records"), f"{len(filtered):,}", f"{len(filtered) / len(data):.1%} {tr('of dataset')}")
        second.metric(tr("Median age"), f"{filtered.Age.median():.0f}")
        third.metric(tr("Cancer types"), f"{filtered.Cancer_Type.nunique()}")
        fourth.metric(tr("Emirates"), f"{filtered.Emirate.nunique()}")

        left, right = st.columns(2)
        with left:
            st.markdown(f"**{tr('Recorded outcome counts')}**")
            outcome_counts = filtered["Outcome"].value_counts().rename(index=tr).rename_axis(tr("Outcome")).to_frame(tr("Records"))
            st.bar_chart(outcome_counts, horizontal=True)
        with right:
            st.markdown(f"**{tr('Outcome mix by cancer stage')}**")
            stage_mix = pd.crosstab(filtered["Cancer_Stage"], filtered["Outcome"], normalize="index")
            stage_mix.columns = [tr(value) for value in stage_mix.columns]
            stage_mix.index.name = tr("Cancer stage")
            st.bar_chart(stage_mix, stack="normalize")

        st.markdown(f"**{tr('Diagnosis volume over time')}**")
        yearly = filtered.groupby("Diagnosis_Year").size().rename(tr("Diagnoses"))
        st.line_chart(yearly)

        st.markdown(f"**{tr('Explore a breakdown')}**")
        breakdown_keys = ["Cancer_Type", "Cancer_Stage", "Emirate", "Smoking_Status", "Nationality"]
        breakdown_labels = [tr(key) for key in breakdown_keys]
        selected_breakdown = st.selectbox(tr("Group records by"), breakdown_labels)
        breakdown = breakdown_keys[breakdown_labels.index(selected_breakdown)]
        breakdown_data = pd.crosstab(filtered[breakdown], filtered["Outcome"])
        breakdown_data.index.name = tr(breakdown)
        breakdown_data.columns = [tr(value) for value in breakdown_data.columns]
        st.bar_chart(breakdown_data)
        st.dataframe(breakdown_data, use_container_width=True)

        with st.expander(tr("View matching records")):
            display_cols = ["Patient_ID", "Age", "Gender", "Emirate", "Diagnosis_Date", "Cancer_Type", "Cancer_Stage", "Outcome", "Smoking_Status"]
            view = filtered[display_cols].head(1000).rename(columns={c: tr(c) for c in display_cols})
            view[tr("Outcome")] = view[tr("Outcome")].map(tr)
            st.dataframe(view, use_container_width=True, height=350)
            st.caption(tr("Showing up to 1,000 of {n:,} matching records.").format(n=len(filtered)))
            st.download_button(tr("Download filtered records as CSV"), filtered.to_csv(index=False).encode("utf-8"),
                               file_name="filtered_cancer_records.csv", mime="text/csv")

with tab2:
    st.write(tr("Adjust diagnosis-time attributes and submit to compare the model's class scores. Treatment and follow-up fields are intentionally excluded."))
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        age = col1.slider(tr("Age"), 18, 100, 50)
        bmi = col1.slider(tr("BMI (derived from weight and height)"), 10.0, 55.0, 24.0, 0.5)
        gender = col2.selectbox(tr("Gender"), ["Female", "Male"])
        nationality = col2.selectbox(tr("Nationality"), ["Emirati", "Expatriate"], format_func=tr)
        emirate = col1.selectbox(tr("Emirate"), ["Abu Dhabi", "Dubai", "Sharjah", "Ajman", "Fujairah", "Ras Al Khaimah", "Umm Al Quwain"], format_func=tr)
        cancer = col1.selectbox(tr("Cancer type"), ["Breast", "Colorectal", "Leukemia", "Liver", "Lung", "Ovarian", "Pancreatic", "Prostate"], format_func=tr)
        stage = col2.selectbox(tr("Cancer stage"), ["I", "II", "III", "IV"])
        smoking = col2.selectbox(tr("Smoking status"), ["Non-Smoker", "Smoker"], format_func=tr)
        comorbidity = col1.selectbox(tr("Recorded comorbidity"), ["Unknown", "Cardiovascular Disease", "Diabetes", "Hypertension"], format_func=tr)
        ethnicity = col2.selectbox(tr("Ethnicity"), ["Arab", "African", "East Asian", "European", "South Asian"], format_func=tr)
        submit = st.form_submit_button(tr("Calculate class scores"), type="primary")
    if submit:
        row = pd.DataFrame([{"Age": age, "BMI": bmi, "Gender": gender,
                             "Nationality": nationality, "Emirate": emirate,
                             "Cancer_Type": cancer, "Cancer_Stage": stage,
                             "Smoking_Status": smoking, "Comorbidities": comorbidity,
                             "Ethnicity": ethnicity}])
        probs = model.predict_proba(row)[0]
        result = pd.DataFrame({"Recorded class": model.classes_, "Model score": probs}).sort_values("Model score", ascending=False)
        best = result.iloc[0]
        st.metric(tr("Most likely recorded class"), tr(best["Recorded class"]),
                  tr("{score:.1%} model score").format(score=best["Model score"]))
        plot_result = result.assign(**{"Recorded class": result["Recorded class"].map(tr)})
        st.bar_chart(plot_result.set_index("Recorded class").rename(columns={"Model score": tr("Model score")}), horizontal=True)
        result_display = result.rename(columns={"Recorded class": tr("Recorded class"), "Model score": tr("Model score")})
        result_display[tr("Recorded class")] = result_display[tr("Recorded class")].map(tr)
        st.dataframe(result_display.style.format({tr("Model score"): "{:.1%}"}), use_container_width=True)
        st.caption(tr("Scores are model probabilities for dataset labels, not calibrated patient risks or clinical outcomes."))

with tab3:
    st.subheader(tr("How the model performed"))
    a, b, c = st.columns(3)
    a.metric(tr("Rows modeled"), f"{metrics['rows']:,}")
    b.metric(tr("Held-out accuracy"), f"{metrics['test_metrics']['accuracy']:.1%}")
    c.metric(tr("Held-out macro F1"), f"{metrics['test_metrics']['macro_f1']:.3f}")
    st.markdown(f"**{tr('Model comparison')}**")
    compare = pd.DataFrame(metrics["comparison"]).T.rename_axis("Model")
    st.dataframe(compare.style.format("{:.3f}"), use_container_width=True)
    st.write(tr("Tuning selection:"), metrics["tuning"])
    st.caption(tr("The target is a recorded label at an unspecified observation time, not survival or treatment effectiveness."))
    st.subheader(tr("Held-out confusion matrix"))
    cm = pd.DataFrame(metrics["test_metrics"]["confusion_matrix"],
                      index=[tr(x) for x in metrics["test_metrics"]["class_order"]],
                      columns=[tr(x) for x in metrics["test_metrics"]["class_order"]])
    st.dataframe(cm, use_container_width=True)
