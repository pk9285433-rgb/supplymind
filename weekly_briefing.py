import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import date

engine = create_engine(os.environ.get("DATABASE_URL",
    "postgresql://postgres.mtgtxjahbovxgpummxfl:gKGFf2AgnNvEjDGw@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"))

# Top 5 at-risk suppliers
risk_df = pd.read_sql("""
    SELECT sp.supplier_id, s.supplier_name,
           AVG(sp.otif_percentage) as avg_otif,
           AVG(sp.fill_rate_pct) as avg_fill_rate
    FROM supplier_performance sp
    JOIN suppliers s ON sp.supplier_id = s.supplier_id
    GROUP BY sp.supplier_id, s.supplier_name
    ORDER BY avg_otif ASC
    LIMIT 5
""", engine)

# Stockout SKUs
stockout_df = pd.read_sql("""
    SELECT ip.sku_id, sk.sku_name, ip.days_of_cover,
           ip.closing_stock_units
    FROM inventory_positions ip
    JOIN skus sk ON ip.sku_id = sk.sku_id
    WHERE ip.date = (SELECT MAX(date) FROM inventory_positions)
    AND ip.days_of_cover < 7
    ORDER BY ip.days_of_cover ASC
""", engine)

# PO Performance
po_df = pd.read_sql("""
    SELECT 
        COUNT(*) as total_pos,
        SUM(CASE WHEN delivered_on_time = 1 THEN 1 ELSE 0 END) as on_time,
        ROUND(SUM(CASE WHEN delivered_on_time = 1
                  THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as on_time_rate
    FROM purchase_orders
""", engine)

print("=" * 60)
print(f"  WEEKLY EXECUTIVE BRIEFING — {date.today()}")
print("  SupplyMind Supply Chain Intelligence")
print("=" * 60)

print("\n TOP 5 AT-RISK SUPPLIERS:")
print("-" * 40)
for _, row in risk_df.iterrows():
    print(f"  {row['supplier_id']} | {row['supplier_name'][:25]}")
    print(f"    OTIF: {round(row['avg_otif'],1)}% | Fill Rate: {round(row['avg_fill_rate'],1)}%")

print(f"\n STOCKOUT RISK SKUs (< 7 days cover): {len(stockout_df)}")
print("-" * 40)
for _, row in stockout_df.iterrows():
    print(f"  {row['sku_id']} | {row['sku_name'][:25]} | {round(row['days_of_cover'],1)} days")

print(f"\n PO PERFORMANCE:")
print("-" * 40)
po = po_df.iloc[0]
print(f"  Total POs: {int(po['total_pos'])}")
print(f"  On Time: {int(po['on_time'])}")
print(f"  On-Time Rate: {po['on_time_rate']}%")
print("\n" + "=" * 60)