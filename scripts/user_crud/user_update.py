import requests
import json

id = 2

api_url = f'http://localhost:8000/api/users/{id}/'

user_data = {
    'username' : 'updateduser',
    'password' : 'updatedpassword',
    'first_name' : 'tupdatedfirstname',
    'last_name' : 'updatedlastname',
    'email' : 'updated@email.com',
    'phone_number' : '4445556666',
    'address' : 'updatedaddress',
    'role' : 'updatedrole',
}

response = requests.put(url=api_url,
                         data=json.dumps(user_data),
                         headers={'Content-Type': 'application/json'})

if response.status_code==200:
    print(f"User updated successfully.")
else:
    print(f"Error updateing user.{response.text}")