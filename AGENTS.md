# Dashboard Giai đoạn 4

## Phạm vi
Streamlit, BigQuery project diabetes-pipeline-511509, bảng gold.readmission_prediction. Đã được người dùng yêu cầu Groq cho hỏi đáp dashboard tổng hợp; không gửi bản ghi/định danh bệnh nhân. Không tạo/commit khóa bí mật. Không commit notebook hay dữ liệu cấp bệnh nhân.

## Testing
python -m unittest discover -s tests -v
python -m compileall -q app.py data.py analytics.py charts.py ui.py metrics.py groq_client.py pages tests

## Hoàn tất và báo cáo
Mục tiêu còn lại: app deploy trên Streamlit, BigQuery thật hoạt động, giảng viên truy cập được. Xem DEPLOYMENT.md. Sau khi có URL cần nhắc người dùng chụp output theo REPORT_SCREENSHOTS.md, và kiểm tra ảnh trước khi viết báo cáo. Không báo deployment hoàn tất chỉ vì đã tạo repo. Secrets chỉ do người dùng nhập trực tiếp trên nền tảng, không yêu cầu gửi vào chat.

## Thiết kế đã duyệt

Người dùng chọn sáng kiểu Power BI/Tableau, trắng–navy–teal và câu chuyện phân tích đầy đủ. Nguồn tham khảo Muzli trong DESIGN.md. Giữ 4 trang; thêm hồ sơ từ wide_table nếu có quyền/schema, nối cả hai khóa, loại cặp khóa nguồn trùng. Không đẩy dữ liệu mô phỏng dùng kiểm tra UI vào app.

## Xác nhận triển khai

Người dùng xác nhận phần hồ sơ đã hiển thị sau khi khởi động lại app. Ngày 26/10/2026, người dùng chọn Groq cho tóm tắt số liệu, giải thích biểu đồ và so sánh mô hình; không chọn diễn giải từng bệnh nhân. Key chỉ nhập trong Streamlit Secrets.
