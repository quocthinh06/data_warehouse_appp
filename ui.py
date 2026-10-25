"""Thành phần giao diện dùng chung; nội dung từ dữ liệu luôn được escape."""
from html import escape
from pathlib import Path
import streamlit as st

RISK_COLORS = {"Cao": "#C55349", "Trung bình": "#B17A20", "Thấp": "#138A83"}
FEATURE_LABELS = {
    "number_inpatient": "Lần nhập viện trước", "number_emergency": "Lần cấp cứu trước",
    "number_outpatient": "Lần khám ngoại trú", "prior_visits_total": "Tổng lượt khám trước",
    "time_in_hospital": "Thời gian nằm viện", "num_medications": "Số thuốc sử dụng",
    "n_meds_active": "Số thuốc đang dùng", "n_dose_changes": "Số thay đổi liều",
    "age_num": "Tuổi", "number_diagnoses": "Số chẩn đoán", "num_lab_procedures": "Số xét nghiệm",
}


def theme():
    st.html((Path(__file__).parent / "assets/theme.css").read_text(encoding="utf-8"))


def heading(title, description):
    st.html(f'<div class="page-heading"><h1>{escape(title)}</h1><p>{escape(description)}</p></div>')


def kpis(items):
    blocks = "".join(f'<div class="kpi"><span>{escape(str(label))}</span><strong>{escape(str(value))}</strong><small>{escape(str(note))}</small></div>' for label, value, note in items)
    st.html(f'<div class="kpi-strip">{blocks}</div>')


def note(title, text):
    st.html(f'<div class="analysis-note"><strong>{escape(title)}</strong><p>{escape(text)}</p></div>')


def feature_label(value):
    return FEATURE_LABELS.get(str(value), str(value))


def patient_columns():
    return {
        "patient_nbr": st.column_config.TextColumn("Mã bệnh nhân"),
        "encounter_id": st.column_config.TextColumn("Lượt khám"),
        "risk_score": st.column_config.ProgressColumn("Điểm nguy cơ", min_value=0, max_value=1, format="%.4f"),
        "risk_level": st.column_config.TextColumn("Nhóm nguy cơ"),
        "top_factors": st.column_config.TextColumn("Yếu tố chính", width="large"),
        "recommended_actions": st.column_config.TextColumn("Theo dõi đề xuất", width="large"),
    }
