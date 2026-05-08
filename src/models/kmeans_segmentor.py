from typing import Optional

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from src.interfaces.segmentor_interface import ISegmentor

_SEGMENT_NAMES = [
    "Champions",
    "Loyal Customers",
    "Potential Loyalists",
    "At Risk",
    "Lost Customers",
]


class KMeansSegmentor(ISegmentor):
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.model: Optional[KMeans] = None
        self._n_clusters: Optional[int] = None

    def find_optimal_k(self, X: np.ndarray, k_range: range = range(2, 11)) -> dict:
        X_scaled = StandardScaler().fit_transform(np.log1p(X))
        inertias, silhouette_scores = [], []

        for k in k_range:
            km = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            labels = km.fit_predict(X_scaled)
            inertias.append(km.inertia_)
            silhouette_scores.append(silhouette_score(X_scaled, labels))

        return {
            'k_range': list(k_range),
            'inertias': inertias,
            'silhouette_scores': silhouette_scores,
        }

    def fit(self, X: np.ndarray, n_clusters: int) -> None:
        X_scaled = self.scaler.fit_transform(np.log1p(X))
        self.model = KMeans(n_clusters=n_clusters, random_state=self.random_state, n_init=10)
        self.model.fit(X_scaled)
        self._n_clusters = n_clusters

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise RuntimeError("Call fit() before predict().")
        return self.model.predict(self.scaler.transform(np.log1p(X)))

    def assign_segment_labels(self, rfm_df: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
        rfm = rfm_df.copy()
        rfm['Cluster'] = labels

        # Score each cluster: recent + frequent + high-value customers score highest
        centroids = rfm.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean()
        centroids['Score'] = centroids['Frequency'] * centroids['Monetary'] / (centroids['Recency'] + 1)

        # Rank 0 = best cluster
        rank_map = (centroids['Score'].rank(ascending=False).astype(int) - 1).to_dict()

        segment_names = _SEGMENT_NAMES[:]
        while len(segment_names) < self._n_clusters:
            segment_names.append(f"Segment {len(segment_names) + 1}")

        rfm['Segment'] = rfm['Cluster'].map(lambda c: segment_names[rank_map[c]])
        return rfm