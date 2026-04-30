# Workflow — Customer Segmentation using RFM + K-means

## 1. Mục tiêu của workflow

File này mô tả chi tiết workflow triển khai dự án Customer Segmentation using RFM + K-means từ dữ liệu thô đến Streamlit app.

Workflow cần đảm bảo:

- Dễ hiểu cho toàn team.
- Có thể chạy lại được.
- Tách rõ từng bước trong pipeline.
- Phân biệt rõ notebook nghiên cứu, source code pipeline và Streamlit app.
- Có output cụ thể sau mỗi bước.

---

## 2. Big Picture Workflow

```text
Raw Data
  ↓
Data Validation
  ↓
Data Cleaning
  ↓
RFM Feature Engineering
  ↓
RFM Transformation
  ↓
Feature Scaling
  ↓
Optimal K Selection
  ↓
K-means Training
  ↓
Cluster Profiling
  ↓
Segment Naming
  ↓
Business Recommendation
  ↓
Streamlit Dashboard
  ↓
Export Results
```

---

## 3. Phase 1 — Raw Data Input

### 3.1. Mục tiêu

Nhận dữ liệu giao dịch thô từ người dùng hoặc từ folder `data/raw`.

### 3.2. Input

File CSV giao dịch có các cột tối thiểu:

```text
InvoiceNo
CustomerID
InvoiceDate
Quantity
UnitPrice
```

Các cột optional:

```text
Country
StockCode
Description
```

### 3.3. Output

DataFrame raw ban đầu.

### 3.4. Checklist

- [ ] Load file CSV.
- [ ] Kiểm tra encoding.
- [ ] Kiểm tra số dòng, số cột.
- [ ] Kiểm tra tên cột.
- [ ] Kiểm tra missing values.
- [ ] Kiểm tra kiểu dữ liệu.
- [ ] Kiểm tra có đủ cột bắt buộc không.

---

## 4. Phase 2 — Data Validation

### 4.1. Mục tiêu

Đảm bảo file upload đúng format trước khi chạy pipeline.

### 4.2. Rule validation

| Điều kiện | Hành động nếu lỗi |
|---|---|
| Thiếu `CustomerID` | Báo lỗi và dừng |
| Thiếu `InvoiceNo` | Báo lỗi và dừng |
| Thiếu `InvoiceDate` | Báo lỗi và dừng |
| Thiếu `Quantity` | Báo lỗi và dừng |
| Thiếu `UnitPrice` | Báo lỗi và dừng |
| `InvoiceDate` không parse được | Convert lỗi thành NaT và loại bỏ |
| `Quantity` không phải số | Convert lỗi thành NaN và loại bỏ |
| `UnitPrice` không phải số | Convert lỗi thành NaN và loại bỏ |

### 4.3. Output

DataFrame đã qua kiểm tra schema.

### 4.4. Checklist

- [ ] Viết hàm `validate_schema(df)`.
- [ ] Trả về danh sách cột thiếu.
- [ ] Hiển thị lỗi trên Streamlit nếu thiếu cột.
- [ ] Dừng app nếu dữ liệu không hợp lệ.

---

## 5. Phase 3 — Data Cleaning

### 5.1. Mục tiêu

Làm sạch transaction data để chuẩn bị tính RFM.

### 5.2. Cleaning rules

| Bước | Mục đích |
|---|---|
| Convert `InvoiceDate` về datetime | Dùng để tính Recency |
| Convert `Quantity`, `UnitPrice` về numeric | Dùng để tính TotalPrice |
| Chuẩn hóa `CustomerID` | Đảm bảo group đúng khách hàng |
| Bỏ missing `CustomerID` | Không biết giao dịch thuộc khách nào |
| Bỏ invoice bắt đầu bằng `C` | Loại hóa đơn hủy |
| Bỏ `Quantity <= 0` | Loại giao dịch không hợp lệ |
| Bỏ `UnitPrice <= 0` | Loại giao dịch không hợp lệ |
| Tạo `TotalPrice` | Dùng để tính Monetary |
| Optional: lọc `Country` | Tập trung vào một thị trường |

### 5.3. Công thức

```text
TotalPrice = Quantity × UnitPrice
```

### 5.4. Output

File/dataframe:

```text
cleaned_transactions.csv
```

### 5.5. Checklist

- [ ] Parse datetime.
- [ ] Chuẩn hóa CustomerID.
- [ ] Loại missing CustomerID.
- [ ] Loại canceled invoice.
- [ ] Loại Quantity/UnitPrice không hợp lệ.
- [ ] Tạo TotalPrice.
- [ ] Log số dòng trước và sau cleaning.
- [ ] Lưu clean data.

---

## 6. Phase 4 — RFM Feature Engineering

### 6.1. Mục tiêu

Biến dữ liệu transaction-level thành customer-level.

### 6.2. Input

Cleaned transaction data.

### 6.3. RFM definition

| Feature | Công thức | Ý nghĩa |
|---|---|---|
| Recency | `snapshot_date - max(InvoiceDate)` | Số ngày từ lần mua cuối |
| Frequency | `nunique(InvoiceNo)` | Số hóa đơn unique |
| Monetary | `sum(TotalPrice)` | Tổng chi tiêu |

### 6.4. Snapshot date

```text
snapshot_date = max(InvoiceDate) + 1 day
```

### 6.5. Output

```text
rfm_table.csv
```

Bảng output:

| CustomerID | Recency | Frequency | Monetary |
|---|---:|---:|---:|

### 6.6. Checklist

- [ ] Group by `CustomerID`.
- [ ] Tính Recency.
- [ ] Tính Frequency.
- [ ] Tính Monetary.
- [ ] Kiểm tra RFM không âm.
- [ ] Kiểm tra Frequency > 0.
- [ ] Kiểm tra Monetary > 0.
- [ ] Lưu RFM table.

---

## 7. Phase 5 — RFM EDA

### 7.1. Mục tiêu

Hiểu phân phối của RFM trước khi đưa vào clustering.

### 7.2. Các phân tích cần làm

- Histogram Recency.
- Histogram Frequency.
- Histogram Monetary.
- Boxplot RFM.
- Correlation heatmap.
- Top customers by Monetary.
- Top customers by Frequency.

### 7.3. Insight cần trả lời

- Khách hàng có mua gần đây không?
- Phần lớn khách mua nhiều hay ít?
- Doanh thu có tập trung vào một nhóm nhỏ không?
- RFM có bị skewed không?
- Có outlier lớn không?

### 7.4. Checklist

- [ ] Vẽ histogram Recency.
- [ ] Vẽ histogram Frequency.
- [ ] Vẽ histogram Monetary.
- [ ] Vẽ boxplot.
- [ ] Ghi nhận skewness.
- [ ] Ghi nhận outliers.
- [ ] Viết insight ngắn.

---

## 8. Phase 6 — RFM Transformation

### 8.1. Mục tiêu

Giảm độ lệch phải của RFM trước khi clustering.

RFM thường bị right-skewed vì:

- Đa số khách mua ít.
- Một số ít khách mua rất nhiều.
- Monetary có outlier lớn.

### 8.2. Option 1 — log1p

Cách đơn giản cho MVP:

```python
X_log = np.log1p(X)
```

Ưu điểm:

- Dễ hiểu.
- Dễ triển khai.
- Xử lý được giá trị 0.
- Không cần lưu lambda.

### 8.3. Option 2 — Box-Cox

Cách chuyên nghiệp hơn:

```python
transformed, lambda_param = boxcox(x)
```

Lưu ý:

- Dữ liệu phải > 0.
- Cần lưu lambda cho từng feature nếu dùng production inference.
- Phù hợp khi muốn bám sát pipeline nâng cao.

### 8.4. Quyết định MVP

MVP có thể dùng:

```text
log1p + StandardScaler
```

Nếu muốn giống pipeline của thầy hơn, có thể dùng:

```text
Box-Cox + StandardScaler
```

### 8.5. Checklist

- [ ] Chọn log1p hoặc Box-Cox.
- [ ] Áp dụng transformation cho RFM.
- [ ] Kiểm tra phân phối sau transform.
- [ ] Lưu transformer nếu cần production.

---

## 9. Phase 7 — Feature Scaling

### 9.1. Mục tiêu

Đưa Recency, Frequency, Monetary về cùng thang đo.

K-means dùng khoảng cách Euclidean nên rất nhạy với scale.

### 9.2. Method

```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_transformed)
```

### 9.3. Output

Scaled RFM matrix:

```text
X_scaled
```

### 9.4. Checklist

- [ ] Fit StandardScaler trên transformed RFM.
- [ ] Tạo `X_scaled`.
- [ ] Kiểm tra shape.
- [ ] Lưu scaler nếu cần production.

---

## 10. Phase 8 — Optimal K Selection

### 10.1. Mục tiêu

Tìm số cụm K phù hợp trước khi train K-means cuối cùng.

### 10.2. Range

Thử K trong khoảng:

```text
K = 2 → 10
```

### 10.3. Metrics

| Metric | Ý nghĩa |
|---|---|
| Inertia/WCSS | Tổng khoảng cách bình phương từ điểm tới centroid |
| Elbow Method | Tìm điểm mà inertia giảm chậm lại |
| Silhouette Score | Đo độ tách biệt và gắn kết của cụm |

### 10.4. Output

```text
k_results.csv
```

| k | inertia | silhouette |
|---:|---:|---:|

### 10.5. Checklist

- [ ] Loop k từ 2 đến 10.
- [ ] Fit K-means cho từng k.
- [ ] Tính inertia.
- [ ] Tính silhouette.
- [ ] Vẽ Elbow chart.
- [ ] Vẽ Silhouette chart.
- [ ] Đề xuất best_k.
- [ ] Cho user chọn lại K trên Streamlit nếu cần.

---

## 11. Phase 9 — K-means Training

### 11.1. Mục tiêu

Huấn luyện K-means với K đã chọn.

### 11.2. Input

```text
X_scaled
selected_k
```

### 11.3. Training

```python
model = KMeans(n_clusters=selected_k, random_state=42, n_init=10)
labels = model.fit_predict(X_scaled)
```

### 11.4. Output

RFM table có thêm cluster label:

| CustomerID | Recency | Frequency | Monetary | Cluster |
|---|---:|---:|---:|---:|

### 11.5. Checklist

- [ ] Fit K-means với selected_k.
- [ ] Gán cluster label.
- [ ] Kiểm tra số khách mỗi cluster.
- [ ] Lưu model nếu cần.
- [ ] Lưu output segmentation.

---

## 12. Phase 10 — Cluster Profiling

### 12.1. Mục tiêu

Hiểu mỗi cluster đại diện cho nhóm khách hàng nào.

### 12.2. Các chỉ số cần tính theo cluster

- Số khách hàng.
- Recency mean/median.
- Frequency mean/median.
- Monetary mean/median.
- Total revenue.
- Revenue share.
- Customer share.

### 12.3. Output

```text
cluster_profile.csv
```

| Cluster | Customer Count | Recency Mean | Frequency Mean | Monetary Mean | Revenue Share |
|---:|---:|---:|---:|---:|---:|

### 12.4. Checklist

- [ ] Group by Cluster.
- [ ] Tính mean/median RFM.
- [ ] Tính số khách.
- [ ] Tính doanh thu theo cluster.
- [ ] Tính revenue share.
- [ ] Viết nhận xét từng cluster.

---

## 13. Phase 11 — Segment Naming

### 13.1. Mục tiêu

Chuyển cluster label kỹ thuật thành tên segment dễ hiểu cho business.

Không được mặc định:

```text
Cluster 0 = Champions
```

Vì cluster ID có thể thay đổi sau mỗi lần train.

Phải đọc profile rồi mới đặt tên.

### 13.2. Gợi ý logic đặt tên

| RFM Pattern | Segment Name |
|---|---|
| Recency thấp, Frequency cao, Monetary cao | Champions |
| Recency cao, Frequency cao, Monetary cao | At Risk VIP |
| Recency thấp, Frequency thấp | New / Recent Customers |
| Recency cao, Frequency thấp, Monetary thấp | Lost Customers |
| Frequency cao, Monetary trung bình/cao | Loyal Customers |
| Monetary cao, Frequency thấp | Big Spenders |
| Các nhóm còn lại | Regular Customers |

### 13.3. Output

RFM table có thêm `Segment`.

| CustomerID | Recency | Frequency | Monetary | Cluster | Segment |
|---|---:|---:|---:|---:|---|

### 13.4. Checklist

- [ ] Xếp hạng cluster theo Recency, Frequency, Monetary.
- [ ] Tạo mapping `Cluster → Segment`.
- [ ] Kiểm tra segment name có hợp lý không.
- [ ] Viết mô tả từng segment.

---

## 14. Phase 12 — Business Recommendation

### 14.1. Mục tiêu

Đưa ra hành động marketing/CRM cho từng segment.

### 14.2. Recommendation mapping

| Segment | Recommendation |
|---|---|
| Champions | VIP program, ưu đãi độc quyền, early access |
| Loyal Customers | Tích điểm, combo, cross-sell |
| Big Spenders | Upsell sản phẩm premium |
| New / Recent Customers | Welcome voucher, khuyến khích đơn thứ hai |
| At Risk VIP | Win-back campaign, voucher cá nhân hóa |
| Lost Customers | Remarketing chi phí thấp |
| Regular Customers | Duy trì tương tác và gợi ý sản phẩm phù hợp |

### 14.3. Checklist

- [ ] Viết recommendation cho từng segment.
- [ ] Gắn recommendation vào output.
- [ ] Hiển thị trên dashboard.
- [ ] Đưa vào report.

---

## 15. Phase 13 — Streamlit App

### 15.1. Mục tiêu

Đóng gói pipeline thành app để người dùng không cần đọc code vẫn dùng được.

### 15.2. Input trên app

- Upload CSV.
- Optional: chọn country.
- Optional: chọn transform method.
- Optional: chọn K hoặc dùng K đề xuất.
- Optional: nhập CustomerID để lookup.

### 15.3. Output trên app

- Data overview.
- RFM table.
- Elbow chart.
- Silhouette chart.
- Segment distribution.
- Revenue by segment.
- Cluster profile.
- Customer lookup.
- Recommendation.
- Download CSV.

### 15.4. Page layout gợi ý

```text
Sidebar
  ├── Upload CSV
  ├── Country filter
  ├── Transform method
  ├── K selection
  └── Run button

Main
  ├── Data Overview
  ├── RFM Table
  ├── K Selection Charts
  ├── Segmentation Result
  ├── Segment Profile
  ├── Business Recommendation
  ├── Customer Lookup
  └── Download Outputs
```

### 15.5. Checklist

- [ ] Tạo `app/streamlit_app.py`.
- [ ] Thêm file uploader.
- [ ] Gọi pipeline từ source code.
- [ ] Hiển thị metrics.
- [ ] Hiển thị charts.
- [ ] Hiển thị tables.
- [ ] Thêm customer lookup.
- [ ] Thêm download button.
- [ ] Test app với file mẫu.

---

## 16. Phase 14 — Export Results

### 16.1. Output files

```text
outputs/cleaned_transactions.csv
outputs/rfm_table.csv
outputs/k_selection_results.csv
outputs/customer_segments.csv
outputs/cluster_profile.csv
```

### 16.2. Checklist

- [ ] Lưu clean data.
- [ ] Lưu RFM table.
- [ ] Lưu K results.
- [ ] Lưu customer segments.
- [ ] Lưu cluster profile.
- [ ] Cho download trong Streamlit.
---

## 17. Role-based Workflow cho team

| Role | Nhiệm vụ |
|---|---|
| AI Engineer Data | Data validation, cleaning, EDA |
| AI Engineer Model | RFM, transformation, K-means, K selection |
| AI Engineer Pipeline | Convert notebook thành source code, run_pipeline |
| Developer | Streamlit app, UI, upload/download |
| QA/Reviewer | Kiểm tra logic, test app, review report |

---

## 18. MVP Acceptance Criteria

Dự án MVP được xem là hoàn thành khi:

- [ ] User upload được file CSV.
- [ ] App kiểm tra được schema.
- [ ] App clean được dữ liệu.
- [ ] App tính được RFM.
- [ ] App transform và scale được RFM.
- [ ] App vẽ được Elbow và Silhouette.
- [ ] App train được K-means.
- [ ] App gán được cluster cho từng customer.
- [ ] App tạo được cluster profile.
- [ ] App đặt được segment name.
- [ ] App hiển thị recommendation.
- [ ] App cho download output CSV.
- [ ] README hướng dẫn chạy app rõ ràng.
- [ ] Report giải thích được business insight.

---

## 19. Notes về SHAP/xAI

SHAP chưa nên là core requirement trong MVP vì chỉ có 3 feature RFM. Việc giải thích cluster bằng profile RFM là đủ rõ.

SHAP có thể được thêm ở module nâng cao khi:

- Bổ sung 16 behavioral features.
- Cụm khó giải thích bằng centroid.
- Cần giải thích feature nào ảnh hưởng nhiều đến việc một khách thuộc cụm nào.

Nếu dùng SHAP, cần nhớ:

```text
SHAP không giải thích trực tiếp K-means.
SHAP giải thích surrogate model được train để bắt chước cluster label.
```

---

## 20. Workflow tóm tắt cho demo

```text
1. Mở Streamlit app.
2. Upload raw transaction CSV.
3. App hiển thị số dòng raw.
4. App chạy cleaning.
5. App hiển thị số dòng sau cleaning.
6. App tính RFM.
7. App vẽ phân phối RFM.
8. App chạy Elbow và Silhouette.
9. User chọn K.
10. App train K-means.
11. App hiển thị segment distribution.
12. App hiển thị cluster profile.
13. App hiển thị recommendation.
14. User tra cứu CustomerID.
15. User download customer_segments.csv.
```

---

## 21. Final Workflow Sentence

Project workflow được thiết kế để biến một file giao dịch thô thành một hệ thống phân khúc khách hàng có thể sử dụng được. Toàn bộ quy trình đi từ data cleaning, RFM feature engineering, transformation, scaling, K-means clustering, cluster interpretation đến dashboard Streamlit. Kết quả cuối cùng không chỉ là cluster label, mà là insight và recommendation có giá trị cho marketing/business team.
