"""Biểu đồ tổng hợp, chỉ dùng dữ liệu đã truy vấn hoặc CSV đánh giá."""
import altair as alt
import streamlit as st
from ui import RISK_COLORS

TEAL = "#087F83"
MODEL_COLORS = ["#087F83", "#416A9A", "#AFB9C7"]
RISK = list(RISK_COLORS)


def risk_color():
    return alt.Color("risk_level:N", title="Nhóm nguy cơ", scale=alt.Scale(domain=RISK, range=list(RISK_COLORS.values())), legend=alt.Legend(orient="bottom"))


def show(chart, description):
    view = st.segmented_control("Chế độ xem", ["Biểu đồ", "Dữ liệu"], default="Biểu đồ",
        key="chart_view_" + description, selection_mode="single")
    if view == "Dữ liệu":
        labels = {"risk_level": "Nhóm nguy cơ", "prediction_count": "Lượt dự báo",
            "share": "Tỷ trọng", "avg_score": "Điểm trung bình", "score_start": "Điểm từ",
            "score_end": "Điểm đến", "factor": "Đặc trưng gốc", "label": "Yếu tố",
            "category": "Nhóm", "dimension": "Chiều phân tích"}
        st.dataframe(chart.data.rename(columns=labels), hide_index=True, width="stretch")
        st.caption("Chọn Biểu đồ để quay lại. Dữ liệu giữ nguyên bộ lọc đang xem.")
        return
    chart = chart.configure(background="#FFFFFF").configure_view(stroke=None).configure_axis(
        labelColor="#526579", titleColor="#526579", gridColor="#EDF1F5",
        domain=False, ticks=False, labelFontSize=11, titleFontSize=11,
        labelPadding=8, titlePadding=12).configure_legend(
        labelColor="#526579", titleColor="#142D4E", labelFontSize=11)
    st.altair_chart(chart, width="stretch", theme=None, alt=description)


def donut(frame):
    base = alt.Chart(frame).encode(theta=alt.Theta("prediction_count:Q", stack=True), color=risk_color(),
        tooltip=[alt.Tooltip("risk_level:N", title="Nguy cơ"), alt.Tooltip("prediction_count:Q", title="Lượt", format=","), alt.Tooltip("share:Q", title="Tỷ lệ", format=".1%")])
    return base.mark_arc(innerRadius=70, outerRadius=110, cornerRadius=3, padAngle=.025).properties(height=255)


def histogram(frame):
    return alt.Chart(frame).mark_bar().encode(
        x=alt.X("score_start:Q", bin="binned", title="Điểm nguy cơ", scale=alt.Scale(domain=[0, 1])),
        x2="score_end:Q", y=alt.Y("prediction_count:Q", title="Lượt dự báo", axis=alt.Axis(format=",.0f", tickCount=5)), color=risk_color(),
        tooltip=[alt.Tooltip("score_start:Q", title="Từ", format=".2f"), alt.Tooltip("score_end:Q", title="Đến", format=".2f"), "risk_level:N", alt.Tooltip("prediction_count:Q", title="Lượt", format=",")]).properties(height=255)


def factors(frame):
    return alt.Chart(frame).mark_bar(color=TEAL, cornerRadiusEnd=4, size=15).encode(
        x=alt.X("prediction_count:Q", title="Lượt dự báo có yếu tố", axis=alt.Axis(format=",.0f", tickCount=5)),
        y=alt.Y("label:N", sort="-x", title=None, axis=alt.Axis(labelLimit=230)),
        tooltip=[alt.Tooltip("factor:N", title="Đặc trưng gốc"), alt.Tooltip("prediction_count:Q", title="Lượt", format=",")]).properties(height=260)


def profile(frame, normalized=False):
    return alt.Chart(frame).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X("category:N", title=None, sort="ascending", axis=alt.Axis(labelAngle=0, labelLimit=110)),
        y=alt.Y("prediction_count:Q", stack="normalize" if normalized else "zero", title="Tỷ trọng" if normalized else "Lượt dự báo", axis=alt.Axis(format=".0%" if normalized else ",.0f", tickCount=5)),
        color=risk_color(), tooltip=[alt.Tooltip("category:N", title="Nhóm"), alt.Tooltip("risk_level:N", title="Nguy cơ"), alt.Tooltip("prediction_count:Q", title="Lượt", format=","), alt.Tooltip("avg_score:Q", title="Điểm TB", format=".4f")]).properties(height=255)


def model_bars(frame, metric):
    return alt.Chart(frame).mark_bar(cornerRadiusEnd=4, size=23).encode(
        x=alt.X(f"{metric}:Q", title=metric, axis=alt.Axis(format=".0%") if metric != "Lift" else alt.Axis()),
        y=alt.Y("Mô hình:N", sort=["XGBoost (đề xuất)", "Logistic Regression", "Ngẫu nhiên"], title=None, axis=alt.Axis(labelLimit=180)),
        color=alt.Color("Mô hình:N", scale=alt.Scale(domain=["XGBoost (đề xuất)", "Logistic Regression", "Ngẫu nhiên"], range=MODEL_COLORS), legend=None),
        tooltip=["Mô hình:N", "K:Q", alt.Tooltip(f"{metric}:Q", format=".2%" if metric != "Lift" else ".2f")]).properties(height=170)
