# Dashboard Giai đoạn 4

## Phạm vi
Streamlit, BigQuery project diabetes-pipeline-511509, bảng gold.readmission_prediction. Không Groq. Không tạo/commit khóa bí mật. Không commit notebook hay dữ liệu cấp bệnh nhân.

## Testing
python -m unittest discover -s tests -v
python -m compileall -q app.py data.py metrics.py pages tests

## Hoàn tất và báo cáo
Mục tiêu còn lại: app deploy trên Streamlit, BigQuery thật hoạt động, giảng viên truy cập được. Xem DEPLOYMENT.md. Sau khi có URL cần nhắc người dùng chụp output theo REPORT_SCREENSHOTS.md, và kiểm tra ảnh trước khi viết báo cáo. Không báo deployment hoàn tất chỉ vì đã tạo repo. Secrets chỉ do người dùng nhập trực tiếp trên nền tảng, không yêu cầu gửi vào chat.
