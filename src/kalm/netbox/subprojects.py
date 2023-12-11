from ..common import prettyllog
import json
import os
import requests


def get_all_tags(env):
    prettyllog("netbox", "get", "all tags", "000", "000" , "getting all tags", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/extras/tags/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
               'Content-Type': 'application/json'
            }
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        alltags = {}
        for tag in data['results']:
            alltags[tag['name']] = tag['id']
        prettyllog("netbox", "get", "all tags", "000", r.status_code , "all tags found", severity="INFO")
        return alltags
    else:
        prettyllog("netbox", "get", "all tags", "000", r.status_code , "unable to get all tags", severity="ERROR")
        return False
    
def get_virtual_server_tags(serverid, env):
    prettyllog("netbox", "get", "virtual server tags", serverid, "000" , "getting virtual server tags", severity="INFO")
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/virtual-machines/" + str(serverid) + "/tags/"
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
               'Content-Type': 'application/json'
            }
    mytags = []
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        for tag in data['results']:
            mytags.append(tag['name'])
        prettyllog("netbox", "get", "virtual server tags", serverid, r.status_code , "virtual server tags found", severity="INFO")
        return mytags
    else:
        prettyllog("netbox", "get", "virtual server tags", serverid, r.status_code , "unable to get virtual server tags", severity="ERROR")
        return mytags      
    
def get_virtual_server_id(servername, env):
        prettyllog("netbox", "get", "virtual server id", servername, "000" , "getting virtual server id", severity="INFO")
        url = env['KALM_NETBOX_URL'] + "/api/virtualization/virtual-machines/?name=" + servername
        headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
                   'Accept': 'application/json',
                   'Content-Type': 'application/json'
                }
        r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
        if r.status_code == 200:
                data = r.json()
                if data['count'] == 1:
                        prettyllog("netbox", "get", "virtual server id", servername, r.status_code , "virtual server id found", severity="INFO")
                        return data['results'][0]['id']
                else:
                        prettyllog("netbox", "get", "virtual server id", servername, r.status_code , "unable to get virtual server id", severity="ERROR")
                return False
        else:
                prettyllog("netbox", "get", "virtual server id", servername, r.status_code , "unable to get virtual server id", severity="ERROR")
                return False
        


def update_subprojects(myenv):
        prettyllog("netbox", "init", "subprojects", "kalm" "ok", "000" , "updating subprojects", severity="INFO")
        for subproject in myenv['subproject']:
                print(subproject)
                for myhost in myenv['subproject'][subproject]['hosts']:
                        myserverid = get_virtual_server_id(myhost, myenv)
                        if myserverid:
                                mytags = get_virtual_server_tags(myserverid, myenv)
                                alltags = get_all_tags(myenv)
                                for tag in mytags:
                                        if tag in alltags:
                                                print("tag %s already exists" % tag)
                                        else:
                                                print("tag %s does not exists" % tag)
                                                # create tag
                                                url = myenv['KALM_NETBOX_URL'] + "/api/extras/tags/"
                                                headers = {'Authorization': 'Token ' + myenv['KALM_NETBOX_TOKEN'],
                                                           'Accept': 'application/json',
                                                           'Content-Type': 'application/json'
                                                        }
                                                data = {'name': tag}
                                                r = requests.post(url, headers=headers, data=json.dumps(data), verify=myenv['KALM_NETBOX_SSL'])
                                                if r.status_code == 201:
                                                        print("tag %s created" % tag)
                                                else:
                                                        print("tag %s not created" % tag)
                                # add tags to server

                                url = myenv['KALM_NETBOX_URL'] + "/api/virtualization/virtual-machines/" + str(myserverid)
                                headers = {'Authorization': 'Token ' + myenv['KALM_NETBOX_TOKEN'],
                                           'Accept': 'application/json',
                                           'Content-Type': 'application/json'
                                        }
                                data = []
                                for tag in mytags:
                                        data.append(alltags[tag])
                                r = requests.post(url, headers=headers, data=json.dumps(data), verify=myenv['KALM_NETBOX_SSL'])
                                if r.status_code == 201:
                                        print("tags added to server")
                                else:
                                        print("tags not added to server")
                        else:
                                print("server %s not found" % myhost)
        return True




                        


        return myenv
