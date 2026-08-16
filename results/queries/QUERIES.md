# Analytical Queries

This document contains all 20 SQL queries used in the Olist e-commerce analysis.

## 1. Top 10 Product Categories by Order Volume

What are the top 10 product categories by total volume of orders?

```sql
select t.product_category_name_english, COUNT(*) as order_count
from olist.order_items oi
join olist.products p on oi.product_id = p.product_id
join olist.product_category_name_translation t on p.product_category_name = t.product_category_name
group by t.product_category_name_english
order by order_count DESC
limit 10;
```

## 2. Sellers with Highest Average Review Score

Which sellers have the highest average review score?

```sql
select oi.seller_id, ROUND(AVG(r.review_score), 2) as avg_review_score, COUNT(*) as total_reviews
from olist.order_reviews r
join olist.order_items oi on r.order_id = oi.order_id
group by oi.seller_id
having COUNT(*) >= 10
order by avg_review_score DESC
limit 20;
```

## 3. Average Delivery Time

What is the average time between order placement and delivery confirmation?

```sql
select ROUND(AVG(extract(EPOCH from (order_delivered_customer_date - order_purchase_timestamp)) / 86400), 2) as avg_delivery_days
from olist.orders
where order_delivered_customer_date is not NULL;
```

## 4. Revenue by State

Which Brazilian states generate the most revenue?

```sql
select c.customer_state, ROUND(sum(oi.price)::numeric, 2) as total_revenue
from olist.order_items oi
join olist.orders o on oi.order_id = o.order_id
join olist.customers c ON o.customer_id = c.customer_id
group by c.customer_state
order by total_revenue DESC;
```

## 5. Orders by Month

How many orders were placed each month over the dataset's time range?

```sql
select
   TO_CHAR(order_purchase_timestamp, 'YYYY-MM') as month,
   COUNT(*) as order_count
from olist.orders
group by TO_CHAR(order_purchase_timestamp, 'YYYY-MM')
order by month;
```

## 6. One-Star Review Rate by Category

Which product categories have the highest rate of 1-star reviews?

```sql
select
   v.product_category_name_english,
   ROUND(100.0 * SUM(case when r.review_score = 1 then 1 else 0 end) / COUNT(*), 2) as one_star_rate
from olist.vw_order_summary v
join olist.order_reviews r on v.order_id = r.order_id
group by v.product_category_name_english
having COUNT(*) >= 50
order by one_star_rate DESC
limit 10;
```

## 7. Late Delivery Impact on Reviews

Do orders that arrive late receive lower review scores on average than orders that arrive on time?

```sql
select
   case
       when order_delivered_customer_date > order_estimated_delivery_date then 'Late'
       else 'On Time'
   end as delivery_status,
   ROUND(AVG(r.review_score), 2) as avg_review_score,
   COUNT(*) as order_count
from olist.vw_order_summary v
join olist.order_reviews r ON v.order_id = r.order_id
where v.order_delivered_customer_date is not NULL
group by delivery_status;
```

## 8. High Sales, Low Reviews Sellers

Which sellers have the highest total sales volume but below-average review scores?

```sql
select
   v.seller_id,
   ROUND(sum(v.price)::numeric, 2) as total_sales,
   ROUND(AVG(r.review_score), 2) as avg_review_score
from olist.vw_order_summary v
join olist.order_reviews r on v.order_id = r.order_id
group by v.seller_id
having AVG(r.review_score) < (
   select AVG(review_score) from olist.order_reviews
)
order by total_sales DESC
limit 20;
```

## 9. Average Order Value by Payment Type

What is the average order value broken down by payment type?

```sql
select
   payment_type,
   ROUND(AVG(payment_value)::numeric, 2) as avg_order_value,
   COUNT(*) as total_payments
from olist.order_payments
group by payment_type
order by avg_order_value DESC;
```

## 10. Top Customers and Their Categories

Which customers have placed the most orders, and what categories do they tend to buy from?

```sql
select
   v.customer_unique_id,
   v.product_category_name_english,
   COUNT(distinct v.order_id) as order_count
from olist.vw_order_summary v
where v.customer_unique_id in (
   select customer_unique_id
   from olist.vw_order_summary
   group by customer_unique_id
   order by COUNT(distinct order_id) DESC
   limit 10
)
group by v.customer_unique_id, v.product_category_name_english
order by v.customer_unique_id, order_count DESC;
```

## 11. Early Delivery Percentage

What percentage of orders are delivered before the estimated delivery date?

```sql
select
   ROUND(100.0 * SUM(case when order_delivered_customer_date < order_estimated_delivery_date then 1 else 0 end) / COUNT(*), 2) as pct_early
from olist.orders
where order_delivered_customer_date is not NULL;
```

## 12. Freight Cost Ratio by Category

Which product categories have the highest average freight cost relative to the product price?

```sql
select
   product_category_name_english,
   ROUND(AVG(freight_value / nullif(price, 0))::numeric, 4) as avg_freight_ratio
from olist.vw_order_summary
where price > 0
group by product_category_name_english
order by avg_freight_ratio DESC
limit 10;
```

## 13. Fast Sellers

Are there sellers who consistently deliver faster than average?

```sql
select
   seller_id,
   ROUND(AVG(extract(epoch from (order_delivered_customer_date - order_purchase_timestamp)) / 86400), 2) as avg_delivery_days
from olist.vw_order_summary
where order_delivered_customer_date is not NULL
group by seller_id
having ROUND(AVG(extract(epoch from (order_delivered_customer_date - order_purchase_timestamp)) / 86400), 2) < (
   select ROUND(AVG(extract(epoch from (order_delivered_customer_date - order_purchase_timestamp)) / 86400), 2)
   from olist.orders
   where order_delivered_customer_date is not NULL
)
order by avg_delivery_days ASC
limit 20;
```

## 14. Payment Installment Distribution

What is the distribution of orders by payment installment count?

```sql
select
   payment_installments,
   COUNT(*) as order_count
from olist.order_payments
group by payment_installments
order by payment_installments;
```

## 15. Delivery Time by State

Which states have the longest average delivery times?

```sql
select
   customer_state,
   ROUND(AVG(extract(epoch from (order_delivered_customer_date - order_purchase_timestamp)) / 86400), 2) as avg_delivery_days
from olist.vw_order_summary
where order_delivered_customer_date is not NULL
group by customer_state
order by avg_delivery_days DESC;
```

## 16. Top Sellers by Category

What are the top 5 sellers by revenue in each product category?

```sql
select product_category_name_english, seller_id, total_revenue
from (
   select
       product_category_name_english,
       seller_id,
       ROUND(SUM(price)::numeric, 2) as total_revenue,
       rank() over (partition by product_category_name_english order by SUM(price) DESC) as rnk
   from olist.vw_order_summary
   group by product_category_name_english, seller_id
) ranked
where rnk <= 5
order by product_category_name_english, total_revenue DESC;
```

## 17. Review Score Over Time

How does the average review score change over time?

```sql
select
   TO_CHAR(o.order_purchase_timestamp, 'YYYY-MM') as month,
   ROUND(AVG(r.review_score), 2) as avg_review_score
from olist.orders o
join olist.order_reviews r on o.order_id = r.order_id
group by TO_CHAR(o.order_purchase_timestamp, 'YYYY-MM')
order by month;
```

## 18. Repeat Customer Analysis

What share of customers made more than one purchase, and how long on average between their first and second order?

```sql
with customer_orders as (
   select
       c.customer_unique_id,
       o.order_purchase_timestamp,
       ROW_NUMBER() over (partition by c.customer_unique_id order by o.order_purchase_timestamp) as order_num
   from olist.orders o
   join olist.customers c on o.customer_id = c.customer_id
),
repeat_customers as (
   select customer_unique_id,
       MIN(case when order_num = 1 then order_purchase_timestamp end) as first_order,
       MIN(case when order_num = 2 then order_purchase_timestamp end) as second_order
   from customer_orders
   group by customer_unique_id
   having COUNT(*) > 1
)
select
   ROUND(100.0 * COUNT(*) / (select COUNT(distinct customer_unique_id) from olist.customers), 2) as pct_repeat_customers,
   ROUND(AVG(extract(epoch from (second_order - first_order)) / 86400), 2) as avg_days_between_orders
from repeat_customers;
```

## 19. Products Bought Together

Which product categories are most frequently bought together in the same order?

```sql
select
   t1.product_category_name_english as category_1,
   t2.product_category_name_english as category_2,
   COUNT(*) as times_bought_together
from olist.order_items oi1
join olist.order_items oi2 on oi1.order_id = oi2.order_id and oi1.product_id < oi2.product_id
join olist.products p1 on oi1.product_id = p1.product_id
join olist.products p2 on oi2.product_id = p2.product_id
join olist.product_category_name_translation t1 on p1.product_category_name = t1.product_category_name
join olist.product_category_name_translation t2 on p2.product_category_name = t2.product_category_name
group by t1.product_category_name_english, t2.product_category_name_english
order by times_bought_together DESC
limit 20;
```

## 20. Slow High-Volume Sellers

Which sellers have fulfilled more than 100 orders but have an average delivery time longer than the overall platform average?

```sql
select
   seller_id,
   COUNT(distinct order_id) as total_orders,
   ROUND(AVG(extract(epoch from (order_delivered_customer_date - order_purchase_timestamp)) / 86400), 2) as avg_delivery_days
from olist.vw_order_summary
where order_delivered_customer_date is not NULL
group by seller_id
having COUNT(distinct order_id) > 100
and AVG(extract(epoch from (order_delivered_customer_date - order_purchase_timestamp)) / 86400) >
   (select AVG(extract(epoch from (order_delivered_customer_date - order_purchase_timestamp)) / 86400)
    from olist.orders
    where order_delivered_customer_date is not NULL)
order by avg_delivery_days DESC;
```