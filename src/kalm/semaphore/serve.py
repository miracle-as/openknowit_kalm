import requests
import os
from ..common import prettyllog
import pprint





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
        print("Login successful")
        return session  # Return the session for subsequent requests
    else:
        # Failed request
        print(f"Error: {response.status_code}")
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
        print("Projects:", projects)
        # map prokects by name
        projects_by_name = {}
        for project in projects:
            projects_by_name[project['name']] = project
        print("Projects by name:", projects_by_name)
        return projects_by_name

    else:
        # Failed request
        print(f"Error: {response.status_code}")

def get_project_by_name(session, project_name):
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
    else:
        # Failed request
        print(f"Error: {response.status_code}")

    
def check_env():
    print("check_env")
    if (os.getenv('KALM_SEMAPHORE_URL') == None):
        print("KALM_SEMAPHORE_URL not set")
        return 1
    else:
        print("KALM_SEMAPHORE_URL set to " + os.getenv('KALM_SEMAPHORE_URL'))
        return 0
    

 # Example: Get a list of your projects

def main():
    session = login()
    if session:
        projects = get_project(session)
        print("Projects:", projects)


    return 0
