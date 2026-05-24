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

## 3. Raw Data Input

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


## 4. Data Cleaning

### 4.1. Mục tiêu

Làm sạch transaction data để chuẩn bị tính RFM.

### 4.2. Cleaning rules

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

### 4.3. Công thức

```text
TotalPrice = Quantity × UnitPrice
```

### 4.4. Output

File/dataframe:

```text
cleaned_transactions.csv
```

## 5. RFM Feature Engineering

### 5.1. Mục tiêu

Biến dữ liệu transaction-level thành customer-level.

### 5.2. Input

Cleaned transaction data.

### 5.3. RFM definition

| Feature | Công thức | Ý nghĩa |
|---|---|---|
| Recency | `snapshot_date - max(InvoiceDate)` | Số ngày từ lần mua cuối |
| Frequency | `nunique(InvoiceNo)` | Số hóa đơn unique |
| Monetary | `sum(TotalPrice)` | Tổng chi tiêu |
| R_Score | Quantile binning (5 tầng) | Điểm Recency từ 1-5, thấp càng tốt |
| F_Score | Quantile binning (5 tầng) | Điểm Frequency từ 1-5, cao càng tốt |
| M_Score | Quantile binning (5 tầng) | Điểm Monetary từ 1-5, cao càng tốt |
| RFM_Score | R_Score + F_Score + M_Score | Tổng điểm RFM (3-15) |

### 5.5. Output

```text
rfm_table.csv
```

Bảng output (8 cột):

| CustomerID | Recency | Frequency | Monetary | R_Score | F_Score | M_Score | RFM_Score |
|---|---:|---:|---:|---:|---:|---:|---:|


## 6. Phase 5 — RFM EDA

### 6.1. Mục tiêu

- Histogram Recency.
- Histogram Frequency.
- Histogram Monetary.
- Boxplot RFM.
- Correlation heatmap.
- Top customers by Monetary.
- Top customers by Frequency.

### 6.3. Insight cần trả lời

- Khách hàng có mua gần đây không?
- Phần lớn khách mua nhiều hay ít?
- Doanh thu có tập trung vào một nhóm nhỏ không?
- RFM có bị skewed không?
- Có outlier lớn không?

---


## 7. Phase 6 — RFM Transformation

### 7.1. Mục tiêu

RFM thường bị right-skewed vì:

- Đa số khách mua ít.
- Một số ít khách mua rất nhiều.
- Monetary có outlier lớn.

### 7.2. Method — log1p

MVP dùng log1p để transformation:

```python
X_log = np.log1p(X)
```

Ưu điểm:

- Dễ hiểu.
- Dễ triển khai.
- Xử lý được giá trị 0.
- Hiệu quả cho RFM-only.

---

## 8. Phase 7 — Feature Scaling

### 8.1. Mục tiêu

Đưa Recency, Frequency, Monetary về cùng thang đo.

K-means dùng khoảng cách Euclidean nên rất nhạy với scale.

### 8.2. Method

```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_transformed)
```

### 8.3. Output

Scaled RFM matrix:

```text
X_scaled
```

---

## 9. Phase 8 — Optimal K Selection (MVP: Fixed K=4)

### 9.1. Mục tiêu

Phiên bản MVP hiện tại sử dụng **K=4 cố định** để đơn giản hóa.

Trong tương lai, có thể thêm tính năng tự động chọn K bằng Elbow Method và Silhouette Score.

### 9.2. MVP — Fixed K

```python
n_clusters = 4  # Cố định cho MVP
```

Lý do chọn K=4:

- Dễ hiểu cho business.
- Champions, Loyal, At-Risk, Lost.
- Cân bằng giữa chi tiết và khả năng hành động.

### 9.3. Future — Automatic K Selection

Trong phiên bản nâng cao, có thể thêm:

```python
K_range = range(2, 11)
# Tính Elbow
# Tính Silhouette
# Đề xuất K tối ưu
# Cho user chọn lại nếu cần
```

---

## 10. Phase 9 — K-means Training

### 10.1. Mục tiêu

Huấn luyện K-means với K đã chọn.

### 10.2. Input

```text
X_scaled
selected_k
```

### 10.3. Training

```python
model = KMeans(n_clusters=selected_k, random_state=42, n_init=10)
labels = model.fit_predict(X_scaled)
```

### 10.4. Output

RFM table có thêm cluster label:

| CustomerID | Recency | Frequency | Monetary | Cluster |
|---|---:|---:|---:|---:|

---

## 11. Phase 10 — Cluster Profiling

### 11.1. Mục tiêu

Hiểu mỗi cluster đại diện cho nhóm khách hàng nào.

### 11.2. Các chỉ số cần tính theo cluster

- Số khách hàng.
- Recency mean/median.
- Frequency mean/median.
- Monetary mean/median.
- Total revenue.
- Revenue share.
- Customer share.

### 11.3. Output

```text
cluster_profile.csv
```

| Cluster | Customer Count | Recency Mean | Frequency Mean | Monetary Mean | Revenue Share |
|---:|---:|---:|---:|---:|---:|

---

## 12. Phase 11 — Segment Naming

### 12.1. Mục tiêu

Chuyển cluster label kỹ thuật thành tên segment dễ hiểu cho business.

Không được mặc định:

```text
Cluster 0 = Champions
```

Vì cluster ID có thể thay đổi sau mỗi lần train.

Phải đọc profile rồi mới đặt tên.

### 12.2. Gợi ý logic đặt tên

| RFM Pattern | Segment Name |
|---|---|
| Recency thấp, Frequency cao, Monetary cao | Champions |
| Recency cao, Frequency cao, Monetary cao | At Risk VIP |
| Recency thấp, Frequency thấp | New / Recent Customers |
| Recency cao, Frequency thấp, Monetary thấp | Lost Customers |
| Frequency cao, Monetary trung bình/cao | Loyal Customers |
| Monetary cao, Frequency thấp | Big Spenders |
| Các nhóm còn lại | Regular Customers |

### 12.3. Output

RFM table có thêm `Cluster` và `Segment` (10 cột).

| CustomerID | Recency | Frequency | Monetary | R_Score | F_Score | M_Score | RFM_Score | Cluster | Segment |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|

---

## 13. Phase 12 — Business Recommendation

### 13.1. Mục tiêu

Đưa ra hành động marketing/CRM cho từng segment.

### 13.2. Recommendation mapping

| Segment | Recommendation |
|---|---|
| Champions | VIP program, ưu đãi độc quyền, early access |
| Loyal Customers | Tích điểm, combo, cross-sell |
| Big Spenders | Upsell sản phẩm premium |
| New / Recent Customers | Welcome voucher, khuyến khích đơn thứ hai |
| At Risk VIP | Win-back campaign, voucher cá nhân hóa |
| Lost Customers | Remarketing chi phí thấp |
| Regular Customers | Duy trì tương tác và gợi ý sản phẩm phù hợp |

---

## 14. Phase 13 — Streamlit Dashboard

### 14.1. Mục tiêu

Hiển thị kết quả segmentation đã được tính toán trước dó bằng `run_full_pipeline.py`.

Streamlit app là dashboard **visualization-only** (không xử lý data trong app).

### 14.2. Workflow sử dụng

1. User chạy `python src/run_full_pipeline.py` để tạo output files.
2. User chạy `streamlit run app/streamlit_app.py` để mở dashboard.
3. App đọc files từ `data/processed/`:
   - `rfm_table.csv`
   - `rfm_segments.csv`
   - `eda_results/` (biểu đồ)
4. App hiển thị kết quả dưới dạng interactive dashboard.

### 14.3. Output trên app

- Data overview (số khách, số giao dịch sau cleaning).
- RFM statistics.
- Segment distribution (bảng + biểu đồ).
- Revenue by segment.
- Cluster profile (RFM mean theo segment).
- Business recommendation.
- Customer lookup (tra cứu CustomerID).
- Download outputs.

### 14.4. Page layout

```text
Sidebar
  ├── Project Title
  ├── File Info
  └── Navigation

Main
  ├── Data Overview
  ├── RFM Statistics
  ├── Segment Distribution
  ├── Revenue by Segment
  ├── Cluster Profile
  ├── Business Recommendation
  ├── Customer Lookup
  └── Download Outputs
```

---

## 15. Phase 14 — Export Results

### 15.1. Output files

Pipeline tạo 4 loại output:

```text
data/processed/
  ├── clean_transactions.csv              # Transaction-level sau cleaning
  ├── rfm_table.csv                       # Customer-level với RFM + scores (8 cols)
  ├── rfm_segments.csv                    # Customer + cluster + segment (10 cols)
  └── eda_results/                        # EDA visualization charts
      ├── revenue_trend_monthly.png       # Doanh thu theo tháng
      ├── revenue_trend_quarterly.png     # Doanh thu theo quý
      ├── orders_by_weekday.png          # Số đơn hàng theo ngày tuần
      ├── orders_by_hour.png             # Heatmap đơn hàng theo giờ
      ├── top_products_revenue.png        # Top 10 sản phẩm theo doanh thu
      ├── top_products_quantity.png       # Top 10 sản phẩm theo số lượng
      └── customer_behavior.png           # Phân phối chi tiêu khách hàng
```

### 15.2. File descriptions

| File | Mục đích |
|---|---|
| clean_transactions.csv | Input cho RFM calculation |
| rfm_table.csv | RFM scores + R/F/M_Score (1-5) |
| rfm_segments.csv | Cluster assignments + segment names |
| eda_results/ | Biểu đồ EDA từ cleaning phase |

---

## 16. Role-based Workflow cho team

| Role | Nhiệm vụ |
|---|---|
| AI Engineer Data | Data validation, cleaning, EDA |
| AI Engineer Model | RFM, transformation, K-means, K selection |
| AI Engineer Pipeline | Convert notebook thành source code, run_pipeline |
| Developer | Streamlit app, UI, upload/download |
| QA/Reviewer | Kiểm tra logic, test app, review report |

---

## 17. Final Workflow Sentence

Project workflow được thiết kế để biến một file giao dịch thô thành một hệ thống phân khúc khách hàng có thể sử dụng được. Toàn bộ quy trình đi từ data cleaning, RFM feature engineering, transformation, scaling, K-means clustering, cluster interpretation đến dashboard Streamlit. Kết quả cuối cùng không chỉ là cluster label, mà là insight và recommendation có giá trị cho marketing/business team.
