import requests

base = 'https://supplymind-zmk0.onrender.com'
r = requests.get(f'{base}/api/analytics/supplier-segments')
data = r.json()

for seg in data['segments']:
    print(f'{seg["segment_name"]}: {seg["supplier_count"]} suppliers')