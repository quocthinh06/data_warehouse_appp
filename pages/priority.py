import streamlit as st
from data import connect, batch_control, patient_rows
from ui import heading, patient_columns, note

heading("Bệnh nhân ưu tiên", "Thu hẹp danh sách, xác định lượt khám cần theo dõi và chuyển sang giải thích dự báo.")
st.page_link("pages/overview.py", label="Quay lại tổng quan", icon=":material/arrow_back:")
bq, fields, location = connect()
latest = batch_control(fields)
with st.container(key="patient_filters"):
    rows = patient_rows(bq, fields, location, latest)
if rows.empty:
    st.info("Không có bản ghi phù hợp. Hãy đổi bộ lọc hoặc trở về trang 1.")
else:
    st.subheader("Danh sách theo điểm nguy cơ giảm dần")
    st.dataframe(rows, hide_index=True, width="stretch", column_config=patient_columns(), height=500)
    st.page_link("pages/explanation.py", label="Xem giải thích theo lượt khám", icon=":material/arrow_forward:")
note("Quy tắc ưu tiên từ pipeline", "Cao ≥ phân vị 90%; Trung bình từ phân vị 70% đến dưới 90%; Thấp là phần còn lại. Điểm hiển thị không phải xác suất đã được hiệu chuẩn. Danh sách phân trang 100 lượt, không phải toàn bộ nhóm.")
