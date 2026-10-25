from pathlib import Path
import pandas as pd
import streamlit as st
from metrics import read_metrics, TOPK_COLUMNS

st.title("Hiệu quả mô hình")
st.caption("Chỉ số đánh giá từ evaluation_metrics.csv · Không cần kết nối BigQuery.")
upload = st.file_uploader("Tải evaluation_metrics.csv", type=["csv"])
path = Path(__file__).resolve().parents[1] / "data" / "evaluation_metrics.csv"
source = upload if upload is not None else path if path.exists() else None
if source is None:
    st.info("Chưa có evaluation_metrics.csv. Tải tệp lên hoặc chép vào data/evaluation_metrics.csv. Không có chỉ số mẫu thay thế.")
    st.stop()
size = upload.size if upload is not None else path.stat().st_size
if size > 5 * 1024 * 1024:
    st.error("CSV vượt giới hạn 5 MB.")
    st.stop()
try:
    frame = read_metrics(source)
except (ValueError, UnicodeError, pd.errors.ParserError, OSError):
    st.error("Không đọc được CSV đánh giá. Kiểm tra nội dung, mã hóa UTF-8 và dấu phân cách phẩy.")
    st.stop()
if TOPK_COLUMNS.issubset(frame.columns):
    top = st.selectbox("Phạm vi ưu tiên Top K", frame["Top %"].drop_duplicates().tolist(), index=1 if frame["Top %"].nunique() > 1 else 0)
    selected = frame[frame["Top %"] == top]
    st.subheader(f"So sánh mô hình tại Top {top}")
    left, right = st.columns(2)
    with left:
        st.write("Precision@K — tỷ lệ ca dương trong nhóm được ưu tiên")
        st.bar_chart(selected.set_index("Mô hình")[["Precision@K"]], color="#176B59")
    with right:
        st.write("Recall@K — tỷ lệ ca dương được tìm thấy")
        st.bar_chart(selected.set_index("Mô hình")[["Recall@K"]], color="#176B59")
    st.dataframe(selected, hide_index=True, width="stretch", column_config={
        "Precision@K": st.column_config.NumberColumn(format="%.4f"),
        "Recall@K": st.column_config.NumberColumn(format="%.4f"),
        "Lift": st.column_config.NumberColumn(format="%.4f")})
    st.caption("Precision/Recall hiển thị dạng tỷ lệ 0–1. Lift là Precision@K chia tỷ lệ dương của toàn tập kiểm thử.")
st.subheader("Toàn bộ kết quả đánh giá")
st.dataframe(frame, hide_index=True, width="stretch")
st.caption("Giữ nguyên tên cột, mô hình và chỉ số từ tệp nguồn. Đã đối chiếu notebook Huan_luyen_AI_Diabetes.ipynb: nhãn dương readmitted = <30; chia tập phân tầng, random_state=42. Mỗi bệnh nhân giữ lần nhập viện đầu theo encounter_id.")
st.warning("Tỷ lệ bệnh nhân được gắn nhãn nguy cơ cao không phải precision, recall hay tỷ lệ tái nhập viện thực tế. Không dựng ROC/PR hoặc ma trận nhầm lẫn khi chưa có nhãn thật và điểm dự báo tương ứng.")

if upload is None:
    st.subheader("Bối cảnh đánh giá từ notebook Giai đoạn 3")
    st.write("Train: 48.631 · Validation: 8.583 · Test: 14.304 bệnh nhân, trong đó 1.259 ca tái nhập viện dưới 30 ngày (8,80%).")
    st.table(pd.DataFrame({"Mô hình": ["XGBoost", "Logistic Regression"],
        "ROC-AUC": [0.6294, 0.6178], "Average precision": [0.1461, 0.1414]}))
    st.caption("Các giá trị trên trích từ output cell 11 của notebook đã lưu, không tính lại trong dashboard. Notebook gọi average_precision_score là PR-AUC; ở đây giữ đúng tên average precision.")
    st.info("Top 10% dùng K = round(14.304 × 10%) = 1.430. Nhóm Cao trong pipeline dùng điểm ≥ phân vị 90%, có 1.431 người theo kết quả BigQuery đã đối chiếu. Hai cách chọn không buộc cho cùng số lượng.")
