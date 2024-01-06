import requests
import libvirt
import os
from pyVmomi import vim
import atexit
import json
import pprint
import pickle
import redis
import time
from pyVim.connect import SmartConnect, Disconnect
from ..common import prettyllog

print("Starting libvirt service")    
print("-------------------------------------------------------")
redishost=os.getenv("KALM_REDIS_HOST")
if redishost is None:
    redishost="localhost"

    
redisport=os.getenv("KALM_REDIS_PORT")
if redisport is None:
    redisport="6379"

redisdb=os.getenv("KALM_REDIS_DB")
if redisdb is None:
    redisdb="0"
print("Using redis host: %s" % redishost)
print("Using redis port: %s" % redisport)
print("Using redis db: %s" % redisdb)

print("-------------------------------------------------------")

r = redis.Redis(host=redishost, port=redisport, db=redisdb)

data = {}


def  get_env():

  myenv = {}
  try:
    myenv['KALM_QEMU_HOST'] = os.getenv("KALM_QEMU_HOST")
    myenv['KALM_QEMU_SSL'] = os.getenv("KALM_QEMU_SSL")
  except KeyError as key_error:
    print(key_error)
    raise SystemExit("Unable to get environment variables.")
  return myenv

def list_vms():
    prettyllog("libvirt", "init", "service", "redis" "ok", "000" , "updating servers", severity="INFO")
    conn = libvirt.open('qemu:///system')
    if conn is None:
        print('Failed to open connection to qemu:///system')
        return

    try:
        # Get the list of domains (VMs)
        domains = conn.listDomainsID()
        if not domains:
            print('No active domains (VMs) found.')
        else:
            print('List of active domains (VMs):')
            for domain_id in domains:
                domain = conn.lookupByID(domain_id)
                print(f'ID: {domain.ID()}, Name: {domain.name()}, State: {domain.info()[0]}')
    finally:
        # Close the connection
        conn.close()

def main():
    list_vms()

