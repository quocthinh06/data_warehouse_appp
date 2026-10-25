# Dashboard redesign — 25/10/2026

## Confirmed brief

Người xem chính: giảng viên và nhóm thực hiện bài tập. Người dùng chọn light Power BI/Tableau, navy–teal; ưu tiên câu chuyện phân tích đầy đủ và mở rộng hồ sơ khi Gold có trường phù hợp. Link Muzli là nguồn tham khảo tổng thể, không chọn một ảnh cụ thể. Giữ 4 trang là quyết định triển khai để giữ đường dẫn hiện có, Tổng quan trở thành dashboard phân tích chính.

## Direction contract

THESIS: Đọc và giải thích nguy cơ trước khi mở danh sách từng bệnh nhân; thay bố cục form dài bằng dashboard phân tích có thứ tự.
OWN-WORLD: Sidebar navy, nền xám xanh sáng, panel trắng và accent teal; màu nguy cơ nhất quán; sans serif vận hành.
STORY: Quy mô dự báo → cơ cấu/điểm → yếu tố/hồ sơ → lượt cần theo dõi → chất lượng lựa chọn của mô hình.
FIRST VIEWPORT: Tiêu đề, thanh lọc ngang, dải bốn KPI; donut và histogram theo tỷ lệ 1:1,65. Các link đi vào danh sách và đánh giá ở phần nhận xét.
FORM: Dashboard lưới theo dữ liệu, bốn trang hiện có; dựng trực tiếp bằng Streamlit để kiểm tra đúng giới hạn layout và dữ liệu.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

## Verification boundary

Không có credential BigQuery local. Kiểm thử giao diện dùng bản sao tách biệt trong work/ với dữ liệu mô phỏng ghi nhãn; bản production không có chế độ dữ liệu giả. CSV đánh giá là tệp thật. Cần kiểm tra wide_table và coverage trên deployment sau khi cập nhật; không lấy khóa từ Streamlit.
