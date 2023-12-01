# keep kalm and manage your vspere

from . import serve
import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and con5entrate on your semaphores", usage="kalm_semaphore <action> \n\n \
\
version : 0.0.2 (semaphore)\n\
actions:\n\
serve      keep kalm and serve vspere\n\
\n\
\
2023 Knowit Miracle\
")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False

    if args.action[0] == "serve":
        serve.main()
        return 0
    