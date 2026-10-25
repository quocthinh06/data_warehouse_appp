# Đưa app lên Streamlit cho giảng viên

## 1. Mã nguồn

Repository dự kiến: quocthinhtb/diabetes-readmission-dashboard, private. Branch main, entrypoint app.py. Chỉ có mã app, CSV chỉ số tổng hợp, tài liệu và tests; không đưa notebook, khóa hay dữ liệu bệnh nhân lên GitHub.

## 2. Việc bạn cần làm trong tài khoản Google Cloud

Mở project diabetes-pipeline-511509 trong Google Cloud Console:

1. IAM & Admin → Service Accounts. Dùng service account riêng cho dashboard chỉ đọc. Nếu chưa có, tạo tài khoản đặt tên dashboard-reader. Không cấp Owner/Editor.
2. Cấp BigQuery Job User trên project diabetes-pipeline-511509.
3. BigQuery → dataset gold → Sharing/Permissions: cấp BigQuery Data Viewer cho đúng email service account (hoặc chỉ trên readmission_prediction nếu thao tác ở mức bảng).
4. Với Streamlit Community Cloud, cần credential service account được đặt trong Secrets. Nếu đã có credential chuyên dụng hợp lệ, dùng credential đó. Nếu chưa có, bạn cần tự tạo JSON key trong Service account → Keys → Add key → Create new key → JSON, nếu chính sách tổ chức cho phép. Trợ lý không tạo hoặc đọc khóa. Không gửi JSON vào chat hoặc upload GitHub. Nếu tổ chức chặn tạo key, báo lại nguyên thông báo đã che thông tin nhạy cảm để chọn cách triển khai phù hợp; không bỏ qua chính sách.
5. Giữ JSON trên máy của bạn ở vị trí ngoài dự án. Chỉ dán nội dung vào giao diện Streamlit Secrets như bước dưới. Không đổi tên khóa thành evaluation_metrics.csv.

## 3. Streamlit Community Cloud

1. Vào https://share.streamlit.io, đăng nhập và kết nối GitHub quocthinhtb; cấp quyền repo private khi Streamlit yêu cầu.
2. Create app → Deploy an app from GitHub. Chọn repository quocthinhtb/diabetes-readmission-dashboard, branch main, Main file path app.py.
3. Advanced settings → Python 3.12.
4. Trong Secrets, dùng đúng định dạng dưới đây. Dán nguyên nội dung file JSON giữa hai dòng dấu nháy đơn ba ký tự. Không thêm dấu #. Không đặt thêm [gcp_service_account] nếu dùng cách này.

```toml
gcp_service_account = '''
DÁN NGUYÊN NỘI DUNG JSON CỦA BẠN TẠI ĐÂY
'''
```

5. Nhấn Deploy, đợi log cài dependencies và app hiện ra. Nếu có lỗi, gửi đoạn log lỗi đã che thông tin nhạy cảm; tuyệt đối không chụp bảng Secrets.
6. Mở từng trang. Trang Hiệu quả mô hình đọc CSV đã đóng gói; 3 trang còn lại phải truy vấn BigQuery được. Không coi chỉ trang metrics chạy là triển khai thành công đầy đủ.
7. Gửi lại URL dạng https://...streamlit.app để trợ lý kiểm tra tiếp. Nếu private chặn truy cập ngoài, gửi ảnh từng trang đã che mã bệnh nhân hoặc thông báo lỗi; không phải mở public chỉ để trợ lý kiểm tra.

## 4. Cho thầy truy cập

Mặc định giữ app private. Trong Settings/Sharing cấu hình email thầy có quyền xem; người xem đăng nhập Google hoặc mã xác nhận qua email theo cơ chế Streamlit. Bạn tự gửi URL và cách đăng nhập cho thầy. Thử bằng phiên trình duyệt khác hoặc nhờ thầy xác nhận. Nếu cần ai có link cũng xem được, trước tiên phải xác nhận phạm vi chia sẻ dữ liệu, và cân nhắc một bản trình diễn đã ẩn định danh; không công khai bảng bệnh nhân một cách mặc định.

Streamlit hiện chỉ cho một private app mỗi tài khoản; nếu đã dùng suất này, báo lại để xử lý, không tự xóa app cũ.

## 5. Xong khi nào?

- URL Streamlit hoạt động.
- Đủ 4 trang, BigQuery thật đọc thành công, CSV khớp.
- Giảng viên có quyền vào xem.
- Bộ ảnh trong REPORT_SCREENSHOTS.md đã chụp từ bản deploy, không từ dữ liệu giả lập.

Trạng thái chưa có credential hoặc URL deploy: chưa hoàn tất deployment. Không lưu secret vào file tiến độ.

Nguồn: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy ; https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management ; https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app
