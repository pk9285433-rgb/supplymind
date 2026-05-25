import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://postgres:skillvance2025@localhost:5432/postgres'
)

def get_inventory_health():
    query = """
    SELECT
        COUNT(DISTINCT sku_id) as total_skus,
        SUM(CASE WHEN days_of_cover < 7
            THEN 1 ELSE 0 END) as critical,
        SUM(CASE WHEN days_of_cover
            BETWEEN 7 AND 14
            THEN 1 ELSE 0 END) as warning,
        SUM(CASE WHEN days_of_cover > 60
            THEN 1 ELSE 0 END) as overstock,
        ROUND(AVG(days_of_cover)::numeric,1)
            as avg_doc
    FROM inventory_positions
    WHERE date = (
        SELECT MAX(date)
        FROM inventory_positions
    )
    """
    return pd.read_sql(query, engine).to_dict(
        orient='records')[0]

def get_reorder_alerts():
    query = """
    SELECT
        sk.sku_name,
        sk.category,
        ip.closing_stock_units as current_stock,
        sk.reorder_point_units,
        ip.days_of_cover,
        CASE
            WHEN ip.days_of_cover < 7
            THEN 'Critical'
            WHEN ip.days_of_cover < 14
            THEN 'Warning'
            ELSE 'OK'
        END as urgency
    FROM skus sk
    JOIN inventory_positions ip
        ON sk.sku_id = ip.sku_id
    WHERE ip.date = (
        SELECT MAX(date)
        FROM inventory_positions
    )
    AND ip.is_low_stock_alert = 1
    ORDER BY ip.days_of_cover ASC
    LIMIT 20
    """
    return pd.read_sql(query, engine).to_dict(
        orient='records')

def get_supplier_summary():
    query = """
    SELECT
        ROUND(AVG(otif_percentage)::numeric,2)
            as avg_otif,
        COUNT(DISTINCT CASE
            WHEN otif_percentage < 75
            THEN supplier_id END)
            as high_risk_count,
        COUNT(DISTINCT supplier_id)
            as total_suppliers
    FROM supplier_performance
    WHERE month = (
        SELECT MAX(month)
        FROM supplier_performance
    )
    """
    return pd.read_sql(query, engine).to_dict(
        orient='records')[0]

# Test all 3 functions
print("=== Inventory Health ===")
print(get_inventory_health())

print("\n=== Reorder Alerts ===")
alerts = get_reorder_alerts()
print(f"Total alerts: {len(alerts)}")
for a in alerts[:5]:
    print(f"  {a['sku_name']} — {a['days_of_cover']} days — {a['urgency']}")

print("\n=== Supplier Summary ===")
print(get_supplier_summary())