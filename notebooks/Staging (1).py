#!/usr/bin/env python
# coding: utf-8

# ## Staging
# 
# New notebook

# In[1]:


df = spark.read.csv("Files/Superstore.csv",header=True,inferSchema=True)
df.printSchema()


# In[2]:


from pyspark.sql.functions import *

df = spark.sql("SELECT * FROM dbo.superstoresales_staging_raw")

# Clean column names
df = df.toDF(*[
    col_name.strip().lower().replace(" ", "_").replace("(", "_").replace(")", "_").replace("-", "_")
    for col_name in df.columns
])

# Clean values by type
numeric_types = {"int", "double", "float", "bigint", "decimal", "long", "short"}
date_cols = {"order_date", "ship_date"}

for c, t in df.dtypes:
    if c in date_cols:
        continue  # skip dates
    elif t == "string":
        df = df.withColumn(c, when(col(c).isNull(), lit("Unknown")).otherwise(trim(col(c))))
    elif t in numeric_types:
        df = df.withColumn(c, when(col(c).isNull(), lit(0)).otherwise(col(c)))

# Cast sales to double
df = df.withColumn("sales", col("sales").cast("double"))

# Check schema
df.printSchema()


# In[5]:


df.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("superstoresales_staging")


# 
# 
