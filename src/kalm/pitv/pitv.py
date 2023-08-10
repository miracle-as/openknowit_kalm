import requests
import os
import urllib3
import glob
import hashlib
import json
import sys
import time
import redis
import stat



from ..common import prettyllog


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




pitvurl = os.getenv("pitv_URL", "https://pitvapi.openknowit.com")  

def status():
  print(pitvurl)

def get_metadata_from_inode(file_path):
  try:
    # Get the inode number of the file
    inode = os.stat(file_path).st_ino
    print(inode)

    # Get the metadata using the inode number
    metadata = os.lstat(f"/proc/self/fd/{inode}")

    # Extract relevant information from the metadata
    file_type = stat.S_IFMT(metadata.st_mode)
    file_mode = stat.S_IMODE(metadata.st_mode)
    file_owner = metadata.st_uid
    file_group = metadata.st_gid
    file_size = metadata.st_size
    access_time = time.ctime(metadata.st_atime)
    modification_time = time.ctime(metadata.st_mtime)
    creation_time = time.ctime(metadata.st_ctime)

    # Print the metadata
    print(f"Inode: {inode}")
    print(f"File type: {file_type}")
    print(f"File mode: {file_mode:o}")
    print(f"Owner: {file_owner}")
    print(f"Group: {file_group}")
    print(f"File size: {file_size} bytes")
    print(f"Access time: {access_time}")
    print(f"Modification time: {modification_time}")
    print(f"Creation time: {creation_time}")
  except FileNotFoundError:
    print("File not found.")
  except PermissionError:
    print("Permission denied.")
  except Exception as e:
    print(f"Error: {e}")


def service():
  r = redis.Redis(host='localhost', port=6379, db=0)
  prettyllog("pitv", "service", "start")  
  while True:
    #find all files in /etc
    files = glob.glob('/etc/**/*', recursive=True)
    for file in files:
      get_metadata_from_inode(file)