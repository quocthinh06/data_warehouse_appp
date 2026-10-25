import streamlit as st
from data import connect, batch_control, patient_rows
from metrics import split_items
from ui import heading, kpis, feature_label, note

heading("Giải thích AI", "Hiểu lý do một lượt khám được ưu tiên và xem hành động theo dõi do pipeline đề xuất.")
bq, fields, location = connect()
latest = batch_control(fields)
with st.container(key="patient_filters"):
    rows = patient_rows(bq, fields, location, latest)
if rows.empty:
    st.info("Không có bản ghi phù hợp. Hãy đổi bộ lọc hoặc số trang.")
    st.stop()
index = st.selectbox("Chọn lượt khám để phân tích", range(len(rows)), format_func=lambda i:
    f"BN {rows.iloc[i].patient_nbr} · Lượt {rows.iloc[i].encounter_id} · {rows.iloc[i].risk_score:.4f}")
row = rows.iloc[index]
kpis([
    ("Mã bệnh nhân", row.patient_nbr, "Định danh trong tập dữ liệu"),
    ("Lượt khám", row.encounter_id, "Bản ghi đang phân tích"),
    ("Nhóm nguy cơ", row.risk_level, "Phân tầng từ pipeline"),
    ("Điểm dự báo", f"{row.risk_score:.4f}", "Thang điểm 0–1"),
])
left, right = st.columns([1, 1.3])
with left, st.container(border=True, key="panel_reasons"):
    st.subheader("Yếu tố thúc đẩy dự báo")
    st.caption("Tối đa 3 yếu tố SHAP dương lớn nhất, theo notebook nguồn")
    for factor in split_items(row.top_factors):
        st.text(feature_label(factor))
        st.text(factor)
        st.divider()
with right, st.container(border=True, key="panel_actions"):
    st.subheader("Hành động theo dõi đề xuất")
    st.caption("Ánh xạ quy tắc từ yếu tố; cần chuyên môn rà soát")
    for i, action in enumerate(split_items(row.recommended_actions), 1):
        st.text(f"{i}. {action}")
note("Giới hạn giải thích", "Bảng chỉ lưu tên yếu tố, không có giá trị SHAP nên không thể vẽ độ lớn tác động hoặc suy ra quan hệ nhân quả. Hành động hiển thị nguyên văn từ pipeline; không do chatbot tạo mới.")
