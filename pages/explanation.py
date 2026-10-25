import streamlit as st
from data import connect, batch_control, patient_rows
from metrics import split_items

st.title("Giải thích AI")
st.caption("Các yếu tố và hành động được pipeline Giai đoạn 3 lưu trong BigQuery.")
bq, fields, location = connect()
rows = patient_rows(bq, fields, location, batch_control(fields))
if rows.empty:
    st.info("Không có bản ghi phù hợp.")
    st.stop()
index = st.selectbox("Chọn lượt khám", range(len(rows)), format_func=lambda i:
    f"BN {rows.iloc[i].patient_nbr} · Lượt {rows.iloc[i].encounter_id} · {rows.iloc[i].risk_score:.4f}")
row = rows.iloc[index]
st.subheader(f"Bệnh nhân {row.patient_nbr}")
st.write(f"Mức nguy cơ: **{row.risk_level}** · Điểm: **{row.risk_score:.4f}**")
left, right = st.columns(2)
with left:
    st.subheader("Yếu tố được ghi nhận")
    for item in split_items(row.top_factors):
        st.text("• " + item)
with right:
    st.subheader("Hành động từ pipeline")
    for item in split_items(row.recommended_actions):
        st.text("• " + item)
st.info("Notebook tạo top_factors từ tối đa 3 giá trị SHAP dương lớn nhất. Bảng chỉ lưu tên yếu tố, không lưu giá trị SHAP, nên dashboard không vẽ độ lớn tác động hoặc suy ra quan hệ nhân quả. Hành động được hiển thị nguyên văn để chuyên môn rà soát.")
