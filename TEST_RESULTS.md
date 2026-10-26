# Kiểm thử giao diện phân tích 0.2.0 — 25/10/2026

- Python 3.12.6, dependency pin trong requirements.txt; Altair 6.3.0 có sẵn từ Streamlit và khai báo trực tiếp.
- 17 unittest/AppTest đạt: schema/SQL tham số, scope, join theo hai khóa và loại key_rows != 1, thiếu metadata/quyền/vùng của bảng tùy chọn, chart spec, 4 trang với có/rỗng, không chọn nhóm, CSV thật, đổi Top K, numeric Top %, credential TOML/JSON, CSV không hợp lệ, lỗi xác thực không lộ chi tiết.
- BigQuery SQL đã được parse theo dialect BigQuery cho schema hồ sơ đầy đủ và từng cột riêng; đây là kiểm tra cú pháp, không phải query live.
- Chrome: kiểm tra 4 trang ở 1440×1100 và 390×844, biểu đồ đã render, bảng đã render canvas, không tràn ngang tài liệu, kiểm tra chọn Top K và nhập mã không hợp lệ. Bản fixture tách biệt trong work/; tổng quan/hồ sơ/bệnh nhân mô phỏng được ghi nhãn. CSV hiệu quả là tệp người dùng thật. Không có fixture trong production.
- Rà soát độc lập tìm thấy một lỗi Top % dạng số, đã sửa f-string và thêm regression test. Rà soát ảnh xác nhận các lỗi đã liệt kê được xử lý: caption opacity=1 (màu #526579 trên trắng, >5:1), table header màu rõ, mobile sidebar thu gọn và logo riêng, số trên trục không dùng scientific notation. Đây không thay cho kiểm thử BigQuery thật.
- Không có credential BigQuery local và không đọc Secrets từ Streamlit. Chưa chạy nối gold.wide_table thật hoặc xác minh coverage trên deployment.
- Không thay đổi cấu hình credential, không tạo khóa, không ghi BigQuery.

## Groq 0.3.0 — 26/10/2026

- Người dùng xác nhận biểu đồ Hồ sơ đã hiển thị sau khi khởi động lại app.
- 25 tests local thành công, gồm 7 tests mới về Groq: whitelist ngữ cảnh không mang cột định danh; payload/model-specific parameters và role boundary; HTTP 401/403/404/429/500 không lộ response/key; validation và lỗi mạng; JSON không hợp lệ/phản hồi bị cắt; không có key thì không gọi API; gửi chat/cooldown/xóa lịch sử khi context đổi.
- Model GPT-OSS dùng include_reasoning=false, không gửi reasoning_format; đã đối chiếu docs riêng của model và sửa sau review độc lập.
- Chrome kiểm tra trạng thái chưa cấu hình key và luồng hội thoại giả lập ở desktop/mobile, clear history và không có exception. Bản sao QA tách biệt với key giả và phản hồi ghi nhãn, không đưa lên production.
- CI được cấu hình chạy Python 3.12 và 3.14 vì log deploy cho thấy Cloud dùng Python 3.14.9.
- Không có key thật trong môi trường trợ lý; chưa gọi API Groq thật hoặc xác nhận phản hồi trên Cloud. Cần chủ app thêm GROQ_API_KEY và thử một câu hỏi theo GROQ_SETUP.md.
