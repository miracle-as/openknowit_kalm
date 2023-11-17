# keep kalm and con5entrate on your semaphores

from . import semaphore
import argparse

def main():
    parser = argparse.ArgumentParser(description="Keep kalm and con5entrate on your semaphores", usage="kalm_semaphore <action> \n\n \
\
version : 0.0.2 (semaphore)\n\
actions:\n\
serve      keep kalm and serve semaphore\n\
init       keep kalm and init semaphore systemd service\n\
start      keep kalm and start semaphore systemd service\n\
stop       keep kalm and stop semaphore systemd service\n\
restart    keep kalm and restart semaphore systemd service\n\
setup      keep kalm and setup semaphore\n\
test       keep kalm and test semaphore\n\
audit      keep kalm and audit semaphore\n\
\n\
\
2023 Knowit Miracle\
")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkis')
    args = parser.parse_args()
    ready = False

    if args.action[0] == "serve":
        semaphore.server()
        return 0
    if args.action[0] == "init":
        semaphore.init()
        return 0
    if args.action[0] == "start":
        semaphore.start()
        return 0
    if args.action[0] == "stop":
        semaphore.stop()
        return 0
    if args.action[0] == "restart":
        semaphore.restart()
        return 0
    if args.action[0] == "audit":
        semaphore.audit()
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


