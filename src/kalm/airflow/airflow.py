import requests
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


airflowurl = os.getenv("AIRFLOW_URL", "https://airflow.openknowit.com/api/v1")  
username = os.getenv("AIRFLOW_USERNAME", "your_username")
password = os.getenv("AIRFLOW_PASSWORD", "your_password")



def status():
  print(airflowurl)

def list_datasets():
    session = requests.Session()
    session.auth = (username, password)
    url = airflowurl + "/datasets"
    try:
        # Make a GET request to the API endpoint
        response = session.get(url, verify=False)

        # Check the response status code
        if response.status_code == 200:
            # API call was successful
            for dataset in response.json()['datasets']:
                print(dataset['id'])
        else:
            # API call failed
            print(f"API call failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle connection or request error
        print(f"An error occurred: {e}")

def delete_dataset(dataset_id):
    session = requests.Session()
    session.auth = (username, password)
    url = airflowurl + "/datasets/" + str(dataset_id)
    try:
        # Make a DELETE request to the API endpoint
        response = session.delete(url, verify=False)

        # Check the response status code
        if response.status_code == 204:
            # API call was successful
            print(f"Dataset {dataset_id} deleted successfully")
        else:
            # API call failed
            print(f"API call failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle connection or request error
        print(f"An error occurred: {e}")

def delete_all_datasets():
    session = requests.Session()
    session.auth = (username, password)
    url = airflowurl + "/datasets"
    try:
        # Make a GET request to the API endpoint
        response = session.get(url, verify=False)

        # Check the response status code
        if response.status_code == 200:
            # API call was successful
            for dataset in response.json()['datasets']:
                delete_dataset(dataset['id'])
        else:
            # API call failed
            print(f"API call failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle connection or request error
        print(f"An error occurred: {e}")


def delete_dag(dag_id):
    session = requests.Session()
    session.auth = (username, password)
    url = airflowurl + "/dags/" + str(dag_id)
    try:
        # Make a DELETE request to the API endpoint
        response = session.delete(url, verify=False)

        # Check the response status code
        if response.status_code == 204:
            # API call was successful
            print(f"DAG {dag_id} deleted successfully")
        else:
            # API call failed
            print(f"API call failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle connection or request error
        print(f"An error occurred: {e}")

def get_dag(dag_id):
    session = requests.Session()
    session.auth = (username, password)
    url = airflowurl + "/dags/" + dag_id
    try:
        # Make a GET request to the API endpoint
        response = session.get(url, verify=False)

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


def list_dags():
    session = requests.Session()
    session.auth = (username, password)
    url = airflowurl + "/dags"
    try:
        # Make a GET request to the API endpoint
        response = session.get(url, verify=False)

        # Check the response status code
        if response.status_code == 200:
            # API call was successful
            for dag in response.json()['dags']:
                print(dag['dag_id'])
        else:
            # API call failed
            print(f"API call failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle connection or request error
        print(f"An error occurred: {e}")

def delete_all_dags():
    session = requests.Session()
    session.auth = (username, password)
    url = airflowurl + "/dags"
    try:
        # Make a GET request to the API endpoint
        response = session.get(url, verify=False)

        # Check the response status code
        if response.status_code == 200:
            # API call was successful
            for dag in response.json()['dags']:
                delete_dag(dag['dag_id'])
        else:
            # API call failed
            print(f"API call failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle connection or request error
        print(f"An error occurred: {e}")
