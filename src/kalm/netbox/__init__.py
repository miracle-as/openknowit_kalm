from . import netbox
import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate netbox", usage="kalm_netbox <action> \n\n \
               \
               version : 0.0.1 (netboxi)   \n                                              \
               actions:\n                                                      \
               refresh     refresh core netbox content \n  \
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False

    if args.action[0] == "refresh":
        print("set jenkins")
        netbox.refresh(args)







