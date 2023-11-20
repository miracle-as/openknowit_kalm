import requests
import os
from ..common import prettyllog
import pprint
import json


debug = True





import os
import requests

def login():
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    user = os.getenv('KALM_SEMAPHORE_USER')
    password = os.getenv('KALM_SEMAPHORE_PASSWORD')
    url = f"{baseurl}/api/auth/login"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'auth': user,
        'password': password
    }

    # Create a session
    session = requests.Session()

    # Make the login request
    response = session.post(url, headers=headers, json=data)
    if response.status_code == 204:
        # Successful request
        prettyllog("semaphore", "Init", "login", "ok",  response.status_code , "login successful", severity="INFO")
        return session  # Return the session for subsequent requests
    else:
        # Failed request
        prettyllog("semaphore", "Init", "login", "error", response.status_code , "login failed", severity="FAIL")
        return None

def get_project(session):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    project_url = f"{baseurl}/api/projects"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use the session for the request
    response = session.get(project_url, headers=headers)
    if response.status_code == 200:
        # Successful request
        projects = response.json()
        # map prokects by name
        projects_by_name = {}
        for project in projects:
            projects_by_name[project['name']] = project
            if debug:
                prettyllog("semaphore", "get", project['name'], "ok", response.status_code , "loadning projects", severity="DEBUG")
        prettyllog("semaphore", "get", "project", "ok", response.status_code , "loadning projects", severity="INFO")
        return projects_by_name
    else:
        # Failed request
        prettyllog("semaphore", "get", "project", "error", response.status_code , "loadning projects", severity="FAIL")

def get_inventory(session, project_id):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    inventory_url = f"{baseurl}/api/project/{project_id}/inventory?sort=name&order=asc' "  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use the session for the request
    response = session.get(inventory_url, headers=headers)
    if response.status_code == 200:
        # Successful request
        inventory = response.json()
        # map prokects by name
        inventory_by_name = {}
        for item in inventory:
            inventory_by_name[item['name']] = item
            if debug:
                prettyllog("semaphore", "get", item['name'], "ok", response.status_code , "loadning inventory", severity="DEBUG")
        prettyllog("semaphore", "get", "inventory", "ok", response.status_code , "loadning inventory", severity="INFO")
        return inventory_by_name
    else:
        # Failed request
        prettyllog("semaphore", "get", "inventory", "error", response.status_code , "loadning inventory", severity="FAIL")

def check_env():
    if (os.getenv('KALM_SEMAPHORE_URL') == None):
        prettyllog("semaphore", "Init", "env", "error", 1 , "KALM_SEMAPHORE_URL not set", severity="FAIL")
        return 1
    else:
        prettyllog("semaphore", "Init", "env", "ok", 0 , "KALM_SEMAPHORE_URL set", severity="INFO")
        return 0

def read_config():
    f = open("etc/kalm/kalm.json", "r")
    mainconf = json.load(f)
    f.close()
    for key in mainconf:
        pprint.pprint(key)
    pprint.pprint(mainconf)

    return 0

 # Example: Get a list of your projects

def main():
    read_config()
    state = {}
    session = login()
    if session:
        projects = get_project(session)
        for project in projects:
            projectname = projects[project]['name']
            state[projectname] = {}
            state[projectname]['project'] = projects[project]
            state[projectname]['inventory'] = {}
            inventory = get_inventory(session, projects[project]['id'])
            for item in inventory:
                itemname = inventory[item]['name']
                state[projectname]['inventory'][itemname] = {}
                state[projectname]['inventory'][itemname]['item'] = inventory[item]
                prettyllog("semaphore", "main", item, "ok", 0 , "item", severity="INFO")

    for state_project in state:
        for state_item in state[state_project]['inventory']:
            pprint.pprint(state[state_project]['inventory'])
            prettyllog("semaphore", "main", state_item, "ok", 0 , "item", severity="INFO")


        



    return 0
