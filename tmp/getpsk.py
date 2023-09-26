import requests
import json

# Replace these with your Zabbix server information and credentials
zabbix_url = 'https://zabbix.openknowit.com/api_jsonrpc.php'
zabbix_user = 'Admin'
zabbix_password = 'ixj90j2s'
auth_token = "9e39c4605ff25083f230b22ccaf1c18128fb8123a502abddeaad73e0b6cff0b8"

# Define the hostname for which you want to retrieve PSK information
hostname = 'Linux server'

# Authenticate and get a session token
auth_data = {
    'jsonrpc': '2.0',
    'method': 'user.login',
    'params': {
        'user': zabbix_user,
        'password': zabbix_password,
    },
    'id': 1,
}

# Make the authentication request
auth_response = requests.post(zabbix_url, data=json.dumps(auth_data), headers={'Content-Type': 'application/json'})

# Parse the authentication response and get the session token
auth_result = auth_response.json()
if 'result' in auth_result:
    auth_token = auth_result['result']

# Get host information by hostname
host_info_data = {
    'jsonrpc': '2.0',
    'method': 'host.get',
    'params': {
        'output': ['hostid'],
        'filter': {
            'host': [hostname],
        },
    },
    'auth': auth_token,
    'id': 2,
}

# Make the host information request
host_info_response = requests.post(zabbix_url, data=json.dumps(host_info_data), headers={'Content-Type': 'application/json'})

# Parse the host information response to get the host ID
host_info_result = host_info_response.json()
if 'result' in host_info_result and len(host_info_result['result']) > 0:
    host_id = host_info_result['result'][0]['hostid']

    # Now that you have the host ID, you can retrieve host interface information
    host_interface_data = {
        'jsonrpc': '2.0',
        'method': 'hostinterface.get',
        'params': {
            'output': 'extend',
            'hostids': host_id,
        },
        'auth': auth_token,
        'id': 3,
    }

    # Make the host interface information request
    host_interface_response = requests.post(zabbix_url, data=json.dumps(host_interface_data), headers={'Content-Type': 'application/json'})

    # Parse the host interface information response to get PSK information
    host_interface_result = host_interface_response.json()
    if 'result' in host_interface_result and len(host_interface_result['result']) > 0:
        try:
            psk = host_interface_result['result'][0]['tls_psk_identity']
            print(f"PSK for host '{hostname}': {psk}")
        except:
            psk = None
            print(f"PSK for host '{hostname}': {psk}")
    else:
        print(f"No PSK information found for host '{hostname}'")
else:
    print(f"Host '{hostname}' not found in Zabbix")

# Don't forget to handle errors and exceptions in a production environment

