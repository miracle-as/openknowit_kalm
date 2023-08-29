import requests
import json
import os
from ..common import prettyllog




def getenv():
    env = {}
    env['KALM_DNS_TYPE'] = os.getenv('KALM_DNS_TYPE')
    env['KALM_DNS_URL'] = os.getenv('KALM_DNS_URL')
    env['KALM_DNS_TOKEN'] = os.getenv('KALM_DNS_TOKEN')
    env['KALM_DNS_DOMAIN'] = os.getenv('KALM_DNS_DOMAIN')
    env['KALM_DNS_PROVIDER'] = os.getenv('KALM_DNS_PROVIDER')
    if env['KALM_DNS_TYPE'] != "cloudflare":
        print("DNS type not supported")
        exit(1)
    if env['KALM_DNS_URL'] == None:
        print("DNS URL not set")
        exit(1)
    # if url ends with /, remove it
    if env['KALM_DNS_URL'][-1] == "/":
        env['KALM_DNS_URL'] = env['KALM_DNS_URL'][:-1]

    if env['KALM_DNS_TOKEN'] == None:
        print("DNS TOKEN not set")
        exit(1)
    if env['KALM_DNS_DOMAIN'] == None:
        print("DNS DOMAIN not set")
        exit(1)
    if env['KALM_DNS_PROVIDER'] == None:
        print("DNS PROVIDER not set")
        exit(1)
    return env




def check_access():
    env = getenv()
    url = env["KALM_DNS_URL"] + "/client/v4/user/tokens/verify"
    print(url)
    print(env["KALM_DNS_TOKEN"])
    bearer = "Bearer " + os.environ.get("KALM_DNS_TOKEN", "")
    headers = {
    "Authorization": bearer,
    "Content-Type": "application/json"
    }
    print(headers)
    response = requests.get(url, headers=headers)
    print(response.content)  # Print the response content
    if response.status_code == 200:
        return True
    else:
        return False


