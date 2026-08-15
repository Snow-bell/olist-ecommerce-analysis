# Olist E-commerce Analysis

Analysis of 100,000+ Brazilian e-commerce orders using PostgreSQL and Python.

## Quick Start

1. Clone repo
```bash
git clone https://github.com/YOUR_USERNAME/olist-ecommerce-analysis.git
cd olist-ecommerce-analysis
```

2. Create `.env` file
```bash
cp .env.example .env
# Add your DATABASE_URL
```

3. Install and run
```bash
pip install -r requirements.txt
python analysis.py
```

## What It Does

Runs 20 SQL queries analyzing:
- Top product categories
- Seller performance and reviews
- Delivery metrics
- Revenue by region
- Customer behavior
- Payment trends

Results are exported as CSV and visualized with matplotlib.

## Dataset

- 99,441 orders
- 99,441 customers
- 3,095 sellers
- 71 product categories

## Output

```
results/
├── queries/ # 20 CSV files with results
└── charts/ # Matplotlib visualizations
```

## Technologies

- PostgreSQL (Supabase)
- Python, pandas, matplotlib
- 20 analytical SQL queries