# Keep kalm and automate

![Python Logo](https://www.python.org/static/community_logos/python-logo.png "Sample inline image")

This is the README file for KALM

export TOWER_PASSWORD="<ADMIN PAASSWORD>"
export TOWER_HOST="https://<ANSIBLE HOST"
export TOWER_USERNAME="<ADMIN USER>"




{
  "kalm": {
    "vault": {
      "vault_addr": "https://demo.vault.com",
      "vault_token": "xcvcvbdsfgsdsdfsdfsdf"
    },
    "ssh": {
      "name": "kalmserver",
      "username": "knowit",
      "password": "xxx",
      "descriptions": "Credentials to login to kalm server and setup kalm service",
      "ssh_private_key": "/opt/kalm/id_rsa",
      "privilege_escalation_method": "xxx"
    }
  },
  "scm": {}
}

