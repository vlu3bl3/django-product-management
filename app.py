import requests
import json
data = requests.get("https://jsonplaceholder.typicode.com/users")
print(data)