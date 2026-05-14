import pandas as pd
from abc import ABC, abstractmethod

class EDAProcessorBase(ABC):
    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        ...

    @abstractmethod
    def export_results(self, results: dict, output_path: str) -> None:
        ...