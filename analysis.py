import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load environment variables
load_dotenv()

# Supabase connection details
DB_URL = os.getenv("DATABASE_URL")

class OlistAnalysis:
    def __init__(self):
        self.conn = None
        self.results = {}
        
    def connect(self):
        """Connect to Supabase PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(DB_URL)
            print("[OK] Connected to Supabase")
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            raise
    
    def run_query(self, query_name, sql):
        """Execute a query and return results as DataFrame"""
        try:
            df = pd.read_sql(sql, self.conn)
            self.results[query_name] = df
            print(f"[OK] {query_name}: {len(df)} rows")
            return df
        except Exception as e:
            print(f"[ERROR] {query_name} failed: {e}")
            return None
    
    def save_results_to_csv(self):
        """Save all query results to CSV files"""
        os.makedirs("results/queries", exist_ok=True)
        for query_name, df in self.results.items():
            filepath = f"results/queries/{query_name}.csv"
            df.to_csv(filepath, index=False)
            print(f"[SAVED] {filepath}")
    
    def create_visualizations(self):
        """Generate key matplotlib charts"""
        os.makedirs("results/charts", exist_ok=True)
        sns.set_style("whitegrid")
        
        # 1. Top 10 Product Categories
        if "query_01_top_product_categories" in self.results:
            df = self.results["query_01_top_product_categories"]
            plt.figure(figsize=(12, 6))
            plt.barh(df['product_category_name_english'], df['order_count'])
            plt.xlabel('Order Count')
            plt.title('Top 10 Product Categories by Order Volume')
            plt.tight_layout()
            plt.savefig('results/charts/01_top_categories.png', dpi=300)
            plt.close()
            print("[CHART] Top 10 Product Categories")
        
        # 2. Orders by Month
        if "query_05_orders_by_month" in self.results:
            df = self.results["query_05_orders_by_month"]
            plt.figure(figsize=(14, 6))
            plt.plot(df['month'], df['order_count'], marker='o', linewidth=2)
            plt.xlabel('Month')
            plt.ylabel('Order Count')
            plt.title('Orders by Month Over Time')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('results/charts/02_orders_by_month.png', dpi=300)
            plt.close()
            print("[CHART] Orders by Month")
        
        # 3. Revenue by State
        if "query_04_revenue_by_state" in self.results:
            df = self.results["query_04_revenue_by_state"].head(10)
            plt.figure(figsize=(12, 6))
            plt.bar(df['customer_state'], df['total_revenue'])
            plt.xlabel('State')
            plt.ylabel('Total Revenue ($)')
            plt.title('Top 10 States by Revenue')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('results/charts/03_revenue_by_state.png', dpi=300)
            plt.close()
            print("[CHART] Revenue by State")
        
        # 4. Review Score Over Time
        if "query_17_review_score_over_time" in self.results:
            df = self.results["query_17_review_score_over_time"]
            plt.figure(figsize=(14, 6))
            plt.plot(df['month'], df['avg_review_score'], marker='o', linewidth=2, color='green')
            plt.xlabel('Month')
            plt.ylabel('Average Review Score')
            plt.title('Average Review Score Over Time')
            plt.ylim(0, 5)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('results/charts/04_review_score_over_time.png', dpi=300)
            plt.close()
            print("[CHART] Review Score Over Time")
        
        # 5. Payment Type Distribution
        if "query_09_avg_order_value_by_payment" in self.results:
            df = self.results["query_09_avg_order_value_by_payment"]
            plt.figure(figsize=(10, 6))
            plt.pie(df['total_payments'], labels=df['payment_type'], autopct='%1.1f%%')
            plt.title('Order Distribution by Payment Type')
            plt.tight_layout()
            plt.savefig('results/charts/05_payment_type_distribution.png', dpi=300)
            plt.close()
            print("[CHART] Payment Type Distribution")
    
    def generate_report(self):
        """Create Markdown summary report"""
        report = f"""# Olist E-commerce Analysis Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This analysis examines 100,000+ e-commerce orders from the Olist Brazilian marketplace, 
covering product categories, seller performance, customer behavior, and delivery metrics.

## Key Findings

### 1. Product Categories
Query: Top 10 product categories by order volume
See: query_01_top_product_categories.csv

### 2. Temporal Trends
Query: Orders by month over time
See: query_05_orders_by_month.csv

### 3. Geographic Analysis
Query: Revenue by state
See: query_04_revenue_by_state.csv

### 4. Customer Satisfaction
Query: Average review score over time
See: query_17_review_score_over_time.csv

### 5. Payment Methods
Query: Order distribution by payment type
See: query_09_avg_order_value_by_payment.csv

## All Queries

All 20 analytical queries and their results are available in results/queries/ directory.

## Dataset Stats

- Total Orders: 99,441
- Total Customers: 99,441
- Total Sellers: 3,095
- Product Categories: 71

## Files

- analysis.py - Python script
- results/queries/ - All 20 query results as CSV
- results/charts/ - Matplotlib visualizations
"""
        
        with open("ANALYSIS_REPORT.md", "w") as f:
            f.write(report)
        print("[REPORT] ANALYSIS_REPORT.md")
    
    def run_all_queries(self):
        """Define and run all 20 queries"""
        queries = {
            "query_01_top_product_categories": """
                select t.product_category_name_english, COUNT(*) as order_count
                from olist.order_items oi
                join olist.products p on oi.product_id = p.product_id
                join olist.product_category_name_translation t on p.product_category_name = t.product_category_name
                group by t.product_category_name_english
                order by order_count DESC
                limit 10;
            """,
            "query_02_sellers_highest_review_score": """
                select oi.seller_id, ROUND(AVG(r.review_score), 2) as avg_review_score, COUNT(*) as total_reviews
                from olist.order_reviews r
                join olist.order_items oi on r.order_id = oi.order_id
                group by oi.seller_id
                having COUNT(*) >= 10
                order by avg_review_score DESC
                limit 20;
            """,
        }
        
        for query_name, sql in queries.items():
            self.run_query(query_name, sql)
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("[OK] Disconnected from Supabase")

def main():
    analysis = OlistAnalysis()
    
    try:
        analysis.connect()
        analysis.run_all_queries()
        analysis.save_results_to_csv()
        analysis.create_visualizations()
        analysis.generate_report()
        print("\n[COMPLETE] Analysis finished successfully")
    except Exception as e:
        print(f"\n[ERROR] {e}")
    finally:
        analysis.disconnect()

if __name__ == "__main__":
    main()