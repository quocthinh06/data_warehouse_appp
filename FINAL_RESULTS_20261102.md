# Bộ kết quả cuối Giai đoạn 4 ngày 02/11/2026

## Kết quả đã đối chiếu từ ZIP

| Nội dung | Giá trị cuối |
|---|---|
| Train / validation / test | 45.771 / 11.443 / 14.304 (64% / 16% / 20%) |
| Nhãn dương tập test | 1.259, readmitted = <30 |
| ROC-AUC XGB / LR | 0,6229 / 0,6177 |
| Average precision XGB / LR | 0,1456 / 0,1412 |
| XGB Top10 | K=1.430; Precision=16,9930%; Recall=19,3010%; Lift=1,9306; 243 ca |
| LR Top10 | K=1.430; Precision=16,8531%; Recall=19,1422%; Lift=1,9148; 241 ca |
| Chênh số ca Top10 | 2 ca, tăng Precision khoảng0,14 điểm phần trăm, Recall khoảng0,16 điểm phần trăm |
| CSV dự báo | 14.304 dòng / bệnh nhân duy nhất |
| Nhóm Cao / Trung bình / Thấp | 1.431 / 2.860 / 10.013 |
| Điểm trung bình / min / max | 0,4541 / 0,0534 / 0,9158 |
| prediction_date | 2026-11-02 |

Ngưỡng nguy cơ theo phân vị trên điểm chưa làm tròn. Không phân loại lại từ min/max đã làm tròn. K=1430 và nhóm Cao1431 dùng cách chọn khác nhau.

## Nghiệm thu trên web

1. Tổng quan: ngày2026-11-02, điểmTB0,4541, 14304 bệnh nhân,1431Cao. Đây là mốc từ CSV ZIP; nếu app khác, gửi ảnh để kiểm tra bảng live, không sửa số hiển thị thủ công.
2. Hiệu quả: Top10 hiện Precision16,99%, Recall19,30%, Lift1,93; train45771/val11443; AUC0,6229.
3. Mở Tổng quan trước, rồi Trợ lý AI; ngữ cảnh có bộ đánh giá02/11 và64/16/20. Hỏi lại so sánhTop10; đối chiếu 243ca và241ca. Không sử dụng ảnh hội thoại cũ247/239.
4. Chụp lại dashboard/biểu đồ hồ sơ và yếu tố/bệnh nhân/giải thích/hiệu quả/hội thoại từ app thật. Hình cấu trúcGitHub/cấu hình kết nối không đổi thì có thể giữ.
5. Mở cửa sổ ẩn danh để xác nhận quyền truy cập giảng viên; không chụp Secrets.

Chủ app đã xác nhận trên Tổng quan: ngày 2026-11-02 và điểm trung bình 0,4541, khớp bộ cuối.

## Giới hạn xác minh

Notebook cells21/31 lưu output đã ghi14304dòng BigQuery; không đồng nghĩa đã kiểm tra trạng thái hiện tại bằng truy vấn live. Chưa gọiGroq thật với ngữ cảnh mới. Lỗi diễn giải và định dạng trong phản hồiGroq cũ chưa được sửa bởi việc thayCSV; không khẳng định mọi phản hồi mới đúng.
