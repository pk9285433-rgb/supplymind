import requests

base = 'https://supplymind-zmk0.onrender.com'

# Get a RED supplier first
r = requests.get(f'{base}/api/analytics/governance-status')
data = r.json()
print(f'Total suppliers: {data["total_suppliers"]}')
print(f'RED: {data["health_summary"]["red_count"]}')
print(f'YELLOW: {data["health_summary"]["yellow_count"]}')
print(f'GREEN: {data["health_summary"]["green_count"]}')

if data['critical_alerts']:
    sid = data['critical_alerts'][0]['supplier_id']
    print(f'\nTesting escalation for: {sid}')
    r2 = requests.post(f'{base}/api/analytics/escalation/{sid}?level=RED')
    print(r2.json())