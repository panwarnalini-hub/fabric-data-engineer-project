# Schema Documentation (Curated Zone)

## dim_customer
| Column Name  | Data Type | Nullable | Description |
|--------------|-----------|----------|-------------|
| customer_id  | String    | No       | Unique identifier for the customer (business key). |
| customer_name| String    | Yes      | Full name of the customer. |
| segment      | String    | Yes      | Market segment (Consumer, Corporate, Home Office). |
| region       | String    | Yes      | Customer’s assigned geographic region. |
| valid_from   | Date      | No       | Start date when this record version became active. |
| valid_to     | Date      | Yes      | End date when this record version was replaced (null = current). |
| is_current   | Boolean   | No       | Flag indicating the active record (1 = current, 0 = historical). |

---

## dim_date
| Column Name | Data Type | Nullable | Description |
|-------------|-----------|----------|-------------|
| date        | Date      | No       | Calendar date. |
| year        | Integer   | No       | Year extracted from date. |
| month       | Integer   | No       | Month extracted from date. |
| day         | Integer   | No       | Day extracted from date. |
| date_id     | Integer   | No       | Surrogate key in `YYYYMMDD` format. |

---

## dim_product
| Column Name   | Data Type | Nullable | Description |
|---------------|-----------|----------|-------------|
| product_id    | String    | No       | Unique identifier for the product. |
| category      | String    | Yes      | High-level product category. |
| sub_category  | String    | Yes      | Product sub-category. |
| product_name  | String    | Yes      | Full product description/name. |

---

## sales_fact
| Column Name  | Data Type | Nullable | Description |
|--------------|-----------|----------|-------------|
| order_id     | String    | No       | Unique identifier for the order. |
| product_id   | String    | No       | Foreign key - `dim_product`. |
| customer_id  | String    | No       | Foreign key - `dim_customer`. |
| date_id      | Integer   | No       | Foreign key - `dim_date`. |
| sales        | Double    | Yes      | Sales amount. |
| order_date   | Date      | Yes      | Date when the order was placed. |
