
import requests

base = 'https://supplymind-zmk0.onrender.com'
suppliers = [
    'SUP-0001','SUP-0010','SUP-0020','SUP-0030',
    'SUP-0040','SUP-0050','SUP-0060','SUP-0070',
    'SUP-0080','SUP-0090','SUP-0100','SUP-0110',
    'SUP-0120','SUP-0130','SUP-0140','SUP-0150',
    'SUP-0160','SUP-0170','SUP-0180','SUP-0190'
]

print('ACTION RECOMMENDATIONS TEST — 20 SUPPLIERS')
print('=' * 70)

for sid in suppliers:
    r = requests.get(
        f'{base}/api/supplier-actions/{sid}',
        timeout=30
    )
    d = r.json()
    name = d.get('supplier_name', 'N/A')
    total = d.get('total_actions', 0)
    actions = d.get('recommended_actions', [])
    print(f'{sid} | {name}')
    for a in actions:
        print(f"  [{a['urgency']}] {a['action']}")
        print(f"  Reason: {a['reason']}")
        print(f"  Act within: {a['act_within']}")
    print()

print('=' * 70)
print('Total suppliers tested: 20')
