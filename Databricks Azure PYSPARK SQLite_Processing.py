# Databricks notebook source
dbutils.fs.mount(
  source="wasbs://manufacturingdata@mdd0303.blob.core.windows.net/",
  mount_point="/mnt/manufacturingdata",
  extra_configs={"fs.azure.account.key.mdd0303.blob.core.windows.net": "pQBeyj+E+r633lfi1m957uXfP/9nZDdM/TL3MVKI7Nl5gP1RfYDK/YZCNAFPaRA/NiYwmd4dqgEC+AStOpIHzA=="}
)


# COMMAND ----------

display(dbutils.fs.ls("/mnt/manufacturingdata"))


# COMMAND ----------

# Copy database from DBFS to local driver storage
local_path = "/tmp/manufacturing_qc.db"
dbfs_path = "dbfs:/mnt/manufacturingdata/manufacturing_qc.db"

dbutils.fs.cp(dbfs_path, f"file:{local_path}", True)


# COMMAND ----------

from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.appName("AzureSQLiteProcessing").getOrCreate()

# Define the local path to SQLite database
sqlite_db_path = "/tmp/manufacturing_qc.db"

# Read SQLite database using JDBC
df = spark.read.format("jdbc").options(
    url=f"jdbc:sqlite:{sqlite_db_path}",
    dbtable="QualityControl"  # Change this to your actual table name
).load()

# Show first few records
df.show(5)


# COMMAND ----------

# Check schema (data types)
df.printSchema()

# Count null or missing values in each column
from pyspark.sql.functions import col, sum

df.select([sum(col(c).isNull().cast("int")).alias(c) for c in df.columns]).show()

# Check for duplicate Product_IDs
df.groupBy("Product_ID").count().filter("count > 1").show()


# COMMAND ----------

from pyspark.sql.functions import col, count, sum, when, isnan

def classify_columns(df):
    classification = {}

    for column in df.columns:
        # Count null values
        null_count = df.select(sum(col(column).isNull().cast("int"))).collect()[0][0] # counts how many values are missing, many nulls poor data
        
        # Count empty strings (for string columns)
        empty_count = df.filter(col(column) == "").count()

        # Count unique values
        unique_count = df.select(column).distinct().count() ## only a few unique values (like Factory_Location = ["NY", "LA", "SF"]), it’s Gold (aggregated category).
         ##If a column has many unique values (like Product_ID), it’s Silver (detailed, but not aggregated).

        # Check data type
        dtype = df.schema[column].dataType.simpleString()

        # Define classification rules
        if null_count > 0.3 * df.count():  # More than 30% null values
            category = "Bronze (Raw - High Nulls)"
        elif dtype in ["string"] and unique_count < 10:  # Low variation categorical data
            category = "Gold (Aggregated Metric)"
        elif dtype in ["int", "double"] and unique_count / df.count() < 0.1:  # Numeric, low uniqueness
            category = "Gold (KPI or Aggregation)"
        elif dtype in ["int", "double", "date"] and null_count == 0:  # Clean continuous data
            category = "Silver (Clean & Usable)"
        else:
            category = "Bronze (Needs Cleaning)"

        classification[column] = {
            "Null Count": null_count,
            "Empty Count": empty_count,
            "Unique Values": unique_count,
            "Data Type": dtype,
            "Category": category
        }

    return classification


# COMMAND ----------

classification_results = classify_columns(df)

# Display results nicely
import pandas as pd
pd.DataFrame.from_dict(classification_results, orient="index")


# COMMAND ----------

df.write.mode("overwrite").parquet("/mnt/manufacturingdata/bronze_data.parquet")


# COMMAND ----------

df.write.mode("overwrite").parquet("/mnt/manufacturingdata/silver_data.parquet")


# COMMAND ----------

df_gold = df.groupBy("Factory_Location").avg("Defect_Rate")
df_gold.write.mode("overwrite").parquet("/mnt/manufacturingdata/gold_avg_defect_rate.parquet")


# COMMAND ----------

df_gold_count = df.groupBy("Factory_Location").count()
df_gold_count.write.mode("overwrite").parquet("/mnt/manufacturingdata/gold_product_count.parquet")


# COMMAND ----------

df_gold_count.coalesce(1).write.mode("overwrite").parquet("/mnt/manufacturingdata/gold_product_count.parquet")


# COMMAND ----------

df_gold_count.coalesce(1).write.mode("overwrite").parquet("/mnt/manufacturingdata/gold_factory_location_tmp")

# Find the actual Parquet file inside the folder
files = dbutils.fs.ls("/mnt/manufacturingdata/gold_factory_location_tmp")
parquet_file = [f.path for f in files if f.path.endswith(".parquet")][0]

# Move it to the main directory with a fixed name
dbutils.fs.mv(parquet_file, "/mnt/manufacturingdata/gold_factory_location.parquet", True)


# COMMAND ----------

display(dbutils.fs.ls("/mnt/manufacturingdata"))


# COMMAND ----------

df_gold_count.coalesce(1).write.mode("overwrite").parquet("/mnt/manufacturingdata/gold_product_count_tmp")

# Get the exact file name that was created
files = dbutils.fs.ls("/mnt/manufacturingdata/gold_product_count_tmp")
parquet_file = [f.path for f in files if f.path.endswith(".parquet")][0]

# Move the file to the main directory with a fixed name
dbutils.fs.mv(parquet_file, "/mnt/manufacturingdata/gold_product_count.parquet", True)


# COMMAND ----------

df_gold_count.coalesce(1).write.mode("overwrite").parquet("/mnt/manufacturingdata/tmp_gold")

# Find the Parquet file inside the directory
files = dbutils.fs.ls("/mnt/manufacturingdata/tmp_gold")
parquet_file = [f.path for f in files if f.path.endswith(".parquet")][0]

# Move and rename the file
dbutils.fs.mv(parquet_file, "/mnt/manufacturingdata/gold_factory_location.parquet", True)

# Remove the temporary folder
dbutils.fs.rm("/mnt/manufacturingdata/tmp_gold", True)

