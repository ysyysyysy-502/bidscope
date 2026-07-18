import requests

BASE = 'http://127.0.0.1:8000'
query = '最近3个月上海服务器与算力招标，请每天9:00汇总发送给我'
res = requests.post(f'{BASE}/api/v1/runs', json={'query': query})
print(res.status_code)
print(res.json()['run_id'])
print(res.json()['report_download_url'])
