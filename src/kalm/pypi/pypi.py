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
