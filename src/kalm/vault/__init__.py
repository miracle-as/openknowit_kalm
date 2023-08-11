from . import vault
import os

import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate", usage="kalm_vault <action> \n\n\
               \
               version : 0.1.2 vault  \n\
               actions:\n\
               signssh </path/to/key>\n\
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")

  
    

    if args.action[0] == "signssh":
          vault.signkey(args)
          return 0
    
        

