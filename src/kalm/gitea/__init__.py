from . import gitea
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
        gitea.list_gitea()
        

    if args.action[0] == "set":
        print("set gitea")
        gitea.set_gitea(args)

    if args.action[0] == "get_plugins":
        print("get gitea plugins")
        gitea.get_plugins()

    if args.action[0] == "plugins":
        print("get gitea plugins")
        gitea.plugins()

    if args.action[0] == "install_plugin":
        print("install gitea plugins")
        try:
            plugin = args.action[1]
        except:
            print("no plugin name")
            exit()
        gitea.install_plugin(plugin)






