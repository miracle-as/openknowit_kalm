import requests
import json
import os
import base64
import xml.etree.ElementTree as ET
import platform
import pprint
import yaml
from ..common import prettyllog
from .organization import get_site_id



def get_cluster_group_id(name, env):
    prettyllog("netbox", "get", "cluster group", name, "000" , "getting cluster group", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/cluster-groups/?name=" + name
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        if len(data['results']) == 1:
            prettyllog("netbox", "get", "cluster group", name, r.status_code , "cluster group found", severity="INFO")
            return data['results'][0]['id']
        else:
            prettyllog("netbox", "get", "cluster group", name, r.status_code , "cluster group not found", severity="INFO")
            return False
    else:
        prettyllog("netbox", "get", "cluster group", name, r.status_code , "unable to get cluster group", severity="ERROR")
        return False

def create_cluster_group(name, env):
    prettyllog("netbox", "create", "cluster group", name, "000" , "creating cluster group", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/cluster-groups/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    payload = {
        "name": name,
        "slug": name,
        "comments": "Created by KALM"
    }
    r = requests.post(url, headers=headers, json=payload, verify=env['KALM_NETBOX_SSL'])
    pprint.pprint(r.content)
    if r.status_code == 201:
        data = r.json()
        prettyllog("netbox", "create", "cluster group", name, r.status_code , "cluster group created", severity="INFO")
        return data['id']
    else:
        prettyllog("netbox", "create", "cluster group", name, r.status_code , "u2nable to create cluster group", severity="ERROR")
        return False
    
def get_clusters(env):
    clusters = {}
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/clusters/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
               'Content-Type': 'application/json'
            }
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        for cluster in data['results']:
            clusters[cluster['name']] = cluster['id']
    else:
        prettyllog("netbox", "get", "clusters", "error", r.status_code , "unable to get clusters", severity="ERROR")
    return clusters

def get_cluster_id(cluster_name, env):
    clusters = get_clusters(env)
    try: 
        return clusters[cluster_name]
    except:
        return False

def get_cluster_type_id(cluster_type, env, netboxdata):
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/cluster-types/?name=" + cluster_type
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
               'Content-Type': 'application/json'
            }
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        if len(data['results']) == 1:
            return data['results'][0]['id']
        else:
            return False
    else:
        prettyllog("netbox", "get", "cluster type", cluster_type, r.status_code , "unable to get cluster type", severity="ERROR")
        return False
    

def create_cluster_type(cluster_type, env, netboxdata):
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/cluster-types/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
               'Content-Type': 'application/json'
            }
    payload = {
        "name": cluster_type,
        "slug": cluster_type.lower().replace(" ", "-"),
        "comments": "Created by KALM"
    }
    r = requests.post(url, headers=headers, json=payload, verify=env['KALM_NETBOX_SSL'])
    pprint.pprint(r.content)
    if r.status_code == 201:
        data = r.json()
        return data['id']
    else:
        if r.status_code == 400:
            return True
        prettyllog("netbox", "create", "cluster type", cluster_type, r.status_code , "unable to create cluster type", severity="ERROR")
        return False
    
    


    
def create_cluster(cluster_name, clustergroup, env, netboxdata):
    prettyllog("netbox", "create", "cluster", cluster_name, "000" , "creating cluster step 1", severity="INFO")
    if not get_cluster_group_id(clustergroup, env):
        create_cluster_group(clustergroup, env)
    clustergroup_id = get_cluster_group_id(clustergroup, env)
    clustertype = "VMware vCenter"
    if not get_cluster_type_id(clustertype, env, netboxdata):
        create_cluster_type(clustertype, env, netboxdata)
    clustertype_id = get_cluster_type_id(clustertype, env, netboxdata)

    if not clustergroup_id:
        prettyllog("netbox", "create", "cluster", cluster_name, "000" , "unable to create cluster group", severity="ERROR")
        return False

    cluster_id = get_cluster_id(cluster_name, env)  
    if cluster_id:
        prettyllog("netbox", "create", "cluster", cluster_name, "000" , "cluster already exists", severity="INFO")
        return True
    prettyllog("netbox", "create", "cluster", cluster_name, "000" , "creating cluster step 2", severity="INFO")
    siteid = get_site_id(netboxdata['sites'][0]['name'], env)
    prettyllog("netbox", "create", "cluster", siteid, "000" , "creating cluster must relate to this site id", severity="INFO")


    url = env['KALM_NETBOX_URL'] + "/api/virtualization/clusters/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
    data = {
        "name": cluster_name,
        "type": clustertype_id,
        "group": clustergroup_id,
        "site": siteid,
        "comments": "Created by KALM"
    }
    r = requests.post(url, headers=headers, json=data, verify=env['KALM_NETBOX_SSL'])
    pprint.pprint(r.content)
    if r.status_code == 201:
        data = r.json()
        return data['id']
    else:
        if r.status_code == 400:
            prettyllog("netbox", "create", "cluster", cluster_name, r.status_code , "cluster already exists", severity="INFO")
            return True
        prettyllog("netbox", "create", "cluster", cluster_name, r.status_code , "u1nable to create cluster 1", severity="ERROR")
        return False

def update_cluster(cluster_name, cluster_type, group, site, env, netboxdata):
    cluster_id = get_cluster_id(cluster_name, env)
    siteid = get_site_id(netboxdata['name'], env)
    clustergroup_id = get_cluster_group_id(clustergroup, env)
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/clusters/" + str(cluster_id) + "/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
                'Content-Type': 'application/json'
            }    
    data = {
        "name": cluster_name,
        "type": 1,
        "group": clustergroup_id,
        "site": siteid,
        "comments": "Updated by KALM"
    }
    r = requests.put(url, headers=headers, data=data, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        return data['id']
    else:
        prettyllog("netbox", "update", "cluster", cluster_name, r.status_code , "unable to update cluster", severity="ERROR")
        return False