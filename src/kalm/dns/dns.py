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


def env_check():
  print("env check")
  domain = os.getenv('KALM_DNS_DOMAIN')
  url=os.getenv('KALM_DNS_URL')
  dns_type=os.getenv('KALM_DNS_TYPE')
  token=os.getenv('KALM_DNS_TOKEN')
  if domain is None:
    print("Error: KALM_DNS_DOMAIN is not set")
    exit(1)
  if url is None:
    print("Error: KALM_DNS_URL is not set")
    exit(1)
  if dns_type is None:
    print("Error: KALM_DNS_TYPE is not set")
    exit(1)
  if token is None:
    print("Error: KALM_DNS_TOKEN is not set")
    exit(1)
  print("KALM_DNS_DOMAIN: " + domain)
  print("KALM_DNS_URL: " + url)
  print("KALM_DNS_TYPE: " + dns_type)
  print("KALM_DNS_TOKEN: " + token)
  

def list_dns():
    print("list dns")
    domain = os.getenv('KALM_DNS_DOMAIN')
    url=os.getenv('KALM_DNS_URL')
    dns_type=os.getenv('KALM_DNS_TYPE')
    token=os.getenv('KALM_DNS_TOKEN')
    url = url + "/api/v1/dnsrecords" 

def sync_dns(args):
  print("sync dns")
  domain = os.getenv('KALM_DNS_DOMAIN')
  url=os.getenv('KALM_DNS_URL')
  dns_type=os.getenv('KALM_DNS_TYPE')
  token=os.getenv('KALM_DNS_TOKEN')
  url = url + "/dns"
  r = requests.get(url, headers={'Authorization': 'Bearer ' + token})
  if r.status_code != 200:
    print("Error: " + str(r.status_code))
    exit(1)
  data = r.json()
  for record in data:
    print(record)
    if record['type'] == 'A':
      print("A record")
    if record['name'] == '@':
      print("root record")

def add_dns(args):
  print("add dns")
  domain = os.getenv('KALM_DNS_DOMAIN')
  url=os.getenv('KALM_DNS_URL')
  dns_type=os.getenv('KALM_DNS_TYPE')
  token=os.getenv('KALM_DNS_TOKEN')
  url = url + "/dns"
  r = requests.get(url, headers={'Authorization': 'Bearer ' + token})
  if r.status_code != 200:
    print("Error: " + str(r.status_code))
    exit(1)
  data = r.json()
  for record in data:
    print(record)
    if record['type'] == 'A':
      print("A record")
    if record['name'] == '@':
      print("root record")

   
   
   
