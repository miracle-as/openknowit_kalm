import os
def usage():
  # export the environment variables
  print("export KALM_NETBOX_URL=\"\"")
  print("export KALM_NETBOX_TOKEN=\"\"")
  print("export KALM_NETBOX_SSL=\"\"")


def  get_env():
  myenv = {}
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

  return myenv
