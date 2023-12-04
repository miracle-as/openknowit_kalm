import requests
import json
import os
import base64
import xml.etree.ElementTree as ET
import platform
import pprint
import yaml
from ..common import prettyllog


def get_orgs(env):
    orgs = {}
    url = env['KALM_NETBOX_URL'] + "/api/tenancy/organizations/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN']}
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        for org in data['results']:
            orgs[org['name']] = org['id']
    else:
        prettyllog("netbox", "get", "orgs", "error", r.status_code , "unable to get orgs", severity="ERROR")
    return orgs



def create_tenant_group(tenant_group_name, env):
    url = env['KALM_NETBOX_URL'] + "/api/tenancy/tenant-groups/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    data = {
        "name": tenant_group_name,
        #strip all wovel characters and replace spaces with -
        "slug": tenant_group_name.lower().replace(" ", "-"),
        "description": "Created by KALM"
    }
    r = requests.post(url, headers=headers, json=data, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 201:
        data = r.json()
        prettyllog("netbox", "create", "tenant_group", tenant_group_name, r.status_code , "tenant_group created", severity="CHANGE")
        return data['id']
    else:
        if r.status_code == 400:
            prettyllog("netbox", "create", "tenant_group", tenant_group_name, r.status_code , "tenant_group already exists", severity="INFO")
            return True
        prettyllog("netbox", "create", "tenant_group", tenant_group_name, r.status_code , "unable to create tenant_group", severity="ERROR")
        return False
    
def get_tenant_group_id(tenant_group_name, env):
    tenant_groups = get_tenant_groups(env)
    try: 
        return tenant_groups[tenant_group_name]
    except:
        return False
    
def get_tenant_groups(env):
    tenant_groups = {}
    url = env['KALM_NETBOX_URL'] + "/api/tenancy/tenant-groups/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN']}
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        for tenant_group in data['results']:
            tenant_groups[tenant_group['name']] = tenant_group['id']
    else:
        prettyllog("netbox", "get", "tenant_groups", "error", r.status_code , "unable to get tenant_groups", severity="ERROR")
    return tenant_groups

def create_tenant(tenant_name, tenant_group, env):
    tenant_group_id = get_tenant_group_id(tenant_group, env)
    url = env['KALM_NETBOX_URL'] + "/api/tenancy/tenants/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    data = {
        "name": tenant_name,
        "slug": tenant_name.lower(),
        "group": tenant_group_id,
        "description": "Created by KALM"
    }
    r = requests.post(url, headers=headers, json=data, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 201:
        data = r.json()
        return data['id']
    else:
        if r.status_code == 400:
            prettyllog("netbox", "create", "tenant", tenant_name, r.status_code , "tenant already exists", severity="INFO")
            return True
        prettyllog("netbox", "create", "tenant", tenant_name, r.status_code , "unable to create tenant", severity="ERROR")
        return False
    
def get_tenant_id(tenant_name, env):
    tenants = get_tenants(env)
    try: 
        return tenants[tenant_name]
    except:
        return False
    
def get_tenants(env):
    tenants = {}
    url = env['KALM_NETBOX_URL'] + "/api/tenancy/tenants/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN']}
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        for tenant in data['results']:
            tenants[tenant['name']] = tenant['id']
    else:
        prettyllog("netbox", "get", "tenants", "error", r.status_code , "unable to get tenants", severity="ERROR")
    return tenants

def create_sitegroups(sitegroup_name, env):
    url = env['KALM_NETBOX_URL'] + "/api/dcim/site-groups/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
               'Content-Type': 'application/json'
            }
    data = {
        "name": sitegroup_name,
        "slug": sitegroup_name.lower().replace(" ", "-"),
        "description": "Created by KALM"
    }
    r = requests.post(url, headers=headers, json=data, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 201:
        data = r.json()
        return data['id']
    else:
        if r.status_code == 400:
            prettyllog("netbox", "create", "sitegroup", sitegroup_name, r.status_code , "sitegroup already exists", severity="INFO")
            return True

        prettyllog("netbox", "create", "sitegroup", sitegroup_name, r.status_code , "unable to create sitegroup", severity="ERROR")
        return False
    
def get_sitegroup_id(sitegroup_name, env):
    sitegroups = get_sitegroups(env)
    try: 
        return sitegroups[sitegroup_name]
    except:
        return False
    
def get_sitegroups(env):
    sitegroups = {}
    url = env['KALM_NETBOX_URL'] + "/api/dcim/site-groups/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN']}
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        for sitegroup in data['results']:
            sitegroups[sitegroup['name']] = sitegroup['id']
    else:
        prettyllog("netbox", "get", "sitegroups", "error", r.status_code , "unable to get sitegroups", severity="ERROR")
    return sitegroups

def create_site(site_name, region, sitegroup, tenant, env):
    sitegroup_id = get_sitegroup_id(sitegroup, env)
    region_id = get_region_id(region, env)
    tenant_id = get_tenant_id(tenant, env)

    url = env['KALM_NETBOX_URL'] + "/api/dcim/sites/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
               'Content-Type': 'application/json'
            }
    data = {
        "name": site_name,
        "slug": site_name.lower().replace(" ", "-"),
        "region": region_id,
        "group": sitegroup_id,
        "tenant": tenant_id,
        "description": "Created by KALM"
    }
    r = requests.post(url, headers=headers, json=data, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 201:
        data = r.json()
        return data['id']
    else:
        if r.status_code == 400:
            prettyllog("netbox", "create", "site", site_name, r.status_code , "site already exists", severity="INFO")
            return True

        prettyllog("netbox", "create", "site", site_name, r.status_code , "unable to create site", severity="ERROR")
        return False
    
def get_site_id(site_name, env):
    sites = get_sites(env)
    try: 
        return sites[site_name]
    except:
        return False
    
def get_sites(env):
    sites = {}
    url = env['KALM_NETBOX_URL'] + "/api/dcim/sites/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN']}
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        for site in data['results']:
            sites[site['name']] = site['id']
    else:
        prettyllog("netbox", "get", "sites", "error", r.status_code , "unable to get sites", severity="ERROR")
    return sites


def create_region(region_name, env):
    url = env['KALM_NETBOX_URL'] + "/api/dcim/regions/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
               'Content-Type': 'application/json'
            }
    data = {
        "name": region_name,
        "slug": region_name.lower().replace(" ", "-"),
        "description": "Created by KALM"
    }
    r = requests.post(url, headers=headers, json=data, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 201:
        data = r.json()
        return data['id']
    else:
        if r.status_code == 400:
            prettyllog("netbox", "create", "region", region_name, r.status_code , "region already exists", severity="INFO")
            return True
        prettyllog("netbox", "create", "region", region_name, r.status_code , "unable to create region", severity="ERROR")
        return False
    
def get_region_id(region_name, env):
    regions = get_regions(env)
    try: 
        return regions[region_name]
    except:
        return False
    
def get_regions(env):
    regions = {}
    url = env['KALM_NETBOX_URL'] + "/api/dcim/regions/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN']}
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        for region in data['results']:
            regions[region['name']] = region['id']
    else:
        prettyllog("netbox", "get", "regions", "error", r.status_code , "unable to get regions", severity="ERROR")
    return regions

def read_etc_json():
    try:
        with open('etc/kalm/netbox.json') as f:
            data = json.load(f)
        return data
    except:
        return False
    

def refresh_netbox_orgs(env):
    netboxdata = read_etc_json()
    """
    this is the data structure we are looking for

    {'name': 'Aarhus Universitetshospital',
     'organisation': 'Region Midtjylland',
     'sites': [{'address': 'Palle Juul-Jensens Boulevard 99, 8200 Aarhus N',
            'description': 'Aarhus Universitetshospital',
            'name': 'Aarhus Universitetshospital',
            'region': 'Region Midtjylland',
            'slug': 'auh',
            'stastus': 'Active'}]}

    """
    create_tenant_group(netboxdata['organization'], env)
    create_tenant(netboxdata['name'], netboxdata['organization'], env)
    for site in netboxdata['sites']:
        create_region(site['region'], env)
        create_sitegroups("Kalm", env)
        create_site(site['name'], site['region'], "Kalm", netboxdata['name'], env)
    return netboxdata


    # create tenant groups
    # we need a group for the organisation


