import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
from scipy import stats

class EDAVisualizer:
    def __init__(self):
        pass

    def plot_revenue_trend(self, df: pd.DataFrame, freq: str = 'M'):
        freq_map = {
            'M': 'Month', 
            'Q': 'Quarter', 
            'Y': 'Year'
        }
        if freq not in freq_map:
            raise ValueError(f"freq='{freq}'không hỗ trợ. Cần chọn: {list(freq_map.keys())}")
        
        col = freq_map[freq]

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df[col], df['Revenue'],
                color='#1D9E75', linewidth=2.5, marker='o', markersize=5)
        ax.fill_between(df[col], df['Revenue'],
                        alpha=0.15, color='#1D9E75')
        ax.set_title(f'Revenue Trend by {col}', fontsize=16)
        ax.set_xlabel(col, fontsize=12)
        ax.set_ylabel('Revenue (£)')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'£{x/1000:.0f}K'))
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        plt.show()
        return fig,ax

    def plot_orders_by_trend(self, df: pd.DataFrame, freq: str = 'weekday'):
        supported_freqs = ['weekday', 'hour']
        if freq not in supported_freqs:
            raise ValueError(f"freq='{freq}' không hỗ trợ. Cần chọn: {supported_freqs}")
        
        fig, ax = plt.subplots(figsize=(12, 5))
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if freq == 'weekday':
            df_sorted = df.set_index('Period').reindex(day_order).reset_index()
            ax.bar(df_sorted['Period'], df_sorted['Order_Count'], color='#1D9E75', alpha=0.8, edgecolor='black')
            ax.set_title('Orders by Day of Week', fontsize=16)
            ax.set_xlabel('Day of Week', fontsize=12)
            ax.set_ylabel('Number of Orders', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            plt.tight_layout()
            plt.show()
            return fig, ax
        
        elif freq == 'hour':
            day_hour_counts = df.groupby(['DayOfWeek', 'HourOfDay']).size().unstack(fill_value=0)
            day_hour_counts = day_hour_counts.reindex(day_order)
            sns.heatmap(day_hour_counts, cmap='viridis', ax=ax, annot=False)
            ax.set_title('Orders by Day and Hour', fontsize=14, fontweight='bold')
            ax.set_xlabel('Hour of Day', fontsize=12)
            ax.set_ylabel('Day of Week', fontsize=12)
       
            plt.tight_layout()
            plt.show()
            return fig, ax


    def plot_top_products(self, df: pd.DataFrame, top_n: int, by: str = 'revenue'):
        supported_freqs = ['quantity', 'revenue']
        if by not in supported_freqs:
            raise ValueError(f"by='{by}' không hỗ trợ. Cần chọn: {supported_freqs}")
        fig, ax = plt.subplots(figsize=(12, 6))
        if by == 'revenue':
            df_sorted = df.sort_values('Revenue', ascending=False).head(top_n)
            ax.barh(df_sorted['Description'], df_sorted['Revenue'], color='#1D9E75', alpha=0.8)
            ax.set_xlabel('Revenue')
            ax.set_title(f'Top {top_n} products by revenue')
            for i, v in enumerate(df_sorted['Revenue']):
                ax.text(v, i, f'{v:,.0f}', va='center', ha='left', fontsize=9)
        
        elif by == 'quantity':
            df_sorted = df.sort_values('Quantity', ascending=False).head(top_n)
            ax.barh(df_sorted['Description'], df_sorted['Quantity'], color='#1D9E75', alpha=0.8)
            ax.set_xlabel('Quantity Sold')
            ax.set_title(f'Top {top_n} products by quantity sold')
            for i, v in enumerate(df_sorted['Quantity']):
                ax.text(v, i, f'{v:,}', va='center', ha='left', fontsize=9)
        
        ax.set_ylabel('Product Name')
        plt.tight_layout()
        return fig, ax

    def plot_customer_spending_distribution(self, df: pd.DataFrame):
        from scipy.stats import gaussian_kde

        fig, axes = plt.subplots(1, 2, figsize=(15, 5))

        # Theo tổng giao dịch
        transactions_per_customer = df.groupby("CustomerID")["InvoiceNo"].nunique()
        trans_filtered = transactions_per_customer[
            transactions_per_customer < transactions_per_customer.quantile(0.99)
        ]
        n_trans = len(trans_filtered)

        axes[0].hist(trans_filtered, bins=30, color='#1D9E75', alpha=0.7, edgecolor='black')

        kde_trans = gaussian_kde(trans_filtered)
        x_trans = np.linspace(trans_filtered.min(), trans_filtered.max(), 200)
        bin_width_trans = (trans_filtered.max() - trans_filtered.min()) / 30
        axes[0].plot(x_trans, kde_trans(x_trans) * n_trans * bin_width_trans,
                    color='darkgreen', linewidth=2, label='KDE')

        axes[0].set_title("Distribution of Number of Orders per Customer (99%ile)", fontsize=12, fontweight='bold')
        axes[0].set_xlabel("Number of Orders", fontsize=11)
        axes[0].set_ylabel("Number of Customers", fontsize=11)
        axes[0].grid(axis='y', alpha=0.3)
        axes[0].legend()

        # Theo tổng chi tiêu
        spend_per_customer = df.groupby("CustomerID")["TotalPrice"].sum()
        spend_filtered = spend_per_customer[
            spend_per_customer < spend_per_customer.quantile(0.99)
        ]
        n_spend = len(spend_filtered)

        axes[1].hist(spend_filtered, bins=30, color='#D65A5A', alpha=0.7, edgecolor='black')

        kde_spend = gaussian_kde(spend_filtered)
        x_spend = np.linspace(spend_filtered.min(), spend_filtered.max(), 200)
        bin_width_spend = (spend_filtered.max() - spend_filtered.min()) / 30
        axes[1].plot(x_spend, kde_spend(x_spend) * n_spend * bin_width_spend,
                    color='darkred', linewidth=2, label='KDE')

        axes[1].set_title("Distribution of Total Spending per Customer (99%ile)", fontsize=12, fontweight='bold')
        axes[1].set_xlabel("Total Spending (GBP)", fontsize=11)
        axes[1].set_ylabel("Number of Customers", fontsize=11)
        axes[1].grid(axis='y', alpha=0.3)
        axes[1].legend()

        plt.tight_layout()
        return fig, axes
    
