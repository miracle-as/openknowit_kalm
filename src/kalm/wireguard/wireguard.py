import requests
import subprocess
import json
import os
import redis
import sys
import time 

netbox_url = os.environ.get('NETBOX_URL')
netbox_token = os.environ.get('NETBOX_TOKEN')

NETBOX_URL = os.getenv("NETBOX_API_URL")
NETBOX_TOKEN = os.getenv("NETBOX_API_TOKEN")


def am_I_virtual_machine():
    return os.path.exists("/proc/1/environ")

def get_virtual_machines():
    returnvms = {}
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/virtualization/virtual-machines/")
    response = requests.get(url, headers=headers)
    vms = response.json()
    for vm in vms["results"]:
        try:
            if returnvms[vm["name"]]:
                print("Duplicate vm name")
        except:
           returnvms[vm["name"]] = vm["id"]
    return returnvms

def get_virtual_machine(id):
    returnvm = {}
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/virtualization/virtual-machines/" + str(id))
    response = requests.get(url, headers=headers)
    vm = response.json()
    return vm    


def get_local_context_data():
    if am_I_virtual_machine():
        # we are running in a virtual machine
        # get the local context data from netbox
        vms = get_virtual_machines()
        vmdata = get_virtual_machine(vms[os.environ.get("HOSTNAME")])
        return vmdata["local_context_data"]

def ansible_inventory(args):
    clusters = get_clusters()
    vms = get_virtual_machines()

    vm_data = []
    for vm in vms:
        vm_entry = {
            "name": vm["name"],
            "cluster": vm["cluster"]["name"] if vm.get("cluster") else "N/A",
            "disk_gb": vm["disk"],
            "cpu": vm["vcpus"],
            "memory_mb": vm["memory"],
            "local_context_data": vm["local_context_data"]
        }
        vm_data.append(vm_entry)

    data = {
        "_meta": {
            "hostvars": {}
        },
        "all": {
            "children": ["clusters"]
        },
        "clusters": {
            "hosts": [cluster["name"] for cluster in clusters]
        }
    }

    for vm in vms:
        if vm.get("cluster"):
            cluster_name = vm["cluster"]["name"]
            if cluster_name not in data:
                data[cluster_name] = {"hosts": []}
            data[cluster_name]["hosts"].append(vm["name"])
            data["_meta"]["hostvars"][vm["name"]] = {
                "disk_gb": vm["disk"],
                "cpu": vm["vcpus"],
                "memory_mb": vm["memory"]
            }

    print(yaml.dump(data))



def refresh(args):
 print(get_local_context_data)

 
