import requests 
import json

def submit_auth_request():
    auth_url = 'https://register.terrortime.app/oauth2/token'
    chat_url = 'https://chat.terrortime.app'
    basic = "cm9iZXJ0by0tdmhvc3QtMzg1QHRlcnJvcnRpbWUuYXBwOlNtSldPQXFoODBEZGtO"
    data = {"audience":"", 
            "grant_type": "client_credentials", 
            "scope": "chat"}
    header = {"Authorization": f'Basic {basic}',
                               'Accept-Encoding': 'UTF-8',
                               'Content-Type': 'application/x-www-form-urlencoded',
                               'X-Server-Select': 'oauth'}

    s = requests.session()
    r = s.post(auth_url, data=data, 
                      headers=header)
    if r.status_code != 200:
        print("Failure to authenticate")
        return None
    else:
        response_token = json.loads(r.content.decode())

        return response_token['access_token']

if __name__ == "__main__":
    print(submit_auth_request())
