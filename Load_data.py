import os

import pandas as pd
from sqlalchemy import create_engine
engine = create_engine(
    "postgresql://postgres.mtgtxjahbovxgpummxfl:gKGFf2AgnNvEjDGw@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
)

tables = {
   'suppliers': 'suppliers.csv',
   'skus': 'skus.csv',
   'purchase_orders': 'purchase_orders.csv',
   'demand_history': 'demand_history.csv',
   'inventory_positions': 'inventory_positions.csv',
   'supplier_performance': 'supplier_performance.csv'
}

for table, file in tables.items():
   df = pd.read_csv(f'data/raw/{file}')
   df.to_sql(table, engine, if_exists='replace', index=False)
   print(f" {table} loaded — {len(df)} rows")