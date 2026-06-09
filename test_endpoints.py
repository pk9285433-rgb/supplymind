import requests

base = "https://supplymind-zmk0.onrender.com"

endpoints = [
    "/api/analytics/supplier-details?supplier_id=SUP-0001",
    "/api/analytics/supplier-risks",
    "/api/analytics/inventory-summary",
    "/api/analytics/forecast-accuracy",
    "/api/analytics/disruption-risks"
]

for ep in endpoints:
    r = requests.get(base + ep)
    print(r.status_code, ep)