import pandas as pd
from sqlalchemy import create_engine, text

# Connect to our newly created SQLite database
engine = create_engine("sqlite:///supply_chain.db")

# --- QUERY 1: Inventory Stockout Risk Alert ---
query_1 = """
SELECT 
    warehouse_name,
    product_name,
    category,
    quantity_on_hand,
    safety_stock_level,
    reorder_point,
    CASE 
        WHEN quantity_on_hand <= safety_stock_level THEN '🔴 CRITICAL: Stockout Risk'
        WHEN quantity_on_hand <= reorder_point THEN '🟡 WARNING: Reorder Triggered'
        ELSE '🟢 Healthy'
    END AS inventory_status
FROM inventory i
JOIN warehouses w ON i.warehouse_id = w.warehouse_id
JOIN products p ON i.product_id = p.product_id
ORDER BY quantity_on_hand ASC;
"""

# --- QUERY 2: Supplier Reliability Matrix ---
query_2 = """
SELECT 
    supplier_name,
    COUNT(shipment_id) AS total_shipments,
    SUM(CASE WHEN status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_shipments,
    ROUND((SUM(CASE WHEN status = 'Delayed' THEN 1 ELSE 0 END) * 100.0 / COUNT(shipment_id)), 2) AS delay_rate_percentage
FROM shipments
GROUP BY supplier_name
ORDER BY delay_rate_percentage DESC;
"""

print("\n📊 RUNNING SUPPLY CHAIN ANALYTICS...")
print("="*60)

with engine.connect() as connection:
    print("\n🔍 INSIGHT 1: CURRENT WAREHOUSE STOCK HEALTH (Top 5 At Risk)")
    df1 = pd.read_sql(text(query_1), connection)
    print(df1.head(5).to_string(index=False))
    
    print("\n" + "="*60)
    print("\n🔍 INSIGHT 2: SUPPLIER PERFORMANCE MATRIX")
    df2 = pd.read_sql(text(query_2), connection)
    print(df2.to_string(index=False))