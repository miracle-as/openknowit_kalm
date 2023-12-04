import os
import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    DEBUG   = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    INFO    = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


VERIFY_SSL = os.getenv("VERIFY_SSL", "false")
if VERIFY_SSL == "false" or VERIFY_SSL == "False" or VERIFY_SSL == "FALSE" or VERIFY_SSL == "no" or VERIFY_SSL == "NO" or VERIFY_SSL == "No":
  VERIFY_SSL = False
else:
  VERIFY_SSL = True

def line_in_file(file_path, search_text):
    with open(file_path, 'r') as f:
        for line in f:
            if search_text in line:
                return True
    return False

    

def get_file_content(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def get_file_content_lines(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()

def prettyllog(function, action, item, organization, statuscode, text, severity="INFO"):
  silence = False
  try:
    if os.getenv("KALM_SILENCE", "false").lower() == "true":
      silence = True
  except:
    silence = False
    
  if silence:
    return True

  d_date = datetime.datetime.now()
  reg_format_date = d_date.strftime("%Y-%m-%d %I:%M:%S %p")
  if severity == "INFO":
    print(f"{bcolors.INFO}%-20s: %-12s %20s %-30s %-50s %-4s %-50s " %( reg_format_date, function,action,item,organization,statuscode, text))
  elif severity == "WARNING":
    print(f"{bcolors.WARNING}%-20s: %-12s %20s %-30s %-50s %-4s %-50s " %( reg_format_date, function,action,item,organization,statuscode, text))
  elif severity == "ERROR":
    print(f"{bcolors.FAIL}%-20s: %-12s %20s %-30s %-50s %-4s %-50s " %( reg_format_date, function,action,item,organization,statuscode, text))
  elif severity == "DEBUG":
    print(f"{bcolors.OKCYAN}%-20s: %-12s %20s %-30s %-50s %-4s %-50s " %( reg_format_date, function,action,item,organization,statuscode, text))
  elif severity == "CHANGE":
    print(f"{bcolors.OKBLUE}%-20s: %-12s %20s %-30s %-50s %-4s %-50s " %( reg_format_date, function,action,item,organization,statuscode, text))
  else:
    print(f"{bcolors.INFO}%-20s: %-12s %20s %-30s %-50s %-4s %-50s " %( reg_format_date, function,action,item,organization,statuscode, text))
  print(f"{bcolors.ENDC}", end='')
  return True
