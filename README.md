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
- Nhóm khách hàng mới.
- Nhóm khách hàng có nguy cơ rời bỏ.
- Nhóm khách hàng đã lâu không quay lại.

## 3. Dữ liệu

- Nguồn: Dữ liệu giao dịch công ty bán lẻ trực tuyến UK (2010-2011)
- Quy mô: 541,909 giao dịch từ 4,372 khách hàng
- Đặc điểm: Giao dịch quà tặng và đồ gia dụng độc đáo

## 3. Cấu trúc thư mục

```text
customer-segmentation-rfm/
│
├── data/
│   ├── raw/                         # Dữ liệu gốc
│   └── processed/                   # Dữ liệu sau xử lý và kết quả phân cụm
│
├── notebooks/
│   ├── 01_cleaning_and_eda.ipynb     # Làm sạch dữ liệu và EDA
│   ├── 02_rfm_feature_engineering.ipynb
│   └── 03_kmeans_modeling.ipynb      # K-means và diễn giải cụm
│
├── src/
│   └── rfm_segmentation.py           # Logic chính: cleaning, RFM, K-means, segment naming
│
├── app/
│   └── streamlit_app.py              # Giao diện Streamlit
│
├── docs/
│   ├── project_overview.md           # Tổng quan project
│   └── workflow.md                   # Quy trình xử lý end-to-end
│
├── README.md                         # Tài liệu hướng dẫn chính
├── requirements.txt                  # Thư viện cần cài đặt
├── .gitignore
└── setup_code.py                     # Script hỗ trợ setup, nếu cần
```

## 4. Giải thích về model và dữ liệu ngành khác nhau

Trong phiên bản demo, app sẽ fit lại K-means trên từng file người dùng upload. Điều này có nghĩa là mỗi dataset sẽ có một kết quả segmentation riêng.

Không nên dùng model đã train từ ngành A để áp dụng trực tiếp cho ngành B nếu hành vi mua hàng khác nhau.

Ví dụ:

| Ngành | Đặc điểm hành vi |
|---|---|
| Thực phẩm | Mua thường xuyên, chu kỳ ngắn |
| Mỹ phẩm | Mua theo chu kỳ vài tuần hoặc vài tháng |
| Nội thất | Mua ít lần nhưng giá trị đơn hàng cao |
| Ô tô | Chu kỳ mua rất dài, Frequency thấp là bình thường |

Vì vậy:

- Có thể dùng lại pipeline RFM + K-means.
- Có thể dùng lại code và giao diện Streamlit.
- Nhưng nên fit lại scaler, K-means và diễn giải segment cho từng ngành hoặc từng doanh nghiệp cụ thể.

## 5. Hướng phát triển tiếp theo

Các hướng mở rộng trong tương lai:

- Thêm 16 behavioral features để cải thiện segmentation.
- So sánh RFM-only với advanced feature engineering.
- Thử các thuật toán khác như DBSCAN, Hierarchical Clustering, Gaussian Mixture Model.
- Thêm SHAP/xAI để giải thích cụm khi số lượng feature tăng lên.
- Xây dựng dashboard nâng cao hơn với bộ lọc theo thời gian, quốc gia, sản phẩm.
- Kết nối database thay vì chỉ upload CSV.
- Lưu model để phục vụ inference cho khách hàng mới trong cùng doanh nghiệp.

Dưới đây là mã Markdown chính xác cho nội dung trong ảnh. Bạn có thể copy toàn bộ đoạn mã trong khung dưới đây để sử dụng:


## Bắt đầu nhanh

1. Cài đặt dependencies:

```bash
pip install -r requirements.txt
```

2. Chạy notebooks theo thứ tự:
    * `01_cleaning_and_eda.ipynb` - Làm sạch và khám phá dữ liệu
    * `02_feature_engineering.ipynb` - Tạo features RFM
    * `03_modeling.ipynb` - Xây dựng mô hình clustering

---

## Công nghệ sử dụng

* **Python**
* **Pandas** - Xử lý dữ liệu
* **Scikit-learn** - Machine learning
* **Matplotlib/Seaborn** - Visualization
* **NumPy** - Tính toán số học

---

## Tài liệu

Chi tiết về phương pháp và lý thuyết được mô tả trong `docs/workflow.md` và `docs/project_overview.md`