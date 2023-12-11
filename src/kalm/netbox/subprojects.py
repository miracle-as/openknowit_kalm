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
    url = env['KALM_NETBOX_URL'] + "/api/virtualization/virtual-machines/" + str(serverid)
    headers = {'Authorization': 'Token ' + env['KALM_NETBOX_TOKEN'],
               'Accept': 'application/json',
               'Content-Type': 'application/json'
            }
    mytags = []
    r = requests.get(url, headers=headers, verify=env['KALM_NETBOX_SSL'])
    if r.status_code == 200:
        data = r.json()
        for tag in data['tags']:
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
        
def setrandomcolor():
        ###############################
        return "00ff00"


def update_subprojects(myenv):
        prettyllog("netbox", "init", "subprojects", "kalm" "ok", "000" , "updating subprojects", severity="INFO")
        for subproject in myenv['subproject']:
                print(subproject)
                for myhost in myenv['subproject'][subproject]['hosts']:
                        myserverid = get_virtual_server_id(myhost, myenv)
                        if myserverid:
                                alltags = get_all_tags(myenv)
                                try:
                                        mysubprojecttagid = alltags[subproject]
                                except:
                                        mysubprojecttagid = False
                                if not mysubprojecttagid:
                                        print("adding tag %s to netbox" % subproject)
                                        url = myenv['KALM_NETBOX_URL'] + "/api/extras/tags/"
                                        headers = {'Authorization': 'Token ' + myenv['KALM_NETBOX_TOKEN'],
                                                   'Accept': 'application/json',
                                                   'Content-Type': 'application/json'
                                                }
                                        data = {
                                                "name": subproject,
                                                "slug": subproject.lower(),
                                                "color": setrandomcolor()
                                                }
                                        r = requests.post(url, headers=headers, data=json.dumps(data), verify=myenv['KALM_NETBOX_SSL'])
                                        if r.status_code == 201:
                                                print("tag %s added to netbox" % subproject)
                                        else:
                                                print("unable to add tag %s to netbox" % subproject)
                                else:
                                        print("tag %s already exists in netbox" % subproject)
                                foundmysubprojecttag = False

                                mytags = get_virtual_server_tags(myserverid, myenv)
                                for tag in mytags:
                                        if tag == subproject:
                                                foundmysubprojecttag = True
                                if foundmysubprojecttag:
                                        print("server %s already has tag %s" % (myhost, subproject))
                                else:
                                        mytagids = []
                                        for tag in mytags:
                                                mytagids.append(alltags[tag])
                                        mytagids.append(mysubprojecttagid)
                                        print("server %s does not have tag %s" % (myhost, subproject))
                                        url = myenv['KALM_NETBOX_URL'] + "/api/virtualization/virtual-machines/" + str(myserverid) + "/"
                                        headers = {'Authorization': 'Token ' + myenv['KALM_NETBOX_TOKEN'],
                                                   'Accept': 'application/json',
                                                   'Content-Type': 'application/json'
                                                }
                                        data = {
                                                "tags": mytagids
                                                }
                                        r = requests.patch(url, headers=headers, data=json.dumps(data), verify=myenv['KALM_NETBOX_SSL'])
                                        if r.status_code == 200:
                                                print("tag %s added to server %s" % (subproject, myhost))
                                        else:
                                                print(r.content)
                                                print("unable to add tag %s to server %s" % (subproject, myhost))


                        else:
                                print("server %s not found" % myhost)
        return True




                        


        return myenv
