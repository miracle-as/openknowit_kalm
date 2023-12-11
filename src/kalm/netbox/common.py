import os
import json


def usage():
  # export the environment variables
  print("export KALM_NETBOX_URL=\"\"")
  print("export KALM_NETBOX_TOKEN=\"\"")
  print("export KALM_NETBOX_SSL=\"\"")


def  get_env():
  myenv = {}
  myenv['subproject'] = {}
  try:
    myenv['KALM_NETBOX_URL'] = os.getenv("KALM_NETBOX_URL")
    myenv['KALM_NETBOX_TOKEN'] = os.getenv("KALM_NETBOX_TOKEN")
    myenv['KALM_NETBOX_SSL'] = os.getenv("KALM_NETBOX_SSL", "false")
  except KeyError as key_error:
    print(key_error)
    usage()
    raise SystemExit("Unable to get environment variables.")
  if myenv['KALM_NETBOX_URL'] == None:
    usage()
    raise SystemExit("Unable to get environment variables.")
  if myenv['KALM_NETBOX_TOKEN'] == None:
    usage()
    raise SystemExit("Unable to get environment variables.")
  
  if myenv['KALM_NETBOX_SSL'] == "false" or myenv['KALM_NETBOX_SSL'] == "False" or myenv['KALM_NETBOX_SSL'] == "FALSE" or myenv['KALM_NETBOX_SSL'] == "no" or myenv['KALM_NETBOX_SSL'] == "NO" or myenv['KALM_NETBOX_SSL'] == "No":
    myenv['KALM_NETBOX_SSL'] = False
  else:
    myenv['KALM_NETBOX_SSL'] = True
  if myenv['KALM_NETBOX_URL'][-1] == "/":
    myenv['KALM_NETBOX_URL'] = myenv['KALM_NETBOX_URL'][:-1]

  f = open("etc/kalm/kalm.json", "r")
  kalmconfig = json.loads(f.read())
  f.close()
  for key in kalmconfig:
    myenv[key] = kalmconfig[key]

  mysubprojects = []
  for subproject in myenv['subprojects']:
    filename = "etc/kalm/conf.d/" + subproject['name'] + ".json"
    print(filename)
    try: 
      ff =  open(filename, "r")
      ff.close()
    except:
      errorstring = "unable to open " + filename
      print(errorstring)
# create file
#{
#  "subproject": {
#    "description": "The zabbix agent installation and configuration"
#  },
#  "inventory": {
#    "globalvars": {
#      "zabbix_server": "zabbix.it.rm.dk"
#    }
#  },
#  "hosts": [
#    "exrhel001.it.rm.dk",
#    "exrhel002.it.rm.dk"
#  ]
#}
      description = "The %s project" % subproject['name']
      data = {
    "subproject": {
        "description": description
    },
    "inventory": {
        "globalvars": {
        }
    },
    "hosts": [
    ]
}
      with open(filename, "w") as file:
        json.dump(data, file, indent=2)

    ff =  open(filename, "r")
    subprojectconfig = json.loads(ff.read())
    print(subprojectconfig)
    myenv['subproject'][subproject['name']] = subprojectconfig
    ff.close()







  return myenv
