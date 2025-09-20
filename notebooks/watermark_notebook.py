#!/usr/bin/env python
# coding: utf-8

# ## watermark_notebook
# 
# New notebook

# In[ ]:


from pyspark.sql.functions import col

# 1. Load staging data
df_staging = spark.table("dbo.superstoresales_staging")

# 2. Get watermark (last order_date in fact table)
last_watermark = spark.sql("""
    SELECT MAX(order_date) as wm
    FROM curated.sales_fact
""").first()["wm"]

print("Last watermark (max order_date in fact):", last_watermark)

# 3. Filter only new rows
df_new = df_staging.filter(col("order_date") > last_watermark)

print("New rows detected:", df_new.count())

# 4. Align schema with curated fact table
df_new = df_new.select(
    "order_id",
    "product_id",
    "customer_id",
    "sales",
    col("order_date").cast("date")
)

# 5. Append new rows into fact table
df_new.write.format("delta") \
    .mode("append") \
    .saveAsTable("curated.sales_fact")

print("Incremental load completed. Rows appended:", df_new.count())

