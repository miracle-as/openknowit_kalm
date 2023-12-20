import requests
import os   
import pprint

def checkenv():
    myenv = {}
    myenv['VAULT_ADDR'] = os.environ.get('KALM_VAULT_ADDR')   
    myenv['VAULT_TOKEN'] = os.environ.get('KALM_VAULT_TOKEN')
    myenv['VAULT_NAMESPACE'] = os.environ.get('KALM_VAULT_NAMESPACE')
    myenv['VAULT_FORMAT'] = os.environ.get('KALM_VAULT_FORMAT')

    if myenv['VAULT_FORMAT'] == None:
        myenv['VAULT_FORMAT'] = "json"

    #Check if we can connect to vault
    
    r = requests.get(myenv['VAULT_ADDR'], headers={"X-Vault-Token": myenv['VAULT_TOKEN']})
    if r.status_code != 200:
            print(r.status_code)
            print(r.content)
            print("Could not connect to vault, status code: " + str(r.status_code))
            exit(1)
    #check if we have a .ssh folder
    if not os.path.exists(os.path.expanduser("~/.ssh")):
        print("Could not find ~/.ssh folder")
        print("create it with mkdir ~/.ssh")
        os.mkdir(os.path.expanduser("~/.ssh"))
        #se access rights
        os.chmod(os.path.expanduser("~/.ssh"), 0o700)
    #check if we have a known_hosts file
    if not os.path.exists(os.path.expanduser("~/.ssh/known_hosts")):
        print("Could not find ~/.ssh/known_hosts file")
        print("create it with touch ~/.ssh/known_hosts")
        os.system("touch ~/.ssh/known_hosts")
        #se access rights
        os.chmod(os.path.expanduser("~/.ssh/known_hosts"), 0o600)
    myenv['SSH_KNOWN_HOSTS'] = os.path.expanduser("~/.ssh/known_hosts")
    return myenv





def signssh():
    myenv = checkenv()
    pprint.pprint(myenv)