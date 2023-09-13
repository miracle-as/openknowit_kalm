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
    bearer = "Bearer " + os.environ.get("KALM_DNS_TOKEN", "")
    headers = {
    "Authorization": bearer,
    "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        if response.json()["result"]["status"] == "active":
            return True
    else:
        return False

def list_dns():
    domain = os.environ.get("KALM_DNS_DOMAIN")
    myenv = getenv()
    #  --url https://api.cloudflare.com/client/v4/zones/zone_identifier/dns_records \
    url = os.environ.get("KALM_DNS_URL") + "/client/v4/zones/" + os.environ.get("KALM_DNS_ZONEID") + "/dns_records"
    bearer = "Bearer " + os.environ.get("KALM_DNS_TOKEN", "")
    headers = {
    "Authorization": bearer,
    "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    records = {}
    if response.status_code == 200:
        for record in response.json()["result"]:
          records[record["name"]] = record["id"]
    else:
        print("Error: " + str(response.status_code))
        exit(1)
    return records

def delete_record(id):
    myenv = getenv()
    url = os.environ.get("KALM_DNS_URL") + "/client/v4/zones/" + os.environ.get("KALM_DNS_ZONEID") + "/dns_records/" + id 
    bearer = "Bearer " + os.environ.get("KALM_DNS_TOKEN", "")
    headers = {
    "Authorization": bearer,
    "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        print("DNS record delete failed")
        return False
    






def add_record(myitem = None):
    prettyllog("manage", "network", "DNS", "new", "000", "add record")
    myenv = getenv()
    records = list_dns()
    prettyllog("manage", "network", "DNS", "new", "000", "list dns records : " + str(len(records))) 
    if os.environ.get("KALM_DNS_RECORD_NAME") == None:
        recordname = myitem["name"]
    else:
        recordname = os.environ.get("KALM_DNS_RECORD_NAME")

    if os.environ.get("KALM_DNS_DOMAIN") == None:
        domain = myitem["domain"]
    else:
        domain = os.environ.get("KALM_DNS_DOMAIN")
    
    if os.environ.get("KALM_DNS_RECORD_TYPE") == None:
        recordtype = myitem["type"]
    else:
        recordtype = os.environ.get("KALM_DNS_RECORD_TYPE")

    if os.environ.get("KALM_DNS_RECORD_TTL") == None:
        recordttl = myitem["ttl"]
    else:
        recordttl = os.environ.get("KALM_DNS_RECORD_TTL")

    if os.environ.get("KALM_DNS_RECORD_PROXIED") == None:
        recordproxied = myitem["proxied"]
    else:
        recordproxied = os.environ.get("KALM_DNS_RECORD_PROXIED")

    

    key = recordname + "." + domain   
    prettyllog("manage", "network", "DNS", "new", "000", "check if record exists : " + key)
    try:
      value =records[key]
    except:
        value = None
    if value != None:
        delete_record(records[key])
    prettyllog("manage", "network", "DNS", "new", "000", "adding : " + key)
    url = os.environ.get("KALM_DNS_URL") + "/client/v4/zones/" + os.environ.get("KALM_DNS_ZONEID") + "/dns_records"
    bearer = "Bearer " + os.environ.get("KALM_DNS_TOKEN", "")
    headers = {
    "Authorization": bearer,
    "Content-Type": "application/json"
    }
    proxied = False
    if os.environ.get("KALM_DNS_RECORD_PROXIED") == "true":
        proxied = True
    if os.environ.get("KALM_DNS_CONTENT") == None:
        content = myitem["ipaddress"]
    else:
        content = os.environ.get("KALM_DNS_CONTENT")

    data = {
    "content": content, 
    "name": key,
    "proxied": proxied,
    "type": recordtype,
    "comment": "DNS record created by KALM",
    "ttl": recordttl
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return True
    else:
        return False
    






