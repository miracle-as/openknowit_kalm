from . import dns
import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate", usage="kalm_dns <action> \n\n \
               \
               version : 0.1.2 BETA \n                                    \
               actions:\n                                                 \
               envcheck    check if env is set \n                         \
               setenv      set env \n                                     \
               list        list dns records \n  \
               sync        sync dns record\n  \
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup netbox')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")

    if args.action[0] == "list":
        print("list dns")
        dns.list_dns()
        
    if args.action[0] == "sync":
        print("sync dns")
        dns.rancher_inabox(args)
        
    if args.action[0] == "envcheck":
        print("env check")
        dns.env_check()
        ready = True

    if args.action[0] == "setenv":
        print("set env")
        dns.set_env(args)
        ready = True
        


    





