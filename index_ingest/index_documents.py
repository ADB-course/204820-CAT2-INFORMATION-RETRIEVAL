import json
import requests

# Load JSON file
with open("diabetes.json") as f:
    docs = json.load(f)

# Index each document
for doc in docs:
    res = requests.post("http://localhost:9200/diabetes/_doc", json=doc)
    print(res.status_code, res.json())

