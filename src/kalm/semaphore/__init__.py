# keep kalm and con5entrate on your semaphores

from . import semaphore
import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and con5entrate on your semaphores", usage="kalm_semaphore <action> \n\n \
               \
                version : 0.0.2 (semaphore)\n\
                actions:\n\
                semaphore                 keep kalm and con5entrate on your semaphores\n\
                \n\
               \
               2023 Knowit Miracle\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False

    if args.action[0] == "semaphore":
        print("semaphore")
        semaphore.Semaphore()
        return 0
    
    if args.action[0] == "help":
        print(parser.print_help())
        return 0
    if args.action[0] == "version":
        print("0.0.2")
        return 0
    if args.action[0] == "test":
        print("test")
        return 0
    if args.action[0] == "setup":
        semaphore.setup()


