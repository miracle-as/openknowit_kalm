import requests
import os
from pyVmomi import vim
import atexit
import json
import pprint
import redis
import time
from pyVim.connect import SmartConnect, Disconnect
from ..common import prettyllog
from .common import get_env
from .organization import refresh_netbox_orgs
from .clusters import get_cluster_id, get_clusters
from .redis import refresh_netbox_from_redis
from .subprojects import update_subprojects



r = redis.Redis(host='localhost', port=6379, db=0)
data = {}

# MAIN
# We are serving vspere and we need an infinite loop
def main():
    prettyllog("netbox", "init", "service", "kalm" "ok", "000" , "starting server", severity="INFO")
    myenv = get_env()
    while True:
        netboxdata = refresh_netbox_orgs(myenv)
        #refresh_netbox_from_redis(myenv, netboxdata)
        update_subprojects(myenv)
        time.sleep(60)

# Refresh netbox from redis
#       clusters=get_clusters(myenv)
#       for cluster in clusters:
#           cluster_id = get_cluster_id(cluster, myenv)
#           if cluster_id:
#               prettyllog("netbox", "get", "cluster", cluster, cluster_id , "getting cluster id", severity="INFO")
#           else:
#               prettyllog("netbox", "get", "cluster", cluster, "000" , "unable to get cluster", severity="ERROR")
#       break








  