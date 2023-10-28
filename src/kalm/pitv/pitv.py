import requests
import time
import os
import urllib3
import redis
from PIL import Image
import subprocess
import hashlib
import hvac


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
r=redis.Redis()


def init_redis():
  r = redis.Redis()
  r.set('foo', 'bar')
  value = r.get('foo')
  if value == b'bar':
    print("Redis is working")
    return r
  else:
    print("Redis is not working")
    exit(1)

pitvurl = os.getenv("pitv_URL", "https://pitvapi.openknowit.com")  

def status():
  print(pitvurl)

def service():
  print("service")



def calculate_md5(filename, block_size=65536):
    if os.path.isfile(filename):
      md5_hash = hashlib.md5()
      try:
        with open(filename, "rb") as file:
          for block in iter(lambda: file.read(block_size), b""):
            md5_hash.update(block)
        return md5_hash.hexdigest()
      except:
        return None
    else:
      return None


def hashit(file):
   #read file in binary mode
    with open(file, 'rb') as f:
        data = f.read()
        #return md5 hash
        data = data.encode("utf-8")
        return hashlib.md5(data).hexdigest()

def check_if_file_is_picture(file):
  print("check if file is a picture")
  file = file.lower()
  if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png") or file.endswith(".gif") or file.endswith(".bmp") or file.endswith(".tiff") or file.endswith(".tif") or file.endswith(".webp") or file.endswith("cr2"):
    
    return True
  else:
    return False

def get_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            metadata = img.info
            if len(metadata) > 0:
              return metadata
            else:
              return None
    except Exception as e:
        print("Error:", e)
        return None

def list_files_recursive(directory):
    files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "rb"):
                    files.append(file_path)
            except PermissionError:
                print("Permission denied for file:", file_path)
    return files

def locate_files(keyword=""):
    try:
        # Run the locate command and capture the output
        command = ["locate", keyword]
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
        output = result.stdout
        file_list = output.splitlines()
        return file_list
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return []

def evacuate():
  redis = init_redis()
  #get all files on the system
  files = locate_files()
  total = len(files)
  count = 0
  for file in files:
    count = count + 1
    if redis.exists(file):
      # get file size
      try:
        filesize = os.path.getsize(file)
      except:
        filesize = 0
        
      status = redis.get(file).decode("utf-8")
      # print a status wihout newline
      print("file " + str(count) + " of " + str(total) + " status: " + status, end="\r")
      md5 = calculate_md5(file)
      print(md5)
      # scp file remotehost:/files/
      if md5 is not None: 
        keys = "MD5:" + md5
        vault.secrets.kv.v2.existing_version(keys)
        if vault.secrets.kv.v2.get_secret_version(keys) is None:
          vault.secrets.kv.v2.create_or_update_secret(keys, md5=md5, file=file)
        
        redis.set(keys, filesize)

      if status == "1":
        metadata = get_image_metadata(file)
        if metadata is not None:
           key = "metadata:" + file
           redis.set(key, str(metadata))
    else:
      print("file " + str(count) + " of " + str(total) + " status: unknown", end="\r")
      if check_if_file_is_picture(file):
        print(file)
        key = "Picture:" + file
        redis.set(file, "1")
      else:
        redis.set(file, "999")
      
    





#      if status == 0 or status == 
#        print("file " + str(count) + " of " + str(total) ) #no newline
#        if check_if_file_is_picture(file):
#          print(file)
#          key = "Picture:" + file
#         redis.set(file, "1")
#       else:
#         redis.set(file, "999")
#      if status == "1":
#        metadata = get_image_metadata(file)
#        print(metadata)
#      else:
#        redis.set(file, "0")
#  print("evacuate")
  #get all files on the system

  
