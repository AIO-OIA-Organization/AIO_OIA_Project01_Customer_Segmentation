from datetime import datetime
from typing import Optional

import pandas as pd

from src.interfaces.rfm_calculator_interface import IRFMCalculator


class RFMCalculator(IRFMCalculator):
    def build_rfm_table(self, df: pd.DataFrame, reference_date: Optional[datetime] = None) -> pd.DataFrame:
        df = df.copy()
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']) # Days since the customer's last purchase 

        if reference_date is None:
            reference_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

        rfm = (
            df.groupby('CustomerID')
            .agg(
                Recency=('InvoiceDate', lambda x: (reference_date - x.max()).days),
                Frequency=('InvoiceNo', 'nunique'),
                Monetary=('TotalPrice', 'sum'),
            )
            .reset_index()
        )
        return rfm

    def score_rfm(self, rfm_df: pd.DataFrame, n_bins: int = 5) -> pd.DataFrame:
        rfm = rfm_df.copy()

        r_cut = pd.qcut(rfm['Recency'], q=n_bins, duplicates='drop')
        f_cut = pd.qcut(rfm['Frequency'], q=n_bins, duplicates='drop')
        m_cut = pd.qcut(rfm['Monetary'], q=n_bins, duplicates='drop')

        n_r = r_cut.cat.categories.size

        # Recency: lower is better → invert codes so highest score = most recent
        rfm['R_Score'] = (n_r - r_cut.cat.codes).astype(int)
        # Frequency and Monetary: higher is better → higher code = higher score
        rfm['F_Score'] = (f_cut.cat.codes + 1).astype(int)
        rfm['M_Score'] = (m_cut.cat.codes + 1).astype(int)

        rfm['RFM_Score'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']
        return rfm
