import argparse
import os


from ..common import prettyllog
from . import serve
from . import stop
from . import start
from . import status
from . import selinux
from . import firewall
from . import setup


def main():
    parser = argparse.ArgumentParser(description="Keep kalm and automate", usage="kalm_ui <action> \n\n\
\
                version : 0.0.1 \n\
                actions:\n\
                serve                        run the service as in systemd but with stdout on the terminal\n\
                start                        start the service in systemd\n\
                stop                         stop the systemd\n\
                status                       Show the status of the systemd services\n\
                selinux                      Ensure selinux is configured\n\
                firewall                     Ensure Firewall is configured\n\
                setup                        Setup server to host kalm_ui\n\
\
                2023 Knowit Miracle\n\
                ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup netbox')
    args = parser.parse_args()
    ready = False
    if args.action[0] == "serve":
        prettyllog("ui", "ui", "ui", "new", "000", "serve")
        serve.main()
        return 0
    
    if args.action[0] == "start":
        prettyllog("ui", "ui", "ui", "new", "000", "start")
        start.main()
        return 0
    
    if args.action[0] == "stop":
        prettyllog("ui", "ui", "ui", "new", "000", "stop")
        stop.main()
        return 0
    
    if args.action[0] == "status":
        prettyllog("ui", "ui", "ui", "new", "000", "status")
        status.main()
        return 0
    
    if args.action[0] == "selinux":
        prettyllog("ui", "ui", "ui", "new", "000", "selinux")
        selinux.main()
        return 0
    
    if args.action[0] == "firewall":
        prettyllog("ui", "ui", "ui", "new", "000", "firewall")
        firewall.main()
        return 0
    
    if args.action[0] == "setup":
        prettyllog("ui", "ui", "ui", "new", "000", "setup")
        setup.main()
        return 0
    
    

        
