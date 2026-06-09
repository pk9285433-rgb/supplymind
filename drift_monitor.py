import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine(os.environ.get("DATABASE_URL",
    "postgresql://postgres.mtgtxjahbovxgpummxfl:gKGFf2AgnNvEjDGw@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"))

# Get monthly OTIF per supplier
df = pd.read_sql("""
    SELECT supplier_id, month, otif_percentage
    FROM supplier_performance
    ORDER BY supplier_id, month DESC
""", engine)

# Calculate month over month change
df['month'] = pd.to_datetime(df['month'])
df = df.sort_values(['supplier_id', 'month'])

# Get last 2 months per supplier
results = []
for sid, group in df.groupby('supplier_id'):
    group = group.sort_values('month', ascending=False)
    if len(group) >= 2:
        current = group.iloc[0]['otif_percentage']
        previous = group.iloc[1]['otif_percentage']
        change = current - previous
        results.append({
            'supplier_id': sid,
            'current_otif': round(current, 2),
            'previous_otif': round(previous, 2),
            'change_pp': round(change, 2),
            'drift_alert': 'YES' if change < -3 else 'NO'
        })

drift_df = pd.DataFrame(results)

# Show suppliers with drift
alerts = drift_df[drift_df['drift_alert'] == 'YES']
print(f"Total suppliers monitored: {len(drift_df)}")
print(f"Drift alerts fired: {len(alerts)}")
print("\nTop 3 suppliers with OTIF decline:")
top3 = drift_df.nsmallest(3, 'change_pp')
print(top3.to_string())

print("\nAll alerts:")
print(alerts.head(10).to_string())