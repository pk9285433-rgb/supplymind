
import requests

base = 'https://supplymind-zmk0.onrender.com'
r = requests.get(f'{base}/api/analytics/supplier-resilience')
data = r.json()
print(f'Total SKUs analyzed: {data["total_skus_analyzed"]}')
print(f'Critical with no backup: {data["critical_no_backup_count"]}')
print()
print('Top 5 lowest resilience scores:')
for item in data['resilience_data'][:5]:
    print(f'  {item["sku_id"]}: Score {item["resilience_score"]}/10, Backup: {item["has_backup"]}')
    