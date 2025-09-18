# 📊 Superstore Data Engineering Project – Microsoft Fabric  

## Overview  
This project is my end-to-end **data engineering workflow** built in **Microsoft Fabric** using the well-known *Superstore Sales* dataset.  

I started with a simple CSV file and turned it into a fully governed analytics solution. Along the way, I set up data pipelines, created a star schema, added row-level security, and automated refreshes. The goal was to practice how real data engineering solutions are designed and operated in Fabric.  

---

## Architecture  
The solution follows a layered approach:  

- **Raw Zone** → original CSV loaded into Lakehouse.  
- **Staging Zone** → cleaned column names, fixed data types, cast `sales` into numeric.  
- **Curated Zone** → built a star schema with:  
  - `sales_fact`  
  - `dim_customer` (with `region`)  
  - `dim_product`  
  - `dim_date` (with surrogate `date_id`, partitioned by year)  

A Fabric **Data Pipeline** orchestrates the flow:  
- Copies raw CSV into Lakehouse  
- Runs PySpark notebook for cleaning + transformations  
- Writes fact and dimension tables into the curated zone  
- Refreshes **daily** and also on **file arrival events** in OneLake  

---

## Data Modeling  
I designed a **star schema** to support flexible analysis:  

- `sales_fact` → transaction data  
- `dim_customer` → customer details and regions  
- `dim_product` → product category & sub-category  
- `dim_date` → calendar with surrogate `date_id`  

This allows analysis by region, product, and time.  

---

## Security (RLS)  
I implemented **Row-Level Security** in the Lakehouse SQL endpoint so users only see data for their region.  

- Created `user_region_map` table (user → region)  
- Wrote a T-SQL function to filter rows using `USER_NAME()`  
- Built a secure view `v_sales_secure` (fact + dims + region)  
- Added a security policy `SalesRLS` on that view  

Result: Nalini only sees East region, Priya only sees West, etc.  

---

## Monitoring & Automation  
- Pipelines are scheduled **daily**  
- Event triggers run automatically when new data lands in OneLake  
- Pipeline run history gives visibility into success/failure  
- Can integrate with Azure Monitor / Log Analytics for proactive alerts  

---

## Tech Stack  
- **Microsoft Fabric** → Lakehouse, SQL Endpoint, Pipelines  
- **PySpark** → data transformations  
- **Delta Lake** → storage format  
- **T-SQL** → secure views, functions, RLS  
- **Power BI** → for reporting (optional)  

---

## How to Run  
1. Upload raw Superstore CSV into the **Raw zone**.  
2. Run the pipeline using trigger/schedule. 
3. Query `curated.v_sales_secure` in the SQL endpoint.  
4. Data is automatically filtered by region using RLS.  

---

## What I Learned  
- How to design **zones** in Fabric (raw → staging → curated).  
- How to build a **star schema** with fact/dim tables.  
- Implementing **RLS** in the SQL endpoint.  
- Automating pipelines with **schedules and event triggers**.  
- The difference between **Lakehouse SQL endpoint vs Warehouse** governance.  

---

## Project Documentation

- [Schema Documentation](docs/schema.md)  
- [Transformation Summary](docs/transformations.md)  
- [Pipeline & Orchestration](docs/pipeline.md)  

## Code Repository

- PySpark Notebooks  
  - [Staging Notebook](notebooks/staging_notebook.py)  
  - [Curated Notebook](notebooks/curated_notebook.py)  

- SQL Scripts  
  - [Create Secure View](sql/create_view.sql)  
  - [Row-Level Security Policy](sql/rls_policy.sql)  


**Author:** Nalini Panwar  
**Status:** Completed (Portfolio Project)

