import requests
import subprocess
import json
import os
import redis
import sys
import libvirt
import time 

def init_redis():
  r = redis.Redis()
  r.set('foo', 'bar')
  value = r.get('foo')
  if value == b'bar':
    print("Redis is working")
    return r
  else:
    print("Redis is not working")
    exit(1)

  
def list_dns():
    print("list dns")
    domain = os.getenv('KALM_DNS_DOMAIN')
    url=os.getenv('KALM_DNS_URL')
    dns_type=os.getenv('KALM_DNS_TYPE')
    token=os.getenv('KALM_DNS_TOKEN')
    url = url + "/api/v1/dnsrecords" 

def sync_dns(args)