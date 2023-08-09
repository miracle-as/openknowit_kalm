from . import inabox
import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate", usage="kalm <action> \n\n \
               \
               version : 0.1.2 BETA \n                                              \
               actions:\n                                                      \
               list        list inabox \n  \
               rancher     activate rancher in a box\n  \
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup netbox')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")

    if args.action[0] == "list":
        print("list inabox")
        inabox.list_inabox()
        
    if args.action[0] == "rancher":
        print("Start rancher in a boc")
        inabox.rancher_inabox()

    if args.action[0] == "ansible_role":
        print("Create ansible role directory structure")
        inabox.ansible_role_inabox()
        


    





