import requests

data = {
    "username" : "kmvdj23",
    "password" : "kristopher@23",
    "email"    : "kristophermatthewdejesus@gmail.com"
}


response = requests.post('http://localhost/api/v1/add_account', data=data)
print(response.text)
