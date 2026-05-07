import pandas as pd
from abc import ABC, abstractmethod

class DataProcessorBase(ABC):
    @abstractmethod
    def read(self) -> pd.DataFrame:
        ...

    @abstractmethod
    def export(self, df: pd.DataFrame, output_path: str) -> None:
        ...