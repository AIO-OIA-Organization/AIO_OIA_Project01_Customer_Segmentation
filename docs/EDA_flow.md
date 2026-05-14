# 📊 EDA Flow - Customer Segmentation

## Quy Trình Xử Lý EDA

### ① Dữ Liệu Đầu Vào
- File: `data/processed/clean_transactions.csv`
- Load qua: `CsvEDA.load_data()`
- Dữ liệu: InvoiceNo, CustomerID, InvoiceDate, TotalPrice, Quantity, Description, StockCode

**1. Phân Tích Doanh Thu**
- Mục đích: Để hiểu xu hướng kinh doanh theo thời gian - có bao nhiêu tiền mỗi kỳ, tăng hay giảm?
- Method: `analyze_revenue_trend(freq: M/Q/Y)`-> Doanh thu theo tháng / quý / năm
- Kết quả: Chọn doanh thu theo tháng và quý , biểu đồ cột

**2. Phân Tích Xu Hướng Đơn Hàng**
- Mục đích: Để phát hiện khi nào khách mua nhiều nhất - ngày nào, giờ nào? Giúp dự báo nhu cầu.
- Method: `analyze_orders_by_trend(freq: weekday/hour)`-> Số đơn hàng theo ngày trong tuần hoặc giờ
- Kết quả: Chọn phân tích đơn hàng 
    - Tổng đơn hàng theo thứ trong tuần (T2,T3,..), dùng biểu đồ cột
    - Tổng đơn hàng theo thứ trong tuần và giờ trong này -> dùng heatmap

**3. Xếp Hạng Sản Phẩm**
- Mục đích: Để biết sản phẩm nào bán chạy nhất - tập trung nguồn lực vào sản phẩm doanh số cao.
- Method: `analyze_top_product(top_n, by: revenue/quantity)`
- Kết quả: Top N sản phẩm theo doanh số hoặc số lượng -> biểu độ cột ngang 

**4. Phân Tích Hành Vi Khách Hàng**
- Mục đích: Để hiểu khách chi tiêu bao nhiêu, mua bao nhiêu lần
- Method: `analyze_customer_behavior()`
- Kết quả: 
    - Dữ liệu chi tiêu của các khách hàng. -> histogram
    - dữ liệu về số lượng giao dịch của các khách hàng -> histogram
    - Thông tin về mức chi tiêu trung bình, trung vị mức chi tiêu, độ lệch chuẩn mức chi tiêu, các giá trị phân vị thứ 25 và 75, mức chi tiêu thấp nhất và cao nhất,..




