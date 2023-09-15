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
import paramiko
from ..common import prettyllog
from . import cloudflare



def get_default_gateway():
    try:
        # Use the socket library to get the default route
        default_route = socket.gethostbyname(socket.gethostname())
        
        # Use the subprocess module to execute 'ip route' command and parse the output
        result = subprocess.check_output(['ip', 'route'], universal_newlines=True)
        lines = result.split('\n')
        
        for line in lines:
            if default_route in line:
                gateway = line.split(' ')[2]
                return gateway
    except Exception as e:
        print("An error occurred:", e)
        return None
    
def get_my_ip(defaut=True):
  if defaut:
    dgw = get_default_gateway()
    return dgw
  else:
    return None
  
def default(args):
  print(get_default_gateway())



def get_ssh_host_key_fingerprint(hostname, port=22):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname, port=port)
        host_key = ssh_client.get_transport().get_remote_server_key()
        fingerprint = ":".join([f"{b:02x}" for b in host_key.get_fingerprint()])
        return fingerprint
    except paramiko.AuthenticationException:
        return "Authentication failed"
    except paramiko.SSHException as e:
        return str(e)
    except Exception as e:
        return str(e)
    finally:
        ssh_client.close()

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

def get_dhcp_leases():
    command = ["virsh", "net-list", "--name"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    mynetworks =  output.decode("utf-8").split("\n")
    myleases = {}
    for mynetwork in mynetworks:
      if mynetwork == "":
        continue
      # Run virsh net-dhcp-leases command
      command = ["virsh", "net-dhcp-leases", mynetwork ]
      process = subprocess.Popen(command, stdout=subprocess.PIPE)
      output, _ = process.communicate()
      for line in output.decode("utf-8").split("\n"):
        if "ipv4" in line:
          ipaddress = line.split("   ipv4       ")[1].split(" ")[0].split("/")[0]
          macaddress = line.split("   ipv4       ")[0].split("   ")[1]
          if ipaddress != None:
              data = {
                "ipaddress" : ipaddress,
                "network" : mynetwork
              }
              myleases[macaddress] = data
    return myleases

def extract_mac_address(line):
    # Regular expression pattern for matching an IP address
    pattern = r"(\d{1,2}:\d{1,2}:\d{1,2}:\d{1,2}:\d{1,2}:\d{1,2})"
    match = re.search(pattern, line)
    if match:
        return match.group()
    else:
        return None

def extract_ip_address(line):
    # Regular expression pattern for matching an IP address
    pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
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
  zoneurl = url + "/zones" 
  headers = {
    "Content-Type": "application/json",
    "Auth-API-Token": token
  }
  r = requests.get(zoneurl, headers=headers)

  if r.status_code != 200:
    print("Error: " + str(r.status_code))
    print(r.content)
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
  prettyllog("manage", "dns", domain, "new", "000", "get zone id %s" % (domain))
  zoneid = get_zone_id()
  if zoneid != None:
    recordurl = url + "/records?zone_id=" + zoneid 
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
    return records


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

def clean(args):
  set_env()
  print(get_records())
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

def get_dns_record(record):
  domain = os.getenv('KALM_DNS_DOMAIN')
  url=os.getenv('KALM_DNS_URL')
  prettyllog("manage", "dns", record, "new", "000", "add dns record %s" % (record))
  dns_type=os.getenv('KALM_DNS_TYPE')

  token=os.getenv('KALM_DNS_TOKEN')
  if token == None:
    print("You need to setup KALM_DNS_TOKEN")  
  
  


def add_dns_record(record, record_type="A", record_value="", ttl=600, update=True):
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
    print("Error: " + str(r.content))

    print("Error: " + str(r.status_code))
    exit(1)
  records = r.json()
  for zone in records['zones']:
    if zone['name'] == domain:
      zone_id = zone['id']
      url = url + "/records"
      data = {
        "name": record,
        "ttl": ttl,
        "type": record_type,
        "value": record_value,
        "zone_id": zone_id
      }
      r = requests.post(url, headers=headers, json=data)
      if r.status_code != 200:
        print("Error: " + str(r.content))
        print("Error: " + str(r.status_code))

def check_dns_record(hostname):
  records = get_records()
  for record in records:
    if record['name'] == hostname:
      return True
  return False

def get_dns_record(hostname):
  records = get_records()
  for record in records:
    if record['name'] == hostname:
      return record
  return False

def delete_dns_record(hostname):
  set_env()
  domain = os.getenv('KALM_DNS_DOMAIN')
  url=os.getenv('KALM_DNS_URL')
  prettyllog("manage", "dns", hostname, "new", "000", "delete dns record %s" % (hostname))
  dns_type=os.getenv('KALM_DNS_TYPE')
  token=os.getenv('KALM_DNS_TOKEN')
  if token == None:
    print("You need to setup KALM_DNS_TOKEN")  


def libvirt_leases():
  prettyllog("manage", "dns", "libvirt", "new", "000", "libvirt")
  myleases = get_dhcp_leases()
  mymacs = list(myleases.keys())
  mac2ip = {}
  for mac in mymacs:
    if mac is not None:
      mac2ip[mac] = myleases[mac]['ipaddress']  
  return mac2ip

def register():
  prettyllog("manage", "dns", "register", "new", "000", "register")
  domain_name = os.environ.get("HOSTNAME")
  network = "default"
  ipaddress = get_my_ip()
  myitem = { "name" : domain_name, "type": "A", "proxied": "False", "ttl": 300, "network" : network, "ipaddress" : ipaddress }
  if os.environ.get("KALM_DNS_TYPE") == "cloudflare":
    if(cloudflare.check_access()):
      prettyllog("manage", "dns", domain_name, "new", "000", "add dns record %s" % (domain_name + "." + network + ".openknowit.com"))
      result = cloudflare.add_record(myitem)
      print(result)
  return True

def virtlightning():
  prettyllog("manage", "dns", "virtlightning", "new", "000", "virtlightning")  
  set_env()
  vlfile = os.getenv('KALM_VIRT_LIGHTNING_FILE')
  if vlfile == None:
    print("You need to setup KALM_VIRT_LIGHTNING_FILE")  
    exit(1)
  vldir = os.getenv('KALM_VIRT_LIGHTNING_DIR')
  if vldir == None:
    print("You need to setup KALM_VIRT_LIGHTNING_DIR")  
    exit(1)
  vlfullpath = vldir + "/" + vlfile
  if not os.path.isfile(vlfullpath):
    print("Error: " + vlfullpath + " not found")
    exit(1)
  prettyllog("manage", "dns", "virtlightning", "new", "000", "virtlightning file found %s" % (vlfullpath))
  command = ["virt-lightning", "status" ]
  process = subprocess.Popen(command, stdout=subprocess.PIPE)
  output, _ = process.communicate()
  mylist =  output.decode("utf-8").split("\n")
  mylist = list(filter(lambda x: x != "", mylist))
  prettyllog("manage", "dns", "virtlightning", "new", "000", "virtlightning list %s" % (mylist))
  for myitem in mylist:
    myname = myitem.split(" ")[1]
    myip = myitem.split('@')[1].split(' ')[0]
    myos = myitem.split('[')[1].split(']')[0]
    mynetwork = "default"
    print(myname + " " + myip + " " + myos)
    myitem = { "name" : myname, "type": "A", "proxied": "False", "ttl": 300, "network" : mynetwork, "ipaddress" : myip }
    if os.environ.get("KALM_DNS_TYPE") == "cloudflare":
      if(cloudflare.check_access()):
        prettyllog("manage", "dns", myname, "new", "000", "add dns record %s" % (myname +  ".openknowit.com"))
        result = cloudflare.add_record(myitem)



  

def libvirt(args):
  prettyllog("manage", "dns", "libvirt", "new", "000", "libvirt")
  myleases = libvirt_leases()
  #open a file for writing in /tmp
  # open a file for writing
  lines = []
  set_env()
  domain_ids = get_domains()
  prettyllog("manage", "dns", "libvirt", "new", "000", "get domains ids")
  ip4s = []
  for domain_id in domain_ids:
    prettyllog("manage", "dns", domain_id, "new", "000", "START: add dns record %s" % (domain_id))
    xml_output = get_virsh_xmldump(domain_id)
    json_output = convert_to_json(xml_output)
    json_dict = json.loads(json_output)
    domain_name = json_dict["domain"]["name"]
    prettyllog("manage", "dns", domain_name, "new", "000", "add dns record %s" % (domain_name))
    try:
      mac_address = json_dict["domain"]["devices"]["interface"]["mac"]["@address"]
    except:
      try:
        mac_address = json_dict["domain"]["device"]["interface"][0]["mac"]["@address"]
      except:
        try:
          mac_address = json_dict["domain"]["device"]["interfaces"][0]["mac"]["@address"]
        except:
          mac_address = "None"   
          try:
            mac_address = json_dict["domain"]["devices"]["interfaces"][0]["mac"]["@address"]
          except:
            mac_address = "None"   
         


    prettyllog("manage", "macadress", domain_name, "new", "000", "Macaddress %s" % (mac_address))
    try:
      network = json_dict["domain"]["devices"]["interface"]["source"]["@network"]
    except:
      network = "None"
    prettyllog("manage", "network", domain_name, "new", "000", "network %s" % (network))
    
    try:
      ipaddress = myleases[mac_address]
    except:
      ipaddress = "None"
    prettyllog("manage", "ipadress", domain_name, "new", "000", "IP address %s" % (ipaddress))
    try:
      netid = get_network_id(network)
    except:
      netid = "None"
    prettyllog("manage", "ipadress", domain_name, "new", "000", "Network id :  %s" % (netid))
    myitem = { "name" : domain_name, "type": "A", "proxied": "False", "ttl": 300, "network" : network, "ipaddress" : ipaddress }
    if os.environ.get("KALM_DNS_TYPE") == "cloudflare":
      if(cloudflare.check_access()):
        prettyllog("manage", "dns", domain_name, "new", "000", "add dns record %s" % (domain_name + "." + network + ".openknowit.com"))
        result = cloudflare.add_record(myitem)

  return True