import requests, time

start = time.time()
r = requests.get('https://supplymind-zmk0.onrender.com/api/analytics/supplier-segments')
ms = round((time.time()-start)*1000, 2)
print(f'Status: {r.status_code}')
print(f'Time: {ms}ms')
data = r.json()
print(f'Total suppliers: {data["total_suppliers_analyzed"]}')
for seg in data['segments']:
    print(f'{seg["segment_name"]}: {seg["supplier_count"]} suppliers, OTIF {seg["average_metrics"]["avg_otif"]}%, Trend: {seg["trend"]}')