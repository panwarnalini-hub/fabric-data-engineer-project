# Technical Transformation Summary

The following transformations were applied to the raw data to ensure consistency and quality:

### 🔹 Column Naming
- Converted all column names to **lowercase**.  
- Replaced spaces and brackets with **underscores**.  
- Example: `"Order Date"` → `order_date`.  

### 🔹 String Columns
- Trimmed leading/trailing whitespace.  
- Replaced `NULL` values with `"Unknown"`.  

### 🔹 Numeric Columns
- Replaced `NULL` values with `0`.  

### 🔹 Date Columns
- Converted `order_date` and `ship_date` from **string** (`MM/dd/yyyy`) to proper **date type**.  
- Fixed single-digit months/days (`8/1/2017 → 08/01/2017`).  

### 🔹 Sales Column
- Cast `sales` from **string** to **double** for numeric calculations.  
