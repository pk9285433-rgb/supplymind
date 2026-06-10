supplier_df = pd.read_sql(query, engine)

print("Critical:", len(supplier_df[supplier_df['status']=="critical"]))
print("Warning :", len(supplier_df[supplier_df['status']=="warning"]))
print("Healthy :", len(supplier_df[supplier_df['status']=="healthy"]))
print("Total   :", len(supplier_df))