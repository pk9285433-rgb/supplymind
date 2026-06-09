import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine(os.environ.get('DATABASE_URL',
    'postgresql://postgres.mtgtxjahbovxgpummxfl:gKGFf2AgnNvEjDGw@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres'))

sid = 'SUP-0050'
df = pd.read_sql("""
    SELECT delivered_on_time
    FROM purchase_orders
    WHERE supplier_id = %(sid)s
""", engine, params={'sid': sid})

total = len(df)
on_time = df['delivered_on_time'].sum()
otif = round(on_time / total * 100, 2)
print(f'Supplier: {sid}')
print(f'Total POs: {total}')
print(f'On Time: {on_time}')
print(f'Manual OTIF: {otif}%')

sp = pd.read_sql("""
    SELECT AVG(otif_percentage) as avg_otif
    FROM supplier_performance
    WHERE supplier_id = %(sid)s
""", engine, params={'sid': sid})

scorecard_otif = round(sp.iloc[0]['avg_otif'], 2)
print(f'Scorecard OTIF: {scorecard_otif}%')