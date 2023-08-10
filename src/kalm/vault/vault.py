import os
import subprocess
import requests

# Vault environment settings
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
VAULT_FORMAT = "json"
VAULT_ADDR = os.getenv("VAULT_ADDR")

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

