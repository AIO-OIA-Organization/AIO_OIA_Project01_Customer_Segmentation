import pandas as pd
from src.processors.data_processor_base import DataProcessorBase
from src.interfaces.data_processor_interface import IDataProcessor

class CSVProcessor(DataProcessorBase, IDataProcessor):

    def __init__(self, input_path: str, encoding: str = "utf-8"):
        self.input_path = input_path
        self.encoding = encoding

    def read(self) -> pd.DataFrame:
        df = pd.read_csv(self.input_path, encoding=self.encoding)
        return df

    def export(self, df: pd.DataFrame, output_path: str) -> None:
        df.to_csv(output_path, index=False, encoding=self.encoding)
        print(f"Đã lưu file cleaned thành công tại: {output_path}")
        print(f"Kích thước cuối cùng: {df.shape[0]} dòng x {df.shape[1]} cột")
        print(f"Số khách hàng cuối cùng: {df['CustomerID'].nunique()}")

    def filter_by_country(self, df: pd.DataFrame, country: str) -> pd.DataFrame:
        return df[df['Country'] == country].copy()

    def handle_missing_values(self, df: pd.DataFrame, subsets: list[str]) -> pd.DataFrame:
        # Luôn xoá NaN trong CustomerID vì nó bắt buộc cho RFM
        required_cols = list(set(subsets + ['CustomerID']))
        df = df.dropna(subset=required_cols).copy()
        return df

    def handle_duplicates(self, df: pd.DataFrame, subsets: list[str]) -> pd.DataFrame:
        df = df.drop_duplicates(subset=subsets, keep='first').reset_index(drop=True).copy()
        return df

    def handle_cancelled_transactions(self, df: pd.DataFrame, key: str, character: str) -> pd.DataFrame:
        df = df[~df[key].astype(str).str.startswith(character, na=False)].copy()
        return df

    def handle_invalid_quantity(self, df: pd.DataFrame) -> pd.DataFrame:
        invalid = df['Quantity'] <= 0
        df = df[~invalid].copy()
        return df

    def handle_invalid_price(self, df: pd.DataFrame) -> pd.DataFrame:
        invalid = df['UnitPrice'] <= 0
        df = df[~invalid].copy()
        return df

    def create_total_price_column(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
        return df   