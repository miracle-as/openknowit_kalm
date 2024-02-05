import requests
import os
from ..common import prettyllog
from ..gitea.git import clone_git_project
from ..netbox.netbox import get_netbox_inventory_from_tag
from ..netbox.netbox import get_netbox_master_inventory


import pprint
import json

import pprint
import json 
import tempfile
import git

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
        # ERRORed request
        prettyllog("semaphore", "Init", "login", "error", response.status_code , "login failed", severity="ERROR")
        return None
    
def crete_user(session, user):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    user_url = f"{baseurl}/api/users"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use the session for the request
    response = session.post(user_url, headers=headers, json=user)
    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", user['username'], "ok", response.status_code , "create user", severity="INFO")
        return response.json()
    else:
        # Failed request
        prettyllog("semaphore", "create", user['username'], "error", response.status_code , "create user", severity="ERROR")

def get_user(session):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    user_url = f"{baseurl}/api/users"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use the session for the request
    response = session.get(user_url, headers=headers)
    if response.status_code == 200:
        # Successful request
        users = response.json()
        # map users by username
        users_by_username = {}
        for user in users:
            users_by_username[user['username']] = user
            if debug:
                prettyllog("semaphore", "get", user['username'], "ok", response.status_code , "loadning users", severity="DEBUG")
        prettyllog("semaphore", "get", "user", "ok", response.status_code , "loadning users", severity="INFO")
        return users_by_username
    else:
        # Failed request
        prettyllog("semaphore", "get", "user", "error", response.status_code , "loadning users", severity="ERROR")

def create_team(session, team):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    team_url = f"{baseurl}/api/teams"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use the session for the request
    response = session.post(team_url, headers=headers, json=team)
    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", team['name'], "ok", response.status_code , "create team", severity="INFO")
        return response.json()
    else:
        # Failed request
        prettyllog("semaphore", "create", team['name'], "error", response.status_code , "create team", severity="ERROR")

def get_team(session):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    team_url = f"{baseurl}/api/teams"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use the session for the request
    response = session.get(team_url, headers=headers)
    if response.status_code == 200:
        # Successful request
        teams = response.json()
        # map teams by name
        teams_by_name = {}
        for team in teams:
            teams_by_name[team['name']] = team
            if debug:
                prettyllog("semaphore", "get", team['name'], "ok", response.status_code , "loadning teams", severity="DEBUG")
        prettyllog("semaphore", "get", "team", "ok", response.status_code , "loadning teams", severity="INFO")
        return teams_by_name
    else:
        # Failed request
        prettyllog("semaphore", "get", "team", "error", response.status_code , "loadning teams", severity="ERROR")

def create_team_member(session, team_id, team_member):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    team_member_url = f"{baseurl}/api/team/{team_id}/members"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use the session for the request
    response = session.post(team_member_url, headers=headers, json=team_member)
    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", team_member['username'], "ok", response.status_code , "create team member", severity="INFO")
        return response.json()
    else:
        # Failed request
        prettyllog("semaphore", "create", team_member['username'], "error", response.status_code , "create team member", severity="ERROR")

def create_key(session, key):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    key_url = f"{baseurl}/api/keys"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use the session for the request
    response = session.post(key_url, headers=headers, json=key)
    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", key['name'], "ok", response.status_code , "create key", severity="INFO")
        return response.json()
    else:
        # Failed request
        prettyllog("semaphore", "create", key['name'], "error", response.status_code , "create key", severity="ERROR")

def get_repositories(session, project_id):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    repository_url = f"{baseurl}/api/project/{project_id}/repositories"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    # Use the session for the request
    response = session.get(repository_url, headers=headers)
    if response.status_code == 200:
        # Successful request
        repositories = response.json()
        # map repositories by name
        repositories_by_name = {}
        for repository in repositories:
            repositories_by_name[repository['name']] = repository
            if debug:
                prettyllog("semaphore", "get", repository['name'], "ok", response.status_code , "loadning repositories", severity="DEBUG")
        prettyllog("semaphore", "get", "repository", "ok", response.status_code , "loadning repositories", severity="INFO")
        return repositories_by_name
    else:
        # Failed request
        prettyllog("semaphore", "get", "repository", "error", response.status_code , "loadning repositories", severity="ERROR")

    
def create_project(session, project):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    project_url = f"{baseurl}/api/projects"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use the session for the request
    response = session.post(project_url, headers=headers, json=project)
    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", project['name'], "ok", response.status_code , "create project", severity="INFO")
        return response.json()
    else:
        # Failed request
        prettyllog("semaphore", "create", project['name'], "error", response.status_code , "create project", severity="ERROR")


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
        prettyllog("semaphore", "get", "project", "error", response.status_code , "loadning projects", severity="ERROR")

def update_inventory(session, project_id, inventory_id, inventory):
    prettyllog("semaphore", "update", inventory['name'], "ok", 0 , "Start update inventory ", severity="INFO")
    # check if inventory exists
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    inventory_url = f"{baseurl}/api/project/{project_id}/inventory/{inventory_id}"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    inventory['id'] = inventory_id
    response = session.put(inventory_url, headers=headers, json=inventory)
    if response.status_code == 204:
        # Successful request
        prettyllog("semaphore", "update", inventory['name'], "ok", response.reason , "update inventory", severity="INFO")
        return True
    elif response.status_code == 400:
        # Failed request
        prettyllog("semaphore", "update", inventory['name'], "error", response.status_code , "update inventory", severity="INFO")
        return True
            
            
    else:
        # Failed request
        prettyllog("semaphore", "update", inventory['name'], "error", response.status_code , "Start update inventory", severity="ERROR")
        return False

def create_inventory(session, project_id, inventory):
    prettyllog("semaphore", "create", inventory['name'], "ok", 0 , "create inventory", severity="INFO")
    # check if inventory exists

    myinv =  get_inventory(session, project_id, inventory['name'])
    print("---------------------------------------- DEBUG ------------------------INVENTORIES------------ %s " % inventory['name'])
    prettyllog("semaphore", "create", inventory['name'], "ok", 0 , "Check if the repo exists", severity="INFO")    
    myrepoexists = False
    try:
        if myinv[inventory['name']]:
            prettyllog("semaphore", "update", inventory['name'], "ok", 0 , "inventory already exists", severity="INFO")
            myrepoexists = True
    except:
        prettyllog("semaphore", "create", inventory['name'], "ok", 0 , "inventory does not exists", severity="INFO")
        myrepoexists = False

        
    if myrepoexists:
        myinvid = myinv[inventory['name']]['id']
        update_inventory(session, project_id, myinvid, inventory)
        return True
    else:
        prettyllog("semaphore", "create", inventory['name'], "ok", 0 , "Create new inventory", severity="INFO")
        baseurl = os.getenv('KALM_SEMAPHORE_URL')
        inventory_url = f"{baseurl}/api/project/{project_id}/inventory"  # Adjust the URL as needed
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
    # Use the session for the request
        response = session.post(inventory_url, headers=headers, json=inventory)
        pprint.pprint(response.reason)
        pprint.pprint(response.status_code)
    
        if response.status_code == 201:
        # Successful request
            prettyllog("semaphore", "create", inventory['name'], "ok", response.status_code , "Successfully created", severity="INFO")
            return response.json()
        else:
            # Failed request
            prettyllog("semaphore", "create", inventory['name'], "error", response.status_code , "Fail creating inventory", severity="ERROR")

def create_credential(session, project_id, credential):
    prettyllog("semaphore", "create", credential['name'], "ok", 0 , "create credential", severity="INFO")
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    credential_url = f"{baseurl}/api/project/{project_id}/keys"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    # Use the session for the request
    response = session.get(credential_url, headers=headers)
    if response.status_code == 200:
        known_keys = response.json()
        for key in known_keys:
            if key['name'] == credential['name']:
                prettyllog("semaphore", "create", credential['name'], "ok", response.status_code , "create credential", severity="INFO")
                return True
    else:
        # Failed request
        prettyllog("semaphore", "create", credential['name'], "error", response.status_code , "create credential", severity="DEBUG")

    response = session.post(credential_url, headers=headers, json=credential)
    if response.status_code == 204:
        # Successful request
        prettyllog("semaphore", "create", credential['name'], "ok", response.status_code , "create credential", severity="INFO")
        return True
    else:
        if response.status_code == 404:
            # Failed request
            prettyllog("semaphore", "create", credential['name'], "error", response.status_code , "create credential", severity="ERROR")
            return False

        # Failed request
        prettyllog("semaphore", "create", credential['name'], "error", response.status_code , "create credential", severity="ERROR")

def popoulate_inventory(session, project_id, inventory_id, inventory):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    inventory_url = f"{baseurl}/api/project/{project_id}/inventory/{inventory_id}"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    response = session.get(inventory_url, headers=headers)

    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", inventory['name'], "ok", response.status_code , "create inventory", severity="INFO")
    else:
        # Failed request
        prettyllog("semaphore", "create", inventory['name'], "error", response.status_code , "create inventory", severity="ERROR")
        return False
    
    inventorydata = response.json()
    inventorydata[''] = inventory

def get_semaphore_inventories(session, project_id):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    inventory_url = f"{baseurl}/api/project/{project_id}/inventory"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = session.get(inventory_url, headers=headers)
    if response.status_code == 201:
        # Successful request
        return response.json()
    elif response.status_code == 200:
        # Successful request
        return response.json()
    else:
        # Failed request
        pprint.pprint(response.status_code)
        pprint.pprint(response.reason)
        return False

def get_inventory(session, project_id, projectname):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    inventory_url = f"{baseurl}/api/project/{project_id}/inventory?sort=name&order=asc' "  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = session.get(inventory_url, headers=headers)
    if response.status_code == 200:
        # Successful request
        inventory = response.json()
        # map projects by name
        inventory_by_name = {}
        for item in inventory:
            prettyllog("semaphore", "get", item['name'], "ok", response.status_code , "loadning inventory", severity="INFO")
            inventory_by_name[item['name']] = item
            if debug:
                prettyllog("semaphore", "get", item['name'], "ok", response.status_code , "loadning inventory", severity="DEBUG")
        prettyllog("semaphore", "get", "inventory", "ok", response.status_code , "loadning inventory", severity="INFO")
        return inventory_by_name
    else:
        # Failed request
        prettyllog("semaphore", "get", "inventory", "error", response.status_code , "loadning inventory", severity="ERROR")
        return None

def check_env():
    envok = True
    myenv = {}
    known_git_types = ['github', 'gitlab', 'bitbucket', 'gitea', 'gogs']
    if (os.getenv('KALM_SEMAPHORE_URL') == None):
        prettyllog("semaphore", "Init", "env", "error", 1 , "KALM_SEMAPHORE_URL not set", severity="ERROR")
        envok = False
    else:
        myenv['KALM_SEMAPHORE_URL'] = os.getenv('KALM_SEMAPHORE_URL')
        prettyllog("semaphore", "Init", "env", "ok", 0 , "KALM_SEMAPHORE_URL set", severity="INFO")

    if (os.getenv('KALM_SEMAPHORE_USER') == None):
        prettyllog("semaphore", "Init", "env", "error", 1 , "KALM_SEMAPHORE_USER not set", severity="ERROR")
        envok = False
    else:       
        myenv['KALM_SEMAPHORE_USER'] = os.getenv('KALM_SEMAPHORE_USER')
        prettyllog("semaphore", "Init", "env", "ok", 0 , "KALM_SEMAPHORE_USER set", severity="INFO")

    if (os.getenv('KALM_SEMAPHORE_PASSWORD') == None):
        prettyllog("semaphore", "Init", "env", "error", 1 , "KALM_SEMAPHORE_PASSWORD not set", severity="ERROR")
        envok = False
    else:
        myenv['KALM_SEMAPHORE_PASSWORD'] = os.getenv('KALM_SEMAPHORE_PASSWORD')
        prettyllog("semaphore", "Init", "env", "ok", 0 , "KALM_SEMAPHORE_PASSWORD set", severity="INFO")

    if (os.getenv('KALM_GIT_TYPE') == None):
        prettyllog("semaphore", "Init", "env", "error", 1 , "KALM_GIT_TYPE not set", severity="ERROR")
        envok = False
    elif (os.getenv('KALM_GIT_TYPE') not in known_git_types):
        prettyllog("semaphore", "Init", "env", "error", 1 , "KALM_GIT_TYPE not set %s " % known_git_types, severity="ERROR")
        envok = False
    else:
        myenv['KALM_GIT_TYPE'] = os.getenv('KALM_GIT_TYPE')
        prettyllog("semaphore", "Init", "env", "ok", 0 , "KALM_GIT_TYPE set", severity="INFO")
    return envok, myenv



def read_config():
    f = open("etc/kalm/kalm.json", "r")
    mainconf = json.load(f)
    prettyllog("semaphore", "Init", "main","main configuration", 0 , "Getting main config", severity="INFO")
    f.close()
    subconf = {}

    # check if automation is enabled for semaphore
    for subproject in mainconf['subprojects']:
        if subproject['engine'] == 'semaphore':
            subconf[subproject['name']] = subproject
            try:
                sf = open("etc/kalm/conf.d/%s.json" % subproject['name'], "r")
                subconf[subproject['name']]['json'] = json.load(sf)
                prettyllog("semaphore", "Init", "subpropject", subproject['name'] , "000", "Getting subproject config", severity="INFO")
                sf.close()
            except:
                prettyllog("semaphore", "Init", "subpropject", subproject['name'] , "000", "Getting subproject config", severity="ERROR")
                [subproject['name']]['json'] = {}
                

            prettyllog("semaphore", "Init", "subpropject", subproject['name'] , "000", "Getting subproject config", severity="DEBUG")
    return True, mainconf, subconf

 # Example: Get a list of your projects

def check_project(projectname, env):
    # we need to check if the project exists in git
    # if not we need to create it
    # if it exists we need to check if it exists in semaphore
    # if not we need to create it
    if env['KALM_GIT_TYPE'] == 'gitea':
        from ..gitea.git import get_git_projects
        git_projects = get_git_projects()
        if git_projects == False:
            prettyllog("semaphore", "Check", "gitea", "error", 0 , "Git inaccesable ignoring git", severity="ERROR")
            return False
        else:
            git_project_names = []
            for git_project in git_projects:
                git_project_names.append(git_project['name'])
            if projectname in git_project_names:
                prettyllog("semaphore", "Check", projectname, "ok", 0 , "project exists in git", severity="INFO")
            # check if project exists in semaphore
            # if not create it
            # if it exists check if it has the correct settings
            # if not update it
            else:
                prettyllog("semaphore", "Create", projectname, "missing", 1 , "project missing in git", severity="WARNING")
                from ..gitea.git import create_git_project 
                project = {}
                project['name'] = projectname
                project['description'] = "kalm project"
                project['private'] = True
                project['auto_init'] = True

            # create project in git
                create_git_project(project)
            # create a temporary dir and clone the project
            prettyllog("semaphore", "Init", "clone", projectname , "000", "Cloning git", severity="DEBUG")
            configdata = clone_git_project(projectname)
            # create project in semaphore
            # create project in git
            # create project in semaphore
            # create project in awx
            # create project in vault
            # create project in dns
    else:
        prettyllog("project", "semaphore", projectname, "error", 1 , "git type not supported", severity="ERROR")
        exit(1)
def get_repository_id(session, project_id, reponame):
    repos = get_repositories(session, project_id)
    prettyllog("semaphore", "get", reponame, "ok", 0 , "get repository id", severity="INFO")
    repoid = None
    for repo in repos:
        if repo == reponame:
            repoid = repos[repo]['id']
            return repoid
    return repoid


def update_repository(session, project_id, reponame):
    print("---------------------------------------- DEBUG ------------------------UPDATE------------ %s " % reponame)
    repoid = get_repository_id(session, project_id, reponame)
    prettyllog("semaphore", "update", reponame, "ok", 0 , "update repository %s " % repoid, severity="INFO")
    try:
        repoid = repoids[reponame]['id']
    except:
        repoid = None
        return False
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    repo_prefix = os.getenv('KALM_GIT_PREFIX')
    repo_project = os.getenv('KALM_GIT_PROJECT')
    giturl = os.getenv('KALM_GIT_SSH') 
    repodata = {}
    repodata['name'] = reponame
    repodata['project_id'] = project_id
    repodata['git_url'] = "%s%s/%s%s.git" % (giturl, repo_project, repo_prefix, reponame)
    repodata['git_branch'] = "main"
    repodata['ssh_key_id'] = get_sshkey_id(session, project_id, "git")
    repo_url = f"{baseurl}/api/project/{project_id}/repositories/{repoid}"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = session.put(repo_url, headers=headers, json=repodata)
    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", repodata['name'], "ok", response.status_code , "create repository", severity="INFO")
        return response.json()
    elif response.status_code == 400:
        prettyllog("semaphore", "create", repodata['name'], "error", response.status_code , "update repository", severity="INFO")
        return True
    elif response.status_code == 204:
        prettyllog("semaphore", "create", repodata['name'], "ok", response.status_code , "update repository", severity="INFO")
        return True
    else:
        # Failed request
        prettyllog("semaphore", "create", repodata['name'], "error", response.status_code , "create repository", severity="ERROR")

#####################################################################################################################
#    Create Repository
#####################################################################################################################
           
def create_repository(session, project_id, reponame):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    giturl = os.getenv('KALM_GIT_SSH') 
    repo_prefix = os.getenv('KALM_GIT_PREFIX')
    repo_project = os.getenv('KALM_GIT_PROJECT')
    repodata = {}
    repodata['name'] = reponame
    repodata['project_id'] = project_id
    repodata['git_url'] = "%s%s/%s%s.git" % (giturl, repo_project, repo_prefix, reponame)
    repodata['git_branch'] = "main"
    repodata['ssh_key_id'] = get_sshkey_id(session, project_id, "git")
    repo_url = f"{baseurl}/api/project/{project_id}/repositories"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = session.post(repo_url, headers=headers, json=repodata)
    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", repodata['name'], "ok", response.status_code , "create repository", severity="INFO")
        return response.json()
    elif response.status_code == 400:
        prettyllog("semaphore", "create", repodata['name'], "error", response.status_code , "update repository", severity="INFO")
        return True
    elif response.status_code == 204:
        prettyllog("semaphore", "create", repodata['name'], "ok", response.status_code , "update repository", severity="INFO")
        return True
    else:
        # Failed request
        prettyllog("semaphore", "create", repodata['name'], "error", response.status_code , "create repository", severity="ERROR")

def get_repository(session, project_id, reponame):
    print("---------------------------------------- DEBUG --------------------iGET REPO---------------- %s" % reponame)
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    repo_url = f"{baseurl}/api/project/{project_id}/repositories?name=%s" % reponame  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = session.get(repo_url, headers=headers)
    if response.status_code == 200:
        # Successful request
        pprint.pprint(response.json())
        repositories = response.json()
        # map repositories by name
        repositories_by_name = {}
        for repository in repositories:
            repositories_by_name[repository['name']] = repository
            if debug:
                prettyllog("semaphore", "get", repository['name'], "ok", response.status_code , "loadning repositories", severity="DEBUG")
        prettyllog("semaphore", "get", "repository", "ok", response.status_code , "loadning repositories", severity="INFO")
        return 
        print("---------------------------------------- DEBUG --------------------iGET REPO---------------- %s" %  repositories_by_name)
    else:
        # Failed request
        prettyllog("semaphore", "get", "repository", "error", response.status_code , "loadning repositories", severity="ERROR")






def get_sshkey_id(session, project_id, sshkeyname):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    sshkey_url = f"{baseurl}/api/project/{project_id}/keys?name=%s" % sshkeyname  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = session.get(sshkey_url, headers=headers)
    if response.status_code == 200:
        # Successful request
        sshkey = response.json()
        myid = None
        for sshkey in response.json():
            if sshkey['name'] == sshkeyname:
                myid = sshkey['id']
                prettyllog("semaphore", "get", sshkeyname, "ok", response.status_code , "loadning sshkeys", severity="INFO")
        return myid
    else:
        # Failed request
        prettyllog("semaphore", "get", "sshkey", "error", response.status_code , "loadning sshkeys", severity="ERROR")

def get_templates(session, project_id):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    template_url = f"{baseurl}/api/project/{project_id}/templates"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = session.get(template_url, headers=headers)
    if response.status_code == 200:
        # Successful request
        templates = response.json()
        # map templates by name
        templates_by_name = {}
        for template in templates:
            templates_by_name[template['name']] = template
            if debug:
                prettyllog("semaphore", "get", template['name'], "ok", response.status_code , "loadning templates", severity="DEBUG")
        prettyllog("semaphore", "get", "template", "ok", response.status_code , "loadning templates", severity="INFO")
        return templates_by_name
    else:
        # Failed request
        prettyllog("semaphore", "get", "template", "error", response.status_code , "loadning templates", severity="ERROR")

def get_environments(session, project_id):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    environments_by_name = {}
    environment_url = f"{baseurl}/api/project/{project_id}/environments"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = session.get(environment_url, headers=headers)
    if response.status_code == 200:
        # Successful request
        environments = response.json()
        # map environments by name
        for environment in environments:
            environments_by_name[environment] = environment
            if debug:
                prettyllog("semaphore", "get", environment, "ok", response.status_code , "loadning environments", severity="DEBUG")
        prettyllog("semaphore", "get", "environment", "ok", response.status_code , "loadning environments", severity="INFO")
        return environments_by_name
    elif response.status_code == 404:
        # Failed request
        prettyllog("semaphore", "get", "environment", "error", response.status_code , "loadning environments", severity="INFO")
        return {}
    else:
        # Failed request
        prettyllog("semaphore", "get", "environment", "error", response.status_code , "loadning environments", severity="ERROR")
        return

def get_environment_id(session, project_id, environmentname):
    environments = get_environments(session, project_id)
    environmentid = None
    for environment in environments:
        if environment == environmentname:
            environmentid = environments[environment]['id']
            prettyllog("semaphore", "get", environmentname, "ok", 0 , "get environment id", severity="INFO")
    return environmentid

def get_views(session, project_id):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    view_url = f"{baseurl}/api/project/{project_id}/views"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use the session for the request
    response = session.get(view_url, headers=headers)
    if response.status_code == 200:
        # Successful request
        views = response.json()
        pprint.pprint(views)
        # map views by name
        views_by_name = {}
        for view in views:
            views_by_name[view['title']] = view
            if debug:
                prettyllog("semaphore", "get", view['title'], "ok", response.status_code , "loadning views", severity="DEBUG")
        prettyllog("semaphore", "get", "view", "ok", response.status_code , "loadning views", severity="INFO")
        return views_by_name
    else:
        # Failed request
        prettyllog("semaphore", "get", "view", "error", response.status_code , "loadning views", severity="ERROR")

def get_view_id(session, project_id, viewname):
    views = get_views(session, project_id)
    viewid = None
    for view in views:
        if view == viewname:
            viewid = views[view]['id']
            prettyllog("semaphore", "get", viewname, "ok", 0 , "get view id", severity="INFO")
    return viewid

def get_credentials(session, project_id):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    credential_url = f"{baseurl}/api/project/{project_id}/keys"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use the session for the request
    response = session.get(credential_url, headers=headers)
    if response.status_code == 200:
        # Successful request
        credentials = response.json()
        # map credentials by name
        credentials_by_name = {}
        for credential in credentials:
            credentials_by_name[credential['name']] = credential
            if debug:
                prettyllog("semaphore", "get", credential['name'], "ok", response.status_code , "loadning credentials", severity="DEBUG")
        prettyllog("semaphore", "get", "credential", "ok", response.status_code , "loadning credentials", severity="INFO")
        return credentials_by_name
    else:
        # Failed request
        prettyllog("semaphore", "get", "credential", "error", response.status_code , "loadning credentials", severity="ERROR")

def get_credential_id(session, project_id, credentialname):
    credentials = get_credentials(session, project_id)
    credentialid = None
    for credential in credentials:
        if credential == credentialname:
            credentialid = credentials[credential]['id']
            prettyllog("semaphore", "get", credentialname, "ok", 0 , "get credential id", severity="INFO")
    return credentialid
    

def get_inventory_id(session, project_id, inventoryname):
    inventories = get_semaphore_inventories(session, project_id)
    inventoryid = None
    for inventory in inventories:
        if inventory['name'] == inventoryname:
            inventoryid = inventory['id']
            prettyllog("semaphore", "get", inventoryname, "ok", 0 , "get inventory id", severity="INFO")
    return inventoryid



def update_template(session, project_id, template, subproject = None, inventory_id = "auto", repository_id = "auto", environment_id = "auto", view_id = "auto"):
    if inventory_id == "auto" and subproject != None:
        inventory_id = get_inventory_id(session, project_id, subproject )
    if repository_id == "auto" and subproject != None:
        repository_id = get_repository_id(session, project_id, subproject )
    if environment_id == "auto" and subproject != None:
        environment_id = get_environment_id(session, project_id, subproject )
    if view_id == "auto" and subproject != None:
        view_id = get_view_id(session, project_id, subproject )
    view_id = 0
    pprint.pprint(view_id)
    print("---------------------------------------- DEBUG ------------------------UPDATE------------ %s " % template['name'])
    prettyllog("semaphore", "update", template['name'], "ok", 0 , "update template", severity="INFO")
    playbook = "playbooks/%s.yml" % template['name']
    data = {
      "project_id": project_id,
      "inventory_id": inventory_id,
      "repository_id": repository_id,
      "environment_id": environment_id,
      "view_id": view_id,
      "name": template['name'],
      "playbook": playbook,
      "arguments": "[]",
      "description": template['description'],
      "allow_override_args_in_task": False,
      "limit": "limitall",
      "suppress_success_alerts": True,
      "survey_vars": [
      {
        "name": "mystringsurveyvar",
        "title": "thestringtitle",
        "description": "thestringdescriptio",
        "type": "String",
        "required": False
      }
      ]
    }
    mytemplateexists = False
    mytemplateid = None
    templates = get_templates(session, project_id)
    for mytemplate in templates:
        if mytemplate == template['name']:
            mytemplateexists = True
            mytemplateid = templates[mytemplate]['id']
    if mytemplateexists:
        prettyllog("semaphore", "update", template['name'], "ok", 0 , "template already exists", severity="INFO")
        baseurl = os.getenv('KALM_SEMAPHORE_URL')
        template_url = f"{baseurl}/api/project/{project_id}/templates/{mytemplateid}"  # Adjust the URL as needed
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = session.put(template_url, headers=headers, json=data)
        if response.status_code == 201:
            # Successful request
            prettyllog("semaphore", "update", template['name'], "ok", response.status_code , "update template", severity="INFO")
            return True
        elif response.status_code == 400:
            # Failed request
            prettyllog("semaphore", "update", template['name'], "error", response.status_code , "update template", severity="INFO")
            return True
        else:
            # Failed request
            prettyllog("semaphore", "update", template['name'], "error", response.status_code , "update template", severity="ERROR")
            return False

def create_template(session, project_id, template, subproject = None, inventory_id = "auto", repository_id = "auto", environment_id = "auto", view_id = "auto"):
    pprint.pprint(subproject)
    if inventory_id == "auto" and subproject != None:
        invname = "Unix Ansible Automation - %s" % (subproject)
        inventory_id = get_inventory_id(session, project_id, invname )
    if repository_id == "auto" and subproject != None:
        repository_id = get_repository_id(session, project_id, subproject )
    if environment_id == "auto" and subproject != None:
        environment_id = get_environment_id(session, project_id, subproject )
        pprint.pprint(environment_id)
        print("-------------------------------------")
    if view_id == "auto" and subproject != None:
        view_id = get_view_id(session, project_id, subproject )

    prettyllog("semaphore", "create", template['name'], "ok", 0 , "create template", severity="INFO")

    playbook = "playbooks/%s.yml" % template['name']
    templatedata = {
      "project_id": project_id,
      "inventory_id": inventory_id,
      "repository_id": repository_id,
      "environment_id": environment_id,
      "view_id": view_id,
      "name": template['name'],
      "playbook": playbook,
      "arguments": "[]",
      "description": template['description'],
      "allow_override_args_in_task": False,
      "limit": "limitall",
      "suppress_success_alerts": True,
      "survey_vars": [
      {
        "name": "mystringsurveyvar",
        "title": "thestringtitle",
        "description": "thestringdescriptio",
        "type": "String",
        "required": False
      }
      ]
    }
    mytemplateexists = False
    mytemplateid = None
    templates = get_templates(session, project_id)
    for mytemplate in templates:
        if mytemplate == template['name']:
            mytemplateexists = True
            mytemplateid = templates[mytemplate]['id']
    if mytemplateexists:
        prettyllog("semaphore", "create", template['name'], "ok", 0 , "template already exists", severity="INFO")
        baseurl = os.getenv('KALM_SEMAPHORE_URL')
        template_url = f"{baseurl}/api/project/{project_id}/templates/{mytemplateid}"  # Adjust the URL as needed
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = session.put(template_url, headers=headers, json=template)
        print("---------------------------------------- DEBUG ------------------------ template update------------ %s " % response.status_code)
        if response.status_code == 201:
            # Successful request
            prettyllog("semaphore", "create", template['name'], "ok", response.status_code , "create template", severity="INFO")
            return True
        elif response.status_code == 400:
            # Failed request
            prettyllog("semaphore", "create", template['name'], "error", response.status_code , "create template", severity="INFO")
            return True
        else:
            # Failed request
            prettyllog("semaphore", "create", template['name'], "error", response.status_code , "create template", severity="ERROR")
            return False
    else:
        baseurl = os.getenv('KALM_SEMAPHORE_URL')
        template_url = f"{baseurl}/api/project/{project_id}/templates"
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = session.post(template_url, headers=headers, json=templatedata)
        print("---------------------------------------- DEBUG ------------------------ template create------------ %s " % response.status_code)
        if response.status_code == 201:
            # Successful request
            prettyllog("semaphore", "create", template['name'], "ok", response.status_code , "create template", severity="INFO")
            return response.json()
        elif response.status_code == 400:
            # Failed request
            prettyllog("semaphore", "create", template['name'], "error", response.status_code , "create template", severity="INFO")
            return True
        
        else:
            # Failed request
            prettyllog("semaphore", "create", template['name'], "error", response.status_code , "create template", severity="ERROR")

def create_environment(session, project_id, environment):
    envjson = { "name": environment }
    envenv = { "name": environment }
    envdata = {
        "name": environment,
        "project_id": project_id,
        "password": "string",
        "json": envjson,
        "env": envenv
        }

    prettyllog("semaphore", "create", environment, "ok", 0 , "create environment", severity="INFO")
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    environment_url = f"{baseurl}/api/project/{project_id}/environments"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    # Use the session for the request
    response = session.post(environment_url, headers=headers, json=envdata)
    pprint.pprint(response.reason)
    pprint.pprint(response.status_code)

    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", environment, "ok", response.status_code , "create environment", severity="INFO")
        return response.json()
    else:
        # Failed request
        prettyllog("semaphore", "create", environment, "error", response.status_code , "create environment", severity="ERROR")

def update_environment(session, project_id, environment):
    prettyllog("semaphore", "create", environment, "ok", 0 , "update environment", severity="INFO")
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    environment_url = f"{baseurl}/api/project/{project_id}/environments/{environment['id']}"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    # Use the session for the request
    response = session.put(environment_url, headers=headers, json=environment)
    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", environment, "ok", response.status_code , "update environment", severity="INFO")
        return response.json()
    elif response.status_code == 400:
        prettyllog("semaphore", "create", environment, "error", response.status_code , "update environment", severity="INFO")
        return True
    else:
        # Failed request
        prettyllog("semaphore", "create", environment, "error", response.status_code , "update environment", severity="ERROR")
    
def create_view(session, project_id, view):
    prettyllog("semaphore", "create", view, "ok", 0 , "create view", severity="INFO")
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    view_url = f"{baseurl}/api/project/{project_id}/views"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    viewdata = {
        "title": view,
        "project_id": project_id
    }
    # Use the session for the request
    response = session.post(view_url, headers=headers, json=viewdata)
    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", view, "ok", response.status_code , "create view", severity="INFO")
        return response.json()
    else:
        # Failed request
        prettyllog("semaphore", "create", view, "error", response.status_code , "create view", severity="ERROR")

def update_view(session, project_id, view):
    prettyllog("semaphore", "create", view, "ok", 0 , "update view", severity="INFO")
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    view_id = get_view_id(session, project_id, view)
    view_url = f"{baseurl}/api/project/{project_id}/views/{view_id}"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use the session for the request
    response = session.put(view_url, headers=headers, json=view)
    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", view, "ok", response.status_code , "update view", severity="INFO")
        return response.json()
    elif response.status_code == 400:
        prettyllog("semaphore", "create", view, "error", response.status_code , "update view", severity="INFO")
        return True
    
    else:
        # Failed request
        prettyllog("semaphore", "create", view, "error", response.status_code , "update view", severity="ERROR")




def main():

    prettyllog("semaphore", "main", "main", "START", 0 , "main", severity="DEBUG")

    semaphore, mainconf, subprojects = read_config()
    organization = mainconf['organisation']['name']
    mysubprojects = mainconf['subprojects']
    checkenv, env = check_env()
    if not checkenv:
        prettyllog("semaphore", "main", "config", "error", 1 , "No semaphore config found", severity="ERROR")
        exit(1)

    state = {}
    session = login()
    # Check if the main project exists , it is the organization name
    # if not create it
    # if it exists check if it has the correct settings
    # if not update it
    prettyllog("semaphore", "main", "config", organization, 1 , "Check the main project", severity="INFO")
    check_project(organization, env)
    if session:
        projects = get_project(session)
        for project in projects:
            projectname = projects[project]['name']
            state[projectname] = {}
            state[projectname]['project'] = projects[project]
            state[projectname]['inventory'] = {}
            inventory = get_inventory(session, projects[project]['id'], projectname)
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
            prettyllog("semaphore", "check project", state_project, "ok", 0 , "subproject", severity="INFO")
        else:
            prettyllog("semaphore", "check project", state_project, "orphan", 1 , "subproject", severity="WARNING")
            orphans[state_project] = state[state_project]


    for missing in missings:
        prettyllog("semaphore", "createi project", missing, "Preparing to create project", 000 , "subproject", severity="DEBUG")
        # create project
        check_project(missing, env)
        create_project(session, missings[missing])

    for orphan in orphans:
        prettyllog("semaphore", "delete proejct", orphan, "Preparing to delete project", 000 , "subproject", severity="DEBUG")
        # delete project
        # delete project in git
        # delete project in semaphore
        # delete project in awx
        # delete project in vault
        # delete project in dns

    # prettyllog("semaphore", "main", "main", "ok", 0 , "subproject", severity="INFO")

    projects = get_project(session)
    prettyllog("semaphore", "projects", "main", "ok", 0 , "project", severity="DEBUG")

    for project in projects:
        prettyllog("semaphore", "projects", project, "ok", 0 , "project", severity="INFO")
        # We need to check if the project exists in git
    
        projectname = projects[project]['name']
        # delete trailing spaces    
        #"delete the last character from string"
        # if projectname.endswith(" "):
        #    projectname2 = projectname[:-1]

        prettyllog("semaphore", "check", projectname, "ok", 0 , "project", severity="INFO")
        state[projectname] = {}
        state[projectname]['project'] = projects[project]
        state[projectname]['inventory'] = {}
        state[projectname]['credentials'] = {}
        # print the keys in subprojects
        prettyllog("semaphore", "check", "credentials", "ok", 0 , "project", severity="DEBUG")
        credential  = {}
        projectname2 = projectname
        if projectname.endswith(" "):
            projectname2 = projectname2[:-1]
        try:
            credential['name'] = subprojects[projectname2]['json']['credentials']['name']
        except:
            credential['name'] = "dummy"
        try:
            credential['type'] = subprojects[projectname2]['json']['credentials']['type']
        except:
            credential['type'] = "none"
            credential['project_id'] = projects[project]['id']

        credential['ssh'] = {}
        try:
            credential['ssh']['login'] = subprojects[projectname2]['json']['credentials']['login']
        except:
            credential['ssh']['login'] = "dummyroot"

        # the private key needs to be read from the file
        try:
            filename =  subprojects[projectname2]['json']['credentials']['private_key']
        except:
            filename = None
        if filename == None:
            credential['ssh']['private_key'] = ""
            prettyllog("semaphore", "check", "credentials", "error", 1 , "private key not found", severity="ERROR")
        else:
            f = open(filename, "r")
            credential['ssh']['private_key'] = f.read()
            f.close()
        create_credential(session, projects[project]['id'] , credential)
        becomekey  = {
            "name": "becomekey",
            "type": "none",
            "project_id": projects[project]['id']
        }
        create_credential(session, projects[project]['id'] , becomekey)
        ssh_key_id = get_sshkey_id(session, projects[project]['id'], credential['name'])
        become_key_id = get_sshkey_id(session, projects[project]['id'], becomekey['name'])

        ########################################################################################
        #   START OF INVENTORY
        ########################################################################################

        prettyllog("semaphore", "check", "inventoty", "master", "000" , "INENTORY", severity="DEBUG")
        prettyllog("semaphore", "check", "inventoty", "master", "000" , "Get master inventory from netbox", severity="INFO")
        myinventory = get_netbox_master_inventory()
        prettyllog("semaphore", "check", "inventoty", "master", "000" , "Get master inventory from semaphore", severity="INFO")

        mysemaphoreinventories = get_semaphore_inventories(session, projects[project]['id'])
        if mysemaphoreinventories == False:
            prettyllog("semaphore", "check", "inventoty", "master", "000" , "No inventories found", severity="ERROR")

        myinvdata = get_inventory(session, projects[project]['id'], projectname)
        print("ONE ---------------------------------------------------------------------------------------------------------------------------------------------->")
        if organization in projectname and projectname in organization: # We are in a uniproject environment
            print("TWO---------------------------------------------------------------------------------------------------------------------------------------------->")
            prettyllog("semaphore", "check", "inventoty", "master", "000" , "Get master inventory from netbox for uniproject %s" % projectname , severity="INFO")
            mysubprojects = mainconf['subprojects']
            # We need to create a inventory for each subproject
            mysemaphoreinventories = get_semaphore_inventories(session, projects[project]['id'])
            pprint.pprint(mysemaphoreinventories)
            print("............................................")
            for mysubproject in mysubprojects:
                mysubprojectname = mysubproject['name']
                mylongname = "%s-%s" % (projectname, mysubprojectname)
                prettyllog("semaphore", "check", "longname", "master", "000" , "%s" % mylongname , severity="INFO")
                try:
                    mysemaphoreinventory = mysemaphoreinventories[mylongname]
                    pprint.pprint(mysemaphoreinventory)
                except:
                    mysemaphoreinventory = {}
                try: 
                    mysemaphoreinventory[mylongname]
                except:
                    mysemaphoreinventory = {}
                if len(mysemaphoreinventory) == 0:
                    if mysubprojectname not in organization:
                        myinventory = ""
                        for host in mysubproject['json']['hosts']:
                            myinventory += "%s\n" % host
                            


                    invetoryname = "%s-%s" % (mysubproject, "netbox")
                    inventorydata = {
                            "name": mylongname,
                            "project_id": projects[project]['id'],
                            "inventory": myinventory,
                            "ssh_key_id": ssh_key_id,
                            "become_key_id": become_key_id,
                            "type": "static"
                    }
                    create_inventory(session, projects[project]['id'], inventorydata)
                else:
                    invetoryname = "%s-%s" % (mysubproject, "netbox")
                    myinvid = get_inventory(session, projects[project]['id'], invetoryname)
                    inventorydata = {
                            "name": mylongname,
                            "project_id": projects[project]['id'],
                            "inventory": myinvdata,
                            "ssh_key_id": ssh_key_id,
                            "become_key_id": become_key_id,
                            "type": "static"
                    }
                    update_inventory(session, projects[project]['id'], myinvid, inventorydata)
                    ###########################################################################################
                    # Start of  views
                    ###########################################################################################
                    prettyllog("semaphore", "check", "view", "master", "000" , "Creating view for subproject %s" % mysubproject, severity="INFO")
                    mysemaphoreviews = get_views(session, projects[project]['id'])
                    myviewexists = False
                    for view in mysemaphoreviews:
                        if view == mysubproject:
                            myviewexists = True
                    if myviewexists:
                        prettyllog("semaphore", "check", "view", "master", "000" , "view exists %s" % mysubproject, severity="INFO")
                        update_view(session, projects[project]['id'], mysubproject)
                    else:
                        prettyllog("semaphore", "check", "view", "master", "000" , "view does not exists %s" % mysubproject, severity="INFO")
                        create_view(session, projects[project]['id'], mysubproject)
                ###########################################################################################
                # Start of  templates
                ###########################################################################################
                prettyllog("semaphore", "check", "template", "master", "000" , "Creating template for subproject %s" % mysubproject, severity="DEBUG")
                mysemaphoretemplates = get_templates(session, projects[project]['id'])
                pprint.pprint(mysemaphoretemplates)
                pprint.pprint(mysubproject)

        else: # We are in a multiproject environment
            myinventories = {}
            mysplitinv = myinventory.split("\n")
            for line in mysplitinv:
                if line.startswith('['):
                    mynameis = line.split('[')[1].split(']')[0]
                    myinventories[mynameis] = ""
                else:
                    myinventories[mynameis] += line + ";"
                    #delete_inventory(session, projects[project]['id'], myinvdata[line]['id'])
#            pprint.pprint(myinventories)
                    
            # Create an inventory call projectname - netbox with all hosts
            invexists = False
            if len(myinvdata) == 0:
                invexists = False
            else:
                invexists = True

            if not invexists:
                invetoryname = "%s-%s" % (projectname, "netbox")
                inventorydata = {
                        "name": invetoryname,
                        "project_id": projects[project]['id'],
                        "inventory": myinventory,
                        "ssh_key_id": ssh_key_id,
                        "become_key_id": become_key_id,
                        "type": "static"
                }
                create_inventory(session, projects[project]['id'], inventorydata)
            else:
                invetoryname = "%s-%s" % (projectname, "netbox")
                myinvid = get_inventory(session, projects[project]['id'], invetoryname)
                inventorydata = {
                        "name": invetoryname,
                        "project_id": projects[project]['id'],
                        "inventory": myinventory,
                        "ssh_key_id": ssh_key_id,
                        "become_key_id": become_key_id,
                        "type": "static"
                }
                update_inventory(session, projects[project]['id'], myinvid, inventorydata)
                # create multible inventpories and repos for each subproject
                for mysubproject in subprojects:
                    prettyllog("semaphore", "check", "inventoty", "master", "000" , "-------> Creating inventory for subproject %s" % mysubproject, severity="DEBUG")
                    if organization in mysubproject and mysubproject in organization:
                        prettyllog("semaphore", "check", "inventoty", "master", "000" , "We are in a single project env %s" % projectname , severity="INFO")
                        mysemaphorerepos = get_repositories(session, projects[project]['id'])
                        prettyllog("semaphore", "check", "Repository", "master", "000" , "check if repository exists %s" % mysubproject , severity="INFO")
                        myrepoexists = False
                        try:
                            myrepoexists = True
                        except:
                            myrepoexists = False
                        if myrepoexists:
                            prettyllog("semaphore", "check", "Repository", "master", "000" , "repository exists %s" % mysubproject , severity="INFO")
                            update_repository(session, projects[project]['id'], mysubproject)
                        else:
                            prettyllog("semaphore", "check", "Repository", "master", "000" , "repository does not exists %s" % mysubproject , severity="INFO")
                            create_repository(session, projects[project]['id'], mysubproject)
                        myinventories = get_netbox_master_inventory()
                        try:
                            mysemaphoreinventory = get_inventory(session, projects[project]['id'], mysubproject) 
                            update_repository(session, projects[project]['id'], mysubproject)
                        except:
                            create_repository(session, projects[project]['id'], mysubproject)
                            try:
                                mysemaphoreinventory = get_inventory(session, projects[project]['id'], mysubproject) 
                            except:
                                mysemaphoreinventory = {}
                            subinv= False
                            for subproject in subprojects:
                                prettyllog("semaphore", "check", "inventoty", "master", "000" , "Creating inventory for subproject %s" % subproject, severity="DEBUG")
                                try:
                                    subinv = True
                                except:
                                    subinv = False
                                if subinv:
                                    prettyllog("semaphore", "check", "inventoty", "master", "000" , "Creating inventory for subproject %s" % subproject, severity="INFO")
                                    create_inventory(session, projects[project]['id'], mysubproject)
                    else:
                        prettyllog("semaphore", "check", "inventoty", "master", "000" , "Get master inventory from netbox for subproject %s" % mysubproject , severity="INFO")
                        mysemaphorerepos = get_repositories(session, projects[project]['id'])
                        myrepoexists = False
                        for repo in mysemaphorerepos:
                            if repo == mysubproject:
                                myrepoexists = True
                        if myrepoexists:
                            prettyllog("semaphore", "check", "Repository", "master", "000" , "repository exists %s" % mysubproject , severity="INFO")
                            update_repository(session, projects[project]['id'], mysubproject)
                        else:
                            prettyllog("semaphore", "check", "Repository", "master", "000" , "repository does not exists %s" % mysubproject , severity="INFO")
                            create_repository(session, projects[project]['id'], mysubproject)
                        prettyllog("semaphore", "check", "repositories", "master", "000" , "repos created and updated %s" % projectname , severity="INFO")
                        # we need an environment for each subproject
                        prettyllog("semaphore", "check", "environment", "master", "000" , "Creating environment for subproject %s" % mysubproject, severity="INFO")
                        mysemaphoreenvironments = get_environments(session, projects[project]['id'])
                        if mysemaphoreenvironments == False:
                            prettyllog("semaphore", "check", "environment", "master", "000" , "No environments found", severity="ERROR")
                        myenvironmentexists = False
                        for environment in mysemaphoreenvironments:
                            if environment == mysubproject:
                                myenvironmentexists = True
                        if myenvironmentexists:
                            prettyllog("semaphore", "check", "environment", "master", "000" , "environment exists %s" % mysubproject, severity="INFO")
                            update_environment(session, projects[project]['id'], mysubproject)
                        else:
                            prettyllog("semaphore", "check", "environment", "master", "000" , "environment does not exists %s" % mysubproject, severity="INFO")
                            create_environment(session, projects[project]['id'], mysubproject)

                        # We need view for each subproject
                        prettyllog("semaphore", "check", "view", "master", "000" , "Creating view for subproject %s" % mysubproject, severity="INFO")
                        mysemaphoreviews = get_views(session, projects[project]['id'])
                        myviewexists = False
                        for view in mysemaphoreviews:
                            if view == mysubproject:
                                myviewexists = True
                        if myviewexists:
                            prettyllog("semaphore", "check", "view", "master", "000" , "view exists %s" % mysubproject, severity="INFO")
                            update_view(session, projects[project]['id'], mysubproject)
                        else:
                            prettyllog("semaphore", "check", "view", "master", "000" , "view does not exists %s" % mysubproject, severity="INFO")
                            create_view(session, projects[project]['id'], mysubproject)

                        # We need to create all the templates defined in the subproject
                    prettyllog("semaphore", "check", "template", "master", "000" , "Creating template for subproject %s" % mysubproject, severity="DEBUG")
                    mysemaphoretemplates = get_templates(session, projects[project]['id'])
                    pprint.pprint(mysemaphoretemplates)
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    try:
                        mytemplates = subprojects[mysubproject]['json']['templates']
                    except:
                        mytemplates = {}
                    for mytemplate in mytemplates:
                        prettyllog("semaphore", "check", "template", "master", "000" , "check template for subproject %s" % mytemplate, severity="DEBUG")
                        try:
                            mysemaphoretemplate = mysemaphoretemplates[mytemplate]
                        except:
                            mysemaphoretemplate = {}
                        
                        if len(mysemaphoretemplate) == 0:
                            prettyllog("semaphore", "check", "template", "master", "000" , "Creating template for subproject %s" % mytemplate, severity="INFO")

                            create_template(session, projects[project]['id'], mytemplate, mysubproject)
                        else:
                            update_template(session, projects[project]['id'], mytemplate, mysubproject) 

    prettyllog("semaphore", "main", "main", "END", 0 , "main", severity="DEBUG")





# END OF MAIN
    mytemplates = get_templates(session, 2)
    pprint.pprint(mytemplates)
    for mytemplate in mytemplates:
        pprint.pprint(mytemplate)


    return 0
