import requests
import json

url = "http://localhost:8000/api/bfhl"
test_data = {"data": ["a","1","334","4","R", "$"]}

response = requests.post(url, json=test_data)
print("Status Code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))