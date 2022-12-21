
# Author: Pierce Brooks

import os
import sys

def run(source, target):
  descriptor = open(source, "r")
  lines = descriptor.readlines()
  descriptor.close()
  headers = []
  objects = {}
  object = None
  for line in lines:
    if (line.startswith("def ")):
      break
    if (line.startswith("class ")):
      if not (object == None):
        objects[object[0]] = object
      object = []
    if (object == None):
      headers.append(line)
    else:
      object.append(line)
  for key in objects:
    last = -1
    temp = ""
    name = key.strip().split(" ")[1:][0].split("(")[0].strip()
    if (name.upper() == name):
      temp += name.lower()
    else:
      for i in range(len(name)):
        if not (last == i-1):
          if (name[i:(i+1)].upper() == name[i:(i+1)]):
            last = i
            temp += "_"
        temp += name[i:(i+1)].lower()
      if (temp.endswith("port")):
        temp += "er"
    print("from ."+temp+" import "+name+"\n")
    temp += ".py"
    path = os.path.join(os.getcwd(), target, temp)
    descriptor = open(path, "w")
    for header in headers:
      descriptor.write(header)
    for other in objects:
      if (key == other):
        continue
      last = -1
      temp = None
      name = other.strip().split(" ")[1:][0].split("(")[0].strip()
      for line in objects[key]:
        if (name in line):
          temp = ""
          break
      if (temp == None):
        continue
      if (name.upper() == name):
        temp += name.lower()
      else:
        for i in range(len(name)):
          if not (last == i-1):
            if (name[i:(i+1)].upper() == name[i:(i+1)]):
              last = i
              temp += "_"
          temp += name[i:(i+1)].lower()
        if (temp.endswith("port")):
          temp += "er"
      descriptor.write("from ."+temp+" import "+name+"\n")
    descriptor.write("\nfrom .utilities import *\n\n")
    for line in objects[key]:
      descriptor.write(line)
    descriptor.close()
  return 0

def launch(arguments):
  if (len(arguments) < 3):
    return False
  source = arguments[1]
  target = arguments[2]
  result = run(source, target)
  print(str(result))
  if not (result == 0):
    return False
  return True

if (__name__ == "__main__"):
  print(str(launch(sys.argv)))
