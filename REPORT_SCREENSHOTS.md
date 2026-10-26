# Ảnh output cho báo cáo Giai đoạn 4

Chụp sau khi app đã deploy và kết nối BigQuery thật. Dùng cửa sổ rộng khoảng 1440 px, zoom 100%, giữ tên trang/bộ lọc và URL Streamlit nếu thuận tiện. Dùng Win+Shift+S; lưu PNG. Không chụp Secrets, JSON key, token, thông tin Billing hoặc email cá nhân. Che mã bệnh nhân/lượt khám khi đưa vào báo cáo chia sẻ công khai.

| Tên ảnh | Thao tác và nội dung | Chú thích gợi ý |
|---|---|---|
| Hinh_4_1_Tong_quan.png | Mở Tổng quan: số lượt, bệnh nhân, điểm trung bình và ngày mới nhất | Dashboard tổng quan dự báo nguy cơ tái nhập viện từ tầng Gold của BigQuery. |
| Hinh_4_2_Phan_bo_nguy_co.png | Chụp biểu đồ và bảng Cao/Trung bình/Thấp | Phân bố nhóm nguy cơ theo ngưỡng phân vị đã tính tại Giai đoạn 3. |
| Hinh_4_3_Benh_nhan_uu_tien.png | Mở Bệnh nhân ưu tiên, chọn Cao, trang 1, hiện thứ tự điểm giảm dần | Danh sách ưu tiên hỗ trợ theo dõi sau xuất viện; giữ nguyên phân tầng từ pipeline. |
| Hinh_4_4_Bo_loc.png | Đổi mức nguy cơ/điểm tối thiểu hoặc tra mã bệnh nhân; chụp cả bộ lọc và kết quả | Bộ lọc cho phép thu hẹp danh sách theo mức nguy cơ và điểm dự báo. |
| Hinh_4_5_Giai_thich_AI.png | Chọn một lượt khám, hiện điểm, top_factors và recommended_actions | Giải thích bằng các yếu tố SHAP dương đã lưu và hành động ánh xạ theo quy tắc. Không có giá trị SHAP cụ thể trong bảng. |
| Hinh_4_6_Hieu_qua_Top10.png | Chọn Top 10%, chụp hai biểu đồ và bảng so sánh | So sánh Precision@K, Recall@K của XGBoost, Logistic Regression và xếp hạng ngẫu nhiên tại K=1.430. |
| Hinh_4_7_Hieu_qua_day_du.png | Chụp bảng đủ 9 dòng và bối cảnh notebook/AUC | Kết quả đánh giá mô hình tại Top 5%, 10%, 20% trên tập kiểm thử. |
| Hinh_4_8_Deploy.png | Chụp app hoạt động trên URL streamlit.app, không mở Secrets/log nhạy cảm | Ứng dụng Giai đoạn 4 được triển khai lên Streamlit Community Cloud để giảng viên truy cập. |
| Hinh_4_9_Doi_chieu_BigQuery.png | Trong BigQuery Console, chạy SQL dưới, chỉ chụp kết quả tổng hợp | Đối chiếu số liệu dashboard với bảng gold.readmission_prediction. |

```sql
SELECT COUNT(*) total_predictions,
       COUNT(DISTINCT patient_nbr) unique_patients,
       COUNTIF(risk_level = 'Cao') high_risk,
       COUNTIF(risk_level = 'Trung bình') medium_risk,
       COUNTIF(risk_level = 'Thấp') low_risk,
       ROUND(AVG(risk_score), 4) avg_risk_score,
       MAX(prediction_date) latest_prediction_date
FROM `diabetes-pipeline-511509.gold.readmission_prediction`
WHERE prediction_date = (
  SELECT MAX(prediction_date)
  FROM `diabetes-pipeline-511509.gold.readmission_prediction`
);
```

Nếu nguồn chưa đổi từ ngày 25/10/2026, có thể đối chiếu 14.304 lượt/bệnh nhân, Cao=1.431, Trung bình=2.860, Thấp=10.013, trung bình 0,4732. Nếu đợt mới thay thế bảng, ghi ngày mới và dùng số thật; không sửa app để khớp số cũ.

Diễn giải đúng: XGBoost Top 10% có Precision@K≈17,27%, Recall@K≈19,62%, Lift≈1,96. Nghĩa là ưu tiên 1.430 người bắt được khoảng 19,62% ca dương của tập test. Không gọi 17,27% là accuracy. Cao=1.431 do quy tắc phân vị, khác Top K cố định. Dashboard không chứng minh can thiệp làm giảm tái nhập viện.

Sau khi bạn gửi URL deploy, trợ lý cần nhắc lại danh sách ảnh này và cùng kiểm tra các output trước khi viết phần báo cáo. Nếu thầy chưa truy cập được, bước bàn giao chưa hoàn thành.

## Bổ sung cho giao diện phân tích 0.2.0

- Hinh_4_10_Dashboard_phan_tich.png: Tổng quan với thanh lọc, 4 KPI, donut và histogram trong cùng khung hình.
- Hinh_4_11_Yeu_to_pho_bien.png: biểu đồ tần suất yếu tố; chú thích rõ đây là số lượt xuất hiện, không phải độ lớn SHAP.
- Hinh_4_12_Ho_so_benh_nhan.png: tỷ lệ nối thành công và biểu đồ tuổi/giới tính từ wide_table. Chỉ chụp khi dữ liệu thật đã nối thành công; không dùng ảnh mô phỏng kiểm thử thay kết quả.
- Hinh_4_13_Lich_su_nhap_vien.png: số lần nhập viện trước và thời gian nằm viện; chụp cả lựa chọn Số lượt/Tỷ trọng nguy cơ.
- Hinh_4_14_So_sanh_Precision_Recall_Lift.png: Top 10%, 4 KPI và 3 biểu đồ ngang trên trang hiệu quả.

Các ảnh có nhãn MÔ PHỎNG KIỂM THỬ chỉ phục vụ duyệt giao diện, không đưa vào phần kết quả thực nghiệm. Sau khi Streamlit cập nhật, dùng URL deploy đã cung cấp để chụp output thực.

## Trợ lý AI Groq 0.3.0

- Hinh_4_15_Groq_nguon_du_lieu.png: mở Trợ lý AI, bung Nguồn và phạm vi dữ liệu gửi cho AI; chụp số tổng hợp và bộ lọc, không chụp Secrets.
- Hinh_4_16_Groq_so_sanh_mo_hinh.png: câu hỏi so sánh Top 10% và phản hồi Groq thật; kiểm tra K/Precision/Recall/Lift khớp CSV trước khi đưa vào báo cáo.
- Hinh_4_17_Groq_tom_tat_dashboard.png: câu hỏi tóm tắt phạm vi đang xem và phản hồi có dẫn nguồn BigQuery; chụp cả nhãn phạm vi để tránh dùng nhầm số liệu.
- Hinh_4_18_Groq_gioi_han.png (tùy chọn): câu hỏi yêu cầu chỉ số không có (ví dụ ma trận nhầm lẫn) để minh họa trợ lý nhận thiếu dữ liệu. Không coi một ví dụ là bằng chứng AI luôn chính xác.

Chỉ chụp sau khi API trả lời thật. Phản hồi mock trong kiểm thử không phải output Groq thực tế.
