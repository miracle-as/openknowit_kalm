from . import netbox 
from . import serve

import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate netbox", usage="kalm_netbox <action> \n\n \
               \
                version : 0.0.2 (netbox)\n\
                actions:\n\
                netboxdata                dump netbox data in json \n\
                inventory_upload          upload ansible inventory to netbox \n\
                ssh_config                dump ssh_config\n\
                ansible_inventory         dump ansible inventory\n\
                devices_types             list device types\n\
                manufacturers             list manufacturers\n\
                tenants                   list tenants\n\
                roles                     list roles\n\
                sites                     list sites\n\
                ipranges                  list ip ranges\n\
                ips                       list ips\n\
                create_cluster            create cluster\n\
                create_tenant_group       create tenant group\n\
                create_tenant             create tenant\n\
                create_manufacturer       create manufacturer\n\
                create_site               create site\n\
                create_role               create role\n\
                create_ip                 create ip address\n\
                create_iprange            create ip range address\n\
                create_device_type        create device type\n\
                add_vm                    add virtual server to netbox\n\
                add_device                add device to netbox\n\
                refresh                   refresh core netbox content\n\
                serve                     \n\
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False

    if args.action[0] == "serve":
        print("serve mode manintaon netbox data")
        serve.main()
        return 0

    if args.action[0] == "inventory_upload":
        print("inventory_upload")
        netbox.inventory_upload()
        return 0
    
    if args.action[0] == "help":
        print(parser.print_help())
        return 0
    if args.action[0] == "version":
        print("0.0.2")
        return 0
    if args.action[0] == "test":
        print("test")
        return 0
    if args.action[0] == "setup":
        netbox.setup()
        return 0

    if args.action[0] == "devices_types":
        print(netbox.get_device_types())
        return 0
    
    if args.action[0] == "manufacturers":
        print(netbox.get_manufacturers())
        return 0
    
    if args.action[0] == "sites":
        print(netbox.get_sites())
        return 0
    

    if args.action[0] == "refresh":
        netbox.refresh()
        return 0
    
    if args.action[0] == "create_iprange":
        netbox.create_iprange(args)
        return 0

    if args.action[0] == "create_ip":
        netbox.create_ip4(args)
        return 0
    
    if args.action[0] == "create_cluster":
        netbox.create_cluster(args)
        return 0
    if args.action[0] == "create_tenant_group":
        netbox.create_tenant_group(args)
        return 0
    
    if args.action[0] == "create_tenant":
        netbox.create_tenant(args)
        return 0
    
    if args.action[0] == "create_device_type":
        netbox.create_device_type(args)
        return 0
    
    if args.action[0] == "create_role":
        netbox.create_role()
        return 0
    
    if args.action[0] == "create_site":
        netbox.create_site(args)
        return 0
    
    if args.action[0] == "create_manufacturer":
        netbox.create_manufacturer(args)
        return 0
    
    if args.action[0] == "ansible_inventory":
        netbox.ansible_inventory(args)
        return 0
    
    if args.action[0] == "ssh_config":
        netbox.sshconfig(args)
        return 0
    
    if args.action[0] == "netboxdata":
        netbox.netboxdata(args)
        return 0
    
    if args.action[0] == "vizualize":
        netbox.vizulize(args)
        return     
    
    if args.action[0] == "sites":
        print(netbox.get_sites())
        return 0
    
    if args.action[0] == "tenants":
        print(netbox.get_tenants())
        return 0
    
    if args.action[0] == "roles":
        print(netbox.get_roles())
        return 0
    
    if args.action[0] == "add_vm":
        return netbox.add_vm()    
    
    if args.action[0] == "add_device":
        print("add_device")
        return netbox.add_device()    
    return 0

    

    







