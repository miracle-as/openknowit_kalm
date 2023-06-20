from . import jenkins
import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate", usage="kalm_jenkins <action> \n\n \
               \
               version : 0.1.2 jenkins  \n                                              \
               actions:\n                                                      \
               list        list jenkins \n  \
               set         set jenkins times \n  \
               plugins     get jenkins plugins \n  \
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")

    if args.action[0] == "list":
        print("list jenkins")
        jenkins.list_jenkins()
        

    if args.action[0] == "set":
        print("set jenkins")
        jenkins.set_jenkins(args)

    if args.action[0] == "get_plugins":
        print("get jenkins plugins")
        jenkins.get_plugins()

    if args.action[0] == "plugins":
        print("get jenkins plugins")
        jenkins.plugins()

    if args.action[0] == "install_plugin":
        print("install jenkins plugins")
        try:
            plugin = args.action[1]
        except:
            print("no plugin name")
            exit()
        jenkins.install_plugin(plugin)






