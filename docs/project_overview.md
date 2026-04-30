# Project Overview — Customer Segmentation using RFM + K-means

## 1. Tên dự án

**Customer Segmentation using RFM + K-means**

Dự án xây dựng một hệ thống phân khúc khách hàng dựa trên dữ liệu giao dịch lịch sử. Hệ thống cho phép người dùng upload file giao dịch thô, sau đó tự động làm sạch dữ liệu, tính toán RFM, huấn luyện mô hình K-means, phân nhóm khách hàng và hiển thị insight trên giao diện Streamlit.

---

## 2. Bối cảnh bài toán

Trong thực tế, doanh nghiệp thường có rất nhiều khách hàng với hành vi mua sắm khác nhau:

- Có khách mua thường xuyên và chi tiêu cao.
- Có khách mới mua lần đầu.
- Có khách từng mua nhiều nhưng lâu rồi chưa quay lại.
- Có khách mua ít, giá trị thấp.
- Có khách cần được chăm sóc VIP.
- Có khách nên được remarketing hoặc win-back.

Nếu doanh nghiệp gửi cùng một chiến dịch marketing cho tất cả khách hàng thì sẽ không tối ưu. Vì vậy cần phân khúc khách hàng để hiểu rõ từng nhóm và đưa ra chiến lược phù hợp.

---

## 3. Mục tiêu dự án

Mục tiêu chính của dự án là xây dựng một pipeline end-to-end có thể:

1. Nhận dữ liệu giao dịch thô từ người dùng.
2. Làm sạch dữ liệu giao dịch.
3. Tính các chỉ số RFM cho từng khách hàng.
4. Chuẩn hóa dữ liệu RFM trước khi clustering.
5. Chọn số cụm K phù hợp bằng Elbow Method và Silhouette Score.
6. Huấn luyện K-means để phân cụm khách hàng.
7. Diễn giải từng cụm thành các nhóm khách hàng có ý nghĩa business.
8. Hiển thị kết quả trên Streamlit dashboard.
9. Cho phép người dùng tải kết quả phân khúc ra file CSV.

---

## 4. Phạm vi hiện tại của dự án

### In scope

Phiên bản hiện tại tập trung vào:

- Data Cleaning.
- RFM Feature Engineering.
- Transformation bằng `log1p` hoặc `Box-Cox`.
- Scaling bằng `StandardScaler`.
- K-means Clustering.
- Chọn K bằng Elbow và Silhouette.
- Cluster Profiling.
- Business Recommendation.
- Streamlit App để upload file và xem kết quả.

### Out of scope

Phiên bản hiện tại **chưa tập trung vào**:

- 16 behavioral features nâng cao.
- SHAP/xAI trong core pipeline.
- Churn Prediction.
- Customer Lifetime Value Prediction.
- Recommendation System.
- Production deployment hoàn chỉnh.
- Database backend.
- Authentication/user management.

Các phần này có thể được đưa vào module mở rộng sau.

---

## 5. Vì sao dùng RFM?

RFM là framework phổ biến trong phân tích khách hàng, gồm 3 chỉ số chính:

| Chỉ số | Ý nghĩa | Cách hiểu |
|---|---|---|
| Recency | Khách mua lần cuối cách hiện tại bao lâu | Recency càng thấp càng tốt |
| Frequency | Khách mua bao nhiêu lần | Frequency càng cao càng tốt |
| Monetary | Khách đã chi tổng cộng bao nhiêu tiền | Monetary càng cao càng tốt |

RFM giúp biến dữ liệu giao dịch từ cấp độ transaction thành cấp độ customer.

Ví dụ:

```text
Raw transactions
        ↓
Group by CustomerID
        ↓
Customer-level RFM table
```

---

## 6. Vì sao dùng K-means?

K-means phù hợp với phiên bản đầu của dự án vì:

- Dễ hiểu.
- Dễ triển khai.
- Tốc độ nhanh.
- Dễ giải thích bằng centroid và cluster profile.
- Phù hợp với bài toán unsupervised learning.
- Có thể kết hợp tốt với RFM.

Trong bài toán này, K-means học ra các tâm cụm khách hàng dựa trên 3 chiều hành vi:

```text
Recency — Frequency — Monetary
```

Sau khi fit, mỗi khách hàng sẽ được gán vào cụm gần nhất.

---

## 7. Input của hệ thống

Người dùng upload một file CSV giao dịch có tối thiểu các cột sau:

| Cột | Ý nghĩa | Bắt buộc |
|---|---|---|
| InvoiceNo | Mã hóa đơn | Có |
| CustomerID | Mã khách hàng | Có |
| InvoiceDate | Ngày giao dịch | Có |
| Quantity | Số lượng mua | Có |
| UnitPrice | Đơn giá | Có |
| Country | Quốc gia | Không bắt buộc |
| StockCode | Mã sản phẩm | Không bắt buộc |
| Description | Tên sản phẩm | Không bắt buộc |

---

## 8. Output của hệ thống

Sau khi chạy pipeline, hệ thống tạo ra các output chính:

### 8.1. Bảng RFM

| CustomerID | Recency | Frequency | Monetary |
|---|---:|---:|---:|
| 17850 | 5 | 20 | 5000 |
| 13047 | 180 | 1 | 50 |

### 8.2. Bảng phân khúc khách hàng

| CustomerID | Recency | Frequency | Monetary | Cluster | Segment |
|---|---:|---:|---:|---:|---|
| 17850 | 5 | 20 | 5000 | 0 | Champions |
| 13047 | 180 | 1 | 50 | 1 | Lost Customers |

### 8.3. Cluster profile

| Cluster | Segment | Customer Count | Recency Mean | Frequency Mean | Monetary Mean |
|---:|---|---:|---:|---:|---:|
| 0 | Champions | 300 | 7.2 | 15.4 | 4200 |
| 1 | Lost Customers | 1200 | 210.5 | 1.2 | 80 |

### 8.4. Business recommendation

| Segment | Recommendation |
|---|---|
| Champions | VIP program, ưu đãi độc quyền, early access |
| At Risk VIP | Win-back campaign, voucher cá nhân hóa |
| New Customers | Welcome voucher, khuyến khích đơn thứ hai |
| Lost Customers | Remarketing chi phí thấp |

---

## 9. Luồng tổng quan end-to-end

```text
User uploads raw CSV
        ↓
Validate schema
        ↓
Clean transaction data
        ↓
Build RFM table
        ↓
Transform RFM values
        ↓
Scale RFM values
        ↓
Find optimal K
        ↓
Train K-means
        ↓
Assign customer clusters
        ↓
Profile clusters
        ↓
Map clusters to segment names
        ↓
Generate business recommendations
        ↓
Show dashboard and allow CSV download
```

---

## 10. Unsupervised Learning trong dự án này

Dự án này thuộc nhóm **Unsupervised Learning** vì dữ liệu ban đầu không có nhãn phân khúc khách hàng.

Model không được cung cấp sẵn nhãn như:

```text
VIP
Loyal
At Risk
Lost
```

Thay vào đó, K-means tự tìm các nhóm khách hàng có hành vi RFM tương đồng. Sau đó team phân tích profile từng cụm để đặt tên business cho các nhóm.

---

## 11. Training và inference

### Training phase

Dùng dữ liệu lịch sử của cùng doanh nghiệp/cùng ngành hàng để:

1. Tính RFM.
2. Transform và scale.
3. Fit K-means.
4. Lưu model nếu cần.
5. Đặt tên và diễn giải cụm.

### Inference phase

Khi có khách hàng mới cùng doanh nghiệp/cùng ngành hàng:

1. Tính RFM cho khách mới.
2. Áp dụng cùng preprocessing.
3. Dùng K-means đã fit để gán cụm.
4. Map cụm sang segment name.
5. Đưa ra recommendation.

Lưu ý: `predict` trong K-means vẫn thuộc unsupervised inference, không phải supervised learning.

---

## 12. Lưu ý khi áp dụng sang ngành khác

Không nên dùng trực tiếp model đã train trên ngành A để predict cho ngành B nếu hành vi mua hàng khác nhau.

Ví dụ:

| Ngành | Đặc điểm |
|---|---|
| Thực phẩm | Mua thường xuyên, chu kỳ ngắn |
| Mỹ phẩm | Mua lại theo chu kỳ vài tuần/vài tháng |
| Nội thất | Mua ít lần nhưng giá trị đơn hàng cao |
| Ô tô | Chu kỳ mua rất dài, Frequency thấp là bình thường |

Có thể dùng lại:

- Pipeline.
- Code.
- Công thức RFM.
- Giao diện dashboard.
- Cách phân tích.

Nhưng cần fit lại:

- Scaler.
- K-means.
- Ngưỡng diễn giải.
- Segment naming.
- Business recommendation.

---

## 13. Có nên dùng SHAP/xAI không?

Với phiên bản RFM-only, SHAP chưa cần thiết vì chỉ có 3 feature:

- Recency.
- Frequency.
- Monetary.

Cluster có thể giải thích trực tiếp bằng bảng trung bình RFM của từng cụm.

SHAP nên được đưa vào module mở rộng khi dự án bổ sung nhiều feature hơn, ví dụ:

- 16 behavioral features.
- Seasonal features.
- Product category features.
- Geographic features.
- Time-based features.

Khi đó cluster khó giải thích bằng mắt, SHAP có thể được dùng thông qua surrogate model.

---

## 14. Future Work

Các hướng mở rộng sau MVP:

1. Bổ sung 16 behavioral features.
2. So sánh RFM-only với RFM + advanced features.
3. Thử DBSCAN, Gaussian Mixture, Hierarchical Clustering.
4. Bổ sung SHAP/xAI để giải thích cluster.
5. Xây dựng dashboard nâng cao.
6. Lưu model và triển khai inference cho khách hàng mới.
7. Kết nối database.
8. Xây dựng API backend.
9. Thêm module churn prediction.
10. Thêm module CLV prediction.
11. Thêm recommendation system.

---

## 15. Tóm tắt dự án

Dự án xây dựng một hệ thống phân khúc khách hàng end-to-end bằng RFM và K-means. Người dùng upload dữ liệu giao dịch, hệ thống tự động làm sạch dữ liệu, tính RFM, chuẩn hóa, chọn K, huấn luyện K-means, gán segment cho từng khách hàng và hiển thị kết quả trên dashboard. Phiên bản hiện tại tập trung vào RFM-only để tạo baseline rõ ràng, dễ giải thích và dễ mở rộng về sau.
