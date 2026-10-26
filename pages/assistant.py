import json
import os
import time
from pathlib import Path
import streamlit as st
from metrics import read_metrics
from groq_client import MODEL, ask_groq, metrics_context
from ui import heading, note

heading("Trợ lý AI · Groq", "Hỏi đáp số liệu tổng hợp, đọc biểu đồ và so sánh hiệu quả mô hình bằng tiếng Việt.")
try:
    api_key = st.secrets.get("GROQ_API_KEY", "")
except FileNotFoundError:
    api_key = ""
api_key = api_key or os.environ.get("GROQ_API_KEY", "")
context = {"evaluation": metrics_context(read_metrics(Path(__file__).resolve().parents[1] / "data/evaluation_metrics.csv")),
    "methodology": {"positive_label": "readmitted = <30", "test_patients": 14304,
        "test_positive_cases": 1259, "train_validation_test": "68% / 12% / 20%, phân tầng, random_state=42",
        "risk_groups": "Cao >= phân vị 90%; Trung bình >= phân vị 70% và <90%; Thấp còn lại",
        "top_k": "K = round(n*pct), khác số người thuộc nhóm Cao theo phân vị",
        "source": "Huan_luyen_AI_Diabetes.ipynb, ghi chú trong SOURCE_NOTES.md"}}
snapshot = st.session_state.get("dashboard_ai_snapshot")
if snapshot:
    context["overview"] = snapshot
    st.caption("Nguồn BigQuery: ảnh chụp số liệu từ lần xem Tổng quan gần nhất trong phiên này; dùng đúng bộ lọc được liệt kê bên dưới.")
else:
    st.info("Chưa nạp số liệu Tổng quan trong phiên này. Trợ lý vẫn có thể giải thích chỉ số và CSV đánh giá; muốn hỏi dữ liệu BigQuery hiện tại, mở Tổng quan trước.")
st.caption("Đánh giá mô hình dùng CSV gốc đi kèm app, không tự lấy tệp tải riêng ở trang Hiệu quả mô hình.")
st.page_link("pages/overview.py", label="Mở Tổng quan để nạp/cập nhật số liệu", icon=":material/refresh:")
with st.expander("Nguồn và phạm vi dữ liệu gửi cho AI"):
    st.json(context)
    st.caption("Chỉ có số liệu tổng hợp. Không tự gửi bảng bệnh nhân, mã bệnh nhân, lượt khám hoặc Secrets. Câu hỏi bạn nhập cũng được gửi tới Groq; không nhập thông tin cá nhân.")
signature = json.dumps(context, sort_keys=True, ensure_ascii=False)
if st.session_state.get("groq_context_signature") != signature:
    st.session_state.groq_history = []
    st.session_state.groq_context_signature = signature
history = st.session_state.setdefault("groq_history", [])
if not api_key:
    st.info("Chưa cấu hình Groq. Chủ app cần thêm GROQ_API_KEY vào Streamlit Settings → Secrets. Dashboard vẫn hoạt động bình thường.")
    st.code('GROQ_API_KEY = "DÁN_API_KEY_TRONG_GIAO_DIỆN_SECRETS"', language="toml")
left, right = st.columns([3, 1])
with left:
    st.caption(f"Model: {MODEL} · Không chạy SQL · Không điều chỉnh dự báo")
with right:
    if st.button("Xóa hội thoại", width="stretch"):
        st.session_state.groq_history = []
        st.rerun()
for item in history:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])
st.caption("Câu hỏi và ngữ cảnh tổng hợp được gửi tới Groq. Không nhập thông tin cá nhân hoặc mã định danh bệnh nhân.")
question = st.chat_input("Ví dụ: XGBoost ở Top 10% tốt hơn Logistic Regression thế nào?", disabled=not bool(api_key), max_chars=1500)
if question:
    if time.monotonic() - st.session_state.get("groq_last_request", -1000) < 15:
        st.warning("Vui lòng chờ ít nhất 15 giây giữa hai yêu cầu Groq.")
    else:
        st.session_state.groq_last_request = time.monotonic()
        with st.chat_message("user"):
            st.markdown(question)
        try:
            with st.spinner("Đang phân tích ngữ cảnh dashboard…"):
                answer = ask_groq(api_key, question, context, history)
        except ValueError as exc:
            st.error(str(exc))
        else:
            history.extend([{"role": "user", "content": question}, {"role": "assistant", "content": answer}])
            st.session_state.groq_history = history[-8:]
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.caption("Phản hồi do AI tạo từ ngữ cảnh ở trên; hãy đối chiếu số liệu nguồn trước khi đưa vào báo cáo.")
note("Phạm vi trợ lý", "Dùng để đọc dashboard và diễn giải kết quả học thuật. Không dùng để chẩn đoán, kê đơn hoặc quyết định chăm sóc cho một bệnh nhân. Hội thoại chỉ lưu trong phiên hiện tại.")
