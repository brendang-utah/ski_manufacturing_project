import requests

id = 2

api_url = f'http://localhost:8000/api/users/{id}/'

response = requests.get(url=api_url,
                        headers={'Content-Type' : 'application/json'})

if response.status_code==200:
    print(f"User retrieved successfully.")
    user_data = response.json()
    print(user_data)
else:
    print(f"Error retrieving user")