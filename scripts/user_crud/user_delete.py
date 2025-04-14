import requests

id = 2

api_url = f'http://localhost:8000/api/users/{id}/'

response = requests.delete(url=api_url,
                         headers={'Content-Type': 'application/json'})

if response.status_code==204:
    print(f"User deleted successfully.")
else:
    print(f"Error deleting user.")