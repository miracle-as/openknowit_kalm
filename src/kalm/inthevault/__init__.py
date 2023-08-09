from . import inthevault
import argparse


def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate", usage="kalm_inthevault <action> \n\n \
               \
               version : 0.1.2 inthevault  \n                                              \
               actions:\n                                                      \
               status        status inthevault \n  \
               list_dags     list inthevault dags \n  \
               delete_all_dags     delete all inthevault dags \n  \
               plugins     get inthevault plugins \n  \
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")


    if args.action[0] == "status":
        print("status inthevault")
        inthevault.status()


    if args.action[0] == "list_datasets":
        print("list_datasets inthevault")
        inthevault.list_datasets()
    
    if args.action[0] == "delete_all_datasets":
        print("delete_all_datasets inthevault")
        inthevault.delete_all_datasets()
        

    if args.action[0] == "delete_all_dags":
        print("delete_all_dags inthevault")
        inthevault.delete_all_dags()


    if args.action[0] == "set":
        print("set inthevault")
        inthevault.set()
    if args.action[0] == "list_dags":
        print("list_dags inthevault")
        inthevault.list_dags()



