import requests, time, statistics

base = 'https://supplymind-zmk0.onrender.com'
endpoints = [
    '/api/analytics/supplier-details?supplier_id=SUP-0001',
    '/api/analytics/supplier-risks',
    '/api/analytics/inventory-summary',
    '/api/analytics/forecast-accuracy',
    '/api/analytics/disruption-risks',
    '/api/analytics/inventory-health',
    '/api/analytics/reorder-alerts',
    '/api/analytics/demand-accuracy',
    '/api/analytics/dashboard-summary',
]

results = []
print('Testing all endpoints...')
print('=' * 70)

for ep in endpoints:
    times = []
    status_codes = []
    rows = 0
    errors = 0

    for i in range(5):
        try:
            start = time.time()
            r = requests.get(base + ep, timeout=30)
            ms = round((time.time()-start)*1000, 2)
            times.append(ms)
            status_codes.append(r.status_code)
            data = r.json()
            if isinstance(data, list):
                rows = len(data)
            elif isinstance(data, dict):
                rows = 1
        except Exception as e:
            errors += 1
            print(f'ERROR on {ep}: {e}')

    if times:
        avg = round(statistics.mean(times), 2)
        mn = min(times)
        mx = max(times)
        med = round(statistics.median(times), 2)
        p95 = round(sorted(times)[int(len(times)*0.95)-1], 2)
        success = status_codes.count(200)
        print(f'Endpoint: {ep}')
        print(f'  Status: {success}/5 success')
        print(f'  Min: {mn}ms | Max: {mx}ms | Avg: {avg}ms | Median: {med}ms')
        print(f'  Rows returned: {rows} | Errors: {errors}')
        print()
        results.append({
            'endpoint': ep,
            'success_rate': f'{success}/5',
            'min': mn, 'max': mx,
            'avg': avg, 'median': med,
            'rows': rows, 'errors': errors
        })

print('=' * 70)
print('SUMMARY:')
all_times = [r['avg'] for r in results]
print(f'Overall Avg Latency: {round(sum(all_times)/len(all_times),2)}ms')
print(f'Total Endpoints Tested: {len(results)}')
print(f'Total Errors: {sum(r["errors"] for r in results)}')