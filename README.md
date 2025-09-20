# Superstore Data Engineering Project – Microsoft Fabric  

## Overview  
This project is my end-to-end **data engineering workflow** built in **Microsoft Fabric** using the well-known *Superstore Sales* dataset.  

I started with a simple CSV file and turned it into a fully governed analytics solution. Along the way, I set up **data pipelines**, created a **star schema**, implemented **row-level security (RLS)**, added **incremental loading (watermarking)**, and practiced **Slowly Changing Dimensions (SCD Type 2)**. The goal was to practice how real data engineering solutions are designed and operated in Fabric.  

---

## Architecture  
The solution follows a layered approach:  

- **Raw Zone** → original CSV loaded into Lakehouse.  
- **Staging Zone** → cleaned column names, fixed data types, cast `sales` into numeric, standardized dates.  
- **Curated Zone** → built a star schema with:  
  - `sales_fact` (fact table)  
  - `dim_customer` (with `region`, SCD Type 2 applied)  
  - `dim_product`  
  - `dim_date` (with surrogate `date_id`, partitioned by year)  

A Fabric **Data Pipeline** orchestrates the flow:  
- Copies raw CSV into Lakehouse  
- Runs PySpark notebooks for staging and curated transformations  
- Implements **incremental loading** with watermarking (only new rows processed)  
- Maintains historical changes in customer dimension using **SCD Type 2**  
- Refreshes **daily** and also on **file arrival events** in OneLake  

---

## Data Modeling  
Designed a **star schema** to support flexible analytics:  

- `sales_fact` → transaction data  
- `dim_customer` → customer details and regions (SCD Type 2 for history)  
- `dim_product` → product category & sub-category  
- `dim_date` → calendar with surrogate `date_id`  

This allows analysis by **region, product, customer, and time**.  

---

## Security (RLS)  
Implemented **Row-Level Security** in the Lakehouse SQL endpoint so users only see data for their region.  

- Created `user_region_map` table (user → region)  
- Wrote a T-SQL function to filter rows using `USER_NAME()`  
- Built a secure view `v_sales_secure` (fact + dims + region)  
- Added a security policy `SalesRLS` on that view  

Result: Analysts query the same view but only see their own region’s data.  

---

## Incremental Loading (Watermarking)  
- Used `MAX(order_date)` from curated fact to detect last load.  
- New rows (`order_date` > watermark) are appended.  
- Ensures efficiency by avoiding reloading the full dataset.  

---

## Slowly Changing Dimensions (SCD Type 2)  
- Implemented on **dim_customer**.  
- Tracks history when customer attributes (e.g., region, segment) change.  
- Columns used: `valid_from`, `valid_to`, `is_current`.  
- Enables point-in-time analysis with historical context.  

---

## Monitoring & Automation  
- Pipelines scheduled **daily**.  
- Event triggers run automatically when new data lands in OneLake.  
- Run logs tracked in Fabric pipeline monitoring.  
- Can be extended to **Azure Monitor / Teams / Email alerts**.  

---

## Tech Stack  
- **Microsoft Fabric** → Lakehouse, Pipelines, SQL Endpoint  
- **PySpark** → data transformations, SCD, watermarking  
- **Delta Lake** → storage format  
- **T-SQL** → secure views, functions, RLS  
- **Power BI** → reporting (future step)  

---

## How to Run  
1. Upload raw Superstore CSV into the **Raw zone**.  
2. Run the pipeline (full load or incremental via parameter).  
3. Curated tables (`sales_fact`, `dim_*`) get refreshed.  
4. Query `curated.v_sales_secure` in the SQL endpoint → regionally filtered data.  

---

## What I Learned  
- How to design **zones** in Fabric (raw → staging → curated).  
- Building a **star schema** with surrogate keys.  
- Implementing **incremental loads with watermarking**.  
- Handling **SCD Type 2** for historical tracking.  
- Applying **RLS** for governance/security.  
- Automating pipelines with **schedules & event triggers**.  

---

## Project Documentation

- [Raw Schema Documentation](docs/schema_raw.md)  
- [Curated Schema Documentation](docs/schema_curated.md)
- [Transformation Summary](docs/transformations.md)  
- [Pipeline & Orchestration](docs/pipeline.md)  

## Code Repository

- PySpark Notebooks  
  - [Staging Notebook](notebooks/staging_notebook.py)  
  - [Curated Notebook](notebooks/curated_notebook.py)  
  - [Incremental Load (Watermark)](notebooks/incremental_notebook.py)  
  - [SCD Type 2](notebooks/scd2_notebook.py)  

- SQL Scripts  
  - [Create Secure View](sql/create_view.sql)  
  - [Row-Level Security Policy](sql/rls_policy.sql)  

---

**Author:** Nalini Panwar  
**Status:** Completed (Portfolio Project)

