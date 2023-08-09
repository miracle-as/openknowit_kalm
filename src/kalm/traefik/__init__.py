from . import traefik
import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate", usage="kalm_traefik <action> \n\n \
               \
               version : 0.1.2 traefik  \n                                              \
               actions:\n                                                      \
               list        list traefik \n  \
               set         set traefik times \n  \
               plugins     get traefik plugins \n  \
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")

    if args.action[0] == "list":
        print("list traefik")
        traefik.list_traefik()

    if args.action[0] == "serve":
        traefik.serve_traefik()
        

