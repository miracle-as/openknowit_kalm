import datetime

def prettyllog(function, action, item, organization, statuscode, text):
  d_date = datetime.datetime.now()
  reg_format_date = d_date.strftime("%Y-%m-%d %I:%M:%S %p")
  print("%-20s: %-12s %20s %-50s %-20s %-4s %-50s " %( reg_format_date, function,action,item,organization,statuscode, text))

  