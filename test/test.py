import requests

resp = requests.post("http://localhost:5000/crop")

print(resp.text)