#!/usr/bin/env python

import requests
import json
import os

# NetBox API configuration
NETBOX_URL = os.getenv("NETBOX_API_URL")
NETBOX_TOKEN = os.getenv("NETBOX_API_TOKEN")



def get_clusters():
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json",
    }
    response = requests.get(f"{NETBOX_URL}/virtualization/clusters/", headers=headers)
    clusters = response.json()
    return clusters["results"]

def get_virtual_machines():
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json",
    }
    response = requests.get(f"{NETBOX_URL}/virtualization/virtual-machines/", headers=headers)
    vms = response.json()
    return vms["results"]

def main():
    clusters = get_clusters()
    vms = get_virtual_machines()

    vm_data = []
    for vm in vms:
        vm_entry = {
            "name": vm["name"],
            "cluster": vm["cluster"]["name"] if vm.get("cluster") else "N/A",
            "disk_gb": vm["disk"],
            "cpu": vm["vcpus"],
            "memory_mb": vm["memory"]
        }
        vm_data.append(vm_entry)

    data = {
        "clusters": [cluster["name"] for cluster in clusters],
        "virtual_machines": vm_data
    }

    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
