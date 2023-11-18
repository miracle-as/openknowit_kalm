import requests
import os

def check_env():
    print("check_env")
    if (os.getenv('KALM_SEMAPHORE_URL') == None):
        print("KALM_SEMAPHORE_URL not set")
        return 1


def serve():
    print("serve")
    if not check_env():
        print("check_env failed")
        SystemExit(1)
        
    print("check_env ok")
    print("KALM_SEMAPHORE_URL: " + os.getenv('KALM_SEMAPHORE_URL'))

    url = os.getenv('KALM_SEMAPHORE_URL') + "/api/v2/projects"
    print(url)
    r = requests.get(url)
    print(r.status_code)
    print(r.headers)
    print(r.text)
    print(r.json)


        
    return 0
