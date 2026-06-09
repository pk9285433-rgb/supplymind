import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine(os.environ.get('DATABASE_URL',
    'postgresql://postgres.mtgtxjahbovxgpummxfl:gKGFf2AgnNvEjDGw@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres'))

# Check what current query returns
print('=== CURRENT QUERY RESULT ===')
df1 = pd.read_sql('''
    SELECT ip.sku_id, sk.sku_name, ip.days_of_cover,
           ip.closing_stock_units
    FROM inventory_positions ip
    JOIN skus sk ON ip.sku_id = sk.sku_id
    WHERE ip.date = (SELECT MAX(date) FROM inventory_positions)
    AND ip.days_of_cover < 7
    ORDER BY ip.days_of_cover ASC
''', engine)
print(f'SKUs with days_of_cover < 7: {len(df1)}')
print(df1.to_string())

# Check with wider threshold
print('\n=== WIDER THRESHOLD (< 14 days) ===')
df2 = pd.read_sql('''
    SELECT ip.sku_id, sk.sku_name, ip.days_of_cover,
           ip.closing_stock_units
    FROM inventory_positions ip
    JOIN skus sk ON ip.sku_id = sk.sku_id
    WHERE ip.date = (SELECT MAX(date) FROM inventory_positions)
    AND ip.days_of_cover < 14
    ORDER BY ip.days_of_cover ASC
''', engine)
print(f'SKUs with days_of_cover < 14: {len(df2)}')
print(df2.to_string())

# Check with even wider threshold
print('\n=== EVEN WIDER (< 30 days) ===')
df3 = pd.read_sql('''
    SELECT COUNT(*) as count
    FROM inventory_positions ip
    WHERE ip.date = (SELECT MAX(date) FROM inventory_positions)
    AND ip.days_of_cover < 30
''', engine)
print(f'SKUs with days_of_cover < 30: {df3.iloc[0]["count"]}')

# Check min days of cover
print('\n=== DISTRIBUTION ===')
df4 = pd.read_sql('''
    SELECT 
        MIN(days_of_cover) as min_doc,
        MAX(days_of_cover) as max_doc,
        AVG(days_of_cover) as avg_doc,
        COUNT(*) as total_skus
    FROM inventory_positions
    WHERE date = (SELECT MAX(date) FROM inventory_positions)
''', engine)
print(df4.to_string())