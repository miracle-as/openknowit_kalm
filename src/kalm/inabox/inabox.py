import requests
import subprocess
import json
import os
import redis
import sys
import time 


from ..common import prettyllog


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

  
  
    




def list_inabox():
    print("list inabox")

def check_dns_resolution(hostname, ip4):
    command = ['dig', '+short', hostname]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        dns_output = result.stdout.strip()
        if dns_output:
            print(dns_output)
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

def setupdns(hostname, ip4):
  data = { "hostname": hostname, "ip_address": ip4 }
  url = "https://dns.openknowit.com/dns"
  headers = {"Content-Type": "application/json"}
  response = requests.post(url, json=data, headers=headers)

  if response.status_code == 200:
    print("DNS entry added successfully.")
    return True
  else:
    print(f"Failed to add DNS entry. Status code: {response.status_code}")
    return False




def checkservice(hostname, ip):
  if check_dns_resolution(hostname, ip):
    print(f"The DNS resolution for {hostname} is correct.")
  else:
     print(f"The DNS resolution for {hostname} is incorrect or unavailable.")
     setupdns('inabox', ip)
     time.sleep(5)
     if check_dns_resolution(hostname, ip):
       print(f"The DNS resolution for {hostname} is correct.")
     else:
       print(f"The DNS resolution for {hostname} is incorrect or unavailable.")
       exit(1)
  return 0

def read_config():
  try:
    with open("./inabox.json", "r") as inabox_config:
      inabox_config = json.load(inabox_config)
      print(inabox_config)
  except:
    print("Failed to read config file")
    exit(1)

  try:
      iso_path = inabox_config['iso_path']
      preseed_path = inabox_config['preseed_path']
  except:
      print("Failed to read iso or preseed path")
      inabox_config['iso_path'] = "iso/debian10.iso"
      inabox_config['preseed_path'] = "preseed.cfg"
  try:
        size = inabox_config['vm_size']
        if size in ['small', 'medium', 'large']:
          print("We have a valid vm size")
        else:
          print("We dont have a valid vm size")
          inabox_config['vm_size'] = "small"
  except:
        inabox_config['vm_size'] = "small"
      
  try: 
        network = inabox_config['vm_network']
        if network in ['inabox', 'inabox2']:
          print("We have a valid network")  
        else:
          print("We dont have a valid network")
          inabox_config['vm_network'] = "inabox"
  except:
        inabox_config['vm_network'] = "inabox"
  return inabox_config
def check_ssh(hostname):
  command = ['ssh', hostname, 'echo', 'hello']
  try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    ssh_output = result.stdout.strip()
    if ssh_output == "hello":
      return True
    else:
      return False
  except subprocess.CalledProcessError:
    return False
  
def check_the_hosts(hosts, meta_data):
    processes = {}
    for member in hosts:
        print(member)
        vm_name = member['hostname']
        if check_if_we_have_a_vm(vm_name):
          print("We have a vm:" + vm_name ) 
          if is_vm_running(vm_name):
            print("We have a running vm:" + vm_name)
            if check_ssh(vm_name):
              print("We have ssh")  

        else:
          print("We dont have a vm")
          size="small"
          print("Creating a vm")
          process = create_virtual_server(vm_name,size,  meta_data)
          print("Waiting for process to finish")
          print(process.pid)
          processes[vm_name] = process

    for process in processes.values():
      print("Waiting for process to finish")
      print(process.pid)
      process.wait()




      print("---------------")

def  check_if_we_have_a_vm(vm_name, ):
  command = ['virsh', 'list', '--all']
  try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    virsh_output = result.stdout.strip()
    if vm_name in virsh_output:
      return True
    else:
      return False
  except subprocess.CalledProcessError:
    return False

def download_file(url, filename):
  print("Downloading file:" + url + " to " + filename)
  r = requests.get(url, allow_redirects=True)
  try:
    open(filename, 'wb').write(r.content)
    return True
  except:
    return False
  
def print_status():
  print("Status:")
  print("-------")
  print("DNS: OK")
  print("VM: OK")
  print("SSH: OK")
  print("-------"
        )

def mb_to_bytes(mb):
  bytes = mb * 1024 * 1024
  return bytes 

def spawn_process(command, stdout_file, stderr_file):
    process = subprocess.Popen(command, start_new_session=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process

def create_virtual_server(vm_name, size="medium", os="debian10" , meta_data):
    if os == "debian10":
      return create_virtual_server_debian(vm_name, size, meta_data)
    else:
      print("Unknown os")
      exit(1)
      

def create_virtual_server_debian(hostname, size, meta_data):
    # check if we have a preseedfile 
    print("check if we have a preseedfile")
    if os.path.exists(meta_data['preseed_path']):
      print("Found preseed.cfg")
    else:
      print("No preseed.cfg found")
      if download_file("https://artifacts.openknowit.com/files/inabox/debian10.preseed.cfg", meta_data['preseed_path']):
        print("Downloaded preseed.cfg")
      else:
        print("Failed to download preseed.cfg")
        exit(1)
    print("check if we have a iso")
    if os.path.exists(meta_data['iso_path']):
      print("Found iso")
    else:
      print("No iso found")
      print("Downloading iso")
      if download_file("https://artifacts.openknowit.com/files/inabox/debian10.iso", meta_data['iso_path']):
        print("Downloaded iso")
      else: 
        print("Failed to download iso")
        exit(1)
      
    # Construct the virt-install command with preseeding options
    mysize = 50
    disksize = "size=" + str(mysize)
    vcpus = 4 
    command = [
       "virt-install", 
       "--install","debian11",
       "--name" , hostname,
       "--memory", "8192",
       "--vcpus", "6",
       "--disk", disksize,
       "--initrd-inject" , "./preseed.cfg",
       "--extra-args", "debian/priority=critical", 
       "--noautoconsole",
       "--noreboot"
    ]

    # Execute the virt-install command
    print("command:" + str(command))
    
    process = spawn_process(command, "logs/" + hostname + ".stdout", "logs" + hostname + ".stderr")
    return process


def is_vm_running(vm_name):
  command = ['virsh', 'list']
  try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    virsh_output = result.stdout.strip()
    if vm_name in virsh_output:
      return True
    else:
      return False
  except subprocess.CalledProcessError:
    return False
  
def start_vm(vm_name):
  command = ['virsh', 'start', vm_name]
  try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    virsh_output = result.stdout.strip()
    if vm_name in virsh_output:
      return True
    else:
      return False
  except subprocess.CalledProcessError:
    return False
  


   
def rancher_inabox():
  r = init_redis()
  conn = init_connection()

  print("Starting rancher in a box")
  get_servers(r, conn)

  
  print("Starting inabox")
  myconf = read_config()
  myfqdn = myconf['service']+ '.' + myconf['domain']
  print("Checking DNS resolution for " + myfqdn + " and " + myconf['ip4'])
        

  checkservice(myfqdn, myconf['ip4']
               )
  print(myconf['domain'])
  hosts  = myconf['hosts']
  try:
    check_the_hosts(hosts, myconf)
  except:
    print("Failed to check the hosts")
    exit(1)
  print_status()
  return 0

def ansible_role_inabox():
  import os

def create_role_directory():
    role_name = input("Enter the name of the role: ")
    role_dir = f"roles/{role_name}"
    os.makedirs(f"{role_dir}/tasks")
    os.makedirs(f"{role_dir}/handlers")
    os.makedirs(f"{role_dir}/templates")
    os.makedirs(f"{role_dir}/vars")
    os.makedirs(f"{role_dir}/defaults")
    os.makedirs(f"{role_dir}/meta")
    os.makedirs(f"{role_dir}/files")
    os.makedirs(f"{role_dir}/tests")

    readme_file = f"{role_dir}/README.md"
    with open(readme_file, "w") as f:
        f.write(f"# {role_name} Role")

    meta_file = f"{role_dir}/meta/main.yml"
    with open(meta_file, "w") as f:
        f.write("---\n# Dependencies (if any)")

    print(f"Directory structure for the role '{role_name}' created successfully!")


def k3s_inabox():
  r = init_redis()
  conn = init_connection()
  print("Starting k3s in a box")
  get_servers(r, conn)
  print("Starting inabox")
  myconf = read_config()
  myfqdn = myconf['service']+ '.' + myconf['domain']
  print("Checking DNS resolution for " + myfqdn + " and " + myconf['ip4'])
  checkservice(myfqdn, myconf['ip4'])
  print(myconf['domain'])
  hosts  = myconf['hosts']
  try:
    check_the_hosts(hosts, myconf)
  except:
    print("Failed to check the hosts")
    exit(1)
  print_status()
  return 0

def up_inabox():
  r = init_redis()
  conn = init_connection()
  print("Starting up inabox")
  get_servers(r, conn)
  print("Starting inabox")
  myconf = read_config()
  myfqdn = myconf['service']+ '.' + myconf['domain']
  print("Checking DNS resolution for " + myfqdn + " and " + myconf['ip4'])
  checkservice(myfqdn, myconf['ip4'])
  print(myconf['domain'])
  hosts  = myconf['hosts']
  try:
    check_the_hosts(hosts, myconf)
  except:
    print("Failed to check the hosts")
    exit(1)
  print_status()
  return 0

def ansible_automation_platform():
  prettyllog("inabox", "start", "ansible_automation_platform", "ansible_automation_platform", "200", "Starting ansible automation platform") 
  r = init_redis()
  conn = init_connection()
  print("Starting ansible automation platform")
  get_servers(r, conn)
  print("Starting inabox")
  myconf = read_config()
  myfqdn = myconf['service']+ '.' + myconf['domain']
  print("Checking DNS resolution for " + myfqdn + " and " + myconf['ip4'])
  checkservice(myfqdn, myconf['ip4'])
  print(myconf['domain'])
  hosts  = myconf['hosts']
  print(hosts)
  try:
    check_the_hosts(hosts, myconf)
  except:
    print("Failed to check the hosts")
    exit(1)
  print_status()
  return 0
