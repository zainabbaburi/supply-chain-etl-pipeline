-- 1. Create the Warehouses Table
CREATE TABLE warehouses (
    warehouse_id SERIAL PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL
);

-- 2. Create the Products Table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL,
    retail_price DECIMAL(10, 2) NOT NULL
);

-- 3. Create the Inventory Snapshot Table
-- tracks current stock and reorder thresholds at specific warehouses
CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    warehouse_id INT REFERENCES warehouses(warehouse_id) ON DELETE CASCADE,
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
    quantity_on_hand INT NOT NULL CHECK (quantity_on_hand >= 0),
    safety_stock_level INT NOT NULL, -- The minimum buffer stock needed
    reorder_point INT NOT NULL       -- Trigger point to order more stock
);

-- 4. Create the Shipments/Supply Chain Table
-- tracks supplier delivery performance and transit delays
CREATE TABLE shipments (
    shipment_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
    warehouse_id INT REFERENCES warehouses(warehouse_id) ON DELETE CASCADE,
    supplier_name VARCHAR(100) NOT NULL,
    order_date DATE NOT NULL,
    expected_delivery_date DATE NOT NULL,
    actual_delivery_date DATE, -- Can be NULL if it hasn't arrived yet
    quantity_ordered INT NOT NULL,
    status VARCHAR(50) NOT NULL -- 'In Transit', 'Delivered', 'Delayed'
);