from . import bump
import argparse
from ..common import prettyllog




def main():
    parser = argparse.ArgumentParser(description="Keep kalm and bump", usage="kalm_bump <action> \n\n \
               \
               version : 1.0.0 bump  \n                                              \
               actions:\n                                                      \
               major        major bump \n  \
               minor        minor bump \n  \
               patch        patch bump \n  \
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")


    if args.action[0] == "major":
        bump.major()
        ready = True
    if args.action[0] == "minor":
        bump.minor()
        ready = True
    if args.action[0] == "patch":
        bump.patch()
        ready = True

    