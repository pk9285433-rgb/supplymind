import requests
import time
import pandas as pd

BASE_URL = "https://supplymind-zmk0.onrender.com"

supplier_ids = [
    "SUP-0001",
    "SUP-0005",
    "SUP-0010",
    "SUP-0015",
    "SUP-0020",
    "SUP-0025",
    "SUP-0030",
    "SUP-0035",
    "SUP-0040",
    "SUP-0045",
    "SUP-0050",
    "SUP-0055",
    "SUP-0060",
    "SUP-0065",
    "SUP-0070",
    "SUP-0075",
    "SUP-0080",
    "SUP-0085",
    "SUP-0090",
    "SUP-0095"
]

results = []

for supplier_id in supplier_ids:

    start = time.time()

    response = requests.get(
        f"{BASE_URL}/api/analytics/supplier-details",
        params={"supplier_id": supplier_id}
    )

    end = time.time()

    latency = round((end - start) * 1000, 2)

    results.append({
        "Supplier ID": supplier_id,
        "Status Code": response.status_code,
        "Latency(ms)": latency
    })

df = pd.DataFrame(results)
warm_df=df.iloc[1:]

print("\nPERFORMANCE TABLE")
print(df)

print("\nSUMMARY")
print("Minimum:", warm_df["Latency(ms)"].min(), "ms")
print("Maximum:", warm_df["Latency(ms)"].max(), "ms")
print("Average:", round(warm_df["Latency(ms)"].mean(), 2), "ms")

df.to_csv("supplier_performance.csv", index=False)

print("\nCSV file saved as supplier_performance.csv")