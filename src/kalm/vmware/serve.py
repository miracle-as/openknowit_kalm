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


r = redis.Redis(host='localhost', port=6379, db=0)

data = {}


def connect(env):
    try:
        if env['KALM_VMWARE_SSL'] == "disable":
            prettyllog("vsphere", "init", "Connect to vcenter", "start", "000" , "Connecting without ssl verify", severity="INFO")
            myhost = env['KALM_VMWARE_URL'].replace("https://", "")
            pprint.pprint(myhost)
            try:
                service_instance = SmartConnect(host=myhost,
                                            user=env['KALM_VMWARE_USERNAME'],
                                            pwd=env['KALM_VMWARE_PASSWORD'],
                                            disableSslCertValidation=True)
            except IOError as io_error: 
                print(io_error)
                raise SystemExit("Unable to connect to host with supplied credentials.")
        else:
            prettyllog("vsphere", "init", "Connect to vcenter", "start", "000" , "Connecting with ssl verify", severity="INFO")
            service_instance = SmartConnect(host=myhost,
                                            user=env['KALM_VMWARE_USERNAME'],
                                            pwd=env['KALM_VMWARE_PASSWORD'])
        #atexit.register(Disconnect, service_instance)
    except IOError as io_error:
        print(io_error)
    if not service_instance:
        raise SystemExit("Unable to connect to host with supplied credentials.")
    return service_instance


def  get_env():

  myenv = {}
  try:
    myenv['KALM_VMWARE_URL'] = os.getenv("KALM_VMWARE_URL")
    myenv['KALM_VMWARE_USERNAME'] = os.getenv("KALM_VMWARE_USERNAME")
    myenv['KALM_VMWARE_PASSWORD'] = os.getenv("KALM_VMWARE_PASSWORD")
    myenv['KALM_VMWARE_SSL'] = os.getenv("KALM_VMWARE_SSL")
  except KeyError as key_error:
    print(key_error)
    raise SystemExit("Unable to get environment variables.")
  
  
  return myenv


# Function to get a list of VMs

def get_cluster_list(content):
    limit = 20
    cluster_list = []
    cluster_details = {}
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.ClusterComputeResource], True
    )
    # promnt items in container
    pprint.pprint(container.view)

    for cluster in container.view:
        if limit == 0:
            break
        limit -= 1
        cluster_list.append(cluster.name)
        cluster_details[cluster.name] = {}
        cluster_details[cluster.name]['configuration'] = cluster.configuration
        cluster_details[cluster.name]['datastore'] = cluster.datastore
        cluster_details[cluster.name]['host'] = cluster.host
        cluster_details[cluster.name]['network'] = cluster.network
        cluster_details[cluster.name]['summary'] = cluster.summary
    return cluster_list, cluster_details

def get_vm_details(content, vmname):
    vm_details = {}
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    for vm in container.view:
        if vm.name == vmname:
            vm_details[vm.name] = {}
            vm_details[vm.name]['config'] = vm.summary.config
            vm_details[vm.name]['guest'] = vm.summary.guest
            vm_details[vm.name]['runtime'] = vm.summary.runtime
            vm_details[vm.name]['storage'] = vm.summary.storage
            vm_details[vm.name]['summary'] = vm.summary
            return vm_details

def get_vm_list(content):
    vm_list = []
    vm_details = {}
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    for vm in container.view:
        vm_list.append(vm.name)
        vm_details[vm.name] = {}
        #vm_details[vm.name]['config'] = vm.summary.config
        #vm_details[vm.name]['guest'] = vm.summary.guest
        #vm_details[vm.name]['runtime'] = vm.summary.runtime
        #vm_details[vm.name]['storage'] = vm.summary.storage
        #vm_details[vm.name]['summary'] = vm.summary
    return vm_list, vm_details

def vm2dict(datacenter, cluster, host, vm, summary):
    # If nested folder path is required, split into a separate function
    vmname = vm.summary.config.name
    data[datacenter][cluster][host][vmname]['folder'] = vm.parent.name
    data[datacenter][cluster][host][vmname]['mem'] = summary['mem']
    data[datacenter][cluster][host][vmname]['diskGB'] = summary['diskGB']
    data[datacenter][cluster][host][vmname]['cpu'] = summary['cpu']
    data[datacenter][cluster][host][vmname]['path'] = summary['path']
    data[datacenter][cluster][host][vmname]['net'] = summary['net']
    data[datacenter][cluster][host][vmname]['ostype'] = summary['ostype']
    data[datacenter][cluster][host][vmname]['state'] = summary['state']
    data[datacenter][cluster][host][vmname]['annotation'] = summary['annotation']


def data2json(raw_data, args):
    with open(args.jsonfile, 'w') as json_file:
        json.dump(raw_data, json_file)    

def get_nics(guest):
    nics = {}
    for nic in guest.net:
        if nic.network:  # Only return adapter backed interfaces
            if nic.ipConfig is not None and nic.ipConfig.ipAddress is not None:
                nics[nic.macAddress] = {}  # Use mac as uniq ID for nic
                nics[nic.macAddress]['netlabel'] = nic.network
                ipconf = nic.ipConfig.ipAddress
                i = 0
                nics[nic.macAddress]['ipv4'] = {}
                for ip in ipconf:
                    if ":" not in ip.ipAddress:  # Only grab ipv4 addresses
                        nics[nic.macAddress]['ipv4'][i] = ip.ipAddress
                        nics[nic.macAddress]['prefix'] = ip.prefixLength
                        nics[nic.macAddress]['connected'] = nic.connected
                    i = i+1
    return nics


def vmsummary(summary, guest):
    vmsum = {}
    config = summary.config
    net = get_nics(guest)
    vmsum['mem'] = str(config.memorySizeMB / 1024)
    vmsum['diskGB'] = str("%.2f" % (summary.storage.committed / 1024**3))
    vmsum['cpu'] = str(config.numCpu)
    vmsum['path'] = config.vmPathName
    vmsum['ostype'] = config.guestFullName
    vmsum['state'] = summary.runtime.powerState
    vmsum['annotation'] = config.annotation if config.annotation else ''
    vmsum['net'] = net

    return vmsum



# Connect to the vCenter server
def connect_to_vcenter(debug=True):
    prettyllog("vsphere", "init", "Connect to vcenter", "start", "000" , "Connecting", severity="INFO")
    myenv = get_env()
    service_instance = connect(myenv)
    if debug:
        print(parse_service_instance(service_instance))
    if not service_instance:
        prettyllog("vsphere", "init", "Connect to vcenter", "error", "000" , "Fail to Connect", severity="ERROR")
        return None
    prettyllog("vsphere", "init", "Connect to vcenter", "ok", "000" , "Connected", severity="INFO")
    return service_instance.RetrieveContent()


def get_obj(content, vimtype, name = None):
    return [item for item in content.viewManager.CreateContainerView(
        content.rootFolder, [vimtype], recursive=True).view]


def parse_service_instance(si):
    """
    Print some basic knowledge about your environment as a Hello World
    equivalent for pyVmomi
    """

    content = si.RetrieveContent()
    pprint.pprint(content.about)
    print("")
    print("Content:")
    print(" - content.about                 = %s" % content.about)
    print(" - content.about.apiType         = %s" % content.about.apiType)
    print(" - content.about.instanceUuid    = %s" % content.about.instanceUuid)
    print(" - content.about.osType          = %s" % content.about.osType)
    print(" - content.about.productLineId   = %s" % content.about.productLineId)
    
    object_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [], True)
    for obj in object_view.view:
        print(obj)
    object_view.Destroy()
    return 0



# MAIN
# We are serving vspere and we need an infinite loop
prettyllog("vsphere", "init", "service", "ok", "000" , "starting server", severity="INFO")

orphans = []
while True:
    content = connect_to_vcenter()
    vm_list, vm_details = get_vm_list(content)
    totalservers = len(vm_list)
    for vm in vm_list:
        knownservers = r.keys("kalm:vmware:*:known")
        detailedservers = r.keys("kalm:vmware:*:details")

        knownservercount = len(knownservers)
        detailedservercount = len(detailedservers)
        prettyllog("vsphere", "get", vm, "check", "000" , "loadning servers (totalservers: %s known: %s updated %s )" % (totalservers, knownservercount, detailedservercount), severity="INFO")
        detailkey = "kalm:vmware:" + vm + ":details"
        knownkey = "kalm:vmware:" + vm + ":known"
        timestamp = time.time()
        get = r.get(detailkey)
        if get is None:
            prettyllog("vsphere", "get", vm, "new", "000" , "loadning servers", severity="CHANGE")
            vm_details = get_vm_details(content, vm)
            r.set(detailkey, str(vm_details), ex=36000)
            r.set(knownkey, str(timestamp))
        else:
            prettyllog("vsphere", "get", vm, "known", "000" , "loadning servers", severity="INFO")
            r.set(knownkey, str(timestamp))







#       hosts = cluster.host  # Variable to make pep8 compliance
#        for host in hosts:  # Iterate through Hosts in the Cluster
#            hostname = host.summary.config.name
#            # Add VMs to data dict by config name
#            data[datacenter.name][cluster.name][hostname] = {}
#            vms = host.vm
#            for vm in vms:  # Iterate through each VM on the host
#                vmname = vm.summary.config.name
#                data[datacenter.name][cluster.name][hostname][vmname] = {}
#                summary = vmsummary(vm.summary, vm.guest)
#                vm2dict(datacenter.name, cluster.name, hostname, vm, summary)





  