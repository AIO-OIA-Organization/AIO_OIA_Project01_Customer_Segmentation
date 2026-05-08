from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

import pandas as pd


class IRFMCalculator(ABC):
    @abstractmethod
    def build_rfm_table(self, df: pd.DataFrame, reference_date: Optional[datetime] = None) -> pd.DataFrame:
        ...

    @abstractmethod
    def score_rfm(self, rfm_df: pd.DataFrame, n_bins: int = 5) -> pd.DataFrame:
        ...
