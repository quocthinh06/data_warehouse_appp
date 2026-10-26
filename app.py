from pathlib import Path
import streamlit as st
from ui import theme

st.set_page_config(page_title="Diabetes Insight · Phân tích nguy cơ tái nhập viện", page_icon=":material/monitoring:", layout="wide")
theme()
st.logo(str(Path(__file__).parent / "assets/logo.svg"), size="large", icon_image=str(Path(__file__).parent / "assets/icon.svg"))
page = st.navigation([
    st.Page("pages/overview.py", title="Tổng quan", icon=":material/dashboard:", default=True),
    st.Page("pages/priority.py", title="Bệnh nhân ưu tiên", icon=":material/format_list_bulleted:"),
    st.Page("pages/explanation.py", title="Giải thích AI", icon=":material/psychology:"),
    st.Page("pages/performance.py", title="Hiệu quả mô hình", icon=":material/analytics:"),
    st.Page("pages/assistant.py", title="Trợ lý AI", icon=":material/chat:"),
])
page.run()
