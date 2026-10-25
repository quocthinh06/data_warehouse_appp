# Đưa app lên Streamlit cho giảng viên

## 1. Mã nguồn

Repository đích: quocthinh06/data_warehouse_appp, public. Branch main, entrypoint app.py. Chỉ có mã app, CSV chỉ số tổng hợp, tài liệu và tests; không đưa notebook, khóa hay dữ liệu bệnh nhân lên GitHub.

## 2. Việc bạn cần làm trong tài khoản Google Cloud

Mở project diabetes-pipeline-511509 trong Google Cloud Console:

1. IAM & Admin → Service Accounts. Dùng service account riêng cho dashboard chỉ đọc. Nếu chưa có, tạo tài khoản đặt tên dashboard-reader. Không cấp Owner/Editor.
2. Cấp BigQuery Job User trên project diabetes-pipeline-511509.
3. BigQuery → dataset gold → Sharing/Permissions: cấp BigQuery Data Viewer cho đúng email service account (hoặc chỉ trên readmission_prediction nếu thao tác ở mức bảng).
4. Với Streamlit Community Cloud, cần credential service account được đặt trong Secrets. Nếu đã có credential chuyên dụng hợp lệ, dùng credential đó. Nếu chưa có, bạn cần tự tạo JSON key trong Service account → Keys → Add key → Create new key → JSON, nếu chính sách tổ chức cho phép. Trợ lý không tạo hoặc đọc khóa. Không gửi JSON vào chat hoặc upload GitHub. Nếu tổ chức chặn tạo key, báo lại nguyên thông báo đã che thông tin nhạy cảm để chọn cách triển khai phù hợp; không bỏ qua chính sách.
5. Giữ JSON trên máy của bạn ở vị trí ngoài dự án. Chỉ dán nội dung vào giao diện Streamlit Secrets như bước dưới. Không đổi tên khóa thành evaluation_metrics.csv.

## 3. Streamlit Community Cloud — từng bước

Repository đang public. Để kiểm soát người xem trước khi kết nối dữ liệu, triển khai lần đầu không nhập Secrets, chuyển app sang private, rồi mới thêm credential.

1. Vào https://share.streamlit.io, kiểm tra GitHub kết nối là quocthinh06. Nếu đang ở workspace quocthinhtb, đổi workspace/tài khoản trước.
2. Create app → Deploy an app from GitHub.
3. Repository: quocthinh06/data_warehouse_appp; branch: main; Main file path: app.py.
4. Nếu không thấy repo, dùng URL repository và kiểm tra kết nối GitHub. Không tạo repo khác.
5. Advanced settings → Python 3.12. Chưa nhập Secrets. Save rồi Deploy.
6. App khởi động có thể báo chưa đọc được BigQuery; đây là trạng thái dự kiến trước xác thực. Trang Hiệu quả mô hình vẫn dùng CSV trong repository.
7. Trong workspace, mở menu dấu ba chấm cạnh app → Settings → Sharing. Chọn chế độ private/giới hạn người xem (tên nhãn có thể thay đổi). Nếu đã hết suất private app, dừng trước bước thêm credential và báo trợ lý; không xóa app cũ.
8. Trong Settings → Secrets, nhập đúng ba phần sau. Thay dòng giữa bằng nguyên nội dung file JSON, từ dấu { đầu tiên đến dấu } cuối cùng; giữ nguyên các ký tự \n trong private_key. Không thay bằng email, tên file hoặc đường dẫn file.

```toml
gcp_service_account = '''
DÁN NGUYÊN NỘI DUNG JSON CỦA BẠN TẠI ĐÂY
'''
```

9. Không thêm [gcp_service_account] khi dùng cách chuỗi JSON này. Nhấn Save, đợi app khởi động lại; nếu cần dùng menu Reboot app/Rerun.
10. Mở Tổng quan, Bệnh nhân ưu tiên, Giải thích AI và Hiệu quả mô hình. Ba trang đầu phải đọc BigQuery thật; trang thứ tư phải có CSV và biểu đồ. Không coi chỉ trang metrics chạy là triển khai đầy đủ.
11. Gửi lại URL https://...streamlit.app để trợ lý kiểm tra tiếp. Nếu app private, không mở public chỉ để trợ lý kiểm tra: gửi ảnh từng trang đã che mã hoặc thông báo lỗi. Không chụp Secrets.

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

## Trạng thái GitHub đã xác minh

GitHub CLI đã đăng nhập quocthinh06, quyền ADMIN trên quocthinh06/data_warehouse_appp. Repository này là đích origin/main. Repository cũ giữ nguyên và không còn là đích push mặc định. Không cần chạy lại đăng nhập GitHub.

## 6. Chi tiết thao tác Google Cloud cho người mới

### Tạo service account và cấp quyền chạy query

1. Vào https://console.cloud.google.com/iam-admin/serviceaccounts?project=diabetes-pipeline-511509 . Kiểm tra project đúng ở thanh trên.
2. Nếu đã có service account riêng cho dashboard với đủ quyền, dùng lại và không tạo thêm key không cần thiết.
3. Nếu chưa có, chọn Create service account. Name/ID: dashboard-reader; mô tả: Streamlit read-only dashboard. Create and continue.
4. Ở Grant this service account access to project, chọn role BigQuery Job User. Continue.
5. Phần cấp người dùng quyền trên service account có thể bỏ trống; Done. Không cần Owner/Editor.
6. Mở tài khoản vừa tạo, sao chép email chính xác được hiển thị.

### Cấp quyền đọc dataset gold

1. Vào https://console.cloud.google.com/bigquery?project=diabetes-pipeline-511509 .
2. Trong Explorer mở project diabetes-pipeline-511509, nhấn dataset gold (không phải project).
3. Sharing → Permissions → Add principal/Grant access. Dán email service account vừa sao chép vào New principals.
4. Chọn role BigQuery Data Viewer → Save. Nếu bảng readmission_prediction không có trong gold, chụp Explorer báo lại, không tạo bảng rỗng thay thế.

### Tạo credential để nhập trực tiếp vào Streamlit

1. Quay lại Service Accounts, nhấn email của tài khoản dashboard → Keys.
2. Nếu đã có JSON key chuyên dụng hợp lệ trên máy, dùng lại. Không thể tải lại private key đã tạo nếu file bị mất.
3. Nếu cần key mới: Add key → Create new key → JSON → Create. Trình duyệt tải file JSON xuống.
4. Giữ file ngoài thư mục dự án. Mở bằng Notepad trên máy của bạn để sao chép vào Settings → Secrets trên Streamlit. Trợ lý không đọc hoặc tạo key.
5. Nếu báo Service account key creation is disabled hoặc thiếu quyền, gửi thông báo lỗi đã che thông tin nhạy cảm; không tự bỏ chính sách tổ chức.

Hoàn tất bước nào bạn có thể báo lại tên bước; chỉ gửi URL và ảnh thông báo, không gửi JSON key.
