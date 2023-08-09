from . import airflow
import argparse


def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate", usage="kalm_airflow <action> \n\n \
               \
               version : 0.1.2 airflow  \n                                              \
               actions:\n                                                      \
               status        status airflow \n  \
               list_dags     list airflow dags \n  \
               delete_all_dags     delete all airflow dags \n  \
               plugins     get airflow plugins \n  \
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")


    if args.action[0] == "status":
        print("status airflow")
        airflow.status()


    if args.action[0] == "list_datasets":
        print("list_datasets airflow")
        airflow.list_datasets()
    
    if args.action[0] == "delete_all_datasets":
        print("delete_all_datasets airflow")
        airflow.delete_all_datasets()
        

    if args.action[0] == "delete_all_dags":
        print("delete_all_dags airflow")
        airflow.delete_all_dags()


    if args.action[0] == "set":
        print("set airflow")
        airflow.set()
    if args.action[0] == "list_dags":
        print("list_dags airflow")
        airflow.list_dags()



