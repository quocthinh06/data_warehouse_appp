# Changelog

## 0.3.0 — 2026-10-26

- Thêm Trợ lý AI dùng Groq để hỏi đáp số liệu tổng hợp, diễn giải biểu đồ và so sánh mô hình.
- Ngữ cảnh whitelist từ Tổng quan và CSV gốc, không lấy mã bệnh nhân/lượt khám; có nguồn và phạm vi bộ lọc.
- Khóa chỉ ở Secrets/env; xử lý thiếu key, lỗi mạng, giới hạn lượt gọi và phản hồi sai định dạng. Không gọi API tự động hoặc chạy SQL do AI tạo.
- Người dùng đã xác nhận phần hồ sơ hiển thị sau khi khởi động lại app.

## 0.2.0 — 2026-10-25

- Thiết kế lại giao diện sáng navy–teal, sidebar, bộ lọc và bảng đọc số liệu.
- Thêm donut, histogram điểm nguy cơ, tần suất yếu tố và ba biểu đồ Precision/Recall/Lift.
- Thêm phân tích tuổi, giới tính, số lần nhập viện và số ngày nằm viện khi gold.wide_table có dữ liệu và quyền truy cập.
- Nối theo hai khóa và chỉ dùng bản ghi nguồn duy nhất, hiển thị coverage; thiếu dữ liệu tùy chọn không chặn dashboard chính.
- Bổ sung kiểm thử query/biểu đồ và hướng dẫn ảnh báo cáo.

## 0.1.0 — 2026-10-25

- Dashboard Streamlit bốn trang đọc gold.readmission_prediction.
- Đánh giá Top K từ CSV thật, biểu đồ Precision/Recall và AUC trích notebook.
- Xác thực ADC local hoặc service account qua Secrets, không chứa khóa.
- Kiểm thử tự động, hướng dẫn deploy và checklist output báo cáo.
