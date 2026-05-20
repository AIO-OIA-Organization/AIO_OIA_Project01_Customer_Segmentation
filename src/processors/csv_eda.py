import pandas as pd
import os
import json
from src.processors.eda_processor_base import EDAProcessorBase
from src.interfaces.eda_processor_interface import IEDAProcessor
from src.utilities.convert_data_type import ConvertDataType

class CsvEDA(EDAProcessorBase, IEDAProcessor):

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def load_data(self) -> pd.DataFrame:
        return self.df

    def export_results(self, results: dict, output_path: str = '../data/processed/eda_results') -> None:
        os.makedirs(output_path, exist_ok=True)
        figures = results.get('figures', {})
        for name, fig in figures.items():
            if fig is not None:
                filepath = os.path.join(output_path, f"{name}.png")
                fig.savefig(filepath, dpi=200, bbox_inches='tight')
                print(f"Export PNG: {filepath}")

    def analyze_revenue_trend(self, df: pd.DataFrame, freq: str = 'M') -> pd.DataFrame:
        df = df.copy()
        freq_map = {
            'M': 'Month',
            'Q': 'Quarter',
            'Y': 'Year',
        }
        if freq not in freq_map.keys():
            raise ValueError(f"freq='{freq}'không hỗ trợ. Cần chọn: {list(freq_map.keys())}")
        col = freq_map[freq]
        df[col] = df['InvoiceDate'].dt.to_period(freq)
        df = ConvertDataType(column_name=col, target_type=str).convert(df)
        
        result = df.groupby(col)['TotalPrice'].sum().reset_index()
        result = result.rename(columns={'TotalPrice': 'Revenue'})
        return result

    def analyze_orders_by_trend(self, df: pd.DataFrame, freq: str = 'weekday') -> pd.DataFrame:
        df = df.copy()
        supported_freqs = ['weekday', 'hour']
        if freq not in supported_freqs:
            raise ValueError(f"freq='{freq}' không hỗ trợ. Cần chọn: {supported_freqs}")
        if freq == 'weekday': #barchat
            df['Period'] = df['InvoiceDate'].dt.day_name()
            weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            result = (
                    df.groupby('Period').size()
                    .reindex(weekday_order, fill_value=0)  
                    .reset_index(name='Order_Count'))
        elif freq == 'hour': #heatmap
            df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()
            df['HourOfDay'] = df['InvoiceDate'].dt.hour
            result = df[['DayOfWeek', 'HourOfDay', 'InvoiceDate']]
        return result

    def analyze_top_product(self, df: pd.DataFrame, top_n: int, by: str = 'revenue') -> pd.DataFrame:
        df = df.copy()
        supported_freqs = ['revenue', 'quantity']
        if by not in supported_freqs:
            raise ValueError(f"by='{by}' không hỗ trợ. Cần chọn: {supported_freqs}")
        
        product_stats = (
            df.groupby(['StockCode', 'Description'])
            .agg({'TotalPrice': 'sum', 'Quantity': 'sum'})
            .reset_index()
        )
        if by == 'revenue':
            product_stats = product_stats.sort_values('TotalPrice', ascending=False)
        elif by == 'quantity':
            product_stats = product_stats.sort_values('Quantity', ascending=False)
        product_stats = product_stats.rename(columns={'TotalPrice': 'Revenue'})
        return product_stats.head(top_n)

    def analyze_customer_behavior(self, df: pd.DataFrame) -> dict:
            df = df.copy()

            customer_spending = df.groupby('CustomerID')['TotalPrice'].sum()
            customer_transactions = df.groupby('CustomerID')['InvoiceNo'].nunique()
            order_totals = df.groupby('InvoiceNo')['TotalPrice'].sum()

            stats = {
                'total_customers': int(customer_spending.index.nunique()),
                'total_orders': int(df['InvoiceNo'].nunique()),
                'avg_order_value': float(order_totals.mean()),
                'avg_orders_per_customer': float(customer_transactions.mean()),
                'spending_stats': customer_spending.describe().to_dict(),
                'transaction_stats': customer_transactions.describe().to_dict(),
                'spending_distribution': customer_spending,
                'transaction_distribution': customer_transactions
            }
            return stats
