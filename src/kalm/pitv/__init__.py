from . import pitv
import argparse
from ..common import prettyllog




def main():
    parser = argparse.ArgumentParser(description="\
Keep kalm and photos safe", usage="kalm_pitv <action> \n\n\
\
version : 0.1.2 pitv  \n\n\
actions:\n\
status        status pitv \n\
service       keep all pictures safe \n\
\n\
\n\
2023 Knowit Miracle\n\
")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")


    if args.action[0] == "status":
        print("status pitv")
        pitv.status()

    if args.action[0] == "service":
        print("Ensure all pictures are safe")
        pitv.service()