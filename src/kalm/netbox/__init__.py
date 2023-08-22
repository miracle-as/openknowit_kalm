from . import netbox
import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate netbox", usage="kalm_netbox <action> \n\n \
               \
               version : 0.0.2 (netbox)\n\
               actions:\n\
               netboxdata                dump netbox data in json \n\
               ssh_config                dump ssh_config\n\
               ansible_inventory         dump ansible inventory\n\
               refresh                   refresh core netbox content\n\
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False

    if args.action[0] == "ansible_inventory":
        netbox.ansible_inventory(args)
        return 0
    
    if args.action[0] == "ssh_config":
        netbox.sshconfig(args)
        return 0
    
    if args.action[0] == "netboxdata":
        netbox.netboxdata(args)
        return 0
    
    return 0

    

    







