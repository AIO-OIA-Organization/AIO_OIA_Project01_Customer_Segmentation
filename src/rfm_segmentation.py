import pandas as pd

from src.models.calculators.rfm_calculator import RFMCalculator
from src.models.kmeans_segmentor import KMeansSegmentor
from src.processors.csv_processor import CSVProcessor


class RFMSegmentationPipeline:
    def __init__(
        self,
        input_path: str,
        output_path: str,
        n_clusters: int = 4,
        rfm_table_path: str | None = None,
        random_state: int = 42,
    ):
        self.processor = CSVProcessor(input_path=input_path)
        self.rfm_calculator = RFMCalculator()
        self.segmentor = KMeansSegmentor()
        self.output_path = output_path
        self.n_clusters = n_clusters
        self.rfm_table_path = rfm_table_path

    def run(self) -> pd.DataFrame:
        df = self.processor.read()

        # Minimal cleaning for Online Retail-style datasets
        if "CustomerID" in df.columns:
            df = self.processor.handle_missing_values(df, subsets=["CustomerID"])

        if "InvoiceNo" in df.columns:
            df = self.processor.handle_cancelled_transactions(df, key="InvoiceNo", character="C")

        if "Quantity" in df.columns:
            df = self.processor.handle_invalid_quantity(df)

        if "UnitPrice" in df.columns:
            df = self.processor.handle_invalid_price(df)

        if "TotalPrice" not in df.columns:
            df = self.processor.create_total_price_column(df)

        rfm = self.rfm_calculator.build_rfm_table(df)
        rfm = self.rfm_calculator.score_rfm(rfm)

        if self.rfm_table_path:
            self.processor.export(rfm, self.rfm_table_path)

        X = rfm[['Recency', 'Frequency', 'Monetary']].values
        self.segmentor.fit(X, self.n_clusters)
        labels = self.segmentor.predict(X)
        rfm = self.segmentor.assign_segment_labels(rfm, labels)

        self.processor.export(rfm, self.output_path)
        return rfm
