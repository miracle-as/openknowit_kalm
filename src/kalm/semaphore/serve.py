import requests
import os
from ..common import prettyllog

def check_env():
    print("check_env")
    if (os.getenv('KALM_SEMAPHORE_URL') == None):
        print("KALM_SEMAPHORE_URL not set")
        return 1
    
def get_projects():
    print("get_projects")
    projects = requests.get(os.getenv('KALM_SEMAPHORE_URL') + "/api/v4/projects")
    return 0


def main():
    print("serve")
    if check_env():
        prettyllog("check_env", "KALM_SEMAPHORE_URL", "not set", "set KALM_SEMAPHORE_URL", "error", "error")


        
    return 0
