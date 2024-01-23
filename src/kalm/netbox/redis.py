import redis
import json
import pprint   
import time
from ..common import prettyllog
from .netbox_server import create_virtual_server
from .netbox import create_tag, addtagtovm, removetagsfromvm, addvmwaretags,  get_virtual_server_id

from .common import get_env
import os

redishost=os.getenv("KALM_REDIS_HOST")
if redishost is None:
    redishost="localhost"

    
redisport=os.getenv("KALM_REDIS_PORT")
if redisport is None:
    redisport="6379"

redisdb=os.getenv("KALM_REDIS_DB")
if redisdb is None:
    redisdb="0"
r = redis.Redis(host=redishost, port=redisport, db=redisdb)

def refresh_netbox_from_redis(myenv, netboxdata):
    knownservers = {}
    knownlinuxservers = {}
    orphanservers = []
    knownserverkeys = r.keys("kalm:vmware:*:known")
    knownlinuxserverkeys = r.keys("kalm:vmware:*:known:linux")
    for key in knownlinuxserverkeys:
        key = key.decode("utf-8")
        server = key.split(":")[2]
        value = r.get(key)
        value = value.decode("utf-8")
        age = time.time() - float(value)
        ageindays = int(age / 86400)
        ageinhours = int(age / 3600)
        ageinminutes = int(age / 60)
        if ageindays > 1:
            prettyllog("netbox", "get", "server", key, ageindays , "Date is older than one day", severity="INFO")
            orphanservers.append(server)
        else:
            if ageindays < 1 and ageinhours > 1:
                prettyllog("netbox", "get", "server", key, ageinhours , "Data is aging (Hours)", severity="INFO")
            else:
                prettyllog("netbox", "get", "server", key, ageinminutes , "data is fresh (Minutes)", severity="INFO")
            #
            detailkey = "kalm:vmware:" + server + ":details"
            if r.exists(detailkey):
              detailvalue = r.get(detailkey)
              decodeddetailvalue = detailvalue.decode("utf-8").replace("'", '"')
              knownlinuxservers[server] = detailvalue.decode("utf-8")
              detailjson = json.loads(decodeddetailvalue)   
              create_virtual_server(detailjson, myenv, netboxdata)
              prettyllog("netbox", "get", "server", key, "000" , "add vmware tags", severity="INFO")
              prettyllog("netbox", "get", "server", key, "000" , "server : %s" % server, severity="INFO")
              vmid = get_virtual_server_id(server, myenv)
              prettyllog("netbox", "get", "server", key, "000" , "server id : %s" % vmid, severity="INFO")
              prettyllog("netbox", "get", "server", key, "000" , "vmid: %s" % vmid, severity="INFO")
              if vmid:
                addvmwaretags(vmid, detailjson, myenv)
            else:
                prettyllog("netbox", "get", "server", key, "001" , "No details found", severity="ERROR")
                orphanservers.append(server)
    print("orphanservers: %s" % len(orphanservers))
    print("knownservers:  %s" % len(knownservers))
    return True     


