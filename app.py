from pathlib import Path
import streamlit as st
from ui import theme

st.set_page_config(page_title="Readmission AI · Diabetes Analytics", page_icon=":material/monitoring:", layout="wide")
theme()
st.logo(str(Path(__file__).parent / "assets/logo.svg"), size="large", icon_image=str(Path(__file__).parent / "assets/icon.svg"))
page = st.navigation([
    st.Page("pages/overview.py", title="Tổng quan", icon=":material/dashboard:", default=True),
    st.Page("pages/priority.py", title="Bệnh nhân ưu tiên", icon=":material/format_list_bulleted:"),
    st.Page("pages/explanation.py", title="Giải thích AI", icon=":material/psychology:"),
    st.Page("pages/performance.py", title="Hiệu quả mô hình", icon=":material/analytics:"),
])
st.sidebar.divider()
st.sidebar.markdown("### Theo dõi sau xuất viện")
st.sidebar.caption("Phân tích nguy cơ tái nhập viện dưới 30 ngày từ tầng Gold của kho dữ liệu.")
st.sidebar.caption("Giai đoạn 4 · Streamlit + BigQuery")
st.sidebar.divider()
st.sidebar.caption("Hỗ trợ ưu tiên theo dõi. Hành động đề xuất cần được nhân viên chuyên môn rà soát.")
page.run()
