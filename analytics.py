"""SQL tổng hợp và nối hồ sơ; không cache dữ liệu bệnh nhân."""
import pandas as pd
import data
from google.cloud import bigquery
from google.api_core.exceptions import Forbidden, NotFound, GoogleAPICallError

WIDE_TABLE = f"{data.PROJECT}.gold.wide_table"
PROFILE_FIELDS = {"age", "gender", "number_inpatient", "time_in_hospital"}


def cohort(fields, latest, levels, minimum):
    where = data.scope(fields, latest) + " AND risk_level IN UNNEST(@levels)"
    params = [bigquery.ArrayQueryParameter("levels", "STRING", levels)]
    if minimum > 0:
        where += " AND risk_score >= @minimum"
        params.append(bigquery.ScalarQueryParameter("minimum", "FLOAT64", minimum))
    return where, params


def load_overview(bq, fields, location, latest, levels, minimum):
    where, params = cohort(fields, latest, levels, minimum)
    date = "MAX(prediction_date)" if "prediction_date" in fields else "NULL"
    summary = data.query(bq, location, f"""SELECT COUNT(*) total_predictions,
        COUNT(DISTINCT patient_nbr) unique_patients, AVG(risk_score) avg_score,
        COUNTIF(risk_score IS NULL OR risk_score < 0 OR risk_score > 1) invalid_scores,
        {date} latest FROM `{data.TABLE}` WHERE {where}""", params).iloc[0]
    distribution = data.query(bq, location, f"""SELECT risk_level, COUNT(*) prediction_count,
        AVG(risk_score) avg_score FROM `{data.TABLE}` WHERE {where} GROUP BY risk_level""", params)
    histogram = data.query(bq, location, f"""SELECT risk_level,
        LEAST(CAST(FLOOR(risk_score * 20) AS INT64), 19) / 20.0 score_start,
        (LEAST(CAST(FLOOR(risk_score * 20) AS INT64), 19) + 1) / 20.0 score_end,
        COUNT(*) prediction_count FROM `{data.TABLE}` WHERE {where}
        AND risk_score BETWEEN 0 AND 1 GROUP BY risk_level, score_start, score_end""", params)
    factors = data.query(bq, location, f"""SELECT factor, COUNT(*) prediction_count
        FROM `{data.TABLE}` CROSS JOIN UNNEST(ARRAY(
            SELECT DISTINCT TRIM(part) FROM UNNEST(SPLIT(COALESCE(top_factors, ''), '|')) part
            WHERE TRIM(part) != '')) factor
        WHERE {where} GROUP BY factor ORDER BY prediction_count DESC, factor LIMIT 8""", params)
    return summary, distribution, histogram, factors


def profile_sql(fields, wide_fields, latest, levels, minimum):
    where, params = cohort(fields, latest, levels, minimum)
    selected = PROFILE_FIELDS & wide_fields
    columns = []
    for name in sorted(selected):
        kind = "STRING" if name in {"age", "gender"} else "FLOAT64"
        columns.append(f"MAX(SAFE_CAST({name} AS {kind})) AS {name}")
    expressions = {
        "age": "CASE WHEN age IS NULL OR TRIM(age) IN ('', '?', 'None') THEN 'Chưa rõ' ELSE age END",
        "gender": "CASE gender WHEN 'Male' THEN 'Nam' WHEN 'Female' THEN 'Nữ' ELSE 'Chưa rõ' END",
        "number_inpatient": "CASE WHEN number_inpatient IS NULL OR number_inpatient < 0 OR MOD(number_inpatient, 1) != 0 THEN 'Chưa rõ' WHEN number_inpatient = 0 THEN '0 lần' WHEN number_inpatient = 1 THEN '1 lần' WHEN number_inpatient = 2 THEN '2 lần' ELSE '3+ lần' END",
        "time_in_hospital": "CASE WHEN time_in_hospital IS NULL OR time_in_hospital <= 0 OR MOD(time_in_hospital, 1) != 0 THEN 'Chưa rõ' WHEN time_in_hospital <= 3 THEN '01–03 ngày' WHEN time_in_hospital <= 7 THEN '04–07 ngày' ELSE '08+ ngày' END",
    }
    dimensions = ", ".join(f"STRUCT('{name}' AS dimension, {expressions[name]} AS category)" for name in sorted(selected))
    sql = f"""WITH p AS (SELECT patient_nbr, encounter_id, risk_level, risk_score FROM `{data.TABLE}` WHERE {where}),
        w AS (SELECT CAST(patient_nbr AS STRING) patient_key, CAST(encounter_id AS STRING) encounter_key,
            COUNT(*) key_rows, {', '.join(columns)} FROM `{WIDE_TABLE}` GROUP BY patient_key, encounter_key),
        joined AS (SELECT p.*, w.* FROM p LEFT JOIN w
            ON CAST(p.patient_nbr AS STRING) = w.patient_key AND CAST(p.encounter_id AS STRING) = w.encounter_key)
        SELECT dimension, category, risk_level, COUNT(*) prediction_count, AVG(risk_score) avg_score
        FROM joined CROSS JOIN UNNEST([{dimensions}]) WHERE key_rows = 1
        GROUP BY dimension, category, risk_level
        UNION ALL SELECT 'coverage', CASE WHEN key_rows = 1 THEN 'matched' WHEN key_rows > 1 THEN 'ambiguous' ELSE 'unmatched' END,
            '', COUNT(*), AVG(risk_score) FROM joined GROUP BY 2"""
    return sql, params


def load_profiles(bq, fields, location, latest, levels, minimum):
    try:
        table = bq.get_table(WIDE_TABLE)
        wide_fields = {f.name for f in table.schema}
        if not {"patient_nbr", "encounter_id"}.issubset(wide_fields):
            return None, "wide_table chưa có đủ patient_nbr và encounter_id để nối an toàn."
        if not PROFILE_FIELDS & wide_fields:
            return None, "wide_table chưa có cột tuổi, giới tính, số lần nhập viện hoặc thời gian nằm viện."
        if table.location != location:
            return None, "Hai bảng khác vùng BigQuery, chưa thể nối trực tiếp."
        sql, params = profile_sql(fields, wide_fields, latest, levels, minimum)
        rows = bq.query(sql, location=location, job_config=bigquery.QueryJobConfig(
            query_parameters=params, maximum_bytes_billed=2_000_000_000, use_legacy_sql=False)).result(timeout=60)
        return pd.DataFrame([dict(row) for row in rows], columns=[f.name for f in rows.schema]), None
    except (Forbidden, NotFound):
        return None, "Chưa đọc được gold.wide_table. Cần BigQuery Data Viewer trên bảng này để phân tích hồ sơ; các biểu đồ dự báo vẫn hoạt động."
    except (GoogleAPICallError, TimeoutError, ValueError):
        return None, "Chưa tải được hồ sơ từ wide_table. Kiểm tra kiểu cột, quyền, vùng và giới hạn 2 GB/truy vấn."
