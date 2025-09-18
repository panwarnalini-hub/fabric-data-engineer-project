#!/usr/bin/env python
# coding: utf-8

# ## Curated
# 
# New notebook

# In[4]:


df = spark.sql("SELECT * FROM dbo.superstoresales_staging") #I kept staging and curated tables in different schemas dbo and curated

from pyspark.sql.functions import *

# Handle order_date
df = df.withColumn(
    "order_date",
    to_date(
        concat_ws("/",
            lpad(split(col("order_date"), "/")[0], 2, "0"),  # day
            lpad(split(col("order_date"), "/")[1], 2, "0"),  # month
            split(col("order_date"), "/")[2]                 # year
        ),
        "dd/MM/yyyy"
    )
)

# Handle ship_date
df = df.withColumn(
    "ship_date",
    to_date(
        concat_ws("/",
            lpad(split(col("ship_date"), "/")[0], 2, "0"),  # day
            lpad(split(col("ship_date"), "/")[1], 2, "0"),  # month
            split(col("ship_date"), "/")[2]                 # year
        ),
        "dd/MM/yyyy"
    )
)

# Check invalid date rows
print("Invalid order_date rows:", df.filter(col("order_date").isNull()).count())
print("Invalid ship_date rows:", df.filter(col("ship_date").isNull()).count())


# In[5]:


sales_fact = df.select(
    "order_id",
    "product_id",
    "customer_id",
    "sales",
    "order_date") #order_date has been added to create the key order_id to link the tablke to dim_date


# In[6]:


from pyspark.sql.functions import year, month, dayofmonth

dim_date = df.select(
    col("order_date").alias("date"),
    year("order_date").alias("year"),
    month("order_date").alias("month"),
    dayofmonth("order_date").alias("day")
).distinct()


# In[7]:


dim_product = df.select(
    "product_id",
    "category",
    "sub_category",
    "product_name"
).distinct()


# In[8]:


dim_customer = df.select(
    "customer_id",
    "customer_name",
    "segment",
    "region"
).distinct()


# In[9]:


from pyspark.sql import SparkSession

data = [
    ("panwarnalini@gmail.com", "East"),
    ("nalinipanwar@gmail.com", "West"),
    ("nalini@gmail.com", "North"),
    ("panwar@gmail.com", "South"),
]

dim_map = spark.createDataFrame(data, ["user_principal_name", "region"])  #diving by region as this is sales data


# In[10]:


spark.sql("CREATE SCHEMA IF NOT EXISTS curated") #created curated schema

sales_fact.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("curated.sales_fact")
dim_date.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("curated.dim_date")
dim_product.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("curated.dim_product")
dim_customer.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("curated.dim_customer")
dim_map.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("curated.user_region_map")


# In[11]:


from pyspark.sql.functions import year, month, dayofmonth, date_format, col

# Read your current dim_date
df_dim_date = spark.table("curated.dim_date")

# Add surrogate key: YYYYMMDD format
df_dim_date = df_dim_date.withColumn(
    "date_id", date_format(col("date"), "yyyyMMdd").cast("int")
)

# Save back with overwrite
df_dim_date.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \ #if the column numbers have increased, make sure to use this
    .saveAsTable("curated.dim_date")


# In[12]:


from pyspark.sql.functions import date_format
# Read the current sales_fact
df_sales_fact = spark.table("curated.sales_fact")

df_sales_fact = df_sales_fact.withColumn("date_id", date_format(col("order_date"), "yyyyMMdd").cast("int")) #created surrogate key date_id

# Save updated fact table
df_sales_fact.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true")\
    .saveAsTable("curated.sales_fact")


# In[20]:


spark.table("curated.sales_fact").printSchema()

