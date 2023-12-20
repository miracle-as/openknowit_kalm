import requests
import os   

def checkenv():
    VAULT_ADDR = os.environ.get('KALM_VAULT_ADDR')   
    VAULT_TOKEN = os.environ.get('KALM_VAULT_TOKEN')
    VAULT_NAMESPACE = os.environ.get('KALM_VAULT_NAMESPACE')

    if VAULT_ADDR == None:
        print("Please set VAULT_ADDR environment variable")
        exit(1)
    if VAULT_TOKEN == None:
        print("Please set VAULT_TOKEN environment variable")
        exit(1)
    if VAULT_NAMESPACE == None:
        print("Please set VAULT_NAMESPACE environment variable")
        exit(1)

    #Check if we can connect to vault
    try:
        r = requests.get(VAULT_ADDR, headers={"X-Vault-Token": VAULT_TOKEN})
        if r.status_code != 200:
            print("Could not connect to vault, status code: " + str(r.status_code))
            exit(1)
    except:
        print("Could not connect to vault")
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
    return True





def signssh():
    checkenv()