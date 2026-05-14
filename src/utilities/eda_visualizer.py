import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
from scipy import stats
from scipy.stats import gaussian_kde

class EDAVisualizer:
    def __init__(self):
        pass

    def plot_revenue_trend(self, df: pd.DataFrame, freq: str = 'M'):
        freq_map = {'M': 'Month', 'Q': 'Quarter', 'Y': 'Year'}
        if freq not in freq_map:
            raise ValueError(f"freq='{freq}' không hỗ trợ. Cần chọn: {list(freq_map.keys())}")
        col = freq_map[freq]

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df[col], df["Revenue"], marker="o", color="#1D9E75", linewidth=2.5, markersize=6)
        ax.fill_between(range(len(df)), df["Revenue"], alpha=0.15, color="#1D9E75")
        ax.set_title(f"Revenue Trend by {col}", fontsize=16)
        ax.set_xlabel(col, fontsize=12)
        ax.set_ylabel("Revenue (£)")
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig, ax


    def plot_orders_by_trend(self, df: pd.DataFrame, freq: str = 'weekday'):
        supported_freqs = ['weekday', 'hour']
        if freq not in supported_freqs:
            raise ValueError(f"freq='{freq}' không hỗ trợ. Cần chọn: {supported_freqs}")

        if freq == 'weekday':
            day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            df_sorted = df.set_index('Period').reindex(day_order).reset_index()
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.bar(df_sorted["Period"], df_sorted["Order_Count"], color="#1D9E75", edgecolor="black", alpha=0.8)
            ax.set_title("Orders by Day of Week", fontsize=16)
            ax.set_xlabel("Day of Week")
            ax.set_ylabel("Number of Orders")
            plt.xticks(rotation=45)
            plt.tight_layout()
            return fig, ax

        elif freq == 'hour':
            day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            day_hour_counts = df.groupby(['DayOfWeek','HourOfDay']).size().unstack(fill_value=0)
            day_hour_counts = day_hour_counts.reindex(day_order)
            fig, ax = plt.subplots(figsize=(12, 5))
            sns.heatmap(day_hour_counts, cmap="viridis", ax=ax)
            ax.set_title("Order by Day and Hour", fontsize=14, fontweight="bold")
            ax.set_xlabel("Hour of Day")
            ax.set_ylabel("Day of Week")
            plt.tight_layout()
            return fig, ax



    def plot_top_products(self, df: pd.DataFrame, top_n: int, by: str = 'revenue'):
        supported_freqs = ['quantity', 'revenue']
        if by not in supported_freqs:
            raise ValueError(f"by='{by}' không hỗ trợ. Cần chọn: {supported_freqs}")

        fig, ax = plt.subplots(figsize=(12, 6))
        if by == 'revenue':
            df_sorted = df.sort_values("Revenue", ascending=False).head(top_n)
            sns.barplot(data=df_sorted, y="Description", x="Revenue", color="#1D9E75", ax=ax)
            ax.set_title(f"Top {top_n} Products by Revenue")
            ax.set_xlabel("Revenue")
            ax.set_ylabel("Tên sản phẩm")
            for i, v in enumerate(df_sorted["Revenue"]):
                ax.text(v, i, f"{v:,.0f}", va="center", ha="left", fontsize=9)

        elif by == 'quantity':
            df_sorted = df.sort_values("Quantity", ascending=False).head(top_n)
            sns.barplot(data=df_sorted, y="Description", x="Quantity", color="#1D9E75", ax=ax)
            ax.set_title(f"Top {top_n} Products by Quantity")
            ax.set_xlabel("Quantity")
            ax.set_ylabel("Tên sản phẩm")
            for i, v in enumerate(df_sorted["Quantity"]):
                ax.text(v, i, f"{v:,}", va="center", ha="left", fontsize=9)

        plt.tight_layout()
        return fig, ax



    def plot_customer_spending_distribution(self, df: pd.DataFrame):
            fig, axes = plt.subplots(1, 2, figsize=(15, 5))

            # Theo số giao dịch
            transactions_per_customer = df.groupby("CustomerID")["InvoiceNo"].nunique()

            # Vẽ biểu đồ histogram
            axes[0].hist(transactions_per_customer, bins=30, color='#1D9E75', alpha=0.7, edgecolor='black')
            # Vẽ đường cong KDE
            kde_trans = gaussian_kde(transactions_per_customer)
            x_trans = np.linspace(transactions_per_customer.min(), transactions_per_customer.max(), 200)
            bin_width_trans = (transactions_per_customer.max() - transactions_per_customer.min()) / 30
            axes[0].plot(x_trans, kde_trans(x_trans) * len(transactions_per_customer) * bin_width_trans,
                        color='darkgreen', linewidth=2, label='KDE')
            axes[0].set_title("Distribution of Number of Orders per Customer", fontsize=12, fontweight='bold')
            axes[0].set_xlabel("Number of Orders", fontsize=11)
            axes[0].set_ylabel("Number of Customers", fontsize=11)
            axes[0].grid(axis='y', alpha=0.3)
            axes[0].legend()

            # Theo chi tiêu
            spend_per_customer = df.groupby("CustomerID")["TotalPrice"].sum()
            spend_filtered = spend_per_customer[
                spend_per_customer < spend_per_customer.quantile(0.99)
            ]
            n_spend = len(spend_filtered)

            # Vẽ biểu đồ histogram
            axes[1].hist(spend_filtered, bins=30, color='#D65A5A', alpha=0.7, edgecolor='black')
            # Vẽ đường cong KDE
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

    
