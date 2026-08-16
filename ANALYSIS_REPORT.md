# Olist E-commerce Analysis Report

## Overview

This analysis examines 100,000+ e-commerce orders from the Olist Brazilian marketplace, 
covering product categories, seller performance, customer behavior, and delivery metrics.

## Key Findings

### 1. Product Categories
Query: Top 10 product categories by order volume
See: query_01_top_product_categories.csv

Household essentials (bed/bath/table, health/beauty, furniture) dominate, accounting for ~38,000 orders. Bed/bath/table leads significantly at 11,115 orders. This suggests customers prioritize practical necessities over non-essential items. A key insight for sellers and an indicator of Olist's market position.

### 2. Temporal Trends
Query: Orders by month over time

The platform shows clear growth trajectory: launching with minimal volume (4 orders in Sept 2016), 
rapidly scaling through 2017 (reaching 7,544 orders in Nov), and stabilizing around 6,000-7,000 
monthly orders by mid-2018. 2018 emerged as the peak year with the highest annual order volume, 
though the sharp decline in Sept-Oct 2018 (16 and 4 orders) suggests incomplete dataset coverage 
rather than actual business decline, as data collection likely ended mid-October.

See: query_05_orders_by_month.csv

### 3. Geographic Analysis
Query: Revenue by state

São Paulo dominates platform revenue with 5.2 million reais (~56% of total), more than 2.8x 
Rio de Janeiro's 1.8 million. The top three states (São Paulo, Rio, Minas Gerais) account for 
~73% of all revenue, reflecting Brazil's economic concentration in the Southeast. Northern 
states (Amazonas, Acre, Amapá, Roraima) contribute minimally, each under 25k reais, indicating 
significant geographic disparities in e-commerce adoption and purchasing power.

See: query_04_revenue_by_state.csv

### 4. Customer Satisfaction
Query: Average review score over time

Platform review scores stabilize around 4.1-4.2 throughout 2017-2018, indicating consistent 
quality despite scaling from 800 to 7,000+ monthly orders. Early volatility (1.0 in Sept 2016, 
5.0 in Dec 2016) reflects minimal order volumes and unreliable samples. A slight dip in late 
2017 (3.91 in Nov) recovers by mid-2018, suggesting the platform successfully maintained 
customer satisfaction as it matured. The sharp decline in Sept-Oct 2018 (1.80, 2.25) mirrors 
incomplete data from that period.

See: query_17_review_score_over_time.csv

### 5. Payment Methods
Query: Order distribution by payment type

Credit cards dominate with 79.7% of transactions (76,795 payments) and the highest average order 
value at 163.32 reais, suggesting convenience and installment options drive larger purchases. 
Boleto, a traditional Brazilian payment method, accounts for 20.5% of transactions but with lower 
average value (145.03 reais), indicating it serves cost-conscious customers. Vouchers average 
just 65.70 reais, used primarily for smaller purchases, while debit cards remain underutilized 
(1.6%). This payment mix reflects Brazil's credit-heavy e-commerce ecosystem with credit card 
installments enabling higher basket sizes.

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
