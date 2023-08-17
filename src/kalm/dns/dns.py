import requests
import subprocess
import json
import os
import redis
import sys
import time 
import json
import subprocess
import xmltodict
import re
import netifaces

from ..common import prettyllog



def convert_to_json(xml_output):
    # Convert XML to dictionary
    xml_dict = xmltodict.parse(xml_output)

    # Convert dictionary to JSON
    json_output = json.dumps(xml_dict, indent=4)
    return json_output

def get_virsh_xmldump(domain):
    # Run virsh xmldump command
    command = ["virsh", "dumpxml", domain]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    return output.decode("utf-8")

def get_domains():
    command = ["virsh", "list", "--id"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    mylist =  output.decode("utf-8").split("\n")
    mylist = list(filter(lambda x: x != "", mylist))
    return mylist

def get_dhcp_leases(network_name, mac_address):
    # Run virsh net-dhcp-leases command
    command = ["virsh", "net-dhcp-leases", network_name]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    for line in output.decode("utf-8").split("\n"):
        if mac_address in line:
          ipaddress = extract_ip_address(line)
          if ipaddress != None:
              return ipaddress


def extract_ip_address(line):
    # Regular expression pattern for matching an IP address
    pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"

    # Search for the IP address in the line
    match = re.search(pattern, line)
    if match:
        return match.group()
    else:
        return None


def get_network_id(network):
    # Run virsh net-info command for the default network
    command = ["virsh", "net-info", network]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    output_str = output.decode("utf-8")

    # Extract the network ID from the output
    match = re.search(r"UUID:\s+(\S+)", output_str)
    if match:
        return match.group(1)
    else:
        return None


# Specify the domain name or ID










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

def set_env():
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

  os.environ['KALM_DNS_DOMAIN'] = domain
  os.environ['KALM_DNS_URL'] = url
  os.environ['KALM_DNS_TYPE'] = dns_type
  os.environ['KALM_DNS_TOKEN'] = token
  return True

def get_zone_id():
  set_env()
  domain = os.getenv('KALM_DNS_DOMAIN')
  url=os.getenv('KALM_DNS_URL')
  dns_type=os.getenv('KALM_DNS_TYPE')
  token=os.getenv('KALM_DNS_TOKEN')
  if url.endswith("/"):
    url = url[:-1]
  zoneurl = url + "/api/v1/zones" 
  headers = {
    "Content-Type": "application/json",
    "Auth-API-Token": token
  }
  r = requests.get(zoneurl, headers=headers)
  if r.status_code != 200:
    print("Error: " + str(r.status_code))
    print(records)
    exit(1)
  
  records = r.content.decode("utf-8")
  zones = json.loads(records)['zones']
  for zone in zones:
    if zone['name'] == domain:
      return zone['id']
  return None
   
def get_records():
  set_env()
  domain = os.getenv('KALM_DNS_DOMAIN')
  url=os.getenv('KALM_DNS_URL')
  dns_type=os.getenv('KALM_DNS_TYPE')
  token=os.getenv('KALM_DNS_TOKEN')
  headers = {
    "Content-Type": "application/json",
    "Auth-API-Token": token
  }

  if url.endswith("/"):
    url = url[:-1]
  zoneid = get_zone_id()
  if zoneid != None:
    recordurl = url + "/api/v1/records?zone_id=" + zoneid 
    #https://dns.hetzner.com/api/v1/records?zone_id=${ZONEID}"
    
    r = requests.get(recordurl, headers=headers)
    if r.status_code != 200:
      print("Error: " + str(r.status_code))
      print(records)
      exit(1)
    records = r.content.decode("utf-8")
    records = json.loads(records)['records']
    for record in records:
      if record['type'] == 'A':
         print(record['value'] + " " + record['name'])
    return True


def list_interfaces():
  interfaces = netifaces.interfaces()
  for interface in interfaces:
    if interface == "lo":
      continue
    addrs = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in addrs:
      ipv4_info = addrs[netifaces.AF_INET]
      for addr in ipv4_info:
        print(f"Interface: {interface}")
        print(f"  IPv4 Address: {addr['addr']}")

def list_dns():
    list_interfaces()
    print(get_my_ipify()  )
    print(get_my_ethernet_interfaces())
    set_env()
    get_records()
    return True

def get_my_ip():
  myip = get_my_ethernet_interfaces()
  return myip

def get_my_ipify():
  r = requests.get("https://api.ipify.org")
  if r.status_code != 200:
    print("Error: " + str(r.status_code))
    exit(1)
  return r.content.decode("utf-8")

def get_my_ethernet_interfaces():
  interfaces = netifaces.interfaces()
  for interface in interfaces:
    if interface.startswith("eth"):
      return interface
  return None

   
def sync_my_system():
  set_env()
  domain = os.getenv('KALM_DNS_DOMAIN')
  url=os.getenv('KALM_DNS_URL')
  prettyllog("manage", "dns", domain, "new", "000", "sync my system")
  dns_type=os.getenv('KALM_DNS_TYPE')
  token=os.getenv('KALM_DNS_TOKEN')
  myip = get_my_ip()
  if myip is None:
    print("Error: can't get my ip")
    exit(1)
  if url.endswith("/"):
    url = url[:-1]
  zoneurl = url + "/api/v1/zones"


def add_dns_record(record, record_type="A", record_value=""):
  domain = os.getenv('KALM_DNS_DOMAIN')
  url=os.getenv('KALM_DNS_URL')
  prettyllog("manage", "dns", record, "new", "000", "add dns record %s" % (record))
  dns_type=os.getenv('KALM_DNS_TYPE')

  token=os.getenv('KALM_DNS_TOKEN')
  if token == None:
    print("You need to setup KALM_DNS_TOKEN")  

  zoneurl = url + "/zones"
  headers = {
    "Content-Type": "application/json",
    "Auth-API-Token": token
  }
  r = requests.get(zoneurl, headers=headers)
  if r.status_code != 200:
    print("Error: " + str(r.status_code))
    exit(1)
  records = r.json()
  for zone in records['zones']:
    if zone['name'] == domain:
      print("found domain")
      zone_id = zone['id']
      print(zone_id)
      url = url + "/records"
      print(url)
      data = {
        "name": record,
        "ttl": 600,
        "type": record_type,
        "value": record_value,
        "zone_id": zone_id
      }
      r = requests.post(url, headers=headers, json=data)
      print(r.content)
      if r.status_code != 200:
        print("Error: " + str(r.status_code))

def virtlib(args):
   set_env()
   print("virtlib")
   print("get domains")
   print("get ip address")
   print("get network")
   print(args)
   
   domain_ids = get_domains()
   for domain_id in domain_ids:
    prettyllog("manage", "dns", domain_id, "new", "000", "add dns record %s" % (domain_id))
    xml_output = get_virsh_xmldump(domain_id)
    json_output = convert_to_json(xml_output)
    json_dict = json.loads(json_output)
    domain_name = json_dict["domain"]["name"]
    prettyllog("manage", "dns", domain_name, "new", "000", "add dns record %s" % (domain_name))
    ip4s = []
    try:
      mac_address = json_dict["domain"]["devices"]["interface"]["mac"]["@address"]
      network = json_dict["domain"]["devices"]["interface"]["source"]["@network"]
      ipaddress = get_dhcp_leases(network, mac_address)
      netid = get_network_id(network)
      prettyllog("manage", "dns", domain_name, "new", "000", "add dns record %s" % (domain_name + "." + network + ".openknowit.com"))
      ipaddress = { "domain_name" : domain_name, "network" : network, "ipaddress" : ipaddress }
      print(ipaddress)

      ip4s.append(ipaddress)
    except:
      try:
        for interface in json_dict["domain"]["devices"]["interface"]:
            mac_address = interface["mac"]["@address"]
            network = interface["source"]["@network"]
            ipaddress = get_dhcp_leases(network, mac_address)
            netid = get_network_id(network)
            prettyllog("manage", "dns", domain_name, "new", "000", "add dns record %s" % (domain_name + "." + network + ".openknowit.com")) 
            ipaddress = { "domain_name" : domain_name, "network" : network, "ipaddress" : ipaddress }
            ip4s.append(ipaddress)
      except:
        print("no network")

    for ip4 in ip4s:
      print(ip4)
      prettyllog("manage", "dns", domain_name, "new", "000", "add dns record %s" % (ip4["domain_name"] + "." + ip4["network"] + ".openknowit.com"))
      add_dns_record(ip4["domain_name"], "A", ip4["ipaddress"])

