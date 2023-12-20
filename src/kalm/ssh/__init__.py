from . import ssh
import argparse
from ..common import prettyllog


def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate ssh", usage="kalm_ssh <action> \n\n \
               \
               version : 0.0.1 kalm_ssh  \n\
               actions:                  \n\
               signssh                   \n\
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False

    if args.action[0] == "signssh":
        ssh.signssh()