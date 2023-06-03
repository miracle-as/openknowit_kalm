from . import jenkins
import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate", usage="kalm <action> \n\n \
               \
               version : 0.1.2 BETA \n                                              \
               actions:\n                                                      \
               list        list jenkins \n  \
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup netbox')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")

    if args.action[0] == "list":
        print("list jenkins")
        jenkins.list_jenkins()
        


    





