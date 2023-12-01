import requests
import json
import os
import base64
import xml.etree.ElementTree as ET
import platform
import pprint
import yaml
from ..common import prettyllog

def get_clusters(env):
    clusters = {}
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/clusters/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN']}
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
    
def create_cluster(cluster_name, env):
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/clusters/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN']}
    data = {
        "name": cluster_name,
        "type": 1,
        "group": 1,
        "site": 1,
        "comments": "Created by KALM"
    }
    r = requests.post(url, headers=headers, data=data, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 201:
        data = r.json()
        return data['id']
    else:
        prettyllog("netbox", "create", "cluster", cluster_name, r.status_code , "unable to create cluster", severity="ERROR")
        return False

def update_cluster(cluster_name, cluster_type, group, site, env):
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/clusters/" + str(cluster_id) + "/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN']}
    data = {
        "name": cluster_name,
        "type": 1,
        "group": 1,
        "site": 1,
        "comments": "Updated by KALM"
    }
    r = requests.put(url, headers=headers, data=data, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        return data['id']
    else:
        prettyllog("netbox", "update", "cluster", cluster_name, r.status_code , "unable to update cluster", severity="ERROR")
        return False