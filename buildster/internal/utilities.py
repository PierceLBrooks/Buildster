
# Author: Pierce Brooks

import os
import shutil
import fnmatch
import pathlib
import zipfile
import tarfile
import inspect
import logging
import platform
import traceback
import subprocess
from urllib.parse import urlparse, unquote
from urllib.request import urlretrieve

def retrieve(context, url, path = None):
  success = True
  if (url == None):
    success = False
  if (path == None):
    path = os.getcwd()
    if not (context == None):
      if not (context.work == None):
        path = context.work
    if not (os.path.isdir(path)):
      success = False
    if (success):
      try:
        path = os.path.join(path, pathlib.Path(unquote(urlparse(url).path)).name)
      except:
        logging.error(traceback.format_exc())
        success = False
  if (success):
    try:
      urlretrieve(url, path)
    except:
      logging.error(traceback.format_exc())
      success = False
  return success

def chmod(left, right):
  success = True
  try:
    os.chmod(left, right)
  except:
    success = False
  return success

def existence(path):
  if ("*" in str(os.path.basename(path))):
    if (os.path.isdir(os.path.dirname(path))):
      for root, folders, files in os.walk(os.path.dirname(path)):
        for name in folders:
          if (fnmatch.fnmatch(name, str(os.path.basename(path)))):
            return True
        for name in files:
          if (fnmatch.fnmatch(name, str(os.path.basename(path)))):
            return True
  else:
    if (os.path.exists(path)):
      return True
  return False

def contains(parent, child):
  if (pathlib.Path(parent) in pathlib.Path(child).parents):
    return True
  return False

def unique(duplicates):
  uniques = []
  for duplicate in duplicates:
    if not (duplicate in uniques):
      uniques.append(duplicate)
  return uniques

def wd():
  if ("BUILDSTER_WD" in os.environ):
    return os.environ["BUILDSTER_WD"]
  filename = inspect.getframeinfo(inspect.currentframe()).filename
  path = os.path.dirname(os.path.abspath(filename))
  if not (path == os.getcwd()):
    return os.getcwd()
  return path

def write(descriptor, line):
  descriptor.write(line+"\n")
  return True
  
def read(path):
  descriptor = open(path, "r")
  lines = descriptor.readlines()
  descriptor.close()
  return lines

def flatten(output, prefix = "", suffix = ""):
  final = ""
  if (output == None):
    return final
  for i in range(len(output)):
    temp = output[i]
    final += prefix
    for j in range(len(temp)):
      final += temp[j]
    final += suffix
  return final

def ensure(string):
  if (string == None):
    return ""
  if (type(string) == list):
    return flatten(string)
  if not (type(string) == str):
    return ""
  return string

def split(path):
  result = path.replace("\\", "/").split("/")
  length = len(result)
  for i in range(length):
    if (result[i].endswith(":")):
      result[i] = result[i]+"\\"
  return result
  
def relativize(base, leaf):
  return os.path.relpath(leaf, base).replace("\\", "/")
  
def find(base, leaf, prefixes = [""]):
  if not (os.path.isdir(base)):
    return None
  for root, folders, files in os.walk(base):
    for name in files:
      for prefix in prefixes:
        if (len(name) > len(prefix)+len(leaf)):
          if (name.startswith(prefix+leaf)):
            if (name[len(prefix)+len(leaf)] == '.'):
              return os.path.join(root, name)
        else:
          if (name == prefix+leaf):
            return os.path.join(root, name)
  return None

def move(source, destination, context = None, rename = None):
  success = True
  src = ""
  dst = ""
  extension = None
  index = -1
  try:
    if not (os.path.exists(source)):
      if not (context == None):
        if not (context.work == None):
          if ("*" in source):
            if (os.path.isdir(context.work)):
              for root, folders, files in os.walk(context.work):
                for name in files:
                  if (fnmatch.fnmatch(name, os.path.basename(source))):
                    src = os.path.join(root, name)
                    break
          else:
            src = os.path.join(context.work, source)
          if not (os.path.exists(src)):
            src = ""
    if (len(src) == 0):
      src += source
    for i in range(len(src)):
      if (src[i:(i+1)] == "."):
        index = i
    if (index > -1):
      extension = src[index:]
    if (os.path.exists(destination)):
      if (os.path.isdir(destination)):
        if (rename == None):
          dst += os.path.join(destination, os.path.basename(source))
        else:
          dst += os.path.join(destination, rename)
          if not (extension == None):
            if not (dst.endswith(extension)):
              dst += extension
      else:
        success = False
    else:
      if not (os.path.isdir(os.path.dirname(destination))):
        if (contains(wd(), os.path.dirname(destination))):
          os.makedirs(os.path.dirname(destination))
          if (rename == None):
            dst = destination
          else:
            os.makedirs(destination)
            dst = os.path.join(destination, rename)
            if not (extension == None):
              if not (dst.endswith(extension)):
                dst += extension
    if (success):
      if (len(dst) == 0):
        dst += destination
  except:
    logging.error(traceback.format_exc())
    success = False
  if (success):
    try:
      src = src.replace("\\", "/")
      dst = dst.replace("\\", "/")
      if (os.path.isdir(src)):
        shutil.copytree(src, dst)
      else:
        shutil.copyfile(src, dst)
    except:
      logging.error(traceback.format_exc())
      success = False
  if (success):
    status = os.stat(src)
    chmod(dst, status.st_mode)
  else:
    if not (context == None):
      context.log(None, "\""+src+"\" -> \""+dst+"\"")
  return success
  
def unzip(source, destination):
  success = True
  try:
    with zipfile.ZipFile(source) as zf:
      zf.extractall(destination)
  except:
    logging.error(traceback.format_exc())
    success = False
  return success
  
def untar(source, destination):
  success = True
  try:
    with open(source, "rb") as handle:
      with tarfile.open(fileobj=handle) as tf:
        tf.extractall(destination)
  except:
    logging.error(traceback.format_exc())
    success = False
  return success

def adjust(path):
  paths = split(path)
  length = len(paths)
  if (length > 1):
    root = paths[0]
    for i in range(length):
      if (i == 0):
        continue
      if (i > 1):
        if not (os.path.exists(root)):
          break
      next = os.path.join(root, paths[i])
      if (os.path.exists(next)):
        if (os.path.isdir(next)):
          root = next
        else:
          next = os.path.join(root, flatten(read(next)).strip())
          if (os.path.exists(next)):
            if (os.path.isdir(next)):
              root = next
      else:
        break
      if (i == length-1):
        if (os.path.exists(root)):
          path = root
          break
  return path
  
def get_parent(parents, tag):
  length = len(parents)
  if (length == 0):
    return None
  for i in range(length):
    temp = (length-1)-i
    if not (parents[temp] == None):
      if not (tag == None):
        if (parents[temp].tag == tag):
          return parents[temp]
      else:
        return parents[temp]
  return None
  
def get_child(node, tag):
  for child in node:
    if (child.tag == tag):
      return child
    temp = get_child(child, tag)
    if not (temp == None):
      return temp
  return None
  
def execute_command(command, environment = None):
  if (len(command) == 0):
    return True
  print(str(command))
  result = None
  try:
    process = subprocess.Popen(command, env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
      line = process.stdout.readline()
      if ((len(line) == 0) and not (process.poll() == None)):
        break
      print(line.decode("UTF-8").strip())
    output = process.communicate()[0]
    exit = process.returncode
    if (exit == 0):
      result = output
  except:
    pass
  if (result == None):
    return ""
  return result

def git_clone(repo_url, repo_path, environment = None):
  command = []
  command.append("git")
  command.append("clone")
  command.append(repo_url)
  command.append(repo_path)
  result = execute_command(command, environment)
  return result
  
def git_checkout(repo_branch, environment = None):
  command = []
  command.append("git")
  command.append("checkout")
  command.append("-f")
  command.append(repo_branch)
  result = execute_command(command, environment)
  return result

def git_submodule(environment = None):
  command = []
  command.append("git")
  command.append("submodule")
  command.append("update")
  command.append("--init")
  command.append("--recursive")
  result = execute_command(command, environment)
  return result

def cmake_configure(generator, architecture, arguments, source, path, installation, variant, environment = None):
  length = len(arguments)
  command = []
  command.append("cmake")
  if not (generator == None):
    command.append("-G")
    command.append(generator)
  if not (architecture == None):
    command.append("-A")
    command.append(architecture)
  for i in range(length):
    command.append(arguments[i])
  if (variant == None):
    command.append("-DCMAKE_INSTALL_PREFIX="+installation.replace("\\", "/"))
  else:
    command.append("-DCMAKE_INSTALL_PREFIX="+os.path.join(installation, variant.lower()).replace("\\", "/"))
  command.append(source)
  if not (os.path.isdir(path)):
    if (contains(wd(), path)):
      os.makedirs(path)
  cwd = os.getcwd()
  os.chdir(path)
  result = execute_command(command, environment)
  os.chdir(cwd)
  return result
  
def cmake_build(path, variant, natives, environment = None):
  command = []
  command.append("cmake")
  command.append("--build")
  command.append(path)
  if not (variant == None):
    command.append("--config")
    command.append(variant)
  if not (natives == None):
    length = len(natives)
    if (length > 0):
      command.append("--")
      for i in range(length):
        command.append(natives[i])
  result = execute_command(command, environment)
  return result
  
def cmake_install(path, variant, installation, natives, environment = None):
  command = []
  if not (platform.system() == "Windows"):
    command.append("sudo")
  command.append("cmake")
  command.append("--build")
  command.append(path)
  if not (variant == None):
    command.append("--config")
    command.append(variant)
  command.append("--target")
  command.append("install")
  if not (natives == None):
    length = len(natives)
    if (length > 0):
      command.append("--")
      for i in range(length):
        command.append(natives[i])
  result = execute_command(command, environment)
  return result
