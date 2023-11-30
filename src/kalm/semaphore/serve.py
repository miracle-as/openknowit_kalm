import requests
import os
from ..common import prettyllog

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

def create_repository(session, repository):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    repository_url = f"{baseurl}/api/repositories"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    pprint.pprint(repository)
    # Use the session for the request
    response = session.post(repository_url, headers=headers, json=repository)
    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", repository['name'], "ok", response.status_code , "create repository", severity="INFO")
        return response.json()
    else:
        # Failed request
        prettyllog("semaphore", "create", repository['name'], "error", response.status_code , "create repository", severity="ERROR")

def get_repository(session):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    repository_url = f"{baseurl}/api/repositories"  # Adjust the URL as needed
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

def create_inventory(session, project_id, inventory):
    baseurl = os.getenv('KALM_SEMAPHORE_URL')
    inventory_url = f"{baseurl}/api/project/{project_id}/inventory"  # Adjust the URL as needed
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use the session for the request
    response = session.post(inventory_url, headers=headers, json=inventory)
    pprint.pprint(response.json())
    pprint.pprint(response.request.body)
    pprint.pprint(response.request.headers)
    pprint.pprint(response.request.url)

    if response.status_code == 201:
        # Successful request
        prettyllog("semaphore", "create", inventory['name'], "ok", response.status_code , "create inventory", severity="INFO")
        return response.json()
    else:
        # Failed request
        prettyllog("semaphore", "create", inventory['name'], "error", response.status_code , "create inventory", severity="ERROR")

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
        # map projects by name
        inventory_by_name = {}
        for item in inventory:
            inventory_by_name[item['name']] = item
            if debug:
                prettyllog("semaphore", "get", item['name'], "ok", response.status_code , "loadning inventory", severity="DEBUG")
        prettyllog("semaphore", "get", "inventory", "ok", response.status_code , "loadning inventory", severity="INFO")
        return inventory_by_name
    else:
        # Failed request
        prettyllog("semaphore", "get", "inventory", "error", response.status_code , "loadning inventory", severity="ERROR")

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
            prettyllog("semaphore", "Init", "subpropject", subproject['name'] , "000", "Getting subproject config", severity="DEBUG")
    return True, mainconf, subconf



    


def clone_git_project(projectname):
    # create a temporary dir and clone the project
    # return the config data
    tempfiledir = tempfile.mkdtemp()
    repo = git.Repo.clone_from(os.getenv('KALM_GIT_URL') + "/gitea/" + projectname + ".git", tempfiledir)
    configdata = {}
    configdata['url'] = os.getenv('KALM_GIT_URL') + "/" + projectname + ".git"
    configdata['path'] = tempfiledir
    configdata['repo'] = repo
    # check if the project has a kalm.json file in etc/kalm
    # if not create it
    if os.path.isfile(tempfiledir + "/etc/kalm/kalm.json"):
        prettyllog("semaphore", "Init", "clone", projectname , "000", "kalm.json exists", severity="DEBUG")
        f = open(tempfiledir + "/etc/kalm/kalm.json", "r")
        configdata['kalm'] = json.load(f)
        f.close()
    else:
        prettyllog("semaphore", "Init", "clone", projectname , "000", "kalm.json missing", severity="DEBUG")
        configdata['kalm'] = {}
        configdata['kalm']['project'] = {}
        configdata['kalm']['project']['name'] = projectname
        configdata['kalm']['project']['description'] = "kalm project"
        configdata['kalm']['project']['private'] = True
        configdata['kalm']['project']['auto_init'] = True
        configdata['kalm']['project']['inventory'] = {}
        configdata['kalm']['project']['inventory']['name'] = "inventory"
        configdata['kalm']['project']['inventory']['description'] = "kalm inventory"
        configdata['kalm']['project']['inventory']['private'] = True
        configdata['kalm']['project']['inventory']['auto_init'] = True
        configdata['kalm']['project']['inventory']['type'] = "static"
        configdata['kalm']['project']['inventory']['items'] = []
        configdata['kalm']['project']['inventory']['items'].append("localhost")
        #save the file
        f = open(tempfiledir + "/etc/kalm/kalm.json", "w")
        json.dump(configdata['kalm'], f)
        f.close()
        # add the file to git
        repo.git.add(A=True)
        repo.index.commit("kalm project created")
        origin = repo.remote(name='origin')
        origin.push()
    return configdata

        


 # Example: Get a list of your projects

def check_project(projectname, env):
    # we need to check if the project exists in git
    # if not we need to create it
    # if it exists we need to check if it exists in semaphore
    # if not we need to create it
    if env['KALM_GIT_TYPE'] == 'gitea':
        from ..gitea.git import get_git_projects
        git_projects = get_git_projects()
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
        configdata = clone_git_project(projectname)
        pprint.pprint(configdata)
            # create project in semaphore

            # create project in git
            # create project in semaphore
            # create project in awx
            # create project in vault
            # create project in dns
    else:
        prettyllog("project", "semaphore", projectname, "error", 1 , "git type not supported", severity="ERROR")
        exit(1)



    



    




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
    for project in projects:
        prettyllog("semaphore", "projects", project, "ok", 0 , "project", severity="INFO")
        # We need to check if the project exists in git
    
        projectname = projects[project]['name']
        state[projectname] = {}
        state[projectname]['project'] = projects[project]
        state[projectname]['inventory'] = {}
        inventorydata = {
                        "name": "Test",
                        "project_id": projects[project]['id'],
                        "inventory": "string",
                        "ssh_key_id": 1,
                        "become_key_id": 1,
                        "type": "static"
        }
        pprint.pprint(inventorydata)

        #create_inventory(session, projects[project]['id'], inventorydata)
        inventory = get_inventory(session, projects[project]['id'])
        for item in inventory:
            itemname = inventory[item]['name']
            state[projectname]['inventory'][itemname] = {}
            state[projectname]['inventory'][itemname]['item'] = inventory[item]
            prettyllog("semaphore", "main", item, "ok", 0 , "item", severity="INFO")
    return 0



