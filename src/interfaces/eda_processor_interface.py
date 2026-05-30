from abc import ABC, abstractmethod
import pandas as pd

class IEDAProcessor(ABC):
    @abstractmethod
    def analyze_revenue_trend(self, df: pd.DataFrame, freq: str = 'M') -> pd.DataFrame:
        ...

    @abstractmethod
    def analyze_orders_by_trend(self, df: pd.DataFrame, freq: str = 'weekday') -> pd.DataFrame:
        ...

    @abstractmethod
    def analyze_top_product(self, df: pd.DataFrame, top_n: int, by: str ='revenue') -> pd.DataFrame:
        ...

    @abstractmethod
    def analyze_customer_behavior(self, df: pd.DataFrame) -> dict:
        ...