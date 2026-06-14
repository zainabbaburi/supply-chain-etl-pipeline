import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text


# SQLITE DATABASE CONNECTION

DATABASE_URL = "sqlite:///supply_chain.db"
engine = create_engine(DATABASE_URL)

print(" Initializing Supply Chain Data Generation Pipeline...")


# DATA INGESTION & GENERATION


warehouses_data = [
    {"warehouse_name": "Ottawa Distribution Center", "location": "Ottawa, ON"},
    {"warehouse_name": "Toronto Hub", "location": "Toronto, ON"},
    {"warehouse_name": "Vancouver Port Facility", "location": "Vancouver, BC"}
]
df_warehouses = pd.DataFrame(warehouses_data)

products_data = [
    {"product_name": "Eco-Friendly Packaging Box", "category": "Packaging", "unit_cost": 1.50, "retail_price": 3.99},
    {"product_name": "Industrial Solder Wire", "category": "Manufacturing", "unit_cost": 12.00, "retail_price": 25.00},
    {"product_name": "Lithium-Ion Battery Pack", "category": "Electronics", "unit_cost": 45.00, "retail_price": 99.99},
    {"product_name": "Fiber Optic Cable 50m", "category": "Telecom", "unit_cost": 18.50, "retail_price": 40.00},
    {"product_name": "Aluminium Casing Unit", "category": "Hardware", "unit_cost": 8.00, "retail_price": 19.50}
]
df_products = pd.DataFrame(products_data)

inventory_records = []
np.random.seed(42)

for w_idx in range(1, len(warehouses_data) + 1):
    for p_idx in range(1, len(products_data) + 1):
        safety_stock = int(np.random.choice([50, 100, 200]))
        reorder_point = int(safety_stock * 1.5)
        quantity_on_hand = int(np.random.randint(safety_stock - 20, reorder_point + 100))
        
        inventory_records.append({
            "warehouse_id": w_idx,
            "product_id": p_idx,
            "quantity_on_hand": max(0, quantity_on_hand),
            "safety_stock_level": safety_stock,
            "reorder_point": reorder_point
        })
df_inventory = pd.DataFrame(inventory_records)

shipment_records = []
suppliers = ["Global Logistics Corp", "Nexus Manufacturing", "Apex Component Supply"]
statuses = ["Delivered", "Delayed", "In Transit"]
base_date = datetime(2026, 4, 1)

for i in range(100):
    p_id = int(np.random.randint(1, len(products_data) + 1))
    w_id = int(np.random.randint(1, len(warehouses_data) + 1))
    order_days_offset = int(np.random.randint(0, 60))
    order_date = base_date + timedelta(days=order_days_offset)
    expected_delivery = order_date + timedelta(days=7)
    status = np.random.choice(statuses, p=[0.70, 0.15, 0.15])
    
    if status == "Delivered":
        actual_delivery = expected_delivery + timedelta(days=int(np.random.randint(-2, 2)))
    elif status == "Delayed":
        actual_delivery = expected_delivery + timedelta(days=int(np.random.randint(3, 10)))
    else:
        actual_delivery = None
        
    shipment_records.append({
        "product_id": p_id,
        "warehouse_id": w_id,
        "supplier_name": np.random.choice(suppliers),
        "order_date": order_date.strftime('%Y-%m-%d'),
        "expected_delivery_date": expected_delivery.strftime('%Y-%m-%d'),
        "actual_delivery_date": actual_delivery.strftime('%Y-%m-%d') if actual_delivery else None,
        "quantity_ordered": int(np.random.choice([100, 250, 500, 1000])),
        "status": status
    })
df_shipments = pd.DataFrame(shipment_records)

print("⚙️ Data transformation complete. Preparing database tier injection...")

# DATABASE PIPELINE BULK LOADING (LOAD)

try:
    print("📖 Reading and parsing schema.sql structure...")
    with open('schema.sql', 'r') as f:
        schema_sql = f.read()
    
    # Clean PostgreSQL syntax 'SERIAL' to make it compatible with SQLite execution
    schema_sql = schema_sql.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")

    # Split commands cleanly by semicolon
    sql_statements = [cmd.strip() for cmd in schema_sql.split(';') if cmd.strip()]

    with engine.connect() as connection:
        for statement in sql_statements:
            connection.execute(text(statement))
        connection.commit()
    print(" Database tables created successfully from schema.sql.")

    # Bulk load dataframes into tables
    df_warehouses.to_sql('warehouses', engine, if_exists='append', index=False)
    df_products.to_sql('products', engine, if_exists='append', index=False)
    df_inventory.to_sql('inventory', engine, if_exists='append', index=False)
    df_shipments.to_sql('shipments', engine, if_exists='append', index=False)
    
    print(" Success! Supply Chain Database has been fully populated.")
except Exception as e:
    print(f" Error while loading data: {e}")