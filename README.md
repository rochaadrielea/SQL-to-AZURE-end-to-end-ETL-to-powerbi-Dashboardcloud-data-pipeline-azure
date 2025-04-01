# SQL-to-AZURE-end-to-end-ETL-to-powerbi-Dashboard

## 📌 Overview

This project demonstrates a complete **ETL (Extract, Transform, Load)** pipeline using:

- **SQLite** as a local source for manufacturing quality control data
- **Azure Blob Storage** for cloud storage and file access
- **Azure Databricks + PySpark** for scalable data processing
- **Power BI** for building dashboards based on clean, aggregated data

The system follows a **modern Data Lakehouse structure** with **Bronze**, **Silver**, and **Gold** data layers to represent raw, cleaned, and aggregated data, respectively.

---

## ⚙️ How It Works

### 🔹 Step 1: Data Simulation (Local)
- Manufacturing data (product quality, temperature, pressure, etc.) is generated in Python and stored in a **SQLite database** (`manufacturing_qc.db`).

### 🔹 Step 2: Upload to Azure
- The `.db` file is uploaded to **Azure Blob Storage** using the Azure SDK for Python.
- Blob containers are listed to confirm the upload.

### 🔹 Step 3: Mount in Azure Databricks
- The Azure storage container is **mounted into Databricks File System (DBFS)**.
- The SQLite file is **copied from DBFS to local driver node**.

### 🔹 Step 4: Data Processing with PySpark
- The SQLite table is read into a **Spark DataFrame**.
- Data is analyzed for nulls, uniqueness, and classified into:
  - 🥉 Bronze: Raw data with high nulls
  - 🥈 Silver: Clean and structured data
  - 🥇 Gold: Aggregated KPIs (e.g. defect rate by factory)

### 🔹 Step 5: Power BI Dashboard
- Gold-level data (in Parquet format) is stored back into **Azure Blob Storage**.
- Power BI connects to Azure Blob Storage or Azure SQL to visualize key metrics:
  - 📉 Average defect rate by factory
  - 📦 Product count per location
  - 📊 Time-based trends in manufacturing quality

---

## 🛠️ Tools Used

- **Python** (data generation, Azure SDK)
- **SQLite** (local lightweight database)
- **Azure Blob Storage** (cloud file storage)
- **Azure Databricks** (processing + transformation)
- **PySpark** (distributed ETL)
- **Power BI** (dashboard visualization)

---

## 📥 Inputs

- `manufacturing_qc.db` file (SQLite database)
- Table: `QualityControl` with fields like:
  - `Product_ID`
  - `Temperature`
  - `Defect_Rate`
  - `Factory_Location`
  - `Production_Date`

---

## 📤 Outputs

- 🟤 **Bronze Layer**: Raw parquet dataset stored in Azure
- ⚪ **Silver Layer**: Cleaned dataset with validated schema
- 🟡 **Gold Layer**: Aggregated metrics ready for reporting
  - Stored in `.parquet` format
  - Connected to Power BI

---

## ✅ Use Cases

- Manufacturing KPIs & quality tracking
- Data pipeline demonstration for interviews
- Teaching ETL concepts using Azure ecosystem
- Prototyping Data Lakehouse architecture with cloud tools

---

## 📎 Notes

- Easy to scale: works for small files or big datasets
- All services used are cloud-based and production-ready
- Modular code: easy to adapt to different data models or domains
