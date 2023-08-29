from . import dns
from . import cloudflare

import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate", usage="kalm_dns <action> \n\n\
\
               version : 0.1.2 BETA \n\
               actions:\n\
               envcheck    check if env is set \n\
               setenv      set env \n\
               list        list dns records \n\
               sync        sync dns record\n\
               libvirt     create dns records for virtlib\n\
\n\
               2023 Knowit Miracle\n\
               ")
    
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup netbox')
    args = parser.parse_args()
    ready = False
    if args.action[0] == "sync":
        print("sync dns")
        dns.sync_dns(args)
        
    if args.action[0] == "envcheck":
        print("env check")
        dns.env_check()

    if args.action[0] == "setenv":
        print("set env")
        dns.set_env(args)
    
    if args.action[0] == "libvirt":
        print("set env")
        dns.libvirt(args)

    if args.action[0] == "default":
        print("set env")
        dns.default(args)

    if args.action[0] == "clean":
        dns.clean(args)

    if args.action[0] == "cloudflare":
        cloudflare.check_access()
        
    if args.action[0] == "list":
        if(cloudflare.check_access()):
            cloudflare.list_dns()   
            return True
        
    if args.action[0] == "add_record":
        if(cloudflare.check_access()):
            record = {
                "type": "A",
                "name": "test",
                "content": "123.123.123.124",
                "ttl": 300,
                "proxied": False
            }


            cloudflare.add_record(record)   
            return True


    





