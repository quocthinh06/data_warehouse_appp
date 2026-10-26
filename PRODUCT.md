# Product
<!-- impeccable:product-schema 1 -->
## Platform
web
## Stack
Streamlit, Python — theo yêu cầu người dùng.
## Product Purpose
Dashboard Giai đoạn 4 gồm Tổng quan, Bệnh nhân ưu tiên, Giải thích AI, Hiệu quả mô hình.
## Capabilities and Constraints
BigQuery diabetes-pipeline-511509.gold.readmission_prediction; chỉ đọc. Groq cho hỏi đáp số liệu tổng hợp đã được người dùng chọn ngày 26/10/2026. Không tạo/commit khóa bí mật.
## Evidence on Hand
Schema 6 cột từ đoạn chat. Đã nhận data/evaluation_metrics.csv, 9 dòng của 3 mô hình tại Top 5/10/20%. Đã đọc notebook Huan_luyen_AI_Diabetes.ipynb ở D:/download và ghi nguồn trong SOURCE_NOTES.md.
## Users
Giảng viên và nhóm sinh viên demo bài tập kho dữ liệu. Người dùng yêu cầu kể câu chuyện dữ liệu → nhóm nguy cơ → bệnh nhân ưu tiên → hiệu quả AI, chụp output từ bản deploy.

## Approved analysis extension

Đọc thêm gold.wide_table nếu có quyền và đủ schema. Phân tích tuổi, giới tính, số lần nhập viện trước, thời gian nằm viện trên các cặp patient_nbr/encounter_id nối duy nhất. Nhãn nguy cơ vẫn lấy từ pipeline, không tính lại.

## Groq

Chỉ hỏi đáp số liệu tổng hợp, giải thích biểu đồ và so sánh mô hình. Không diễn giải từng bệnh nhân. Dùng nguồn có phạm vi rõ, lịch sử theo phiên, key do chủ app tự thêm vào Secrets.
