"""Truy vấn chỉ đọc, có tham số, không cache dữ liệu bệnh nhân giữa các phiên."""
import json
import pandas as pd
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT = "diabetes-pipeline-511509"
TABLE = f"{PROJECT}.gold.readmission_prediction"
REQUIRED = {"patient_nbr", "encounter_id", "risk_score", "risk_level", "top_factors", "recommended_actions"}
RISK_LEVELS = ["Cao", "Trung bình", "Thấp"]


def client():
    try:
        info = st.secrets.get("gcp_service_account")
    except FileNotFoundError:
        info = None
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(info) if isinstance(info, str) else dict(info)) if info else None
    return bigquery.Client(project=PROJECT, credentials=credentials)


def connect():
    try:
        bq = client()
        table = bq.get_table(TABLE)
        fields = {field.name for field in table.schema}
        missing = REQUIRED - fields
        if missing:
            st.error("Bảng thiếu cột: " + ", ".join(sorted(missing)))
            st.stop()
        return bq, fields, table.location
    except Exception:
        st.error("Chưa đọc được BigQuery. Kiểm tra xác thực, quyền truy cập và tên bảng theo README.")
        st.stop()


def scope(fields, latest):
    if latest and "prediction_date" in fields:
        return f"prediction_date = (SELECT MAX(prediction_date) FROM `{TABLE}`)"
    return "TRUE"


def query(bq, location, sql, parameters=()):
    try:
        job = bq.query(sql, location=location, job_config=bigquery.QueryJobConfig(
            query_parameters=list(parameters), maximum_bytes_billed=2_000_000_000,
            use_legacy_sql=False))
        rows = job.result(timeout=60)
        return pd.DataFrame([dict(row) for row in rows], columns=[f.name for f in rows.schema])
    except Exception:
        st.error("Truy vấn không hoàn tất. Kiểm tra quyền, vùng dữ liệu và giới hạn 2 GB mỗi truy vấn; xem README.")
        st.stop()


def batch_control(fields):
    if "prediction_date" not in fields:
        st.info("Chưa xác nhận cột prediction_date: đang thống kê tất cả bản ghi, có thể gồm nhiều đợt dự báo.")
        return False
    return st.checkbox("Chỉ xem đợt dự báo mới nhất", value=True)


def patient_filters():
    levels = st.multiselect("Mức nguy cơ", RISK_LEVELS, default=["Cao"])
    minimum = st.slider("Điểm nguy cơ tối thiểu", 0.0, 1.0, 0.0, 0.01)
    patient = st.text_input("Mã bệnh nhân (khớp chính xác)").strip()
    if patient and (not patient.isascii() or not patient.isdigit()):
        st.warning("Mã bệnh nhân chỉ gồm chữ số.")
        st.stop()
    return levels, minimum, patient


def detail_sql(fields, latest, levels, minimum, patient, page):
    where = scope(fields, latest) + " AND risk_level IN UNNEST(@levels) AND risk_score >= @minimum"
    params = [bigquery.ArrayQueryParameter("levels", "STRING", levels),
              bigquery.ScalarQueryParameter("minimum", "FLOAT64", minimum)]
    if patient:
        where += " AND CAST(patient_nbr AS STRING) = @patient"
        params.append(bigquery.ScalarQueryParameter("patient", "STRING", patient))
    params.append(bigquery.ScalarQueryParameter("offset", "INT64", (page - 1) * 100))
    sql = f"""SELECT CAST(patient_nbr AS STRING) patient_nbr,
        CAST(encounter_id AS STRING) encounter_id, risk_score, risk_level,
        top_factors, recommended_actions FROM `{TABLE}` WHERE {where}
        ORDER BY risk_score DESC, patient_nbr, encounter_id LIMIT 101 OFFSET @offset"""
    return sql, params


def patient_rows(bq, fields, location, latest):
    levels, minimum, patient = patient_filters()
    page = st.number_input("Trang kết quả (100 bản ghi/trang)", min_value=1, value=1, step=1)
    sql, params = detail_sql(fields, latest, levels, minimum, patient, page)
    rows = query(bq, location, sql, params)
    st.caption(f"Trang {page} · Có trang sau: {'Có' if len(rows) > 100 else 'Không'}")
    return rows.head(100)
