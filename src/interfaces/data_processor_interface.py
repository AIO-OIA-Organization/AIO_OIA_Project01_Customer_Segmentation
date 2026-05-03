from abc import ABC, abstractmethod
import pandas as pd

class IDataProcessor(ABC):
    @abstractmethod
    def filter_by_country(self, df: pd.DataFrame, country: str) -> pd.DataFrame:
        ...

    @abstractmethod
    def handle_missing_values(self, df: pd.DataFrame, subsets: str) -> pd.DataFrame:
        ...

    @abstractmethod
    def handle_duplicates(self, df: pd.DataFrame, subsets: list[str]) -> pd.DataFrame:
        ...

    @abstractmethod
    def handle_cancelled_transactions(self, df: pd.DataFrame, key: str, character: str) -> pd.DataFrame:
        ...

    @abstractmethod
    def handle_invalid_quantity(self, df: pd.DataFrame) -> pd.DataFrame:
        ...

    @abstractmethod
    def handle_invalid_price(self, df: pd.DataFrame) -> pd.DataFrame:
        ...

    @abstractmethod
    def create_total_price_column(self, df: pd.DataFrame) -> pd.DataFrame:
        ...