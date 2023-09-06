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
def get_ip4_id(ip4_address):
    ip4s = get_ip4s()
    try:
        return ip4s[ip4_address]
    except:
        return None
    
def get_ip6_id(ip6_address):
    ip6s = get_ip6s()
    try:
        return ip6s[ip6_address]
    except:
        return None
    

def get_site_id(site_name):
    sites = get_sites()
    try:
        return sites[site_name]
    except:
        return None

def get_device_id(device_name):
    devices = get_devices()
    try:    
        return devices[device_name]
    except:
        return None

def get_role_id(role_name):
    roles = get_roles()
    try: 
        return roles[role_name]
    except:
        return None


def get_type_id(type_name):
    types = get_types()
    try:
        return types[type_name]
    except:
        if create_type(type_name):
            return types[type_name]
        return None

def get_platform_id(platform_name):
    platforms = get_platforms()
    try:
        return platforms[platform_name]
    except:
        return None

def get_tenant_id(tenant_name):
    tenants = get_tenants()
    try:
        return tenants[tenant_name]
    except:
        return None

def get_cluster_id(cluster_name):
    clusters = get_clusters()
    try: 
        return clusters[cluster_name]
    except:
        if create_cluster(cluster_name):
            return clusters[cluster_name]
        else:
            return None

def get_manufacturer_id(manufacturer_name):
    manufacturers = get_manufacturers()
    try:
        return manufacturers[manufacturer_name]
    except:
        if create_manufacturer(manufacturer_name):
            return manufacturers[manufacturer_name]
        else:
            return None
def get_virtual_machine_id(vm_name):
    vms = get_virtual_machines()
    try:
        return vms[vm_name]
    except:
        return None

def create_manufacturer(manufacturer_name):
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    manufacturer_name = os.environ.get('KALM_MANUFACTURER_NAME')
    if manufacturer_name == None:
        manufacturer_name = "default"

    manufacturer_slug = os.environ.get('KALM_MANUFACTURER_SLUG')
    if manufacturer_slug == None:
        manufacturer_name = manufacturer_name.lower()
    manufacturer_description = os.environ.get('KALM_MANUFACTURER_DESCRIPTION')
    if manufacturer_description == None:
        manufacturer_description = ""
    manufacturer_comments = os.environ.get('KALM_MANUFACTURER_COMMENTS')
    if manufacturer_comments == None:
        manufacturer_comments = ""
    manufacturer_custom_fields = os.environ.get('KALM_MANUFACTURER_CUSTOM_FIELDS')
    if manufacturer_custom_fields == None:
        manufacturer_custom_fields = {}

    data = {
        "name": manufacturer_name,
        "slug": manufacturer_name,
        "description": "",
        "comments": "",
        "custom_fields": {}
    }
    manufacturer_id = get_manufacturer_id(manufacturer_name)
    if manufacturer_id != None:
        return True

    url = fix_url("/dcim/manufacturers/")
    response = requests.post(url, headers=headers, json=data)
    print(response)
    print(response.json())
    print(response.status_code)
    print(response.content)
    if response.status_code == 200:
        return True
    else:
        return False
    


def create_device_type(device_type_name):
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    device_type_name = os.environ.get('KALM_DEVICE_TYPE_NAME')
    if device_type_name == None:
        device_type_name = "default"
    device_type_model = os.environ.get('KALM_DEVICE_TYPE_MODEL')
    if device_type_model == None:
        device_type_model = "default"
    device_type_slug = os.environ.get('KALM_DEVICE_TYPE_SLUG')
    if device_type_slug == None:
        device_type_slug = device_type_name.lower()
    device_type_description = os.environ.get('KALM_DEVICE_TYPE_DESCRIPTION')
    if device_type_description == None:
        device_type_description = ""
    device_type_comments = os.environ.get('KALM_DEVICE_TYPE_COMMENTS')
    if device_type_comments == None:
        device_type_comments = ""
    device_type_custom_fields = os.environ.get('KALM_DEVICE_TYPE_CUSTOM_FIELDS')
    if device_type_custom_fields == None:

        device_type_custom_fields = {}
    # Optional fields
    device_type_part_number = os.environ.get('KALM_DEVICE_TYPE_PART_NUMBER')
    if device_type_part_number == None:
        device_type_part_number = ""
    device_type_is_full_depth = os.environ.get('KALM_DEVICE_TYPE_IS_FULL_DEPTH')
    if device_type_is_full_depth == None:
        device_type_is_full_depth = True
    device_type_is_console_server = os.environ.get('KALM_DEVICE_TYPE_IS_CONSOLE_SERVER')
    if device_type_is_console_server == None:
        device_type_is_console_server = False
    device_type_is_pdu = os.environ.get('KALM_DEVICE_TYPE_IS_PDU')
    if device_type_is_pdu == None:
        device_type_is_pdu = False
    device_type_is_network_device = os.environ.get('KALM_DEVICE_TYPE_IS_NETWORK_DEVICE')
    if device_type_is_network_device == None:
        device_type_is_network_device = False
    device_type_subdevice_role = os.environ.get('KALM_DEVICE_TYPE_SUBDEVICE_ROLE')
    if device_type_subdevice_role == None:
        device_type_subdevice_role = None
    device_type_interface_ordering = os.environ.get('KALM_DEVICE_TYPE_INTERFACE_ORDERING')
    if device_type_interface_ordering == None:
        device_type_interface_ordering = None
    device_type_tags = os.environ.get('KALM_DEVICE_TYPE_TAGS')
    if device_type_tags == None:
        device_type_tags = []
    device_type_manufacturer = os.environ.get('KALM_DEVICE_TYPE_MANUFACTURER')
    if device_type_manufacturer == None:
        device_type_manufacturer = "default"
    device_type_manufacturer_id = get_manufacturer_id(device_type_manufacturer)
    if device_type_manufacturer_id == None:
        create_manufacturer(device_type_manufacturer)
        device_type_manufacturer_id = get_manufacturer_id(device_type_manufacturer)
    device_type_height = os.environ.get('KALM_DEVICE_TYPE_HEIGHT')
    if device_type_height == None:
        device_type_height = 1

    data = {
        "name": device_type_name,
        "model": device_type_model,
        "manufacturer": device_type_manufacturer_id,
        "slug": device_type_slug,
        "u_height": device_type_height,
        "is_full_depth": device_type_is_full_depth,
        "is_console_server": device_type_is_console_server,
        "is_pdu": device_type_is_pdu,
        "is_network_device": device_type_is_network_device,
        "subdevice_role": device_type_subdevice_role,
        "interface_ordering": device_type_interface_ordering,
        "comments": device_type_comments,
        "tags": device_type_tags,
        "custom_fields": device_type_custom_fields
    }
    device_type_id = get_type_id(device_type_name)
    if device_type_id != None:
        return True
    url = fix_url("/dcim/device-types/")
    response = requests.post(url, headers=headers, json=data)
    print(response)
    print(response.json())
    print(response.status_code)
    print(response.content)
    if response.status_code == 200:
        return True
    else:
        return False
    


def create_site(site_name):
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    site_name = os.environ.get('KALM_SITE_NAME')
    if site_name == None:
        site_name = "default"
    site_slug = os.environ.get('KALM_SITE_SLUG')
    if site_slug == None:
        site_slug = site_name.lower()
    site_description = os.environ.get('KALM_SITE_DESCRIPTION')
    if site_description == None:
        site_description = ""
    site_comments = os.environ.get('KALM_SITE_COMMENTS')
    if site_comments == None:
        site_comments = ""
    site_custom_fields = os.environ.get('KALM_SITE_CUSTOM_FIELDS')
    if site_custom_fields == None:
        site_custom_fields = {}

    data = {
        "name": site_name,
        "slug": site_slug,
        "description": site_description,
        "comments": site_comments,
        "custom_fields": site_custom_fields
    }   
    site_id = get_site_id(site_name)
    if site_id != None:
        return True
    url = fix_url("/dcim/sites/")
    response = requests.post(url, headers=headers, json=data)
    print(response)
    print(response.json())
    print(response.status_code)
    print(response.content)
    if response.status_code == 200:
        return True
    else:
        return False



def create_manufacturer(manufacturer_name):
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    manufacturer_name = os.environ.get('KALM_MANUFACTURER_NAME')
    if manufacturer_name == None:
        manufacturer_name = "default"

    manufacturer_slug = os.environ.get('KALM_MANUFACTURER_SLUG')
    if manufacturer_slug == None:
        manufacturer_name = manufacturer_name.lower()
    manufacturer_description = os.environ.get('KALM_MANUFACTURER_DESCRIPTION')
    if manufacturer_description == None:
        manufacturer_description = ""
    manufacturer_comments = os.environ.get('KALM_MANUFACTURER_COMMENTS')
    if manufacturer_comments == None:
        manufacturer_comments = ""
    manufacturer_custom_fields = os.environ.get('KALM_MANUFACTURER_CUSTOM_FIELDS')
    if manufacturer_custom_fields == None:
        manufacturer_custom_fields = {}

    data = {
        "name": manufacturer_name,
        "slug": manufacturer_name,
        "description": "",
        "comments": "",
        "custom_fields": {}
    }
    manufacturer_id = get_manufacturer_id(manufacturer_name)
    if manufacturer_id != None:
        return True
    
    url = fix_url("/dcim/manufacturers/")
    response = requests.post(url, headers=headers, json=data)
    print(response)
    print(response.json())
    print(response.status_code)
    print(response.content)
    if response.status_code == 200:
        return True
    else:
        return False



def create_type(type_name):
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields

    data = {
        "name": type_name, 
        "model": type_name,
        "manufacturer": 1,
        "slug": type_name,
        "u_height": 1,
        "is_full_depth": True,
        "is_console_server": False,
        "is_pdu": False,
        "is_network_device": False,
        "subdevice_role": None,
        "interface_ordering": None,
        "comments": "",
        "tags": [],
        "custom_fields": {}
    }

    url = fix_url("/dcim/device-types/")
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return True
    else:
        return False
    

def create_cluster(cluster_name):
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    vmtype = os.environ.get('KALM_VM_TYPE')
    if vmtype == None:
        vmtype = "default"
    typeid = get_type_id(vmtype)

    data = {
        "name": cluster_name,
        "type": typeid
    }

    url = fix_url("/virtualization/clusters/")
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return True
    else:
        return False
    
def create_tenant(tenant_name):

    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    tenant_name = os.environ.get('KALM_TENANT_NAME')
    if tenant_name == None:
        tenant_name = "default"
    tenant_slug = os.environ.get('KALM_TENANT_SLUG')
    if tenant_slug == None:
        tenant_slug = tenant_name.lower()
    tenant_description = os.environ.get('KALM_TENANT_DESCRIPTION')
    if tenant_description == None:
        tenant_description = ""
    tenant_comments = os.environ.get('KALM_TENANT_COMMENTS')
    if tenant_comments == None:
        tenant_comments = ""
    tenant_custom_fields = os.environ.get('KALM_TENANT_CUSTOM_FIELDS')
    if tenant_custom_fields == None:
        tenant_custom_fields = {}
        
    data = {
        "name": tenant_name,
        "slug": tenant_slug,
        "description": tenant_description,
        "comments": tenant_comments,
        "custom_fields": tenant_custom_fields
    }
    tenant_id = get_tenant_id(tenant_name)
    if tenant_id != None:
        return True
    url = fix_url("/tenancy/tenants/")
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return True
    else:
        return False
    
    



def add_vm():
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    vmname = os.environ.get('KALM_VM_NAME')
    if vmname == None:
        vmname = os.environ.get('HOSTNAME')
    if vmname == None:  
        raise Exception("No VM name provided (KALM_VM_NAME)")
    vmcluster = os.environ.get('KALM_VM_CLUSTER')
    if vmcluster == None:
        raise Exception("No VM cluster provided (KALM_VM_CLUSTER)")
    # Optional fields
    vmsite = os.environ.get('KALM_VM_SITE')
    if vmsite == None:
        vmsite = "default"
    vmrole = os.environ.get('KALM_VM_ROLE')
    if vmrole == None:
        vmrole = "default"
    vmtype = os.environ.get('KALM_VM_TYPE')
    if vmtype == None:
        vmtype = "default"
    vmplatform = os.environ.get('KALM_VM_PLATFORM')
    if vmplatform == None:
        vmplatform = "default"
    vmtentant = os.environ.get('KALM_VM_TENANT')
    if vmtentant == None:
        vmtentant = "default"
    vmdevice = os.environ.get('KALM_VM_DEVICE')
    if vmdevice == None:
        vmdevice = "default"
    vmstatus = os.environ.get('KALM_VM_STATUS')
    if vmstatus == None:
        vmstatus = "active"
    vmdisk = os.environ.get('KALM_VM_DISK')
    if vmdisk == None:
        vmdisk = 1
    vmcpus = os.environ.get('KALM_VM_CPU')
    if vmcpus == None:
        vmcpus = 1
    vmmemory = os.environ.get('KALM_VM_MEMORY')
    if vmmemory == None:
        vmmemory = 1
    vmip = os.environ.get('KALM_VM_IP') 
    if vmip == None:
        vmip = ""
    vmip6 = os.environ.get('KALM_VM_IP6') 
    if vmip6 == None:
        vmip6 = ""
    vmdescription = os.environ.get('KALM_VM_DESCRIPTION')
    if vmdescription == None:
        vmdescription = ""

    vmcomments = os.environ.get('KALM_VM_COMMENTS')
    if vmcomments == None:
        vmcomments = ""

    vmlocal_context_data = os.environ.get('KALM_VM_LOCAL_CONTEXT_DATA')
    if vmlocal_context_data == None:
        vmlocal_context_data = {}
    
    vmtags = os.environ.get('KALM_VM_TAGS')
    if vmtags == None:
        vmtags = []
    vmcustom_fields = os.environ.get('KALM_VM_CUSTOM_FIELDS')
    if vmcustom_fields == None:
        vmcustom_fields = {}




    # Get the IDs from Netbox
    
    cluster_id = get_cluster_id(vmcluster)
    site_id = get_site_id(vmsite)
    device_id = get_device_id(vmdevice)
    role_id = get_role_id(vmrole)
    type_id = get_type_id(vmtype)
    platform_id = get_platform_id(vmplatform)
    tenant_id = get_tenant_id(vmtentant)
    ip4_id = get_ip4_id(vmip)
    ip6_id = get_ip6_id(vmip6)


    data = {
            "name": vmname, 
            "status": vmstatus,
            "site": site_id,
            "cluster": cluster_id,
            "device": device_id,
            "role": role_id,
            "tenant": tenant_id,
            "platform": platform_id,
            "primary_ip4": ip4_id,     
            "primary_ip6": ip6_id,  
            "vcpus": vmcpus,
            "memory":    vmmemory,
            "disk": vmdisk,
            "description": vmdescription,
            "comments": vmcomments,
            "local_context_data": vmlocal_context_data,
            "tags": vmtags,
            "custom_fields": vmcustom_fields
        }
    if os.environ.get('NETBOX_API_URL') == None:
        print("No NETBOX_API_URL provided")
        return False
    if os.environ.get('NETBOX_API_TOKEN') == None:
        print("No NETBOX_API_TOKEN provided")
        return False
    nburl=os.environ.get('NETBOX_API_URL')
    if nburl.endswith("/"):
        nburl = nburl[:-1]
    if not nburl.endswith("/api"):
        nburl = nburl + "/api"
    vmid = get_virtual_machine_id(vmname)
    if vmid != None:
        return True
    
    url = nburl + "/virtualization/virtual-machines/"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return True
    else:
        return False

def fix_url(apiurl):
    nburl=os.environ.get('NETBOX_API_URL')
    if nburl.endswith("/"):
        nburl = nburl[:-1]
    if not nburl.endswith("/api"):
        nburl = nburl + "/api"
    nburl = nburl + apiurl
    return nburl

def get_tenants():
    returntenants = {}

    # https://netbox.openknowit.com/api/tenancy/tenants/
    # https://netbox.openknowit.com/api/tenancy/tenants/?limit=1000
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/tenancy/tenants/")
    response = requests.get(url, headers=headers)
    tenants = response.json()
    for tenant in tenants["results"]:
        try:
            if returntenants[tenant["name"]]:
                print("Duplicate tenant name")
        except:
           returntenants[tenant["name"]] = tenant["id"]
    return returntenants

def get_roles():
    returnroles = {}
    #GET /api/dcim/device-roles/35/
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/dcim/device-roles/")
    response = requests.get(url, headers=headers)
    roles = response.json()
    for role in roles["results"]:
        try:
            if returnroles[role["name"]]:
                print("Duplicate role name")
        except:
           returnroles[role["name"]] = role["id"]
    return returnroles

def get_ip4s():
    returnip4s = {}
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/ipam/ip-addresses/")
    response = requests.get(url, headers=headers)
    ip4s = response.json()
    for ip4 in ip4s["results"]:
        try:
            if returnip4s[ip4["address"]]:
                print("Duplicate ip4 address")
        except:
           returnip4s[ip4["address"]] = ip4["id"]
    return returnip4s

def get_manufacturers():
    returnmanufacturers = {}
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/dcim/manufacturers/")
    response = requests.get(url, headers=headers)
    manufacturers = response.json()
    for manufacturer in manufacturers["results"]:
        try:
            if returnmanufacturers[manufacturer["name"]]:
                print("Duplicate manufacturer name")
        except:
           returnmanufacturers[manufacturer["name"]] = manufacturer["id"]
    return returnmanufacturers



def get_ip6s():
    returnip6s = {}
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/ipam/ip-addresses/")
    response = requests.get(url, headers=headers)




def get_types():
    returntypes = {}
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/dcim/device-types/")
    response = requests.get(url, headers=headers)
    types = response.json()
    for type in types["results"]:
        try:
            if returntypes[type["name"]]:
                print("Duplicate type name")
        except:
           returntypes[type["display"]] = type["id"]
    return  returntypes

def get_platforms():
    returnplarforms = {}
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/dcim/platforms/")
    response = requests.get(url, headers=headers)
    platforms = response.json()
    for platform in platforms["results"]:
        try:
            if returnplarforms[platform["name"]]:
                print("Duplicate platform name")
        except:
           returnplarforms[platform["name"]] = platform["id"]
    return returnplarforms 

def get_devices():
    returndevices = {}

     #/api/dcim/devices/
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/dcim/devices/")
    response = requests.get(url, headers=headers)
    devices = response.json()
    for device in devices["results"]:
        try:
            if returndevices[device["name"]]:
                print("Duplicate device name")
        except:
           returndevices[device["name"]] = device["id"]
    return returndevices


def get_sites():
    returnsites = {}
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/dcim/sites/")
    response = requests.get(url, headers=headers)
    sites = response.json()
    for site in sites["results"]:
        try:
            if returnsites[site["name"]]:
                print("Duplicate site name")
        except:
           returnsites[site["name"]] = site["id"]
    return returnsites

def get_clusters():
    returnclusters = {}
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/virtualization/clusters")
    response = requests.get(url, headers=headers)
    clusters = response.json()
    for cluster in clusters["results"]:
        try:
            if returnclusters[cluster["name"]]:
                print("Duplicate cluster name")
        except:
           returnclusters[cluster["name"]] = cluster["id"]
    return returnclusters

def get_virtual_machine(id):
    returnvm = {}
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/virtualization/virtual-machines/" + str(id))
    print(url)
    response = requests.get(url, headers=headers)
    print(response.content)
    vm = response.json()
    return vm

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


    
def netboxdata(args):
    clusters = get_clusters()
    vms = get_virtual_machines()
    print(vms)

    vm_data = []
    for vm in vms:
        vmdata = get_virtual_machine(vms[vm])
        try:
            cluster = vmdata["cluster"]["name"]
        except:
            cluster = None
        print("---------------------------------------")
        print(vmdata['name'])
        print("---------------------------------------")
        vm_entry = {
            "name": vmdata['name'],
            "cluster": cluster,
            "disk_gb": vmdata["disk"],
            "cpu": vmdata["vcpus"],
            "memory_mb": vmdata["memory"],
            "local_context_data": vmdata["local_context_data"]
        }
        vm_data.append(vm_entry)

    data = {
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
    MYHOME = os.getenv("HOME")
    configdir = os.path.expanduser(MYHOME + "/.ssh")
    if not os.path.exists(configdir):
        os.makedirs(configdir)
    configdir = os.path.expanduser(MYHOME + "/.ssh/conf.d")
    if not os.path.exists(configdir):
        os.makedirs(configdir)
    configfilemaster = MYHOME + "/.ssh/config"
    if not os.path.isfile(configfilemaster):
        open(configfilemaster, "x").write("Include ~/.ssh/conf.d/*\n")
    includeexists = False
    with open(configfilemaster) as fh:
        for line in fh:
            if line.startswith("Include ~/.ssh/conf.d/*"):
                includeexists = True
    if not includeexists:
        open(configfilemaster, "w").write("Include ~/.ssh/conf.d/*\n")
    MYHOME = os.getenv("HOME")
    configfile = os.path.expanduser(MYHOME + "/.ssh/conf.d/kalm.conf")
    os.chmod(configfilemaster, 0o0600)
    os.chmod(configfile, 0o0600)
    open(configfile, "w").write(ssh_config_content)
    print(ssh_config_content)






def generate_ssh_config_entry(vm):
    proxy_jump = ""
    if vm["cluster"] != vm["name"]:

        proxy_jump = f"ProxyJump {vm['cluster']}".split(".openknowit.com")[0]
        if proxy_jump == "None":
            return ssh_config_template.format(
            hostname=vm["name"],
            full_hostname=vm["name"] + ".openknowit.com",
            )
        else:
            return ssh_config_template.format(
            hostname=vm["name"],
            full_hostname=vm["name"] + ".openknowit.com",
            proxy_jump=proxy_jump
            )
    else:
        return ssh_config_template.format(
        hostname=vm["name"],
        full_hostname=vm["name"] + ".openknowit.com"
        )




