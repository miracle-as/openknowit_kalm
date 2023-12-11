import redis
import json
import pprint   
import time
from ..common import prettyllog
from .netbox_server import create_virtual_server
from .common import get_env
import os



def refresh_netbox_from_redis(myenv, netboxdata):
    r = redis.Redis(host='localhost', port=6379, db=0)
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
              pprint.pprint(detailjson)
              create_virtual_server(detailjson, myenv, netboxdata)
            else:
                prettyllog("netbox", "get", "server", key, "000" , "No details found", severity="ERROR")
                orphanservers.append(server)
    print("orphanservers: %s" % len(orphanservers))
    print("knownservers:  %s" % len(knownservers))
    return True


