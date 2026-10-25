"""Đọc CSV đánh giá nguyên bản; không suy diễn chỉ số chưa có."""
import math
import pandas as pd

TOPK_COLUMNS = {"Mô hình", "Top %", "K", "Precision@K", "Recall@K", "Lift"}


def split_items(value):
    if value is None or (not isinstance(value, (list, tuple)) and pd.isna(value)):
        return ["Chưa có dữ liệu"]
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value] or ["Chưa có dữ liệu"]
    return [item.strip() for item in str(value).split("|") if item.strip()] or ["Chưa có dữ liệu"]


def read_metrics(source):
    frame = pd.read_csv(source, encoding="utf-8-sig")
    if frame.empty or not len(frame.columns):
        raise ValueError("CSV không có dữ liệu đánh giá.")
    if len(frame) > 10000 or len(frame.columns) > 100:
        raise ValueError("CSV đánh giá vượt giới hạn 10.000 dòng / 100 cột.")
    if TOPK_COLUMNS.issubset(frame.columns):
        if frame[list(TOPK_COLUMNS)].isna().any().any():
            raise ValueError("Thiếu dữ liệu chỉ số Top K.")
        if frame.duplicated(["Mô hình", "Top %"]).any():
            raise ValueError("Trùng mô hình và Top K.")
        for column in ["K", "Precision@K", "Recall@K", "Lift"]:
            frame[column] = pd.to_numeric(frame[column], errors="raise")
            if not frame[column].map(math.isfinite).all():
                raise ValueError("Chỉ số phải hữu hạn.")
        if not frame["K"].gt(0).all() or not frame["K"].mod(1).eq(0).all():
            raise ValueError("K phải là số nguyên dương.")
        if not frame[["Precision@K", "Recall@K"]].apply(lambda s: s.between(0, 1)).all().all():
            raise ValueError("Precision/Recall phải trong [0,1].")
        if not frame["Lift"].ge(0).all():
            raise ValueError("Lift không được âm.")
    return frame
