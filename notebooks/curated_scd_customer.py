#!/usr/bin/env python
# coding: utf-8

# ## curated_scd_customer
# 
# New notebook

# In[ ]:


from pyspark.sql.functions import current_date, lit
from delta.tables import DeltaTable

# Loading dim_customer table
dim_customer = DeltaTable.forName(spark, "curated.dim_customer")

# Distinct customers from staging
df_staging_cust = spark.table("dbo.superstoresales_staging") \
    .select("customer_id", "customer_name", "region", "segment") \
    .dropDuplicates(["customer_id"])

# Step 1: Expire old rows where data changed
(
    dim_customer.alias("t")
    .merge(
        df_staging_cust.alias("s"),
        "t.customer_id = s.customer_id AND t.is_current = true"
    )
    .whenMatchedUpdate(
        condition="""
            t.customer_name <> s.customer_name OR 
            t.region <> s.region OR 
            t.segment <> s.segment
        """,
        set={
            "valid_to": "current_date()",
            "is_current": "false"
        }
    )
    .execute()
)

# Step 2: Insert new versions
df_new_versions = df_staging_cust.withColumn("valid_from", current_date()) \
                                .withColumn("valid_to", lit(None).cast("date")) \
                                .withColumn("is_current", lit(True))

df_new_versions.write.format("delta").mode("append").saveAsTable("curated.dim_customer")

print("SCD2 applied to dim_customer")

