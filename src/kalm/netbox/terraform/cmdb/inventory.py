import requests
import json
import os

# NetBox API configuration
NETBOX_URL = os.getenv("NETBOX_API_URL")
NETBOX_TOKEN = os.getenv("NETBOX_API_TOKEN")

# Fetch virtual machines from NetBox
def get_virtual_machines():
    headers = {
        "Authorization": f"Token {NETBOX_TOKEN}",
        "Accept": "application/json",
    }
    response = requests.get(f"{NETBOX_URL}/virtualization/virtual-machines/", headers=headers)
    print(response.content)
    vms = response.json()
    return vms

# Create inventory dictionary
def create_inventory(vms):
    inventory = {"all": {"hosts": {}}, "_meta": {"hostvars": {}}}
    
    for vm in vms["results"]:
        inventory["all"]["hosts"][vm["name"]] = None
        inventory["_meta"]["hostvars"][vm["name"]] = {
            "ip_address": vm["primary_ip4"]["address"] if vm.get("primary_ip4") else "",
            "guest_os": vm["virtual_machine"]["name"] if vm.get("virtual_machine") else "",
        }

    return inventory

# Write inventory to a file
def write_inventory(inventory, filename):
    with open(filename, "w") as file:
        json.dump(inventory, file, indent=2)

def main():
    vms = get_virtual_machines()
    inventory = create_inventory(vms)
    write_inventory(inventory, "inventory.json")

if __name__ == "__main__":
    main()

