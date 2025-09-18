# Pipeline & Orchestration

This document explains how the Microsoft Fabric pipeline was designed to orchestrate the data flow from **Raw → Staging → Curated**, and how monitoring and automation were implemented.

---

## 1. Pipeline Activities

### Activity 1: Ingest Raw Data
- **Tool**: Copy Data activity  
- **Source**: CSV file stored in OneLake  
- **Destination**: Lakehouse `raw` zone  
- **Format**: CSV → Delta

### Activity 2: Transform in Staging
- **Tool**: PySpark notebook  
- **Operations**:
  - Standardized column names (lowercase, underscores)  
  - Trimmed string fields, replaced nulls  
  - Converted dates (`order_date`, `ship_date`) into proper `Date` type  
  - Cast `sales` to double  
- **Output**: Lakehouse `staging` zone tables

### Activity 3: Curated Zone (Star Schema)
- **Tool**: PySpark notebook  
- **Transformations**:
  - Built **dimension tables** (`dim_customer`, `dim_date`, `dim_product`)  
  - Built **fact table** (`sales_fact`)  
  - Added surrogate keys (`date_id`) for joins  
- **Output**: `curated` zone, partitioned & ready for analytics

---

## 2. Scheduling & Automation
- Added a **daily trigger** to refresh the pipeline automatically.  
- Configured **OneLake events** to trigger refresh when new files are added.  

---

## 3. Monitoring
- Pipeline run logs are tracked in Fabric (success/failure for each activity).  
- Real-time monitoring via Fabric’s **Eventstream** → can be extended to alerting systems (e.g., Teams/Email).  

---

## 4. Governance & Security
- Row-Level Security (RLS) applied in **SQL endpoint** using secure views.  
- Only authorized users can query curated views (e.g., `v_sales_secure`).  
- Data engineers (pipeline) have full access; analysts see filtered data.

---

This pipeline ensures **repeatable, automated, and secure data flow** — from ingestion to analytics-ready tables.
