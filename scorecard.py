import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine(os.environ.get("DATABASE_URL",
    "postgresql://postgres.mtgtxjahbovxgpummxfl:gKGFf2AgnNvEjDGw@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"))

# Load supplier performance data
df = pd.read_sql("""
    SELECT 
        sp.supplier_id,
        s.supplier_name,
        s.city,
        AVG(sp.otif_percentage) as otif_pct,
        AVG(sp.avg_lead_time_days) as avg_lead_time,
        AVG(sp.quality_reject_rate_pct) as quality_reject,
        AVG(sp.fill_rate_pct) as fill_rate,
        AVG(sp.capacity_utilization_pct) as capacity_util,
        AVG(sp.invoices_paid_on_time * 100.0 / 
            NULLIF(sp.invoices_submitted, 0)) as payment_compliance
    FROM supplier_performance sp
    JOIN suppliers s ON sp.supplier_id = s.supplier_id
    GROUP BY sp.supplier_id, s.supplier_name, s.city
""", engine)

# Color coding function
def color_code(row):
    if row['otif_pct'] > 90 and row['quality_reject'] < 2 and row['fill_rate'] > 95:
        return 'GREEN'
    elif row['otif_pct'] < 80 or row['quality_reject'] > 5 or row['fill_rate'] < 85:
        return 'RED'
    else:
        return 'AMBER'

df['color'] = df.apply(color_code, axis=1)
df = df.round(2)

print(f"Total suppliers scored: {len(df)}")
print(f"GREEN: {len(df[df['color']=='GREEN'])}")
print(f"AMBER: {len(df[df['color']=='AMBER'])}")
print(f"RED:   {len(df[df['color']=='RED'])}")
print("\nSample 10 suppliers:")
print(df[['supplier_id','supplier_name','otif_pct','avg_lead_time',
          'quality_reject','fill_rate','capacity_util',
          'payment_compliance','color']].head(10).to_string())

df.to_csv("scorecard_output.csv", index=False)
print("\nScorecard saved to scorecard_output.csv")