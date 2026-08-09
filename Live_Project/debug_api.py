import requests
try:
    response = requests.get("https://reqres.in/api/users?page=2", headers={"User-Agent": "Mozilla/5.0"})
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
