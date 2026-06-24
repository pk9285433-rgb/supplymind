import requests, time

segments = ['high-performing', 'medium-performing', 'low-performing', 'strategic']
base = 'https://supplymind-zmk0.onrender.com'

for seg in segments:
    start = time.time()
    r = requests.get(f'{base}/api/analytics/segment-actions/{seg}')
    ms = round((time.time()-start)*1000, 2)
    data = r.json()
    print(f'{seg}: {r.status_code} | {ms}ms | suppliers:{data.get("supplier_count",0)}')