import os
import io
import subprocess
import requests
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend


# Vault environment settings
try:
  os.environ["VAULT_TOKEN"]
except KeyError:
    print("Error: VAULT_TOKEN is not set")
    exit(1)
try:
    os.environ["VAULT_ADDR"]
except KeyError:
    print("Error: VAULT_ADDR is not set")
    exit(1)


VAULT_TOKEN = os.getenv("VAULT_TOKEN")
VAULT_FORMAT = "json"
VAULT_ADDR = os.getenv("VAULT_ADDR")

def extract_certificate_expiry(cert_path):
    with open(cert_path, 'rb') as cert_file:
        cert_data = cert_file.read()
    
    cert = x509.load_pem_x509_certificate(cert_data, default_backend())
    not_after = cert.not_valid_after
    expiration_date = not_after.strftime('%Y-%m-%d %H:%M:%S')
    return expiration_date

        
def signkey(args):
  ready = False
  try:
    sshpath = os.path.dirname(args.action[1])
    sshfile = os.path.basename(args.action[1])
    #create path if it does not exist
    if not os.path.exists(sshpath):
      try:
        os.makedirs(sshpath)
        ready = True
      except:
        print("could not create directory")
        ready = False

    
    if os.path.exists(sshpath) and os.path.isdir(sshpath):
      print("directory exists")
      ready = True
    else:
      print("directory does not exist")
      ready = False
      
    if os.path.exists(args.action[1]) and os.path.isfile(args.action[1]):
      print("file exists")
      os.system("rm -f " + args.action[1])
    else:
      print("file does not exist")
      ready = True
  except:
    print("not ready")
    ready = False
  if ready:
    #create new ssh key
    os.system("ssh-keygen -f " + args.action[1] + " -q -N \"\"")
    #sign ssh key
    #read the public key
    with open(args.action[1] + ".pub", "r") as f:
        public_key = f.read()

    data = {
        "public_key": public_key
    }
    urlpath = "ssh-client-signer/sign/my-role"
    url = f"{VAULT_ADDR}/v1/{urlpath}"
    output_path = sshpath + "/" + sshfile + ".signed"
    response = requests.post(url, json=data, headers={"X-Vault-Token": VAULT_TOKEN})
    response_json = response.json()
    sign_public_key = response_json['data']['signed_key']
    with open(output_path, "w") as f:
        f.write(sign_public_key)
    #change permissions
    os.system("chmod 600 " + output_path)
    os.system("chmod 600 " + args.action[1] )
    os.system("chmod 600 " + args.action[1] + ".pub")
    print("signed key written to " + output_path)
    return True

    
    


# Directory to store the SSH key pair

def generate_ssh_key(KEY_DIR, KEY_NAME):
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)
    # Generate an SSH key pair without a passphrase
    subprocess.run(["rm", "-f", os.path.join(KEY_DIR, KEY_NAME)])
    subprocess.run(["ssh-keygen", "-t", "rsa", "-N", "", "-f", os.path.join(KEY_DIR, KEY_NAME)])

def sign_public_key(public_key):
    # Set up the Vault API endpoint for signing
    sign_url = f"{VAULT_ADDR}/v1/ssh-client-signer/sign/client-key"
    
    # Create the payload with the public key
    data = {
        "public_key": public_key
    }
    
    headers = {
        "X-Vault-Token": VAULT_TOKEN,
        "Content-Type": "application/json"
    }
    
    # Send a POST request to Vault for signing the key
    response = requests.post(sign_url, json=data, headers=headers)
    
    if response.status_code == 200:
        signed_key = response.json()["data"]["signed_key"]
        return signed_key
    else:
        print("Error signing the key.")
        return None

    
def refresh_key(KEY_DIR, KEY_NAME):
    print("Refreshing key...")
    # Generate an SSH key pair
    generate_ssh_key(KEY_DIR, KEY_NAME)
    # Read the public key from the generated key pair
    public_key_path = os.path.join(KEY_DIR, KEY_NAME + ".pub")
    with open(public_key_path, "r") as f:
        public_key = f.read().strip()
    print("Public key:")
    print(public_key)
    

    # Sign the public key using Vault
    signed_key = sign_public_key(public_key)
    
    if signed_key:
        print("Signed key:")
        print(signed_key)

