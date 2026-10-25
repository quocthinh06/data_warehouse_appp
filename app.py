import streamlit as st

st.set_page_config(page_title="Theo dõi nguy cơ tái nhập viện", layout="wide")
st.sidebar.title("Dashboard Giai đoạn 4")
st.sidebar.caption("Diabetes · BigQuery Gold")
st.sidebar.info("Thông tin hỗ trợ ưu tiên theo dõi. Các hành động cần được nhân viên chuyên môn rà soát.")
page = st.navigation([
    st.Page("pages/overview.py", title="Tổng quan", default=True),
    st.Page("pages/priority.py", title="Bệnh nhân ưu tiên"),
    st.Page("pages/explanation.py", title="Giải thích AI"),
    st.Page("pages/performance.py", title="Hiệu quả mô hình"),
])
page.run()
