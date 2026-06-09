import requests, time, statistics

base = 'https://supplymind-zmk0.onrender.com'
endpoints = [
    '/api/analytics/supplier-details?supplier_id=SUP-0001',
    '/api/analytics/supplier-risks',
    '/api/analytics/inventory-summary',
    '/api/analytics/forecast-accuracy',
    '/api/analytics/disruption-risks',
]

all_times = []

for ep in endpoints:
    times = []
    for i in range(5):
        try:
            start = time.time()
            r = requests.get(base + ep, timeout=30)
            ms = round((time.time()-start)*1000, 2)
            times.append(ms)
            all_times.append(ms)
        except:
            pass
    
    if times:
        print(f'Endpoint: {ep}')
        print(f'  Min: {min(times)}ms')
        print(f'  Max: {max(times)}ms')
        print(f'  Avg: {round(statistics.mean(times),2)}ms')
        print(f'  Median: {round(statistics.median(times),2)}ms')
        print()

# Overall summary
all_times.sort()
n = len(all_times)
p95 = all_times[int(n*0.95)-1]
p99 = all_times[int(n*0.99)-1]

print('=' * 50)
print('OVERALL LATENCY SUMMARY')
print('=' * 50)
print(f'Min:    {min(all_times)}ms')
print(f'Max:    {max(all_times)}ms')
print(f'Avg:    {round(statistics.mean(all_times),2)}ms')
print(f'Median: {round(statistics.median(all_times),2)}ms')
print(f'P95:    {p95}ms')
print(f'P99:    {p99}ms')
print(f'Total calls: {n}')