import requests

#url = 'https://api.example.com/resource'
url = 'http://127.0.0.1:8888/scores/x/'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()  # Assuming the response contains JSON data
    # Process the retrieved data
else:
    print("Failed to fetch data:", response.status_code)
