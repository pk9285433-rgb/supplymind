import requests

BASE_URL = "https://supplymind-zmk0.onrender.com"

supplier_ids = [
    "SUP-0001",
    "SUP-0010",
    "SUP-0020",
    "SUP-0030",
    "SUP-0040"
]

for supplier_id in supplier_ids:

    response = requests.get(
        f"{BASE_URL}/api/analytics/supplier-details",
        params={"supplier_id": supplier_id}
    )

    data = response.json()
    print(data)

    print("\n----------------------")
    print("Supplier:", supplier_id)
    print("City:", data.get("city"))
    print("Tier:", data.get("tier"))
    print("Current OTIF:", data.get("current_otif"))
    print("Fill Rate %:", data.get("fill_rate_pct"))
    print("Average Lead Time:", data.get("avg_lead_time_days"))