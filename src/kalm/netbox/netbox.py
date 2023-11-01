import requests
import json
import os
import base64
import xml.etree.ElementTree as ET
import platform
import yaml
from ..common import prettyllog


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
    prettyllog("manage", "netbox", "device", "new", "000", "Getting device id")
    devices = get_devices()
    try:    
        prettyllog("manage", "netbox", "device", "new", "000", "Device id is %s" % devices[device_name])
        return devices[device_name]
    except:
        prettyllog("manage", "netbox", "device", "new", "000", "Device id is None")
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
        return None

def get_manufacturer_id(manufacturer_name):
    manufacturers = get_manufacturers()
    try:
        return manufacturers[manufacturer_name]
    except:
        return None
        
def get_virtual_machine_id(vm_name):
    vms = get_virtual_machines()
    try:
        return vms[vm_name]
    except:
        return None
    
def get_interface_id(interface_name):
    interfaces = get_interfaces()
    try:
        return interfaces[interface_name]
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
    prettyllog("manage", "netbox", "device", "new", "000", "Creating device type")
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    prettyllog("manage", "netbox", "device", "new", "000", "Getting device type name")
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
        device_type_subdevice_role = "" 
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
    
def create_device():
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }

    # Mandatory fields
    device_name = os.environ.get('KALM_DEVICE_NAME')
    if device_name == None:
        device_name = "default"
    device_type = os.environ.get('KALM_DEVICE_TYPE')
    if device_type == None:
        device_type = "default"
    device_role = os.environ.get('KALM_DEVICE_ROLE')
    if device_role == None:
        device_role = "default"
    device_site = os.environ.get('KALM_DEVICE_SITE')
    if device_site == None:
        device_site = "default"
    device_status = os.environ.get('KALM_DEVICE_STATUS')
    if device_status == None:
        device_status = "active"
    device_comments = os.environ.get('KALM_DEVICE_COMMENTS')
    if device_comments == None:
        device_comments = ""
    devicetype_id = get_type_id(device_type)
    if devicetype_id == None:
        create_device_type(device_type)
        devicetype_id = get_type_id(device_type)
    device_role_id = get_role_id(device_role)
    if device_role_id == None:
        create_role(device_role)
        device_role_id = get_role_id(device_role)
    device_site_id = get_site_id(device_site)
    if device_site_id == None:
        create_site(device_site)
        device_site_id = get_site_id(device_site)



    data = {
        "name": device_name,
        "device_type": 1,
        "device_role": 1,
        "site": 1,
        "status": "active",  
        "comments": "This is an example device in NetBox."
    }

def create_role():
    prettyllog("manage", "netbox", "device", "new", "000", "Creating role")
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    prettyllog("manage", "netbox", "device", "new", "000", "Getting role name")
    role_name = os.environ.get('KALM_ROLE_NAME')
    if role_name == None:
        role_name = "default"
    prettyllog("manage", "netbox", "device", "new", "000", "Getting role name is %s" % role_name)
    prettyllog("manage", "netbox", "device", "new", "000", "Getting role slug")
    role_slug = os.environ.get('KALM_ROLE_SLUG')
    if role_slug == None:
        role_slug = role_name.lower()
    prettyllog("manage", "netbox", "device", "new", "000", "Getting role slug is %s" % role_slug)
    prettyllog("manage", "netbox", "device", "new", "000", "Getting role description")
    role_description = os.environ.get('KALM_ROLE_DESCRIPTION')
    if role_description == None:
        role_description = ""
    prettyllog("manage", "netbox", "device", "new", "000", "Getting role description is %s" % role_description)
    prettyllog("manage", "netbox", "device", "new", "000", "Getting role comments")

    role_comments = os.environ.get('KALM_ROLE_COMMENTS')
    if role_comments == None:
        role_comments = ""
    prettyllog("manage", "netbox", "device", "new", "000", "Getting role comments is %s" % role_comments)
    prettyllog("manage", "netbox", "device", "new", "000", "assemble data")
    data = {
        "name": role_name,
        "slug": role_slug,
        "description": role_description,
        "comments": role_comments
    }
    role_id = get_role_id(role_name)
    if role_id != None:
        prettyllog("manage", "netbox", "device", "new", "000", "Role already exists")
        return True
    url = fix_url("/dcim/device-roles/")
    response = requests.post(url, headers=headers, json=data)
    print(response)
    print(response.json())
    print(response.status_code)
    print(response.content)
    if response.status_code == 200:
        return True
    else:
        return False

def create_platform(platform_name):
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    platform_name = os.environ.get('KALM_PLATFORM_NAME')
    if platform_name == None:
        platform_name = "default"
    platform_slug = os.environ.get('KALM_PLATFORM_SLUG')
    if platform_slug == None:
        platform_slug = platform_name.lower()
    platform_description = os.environ.get('KALM_PLATFORM_DESCRIPTION')
    if platform_description == None:
        platform_description = ""
    platform_comments = os.environ.get('KALM_PLATFORM_COMMENTS')
    if platform_comments == None:
        platform_comments = ""



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
    manufacturer = os.environ.get("KALM_NETBOX_MANUFACTURER")
    if manufacturer == None:
        manufacturer == "noname"
    manufacturer_id = get_manufacturer_id(manufacturer)
    if manufacturer_id == None:
        create_manufacturer(manufacturer)
        manufacturer_id = get_manufacturer_id(manufacturer)

    data = {
        "name": type_name, 
        "model": type_name,
        "manufacturer": manufacturer_id,
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
    
def create_platform(platform_name):
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    platform_name = os.environ.get('KALM_PLATFORM_NAME')
    if platform_name == None:
        platform_name = "default"
    platform_slug = os.environ.get('KALM_PLATFORM_SLUG')
    if platform_slug == None:
        platform_slug = platform_name.lower()
    platform_description = os.environ.get('KALM_PLATFORM_DESCRIPTION')
    if platform_description == None:
        platform_description = ""
    platform_comments = os.environ.get('KALM_PLATFORM_COMMENTS')
    if platform_comments == None:
        platform_comments = ""
    platform_napalm_driver = os.environ.get('KALM_PLATFORM_NAPALM_DRIVER')
    if platform_napalm_driver == None:
        platform_napalm_driver = ""
    platform_napalm_args = os.environ.get('KALM_PLATFORM_NAPALM_ARGS')
    if platform_napalm_args == None:
        platform_napalm_args = ""
    data = {
        "name": platform_name,
        "slug": platform_slug,
        "napalm_driver": platform_napalm_driver,
        "napalm_args": platform_napalm_args,
        "description": platform_description,
        "comments": platform_comments
    }
    platform_id = get_platform_id(platform_name)
    if platform_id != None:
        return True
    url = fix_url("/dcim/platforms/")
    response = requests.post(url, headers=headers, json=data)
    print(response)
    print(response.json())
    print(response.status_code)
    print(response.content)
    if response.status_code == 200:
        return True
    else:
        return False
    
def create_virtual_machine(vm_name):
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    vm_name = os.environ.get('KALM_VM_NAME')
    if vm_name == None:
        vm_name = "default"

    vm_cluster = os.environ.get('KALM_VM_CLUSTER')
    if vm_cluster == None:
        vm_cluster = "default"
    vm_tenant = os.environ.get('KALM_VM_TENANT')
    if vm_tenant == None:
        vm_tenant = "default"
    vm_role = os.environ.get('KALM_VM_ROLE')
    if vm_role == None:
        vm_role = "default"
    vm_status = os.environ.get('KALM_VM_STATUS')
    if vm_status == None:
        vm_status = "active"
    vm_comments = os.environ.get('KALM_VM_COMMENTS')
    if vm_comments == None:
        vm_comments = ""
    vm_custom_fields = os.environ.get('KALM_VM_CUSTOM_FIELDS')
    if vm_custom_fields == None:
        vm_custom_fields = {}
    vm_type = os.environ.get('KALM_VM_TYPE')
    if vm_type == None:
        vm_type = "default"
    vm_type_id = get_type_id(vm_type)
    if vm_type_id == None:
        create_type(vm_type)
        vm_type_id = get_type_id(vm_type)
    vm_tenant_id = get_tenant_id(vm_tenant)
    if vm_tenant_id == None:
        create_tenant(vm_tenant)
        vm_tenant_id = get_tenant_id(vm_tenant)
    vm_role_id = get_role_id(vm_role)
    if vm_role_id == None:
        create_role(vm_role)
        vm_role_id = get_role_id(vm_role)
    vm_cluster_id = get_cluster_id(vm_cluster)
    if vm_cluster_id == None:
        create_cluster(vm_cluster)
        vm_cluster_id = get_cluster_id(vm_cluster)
    data = {
        "name": vm_name,
        "cluster": vm_cluster_id,
        "tenant": vm_tenant_id,
        "role": vm_role_id,
        "status": vm_status,
        "comments": vm_comments,
        "custom_fields": vm_custom_fields,
        "type": vm_type_id
    }
    vm_id = get_virtual_machine_id(vm_name)
    if vm_id != None:
        return True
    url = fix_url("/virtualization/virtual-machines/")
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return True
    else:
        return False
    
def create_iprange(iprange_description = "default"):
    prettyllog("manage", "netbox", "iprange", "new", "000", "Creating iprange")
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    prettyllog("manage", "netbox", "iprange", "new", "000", "Getting iprange start address")
    ip_start_address = os.environ.get('KALM_IP_START_ADDRESS')
    if ip_start_address == None:
        ip_start_address = ""
    prettyllog("manage", "netbox", "iprange", "new", "000", "Getting iprange end address")
    ip_end_address = os.environ.get('KALM_IP_END_ADDRESS')
    if ip_end_address == None:
        ip_end_address = ""
    prettyllog("manage", "netbox", "iprange", "new", "000", "Getting iprange status")
    ip_status = os.environ.get('KALM_IP_STATUS')
    if ip_status == None:
        ip_status = "active"
    prettyllog("manage", "netbox", "iprange", "new", "000", "Getting iprange vrf")

    ip_vrf = os.environ.get('KALM_IP_VRF')
    if ip_vrf == None:
        ip_vrf = "Global"
    prettyllog("manage", "netbox", "iprange", "new", "000", "Getting iprange role")
    ip_role = os.environ.get('KALM_IP_ROLE')
    if ip_role == None:
        ip_role = "loopback"

    prettyllog("manage", "netbox", "iprange", "new", "000", "Getting iprange tenant")
    ip_tenant = os.environ.get('KALM_IP_TENANT')
    if ip_tenant == None:
        ip_tenant = "default"
    ip_tenant_id = get_tenant_id(ip_tenant)
    prettyllog("manage", "netbox", "iprange", "new", "000", "Getting iprange tenana id")
    if ip_tenant_id == None:
        create_tenant(ip_tenant)
        ip_tenant_id = get_tenant_id(ip_tenant)
    prettyllog("manage", "netbox", "iprange", "new", "000", "Getting iprange description")
    iprange_description = os.environ.get('KALM_IPRANGE_DESCRIPTION')
    prettyllog("manage", "netbox", "iprange", "new", "000", "Getting iprange description is %s" % iprange_description)
    prettyllog("manage", "netbox", "iprange", "new", "000", "Getting iprange iprange id")
    iprange_description_id = get_iprange_id(iprange_description)
    if iprange_description_id != None:
        prettyllog("manage", "netbox", "iprange", "new", "000", "Ip range already exists")
        return True


#            "id": 2,
#            "url": "http://netbox.openknowit.com/api/ipam/ip-ranges/2/",
#            "display": "192.168.86.0-255/24",
#            "family": {
#                "value": 4,
#                "label": "IPv4"
#            },
#            "start_address": "192.168.86.0/24",
#           "end_address": "192.168.86.255/24",
#            "size": 256,
#            "vrf": null,
#            "tenant": null,
#            "status": {
#                "value": "active",
#                "label": "Active"
#            },
#            "role": null,
#            "description": "",
#            "comments": "",
#           "tags": [],
#            "custom_fields": {},
#            "created": "2023-09-09T21:00:01.355556Z",
#            "last_updated": "2023-09-09T21:00:01.355576Z",
#            "mark_utilized": false

    data  = {
        "start_address": ip_start_address,
        "end_address": ip_end_address,
        "status": ip_status,
        "vrf": ip_vrf,
        "role": ip_role,
        "tenant": ip_tenant_id,
        "description": iprange_description
    }

    url = fix_url("/ipam/ip-ranges/")
    response = requests.post(url, headers=headers, json=data)
    print(response.content)
    if response.status_code == 200:
        return True
    else:
        return False
    




    
def create_ip4(ip4_address = "default"):
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }

    # Mandatory fields
    ip_address = os.environ.get('KALM_IP_ADDRESS')
    if ip_address == None:
        ip_address = "127.0.0.1"
    ip4_status = os.environ.get('KALM_IP_STATUS')
    if ip_status == None:  
        ip_status = "active"
    ip4_role = os.environ.get('KALM_IP4_ROLE')
    if ip_role == None:
        ip_role = "loopback"
    tenant = os.environ.get('KALM_NETBOX_TENANT')   
    if ip_tenant == None:
        ip_tenant = "default"
    tenant_id = get_tenant_id(ip_tenant)
    if tenant_id == None:
        create_tenant(tenant)
        tenant_id = get_tenant_id(tenant)





def create_virtual_interface(interface_name):
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    interface_name = os.environ.get('KALM_VINTERFACE_NAME')
    if interface_name == None:
        interface_name = "default"
    interface_type = os.environ.get('KALM_INTERFACE_TYPE')
    if interface_type == None:
        interface_type = "virtual"
    interface_mac_address = os.environ.get('KALM_INTERFACE_MAC_ADDRESS')
    if interface_mac_address == None:
        interface_mac_address = ""
    interface_mtu = os.environ.get('KALM_INTERFACE_MTU')
    if interface_mtu == None:
        interface_mtu = ""
    interface_description = os.environ.get('KALM_INTERFACE_DESCRIPTION')
    if interface_description == None:
        interface_description = ""
    interface_mode = os.environ.get('KALM_INTERFACE_MODE')

    

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
    
    
def get_system_info():
    system_info = platform.uname()
    system_manufacturer = system_info.system
    is_virtual = "QEMU" in system_manufacturer

    return system_manufacturer, is_virtual

def is_kvm_qemu_host():
    # Check if KVM kernel module is loaded
    kvm_module_loaded = os.path.exists('/dev/kvm')

    # Check if QEMU-KVM process is running
    qemu_process_running = False
    with os.popen('pgrep -f qemu') as process:
        qemu_process_running = process.read().strip() != ''

    # Check for presence of QEMU virtualization tools
    qemu_tools_installed = os.path.exists('/usr/bin/qemu-system-x86_64')

    # Check if virt-what tool is available and if it reports "kvm" or "qemu"
    virt_what_installed = os.path.exists('/usr/sbin/virt-what')
    virt_what_result = None
    if virt_what_installed:
        with os.popen('/usr/sbin/virt-what') as process:
            virt_what_result = process.read().strip()
    return kvm_module_loaded or qemu_process_running or qemu_tools_installed or virt_what_result == "kvm" or virt_what_result == "qemu"

def add_device():
    prettyllog("manage", "netbox", "device", "new", "000", "Adding device to netbox")
    prettyllog("manage", "netbox", "device", "new", "000", "Getting system info")
    manufacturer, is_virtual = get_system_info()
    prettyllog("manage", "netbox", "device", "new", "000", "The system is %s and %s " % (manufacturer, str(is_virtual)))
    if not is_virtual:
        prettyllog("manage", "netbox", "device", "new", "000",  "Not a virtual machine, adding to netbox")
        headers = {
            "Authorization": f"Token {NETBOX_TOKEN}",
            "Accept": "application/json"
        }
        # Mandatory fields
        prettyllog("manage", "netbox", "device", "new", "000", "Getting device name")
        device_name = os.environ.get("KALM_DEVICE_NAME")
        if device_name == None:
            device_name = os.environ.get('HOSTNAME')
        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device name is %s" % device_name)

        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device type")    
        device_type = os.environ.get("KALM_DEVICE_TYPE")
        if device_type == None:
            device_type = "default"
        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device type is %s" % device_type)

        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device role")    
        device_role = os.environ.get("KALM_DEVICE_ROLE")
        if device_role == None:
            device_role = "default"
        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device role is %s" % device_role)   

        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device site")
        device_site = os.environ.get("KALM_DEVICE_SITE")
        if device_site == None:
            device_site = "default"
        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device site is %s" % device_site)

        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device status")
        device_status = os.environ.get("KALM_DEVICE_STATUS")
        if device_status == None:
            device_status = "active"
        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device status is %s" % device_status)


        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device comments")    
        device_comments = os.environ.get("KALM_DEVICE_COMMENTS")
        if device_comments == None:
            device_comments = ""
        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device comments is %s" % device_comments)

        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device type id")
        devicetype_id = get_type_id(device_type)
        if devicetype_id == None:
            prettyllog("manage", "netbox", "device", "new", "000",  "Creating device type")
            create_device_type(device_type)
            devicetype_id = get_type_id(device_type)
        prettyllog("manage", "netbox", "device", "new", "000", "Getting device type id is %s" % devicetype_id)

        prettyllog("manage", "netbox", "device", "new", "000", "Getting device role id")
        device_role_id = get_role_id(device_role)
        if device_role_id == None:
            create_role()
            device_role_id = get_role_id(device_role)
        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device role id is %s" % device_role_id)

        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device site id")
        device_site_id = get_site_id(device_site)
        if device_site_id == None:
            create_site(device_site)
            device_site_id = get_site_id(device_site)
        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device site id is %s" % device_site_id)

        prettyllog("manage", "netbox", "device", "new", "000",  "Assembling device data")
        data = {
            "name": device_name,
            "device_type": devicetype_id,
            "role": device_role_id,
            "device_role": device_role_id,
            "site": device_site_id,
            "status": device_status,
            "comments": device_comments
        }
        prettyllog("manage", "netbox", "device", "new", "000",  "Assembled device data is %s" % data)
        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device id")
        device_id = get_device_id(device_name)
        if device_id != None:
            prettyllog("manage", "netbox", "device", "new", "000",  "Device already exists")
            return True
        prettyllog("manage", "netbox", "device", "new", "000",  "Getting device id is %s" % device_id)

        prettyllog("manage", "netbox", "device", "new", "000",  "Preparing to add device")
        url = fix_url("/dcim/devices/")
        response = requests.post(url, headers=headers, json=data)
        prettyllog("manage", "netbox", "device", "new", "000",  "Api call status is %s" % response.status_code)
        print(response.content)
        if response.status_code == 200:
            return True
        else:
            return False
    else:
        return True
    
        
      




    return False

def add_vm():
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    # Mandatory fields
    kvm_qemu_host = is_kvm_qemu_host()

    manufacturer, is_virtual = get_system_info()
    if manufacturer == "QEMU":
        is_virtual = True
    else:
        is_virtual = False
    if not is_virtual:
      servername = os.environ.get("KALM_SERVER_NAME")
      if servername == None:
        servername = os.environ.get('HOSTNAME')
      


    if is_virtual:    
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
    if nburl == None:
        print("No NETBOX_API_URL provided")
        return False

    if nburl.endswith("/"):
        nburl = nburl[:-1]
    if not nburl.endswith("/api"):
        nburl = nburl + "/api"
    nburl = nburl + apiurl
    return nburl

def get_iprange_id(iprange_description):
    ipranges =  get_ipranges()
    try:
        return ipranges[iprange_description]
    except:
        return None


def get_ipranges():
    returnipranges = {}
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/ipam/ip-ranges/")
    response = requests.get(url, headers=headers)
    ipranges = response.json()
    for iprange in ipranges["results"]:
        try:
            if returnipranges[iprange["description"]]:
                print("Duplicate iprange name")
        except:
           returnipranges[iprange["description"]] = iprange["id"]
    return returnipranges



def get_interfaces():
    returninterfaces = {}
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/dcim/interfaces/")
    response = requests.get(url, headers=headers)
    interfaces = response.json()
    for interface in interfaces["results"]:
        try:
            if returninterfaces[interface["name"]]:
                print("Duplicate interface name")
        except:
           returninterfaces[interface["name"]] = interface["id"]
    return returninterfaces



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
        print(role)
        try:
            if returnroles[role["name"]]:
                print("Duplicate role name")
        except:
           returnroles[role["name"]] = role["id"]
    return returnroles



def get_device_types():
    returntypes = {}
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json"
    }
    url = fix_url("/dcim/device-types/")
    response = requests.get(url, headers=headers)
    types = response.json()
    for type in types["results"]:
        print(type)
        try:
            if returntypes[type["display"]]:
                print("Duplicate type name")
        except:
           returntypes[type["display"]] = type["id"]
    return returntypes

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
    response = requests.get(url, headers=headers)
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
    vm_data = []
    for vm in vms:
        vmdata = get_virtual_machine(vms[vm])
        try:
            cluster = vmdata["cluster"]["name"]
        except:
            cluster = None
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
    prettyllog("ssh_config", "update ssh config", "~/.ssh/conf.d/organisation", "organization", "000", "Starting ssh config update", "INFO")
    data = netboxdata(args)
    prettyllog("ssh_config", "update ssh config", "~/.ssh/conf.d/organisation", "organization", "000", "Got netbox data", "INFO")
    virtual_machines = data["virtual_machines"]
    prettyllog("ssh_config", "update ssh config", "~/.ssh/conf.d/organisation", "organization", "000", "Got virtual machines", "INFO")
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
    #create an empty file if its missing
    touch(configfile)
    touch(configfilemaster) 
    



    os.chmod(configfilemaster, 0o0600)
    os.chmod(configfile, 0o0600)
    # open config file and create it if its missing
    open(configfile, "w").write(ssh_config_content)
    prettyllog("ssh_config", "update ssh config", "~/.ssh/conf.d/organisation", "organization", "000", "new ssh config written", "INFO")




def touch(file_path):
    try:
        # Open the file in append mode, which creates the file if it doesn't exist
        with open(file_path, "a"):
            os.utime(file_path, None)  # Update the file's access and modification timestamps
        print(f"File '{file_path}' created or updated successfully.")
    except Exception as e:
        print(f"Error: {e}")


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

import subprocess

def get_unique_sorted_items(filename):

# Run the 'cat inventory' command and capture its output
    cat_process = subprocess.Popen(['cat', 'inventory'], stdout=subprocess.PIPE)
    inventory_output, _ = cat_process.communicate()

# Split the output into lines, filter out lines starting with "[", and containing lowercase letters
    filtered_lines = [line for line in inventory_output.decode().splitlines() if not line.startswith('[') and any(c.islower() for c in line)]

# Extract the first column from each line
    first_columns = [line.split()[0] for line in filtered_lines]

# Remove duplicate entries and sort the result
    unique_sorted_items = sorted(set(first_columns))
    return unique_sorted_items

def serve():
    prettyllog("manage", "netbox", "serve", "000", "Starting netbox serve")
    prettyllog("manage", "netbox", "serve", "000", "Getting netbox token")
    global NETBOX_TOKEN
    NETBOX_TOKEN = os.environ.get('NETBOX_API_TOKEN')
    if NETBOX_TOKEN == None:
        prettyllog("manage", "netbox", "serve", "000", "No netbox token found")
        return False
    prettyllog("manage", "netbox", "serve", "000", "Getting netbox url")
    global NETBOX_URL
    NETBOX_URL = os.environ.get('NETBOX_API_URL')
    if NETBOX_URL == None:
        prettyllog("manage", "netbox", "serve", "000", "No netbox url found")
        return False
    prettyllog("manage", "netbox", "serve", "000", "Read the /etc/kalm/kalm_netbox.json file")
    data = {}
    with open('/etc/kalm/kalm_netbox.json') as json_file:
        data = json.load(json_file)
        prettyllog("manage", "netbox", "serve", "000", "The data is %s" % data)
        prettyllog("manage", "netbox", "serve", "000", "The data is %s" % data["netbox"])
        prettyllog("manage", "netbox", "serve", "000", "The data is %s" % data["netbox"]["token"])
        NETBOX_TOKEN = data["netbox"]["token"]
        NETBOX_URL = data["netbox"]["url"]
    
    

def inventory_upload():
    prettyllog("manage", "netbox", "inventory", "upload", "000", "Uploading inventory to netbox")
    prettyllog("manage", "netbox", "inventory", "upload", "000", "locating inventory file")
    inventory_file = os.environ.get("KALM_INVENTORY_FILE")
    if inventory_file == None:
        inventory_file = "inventory"
    prettyllog("manage", "netbox", "inventory", "upload", "000", "inventory file is %s" % inventory_file)
    prettyllog("manage", "netbox", "inventory", "upload", "000", "print the inventory file")
    invfile = open(inventory_file, "r")
    print(invfile.read())
    prettyllog("manage", "netbox", "inventory", "upload", "000", "inventory file printed")
    items = get_unique_sorted_items(inventory_file)
    for item in items:
        prettyllog("manage", "netbox", "inventory", "upload", "000", "Adding %s to netbox" % item)
        os.environ["KALM_DEVICE_NAME"] = item
        add_device()



