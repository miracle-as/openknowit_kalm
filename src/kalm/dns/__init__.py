from . import dns
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
    if args.action[0] == "list":
        dns.list_dns()
        
    if args.action[0] == "sync":
        print("sync dns")
        dns.sync_dns(args)
        
    if args.action[0] == "envcheck":
        print("env check")
        dns.env_check()
        ready = True

    if args.action[0] == "setenv":
        print("set env")
        dns.set_env(args)
        ready = True
    
    if args.action[0] == "libvirt":
        print("set env")
        dns.virtlib(args)
        ready = True

    if args.action[0] == "default":
        print("set env")
        dns.(args)
        ready = True


        


    





