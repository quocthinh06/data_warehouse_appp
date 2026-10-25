import streamlit as st
from data import TABLE, connect, query, scope, batch_control

st.title("Tổng quan")
st.caption("Quy mô dự báo và phân bố nhóm nguy cơ từ dữ liệu thực tế.")
bq, fields, location = connect()
latest = batch_control(fields)
where = scope(fields, latest)
summary = query(bq, location, f"""SELECT COUNT(*) total_predictions,
    COUNT(DISTINCT patient_nbr) unique_patients, AVG(risk_score) avg_score,
    MIN(risk_score) min_score, MAX(risk_score) max_score FROM `{TABLE}` WHERE {where}""").iloc[0]
a, b, c = st.columns(3)
a.metric("Lượt dự báo", f"{int(summary.total_predictions):,}")
b.metric("Bệnh nhân duy nhất", f"{int(summary.unique_patients):,}")
c.metric("Điểm nguy cơ trung bình", "—" if summary.avg_score is None else f"{summary.avg_score:.4f}")
if not summary.total_predictions:
    st.info("Chưa có dự báo trong phạm vi đã chọn.")
    st.stop()
st.subheader("Phân bố nguy cơ")
distribution = query(bq, location, f"""SELECT risk_level, COUNT(*) prediction_count,
    COUNT(DISTINCT patient_nbr) unique_patients, AVG(risk_score) avg_score,
    MIN(risk_score) min_score, MAX(risk_score) max_score
    FROM `{TABLE}` WHERE {where} GROUP BY risk_level""")
distribution["percentage"] = distribution.prediction_count / summary.total_predictions * 100
st.bar_chart(distribution.set_index("risk_level")["prediction_count"], color="#176B59")
st.dataframe(distribution, hide_index=True, width="stretch")
st.caption("Tỷ lệ tính theo lượt dự báo; một bệnh nhân có thể có nhiều lượt. Điểm nguy cơ chưa được xác nhận là xác suất đã hiệu chuẩn.")
if "prediction_date" in fields:
    date = query(bq, location, f"SELECT MAX(prediction_date) latest FROM `{TABLE}`").iloc[0, 0]
    st.caption(f"Thời điểm dự báo mới nhất: {date}")
