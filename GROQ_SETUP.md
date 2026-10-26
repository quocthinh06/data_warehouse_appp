# Thiết lập Trợ lý AI Groq

## Phạm vi đã thống nhất

Trợ lý hỏi đáp dashboard: tóm tắt số liệu tổng hợp, giải thích biểu đồ và so sánh mô hình. Không tra cứu hoặc diễn giải từng bệnh nhân. Bốn trang phân tích giữ nguyên; thêm trang Trợ lý AI.

Mô hình hiện dùng: openai/gpt-oss-120b qua https://api.groq.com/openai/v1/chat/completions. Gọi trực tiếp bằng thư viện chuẩn Python, không cần cài SDK mới. Mỗi lần gửi tối đa 1.500 ký tự câu hỏi, ngữ cảnh tối đa 24.000 ký tự, lịch sử gửi tối đa 4 tin nhắn gần nhất, timeout 30 giây và giới hạn 2.048 completion tokens; không tự retry để tránh nhân đôi lượt gọi. Chờ ít nhất 15 giây giữa hai yêu cầu trong cùng phiên. Giới hạn toàn tài khoản do Groq quản lý; app có thông báo khi nhận HTTP 429.

## Việc chủ app cần làm

1. Vào https://console.groq.com/keys , đăng nhập Groq, tạo API key riêng cho dashboard. Không gửi key cho trợ lý và không upload lên GitHub.
2. Vào https://share.streamlit.io → dấu ba chấm cạnh app → Settings → Secrets.
3. Giữ nguyên credential BigQuery hiện có. Thêm dòng sau ở ĐẦU Secrets, trước bất kỳ tiêu đề [gcp_service_account] hoặc [table] nào:

```toml
GROQ_API_KEY = "DÁN_KEY_THẬT_TRỰC_TIẾP_TẠI_STREAMLIT"
```

4. Nhấn Save, đợi app cập nhật; nếu chưa có trang Trợ lý AI hoặc sidebar chưa ghi 0.3.0, dùng Reboot app. Không xóa app hoặc credential BigQuery.
5. Mở Tổng quan, chọn bộ lọc và đợi dữ liệu/biểu đồ hoàn tất. Mở Trợ lý AI; xem expander Nguồn và phạm vi dữ liệu gửi cho AI để kiểm tra ảnh chụp ngữ cảnh.
6. Gửi: “Ở Top 10%, so sánh XGBoost với Logistic Regression và giải thích Precision@K, Recall@K, Lift.”
7. Đối chiếu với CSV: XGBoost K=1.430, Precision≈17,27%, Recall≈19,62%, Lift≈1,96. Đây là chỉ số tập test gốc, không phải chỉ số tính lại theo bộ lọc Tổng quan.
8. Gửi thêm câu hỏi: “Tóm tắt nhóm nguy cơ trong phạm vi đang xem và nêu giới hạn.” Kiểm tra số trích dẫn khớp ngữ cảnh nguồn.
9. Báo “Groq đã trả lời” hoặc gửi thông báo lỗi đã che thông tin nhạy cảm. Không chụp Secrets hoặc API key.

Local: dùng biến môi trường GROQ_API_KEY hoặc key trong .streamlit/secrets.toml (bị gitignore). Không cần tạo file secrets để dùng Cloud.

## Dữ liệu nào được gửi?

- Ngữ cảnh: số lượt, số bệnh nhân duy nhất, điểm trung bình, phân bố nguy cơ và tần suất yếu tố từ lần xem Tổng quan gần nhất. Khi hồ sơ được nạp, có thêm các nhóm tuổi/giới tính/lịch sử nhập viện đã tổng hợp và coverage.
- Phạm vi: mức nguy cơ, điểm tối thiểu, lựa chọn đợt mới nhất và ngày dự báo. Đổi số liệu/ngữ cảnh sẽ xóa lịch sử để tránh trộn hai phạm vi.
- CSV gốc data/evaluation_metrics.csv và ghi chú phương pháp từ notebook đã đối chiếu. Không tự dùng CSV người xem tải riêng trên trang Hiệu quả.
- Chính câu hỏi người dùng và tối đa 4 tin nhắn gần nhất. Không nhập thông tin cá nhân trong câu hỏi.
- Không tự gửi bảng bệnh nhân, patient_nbr, encounter_id, credential Google, API key, hoặc toàn bộ notebook. API key chỉ đi trong header Authorization tới Groq, không đưa vào prompt.

Hội thoại chỉ nằm trong session Streamlit; không ghi vào BigQuery, file hoặc cache dùng chung. Người dùng có nút Xóa hội thoại. Groq vẫn xử lý dữ liệu theo chính sách của dịch vụ; không khẳng định dữ liệu không được lưu ở phía nhà cung cấp.

## Kiểm thử và giới hạn

Tests mô phỏng HTTP và UI, không gọi Groq thật hoặc dùng API key thật. Khi thiếu key, input bị vô hiệu hóa nhưng dashboard vẫn chạy. Lỗi 401 yêu cầu kiểm tra key; 403/404 kiểm tra model/quyền; 429 chờ và xem Limits; lỗi mạng hoặc phản hồi sai có thông báo phục hồi. Không hiển thị raw response lỗi hoặc header.

AI có thể nhầm số hoặc diễn giải. Prompt yêu cầu nêu nguồn, nhận thiếu dữ liệu và phân biệt forecast với đánh giá, nhưng đây không phải bảo đảm máy móc về tính đúng của mọi câu trả lời. Cần đối chiếu trước khi đưa vào báo cáo. Không có truy cập web, tool calling, SQL execution, kê đơn hay thay đổi dự báo.

Nguồn chính thức: https://console.groq.com/docs/model/openai/gpt-oss-120b ; https://console.groq.com/docs/api-reference ; https://console.groq.com/docs/errors ; https://console.groq.com/docs/rate-limits . Kiểm tra ngày 26/10/2026.
