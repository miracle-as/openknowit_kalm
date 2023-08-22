import requests
import subprocess
import json
import os
import redis
import sys
import time 


def versions(args):
    package = args.action[1]
    r = requests.get("https://pypi.org/pypi/{}/json".format(package))
    if r.status_code == 200:
        data = r.json()
        print("Package: {}".format(package))
        print("Latest version: {}".format(data["info"]["version"]))
        print("Releases:")
        for version in data["releases"]:
            print(" - {}".format(version))
    else:
        print("Package not found")



def get_pip_freeze_output():
    try:
        pip_freeze_output = subprocess.check_output(['pip', 'freeze'], universal_newlines=True)
        return pip_freeze_output
    except subprocess.CalledProcessError as e:
        return str(e)

def poetry_dependensies():
  pip_freeze_output = get_pip_freeze_output()
  lines = pip_freeze_output.strip().split("\n")
  formatted_dependencies = []
  for line in lines:
    package, version = line.split("==")
    formatted_dependencies.append(f"{package} = \"{version}\"")
  formatted_output = "\n".join(formatted_dependencies)
  print(formatted_output)