import requests
import json
import os
import base64
import xml.etree.ElementTree as ET

netbox_url = os.environ.get('NETBOX_URL')
netbox_token = os.environ.get('NETBOX_TOKEN')

headers = {
    'Authorization': 'Token ' + netbox_token,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

def get_netbox_data(url):
    response = requests.get(url, headers=headers)
    return response.json()

def read_file(file):
    with open(file, 'r') as myfile:
        data = myfile.read()
    return data

def refresh_netbox():
    config = read_file('/etc/kalm/netbox.json')
    config = json.loads(config)
    for key in config:
        print(key)
        



   
