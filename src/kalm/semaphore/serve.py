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
        prettyllog("state", "Init", "login", "ok",  response.status_code , "login successful", severity="INFO")
        return session  # Return the session for subsequent requests
    else:
        # ERRORed request
        prettyllog("state", "Init", "login", "error", response.status_code , "login failed", severity="ERROR")
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
                prettyllog("state", "get", project['name'], "ok", response.status_code , "loadning projects", severity="DEBUG")
        prettyllog("state", "get", "project", "ok", response.status_code , "loadning projects", severity="INFO")
        return projects_by_name
    else:
        # Failed request
        prettyllog("state", "get", "project", "error", response.status_code , "loadning projects", severity="ERROR")

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
                prettyllog("state", "get", item['name'], "ok", response.status_code , "loadning inventory", severity="DEBUG")
        prettyllog("state", "get", "inventory", "ok", response.status_code , "loadning inventory", severity="INFO")
        return inventory_by_name
    else:
        # Failed request
        prettyllog("state", "get", "inventory", "error", response.status_code , "loadning inventory", severity="ERROR")

def check_env():
    envok = True
    myenv = {}
    known_git_types = ['github', 'gitlab', 'bitbucket', 'gitea', 'gogs']
    if (os.getenv('KALM_SEMAPHORE_URL') == None):
        prettyllog("check", "Init", "env", "error", 1 , "KALM_SEMAPHORE_URL not set", severity="ERROR")
        envok = False
    else:
        myenv['KALM_SEMAPHORE_URL'] = os.getenv('KALM_SEMAPHORE_URL')
        prettyllog("check", "Init", "env", "ok", 0 , "KALM_SEMAPHORE_URL set", severity="INFO")

    if (os.getenv('KALM_SEMAPHORE_USER') == None):
        prettyllog("check", "Init", "env", "error", 1 , "KALM_SEMAPHORE_USER not set", severity="ERROR")
        envok = False
    else:       
        myenv['KALM_SEMAPHORE_USER'] = os.getenv('KALM_SEMAPHORE_USER')
        prettyllog("check", "Init", "env", "ok", 0 , "KALM_SEMAPHORE_USER set", severity="INFO")

    if (os.getenv('KALM_SEMAPHORE_PASSWORD') == None):
        prettyllog("check", "Init", "env", "error", 1 , "KALM_SEMAPHORE_PASSWORD not set", severity="ERROR")
        envok = False
    else:
        myenv['KALM_SEMAPHORE_PASSWORD'] = os.getenv('KALM_SEMAPHORE_PASSWORD')
        prettyllog("check", "Init", "env", "ok", 0 , "KALM_SEMAPHORE_PASSWORD set", severity="INFO")

    if (os.getenv('KALM_GIT_TYPE') == None):
        prettyllog("check", "Init", "env", "error", 1 , "KALM_GIT_TYPE not set", severity="ERROR")
        envok = False
    elif (os.getenv('KALM_GIT_TYPE') not in known_git_types):
        prettyllog("check", "Init", "env", "error", 1 , "KALM_GIT_TYPE not set %s " % known_git_types, severity="ERROR")
        envok = False
    else:
        myenv['KALM_GIT_TYPE'] = os.getenv('KALM_GIT_TYPE')
        prettyllog("check", "Init", "env", "ok", 0 , "KALM_GIT_TYPE set", severity="INFO")
    return envok, myenv



def read_config():
    f = open("etc/kalm/kalm.json", "r")
    mainconf = json.load(f)
    prettyllog("conf", "Init", "main","main configuration", 0 , "Getting main config", severity="INFO")
    f.close()
    subconf = {}

    # check if automation is enabled for semaphore
    for subproject in mainconf['subprojects']:
        if subproject['engine'] == 'semaphore':
            subconf[subproject['name']] = subproject
            prettyllog("conf", "Init", "subpropject", subproject['name'] , "000", "Getting subproject config", severity="DEBUG")
    return True, mainconf, subconf

    


    


 # Example: Get a list of your projects

def check_project(projectname, env):
    # we need to check if the project exists in git
    # if not we need to create it
    # if it exists we need to check if it exists in semaphore
    # if not we need to create it
    if env['KALM_GIT_TYPE'] == 'gitea':
        from ..gitea.gitea import get_git_token

    
    get_git_token()


    




def main():
    semaphore, mainconf, subprojects = read_config()
    organization = mainconf['organisation']['name']
    mysubprojects = mainconf['subprojects']
    checkenv, env = check_env()
    if not checkenv:
        prettyllog("semaphore", "main", "config", "error", 1 , "No semaphore config found", severity="ERROR")
        exit(1)

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

    missings = {}
    for subproject in subprojects:
        if subproject in state:
            prettyllog("semaphore", "main", subproject, "ok", 0 , "subproject", severity="INFO")
        else:
            prettyllog("semaphore", "main", subproject, "missing", 1 , "subproject", severity="DEBUG")
            missings[subproject] = subprojects[subproject]

    orphans = {}    
    for state_project in state:
        if state_project in subprojects or state_project == organization:
            prettyllog("semaphore", "main", state_project, "ok", 0 , "subproject", severity="INFO")
        else:
            prettyllog("semaphore", "main", state_project, "orphan", 1 , "subproject", severity="WARNING")
            orphans[state_project] = state[state_project]


    for missing in missings:
        prettyllog("project", "create", missing, "Preparing to create project", 000 , "subproject", severity="DEBUG")
        # create project
        check_project(missing, env)
        




    return 0

