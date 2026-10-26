# Readmission AI · Diabetes Analytics

Người dùng đã chọn giao diện sáng kiểu Power BI/Tableau, trắng và navy–teal, ưu tiên câu chuyện dữ liệu → nguy cơ → bệnh nhân → hiệu quả AI. Nguồn cảm hứng: https://muz.li/blog/best-dashboard-design-examples-inspirations-for-2026/ . Giữ 4 trang Streamlit; Tổng quan là dashboard chính. Bố cục phục vụ demo trên laptop và chụp báo cáo.

## Tokens

- Nền trang #F3F6FA, panel #FFFFFF, chữ chính/sidebar #142D4E.
- Teal #087F83 cho biểu đồ và tương tác; chữ phụ #526579; đường phân cách #E2E9F0.
- Nhóm Cao #C55349, Trung bình #B17A20, Thấp #138A83; luôn có nhãn chữ và tooltip.
- Font sans serif theo Streamlit/platform, tiêu đề 32px, nhãn 13–15px, số liệu dùng tabular numerals.
- Panel radius 12px, viền 1px, không shadow trang trí. KPI là một dải thống nhất, không bốn khối rời.
- Mobile 390px: KPI 2×2; cột biểu đồ chuyển dọc, sidebar gập; bảng cuộn bên trong.

## Thành phần và thứ tự

Logo SVG riêng trước menu; icon Material cùng hệ. Bộ lọc ở thanh trắng ngay dưới tiêu đề, sau đó KPI, donut/histogram, tần suất yếu tố và liên kết hành động. Hồ sơ bệnh nhân nằm dưới với báo cáo tỷ lệ nối, tùy chọn số lượng/tỷ trọng và bốn biểu đồ. Trang bệnh nhân dùng bảng có progress cho điểm và nhãn tiếng Việt. Trang giải thích tách yếu tố với hành động; không bịa SHAP waterfall. Trang hiệu quả có KPI thật từ CSV và ba biểu đồ so sánh ngang.

## Dữ liệu và trạng thái

Không đặt nội dung kỹ thuật dài ở đầu dashboard. Lỗi, rỗng, thiếu bảng tùy chọn có hướng dẫn phục hồi. SQL lấy số liệu tổng hợp; không đưa identifier vào biểu đồ. Chỉ kết quả nối duy nhất trên cặp patient_nbr/encounter_id mới được dùng cho hồ sơ; báo riêng không khớp và khóa trùng. Không dựng dữ liệu thay thế trong app khi thiếu quyền.

## Trợ lý AI (0.3.0)

Trang thứ năm kế thừa hệ màu và typography hiện có, dùng chat native Streamlit. Luôn thấy nguồn và phạm vi, nút về Tổng quan để nạp lại, nút xóa hội thoại; key thiếu thì khóa input và chỉ dẫn cho chủ app. Thông báo dữ liệu được gửi Groq đặt trước input. Không tự tạo câu trả lời khi API chưa được cấu hình.
