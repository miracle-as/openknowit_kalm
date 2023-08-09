import requests
import os
import urllib3
import hashlib


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

inthevaulturl = os.getenv("INTHEVAULT_URL", "https://inthevault.openknowit.com/api/v1")  
inthevaulttoken = os.getenv("INTHEVAULT_TOKEN", "inthevault_token")

def list():
    url = inthevaulturl + "/list"
    try:
        # Make a GET request to the API endpoint
        response = requests.get(url, verify=False)

        # Check the response status code
        if response.status_code == 200:
            # API call was successful
            print(response.json())
        else:
            # API call failed
            print(f"API call failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle connection or request error
        print(f"An error occurred: {e}")

def save_file(file):
    md5 = create_md5sum_file(file)
    url = inthevaulturl + "/" + md5
    try:
        # Make a GET request to the API endpoint
        response = requests.get(url, verify=False)

        # Check the response status code
        if response.status_code == 200:
            # API call was successful
            print(response.json())
        else:
            # API call failed
            print(f"API call failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # File is unknown upload it
        print(f"An error occurred: {e}")
        url = inthevaulturl + "/save_file"
        try:
          # Make a GET request to the API endpoint
          response = requests.get(url, verify=False)
          # Check the response status code
          if response.status_code == 200:
            # API call was successful
            print(response.json())
          else:
            # API call failed
            print(f"API call failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
        # Handle connection or request error
          print(f"An error occurred: {e}")

def create_md5sum_file(file):
    md5sum = hashlib.md5(open(file,'rb').read()).hexdigest()
    return md5sum

def create_sha256sum_file(file):
    sha256sum = hashlib.sha256(open(file,'rb').read()).hexdigest()
    return sha256sum






def read_file(file):
    filename = file
    open_file = open(filename, "r")
    read_file = open_file.read()
    print(read_file)
    open_file.close()
    