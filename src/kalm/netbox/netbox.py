import requests
import json
import os
import base64
import xml.etree.ElementTree as ET
import yaml

netbox_url = os.environ.get('NETBOX_URL')
netbox_token = os.environ.get('NETBOX_TOKEN')

NETBOX_URL = os.getenv("NETBOX_API_URL")
NETBOX_TOKEN = os.getenv("NETBOX_API_TOKEN")

ssh_config_template = """
Host {hostname}
    HostName {full_hostname}
    User root
    IdentityFile ~/.ssh/disposeablekey
    IdentityFile ~/.ssh/disposeablekey.signed
    Port 22
    {proxy_jump}
"""
def vizulize(args):
    cluseters = get_clusters()
    vms = get_virtual_machines()
    print("digraph G {")
    for cluster in cluseters:
        print(f"    {cluster['name']}")
    for vm in vms:
        print(f"    {vm['name']}")
        if vm.get("cluster"):
            print(f"    {vm['name']} -> {vm['cluster']['name']}")
    print("}")


def add_vm():
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"

    }
    try:
        vmname = os.environ.get('KALM_VM_NAME')
        if vmname == None:
            raise Exception("No VM name provided (KALM_VM_NAME)")
        print(vmname)
    except:

        print("No VM name provided (KALM_VM_NAME)")
        return False
    try:
        vmcluster = os.environ.get('KALM_VM_CLUSTER')
        if vmcluster == None:
            raise Exception("No VM cluster provided (KALM_VM_CLUSTER)")
        print(vmcluster)
    except:
        print("No VM cluster provided (KALM_VM_CLUSTER)")
        return False
    try: 
        vmdisk = os.environ.get('KALM_VM_DISK')
        if vmdisk == None:
            vmdisk = 0
        print(vmdisk)
    except:
        print("No VM disk provided (KALM_VM_DISK)")
        return False
    try:
        vmcpus = os.environ.get('KALM_VM_CPU')
        if vmcpus == None:
            vmcpus = 0
        print(vmcpus)
    except:
        print("No VM cpu provided (KALM_VM_CPU)")
        return False
    try:
        vmmemory = os.environ.get('KALM_VM_MEMORY')
        if vmmemory == None:
            vmmemory = 0

        print(vmmemory)
    except:
        print("No VM memory provided (KALM_VM_MEMORY)")
        return False
    try:
        vmip = os.environ.get('KALM_VM_IP') 
        print(vmip)
    except:
        print("No VM IP provided (KALM_VM_IP)")
        return False
    data = {
  "name": "string",
  "status": "offline",
  "site": 0,
  "cluster": 0,
  "device": 0,
  "role": 0,
  "tenant": 0,
  "platform": 0,
  "primary_ip4": 0,
  "primary_ip6": 0,
  "vcpus": 9999,
  "memory": 2147483647,
  "disk": 2147483647,
  "description": "string",
  "comments": "string",
  "local_context_data": {
    "additionalProp1": "string",
    "additionalProp2": "string",
    "additionalProp3": "string"
  },
  "tags": [
    {
      "name": "string",
      "slug": "Hvxpc-MwFr9e_yu-JwWyS7KSZSF",
      "color": "3c53c8"
    }
  ],
  "custom_fields": {
    "additionalProp1": "string",
    "additionalProp2": "string",
    "additionalProp3": "string"
  }
}

    print(data)
    print(headers)
    if os.environ.get('NETBOX_API_URL') == None:
        print("No NETBOX_API_URL provided")
        return False
    url = os.environ.get("NETBOX_API_URL") + "/virtualization/virtual-machines/"
    print(url)
    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response)
    print(response.json())
    print(response.status_code) 
    print(response.content)    
    if response.status_code == 200:
        return True
    else:
        return False


    
    

def get_clusters():
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    response = requests.get(f"{NETBOX_URL}/virtualization/clusters/", headers=headers)
    clusters = response.json()
    return clusters["results"]

def get_virtual_machines():
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    response = requests.get(f"{NETBOX_URL}/virtualization/virtual-machines/", headers=headers)
    vms = response.json()
    return vms["results"]

    
def netboxdata(args):
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
        "clusters": [cluster["name"] for cluster in clusters],
        "virtual_machines": vm_data
    }
    print(json.dumps(data, indent=2))
    return data

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


def sshconfig(args):    
    data = netboxdata(args)
    virtual_machines = data["virtual_machines"]
    ssh_config_entries = [generate_ssh_config_entry(vm) for vm in virtual_machines]
    ssh_config_content = "\n".join(ssh_config_entries)
    configdir = os.path.expanduser("~/.ssh/config") + "conf.d"
    if not os.path.exists(configdir):
        os.makedirs(configdir)
    configfile = os.path.expanduser("~/.ssh/config") + "conf.d/openstack.conf"
    open(configfile, "w").write(ssh_config_content)
    print(ssh_config_content)





def generate_ssh_config_entry(vm):
    proxy_jump = ""
    if vm["cluster"] != vm["name"]:
        proxy_jump = f"ProxyJump {vm['cluster']}"
    
    return ssh_config_template.format(
        hostname=vm["name"],
        full_hostname=vm["name"] + ".openknowit.com",
        proxy_jump=proxy_jump
    )


