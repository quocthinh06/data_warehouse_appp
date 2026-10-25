# Kiểm thử ngày 25/10/2026

- Windows, Python 3.12.6; các dependency được pin trong requirements.txt.
- 10 unittest/AppTest thành công: phạm vi đợt; SQL tham số/phân trang; đọc CSV và tách yếu tố; Tổng quan; hai trang bệnh nhân với có/rỗng; thiếu CSV; CSV thật và đổi Top K; lỗi xác thực không lộ chi tiết; định dạng credential TOML/JSON; từ chối chỉ số không hợp lệ/trùng tổ hợp.
- Đã đối chiếu notebook Giai đoạn 3, công thức và output: SOURCE_NOTES.md.
- Đã kiểm tra Streamlit khởi động local và trả HTTP health 200.
- Kiểm tra Chrome thực tế: điều hướng trang Hiệu quả mô hình, đổi Top 10% sang 5%, kiểm tra không có exception, chụp desktop/mobile với CSV thực. Ba trang dùng BigQuery chưa có credential nên chỉ kiểm tra giao diện lỗi xác thực; dữ liệu bệnh nhân trong AppTest là tổng hợp.
- Chưa xác minh truy cập BigQuery thật, deployment Streamlit Cloud hoặc quyền truy cập giảng viên.
- GitHub Actions sẽ chạy lại 10 tests trên Linux/Python 3.12 khi push, không dùng credential.
- Không tạo hoặc commit khóa bí mật; notebook không nằm trong repository.
