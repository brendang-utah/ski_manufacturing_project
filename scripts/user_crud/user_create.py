import requests
import json

api_url = 'http://localhost:8000/api/users/'

user_data = {
    'username' : 'testuser',
    'password' : 'testpassword',
    'first_name' : 'testfirstname',
    'last_name' : 'testlastname',
    'email' : 'test@email.com',
    'phone_number' : '1112223333',
    'address' : 'testaddress',
    'role' : 'testrole',
}

response = requests.post(url=api_url,
                         data=json.dumps(user_data),
                         headers={'Content-Type': 'application/json'})

if response.status_code==201:
    print(f"User created successfully.")
else:
    print(f"Error creating user.{response.text}")