# Schema Documentation (Data Dictionary)

| Column Name     | Data Type | Nullable | Description |
|-----------------|-----------|----------|-------------|
| row_id          | Integer   | Yes      | Unique numeric identifier for each row. |
| order_id        | String    | Yes      | Unique identifier for each order. |
| order_date      | Date      | Yes      | Date when the order was placed (`MM/dd/yyyy`). |
| ship_date       | Date      | Yes      | Date when the order was shipped (`MM/dd/yyyy`). |
| ship_mode       | String    | Yes      | Mode of shipment (Standard Class, Second Class, etc.). |
| customer_id     | String    | Yes      | Unique identifier for the customer. |
| customer_name   | String    | Yes      | Full name of the customer. |
| segment         | String    | Yes      | Market segment (Consumer, Corporate, Home Office). |
| country         | String    | Yes      | Country of the order. |
| city            | String    | Yes      | City of the order. |
| state           | String    | Yes      | State/Province of the order. |
| postal_code     | Integer   | Yes      | Postal code of the shipping address. |
| region          | String    | Yes      | Geographic region (East, West, Central, South). |
| product_id      | String    | Yes      | Unique identifier for the product. |
| category        | String    | Yes      | High-level product category. |
| sub_category    | String    | Yes      | Product sub-category. |
| product_name    | String    | Yes      | Full product description/name. |
| sales           | Double    | Yes      | Sales amount for the line item. |
