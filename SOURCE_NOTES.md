# Đối chiếu Giai đoạn 3

Nguồn local: D:/download/Huan_luyen_AI_Diabetes.ipynb. Chỉ đọc, không chạy lại, không đưa notebook chứa thông tin ngoài phạm vi lên GitHub.

- Cell 8: nhãn dương readmitted == '<30', loại mã xuất viện 11/13/14/19/20/21, sắp encounter_id và giữ lần đầu mỗi bệnh nhân.
- Cell 9: test 20%, validation 15% của 80% còn lại (tổng 12%), train 68%; stratify và random_state=42. Output: 48.631 train, 8.583 validation, 14.304 test.
- Cell 11: test 1.259 dương (8,80%), K=int(round(n*pct)); Precision=hit/K, Recall=hit/total_positive, Lift=Precision/prevalence. ROC-AUC XGBoost 0,6294, Logistic 0,6178; average precision 0,1461 và 0,1414 (notebook đặt tên PR-AUC).
- Cell 18: ngưỡng quantile 90%/70% trên s_xgb chưa làm tròn; sau đó risk_score mới làm tròn 4 chữ số. Không phân loại lại theo điểm đã làm tròn. top_factors lấy tối đa 3 SHAP dương lớn nhất; recommended_actions là ánh xạ quy tắc, nhóm Thấp để trống. prediction_date là ngày chạy lúc 00:00, chung cho toàn đợt.
- Cell 19: ghi BigQuery WRITE_TRUNCATE; dashboard chỉ đọc và không thực thi thao tác ghi này.
- Schema xuất: patient_nbr, encounter_id, risk_score, risk_level, top_factors, recommended_actions, prediction_date.
- CSV evaluation_metrics.csv khớp 9 tổ hợp (3 mô hình × 3 Top K) và các cột của cell 11.
- Chênh lệch Top K=1.430 và nhóm Cao=1.431 phù hợp cơ chế chọn khác nhau; chưa chạy truy vấn BigQuery thật từ dashboard để xác minh trạng thái bảng hiện tại.

SHA256 notebook: 3bb60918c04c83f2180caab5153b8630b45dd05377216dcfd62495cdfd0d449e
