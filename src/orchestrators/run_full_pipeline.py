import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT.parent))

from src.processors.csv_processor import CSVProcessor
from src.processors.csv_eda import CsvEDA
from src.utilities.eda_visualizer import EDAVisualizer
from src.orchestrators.eda_orchestractor import EDAOrchestrator
from src.utilities.convert_data_type import ConvertDataType
from orchestrators.rfm_segmentation import RFMSegmentationPipeline


class FullCustomerSegmentationPipeline:
  
    def __init__(
        self,
        raw_data_path: str,
        target_country: str = 'United Kingdom',
        n_clusters: int = 4,
        random_state: int = 42
    ):
        self.raw_data_path = raw_data_path
        self.target_country = target_country
        self.n_clusters = n_clusters
        self.random_state = random_state
        
        # Define output paths
        self.project_root = PROJECT_ROOT
        self.data_processed = self.project_root / "data" / "processed"
        self.clean_data_path = str(self.data_processed / "clean_transactions.csv")
        self.eda_results_path = str(self.data_processed / "eda_results")
        self.rfm_table_path = str(self.data_processed / "rfm_table.csv")
        self.rfm_segments_path = str(self.data_processed / "rfm_segments.csv")
        
    def print_section(self, title: str):
        print(f"\n{'='*80}")
        print(f"{title}")
        print(f"{'='*80}\n")
    
    def data_cleaning(self):
        self.print_section("DATA CLEANING")

        print("Đọc dữ liệu gốc...")
        processor = CSVProcessor(input_path=self.raw_data_path)
        df_raw = processor.read()
        print(f"Kích thước: {df_raw.shape[0]:,} dòng x {df_raw.shape[1]} cột")
        print(f"Số khách: {df_raw['CustomerID'].nunique():,}")
        print(f"Top 3 quốc gia: \n{df_raw['Country'].value_counts().head(3).to_string()}\n")

        print(f"Lọc dữ liệu {self.target_country}...")
        df_uk = processor.filter_by_country(df_raw, country=self.target_country)
        uk_size_before = df_uk.shape
        uk_customer_before = df_uk['CustomerID'].nunique()
        print(f"Kích thước UK: {df_uk.shape[0]:,} dòng x {df_uk.shape[1]} cột")
        print(f"Số khách UK: {uk_customer_before:,}\n")

        print("Xử lý missing values...")
        missing_count_before = df_uk['CustomerID'].isna().sum()
        df_uk = processor.handle_missing_values(df_uk, subsets=['CustomerID'])
        print(f"Loại bỏ: {missing_count_before:,} dòng missing CustomerID\n")

        print("Chuyển đổi kiểu dữ liệu...")
        df_uk = ConvertDataType(column_name='CustomerID', target_type=int).convert(df_uk)
        df_uk = ConvertDataType(column_name='CustomerID', target_type=str).convert(df_uk)
        df_uk = ConvertDataType(column_name='InvoiceDate', target_type='datetime').convert(df_uk)
        print(df_uk[['CustomerID', 'InvoiceDate']].dtypes)

        print(" Xử lý giao dịch trùng...")
        duplicates_before = df_uk.duplicated(subset=['InvoiceNo', 'StockCode'], keep=False).sum()
        df_uk = processor.handle_duplicates(df_uk, subsets=['InvoiceNo', 'StockCode'])
        print(f"Loại bỏ: {duplicates_before:,} dòng trùng\n")

        print("Xử lý giao dịch bị hủy...")
        cancelled_count = df_uk['InvoiceNo'].astype(str).str.startswith('C').sum()
        df_uk = processor.handle_cancelled_transactions(df_uk, key='InvoiceNo', character='C')
        print(f"Loại bỏ: {cancelled_count:,} giao dịch bị hủy (C*)\n")

        print("Xử lý Quantity/Price âm...")
        invalid_qty = (df_uk['Quantity'] <= 0).sum()
        invalid_price = (df_uk['UnitPrice'] <= 0).sum()
        df_uk = processor.handle_invalid_quantity(df_uk)
        df_uk = processor.handle_invalid_price(df_uk)
        print(f"Loại bỏ: {invalid_qty:,} dòng Quantity <= 0")
        print(f"Loại bỏ: {invalid_price:,} dòng UnitPrice <= 0\n")

        print("Tạo cột TotalPrice...")
        df_uk = processor.create_total_price_column(df_uk)
        print(f"TotalPrice = Quantity × UnitPrice\n")

        print("Xuất cleaned dataset...")
        processor.export(df_uk, self.clean_data_path)
        print(f"File: {self.clean_data_path}\n")

        print("SUMMARY CLEANING:")
        print(f"Trước: {uk_size_before[0]:,} dòng x {uk_size_before[1]} cột ({uk_customer_before:,} khách)")
        print(f"Sau:   {df_uk.shape[0]:,} dòng x {df_uk.shape[1]} cột ({df_uk['CustomerID'].nunique():,} khách)")
        print(f"Loại bỏ: {((uk_size_before[0] - df_uk.shape[0]) / uk_size_before[0] * 100):.2f}% dữ liệu\n")

        return df_uk

    def exploratory_data_analysis(self, df_clean: pd.DataFrame):

        self.print_section("EXPLORATORY DATA ANALYSIS")

        print("Khởi tạo EDA components...")
        analyzer = CsvEDA(df_clean)
        visualizer = EDAVisualizer()
        eda_orchestrator = EDAOrchestrator(analyzer=analyzer, visualizer=visualizer)

        results = {'figures': {}}

        print("\nPhân tích doanh thu theo thời gian...")
        fig_monthly, _ = eda_orchestrator.revenue_trend_orchestrator(df_clean, freq='M')
        results['figures']['revenue_trend_monthly'] = fig_monthly
        print("Revenue trend (Monthly)")
        
        fig_quarterly, _ = eda_orchestrator.revenue_trend_orchestrator(df_clean, freq='Q')
        results['figures']['revenue_trend_quarterly'] = fig_quarterly
        print("Revenue trend (Quarterly)")

        print("\nPhân tích thời gian mua hàng...")
        fig_weekday, _ = eda_orchestrator.orders_by_trend_orchestrator(df_clean, freq='weekday')
        results['figures']['orders_by_weekday'] = fig_weekday
        print("Orders by day of week")

        fig_hour, _ = eda_orchestrator.orders_by_trend_orchestrator(df_clean, freq='hour')
        results['figures']['orders_by_hour'] = fig_hour
        print("Orders by hour of day")

        print("\nPhân tích sản phẩm bán chạy...")
        fig_revenue, _ = eda_orchestrator.top_products_orchestrator(df_clean, top_n=10, by='revenue')
        results['figures']['top_products_revenue'] = fig_revenue

        print("Top 10 products (by revenue)")
        fig_quantity, _ = eda_orchestrator.top_products_orchestrator(df_clean, top_n=10, by='quantity')
        results['figures']['top_products_quantity'] = fig_quantity
        print("Top 10 products (by quantity)")

        print("\nPhân tích hành vi khách hàng...")
        fig_behavior, _ = eda_orchestrator.customer_behavior_orchestrator(df_clean)
        results['figures']['customer_behavior'] = fig_behavior
        print("Customer spending distribution")

        print("\nXuất EDA results (PNG)...")
        analyzer.export_results(results, output_path=self.eda_results_path)
        print(f"Folder: {self.eda_results_path}\n")

    def rfm_segmentation(self):

        self.print_section("RFM + K-MEANS SEGMENTATION")

        print("Khởi tạo RFM Pipeline...")
        rfm_pipeline = RFMSegmentationPipeline(
            input_path=self.clean_data_path,
            output_path=self.rfm_segments_path,
            n_clusters=self.n_clusters,
            rfm_table_path=self.rfm_table_path,
            random_state=self.random_state
        )
        print(f"Config: K={self.n_clusters}, Random State={self.random_state}\n")

        print("Chạy RFM Pipeline...")
        rfm_results = rfm_pipeline.run()

        print(f"\nRFM RESULTS SUMMARY:")
        print(f"Số khách: {len(rfm_results):,}")
        print(f"Số segment: {rfm_results['Segment'].nunique()}")
        print(f"\nDistribution:")
        print(rfm_results['Segment'].value_counts().sort_index().to_string())

        print(f"\n Output files:")
        print(f"{self.rfm_table_path}")
        print(f"{self.rfm_segments_path}\n")

        return rfm_results
    
    def run(self):
        print("FULL CUSTOMER SEGMENTATION PIPELINE")

        df_clean = self.data_cleaning()
        self.exploratory_data_analysis(df_clean)
    
        rfm_results = self.rfm_segmentation()
        
        self.print_section("PIPELINE COMPLETE")
        print("Output Files:")
        print(f"1. {self.clean_data_path}")
        print(f"2. {self.eda_results_path}/")
        print(f"3. {self.rfm_table_path}")
        print(f"4. {self.rfm_segments_path}")
        print()
        
        return {
            'clean_data': df_clean,
            'rfm_segments': rfm_results
        }


if __name__ == "__main__":
    RAW_DATA_PATH = str(PROJECT_ROOT / "data" / "raw" / "online_retail.csv")
    TARGET_COUNTRY = 'United Kingdom'
    N_CLUSTERS = 4
    RANDOM_STATE = 42
    
    pipeline = FullCustomerSegmentationPipeline(
        raw_data_path=RAW_DATA_PATH,
        target_country=TARGET_COUNTRY,
        n_clusters=N_CLUSTERS,
        random_state=RANDOM_STATE
    )

    results = pipeline.run()
