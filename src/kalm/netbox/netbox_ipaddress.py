import pprint
from ..common import prettyllog
import requests
from .organization import get_site_id
from .organization import get_tenant_id
import json
import pprint
import time


def create_ip_address_role(name, env):
    prettyllog("netbox", "create", "ip address role", name, "000" , "creating ip address role", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/ipam/roles/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    payload = {
        "name": name,
        "slug": name,
        "weight": 100
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload), verify=env['KALM_NETBOX_SSL'])
    pprint.pprint(r.content)
    if r.status_code == 201:
        prettyllog("netbox", "create", "ip address role", name, r.status_code , "ip address role created", severity="INFO")
        return True
    else:
        if r.status_code == 400:
            prettyllog("netbox", "create", "ip address role", name, r.status_code , "ip address role already exists", severity="INFO")
            return True
        prettyllog("netbox", "create", "ip address role", name, r.status_code , "unable to create ip address role", severity="ERROR")
        return False
    
def  get_ip_address_role_id(name, env):
    prettyllog("netbox", "get", "ip address role", name, "000" , "getting ip address role", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/ipam/roles/?name=" + name
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        if len(data['results']) == 1:
            prettyllog("netbox", "get", "ip address role", name, r.status_code , "ip address role found", severity="INFO")
            return data['results'][0]['id']
        else:
            prettyllog("netbox", "get", "ip address role", name, r.status_code , "ip address role not found", severity="INFO")
            return False
    else:
        prettyllog("netbox", "get", "ip address role", name, r.status_code , "unable to get ip address role", severity="ERROR")
        return False

def create_ip_address_status(name, env):
    prettyllog("netbox", "create", "ip address status", name, "000" , "creating ip address status", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/ipam/statuses/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    payload = {
        "name": name,
        "slug": name,
        "color": "ff0000"
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload), verify=env['KALM_NETBOX_SSL'])
    pprint.pprint(r.content)
    if r.status_code == 201:
        prettyllog("netbox", "create", "ip address status", name, r.status_code , "ip address status created", severity="INFO")
        return True
    else:
        if r.status_code == 400:
            prettyllog("netbox", "create", "ip address status", name, r.status_code , "ip address status already exists", severity="INFO")
            return True
        prettyllog("netbox", "create", "ip address status", name, r.status_code , "unable to create ip address status", severity="ERROR")
        return False
    
def get_ip_address_status_id(name, env):
    prettyllog("netbox", "get", "ip address status", name, "000" , "getting ip address status", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/ipam/statuses/?name=" + name
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        if len(data['results']) == 1:
            prettyllog("netbox", "get", "ip address status", name, r.status_code , "ip address status found", severity="INFO")
            return data['results'][0]['id']
        else:
            prettyllog("netbox", "get", "ip address status", name, r.status_code , "ip address status not found", severity="INFO")
            return False
    else:
        prettyllog("netbox", "get", "ip address status", name, r.status_code , "unable to get ip address status", severity="ERROR")
        return False
    

def get_ip_address_id(ip, env):
    if ip == "" or ip == None:
        return False
    prettyllog("netbox", "get", "ip address", ip, "000" , "getting ip address", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/ipam/ip-addresses/?address=" + ip
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        if len(data['results']) == 1:
            prettyllog("netbox", "get", "ip address", ip, r.status_code , "ip address found", severity="INFO")
            return data['results'][0]['id']
        else:
            prettyllog("netbox", "get", "ip address", ip, r.status_code , "ip address not found", severity="INFO")
            return False
    else:
        prettyllog("netbox", "get", "ip address", ip, r.status_code , "unable to get ip address", severity="ERROR")
        return False

def create_ip_address(ip, env, netboxdata):
    if ip == "" or ip == None:
        return False
    prettyllog("netbox", "create", "ip address", ip, "000" , "creating ip address", severity="INFO")
    tenant = netboxdata['name']
    tenantid = get_tenant_id(tenant,env)
    url = env['KALM_NETBOX_URL'] + "/api/ipam/ip-addresses/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    payload = {
        "address": ip,
        "tenant": tenantid,
        "dns_name": ip,
        "description": ip,
        "nat_inside": None,
        "nat_outside": None,
        "interface": None,
        "vrf": None,
        "tags": []
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload), verify=env['KALM_NETBOX_SSL'])
    pprint.pprint(r.content.decode("utf-8"))
    if r.status_code == 201:
        prettyllog("netbox", "create", "ip address", ip, r.status_code , "ip address created", severity="INFO")
        return True
    else:
        if r.status_code == 400:
            prettyllog("netbox", "create", "ip address", ip, r.status_code , "ip address already exists", severity="INFO")
            return True
        prettyllog("netbox", "create", "ip address", ip, r.status_code , "unable to create ip address", severity="ERROR")
        return False
    
def remove_ip_address(ip, env):
    prettyllog("netbox", "delete", "ip address", ip, "000" , "deleting ip address", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/ipam/ip-addresses/" + str(ip) + "/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    r = requests.delete(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 204:
        prettyllog("netbox", "delete", "ip address", ip, r.status_code , "ip address deleted", severity="INFO")
        return True
    else:
        prettyllog("netbox", "delete", "ip address", ip, r.status_code , "unable to delete ip address", severity="ERROR")
        return False
    

    


def create_ip_network(cidr, env):
    prettyllog("netbox", "create", "ip network", cidr, "000" , "creating ip network", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/ipam/prefixes/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    payload = {
        "prefix": cidr,
        "status": 1,
        "role": 1,
        "site": get_site_id(env),
        "tenant": 1
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload), verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 201:
        prettyllog("netbox", "create", "ip network", cidr, r.status_code , "ip network created", severity="INFO")
        return True
    else:
        prettyllog("netbox", "create", "ip network", cidr, r.status_code , "unable to create ip network", severity="ERROR")
        return False

def get_ip_network_id(cidr, env):
    prettyllog("netbox", "get", "ip network id", cidr, "000" , "getting ip network id", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/ipam/prefixes/?prefix=" + cidr
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        if len(data['results']) == 1:
            prettyllog("netbox", "get", "ip network id", cidr, r.status_code , "ip network id found", severity="INFO")
            return data['results'][0]['id']
        else:
            prettyllog("netbox", "get", "ip network id", cidr, r.status_code , "ip network id not found", severity="INFO")
            return False
    else:
        prettyllog("netbox", "get", "ip network id", cidr, r.status_code , "unable to get ip network id", severity="ERROR")
        return False
    