# Fabric Data Engineer Project

A hands-on project to demonstrate skills aligned with the **Microsoft DP-700: Fabric Data Engineer Associate** certification.  
This repository showcases data ingestion, transformation, documentation, and reporting using Microsoft Fabric and related tools.

---

## 📂 Project Structure

fabric-data-engineer-project/
│
├── data/ # Sample datasets (e.g., Superstore.csv)
├── notebooks/ # Synapse/Databricks notebooks
├── scripts/ # Pyspark scripts for transformations
├── docs/ # Documentation (schema, architecture, etc.)
│ └── schema.md # Data schema details
└── README.md # Project overview


---

## 🚀 Project Workflow

1. **Data Ingestion**
   - Load CSV/Excel datasets into Fabric Lakehouse.
   - Document schema (columns, datatypes, nullable).

2. **Data Transformation**
   - Clean and standardize data using PySpark/Pandas.
   - Handle nulls, enforce datatypes, and create curated tables.

3. **Data Modeling**
   - Create star schema with Fact and Dimension tables.
   - Document lineage and relationships.

4. **Data Analysis**
   - Run SQL queries to validate transformations.
   - Perform aggregations and KPIs for reporting.

5. **Visualization**
   - Connect Fabric dataset to Power BI.
   - Build dashboards to showcase insights.

---

# 📑 Schema Documentation Example

```text
root
|-- Row ID: integer (nullable = true)
|-- Order ID: string (nullable = true)
|-- Order Date: string (nullable = true)
|-- Ship Date: string (nullable = true)
|-- Ship Mode: string (nullable = true)
|-- Customer ID: string (nullable = true)
|-- Customer Name: string (nullable = true)
|-- Segment: string (nullable = true)
|-- Country: string (nullable = true)
|-- City: string (nullable = true)
|-- State: string (nullable = true)
|-- Postal Code: integer (nullable = true)
|-- Region: string (nullable = true)
|-- Product ID: string (nullable = true)
|-- Category: string (nullable = true)
|-- Sub-Category: string (nullable = true)
|-- Product Name: string (nullable = true)
|-- Sales: double (nullable = true)
```

---
🛠️ Tools & Technologies

Microsoft Fabric (Lakehouse, Dataflows, Pipelines, Notebooks)

Azure Synapse Analytics

Apache Spark (PySpark)

Power BI

GitHub (Version control & project portfolio)

🎯 Learning Goals

Demonstrate end-to-end data engineering workflow in Fabric.

Practice schema documentation, transformations, and reporting.

Build a project portfolio for job applications and interviews.

📌 Next Steps

 Add data cleaning notebooks

 Create curated dimension & fact tables

 Publish Power BI dashboard screenshots

 Write architecture diagram in docs/

👩‍💻 Author: Nalini Panwar

📅 Started: September 2025
---
