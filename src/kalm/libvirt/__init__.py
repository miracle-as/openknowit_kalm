
from . import libvirt
from . import serve

import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate libvirt qemu", usage="kalm_libvirt <action> \n\n \
               \
                version : 0.0.2 (netbox)\n\
                actions:\n\
                serve                     \n\
               \
               2024 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False

    if args.action[0] == "serve":
        print("serve mode manintaon netbox data")
        serve.main()
        return 0