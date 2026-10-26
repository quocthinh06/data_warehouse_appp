# Đánh giá giao diện 0.3.1

Đã xử lý: điều khiển Biểu đồ / Dữ liệu rõ ràng trên từng biểu đồ; nút quay lại Tổng quan và danh sách bệnh nhân; bỏ giới thiệu dài ở sidebar; tên Diabetes Insight phù hợp chủ đề. Năm trang chạy trong kiểm tra local, desktop và mobile không tràn ngang.

Mức hoàn thiện: đủ luồng chức năng cho demo sau khi kiểm tra dữ liệu và truy cập thật. Chưa thể xác nhận toàn bộ bản deploy từ môi trường kiểm thử.

Cần nghiệm thu trên app thật:
1. Mở cửa sổ ẩn danh để kiểm tra giảng viên truy cập được.
2. Tổng quan có dữ liệu BigQuery và hồ sơ; chuyển Biểu đồ / Dữ liệu rồi quay lại, giữ bộ lọc.
3. Trợ lý AI trả lời bằng Groq thật và đối chiếu số liệu CSV; nếu thiếu key, chủ app nhập trực tiếp Streamlit Secrets.
4. Chụp bộ output theo REPORT_SCREENSHOTS.md, gồm hai chế độ của cùng biểu đồ.

Giới hạn còn lại: trang Bệnh nhân ưu tiên và Giải thích AI dùng bộ lọc riêng; khi chuyển trang cần chọn lại lượt khám. Không có SHAP dạng số nên chỉ giải thích tên yếu tố. LLM có thể diễn giải sai, phải đối chiếu nguồn trước khi đưa vào báo cáo.
