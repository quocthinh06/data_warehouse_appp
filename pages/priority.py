import streamlit as st
from data import connect, batch_control, patient_rows

st.title("Bệnh nhân ưu tiên")
st.caption("Sắp xếp điểm nguy cơ giảm dần. Lọc theo mức nguy cơ hoặc mã bệnh nhân.")
bq, fields, location = connect()
rows = patient_rows(bq, fields, location, batch_control(fields))
if rows.empty:
    st.info("Không có bản ghi phù hợp. Hãy đổi bộ lọc hoặc số trang.")
else:
    st.dataframe(rows, hide_index=True, width="stretch", column_config={
        "risk_score": st.column_config.NumberColumn("Điểm nguy cơ", format="%.4f")})
st.caption("Mức lấy từ pipeline: Cao ≥ phân vị 90%; Trung bình từ phân vị 70% đến dưới 90%; Thấp là phần còn lại. Dashboard không tự đặt lại ngưỡng. Không xuất dữ liệu bệnh nhân trong phiên bản này.")
