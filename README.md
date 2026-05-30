# Customer Segmentation System using RFM + K-means

Dự án xây dựng hệ thống **phân khúc khách hàng** dựa trên dữ liệu giao dịch mua hàng. Hệ thống sử dụng phương pháp **RFM** kết hợp với thuật toán **K-means Clustering** để chia khách hàng thành các nhóm có hành vi mua sắm tương tự nhau, sau đó hiển thị kết quả qua **Streamlit App**.

## 1. Mục tiêu dự án

Mục tiêu của dự án là biến dữ liệu giao dịch thô thành các nhóm khách hàng có ý nghĩa kinh doanh.

Cụ thể, hệ thống giúp:

- Làm sạch dữ liệu giao dịch bán hàng.
- Tính chỉ số RFM cho từng khách hàng.
- Phân cụm khách hàng bằng K-means.
- Tìm số cụm phù hợp bằng Elbow Method và Silhouette Score.
- Diễn giải từng cụm khách hàng theo góc nhìn business.
- Đưa ra gợi ý chiến lược marketing cho từng nhóm.
- Xây dựng giao diện Streamlit để người dùng upload file và xem kết quả trực quan.

## 2. Bài toán cần giải quyết

Doanh nghiệp có nhiều khách hàng với hành vi mua hàng khác nhau. Nếu áp dụng cùng một chiến dịch marketing cho tất cả khách hàng thì hiệu quả thường không cao.

Dự án này giải quyết câu hỏi:

> Khách hàng của doanh nghiệp có thể được chia thành những nhóm nào dựa trên hành vi mua hàng trong quá khứ?

Ví dụ, hệ thống có thể giúp phát hiện:

- Nhóm khách hàng giá trị cao.
- Nhóm khách hàng trung thành.
- Nhóm khách hàng có nguy cơ rời bỏ.
- Nhóm khách hàng đã lâu không quay lại.

## 3. Dữ liệu

- Nguồn: Dữ liệu giao dịch công ty bán lẻ trực tuyến UK (2010-2011)
- Quy mô: 541,909 giao dịch từ 4,372 khách hàng
- Đặc điểm: Giao dịch quà tặng và đồ gia dụng độc đáo

## 4. Cấu trúc thư mục

```
AIO_OIA_Project01_Customer_Segmentation/
│
├── data/
│   ├── raw/
│   │   └── online_retail.csv              # Dữ liệu gốc
│   └── processed/
│       ├── clean_transactions.csv         # Dữ liệu sau làm sạch
│       ├── rfm_table.csv                  # RFM scores
│       ├── rfm_segments.csv               # Kết quả phân cụm cuối cùng
│       └── eda_results/                   # Kết quả EDA (hình ảnh)
│
├── notebooks/
│   ├── 01_cleaning_and_eda_1.ipynb       # Làm sạch và EDA
│   ├── rfm_feature_engineering.ipynb     # Tạo features RFM
│   ├── kmeans_modeling.ipynb             # K-means clustering
│   └── rfm_kmeans_complete.ipynb         # Pipeline hoàn chỉnh
│
├── src/
│   ├── run_full_pipeline.py              # pipeline làm sạch + EDA + RFM + K-means
│   ├── rfm_segmentation.py               # RFM + K-means pipeline
│   ├── interfaces/                       # Định nghĩa interface, business logic
│   │   ├── data_processor_interface.py
│   │   ├── eda_processor_interface.py
│   │   ├── rfm_calculator_interface.py
│   │   └── segmentor_interface.py
│   ├── models/
│   │   ├── kmeans_segmentor.py           # Phân cụm K-means
│   │   └── calculators/
│   │       └── rfm_calculator.py         # Logic tính RFM
│   ├── processors/
│   │   ├── csv_processor.py              # Xử lý dữ liệu CSV
│   │   ├── csv_eda.py                    # Phân tích EDA
│   │   ├── data_processor_base.py        # Lớp cơ sở, logic kỹ thuật
│   │   └── eda_processor_base.py         # Lớp cơ sở, logic kỹ thuật
│   ├── orchestrators/
│   │   └── eda_orchestractor.py          # điều phối EDA
│   └── utilities/
│       ├── convert_data_type.py          # Chuyển đổi kiểu dữ liệu
│       └── eda_visualizer.py             # Trực quan hóa
│
├── app/
│   └── streamlit_app.py                  # Giao diện Streamlit
│
├── docs/
│   ├── project_overview.md               # Tổng quan project
│   ├── workflow.md                       # Chi tiết workflow
│   └── EDA_flow.md                       # Chi tiết EDA flow
│
├── README.md                             # Tài liệu này
├── requirements.txt                      # Thư viện phụ thuộc
└── LICENSE
```

## 5. Key Insights

### RFM Metrics

- **Recency (R)**: Khách càng gần đây mua, Recency càng nhỏ, customer càng active
- **Frequency (F)**: Khách hàng trung thành có Frequency cao
- **Monetary (M)**: Chi tiêu cao = customer giá trị cao

### K-Means Segments

4 phân khúc mặc định (có thể tune `n_clusters`):
- **Segment 0**: Có thể là VIP customers (R, F, M đều cao)
- **Segment 1**: Có thể là At-Risk (R cao = lâu không mua)
- **Segment 2**: Có thể là Regular customers
- **Segment 3**: Có thể là New customers (F thấp)

### Ứng dụng Business

- **Marketing**: Chiến dịch khác nhau cho mỗi segment
- **Retention**: Tập trung vào segment At-Risk
- **Growth**: Upsell/Cross-sell cho VIP customers
- **Churn Prevention**: Theo dõi khách hàng từ Regular → At-Risk


## 6. Hướng phát triển tiếp theo

- Thêm 16 behavioral features để cải thiện segmentation.
- So sánh RFM-only với advanced feature engineering.
- Thử các thuật toán khác như DBSCAN, Hierarchical Clustering, Gaussian Mixture Model.
- Thêm SHAP/xAI để giải thích cụm khi số lượng feature tăng lên.
- Xây dựng dashboard nâng cao hơn với bộ lọc theo thời gian, quốc gia, sản phẩm.
- Kết nối database thay vì chỉ upload CSV.
- Lưu model để phục vụ inference cho khách hàng mới trong cùng doanh nghiệp.

---

