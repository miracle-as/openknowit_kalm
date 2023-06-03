import requests
import subprocess
import json
import os
import sys
import libvirt

conn = libvirt.open()

if conn is None:
    print('Failed to open connection to the hypervisor.')
    exit(1)

def list_inabox():
    print("list inabox")

def get_servers():
  domains = conn.listAllDomains()
  print('List of KVM virtual machines:')
  for domain in domains:
    name = domain.name()
    state, _ = domain.state()
    state_str = libvirt.VIR_DOMAIN_STATE_LOOKUP[state][0]
    print(f'Name: {name}, State: {state_str}')
  conn.close()
  return domains




def check_dns_resolution(hostname):
    command = ['dig', '+short', hostname]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        dns_output = result.stdout.strip()
        if dns_output:
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

def checkservice():
  hostname = 'inabox.openknowit.com'
  if check_dns_resolution(hostname):
    print(f"The DNS resolution for {hostname} is correct.")
  else:
     print(f"The DNS resolution for {hostname} is incorrect or unavailable.")
     setupdns('inabox', '88.99.58.240')
     os.sleep(5)
     if check_dns_resolution(hostname):
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
    for group in hosts.keys():
      print("Checking group:" + group)
      for memeber in hosts[group]['members']:
        vm_name = memeber['hostname']
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

def create_virtual_server(hostname, size, meta_data):
    # check if we have a preseedfile 
    if os.path.exists(meta_data['preseed_path']):
      print("Found preseed.cfg")
    else:
      print("No preseed.cfg found")
      if download_file("https://artifacts.openknowit.com/files/inabox/debian10.preseed.cfg", meta_data['preseed_path']):
        print("Downloaded preseed.cfg")
      else:
        print("Failed to download preseed.cfg")
        exit(1)

    if os.path.exists(meta_data['iso_path']):
      print("Found iso")
    else:
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
  print("Starting rancher in a box")
  get_servers()
  
  print("Starting inabox")
  checkservice()
  myconf = read_config()
  print(myconf['domain'])
  hosts  = myconf['hosts']
  try:
    check_the_hosts(hosts, myconf)
  except:
    print("Failed to check the hosts")
    exit(1)
  print_status()


  
  return 0


 