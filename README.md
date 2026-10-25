# Streamlit Dashboard — Giai đoạn 4

Dashboard tiếng Việt, chỉ đọc từ `diabetes-pipeline-511509.gold.readmission_prediction`. Không dùng Groq, không huấn luyện lại mô hình, không ghi BigQuery. Python 3.12 được dùng để kiểm thử.

## Trạng thái nguồn

Đã có schema qua đoạn chat: `patient_nbr`, `encounter_id`, `risk_score`, `risk_level`, `top_factors`, `recommended_actions`. Trước truy vấn, ứng dụng kiểm tra metadata của bảng. `prediction_date` là cột tùy chọn: nếu có, mặc định lấy đúng timestamp lớn nhất; bỏ chọn để xem mọi đợt. Nếu pipeline ghi timestamp khác nhau cho từng dòng trong cùng đợt, bỏ chọn và cần bổ sung batch_id từ pipeline trước khi dùng lọc đợt. Nếu không có cột này, ứng dụng thông báo đang đọc tất cả dữ liệu. Bảng rỗng được xử lý riêng.

**Đã tích hợp CSV từ D:/download/evaluation_metrics.csv và đối chiếu notebook Huan_luyen_AI_Diabetes.ipynb ở cùng thư mục.** Xem SOURCE_NOTES.md để biết cell nguồn, output và SHA256 notebook. Không chạy lại notebook, không ghi BigQuery. Các biểu đồ Top K dùng CSV thật; AUC và bối cảnh tập kiểm thử trích từ output notebook đã lưu, có ghi nguồn riêng.

Chép CSV thực vào `data/evaluation_metrics.csv` hoặc dùng nút tải CSV ở trang Hiệu quả mô hình. CSV UTF-8, dấu phẩy, có tiêu đề; nhận cả bảng rộng và bảng dài, hiển thị bảng gốc và biểu đồ so sánh cho schema Top K đã xác nhận. Không suy diễn accuracy hoặc dựng đường ROC từ chỉ số tổng hợp. AUC chỉ hiển thị theo output notebook nguồn. Tệp tải lên chỉ dùng trong phiên; không tự lưu xuống ổ đĩa. Giới hạn 5 MB, 10.000 dòng và 100 cột.

Các số 14.304 bệnh nhân, 1.431 cao, 2.860 trung bình, 10.013 thấp và điểm trung bình 0,4732 ngày 25/10/2026 là thông tin đối chiếu từ đoạn chat, **không hardcode làm kết quả dashboard**. Nếu bảng đã có đợt mới, số liệu có thể khác. Phân bố tính theo lượt dự báo; bệnh nhân duy nhất được đếm riêng. Không đặt lại ngưỡng từ các giá trị min/max vì các khoảng có thể trùng sau làm tròn.

## Cấu trúc

- `app.py`: điều hướng bốn trang.
- `pages/overview.py`: số lượt dự báo, số bệnh nhân, điểm trung bình, phân bố nguy cơ.
- `pages/priority.py`: lọc mức nguy cơ, điểm tối thiểu, mã bệnh nhân; 100 bản ghi mỗi trang.
- `pages/explanation.py`: yếu tố và hành động theo lượt khám; không gọi LLM.
- `pages/performance.py`: bảng đánh giá từ CSV, hoạt động cả khi chưa xác thực BigQuery.
- `data.py`: kiểm tra schema, truy vấn có tham số, giới hạn chi phí và timeout.
- `metrics.py`: đọc CSV và tách danh sách theo dấu `|`.
- `.streamlit/secrets.toml.example`: mẫu chú thích, không chứa khóa.
- `tests/test_dashboard.py`: unit tests và Streamlit AppTest dùng BigQuery giả lập.

## Cài đặt và chạy trên Windows PowerShell

```powershell
Set-Location -LiteralPath 'D:\HK7\Nhà kho\Dashboard_warehouse'
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Xác thực local bằng ADC (không cần tạo khóa JSON)

Cài Google Cloud CLI, rồi chạy:

```powershell
gcloud auth application-default login
gcloud auth application-default set-quota-project diabetes-pipeline-511509
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Mở địa chỉ local do Streamlit hiển thị (thường là http://localhost:8501). `gcloud auth login` đơn thuần không thay cho ADC của thư viện Python. Khi dùng quota project, tài khoản có thể cần quyền `serviceusage.services.use` (Service Usage Consumer) trên project này. Không tạo secrets.toml nếu dùng ADC.

Nhờ quản trị viên cấp quyền tối thiểu cho đúng tài khoản đăng nhập hoặc service account:

- BigQuery Job User (`roles/bigquery.jobUser`) trên project thực thi `diabetes-pipeline-511509`.
- BigQuery Data Viewer (`roles/bigquery.dataViewer`) trên bảng hoặc dataset `gold`.

Project cần bật BigQuery API và cấu hình thanh toán thích hợp. Ứng dụng dùng vùng lấy từ metadata của bảng và BigQuery REST, không cần BigQuery Storage API. Giới hạn mỗi query 2 GB được đặt trong `data.py`; nếu vượt, truy vấn dừng. `LIMIT` chỉ giới hạn kết quả, không đảm bảo giảm bytes scan. Phân trang dùng OFFSET, phù hợp quy mô hiện tại khoảng 14 nghìn bản ghi; với bảng lớn hơn nên chuyển sang keyset pagination. Không cache dữ liệu bệnh nhân chung giữa các phiên.

### Lựa chọn service account

Ưu tiên ADC local và danh tính gắn với dịch vụ trên Google Cloud. Nếu nền tảng chỉ hỗ trợ khóa service account, cấu hình mục `[gcp_service_account]` trong kho Secrets của nền tảng theo file example. Cần các trường type, project_id, private_key_id, private_key, client_email, token_uri của tài khoản thật. Khóa PEM phải giữ xuống dòng, dùng TOML multiline string. **Không chép khóa vào mã nguồn, README, CSV hay Git.** Không có khóa nào được tạo bởi dự án này. Không dùng file example còn giá trị mẫu làm secrets thật. Không in secrets hoặc nguyên lỗi Google chứa chi tiết tài khoản lên giao diện.

## Deploy Streamlit Community Cloud

1. Kiểm thử local trước. Đưa mã nguồn vào repository do bạn kiểm soát; xem lại thay đổi để loại mọi khóa và dữ liệu bệnh nhân. Dự án hiện chưa được commit/push.
2. Nếu muốn CSV đánh giá được đóng gói, chỉ đưa CSV chỉ số tổng hợp đã kiểm tra vào repo, tệp data/evaluation_metrics.csv đã được cho phép trong Git; các CSV khác vẫn bị bỏ qua. Không đưa CSV cấp bệnh nhân lên repo. Hoặc tải CSV tại giao diện mỗi phiên.
3. Trên Community Cloud tạo app từ repository, chọn `app.py`, Python 3.12, cài bằng `requirements.txt`.
4. Trong Advanced settings / Secrets, cấu hình `[gcp_service_account]` bằng thông tin thật. Không upload file khóa vào repository. Đảm bảo service account có hai quyền BigQuery ở trên.
5. Cấu hình quyền xem app riêng tư và kiểm tra bằng tài khoản người xem trước khi sử dụng. Không triển khai dashboard bệnh nhân dưới chế độ công khai. Phiên bản này không có hệ thống đăng nhập trong ứng dụng hoặc phân quyền từng bệnh nhân; cần lớp kiểm soát truy cập của nền tảng. Nếu gói nền tảng không cung cấp kiểm soát phù hợp, dùng môi trường tổ chức có xác thực thay thế.
6. Kiểm tra đủ bốn trang, bộ lọc, trường hợp rỗng, CSV và số liệu đối chiếu; kiểm tra Cloud Billing sau lần chạy đầu. Chưa có deploy nào được thực hiện.

## Kiểm thử

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall -q app.py data.py metrics.py pages tests
```

Tests dùng dữ liệu tổng hợp rõ ràng trong bộ nhớ; không gọi BigQuery, không dùng dữ liệu bệnh nhân thật và không ghi vào bảng. Kiểm thử giao diện bằng Streamlit AppTest không thay thế kiểm tra trình duyệt thực tế. Đã đối chiếu công thức và output notebook Giai đoạn 3; chưa xác minh BigQuery thật hoặc deploy.

## Khi gặp lỗi

- Chưa đọc được BigQuery: kiểm tra ADC, email đang đăng nhập, BigQuery API, tên bảng, quyền metadata và quyền đọc. Không gửi khóa trong chat.
- Truy vấn không hoàn tất: kiểm tra Billing, vùng dataset, quyền Job User, kiểu cột (risk_score phải là số), chi phí ước lượng trong BigQuery Console. Thông báo UI cố ý không hiển thị raw exception.
- Thiếu cột: đối chiếu notebook Giai đoạn 3 và schema thực tế; không tự đổi tên cột chưa xác nhận.
- Rỗng: kiểm tra bộ lọc, số trang và lựa chọn đợt mới nhất.
- CSV không đọc được: dùng UTF-8, dấu phẩy và có hàng tiêu đề; tránh file Excel đổi đuôi thành CSV.

## Tài liệu chính thức

- [Xác thực BigQuery và ADC](https://docs.cloud.google.com/bigquery/docs/authentication)
- [Quyền BigQuery](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery)
- [Kết nối Streamlit với BigQuery](https://docs.streamlit.io/develop/tutorials/databases/bigquery)
- [Quản lý secrets khi triển khai](https://docs.streamlit.io/deploy/concepts/secrets)

## Chép sang máy khác

Bản ZIP đi kèm chứa mã nguồn, ví dụ cấu hình và hướng dẫn, không chứa khóa. Giải nén thư mục `Dashboard_warehouse` vào `D:\HK7\Nhà kho`, sau đó tạo môi trường và xác thực như trên. Không sao chép .venv giữa các máy.

## Đối chiếu CSV đã nhận

XGBoost (đề xuất), Top 10%: K=1.430, Precision@K=17,27%, Recall@K=19,62%, Lift=1,9624. K=1.430 trong CSV khác 1.431 bản ghi mức Cao ở BigQuery đã báo trong chat. Dashboard giữ nguyên hai nguồn; chưa thể coi chúng là cùng tập ưu tiên do notebook dùng round(n*pct) cho Top K và quantile cho phân tầng nguy cơ.

## Triển khai và báo cáo

Xem [DEPLOYMENT.md](DEPLOYMENT.md) cho các bước thao tác tài khoản và [REPORT_SCREENSHOTS.md](REPORT_SCREENSHOTS.md) cho danh sách ảnh cần chụp sau khi app chạy trên Cloud.
