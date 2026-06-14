
# Supply Chain ETL Pipeline & Analytics Console

An end-to-end data engineering pipeline that simulates an enterprise supply chain logistics system, transforms raw data streams, and loads them into a structured database tier for operational analytics. 

##  System Architecture & Capabilities
This project implements a complete **Extract, Transform, Load (ETL)** architecture to solve real-world inventory tracking and vendor management challenges.

* **Data Generation & Extraction:** Utilizes Python (Pandas, NumPy) to programmatically model realistic, non-uniform corporate logistics data spanning warehouses, product catalogs, tracking intervals, and randomized supplier shipment timelines.
* **Schema Enforcement & Transformation:** Automatically reads an external declarative database architecture blueprint (`schema.sql`), dynamically translates specific data types for environmental compatibility, cleans transactional records, and enforces structural integrity.
* **Bulk Database Loading:** Leverages SQLAlchemy to securely establish programmatic connection pipelines and inject structured data directly into relational storage.
* **Business Intelligence Console:** Implements complex relational analytical scripts using advanced SQL operations (`JOIN` queries, aggregated matrices, and conditional formatting conditional logic) to isolate operational bottlenecks.

---

##  Tech Stack & Utilities
* **Languages:** Python, SQL
* **Libraries:** Pandas, NumPy, SQLAlchemy
* **Database Engine:** SQLite / PostgreSQL Compatibility

---

##  Analytics Dashboard Insights
When executed, the pipeline feeds data into an analytical query console that dynamically surfaces mission-critical business intelligence:

### 1. Warehouse Stock Health Matrix
Automatically calculates current stock positions against safety stock thresholds to isolate critical stockout vulnerabilities.
* **Logic applied:** Conditional logic (`CASE WHEN`) to dynamically flag real-time status levels (` CRITICAL`, ` WARNING`, ` Healthy`).

### 2. Supplier Reliability & Performance Matrix
Aggregates high-volume delivery timelines across independent freight vendors to score fulfillment pipelines.
* **Logic applied:** Grouped multi-table aggregations (`COUNT`, `SUM`, `ROUND`) to expose explicit supplier delay rates.

---

##  How to Run the Pipeline

### 1. Prerequisites
Ensure you have Python installed along with the required libraries:
```bash
pip install pandas numpy sqlalchemy
