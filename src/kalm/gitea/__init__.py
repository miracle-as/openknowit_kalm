from . import git
import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate", usage="kalm_gitea <action> \n\n \
               \
               version : 0.1.2 gitea  \n                                              \
               actions:\n                                                      \
               list        list gitea \n  \
               set         set gitea times \n  \
               plugins     get gitea plugins \n  \
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")

    if args.action[0] == "list":
        print("list gitea")
        git.list_gitea()
