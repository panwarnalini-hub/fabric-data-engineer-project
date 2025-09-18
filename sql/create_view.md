```sql
CREATE VIEW curated.v_sales_secure
WITH SCHEMABINDING  --make sure to use SCHEMABINDING so that columns cannot be altered in the OG table
AS
SELECT
    f.order_id,
    f.sales,
    f.customer_id,
    f.product_id,
    f.date_id,
    c.region,              -- region from dim_customer (used in RLS)
    c.customer_name,
    d.date,                -- dim_date has "date", not "order_date", as the fact table was created
    d.year,
    d.month,
    p.category,
    p.sub_category
FROM curated.sales_fact f
JOIN curated.dim_customer c ON f.customer_id = c.customer_id
JOIN curated.dim_date d     ON f.date_id = d.date_id
JOIN curated.dim_product p  ON f.product_id = p.product_id;
```
