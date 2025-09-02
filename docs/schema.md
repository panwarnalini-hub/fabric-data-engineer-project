# 📑 Schema Documentation – Superstore Dataset

This document describes the schema of the **Superstore.csv** dataset after ingestion and cleaning.

---

## 🗂️ Columns & Data Types

| Column Name   | Inferred Data Type | Final Data Type | Nullable | Notes / Fixes |
|---------------|--------------------|-----------------|----------|----------------|
| Row ID        | integer            | integer         | Yes      | Correctly inferred |
| Order ID      | string             | string          | Yes      | Kept as string (unique identifier) |
| Order Date    | string             | date            | Yes      | Converted from string → date using `to_date` |
| Ship Date     | string             | date            | Yes      | Converted from string → date using `to_date` |
| Ship Mode     | string             | string          | Yes      | No change |
| Customer ID   | string             | string          | Yes      | Identifier |
| Customer Name | string             | string          | Yes      | Kept as string |
| Segment       | string             | string          | Yes      | No change |
| Country       | string             | string          | Yes      | No change |
| City          | string             | string          | Yes      | No change |
| State         | string             | string          | Yes      | No change |
| Postal Code   | integer            | integer         | Yes      | Correctly inferred |
| Region        | string             | string          | Yes      | No change |
| Product ID    | string             | string          | Yes      | Identifier |
| Category      | string             | string          | Yes      | No change |
| Sub-Category  | string             | string          | Yes      | No change |
| Product Name  | string             | string          | Yes      | No change |
| Sales         | string             | double          | Yes      | Converted from string → double for aggregation |

---

## 📝 Notes
- Dates were standardized using `to_date` in Spark.  
- Sales column converted to **double** to enable numeric aggregations.  
- Unique identifiers (`Order ID`, `Customer ID`, `Product ID`) kept as **string**.  
- No missing column names found in dataset.  

---

👩‍💻 **Author**: Nalini Panwar  
📅 **Last Updated**: September 2025
