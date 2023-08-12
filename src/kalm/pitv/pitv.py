import requests
import os
import urllib3
import redis
from PIL import Image
import subprocess


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

def check_if_file_is_picture(file):
  print("check if file is a picture")
  if file.lower.endswith(".jpg") or file.lower.endswith(".jpeg") or file.lower.endswith(".png") or file.lower.endswith(".gif") or file.lower.endswith(".bmp") or file.lower.endswith(".tiff") or file.lower.endswith(".tif") or file.lower.endswith(".webp") or file.lower.endswith("cr2"):
    
    return True
  else:
    return False
  


def get_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            metadata = img.info
            return metadata
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
      status = redis.get(file).decode("utf-8")
      print(status)
      if status == "0":
        print("file " + str(count) + " of " + str(total) ) #no newline
        if check_if_file_is_picture(file):
          print(file)
          key = "Picture:" + file
          redis.set(file, "1")
        else:
          redis.set(file, "999")
      if status == "1":
        metadata = get_image_metadata(file)
        print(metadata)
      else:
        redis.set(file, "0")
  print("evacuate")
  #get all files on the system

  
