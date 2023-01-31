
# Author: Pierce Brooks

import os
import sys
from packaging.version import parse

def bump(path, before, after, affix):
  success = False
  if not (os.path.exists(path)):
    return success
  before = affix+before+affix
  after = affix+after+affix
  descriptor = open(path, "r")
  lines = descriptor.readlines()
  descriptor.close()
  for i in range(len(lines)):
    line = lines[i]
    if not (before in line):
      continue
    lines[i] = line.replace(before, after)
    success = True
    #print(before+" = "+after)
    break
  descriptor = open(path, "w")
  for i in range(len(lines)):
    line = lines[i]
    descriptor.write(line)
  descriptor.close()
  return success

def run(version):
  if not ("." in version):
    return -1
  after = parse(version)
  before = str(after.major)+"."+str(after.minor-1)
  success = bump(os.path.join(os.getcwd(), "upload.bat"), before, str(after), "-")
  success = bump(os.path.join(os.getcwd(), "setup.py"), before, str(after), "\"") and success
  before += "."+str(after.micro)
  if (len(str(after).split(".")) > 2):
    success = bump(os.path.join(os.getcwd(), "buildster", "__init__.py"), before, str(after), "\"") and success
  else:
    success = bump(os.path.join(os.getcwd(), "buildster", "__init__.py"), before, str(after)+"."+str(after.micro), "\"") and success
  if not (success):
    return -2
  return 0

def launch(arguments):
  if (len(arguments) < 2):
    return False
  version = arguments[1]
  result = run(version)
  print(str(result))
  if not (result == 0):
    return False
  return True

if (__name__ == "__main__"):
  print(str(launch(sys.argv)))
