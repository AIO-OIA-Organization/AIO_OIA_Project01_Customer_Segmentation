import pandas as pd
from src.utilities.eda_visualizer import EDAVisualizer
from src.processors.csv_eda import CsvEDA
import matplotlib.pyplot as plt

class EDAOrchestrator:
    
    def __init__(self, analyzer: CsvEDA, visualizer: EDAVisualizer = None):
        self.analyzer = analyzer or CsvEDA(pd.DataFrame())
        self.visualizer = visualizer or EDAVisualizer()
    
    def revenue_trend_orchestrator(self, df: pd.DataFrame, freq: str = 'M'):
        result = self.analyzer.analyze_revenue_trend(df, freq=freq)
        fig, ax = self.visualizer.plot_revenue_trend(result, freq=freq)
        return fig, ax
    
    def orders_by_trend_orchestrator(self, df: pd.DataFrame, freq: str = 'weekday'):
        result = self.analyzer.analyze_orders_by_trend(df, freq=freq)
        fig, ax = self.visualizer.plot_orders_by_trend(result, freq=freq)
        return fig, ax
    
    def top_products_orchestrator(self, df: pd.DataFrame, top_n: int = 10, by: str = 'revenue'):
        result = self.analyzer.analyze_top_product(df, top_n=top_n, by=by)
        fig, ax = self.visualizer.plot_top_products(result, top_n=top_n, by=by)
        return fig, ax
    
    def customer_behavior_orchestrator(self, df: pd.DataFrame):
        report = self.analyzer.analyze_customer_behavior(df)
        fig, axes = self.visualizer.plot_customer_spending_distribution(df)

        print(f"\n PHÂN TÍCH HÀNH VI KHÁCH HÀNG")
        print("\n THỐNG KÊ CHUNG:")
        print(f"  Tổng số khách hàng : {report['total_customers']:,}")
        print(f"  Tổng số đơn hàng   : {report['total_orders']:,}")
        print(f"  Giá trị TB/đơn hàng: £{report['avg_order_value']:.2f}")
            
        print("\n CHI TIÊU KHÁCH HÀNG:")
        spending = report['spending_stats']
        print(f"  Số khách   : {int(spending['count']):,}")
        print(f"  Trung bình : £{spending['mean']:.2f}")
        print(f"  Độ lệch chuẩn: £{spending['std']:.2f}")
        print(f"  Tối thiểu  : £{spending['min']:.2f}")
        print(f"  25%ile     : £{spending['25%']:.2f}")
        print(f"  Median     : £{spending['50%']:.2f}")
        print(f"  75%ile     : £{spending['75%']:.2f}")
        print(f"  Tối đa     : £{spending['max']:,.2f}")
        
        print("\n HÀNH VI MUA HÀNG:")
        transactions = report['transaction_stats']
        print(f"  Trung bình : {transactions['mean']:.2f} lần/khách")
        print(f"  Tối thiểu  : {int(transactions['min'])} lần")
        print(f"  Tối đa     : {int(transactions['max'])} lần")

        return fig, axes