# Pipeline & Orchestration

This document explains how the Microsoft Fabric pipeline was designed to orchestrate the data flow from **Raw → Staging → Curated**, and how monitoring, incremental loading, and SCD2 were implemented.

---

## 1. Pipeline Activities

**Activity 1: Ingest Raw Data**

* **Tool:** Copy Data activity
* **Source:** CSV file stored in OneLake
* **Destination:** Lakehouse raw zone
* **Format:** CSV → Delta

**Activity 2: Transform in Staging**

* **Tool:** PySpark notebook
* **Operations:**

  * Standardized column names (lowercase, underscores)
  * Trimmed string fields, replaced nulls
  * Converted dates (`order_date`, `ship_date`) into proper `Date` type
  * Cast `sales` to `double`
* **Output:** Lakehouse staging zone tables

**Activity 3: Curated Zone (Star Schema)**

* **Tool:** PySpark notebook
* **Transformations:**

  * Built dimension tables (`dim_customer`, `dim_date`, `dim_product`)
  * Built fact table (`sales_fact`)
  * Added surrogate keys (`date_id`) for joins
* **Output:** Curated zone, partitioned & ready for analytics

---

## 2. Incremental Load (Watermarking)

* Implemented via **parameterized curated notebook**.
* Logic: pipeline checks **last processed order\_date** from `curated.sales_fact`.
* Only new rows greater than watermark are processed and appended.
* Ensures efficient daily refresh without full reloads.

---

## 3. Slowly Changing Dimension (SCD2)

* Implemented in `dim_customer` to preserve history of customer changes.
* Added tracking columns: `valid_from`, `valid_to`, `is_current`.
* **Process:**

  * If customer attributes change (region, segment, name), old record is expired (`valid_to` updated, `is_current=false`).
  * New version is inserted (`valid_from=current_date`, `is_current=true`).
* Ensures facts always link to the correct customer version historically.

---

## 4. Scheduling & Automation

* Added a **daily trigger** to refresh the pipeline automatically.
* Configured **OneLake events** to trigger refresh when new files are added.

---

## 5. Monitoring

* Pipeline run logs tracked in **Fabric** (success/failure for each activity).
* Real-time monitoring via **Fabric’s Eventstream** → extendable to alerting systems (e.g., Teams/Email).

---

## 6. Governance & Security

* **Row-Level Security (RLS):** applied in SQL endpoint using secure views.
* Only authorized users can query curated views (e.g., `v_sales_secure`).
* **Data engineers:** full access.
* **Analysts:** filtered access via RLS.

---

This pipeline ensures **repeatable, automated, incremental, and secure data flow** — from ingestion to analytics-ready tables with full history tracking.

<img width="940" height="344" alt="image" src="https://github.com/user-attachments/assets/88ac9a2a-321d-4f12-a186-aabc9706c06f" />

<img width="940" height="353" alt="image" src="https://github.com/user-attachments/assets/9a119938-93dc-4392-bae4-ab1eabe8e5ea" />


