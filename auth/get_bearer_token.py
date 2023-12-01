import requests
import json
def get_saml_token():
    url = "https://idbrokerbts.webex.com/idb/token/8b158acc-2cf4-4e16-9f76-a1d751b6fcba/v2/actions/GetBearerToken/invoke"

    payload = json.dumps({
      "name": "wcc-core-intgus1-machine",
      "password": "UrCB8/6eiC7(six6?[!tS|23;2jZW5R+@Jul-17-2023"
    })
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'amlbcookie=15; amlbcookiesm=15; JSESSIONID=D476EE957197380300C44980ACC1973F'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['BearerToken']

def get_saml_token_prod():
    url = "https://idbroker.webex.com/idb/token/31e53699-5914-45d4-af9f-ba49d538e382/v2/actions/GetBearerToken/invoke"

    payload = json.dumps({
	"name" : "wcc-core-produs1-machine2",
	"password" : "w1#15V~}wXn9KI*E2Q5In(br(8gS9|v&@May-25-2023"
    })
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'amlbcookie=15; amlbcookiesm=15; JSESSIONID=D476EE957197380300C44980ACC1973F'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['BearerToken']

def get_bearer_token():

    url = "https://idbrokerbts.webex.com/idb/oauth2/v1/access_token"

    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:saml2-bearer',
        'assertion': get_saml_token(),
        'scope': 'cjp:config_write cjp:config_read sunlight-internal-service:read sunlight-internal-service:write'
    }
    headers = {
        'Authorization': 'Basic QzRjNTA5OThhYjg3N2MyYzhmNzJkN2VkNzdhMTlhODE0MjJkNDA0ZTNjMzE3NGMwYWQ2N2QzNzA3ZjE0ZDc4OWI6YjY1ZThjNTQ4MWQ4Y2RhYjA3Y2M3MTFkMzMwNzBhZWFiY2YyZjZlN2I1NDVhM2M0MzVmNTFkZGI3MWMwYTA1Mw==',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'amlbcookie=15; amlbcookiesm=15; JSESSIONID=27F44F9ECEB872A413C290003D0A5CC8'
    }

    response = requests.request("POST", url, headers=headers, data=data)

    print(response.json()['access_token'])

    return response.json()['access_token']

def get_bearer_token_prod():

    url = "https://idbroker.webex.com/idb/oauth2/v1/access_token"

    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:saml2-bearer',
        'assertion': get_saml_token_prod(),
        'scope': 'cjp:config_write cjp:config_read sunlight-internal-service:read sunlight-internal-service:write'
    }
    headers = {
        'Authorization': 'Basic QzRjNTA5OThhYjg3N2MyYzhmNzJkN2VkNzdhMTlhODE0MjJkNDA0ZTNjMzE3NGMwYWQ2N2QzNzA3ZjE0ZDc4OWI6YjY1ZThjNTQ4MWQ4Y2RhYjA3Y2M3MTFkMzMwNzBhZWFiY2YyZjZlN2I1NDVhM2M0MzVmNTFkZGI3MWMwYTA1Mw==',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'amlbcookie=15; amlbcookiesm=15; JSESSIONID=27F44F9ECEB872A413C290003D0A5CC8'
    }

    response = requests.request("POST", url, headers=headers, data=data)

    return response.json()['access_token']