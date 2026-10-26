import pandas as pd
import streamlit as st
from data import connect, batch_control, RISK_LEVELS
from analytics import load_overview, load_profiles
from ui import heading, kpis, note, feature_label
import charts
from groq_client import overview_context, profiles_context

heading("Tổng quan nguy cơ tái nhập viện", "Từ dữ liệu kho Gold đến nhóm bệnh nhân cần ưu tiên theo dõi sau xuất viện.")
st.session_state.pop("dashboard_ai_snapshot", None)
bq, fields, location = connect()
with st.container(key="overview_filters"):
    a, b, c = st.columns([2, 1.3, 1.5], vertical_alignment="bottom")
    with a:
        levels = st.multiselect("Nhóm nguy cơ", RISK_LEVELS, default=RISK_LEVELS)
    with b:
        minimum = st.slider("Điểm nguy cơ tối thiểu", 0.0, 1.0, 0.0, .05)
    with c:
        latest = batch_control(fields)
if not levels:
    st.info("Chọn ít nhất một nhóm nguy cơ để bắt đầu phân tích.")
    st.stop()
summary, distribution, histogram, factor_rows = load_overview(bq, fields, location, latest, levels, minimum)
total = int(summary.total_predictions)
if not total:
    st.info("Không có dự báo phù hợp. Hãy mở rộng bộ lọc.")
    st.stop()
st.session_state["dashboard_ai_snapshot"] = overview_context(summary, distribution, histogram, factor_rows, levels, minimum, latest)
distribution = distribution.sort_values("risk_level", key=lambda s: s.map({risk: i for i, risk in enumerate(RISK_LEVELS)}))
distribution["share"] = distribution.prediction_count / total
high = int(distribution.loc[distribution.risk_level == "Cao", "prediction_count"].sum())
score = "—" if pd.isna(summary.avg_score) else f"{summary.avg_score:.4f}"
date = "—" if pd.isna(summary.get("latest")) else str(summary["latest"])[:10]
kpis([
    ("Bệnh nhân", f"{int(summary.unique_patients):,}", f"{total:,} lượt dự báo trong bộ lọc"),
    ("Nguy cơ cao", f"{high:,}", f"{high / total:.1%} lượt cần ưu tiên"),
    ("Điểm nguy cơ trung bình", score, "Thang điểm 0–1 · chưa hiệu chuẩn"),
    ("Ngày dự báo", date, "Đợt mới nhất" if latest else "Trong phạm vi đang xem"),
])
if summary.get("invalid_scores", 0):
    st.warning("Có điểm trống hoặc ngoài [0,1]; các điểm này không được đưa vào histogram.")
left, right = st.columns([1, 1.65])
with left, st.container(border=True, key="panel_risk"):
    st.subheader("Cơ cấu nhóm nguy cơ")
    st.caption("Tỷ trọng lượt dự báo theo phân tầng từ pipeline")
    charts.show(charts.donut(distribution), "Biểu đồ vòng phân bố các nhóm nguy cơ")
    for _, row in distribution.iterrows():
        st.caption(f"{row.risk_level}: {int(row.prediction_count):,} lượt · {row.share:.1%}")
with right, st.container(border=True, key="panel_histogram"):
    st.subheader("Phân bố điểm dự báo")
    st.caption("Mỗi khoảng rộng 0,05 điểm · màu thể hiện nhóm nguy cơ")
    charts.show(charts.histogram(histogram), "Histogram điểm nguy cơ từ 0 đến 1 theo nhóm")
left, right = st.columns([1.65, 1])
with left, st.container(border=True, key="panel_factors"):
    st.subheader("Yếu tố xuất hiện thường xuyên")
    st.caption("Tần suất trong top_factors của các lượt dự báo đã lọc")
    if factor_rows.empty:
        st.info("Chưa có yếu tố giải thích trong phạm vi đã chọn.")
    else:
        factor_rows["label"] = factor_rows.factor.map(feature_label)
        charts.show(charts.factors(factor_rows), "Các yếu tố giải thích xuất hiện nhiều nhất")
with right:
    note("Từ phân tích đến ưu tiên", f"Trong phạm vi đang xem, {high:,} lượt thuộc nhóm Cao. Mở Bệnh nhân ưu tiên để xem thứ tự điểm giảm dần, sau đó xem Giải thích AI theo từng lượt khám.")
    st.page_link("pages/priority.py", label="Xem bệnh nhân ưu tiên", icon=":material/arrow_forward:")
    st.page_link("pages/performance.py", label="Đối chiếu hiệu quả mô hình", icon=":material/analytics:")
    st.caption("Tần suất yếu tố không phải độ lớn SHAP. Nguy cơ dự báo không phải kết quả tái nhập viện thực tế.")
st.subheader("Hồ sơ & lịch sử nhập viện")
st.caption("Nối dữ liệu dự báo với gold.wide_table theo patient_nbr và encounter_id.")
if st.toggle("Hiển thị phân tích hồ sơ", value=True):
    profiles, reason = load_profiles(bq, fields, location, latest, levels, minimum)
    if profiles is None:
        st.info(reason)
    else:
        st.session_state["dashboard_ai_snapshot"]["profiles"] = profiles_context(profiles)
        coverage = profiles[profiles.dimension == "coverage"].set_index("category").prediction_count
        matched = int(coverage.get("matched", 0))
        st.caption(f"Nối duy nhất: {matched:,}/{total:,} lượt ({matched/total:.1%}) · Không khớp: {int(coverage.get('unmatched', 0)):,} · Khóa trùng, loại khỏi hồ sơ: {int(coverage.get('ambiguous', 0)):,}.")
        if not matched:
            st.info("Không có lượt nào nối duy nhất; chưa hiển thị biểu đồ hồ sơ để tránh kết quả sai.")
        else:
            normalized = st.segmented_control("Cách so sánh nhóm", ["Số lượt", "Tỷ trọng nguy cơ"], default="Số lượt") == "Tỷ trọng nguy cơ"
            for pair in [[("age", "Phân bố theo nhóm tuổi"), ("gender", "Phân bố theo giới tính")], [("number_inpatient", "Số lần nhập viện trước"), ("time_in_hospital", "Thời gian nằm viện")]]:
                columns = st.columns(2)
                for column, (dimension, title) in zip(columns, pair):
                    with column, st.container(border=True, key=f"panel_{dimension}"):
                        st.subheader(title)
                        subset = profiles[profiles.dimension == dimension]
                        if subset.empty:
                            st.info("Chưa có trường dữ liệu phù hợp.")
                        else:
                            charts.show(charts.profile(subset, normalized), title)
            st.caption("Phân tích trên các lượt nối duy nhất, không suy ra quan hệ nhân quả. Dữ liệu thiếu/không hợp lệ được giữ ở nhóm Chưa rõ.")
with st.expander("Số liệu tổng hợp & cách đọc"):
    st.dataframe(distribution.rename(columns={"risk_level": "Nguy cơ", "prediction_count": "Lượt dự báo", "avg_score": "Điểm TB", "share": "Tỷ trọng"}), hide_index=True, width="stretch")
    st.caption("Cao ≥ phân vị 90%, Trung bình ≥ phân vị 70% đến dưới 90%, Thấp là phần còn lại. Dashboard giữ nguyên nhãn pipeline; không phân loại lại từ điểm đã làm tròn.")
