#!/usr/bin/env python
# coding: utf-8

# ## Curated_Full_Incremental
# 
# New notebook

# In[2]:


from pyspark.sql.functions import *
from delta.tables import DeltaTable

#Creating Parameter
try:
    is_full_load = dbutils.widgets.get("is_full_load")
except:
    is_full_load = "True"  # default for manual runs

is_full_load = is_full_load.lower() == "true"
print("Full load?" , is_full_load)

# Reading staging table

df_staging = spark.table("dbo.superstoresales_staging")

# Filtering rows (full vs incremental)

if is_full_load:
    print("Running FULL load")
    df_new = df_staging
else:
    print("Running INCREMENTAL load")
    last_watermark = spark.sql("SELECT MAX(order_date) as wm FROM curated.sales_fact").first()["wm"]
    df_new = df_staging.filter(col("order_date") > last_watermark)

print("Rows to process:", df_new.count())

# Creating Dimensions

# Dim Date
df_dim_date = df_new.select("order_date").distinct() \
    .withColumn("date_id", date_format(col("order_date"), "yyyyMMdd").cast("int")) \
    .withColumn("year", year(col("order_date"))) \
    .withColumn("month", month(col("order_date"))) \
    .withColumn("day", dayofmonth(col("order_date")))

df_dim_date.write.format("delta") \
    .mode("overwrite" if is_full_load else "append") \
    .option("mergeSchema", "true") \
    .saveAsTable("curated.dim_date")

# Dim Customer
df_dim_customer = df_new.select("customer_id", "customer_name", "region").distinct()\
    .withColumn("valid_from", current_date()) \
    .withColumn("valid_to", lit(None).cast("date")) \
    .withColumn("is_current", lit(True))
df_dim_customer.write.format("delta") \
    .mode("overwrite" if is_full_load else "append") \
    .option("mergeSchema", "true") \
    .saveAsTable("curated.dim_customer")

# Dim Product
df_dim_product = df_new.select("product_id", "category", "sub_category").distinct()
df_dim_product.write.format("delta") \
    .mode("overwrite" if is_full_load else "append") \
    .option("mergeSchema", "true") \
    .saveAsTable("curated.dim_product")

# Creating Fact Table
df_fact = df_new.select(
    "order_id",
    "product_id",
    "customer_id",
    "sales",
    col("order_date").cast("date").alias("order_date")
)

df_fact.write.format("delta") \
    .mode("overwrite" if is_full_load else "append") \
    .option("mergeSchema", "true") \
    .saveAsTable("curated.sales_fact")

print("Load completed.")

