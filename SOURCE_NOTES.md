# Đối chiếu Giai đoạn 3 — bộ kết quả cuối 02/11/2026

Nguồn: Project-20261102T153659Z-1-001.zip do người dùng gửi ngày 02/11/2026. Chỉ đọc ZIP; không chạy notebook, không nạp joblib, không ghi BigQuery. Notebook và CSV cấp bệnh nhân không được đưa lên GitHub.

- Notebook: Project/Huan_luyen_AI_Diabetes.ipynb. SHA256: e9d997a09a7b0732185145fd64c0a2c47d119872280c0e7974b1385224ac11c9.
- CSV tổng hợp: Project/03_models/evaluation_metrics.csv, 9 dòng, 3 mô hình × 3 Top K. SHA256: 38a4077acc6f07a1b20ec27b5c6c16a7e9bdf9917660105c1b26d2f591ea3e7b. Sao chép nguyên bản vào data/evaluation_metrics.csv.
- Cell 11 (index từ 0): 45.771 train, 11.443 validation, 14.304 test, tỷ lệ 64%/16%/20%, phân tầng random_state=42.
- Cell 13: XGBoost 400 cây, không cấu hình early stopping. ROC-AUC XGB 0,6229 / LR 0,6177; average_precision_score XGB 0,1456 / LR 0,1412 (output đặt tên PR-AUC).
- Cell 14: test 1.259 ca dương (8,80%), nhãn readmitted = <30. Top K = max(1, int(round(n*pct))). CSV Top 10%: XGB 243/1.430, Recall 243/1.259, Lift 1,930643; LR 241/1.430, Recall 241/1.259, Lift 1,914753.
- Cell 20: risk_level theo quantile 90%/70% trên điểm chưa làm tròn; risk_score làm tròn 4 chữ số sau đó. Tối đa ba SHAP dương; recommended_actions ánh xạ quy tắc, nhóm Thấp rỗng.
- Cells 21 và 31 có output xác nhận đã ghi 14.304 dòng lên gold.readmission_prediction bằng WRITE_TRUNCATE. Đây là bằng chứng từ output notebook, chưa phải truy vấn trực tiếp trạng thái BigQuery hiện tại.
- Đối chiếu CSV dự báo trong ZIP: 14.304 dòng, 14.304 patient_nbr và encounter_id duy nhất; 7 cột đúng schema. prediction_date 2026-11-02; Cao 1.431 / Trung bình 2.860 / Thấp 10.013; trung bình 0,4541007271; min 0,0534 / max 0,9158. Đây là mốc nghiệm thu, không hardcode vào kết quả BigQuery live.
- Schema không đổi; dashboard tiếp tục đọc Gold, không tải CSV cấp bệnh nhân lên Cloud.
- Thay thế bộ nguồn ngày 25/10/2026. Không dùng số liệu, ảnh Groq hoặc ảnh dashboard cũ để minh họa bộ kết quả cuối.

Người dùng xác nhận trên app ngày 02/11/2026: prediction_date = 2026-11-02 và điểm trung bình = 0,4541, khớp CSV cuối. Đây là kiểm tra live do chủ app cung cấp, không phải truy vấn trực tiếp của trợ lý.
