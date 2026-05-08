from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class ISegmentor(ABC):
    @abstractmethod
    def find_optimal_k(self, X: np.ndarray, k_range: range) -> dict:
        ...

    @abstractmethod
    def fit(self, X: np.ndarray, n_clusters: int) -> None:
        ...

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        ...

    @abstractmethod
    def assign_segment_labels(self, rfm_df: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
        ...
