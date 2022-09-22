
# Author: Pierce Brooks

import re
import os
import ast
import sys
import copy
import json
import stat
import wget
import shlex
import shutil
import base64
import pathlib
import zipfile
import tarfile
import inspect
import logging
import platform
import importlib
import traceback
import subprocess
import xml.etree.ElementTree as xml_tree
from datetime import datetime

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
  src = ""
  dst = ""
  if not (os.path.exists(source)):
    if not (context == None):
      if not (context.work == None):
        src = os.path.join(context.work, source)
        if not (os.path.exists(src)):
          src = ""
  if (os.path.exists(destination)):
    if (os.path.isdir(destination)):
      if (rename == None):
        dst += os.path.join(destination, os.path.basename(source))
      else:
        dst += os.path.join(destination, rename)
    else:
      return False
  else:
    if not (os.path.isdir(os.path.dirname(destination))):
      if (contains(wd(), os.path.dirname(destination))):
        os.makedirs(os.path.dirname(destination))
  if (len(src) == 0):
    src += source
  if (len(dst) == 0):
    dst += destination
  if not (context == None):
    context.log(None, "\""+src+"\" -> \""+dst+"\"")
  try:
    shutil.copyfile(src.replace("\\", "/"), dst.replace("\\", "/"))
  except:
    return False
  return True
  
def unzip(source, destination):
  success = True
  try:
    with zipfile.ZipFile(source) as zf:
      zf.extractall(destination)
  except Exception as exception:
    logging.error(traceback.format_exc())
    success = False
  return success
  
def untar(source, destination):
  success = True
  try:
    with open(source, "rb") as handle:
      with tarfile.open(fileobj=handle) as tf:
        tf.extractall(destination)
  except Exception as exception:
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
  
def cmake_build(path, variant, environment = None):
  command = []
  command.append("cmake")
  command.append("--build")
  command.append(path)
  if not (variant == None):
    command.append("--config")
    command.append(variant)
  result = execute_command(command, environment)
  return result
  
def cmake_install(path, variant, installation, environment = None):
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
  result = execute_command(command, environment)
  return result

class Object(object):
  def __init__(self):
    self.node = None
    
  def getContent(self):
    return ""
    
  def toString(self, *arguments):
    if (len(arguments) == 0):
      return "("+self.__class__.__name__+")"+str(self)
    other = arguments[0]
    if (other == None):
      return "/NULL/"
    if (type(other) == str):
      return str(other)
    if (type(other) == list):
      length = len(other)
      string = "["
      for i in range(length):
        string += self.toString(other[i])
        if not (i == length-1):
          string += ", "
      string += "]"
      return string
    if not (isinstance(other, Object)):
      return "/INVALID/"
    return other.toString()
    
class Element(Object):
  def __init__(self):
    super(Element, self).__init__()
    self.parent = None
    
  def build(self, owner, variant):
    return True
    
  def distribute(self, owner, distribution, variant):
    return True
    
  def getParent(self):
    return self.parent
    
  def getContent(self):
    return ""
    
class Performer(Object):
  def __init__(self):
    super(Performer, self).__init__()
    
  def perform(self, context):
    return True
    
  def getContent(self):
    return ""
    
class Build(Element):
  def __init(self):
    super(Build, self).__init__()
    
  def build(self, owner, variant):
    owner.getContext().record(self.node, str(self.importsContent))
    owner.getContext().record(self.node, str(self.exportsContent))
    return True
    
  def filterExports(self, exportsContent, need):
    content = {}
    if not (need == None):
      if (isinstance(need, Build)):
        for key in exportsContent:
          if not (exportsContent[key][2] == None):
            if not (need.getLabel() in exportsContent[key][2]):
              content[key] = exportsContent[key]
          else:
            content[key] = exportsContent[key]
      else:
        for key in exportsContent:
          content[key] = exportsContent[key]
    else:
      for key in exportsContent:
        content[key] = exportsContent[key]
    return content
    
  def addExport(self, add, variant, exceptions):
    if not (isinstance(add, Export)):
      return False
    success = self.doExport(add.key.getContent(), add.value.getContent(), add.export.getContent(), variant, exceptions)
    if not (success):
      return False
    return True
    
  def addImport(self, add, variant):
    if not (isinstance(add, Import)):
      return False
    success = self.doImport(add.getContent(), variant)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export, variant, exceptions):
    return True
    
  def doImport(self, label, variant):
    return True
    
  def getExports(self, variant, need):
    return []
    
  def getGenerator(self, owner):
    name = platform.system()
    if (name == "Windows"):
      return "MinGW Makefiles"
    if (name == "Linux"):
      return "Unix Makefiles"
    if (name == "Darwin"):
      return "Xcode"
    return ""
    
  def getLabel(self):
    return ""
    
  def getContent(self):
    return self
    
class String(Object):
  def __init__(self, content = None):
    super(String, self).__init__()
    self.content = ""
    if (type(content) == str):
      self.content = content
      
  def getContent(self):
    return self.content
      
  def __str__(self):
    return "<\""+self.content+"\">"
    
class List(Element):
  def __init__(self, content = None):
    super(List, self).__init__()
    self.content = []
    if (type(content) == list):
      self.content = content
      
  def build(self, owner, variant):
    return True
    
  def add(self, content):
    if not (content == None):
      if (type(content) == list):
        length = len(content)
        for i in range(length):
          if not (self.add(content[i])):
            return False
        return True
      elif (isinstance(content, Object)):
        self.content.append(content)
        return True
      else:
        return False
    return False
    
  def getContent(self):
    content = []
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Object)):
        content.append(self.content[i].getContent())
    return content
    
  def __len__(self):
    return len(self.content)
      
  def __str__(self):
    to = "<["
    length = len(self.content)
    for i in range(length):
      to += self.content[i].toString()
      if not (i == length-1):
        to += ", "
    to += "]>"
    return to

class Key(Object):
  def __init__(self, string = None):
    super(Key, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
class Value(Object):
  def __init__(self, string = None):
    super(Value, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
class Destination(Object):
  def __init__(self, path = None):
    super(Destination, self).__init__()
    self.path = None
    if (type(path) == Path):
      self.path = path
      
  def getContent(self):
    return self.path.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.path)+">"
    
class Content(Object):
  def __init__(self, string = None):
    super(Content, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
class CopierSource(Object):
  def __init__(self, path = None):
    super(CopierSource, self).__init__()
    self.path = None
    if (type(path) == Path):
      self.path = path
      
  def getContent(self):
    return self.path.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.path)+">"
    
class CopierDestination(Object):
  def __init__(self, path = None):
    super(CopierDestination, self).__init__()
    self.path = None
    if (type(path) == Path):
      self.path = path
      
  def getContent(self):
    return self.path.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.path)+">"
    
class CopierRename(Object):
  def __init__(self, name = None):
    super(CopierRename, self).__init__()
    self.name = None
    if (type(name) == String):
      self.name = name
      
  def getContent(self):
    return self.name.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.name)+">"
    
class Writer(Performer):
  def __init__(self, destination = None, content = None):
    super(Writer, self).__init__()
    self.destination = None
    self.content = None
    if (type(destination) == Destination):
      self.destination = destination
    if (type(content) == Content):
      self.content = content
      
  def getContent(self):
    return self.destination.getContent()
    
  def perform(self, context):
    context.log(None, "Writing \""+self.toString(self.destination)+"\"...")
    if ((self.destination == None) or (self.content == None)):
      return False
    content = self.getContent().strip()
    if (len(content) == 0):
      return False
    descriptor = open(content, "w")
    if not (write(descriptor, self.content.getContent())):
      return False
    descriptor.close()
    context.log(None, "Wrote \""+self.toString(self.destination)+"\"!")
    return True
    
  def __str__(self):
    return "<"+self.toString(self.destination)+", "+self.toString(self.content)+">"

class Copier(Performer):
  def __init__(self, source = None, destination = None, rename = None):
    super(Copier, self).__init__()
    self.source = None
    self.destination = None
    self.rename = None
    if (type(source) == CopierSource):
      self.source = string
    if (type(destination) == CopierDestination):
      self.destination = destination
    if (type(rename) == CopierRename):
      self.rename = rename
      
  def perform(self, context):
    context.log(None, "Copying from \""+self.toString(self.source)+"\" to \""+self.toString(self.destination)+"\"...")
    if ((self.source == None) or (self.destination == None)):
      return False
    source = self.source.getContent()
    destination = self.destination.getContent()
    rename = None
    if not (self.rename == None):
      rename = self.rename.getContent()
    if ("*" in source):
      for root, folders, files in os.walk(os.path.dirname(source)):
        names = []
        for name in folders:
          names.append(name)
        for name in files:
          names.append(name)
        for name in names:
          if (str(os.path.basename(source)).replace("*", "") in name):
            temp = None
            if (rename == None):
              temp = os.path.join(destination, os.path.relpath(root, os.path.dirname(source)), name)
            else:
              temp = os.path.join(destination, os.path.relpath(root, os.path.dirname(source)), rename)
            context.log(None, "Copying from \""+str(os.path.join(root, name))+"\" to \""+str(temp)+"\"...")
            if not (move(os.path.join(root, name), temp, context, rename)):
              return False
            context.log(None, "Copied from \""+str(os.path.join(root, name))+"\" to \""+str(temp)+"\"!")
    else:
      if not (move(source, destination, context, rename)):
        return False
    context.log(None, "Copied from \""+self.toString(self.source)+"\" to \""+self.toString(self.destination)+"\"!")
    return True
    
  def __str__(self):
    return "<"+self.toString(self.source)+", "+self.toString(self.destination)+", "+self.toString(self.rename)+">"

class Deleter(Performer):
  def __init__(self, path = None):
    super(Deleter, self).__init__()
    self.path = None
    if (type(path) == Path):
      self.path = path
      
  def getContent(self):
    return self.path.getContent()
    
  def perform(self, context):
    context.log(None, "Deleting \""+self.toString(self.path)+"\"...")
    if (self.path == None):
      return False
    content = self.getContent().strip()
    if (len(content) == 0):
      return False
    if not (os.path.exists(content)):
      context.log(None, "Deleted \""+self.toString(self.path)+"\"!")
      return True
    if (os.path.isfile(content)):
      os.unlink(content)
    else:
      shutil.rmtree(content)
    context.log(None, "Deleted \""+self.toString(self.path)+"\"!")
    return True
    
  def __str__(self):
    return "<"+self.toString(self.path)+">"
    
class Extractor(Performer):
  def __init__(self, path = None):
    super(Extractor, self).__init__()
    self.path = None
    if (type(path) == Path):
      self.path = path
      
  def getContent(self):
    return self.path.getContent()
    
  def perform(self, context):
    context.log(None, "Extracting \""+self.toString(self.path)+"\"...")
    if (self.path == None):
      return False
    content = self.getContent().strip()
    if (len(content) == 0):
      return False
    if not (os.path.isfile(content)):
      return False
    path = os.path.dirname(content)
    filename = os.path.basename(content)
    index = -1
    for i in range(len(filename)):
      if (filename[i:(i+1)] == "."):
        index = i
        break
    if (index < 0):
      return False
    extension = filename[index:].lower()
    filename = filename[:index]
    if (os.path.exists(os.path.join(path, filename))):
      context.log(None, "Extracted \""+self.toString(self.path)+"\"!")
      return True
    if (extension == ".zip"):
      if not (unzip(content, os.path.join(path, filename))):
        return False
    elif ((extension == ".tgz") or (extension == ".txz") or (extension == ".tbz") or (extension.startswith(".tar"))):
      if not (untar(content, os.path.join(path, filename))):
        return False
    else:
      return False
    context.log(None, "Extracted \""+self.toString(self.path)+"\"!")
    return True
    
  def __str__(self):
    return "<"+self.toString(self.path)+">"
    
class Branch(Object):
  def __init__(self, string = None):
    super(Branch, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"

class Architecture(Object):
  def __init__(self, string = None):
    super(Architecture, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"

class Generator(Object):
  def __init__(self, string = None, architecture = None):
    super(Generator, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
    self.architecture = None
    if (type(architecture) == Architecture):
      self.architecture = architecture
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+", "+self.toString(self.architecture)+">"

class Path(Object):
  def __init__(self, string = None):
    super(Path, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"

class URL(Object):
  def __init__(self, string = None):
    super(URL, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"

class Label(Object):
  def __init__(self, string = None):
    super(Label, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
class Work(Object):
  def __init__(self, string = None):
    super(Work, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"

class Root(Object):
  def __init__(self, string = None):
    super(Root, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
class Term(Object):
  def __init__(self, string = None):
    super(Term, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
class Argument(Element):
  def __init__(self, string = None):
    super(Argument, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def build(self, owner, variant):
    return True
    
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
class ArgumentList(List):
  def __init__(self):
    super(ArgumentList, self).__init__()
    
  def build(self, owner, variant):
    return True
        
  def addArgument(self, argument):
    if not (isinstance(argument, Argument)):
      return False
    return super(ArgumentList, self).add(argument)
    
class Hint(Element):
  def __init__(self, string = None):
    super(Hint, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def build(self, owner, variant):
    return True
    
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
class HintList(List):
  def __init__(self):
    super(HintList, self).__init__()
    
  def build(self, owner, variant):
    return True
        
  def addHint(self, hint):
    if not (isinstance(hint, Hint)):
      return False
    return super(HintList, self).add(hint)
    
class Variable(Element):
  def __init__(self, key = None, value = None):
    super(Variable, self).__init__()
    self.key = None
    self.value = None
    if (type(key) == Key):
      self.key = key
    if (type(value) == Value):
      self.value = value
      
  def build(self, owner, variant):
    return True
    
  def getContent(self):
    return self.key.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.key)+", "+self.toString(self.value)+">"
    
class VariableList(List):
  def __init__(self):
    super(VariableList, self).__init__()
    
  def build(self, owner, variant):
    return True
        
  def addVariable(self, variable):
    if not (isinstance(variable, Variable)):
      return False
    return super(VariableList, self).add(variable)
    
class Package(Element):
  def __init__(self, label = None, exports = None, hints = None, variables = None):
    super(Package, self).__init__()
    self.label = Label(String(""))
    if (type(label) == Label):
      self.label = label
    self.exports = None
    if (type(exports) == ExportList):
      self.exports = exports
    self.hints = None
    if (type(hints) == HintList):
      self.hints = hints
    self.variables = None
    if (type(variables) == VariableList):
      self.variables = variables
      
  def build(self, owner, variant):
    return True
    
  def getContent(self):
    return self.label.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.exports)+", "+self.toString(self.hints)+", "+self.toString(self.variables)+">"
    
class PackageList(List):
  def __init__(self):
    super(PackageList, self).__init__()
    
  def build(self, owner, variant):
    return True
        
  def addPackage(self, package):
    if not (isinstance(package, Package)):
      return False
    return super(PackageList, self).add(package)
    
class Module(Element):
  def __init__(self, label = None, exports = None):
    super(Module, self).__init__()
    self.label = Label(String(""))
    if (type(label) == Label):
      self.label = label
    self.exports = None
    if (type(exports) == ExportList):
      self.exports = exports
      
  def build(self, owner, variant):
    return True
    
  def getContent(self):
    return self.label.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.exports)+">"
    
class ModuleList(List):
  def __init__(self):
    super(ModuleList, self).__init__()
    
  def build(self, owner, variant):
    return True
        
  def addModule(self, module):
    if not (isinstance(module, Module)):
      return False
    return super(ModuleList, self).add(module)
    
class Definition(Object):
  def __init__(self, key = None, value = None):
    super(Definition, self).__init__()
    self.key = Key(String(""))
    if (type(key) == Key):
      self.key = key
    self.value = Value(String(""))
    if (type(value) == Value):
      self.value = value
      
  def getContent(self):
    return self.key.getContent()+"="+self.value.getContent()
      
  def __str__(self):
    return "<"+self.toString(self.key)+", "+self.toString(self.value)+">"
    
class DefinitionList(List):
  def __init__(self):
    super(DefinitionList, self).__init__()
    
  def build(self, owner, variant):
    return True
        
  def addDefinition(self, definition):
    if not (isinstance(definition, Definition)):
      return False
    return super(DefinitionList, self).add(definition)
    
class Link(Object):
  def __init__(self, string = None):
    super(Link, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
class LinkList(List):
  def __init__(self):
    super(LinkList, self).__init__()
    
  def build(self, owner, variant):
    return True
        
  def addLink(self, link):
    if not (isinstance(link, Link)):
      return False
    return super(LinkList, self).add(link)
    
class Export(Object):
  def __init__(self, key = None, value = None, export = None, exceptions = None):
    super(Export, self).__init__()
    self.key = None
    if (type(key) == Key):
      self.key = key
    self.value = None
    if (type(value) == Value):
      self.value = value
    self.export = None
    if (type(export) == String):
      self.export = export
    self.exceptions = None
    if (type(exceptions) == String):
      self.exceptions = exceptions
      
  def doExport(self, owner, variant):
    exceptions = None
    if not (self.exceptions == None):
      exceptions = self.exceptions.getContent()
    if not (isinstance(owner, Build)):
      return False
    if not (exceptions == None):
      if (owner.getLabel() in exceptions):
        return True
    owner.addExport(self, variant, exceptions)
    return True
      
  def __str__(self):
    return "<"+self.toString(self.key)+", "+self.toString(self.value)+", "+self.toString(self.export)+">"
    
class ExportList(List):
  def __init__(self):
    super(ExportList, self).__init__()
    
  def build(self, owner, variant):
    return True

  def doExport(self, owner, variant):
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Export)):
        if not (self.content[i].doExport(owner, variant)):
          return False
    return True

  def addExport(self, add):
    if not (isinstance(add, Export)):
      return False
    return super(ExportList, self).add(add)
    
class Import(Object):
  def __init__(self, label = None):
    super(Import, self).__init__()
    self.label = None
    if (type(label) == Label):
      self.label = label
      
  def getContent(self):
    return self.label.getContent()
    
  def doImport(self, owner, variant):
    if not (isinstance(owner, Build)):
      return False
    owner.addImport(self, variant)
    return True
    
  def __str__(self):
    return "<"+self.toString(self.label)+">"
    
class ImportList(List):
  def __init__(self):
    super(ImportList, self).__init__()
    
  def build(self, owner, variant):
    return True

  def doImport(self, owner, variant):
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Import)):
        if not (self.content[i].doImport(owner, variant)):
          return False
    return True

  def addImport(self, add):
    if not (isinstance(add, Import)):
      return False
    return super(ImportList, self).add(add)
    
class BuildInstruction(Object):
  def __init__(self, arguments = None, pre = None, post = None, timing = None):
    super(BuildInstruction, self).__init__()
    self.arguments = None
    if (type(arguments) == ArgumentList):
      self.arguments = arguments
    self.pre = None
    if (type(pre) == PreBuildInstruction):
      self.pre = pre
    self.post = None
    if (type(post) == PostBuildInstruction):
      self.post = post
    self.timing = None
    if (type(timing) == String):
      self.timing = timing
    
  def build(self, owner, path, subpath, installation, imports, variant):
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    return True
    
  def getPath(self, path, subpath):
    return os.path.join(path, subpath)
    
  def getPre(self):
    return self.pre
  
  def getPost(self):
    return self.post
  
  def __str__(self):
    return "<BuildInstruction()>"
    
class PreBuildInstruction(BuildInstruction):
  def __init__(self):
    super(PreBuildInstruction, self).__init__()
    self.instructions = []
      
  def build(self, owner, path, subpath, installation, imports, variant):
    length = len(self.instructions)
    for i in range(length):
      if (isinstance(self.instructions[i], BuildInstruction)):
        if not (self.instructions[i].build(owner, path, subpath, installation, imports, variant)):
          return False
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    return True
    
  def __str__(self):
    string = "<"
    length = len(self.instructions)
    for i in range(length):
      string += self.toString(self.instructions[i])
      if not (i == length-1):
        string += ", "
    string += ">"
    return string
    
class PostBuildInstruction(BuildInstruction):
  def __init__(self):
    super(PostBuildInstruction, self).__init__()
    self.instructions = []
      
  def build(self, owner, path, subpath, installation, imports, variant):
    length = len(self.instructions)
    for i in range(length):
      if (isinstance(self.instructions[i], BuildInstruction)):
        if not (self.instructions[i].build(owner, path, subpath, installation, imports, variant)):
          return False
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    return True
    
  def __str__(self):
    string = "<"
    length = len(self.instructions)
    for i in range(length):
      string += self.toString(self.instructions[i])
      if not (i == length-1):
        string += ", "
    string += ">"
    return string
    
class CmakeBuildInstruction(BuildInstruction):
  def __init__(self, arguments = None, generator = None, source = None):
    super(CmakeBuildInstruction, self).__init__(arguments)
    self.generator = None
    if (type(generator) == Generator):
      self.generator = generator
    self.source = None
    if (type(source) == Path):
      self.source = source
      
  def build(self, owner, path, subpath, installation, imports, variant):
    if (self.generator == None):
      return False
    if (self.source == None):
      return False
    if (self.arguments == None):
      return False
    cmake = self.getPath(path, subpath)
    arguments = self.arguments.getContent()
    exports = owner.getExports(imports, variant, [self])
    if (variant in imports):
      for i in range(len(exports)):
        export = exports[i]
        if (export[0] in imports[variant]):
          export = export[1]
          for key in export:
            if (export[key][0] == "other"):
              arguments.append("-D"+key+"=\""+export[key][1].replace("\\", "/")+"\"")
            else:
              arguments.append("-D"+key+"="+export[key][1].replace("\\", "/"))
    if not (self.getPre() == None):
      if not (self.getPre().timing == None):
        if (self.getPre().timing.getContent() == "build"):
          if not (self.getPre().build(owner, path, subpath, installation, imports, variant)):
            return False
      else:
        if not (self.getPre().build(owner, path, subpath, installation, imports, variant)):
          return False
    if not (self.buildVariant(owner, arguments, cmake, installation, variant)):
      return False
    if not (self.getPost() == None):
      if not (self.getPost().timing == None):
        if (self.getPost().timing.getContent() == "build"):
          if not (self.getPost().build(owner, path, subpath, installation, imports, variant)):
            return False
      else:
        if not (self.getPost().build(owner, path, subpath, installation, imports, variant)):
          return False
    return True

  def buildVariant(self, owner, arguments, cmake, installation, variant):
    generator = None
    architecture = None
    if not (self.generator == None):
      generator = self.generator.getContent()
      if not (self.generator.architecture == None):
        architecture = self.generator.architecture.getContent()
    path = os.path.join(cmake, variant.lower()).replace("\\", "/")
    result = cmake_configure(generator, architecture, arguments+["-DCMAKE_BUILD_TYPE="+variant], os.path.join(path, "..", self.source.getContent()).replace("\\", "/"), path, installation, variant)
    owner.getContext().log(self.node, result)
    result = cmake_build(os.path.join(cmake, variant.lower()).replace("\\", "/"), variant)
    owner.getContext().log(self.node, result)
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    cmake = self.getPath(path, subpath)
    if not (self.installVariant(owner, cmake, installation, variant)):
      return False
    return True

  def installVariant(self, owner, cmake, installation, variant):
    result = cmake_install(os.path.join(cmake, variant.lower()).replace("\\", "/"), variant, os.path.join(installation, variant.lower()).replace("\\", "/"))
    owner.getContext().log(self.node, result)
    return True
    
  def __str__(self):
    return "<"+self.toString(self.arguments)+", "+self.toString(self.generator)+", "+self.toString(self.source)+">"
    
class ShellsBuildInstruction(BuildInstruction):
  def __init__(self, arguments = None, generator = None, source = None):
    super(ShellsBuildInstruction, self).__init__(arguments)
    self.shells = []
    
  def build(self, owner, path, subpath, installation, imports, variant):
    length = len(self.shells)
    if not (self.getPre() == None):
      if not (self.getPre().timing == None):
        if (self.getPre().timing.getContent() == "build"):
          if not (self.getPre().build(owner, path, subpath, installation, imports, variant)):
            return False
      else:
        if not (self.getPre().build(owner, path, subpath, installation, imports, variant)):
          return False
    for i in range(length):
      if ("ShellBuildInstruction" in str(type(self.shells[i]))):
        if not (self.shells[i].build(owner, path, subpath, installation, imports, variant)):
          return False
      else:
        owner.getContext().log(self.node, str(type(self.shells[i])))
        return False
    if not (self.getPost() == None):
      if not (self.getPost().timing == None):
        if (self.getPost().timing.getContent() == "build"):
          if not (self.getPost().build(owner, path, subpath, installation, imports, variant)):
            return False
      else:
        if not (self.getPost().build(owner, path, subpath, installation, imports, variant)):
          return False
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.shells)+">"
    
class ShellBuildInstruction(BuildInstruction):
  def __init__(self, commands = None, work = None):
    super(ShellBuildInstruction, self).__init__()
    self.commands = None
    self.work = None
      
  def build(self, owner, path, subpath, installation, imports, variant):
    if (self.commands == None):
      return False
    if not ("CommandsBuildInstruction" in str(type(self.commands))):
      return False
    if (self.work == None):
      return False
    if not ("Work" in str(type(self.work))):
      return False
    owner.getContext().work = self.work.getContent()
    if not (self.commands.build(owner, self.getPath(path, subpath), self.work.getContent(), installation, imports, variant)):
      return False
    owner.getContext().work = None
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.commands)+">"

class CommandsBuildInstruction(BuildInstruction):
  def __init__(self, arguments = None, generator = None, source = None):
    super(CommandsBuildInstruction, self).__init__(arguments)
    self.commands = []
      
  def build(self, owner, path, subpath, installation, imports, variant):
    length = len(self.commands)
    for i in range(length):
      if ("CommandBuildInstruction" in str(type(self.commands[i]))):
        if not (self.commands[i].build(owner, path, subpath, installation, imports, variant)):
          return False
      else:
        owner.getContext().log(self.node, str(type(self.commands[i])))
        return False
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.commands)+">"
    
class CommandBuildInstruction(BuildInstruction):
  def __init__(self, arguments = None, generator = None, source = None):
    super(CommandBuildInstruction, self).__init__(arguments)
    self.string = None
    self.extracts = []
    self.copies = []
    self.deletes = []
    self.writes = []
    self.setters = []
    
  def build(self, owner, path, subpath, installation, imports, variant):
    mature = False
    if not (os.path.isdir(subpath)):
      if (contains(wd(), subpath)):
        os.makedirs(subpath)
    if not (len(self.extracts) == 0):
      for i in range(len(self.extracts)):
        extract = self.extracts[i]
        if (extract == None):
          continue
        if not (extract.perform(owner.getContext())):
          return False
      mature = True
    if not (len(self.copies) == 0):
      for i in range(len(self.copies)):
        copy = self.copies[i]
        if (copy == None):
          continue
        if not (copy.perform(owner.getContext())):
          return False
      mature = True
    if not (len(self.deletes) == 0):
      for i in range(len(self.deletes)):
        delete = self.deletes[i]
        if (delete == None):
          continue
        if not (delete.perform(owner.getContext())):
          return False
      mature = True
    if not (len(self.writes) == 0):
      for i in range(len(self.writes)):
        wrote = self.writes[i]
        if (wrote == None):
          continue
        if not (wrote.perform(owner.getContext())):
          return False
      mature = True
    if not (len(self.setters) == 0):
      for i in range(len(self.setters)):
        setter = self.setters[i]
        if (setter == None):
          continue
        if not (setter.perform(owner.getContext())):
          return False
      mature = True
    if (mature):
      return True
    if (self.string == None):
      return False
    command = shlex.split(self.string.getContent().replace("\\", "/"))
    owner.getContext().log(self.node, self.string.getContent())
    owner.getContext().log(self.node, str(command))
    owner.getContext().log(self.node, subpath)
    cwd = os.getcwd()
    os.chdir(subpath)
    result = execute_command(command, owner.getContext().environment)
    os.chdir(cwd)
    #owner.getContext().log(self.node, result)
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.string)+", "+self.toString(self.extracts)+", "+self.toString(self.copies)+", "+self.toString(self.deletes)+", "+self.toString(self.writes)+", "+self.toString(self.setters)+">"
    
class Setter(BuildInstruction, Performer):
  def __init__(self, key = None, value = None):
    super(Setter, self).__init__()
    self.key = None
    if (type(key) == Key):
      self.key = key
    self.value = None
    if (type(value) == Value):
      self.value = value
      
  def build(self, owner, path, subpath, installation, imports, variant):
    return self.perform(owner.getContext())
    
  def perform(self, context):
    if not ((self.key == None) or (self.value == None)):
      context.data[self.key.getContent()] = self.value.getContent()
      context.environment[self.key.getContent()] = self.value.getContent()
      context.log(self.node, "<\""+self.key.getContent()+"\" -> \""+self.value.getContent()+"\">")
      return True
    return False
    
  def install(self, owner, path, subpath, installation):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.key)+", "+self.toString(self.value)+">"

class Dependency(Build):
  def __init__(self, subpath = None, label = None, instruction = None, imports = None, exports = None):
    super(Dependency, self).__init__()
    self.subpath = None
    if (type(subpath) == Path):
      self.subpath = subpath
    self.label = None
    if (type(label) == Label):
      self.label = label
    self.instruction = None
    if (type(instruction) == BuildInstruction):
      self.instruction = instruction
    self.imports = None
    if (type(imports) == ImportList):
      self.imports = imports
    self.exports = None
    if (type(exports) == ExportList):
      self.exports = exports
    
  def build(self, owner, variant):
    success = True
    if not (self.imports == None):
      success = self.imports.doImport(self, variant)
    if not (success):
      return False
    if not (self.exports == None):
      success = self.exports.doExport(self, variant)
    if not (success):
      return False
    success = super(Dependency, self).build(owner, variant)
    if not (success):
      return False
    return True
    
  def distribute(self, owner, distribution, variant):
    context = owner.getContext()
    exports = self.getExports(variant, self)
    if not (type(exports) == dict):
      return False
    for key in exports:
      export = exports[key]
      if (export[0] == "libraries"):
        if (os.path.isdir(export[1])):
          for root, folders, files in os.walk(export[1]):
            for name in files:
              if (context.exclude(name)):
                continue
              if not (os.path.exists(os.path.join(distribution, variant.lower(), name))):
                if not (move(os.path.join(root, name).replace("\\", "/"), os.path.join(distribution, variant.lower(), name).replace("\\", "/"))):
                  return False
        elif (os.path.isfile(export[1])):
          if not (os.path.exists(os.path.join(distribution, variant.lower(), os.path.basename(export[1])))):
            if not (move(export[1].replace("\\", "/"), os.path.join(distribution, variant.lower(), os.path.basename(export[1])).replace("\\", "/"))):
              return False
          if (os.path.isdir(os.path.dirname(export[1]))):
            for root, folders, files in os.walk(os.path.dirname(export[1])):
              for name in files:
                if (context.exclude(name)):
                  continue
                if not (os.path.exists(os.path.join(distribution, variant.lower(), name))):
                  if not (move(os.path.join(root, name).replace("\\", "/"), os.path.join(distribution, variant.lower(), name).replace("\\", "/"))):
                    return False
      elif (export[0] == "all"):
        if (os.path.isdir(export[1])):
          if (os.path.isdir(os.path.join(export[1], "bin"))):
            for root, folders, files in os.walk(os.path.join(export[1], "bin")):
              for name in files:
                if (context.exclude(name)):
                  continue
                if not (os.path.exists(os.path.join(distribution, variant.lower(), name))):
                  if not (move(os.path.join(root, name).replace("\\", "/"), os.path.join(distribution, variant.lower(), name).replace("\\", "/"))):
                    return False
          if (os.path.isdir(os.path.join(export[1], "lib"))):
            for root, folders, files in os.walk(os.path.join(export[1], "lib")):
              for name in files:
                if (context.exclude(name)):
                  continue
                if not (os.path.exists(os.path.join(distribution, variant.lower(), name))):
                  if not (move(os.path.join(root, name).replace("\\", "/"), os.path.join(distribution, variant.lower(), name).replace("\\", "/"))):
                    return False
    return True
    
  def getPath(self, owner, variant, purpose):
    return adjust(os.path.join(wd(), owner.getContext().root.directory.getContent(), owner.directory.getContent(), purpose, "dependencies", self.label.getContent()))
    
  def getLabel(self):
    return self.label.getContent()
    
  def doExport(self, key, value, export, variant, exceptions):
    return True
    
  def doImport(self, label, variant):
    return True
    
  def getExports(self, variant, need):
    return {}

class RemoteDependency(Dependency):
  def __init__(self, url = None):
    super(RemoteDependency, self).__init__()
    self.url = None
    if (type(url) == URL):
      self.url = url
      
  def build(self, owner, variant):
    success = super(RemoteDependency, self).build(owner, variant)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export, variant, exceptions):
    return True
    
  def doImport(self, label, variant):
    return True
    
  def getExports(self, variant, need):
    return {}

class DependencyList(List):
  def __init__(self):
    super(DependencyList, self).__init__()
    self.owner = None
    self.directory = None
    
  def build(self, owner, variant):
    self.owner = owner
    self.directory = self.owner.directory
    context = self.getContext()
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Dependency)):
        if ("BUILDSTER_BUILD" in context.data):
          if not (self.content[i].label == None):
            if not (self.content[i].label.getContent() == context.data["BUILDSTER_BUILD"]):
              if not (self.content[i].imports == None):
                if not (self.content[i].imports.doImport(self.content[i], variant)):
                  return False
              if not (self.content[i].exports == None):
                if not (self.content[i].exports.doExport(self.content[i], variant)):
                  return False
              continue
        if not (self.content[i].build(self, variant)):
          self.getContext().log(self.node, "Dependency build failure @ "+str(i)+"!")
          return False
    return True
    
  def distribute(self, owner, distribution, variant):
    self.owner = owner
    self.directory = self.owner.directory
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Dependency)):
        if not (self.content[i].distribute(self, distribution, variant)):
          self.getContext().log(self.node, "Dependency distribution failure @ "+str(i)+"!")
          return False
    return True
        
  def addDependency(self, dependency):
    if not (isinstance(dependency, Dependency)):
      return False
    return super(DependencyList, self).add(dependency)
    
  def getExports(self, imports, variant, need):
    if (need == None):
      return self.owner.getExports(imports, variant, [self])
    if (len(need) == 0):
      return self.owner.getExports(imports, variant, [self])
    exports = self.owner.getExports(imports, variant, need+[self])
    length = len(self.content)
    if not (variant in imports):
      return exports
    for i in range(length):
      if (isinstance(self.content[i], Dependency)):
        label = self.content[i].getLabel()
        if (label in imports[variant]):
          if not (self.content[i] in need):
            exports.append([label, self.content[i].getExports(variant, need[0])])
    return exports
    
  def getTargets(self):
    if (self.owner == None):
      return None
    return self.owner.getTargets()
    
  def getDependencies(self):
    return self
    
  def getContext(self):
    if (self.owner == None):
      return None
    return self.owner.getContext()

class LocalDependency(Dependency):
  def __init__(self, path = None):
    super(LocalDependency, self).__init__()
    self.exportsContent = {}
    self.importsContent = {}
    self.path = None
    if (type(path) == String):
      self.path = path
    
  def build(self, owner, variant):
    installation = self.getPath(owner, None, "install")
    path = self.getPath(owner, None, "build")
    success = super(LocalDependency, self).build(owner, variant)
    if not (success):
      return False
    if (self.instruction == None):
      return False
    success = self.instruction.build(owner, path, self.subpath.getContent(), installation, self.importsContent[variant], variant)
    if not (success):
      return False
    success = self.instruction.install(owner, path, self.subpath.getContent(), installation, variant)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export, variant, exceptions):
    if not (variant in self.exportsContent):
      self.exportsContent[variant] = {}
    if (key in self.exportsContent[variant]):
      return False
    self.exportsContent[variant][key] = [export, value, exceptions]
    return True
    
  def doImport(self, label, variant):
    if not (variant in self.importsContent):
      self.importsContent[variant] = []
    if (label in self.importsContent[variant]):
      return False
    self.importsContent[variant].append(label)
    return True
    
  def getExports(self, variant, need):
    if not (variant in self.exportsContent):
      self.exportsContent[variant] = {}
    exportsContent = self.filterExports(self.exportsContent[variant], need)
    return exportsContent

  def __str__(self):
    return "<"+self.toString(self.subpath)+", "+self.toString(self.path)+", "+self.toString(self.instruction)+", "+self.toString(self.imports)+", "+self.toString(self.exports)+">"

class Username(Object):
  def __init__(self, string = None):
    super(Username, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
class Password(Object):
  def __init__(self, string = None):
    super(Password, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"

class Credentials(Object):
  def __init__(self, username = None, password = None):
    super(Credentials, self).__init__()
    self.username = None
    self.password = None
    if (type(username) == Username):
      self.username = username
    if (type(password) == Password):
      self.password = password
    
  def __str__(self):
    return "<"+self.toString(self.username)+", "+self.toString(self.password)+">"
    
class GitRepoDependency(RemoteDependency):
  def __init__(self, url = None, branch = None, credentials = None):
    super(GitRepoDependency, self).__init__(url)
    self.exportsContent = {}
    self.importsContent = {}
    self.branch = None
    if (type(branch) == Branch):
      self.branch = branch
    self.credentials = None
    if (type(credentials) == Credentials):
      self.credentials = credentials
    
  def clone(self, owner, path):
    if (self.url == None):
      return False
    if (self.branch == None):
      return False
    if (self.label == None):
      return False
    if not (os.path.isdir(path)):
      result = git_clone(self.url.getContent(), path)
      owner.getContext().log(self.node, result)
    cwd = os.getcwd()
    os.chdir(path)
    result = git_checkout(self.branch.getContent())
    owner.getContext().log(self.node, result)
    result = git_submodule()
    owner.getContext().log(self.node, result)
    os.chdir(cwd)
    return True
    
  def build(self, owner, variant):
    installation = self.getPath(owner, None, "install")
    path = self.getPath(owner, None, "build")
    success = self.clone(owner, path)
    if not (success):
      return False
    success = super(GitRepoDependency, self).build(owner, variant)
    if not (success):
      return False
    if (self.instruction == None):
      return False
    success = self.instruction.build(owner, path, self.subpath.getContent(), installation, self.importsContent, variant)
    if not (success):
      return False
    success = self.instruction.install(owner, path, self.subpath.getContent(), installation, variant)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export, variant, exceptions):
    if not (variant in self.exportsContent):
      self.exportsContent[variant] = {}
    if (key in self.exportsContent[variant]):
      return False
    self.exportsContent[variant][key] = [export, value, exceptions]
    return True
    
  def doImport(self, label, variant):
    if not (variant in self.importsContent):
      self.importsContent[variant] = []
    if (label in self.importsContent[variant]):
      return False
    self.importsContent[variant].append(label)
    return True
    
  def getExports(self, variant, need):
    if not (variant in self.exportsContent):
      self.exportsContent[variant] = {}
    exportsContent = self.filterExports(self.exportsContent[variant], need)
    return exportsContent
    
  def __str__(self):
    return "<"+self.toString(self.subpath)+", "+self.toString(self.url)+", "+self.toString(self.branch)+", "+self.toString(self.credentials)+", "+self.toString(self.instruction)+">"
    
class WGetDependency(RemoteDependency):
  def __init__(self, url = None, string = None):
    super(WGetDependency, self).__init__(url)
    self.exportsContent = {}
    self.importsContent = {}
    self.string = None
    if (type(string) == String):
      self.string = string
    
  def build(self, owner, variant):
    if (self.string == None):
      return False
    content = self.string.getContent()
    installation = self.getPath(owner, None, "install")
    path = self.getPath(owner, None, "build")
    if (content == None):
      return False
    content = content.strip()
    if (len(content) == 0):
      return False
    if not (os.path.isdir(path)):
      if (contains(wd(), path)):
        os.makedirs(path)
    success = True
    if not (os.path.exists(os.path.join(path, content))):
      try:
        filename = wget.download(self.url.getContent(), out=path)
        if (filename == None):
          success = False
        else:
          if not (os.path.exists(os.path.join(path, filename))):
            success = False
          else:
            if not (move(os.path.join(path, filename), os.path.join(path, content))):
              success = False
            else:
              if not (os.path.exists(os.path.join(path, content))):
                success = False
      except:
        success = False
    if not (success):
      return False
    success = super(WGetDependency, self).build(owner, variant)
    if not (success):
      return False
    if (self.instruction == None):
      return False
    success = self.instruction.build(owner, path, self.subpath.getContent(), installation, self.importsContent, variant)
    if not (success):
      return False
    success = self.instruction.install(owner, path, self.subpath.getContent(), installation, variant)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export, variant, exceptions):
    if not (variant in self.exportsContent):
      self.exportsContent[variant] = {}
    if (key in self.exportsContent[variant]):
      return False
    self.exportsContent[variant][key] = [export, value, exceptions]
    return True
    
  def doImport(self, label, variant):
    if not (variant in self.importsContent):
      self.importsContent[variant] = []
    if (label in self.importsContent[variant]):
      return False
    self.importsContent[variant].append(label)
    return True
    
  def getExports(self, variant, need):
    if not (variant in self.exportsContent):
      self.exportsContent[variant] = {}
    exportsContent = self.filterExports(self.exportsContent[variant], need)
    return exportsContent
    
  def __str__(self):
    return "<"+self.toString(self.subpath)+", "+self.toString(self.url)+", "+self.toString(self.string)+", "+self.toString(self.instruction)+">"
    
    
class Target(Build):
  def __init__(self, label = None, subpath = None, definitions = None, links = None, imports = None, exports = None, generator = None, pre = None, post = None, arguments = None, packages = None, modules = None, linkage = None):
    super(Target, self).__init__()
    self.label = None
    self.subpath = None
    self.importsContent = {}
    self.exportsContent = {}
    if (type(label) == Label):
      self.label = label
    self.definitions = None
    if (type(definitions) == DefinitionList):
      self.definitions = definitions
    self.links = None
    if (type(links) == LinkList):
      self.links = links
    self.imports = None
    if (type(imports) == ImportList):
      self.imports = imports
    self.exports = None
    if (type(exports) == ExportList):
      self.exports = exports
    self.generator = None
    if (type(generator) == Generator):
      self.generator = generator
    self.pre = None
    if (type(pre) == PreBuildInstruction):
      self.pre = pre
    self.post = None
    if (type(post) == PostBuildInstruction):
      self.post = post
    self.arguments = None
    if (type(arguments) == ArgumentList):
      self.arguments = arguments
    self.packages = None
    if (type(packages) == PackageList):
      self.packages = packages
    self.modules = None
    if (type(modules) == ModuleList):
      self.modules = modules
    self.linkage = None
    if (type(linkage) == String):
      self.linkage = linkage
      
  def install(self, owner, path, installation, variant):
    result = cmake_install(path, variant, installation)
    owner.getContext().log(self.node, result)
    return True
    
  def build(self, owner, variant):
    context = owner.owner.getContext()
    installation = self.getPath(owner.owner, variant, "install")
    subpath = self.getPath(owner.owner, variant, None)
    path = self.getPath(owner.owner, variant, "build")
    success = True
    if not (self.imports == None):
      success = self.imports.doImport(self, variant)
    if not (success):
      context.log(self.node, "Import failure!")
      return False
    if not (self.exports == None):
      success = self.exports.doExport(self, variant)
    if not (success):
      context.log(self.node, "Export failure!")
      return False
    success = super(Target, self).build(owner.owner, variant)
    if not (success):
      context.log(self.node, "Super build failure!")
      return False
    links = []
    builds = []
    labels = {}
    imports = {}
    exports = {}
    includes = []
    linkages = []
    project = []
    packages = []
    definitions = []
    modules = []
    arguments = []
    for i in range(len(owner.getDependencies().getContent())):
      dependency = owner.getDependencies().getContent()[i]
      if not (dependency == self):
        builds.append(dependency)
    for i in range(len(owner.getTargets().getContent())):
      target = owner.getTargets().getContent()[i]
      if not (target == self):
        builds.append(target)
    for i in range(len(builds)):
      if not ("Executable" in str(type(builds[i]))):
        label = builds[i].label.getContent()
        labels[label] = builds[i]
      else:
        builds[i] = None
    for label in labels:
      if not (self.imports == None):
        for i in range(len(self.imports.content)):
          if (label == self.imports.content[i].getContent()):
            if not (label in imports):
              if ("Target" in str(type(labels[label]))):
                linkages = linkages+labels[label].getLinkages(owner, variant)
                includes = includes+labels[label].getIncludes(owner)
              imports[label] = []
              if not (labels[label].exports == None):
                for j in range(len(labels[label].exports.content)):
                  export = labels[label].exports.content[j]
                  imports[label].append(export)
    for label in imports:
      for i in range(len(imports[label])):
        export = imports[label][i]
        key = export.key.getContent()
        value = export.value.getContent()
        if not (key in exports):
          exports[key] = [value, export.export.getContent()]
    if not (self.pre == None):
      if not (self.pre.timing == None):
        if not (self.pre.timing.getContent() == "build"):
          success = False
      if (success):
        success = self.pre.build(owner, subpath, path, installation, imports, variant)
      else:
        success = True
    if not (success):
      context.log(self.node, "Pre build step failure!")
      return False
    if not (os.path.isdir(path)):
      if (contains(wd(), path)):
        os.makedirs(path)
    if not (self.packages == None):
      packages = packages+self.packages.content
    if not (self.modules == None):
      modules = modules+self.modules.content
    if not (self.definitions == None):
      definitions = definitions+self.definitions.getContent()
    if not (self.arguments == None):
      arguments = arguments+self.arguments.getContent()
    project = unique(project+self.getFiles(owner))
    includes = unique(includes+self.getIncludes(owner))
    files = self.getFiles(owner, "CMakeLists\\.txt")
    temp = "."
    if not (self.subpath == None):
      temp = self.subpath.getContent()
    if not ((os.path.join(self.getPath(owner, variant, None), "CMakeLists.txt").replace("\\", "/") in files) or (os.path.join(self.getPath(owner, variant, None), temp, "CMakeLists.txt").replace("\\", "/") in files)):
      descriptor = open(os.path.join(path, "CMakeLists.txt"), "w")
      base = path
      write(descriptor, "cmake_minimum_required(VERSION 3.12.0 FATAL_ERROR)")
      if not (context == None):
        if not (context.project == None):
          if not (context.project.cmake_modules == None):
            if not (context.project.directory == None):
              cmake_modules = os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), context.project.cmake_modules.getContent()).replace("\\", "/")
              if (os.path.isdir(cmake_modules)):
                cmake_modules = relativize(base, cmake_modules).replace("\\", "/")
                write(descriptor, "set(CMAKE_MODULE_PATH \"${CMAKE_CURRENT_LIST_DIR}/"+cmake_modules+"\")")
      write(descriptor, "project(\""+self.label.getContent()+"Project\")")
      write(descriptor, "set(BUILDSTER_HEADERS )")
      write(descriptor, "set(BUILDSTER_FILES )")
      for i in range(len(arguments)):
        argument = arguments[i]
        if (len(argument) > 2):
          if (argument[:2] == "-D"):
            argument = argument[2:].split("=")
            if (len(argument) > 1):
              key = argument[0]
              value = ""
              argument = argument[1:]
              for j in range(len(argument)):
                value += argument[j]
              write(descriptor, "set("+key+" "+value+")")
      for i in range(len(modules)):
        module = modules[i]
        if (module == None):
          continue
        if not (module.exports == None):
          for j in range(len(module.exports.content)):
            export = module.exports.content[j]
            if (export == None):
              continue
            if (export.key == None):
              continue
            if (len(export.key.getContent()) == 0):
              continue
            write(descriptor, "set("+export.key.getContent()+" )")
        if (os.path.isfile(module.getContent())):
          write(descriptor, "include(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, module.getContent()).replace("\\", "/")+"\")")
        else:
          write(descriptor, "include("+module.getContent()+")")
        if not (module.exports == None):
          for j in range(len(module.exports.content)):
            export = module.exports.content[j]
            if (export == None):
              continue
            if (export.export == None):
              continue
            if (export.key == None):
              continue
            if (export.export.getContent() == "headers"):
              if not (export.value == None):
                if not (len(export.value.getContent()) == 0):
                  if (os.path.isdir(export.value.getContent())):
                    write(descriptor, "include_directories(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, export.value.getContent()).replace("\\", "/")+"\")")
                  else:
                    write(descriptor, "include_directories("+export.value.getContent()+")")
                else:
                  write(descriptor, "include_directories(${"+export.key.getContent()+"})")
              else:
                write(descriptor, "include_directories(${"+export.key.getContent()+"})")
            elif (export.export.getContent() == "libraries"):
              if not (export.value == None):
                if not (len(export.value.getContent()) == 0):
                  if (os.path.isdir(export.value.getContent())):
                    write(descriptor, "link_libraries(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, export.value.getContent()).replace("\\", "/")+"\")")
                  else:
                    write(descriptor, "link_libraries("+export.value.getContent()+")")
                else:
                  write(descriptor, "link_libraries(${"+export.key.getContent()+"})")
              else:
                write(descriptor, "link_libraries(${"+export.key.getContent()+"})")
            elif (export.export.getContent() == "files"):
              write(descriptor, "list(APPEND BUILDSTER_FILES ${"+export.key.getContent()+"})")
            else:
              pass
      for i in range(len(definitions)):
        definition = definitions[i]
        write(descriptor, "add_definitions(-D"+definition+")")
      for i in range(len(includes)):
        include = includes[i]
        write(descriptor, "include_directories(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, include.replace("\\", "/"))+"\")")
      for export in exports:
        if (exports[export][1] == "headers"):
          headers = exports[export][0].replace("\\", "/")
          if not (os.path.isdir(headers)):
            if (contains(wd(), headers)):
              os.makedirs(headers)
          write(descriptor, "include_directories(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, headers.replace("\\", "/"))+"\")")
        elif (exports[export][1] == "libraries"):
          libraries = exports[export][0].replace("\\", "/")
          if not (os.path.isdir(libraries)):
            if (contains(wd(), libraries)):
              os.makedirs(libraries)
          for root, folders, files in os.walk(libraries):
            for name in files:
              for i in range(len(owner.getContext().libraries)):
                if (name.endswith("."+owner.getContext().libraries[i])):
                  links.append(str(root).replace("\\", "/"))
                  write(descriptor, "link_directories(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, links[len(links)-1])+"\")")
                  name = None
                  break
              if (name == None):
                break
        else:
          pass
      for i in range(len(linkages)):
        linkage = linkages[i]
        links.append(linkage.replace("\\", "/"))
        write(descriptor, "link_directories(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, links[len(links)-1])+"\")")
      if not (self.links == None):
        for i in range(len(self.links.content)):
          link = self.links.content[i].getContent().strip()
          if ("*" in link):
            for j in range(len(links)):
              for root, folders, files in os.walk(links[j]):
                for name in files:
                  if (link.replace("*", "") in name):
                    for k in range(len(owner.getContext().libraries)):
                      if (name.endswith("."+owner.getContext().libraries[k])):
                        write(descriptor, "link_libraries(\""+name+"\")")
                        break
          else:
            write(descriptor, "link_libraries("+link+")")
      if (platform.system() == "Linux"):
        write(descriptor, "find_package(PkgConfig REQUIRED)")
      for i in range(len(packages)):
        package = packages[i]
        if (package == None):
          continue
        hints = None
        variables = None
        if not (package.hints == None):
          hints = ""
          for j in range(len(package.hints.content)):
            if (j+1 < len(package.hints.content)):
              hints += " "
            hint = package.hints.content[j]
            if (hint == None):
              continue
            hint = hint.getContent()
            hints += hint
          if (len(hints) == 0):
            hints = None
        if not (package.variables == None):
          variables = []
          for j in range(len(package.variables.content)):
            variable = package.variables.content[j]
            if (variable == None):
              continue
            if ((variable.key == None) or (variable.value == None)):
              continue
            variable = "set("+variable.key.getContent()+" "+variable.value.getContent()+")"
            variables.append(variable)
          if (len(variables) == 0):
            variables = None
        if (hints == None):
          write(descriptor, "find_package("+package.getContent()+" REQUIRED)")
        else:
          write(descriptor, "pkg_search_module("+package.getContent()+" REQUIRED "+hints+")")
        if not (variables == None):
          for variable in variables:
            write(descriptor, variable)
        if not (package.exports == None):
          for j in range(len(package.exports.content)):
            export = package.exports.content[j]
            if (export == None):
              continue
            if (export.export == None):
              continue
            if (export.key == None):
              continue
            if (export.export.getContent() == "headers"):
              write(descriptor, "include_directories(${"+export.key.getContent()+"})")
            elif (export.export.getContent() == "libraries"):
              write(descriptor, "link_libraries(${"+export.key.getContent()+"})")
            else:
              pass
      if (platform.system() == "Linux"):
        write(descriptor, "find_package(Threads REQUIRED)")
        write(descriptor, "link_libraries(${CMAKE_THREAD_LIBS_INIT})")
      if (len(project) > 0):
        target = str(type(self))
        for i in range(len(project)):
          for j in range(len(owner.getContext().extensions)):
            extension = "."+owner.getContext().extensions[j]
            if (project[i].endswith(extension)):
              write(descriptor, "list(APPEND BUILDSTER_FILES \"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, project[i].replace("\\", "/"))+"\")")
              if ("Library" in target):
                for k in range(len(owner.getContext().headers)):
                  if (extension == "."+owner.getContext().headers[k]):
                    write(descriptor, "list(APPEND BUILDSTER_HEADERS \"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, project[i].replace("\\", "/"))+"\")")
                    break
              break
        if ("Executable" in target):
          write(descriptor, "add_executable("+self.label.getContent()+" ${BUILDSTER_FILES})")
          if (platform.system() == "Darwin"):
            write(descriptor, "add_custom_command(TARGET "+self.label.getContent()+" POST_BUILD COMMAND ${CMAKE_INSTALL_NAME_TOOL} -add_rpath \"@executable_path/\" $<TARGET_FILE:"+self.label.getContent()+"> || :)")
          write(descriptor, "target_compile_features("+self.label.getContent()+" PRIVATE cxx_std_"+context.root.cpp.getContent()+")")
        elif ("Library" in target):
          if (self.linkage == None):
            write(descriptor, "add_library("+self.label.getContent()+" ${BUILDSTER_FILES})")
          else:
            write(descriptor, "add_library("+self.label.getContent()+" "+self.linkage.getContent().upper()+" "+"${BUILDSTER_FILES})")
          write(descriptor, "set_target_properties("+self.label.getContent()+" PROPERTIES PUBLIC_HEADER \"${BUILDSTER_HEADERS}\")")
          write(descriptor, "target_compile_features("+self.label.getContent()+" PRIVATE cxx_std_"+context.root.cpp.getContent()+")")
        else:
          pass
        write(descriptor, "install(TARGETS "+self.label.getContent()+")")
      else:
        context.log(self.node, "Source failure!")
        return False
      descriptor.close()
    else:
      path = self.getPath(owner, variant, None)
    generator = None
    architecture = None
    if (self.generator == None):
      generator = self.getGenerator(owner)
    else:
      generator = self.generator.getContent()
      if not (self.generator.architecture == None):
        architecture = self.generator.architecture.getContent()
    if (generator == None):
      context.log(self.node, "Generator failure!")
      return False
    exports = owner.getExports(self.importsContent, variant, [self])
    if (variant in self.importsContent):
      for i in range(len(exports)):
        export = exports[i]
        if (export[0] in self.importsContent[variant]):
          export = export[1]
          for key in export:
            if (export[key][0] == "other"):
              arguments.append("-D"+key+"=\""+export[key][1].replace("\\", "/")+"\"")
            else:
              arguments.append("-D"+key+"="+export[key][1].replace("\\", "/"))
    success = self.buildVariant(owner, generator, architecture, arguments, path, installation, variant)
    if not (success):
      context.log(self.node, "Build failure!")
      return False
    if not (self.post == None):
      if not (self.post.timing == None):
        if not (self.post.timing.getContent() == "build"):
          success = False
      if (success):
        success = self.post.build(owner, subpath, path, installation, imports, variant)
      else:
        success = True
    if not (success):
      context.log(self.node, "Post build step failure!")
      return False
    return True

  def buildVariant(self, owner, generator, architecture, arguments, path, installation, variant):
    if (self.subpath == None):
      result = cmake_configure(generator, architecture, arguments+["-DCMAKE_BUILD_TYPE="+variant], path, os.path.join(path, "build").replace("\\", "/"), installation, None)
    else:
      result = cmake_configure(generator, architecture, arguments+["-DCMAKE_BUILD_TYPE="+variant], os.path.join(path, self.subpath.getContent()), os.path.join(path, "build").replace("\\", "/"), installation, None)
    owner.getContext().log(self.node, result)
    result = cmake_build(os.path.join(path, "build").replace("\\", "/"), variant)
    owner.getContext().log(self.node, result)
    success = self.install(owner, os.path.join(path, "build").replace("\\", "/"), installation.replace("\\", "/"), variant)
    return success
    
  def distribute(self, owner, distribution, variant):
    target = str(type(self))
    prefixes = [""]
    if ("Library" in target):
      prefixes = prefixes+["lib"]
    installation = find(os.path.join(self.getPath(owner, variant, "install")).replace("\\", "/"), self.label.getContent(), prefixes)
    if (installation == None):
      return False
    source = installation.replace("\\", "/")
    destination = os.path.join(distribution, variant.lower(), os.path.basename(installation)).replace("\\", "/")
    if not (move(source, destination)):
      return False
    if not (platform.system() == "Linux"):
      return True
    success = True
    if ("Executable" in target):
      if (os.path.exists(destination)):
        if (os.path.isfile(destination)):
          patcher = None
          try:
            patcher = importlib.import_module("pypatchelf")
          except:
            patcher = None
          if not (patcher == None):
            try:
              command = []
              command.append(patcher.PATCHELF)
              command.append("--set-rpath")
              command.append("$ORIGIN")
              command.append(destination)
              result = execute_command(command)
              #owner.getContext().log(self.node, result)
              success = True
            except:
              success = False
          else:
            success = False
    return success

  def doExport(self, key, value, export, variant, exceptions):
    if not (variant in self.exportsContent):
      self.exportsContent[variant] = {}
    if (key in self.exportsContent[variant]):
      return False
    self.exportsContent[variant][key] = [export, value, exceptions]
    return True
    
  def doImport(self, label, variant):
    if not (variant in self.importsContent):
      self.importsContent[variant] = []
    if (label in self.importsContent[variant]):
      return False
    self.importsContent[variant].append(label)
    return True
    
  def getExports(self, variant, need):
    if not (variant in self.exportsContent):
      self.exportsContent[variant] = {}
    exportsContent = self.filterExports(self.exportsContent[variant], need)
    return exportsContent
    
  def getPath(self, owner, variant, purpose):
    if (purpose == None):
      return adjust(os.path.join(wd(), owner.getContext().root.directory.getContent(), owner.directory.getContent(), self.label.getContent()))
    if (variant == None):
      return adjust(os.path.join(wd(), owner.getContext().root.directory.getContent(), owner.directory.getContent(), purpose, "targets", self.label.getContent()))
    return adjust(os.path.join(wd(), owner.getContext().root.directory.getContent(), owner.directory.getContent(), purpose, "targets", self.label.getContent(), variant.lower()))
    
  def getLabel(self):
    return self.label.getContent()
    
  def getFiles(self, owner, pattern = None):
    result = []
    path = self.getPath(owner, None, None)
    for root, folders, files in os.walk(path):
      for name in files:
        if not (pattern == None):
          match = re.search(pattern, name)
          if (match == None):
            continue
          if not (match.group() == name):
            continue
        result.append(os.path.join(root, name).replace("\\", "/"))
    return result

  def getIncludes(self, owner):
    result = []
    path = self.getPath(owner, None, None)
    for root, folders, files in os.walk(path):
      result.append(root)
    return result
    
  def getLinkages(self, owner, variant):
    result = []
    path = self.getPath(owner, variant, "install")
    for root, folders, files in os.walk(path):
      result.append(root)
    return result
    
class TargetList(List):
  def __init__(self):
    super(TargetList, self).__init__()
    self.owner = None
    self.directory = None
    
  def build(self, owner, variant):
    self.owner = owner
    self.directory = self.owner.directory
    context = self.getContext()
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Target)):
        if ("BUILDSTER_BUILD" in context.data):
          if not (self.content[i].label == None):
            if not (self.content[i].label.getContent() == context.data["BUILDSTER_BUILD"]):
              if not (self.content[i].imports == None):
                if not (self.content[i].imports.doImport(self.content[i], variant)):
                  return False
              if not (self.content[i].exports == None):
                if not (self.content[i].exports.doExport(self.content[i], variant)):
                  return False
              continue
        if not (self.content[i].build(self, variant)):
          self.getContext().log(self.node, "Target build failure @ "+str(i)+"!")
          return False
    return True
    
  def distribute(self, owner, distribution, variant):
    self.owner = owner
    self.directory = self.owner.directory
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Target)):
        if not (self.content[i].distribute(self, distribution, variant)):
          self.getContext().log(self.node, "Target distribution failure @ "+str(i)+"!")
          return False
    return True
        
  def addTarget(self, target):
    if not (isinstance(target, Target)):
      return False
    return super(TargetList, self).add(target)
    
  def getExports(self, imports, variant, need):
    if (need == None):
      return self.owner.getExports(imports, variant, [self])
    if (len(need) == 0):
      return self.owner.getExports(imports, variant, [self])
    exports = self.owner.getExports(imports, variant, need+[self])
    length = len(self.content)
    if not (variant in imports):
      return exports
    for i in range(length):
      if (isinstance(self.content[i], Target)):
        label = self.content[i].getLabel()
        if (label in imports[variant]):
          if not (self.content[i] in need):
            exports.append([label, self.content[i].getExports(variant, need[0])])
    return exports
    
  def getTargets(self):
    return self
    
  def getDependencies(self):
    if (self.owner == None):
      return None
    return self.owner.getDependencies()
    
  def getContext(self):
    if (self.owner == None):
      return None
    return self.owner.getContext()
    
class ExecutableTarget(Target):
  def __init__(self, label = None, definitions = None, links = None, imports = None):
    super(ExecutableTarget, self).__init__(label, definitions, links, imports)
    self.exportsContent = {}
    self.importsContent = {}
    
  def build(self, owner, variant):
    success = super(ExecutableTarget, self).build(owner, variant)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export, variant, exceptions):
    if not (variant in self.exportsContent):
      self.exportsContent[variant] = {}
    if (key in self.exportsContent[variant]):
      return False
    self.exportsContent[variant][key] = [export, value, exceptions]
    return True
    
  def doImport(self, label, variant):
    if not (variant in self.importsContent):
      self.importsContent[variant] = []
    if (label in self.importsContent[variant]):
      return False
    self.importsContent[variant].append(label)
    return True
    
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.definitions)+", "+self.toString(self.links)+", "+self.toString(self.imports)+", "+self.toString(self.arguments)+", "+self.toString(self.packages)+", "+self.toString(self.modules)+">"
    
class LibraryTarget(Target):
  def __init__(self, label = None, definitions = None, links = None, imports = None, exports = None):
    super(LibraryTarget, self).__init__(label, definitions, links, imports, exports)
    self.exportsContent = {}
    self.importsContent = {}
    
  def build(self, owner, variant):
    success = super(LibraryTarget, self).build(owner, variant)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export, variant, exceptions):
    if not (variant in self.exportsContent):
      self.exportsContent[variant] = {}
    if (key in self.exportsContent[variant]):
      return False
    self.exportsContent[variant][key] = [export, value, exceptions]
    return True
    
  def doImport(self, label, variant):
    if not (variant in self.importsContent):
      self.importsContent[variant] = []
    if (label in self.importsContent[variant]):
      return False
    self.importsContent[variant].append(label)
    return True
    
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.definitions)+", "+self.toString(self.links)+", "+self.toString(self.imports)+", "+self.toString(self.exports)+", "+self.toString(self.arguments)+", "+self.toString(self.packages)+", "+self.toString(self.modules)+">"
    
class Project(Element):
  def __init__(self, dependencies = None, targets = None, directory = None, cmake_modules = None, context = None):
    super(Project, self).__init__()
    self.pre = None
    self.post = None
    self.dependencies = None
    self.targets = None
    self.directory = None
    self.cmake_modules = None
    self.context = None
    self.owner = None
    if (type(dependencies) == DependencyList):
      self.dependencies = dependencies
    if (type(targets) == TargetList):
      self.targets = targets
    if (type(directory) == Path):
      self.directory = directory
    if (type(cmake_modules) == Path):
      self.cmake_modules = cmake_modules
    if (str(type(context)) == "Context"):
      self.context = context
      
  def buildPre(self, variant):
    path = None
    if not (self.directory == None):
      path = os.path.join(wd(), self.getContext().root.directory.getContent(), self.directory.getContent(), "build", "dependencies")
    if not (path == None):
      if not (os.path.exists(path)):
        if (contains(wd(), path)):
          os.makedirs(path)
    path = None
    if not (self.directory == None):
      path = os.path.join(wd(), self.getContext().root.directory.getContent(), self.directory.getContent(), "build", "targets")
    if not (path == None):
      if not (os.path.exists(path)):
        if (contains(wd(), path)):
          os.makedirs(path)
    path = None
    if not (self.directory == None):
      path = os.path.join(wd(), self.getContext().root.directory.getContent(), self.directory.getContent(), "install", "dependencies")
    if not (path == None):
      if not (os.path.exists(path)):
        if (contains(wd(), path)):
          os.makedirs(path)
    path = None
    if not (self.directory == None):
      path = os.path.join(wd(), self.getContext().root.directory.getContent(), self.directory.getContent(), "install", "targets")
    if not (path == None):
      if not (os.path.exists(path)):
        if (contains(wd(), path)):
          os.makedirs(path)
    if (self.pre == None):
      return True
    if not (self.pre.timing == None):
      if not (self.pre.timing.getContent() == "build"):
        return True
    if not (self.pre.build(self, os.path.join(wd(), self.getContext().root.directory.getContent(), self.directory.getContent(), os.path.basename(self.directory.getContent())), os.path.join(wd(), self.getContext().root.directory.getContent(), self.directory.getContent()), os.path.join(wd(), self.getContext().root.directory.getContent(), self.directory.getContent(), "install"), {}, variant)):
      return False
    return True
    
  def buildPost(self, variant):
    if (self.post == None):
      return True
    if not (self.post.timing == None):
      if not (self.post.timing.getContent() == "build"):
        return True
    if not (self.post.build(self, os.path.join(wd(), self.getContext().root.directory.getContent(), self.directory.getContent(), os.path.basename(self.directory.getContent())), os.path.join(wd(), self.getContext().root.directory.getContent(), self.directory.getContent()), os.path.join(wd(), self.getContext().root.directory.getContent(), self.directory.getContent(), "install"), {}, variant)):
      return False
    return True
      
  def build(self, owner, variant):
    self.owner = owner
    if not (self.dependencies == None):
      self.dependencies.owner = self
    if not (self.targets == None):
      self.targets.owner = self
    if not (self.buildPre(variant)):
      self.context.log(self.node, "Pre build step failure!")
      return False
    if not (self.dependencies == None):
      if not (self.dependencies.build(self, variant)):
        self.context.log(self.node, "Dependency list build failure!")
        return False
    if not (self.targets == None):
      if not (self.targets.build(self, variant)):
        self.context.log(self.node, "Target list build failure!")
        return False
    return True
    
  def distribute(self, owner, distribution, variant):
    self.owner = owner
    path = os.path.join(distribution, variant.lower()).replace("\\", "/")
    if (os.path.isdir(path)):
      shutil.rmtree(path)
    if (contains(wd(), path)):
      os.makedirs(path)
    if not (self.dependencies == None):
      if not (self.dependencies.distribute(self, distribution, variant)):
        self.context.log(self.node, "Dependency list distribution failure!")
        return False
    if not (self.targets == None):
      if not (self.targets.distribute(self, distribution, variant)):
        self.context.log(self.node, "Target list distribution failure!")
        return False
    for root, folders, files in os.walk(path):
      for name in files:
        target = os.path.join(root, name).replace("\\", "/")
        index = -1
        for i in range(len(name)):
          if (name[i:(i+1)] == "."):
            index = i
            break
        if (index < 0):
          continue
        extension = name[index:]
        if (len(extension) < 2):
          continue
        extension = extension[1:].lower()
        if ((extension in self.context.sources) or (extension in self.context.headers) or (extension in self.context.scripts)):
          os.unlink(target)
    if not (platform.system() == "Windows"):
      for root, folders, files in os.walk(path):
        for name in files:
          target = os.path.join(root, name).replace("\\", "/")
          status = os.stat(target)
          os.chmod(target, status.st_mode|stat.S_IEXEC)
    if not (self.buildPost(variant)):
      self.context.log(self.node, "Post build step failure!")
      return False
    return True
    
  def getExports(self, imports, variant, need):
    exports = []
    if (need == None):
      return exports
    if (len(need) == 0):
      return exports
    if not (self.dependencies == None):
      if not (self.dependencies in need):
        exports = exports+self.dependencies.getExports(imports, variant, need)
    if not (self.targets == None):
      if not (self.targets in need):
        exports = exports+self.targets.getExports(imports, variant, need)
    return exports
    
  def getTargets(self):
    return self.targets
    
  def getDependencies(self):
    return self.dependencies
    
  def getContext(self):
    return self.context
    
  def getDistribution(self):
    return self.owner.context.root.getDisribution()
    
  def __str__(self):
    return "<"+self.toString(self.dependencies)+", "+self.toString(self.targets)+", "+self.toString(self.directory)+", "+self.toString(self.pre)+", "+self.toString(self.post)+">"

class Buildster(Element):
  def __init__(self, directory = None, distribution = None, cpp = None, context = None):
    super(Buildster, self).__init__()
    self.directory = None
    self.distribution = None
    self.cpp = String("14")
    self.context = None
    if (str(type(directory)) == "Path"):
      self.directory = directory
    if (str(type(distribution)) == "Path"):
      self.distribution = distribution
    if (str(type(cpp) == "String")):
      self.cpp = cpp
    if (str(type(context)) == "Context"):
      self.context = context
      
  def build(self, owner, variant):
    return True
    
  def getDisribution(self):
    return self.distribution
    
  def __str__(self):
    return "<"+self.toString(self.directory)+", "+self.toString(self.distribution)+">"

class Context(Element):
  def __init__(self, data, variant, debug = True):
    super(Context, self).__init__()
    

    self.variant = variant
    
    
    self.exclusions = []
    
    self.exclusions.append("o")
    self.exclusions.append("obj")
    self.exclusions.append("lo")
    self.exclusions.append("la")
    self.exclusions.append("d")
    self.exclusions.append("in")
    self.exclusions.append("ac")
    self.exclusions.append("cmake")
    self.exclusions.append("txt")
    self.exclusions.append("log")
    self.exclusions.append("bin")
    self.exclusions.append("make")
    self.exclusions.append("internal")

    self.extensions = []
    
    self.extensions.append("exe")
    
    self.headers = []
    
    self.headers.append("h")
    self.headers.append("hh")
    self.headers.append("hpp")
    self.headers.append("hxx")
    self.headers.append("h++")
    self.headers.append("i")
    self.headers.append("ii")
    self.headers.append("ipp")
    self.headers.append("ixx")
    self.headers.append("i++")
    self.headers.append("inl")
    self.headers.append("inc")
    self.headers.append("t")
    self.headers.append("tt")
    self.headers.append("tpp")
    self.headers.append("txx")
    self.headers.append("t++")
    self.headers.append("tpl")
    
    self.sources = []
    
    self.sources.append("c")
    self.sources.append("cc")
    self.sources.append("cpp")
    self.sources.append("cxx")
    self.sources.append("c++")
    self.sources.append("cs")
    self.sources.append("m")
    self.sources.append("objc")
    self.sources.append("swift")
    
    self.scripts = []
    
    self.scripts.append("java")
    self.scripts.append("py")
    self.scripts.append("rb")
    self.scripts.append("sh")
    self.scripts.append("bat")
    
    self.libraries = []
    
    self.libraries.append("dll")
    self.libraries.append("a")
    self.libraries.append("lib")
    self.libraries.append("dylib")
    self.libraries.append("so")
    self.libraries.append("jar")
    
    self.extensions = self.headers+self.sources+self.scripts+self.libraries+self.extensions
    
    self.substitutes = []
    
    self.substitutes.append("distribution")
    self.substitutes.append("origin")
    self.substitutes.append("install")
    self.substitutes.append("python")
    self.substitutes.append("home")
    self.substitutes.append("execute")
    self.substitutes.append("encode")
    self.substitutes.append("decode")
    self.substitutes.append("escape")
    self.substitutes.append("unescape")
    self.substitutes.append("lower")
    self.substitutes.append("upper")
    self.substitutes.append("exists")
    
    self.conditionals = []
    
    self.conditionals.append("if")
    self.conditionals.append("if_check")
    self.conditionals.append("if_exists")
    self.conditionals.append("switch")
    self.conditionals.append("else")
    self.conditionals.append("case")
    self.conditionals.append("default")
    
    self.nonconditionals = []
    
    self.nonconditionals.append("log")
    self.nonconditionals.append("read")
    self.nonconditionals.append("json")
    self.nonconditionals.append("data")
    self.nonconditionals.append("case")
    self.nonconditionals.append("default")
    self.nonconditionals.append("search")
    self.nonconditionals.append("set")
    for substitute in self.substitutes:
      if not (substitute in self.nonconditionals):
        self.nonconditionals.append(substitute)
    
    self.processes = []
    
    self.processes.append("message")
    self.processes.append("quit")
    
    self.any = "any"
    
    
    nodeTags = []
    
    nodeTags.append("case")
    nodeTags.append("default")
    nodeTags.append("else")
    nodeTags.append("data")
    nodeTags.append("buildster")
    nodeTags.append("project")
    nodeTags.append("dependencies")
    nodeTags.append("dependency")
    nodeTags.append("local")
    nodeTags.append("remote")
    nodeTags.append("path")
    nodeTags.append("subpath")
    nodeTags.append("git_repo")
    nodeTags.append("wget")
    nodeTags.append("url")
    nodeTags.append("branch")
    nodeTags.append("credentials")
    nodeTags.append("username")
    nodeTags.append("password")
    nodeTags.append("targets")
    nodeTags.append("target")
    nodeTags.append("executable")
    nodeTags.append("library")
    nodeTags.append("label")
    nodeTags.append("definitions")
    nodeTags.append("definition")
    nodeTags.append("key")
    nodeTags.append("value")
    nodeTags.append("links")
    nodeTags.append("link")
    nodeTags.append("build")
    nodeTags.append("arguments")
    nodeTags.append("argument")
    nodeTags.append("cmake")
    nodeTags.append("generator")
    nodeTags.append("source")
    nodeTags.append("exports")
    nodeTags.append("export")
    nodeTags.append("imports")
    nodeTags.append("import")
    nodeTags.append("install")
    nodeTags.append("origin")
    nodeTags.append("distribution")
    nodeTags.append("root")
    nodeTags.append("work")
    nodeTags.append("shells")
    nodeTags.append("shell")
    nodeTags.append("commands")
    nodeTags.append("command")
    nodeTags.append("write")
    nodeTags.append("extract")
    nodeTags.append("copy")
    nodeTags.append("rename")
    nodeTags.append("delete")
    nodeTags.append("from")
    nodeTags.append("to")
    nodeTags.append("destination")
    nodeTags.append("content")
    nodeTags.append("search")
    nodeTags.append("term")
    nodeTags.append("set")
    nodeTags.append("pre")
    nodeTags.append("post")
    nodeTags.append("variables")
    nodeTags.append("variable")
    nodeTags.append("packages")
    nodeTags.append("package")
    nodeTags.append("modules")
    nodeTags.append("module")
    nodeTags.append("hints")
    nodeTags.append("hint")
    nodeTags.append("python")
    nodeTags.append("home")
    nodeTags.append("execute")
    nodeTags.append("encode")
    nodeTags.append("decode")
    nodeTags.append("escape")
    nodeTags.append("unescape")
    nodeTags.append("lower")
    nodeTags.append("upper")
    for conditional in self.conditionals:
      if not (conditional in nodeTags):
        nodeTags.append(conditional)
    for nonconditional in self.nonconditionals:
      if not (nonconditional in nodeTags):
        nodeTags.append(nonconditional)
    for process in self.processes:
      if not (process in nodeTags):
        nodeTags.append(process)
    
    nodeParents = {}
    nodeAttributes = {}
    
    for i in range(len(nodeTags)):
      tag = nodeTags[i]
      parents = []
      attributes = []
      if not (tag == "buildster"):
        for conditional in self.conditionals:
          parents.append(conditional)
        for process in self.processes:
          parents.append(process)
      nodeParents[tag] = parents
      nodeAttributes[tag] = attributes
    
    nodeParents["lower"].append(self.any)
    nodeParents["upper"].append(self.any)
    nodeParents["python"].append(self.any)
    nodeParents["home"].append(self.any)
    nodeParents["execute"].append(self.any)
    nodeParents["encode"].append(self.any)
    nodeParents["decode"].append(self.any)
    nodeParents["escape"].append(self.any)
    nodeParents["unescape"].append(self.any)
    nodeParents["set"].append(self.any)
    nodeParents["search"].append(self.any)
    nodeParents["distribution"].append(self.any)
    nodeParents["origin"].append(self.any)
    nodeParents["install"].append(self.any)
    nodeParents["message"].append(self.any)
    nodeParents["quit"].append(self.any)
    nodeParents["data"].append(self.any)
    nodeParents["json"].append(self.any)
    nodeParents["read"].append(self.any)
    nodeParents["log"].append(self.any)
    nodeParents["if"].append(self.any)
    nodeParents["if_check"].append(self.any)
    nodeParents["if_exists"].append(self.any)
    nodeParents["switch"].append(self.any)
    nodeParents["case"].append("switch")
    nodeParents["else"].append("if")
    nodeParents["else"].append("if_check")
    nodeParents["else"].append("if_exists")
    #nodeParents["buildster"].append("")
    nodeParents["project"].append("buildster")
    nodeParents["dependencies"].append("project")
    nodeParents["dependency"].append("dependencies")
    nodeParents["remote"].append("dependency")
    nodeParents["local"].append("dependency")
    nodeParents["subpath"].append("dependency")
    nodeParents["subpath"].append("target")
    nodeParents["path"].append("local")
    nodeParents["git_repo"].append("remote")
    nodeParents["wget"].append("remote")
    nodeParents["url"].append("remote")
    nodeParents["branch"].append("git_repo")
    nodeParents["credentials"].append("git_repo")
    nodeParents["username"].append("credentials")
    nodeParents["password"].append("credentials")
    nodeParents["targets"].append("project")
    nodeParents["target"].append("targets")
    nodeParents["label"].append("dependency")
    nodeParents["label"].append("target")
    nodeParents["label"].append("package")
    nodeParents["label"].append("module")
    nodeParents["definitions"].append("target")
    nodeParents["definition"].append("definitions")
    nodeParents["key"].append("variable")
    nodeParents["value"].append("variable")
    nodeParents["key"].append("definition")
    nodeParents["value"].append("definition")
    nodeParents["key"].append("export")
    nodeParents["value"].append("export")
    nodeParents["key"].append("set")
    nodeParents["value"].append("set")
    nodeParents["links"].append("target")
    nodeParents["link"].append("links")
    nodeParents["build"].append("pre")
    nodeParents["build"].append("post")
    nodeParents["build"].append("dependency")
    nodeParents["arguments"].append("build")
    nodeParents["arguments"].append("target")
    nodeParents["argument"].append("arguments")
    nodeParents["cmake"].append("build")
    nodeParents["generator"].append("cmake")
    nodeParents["generator"].append("target")
    nodeParents["source"].append("cmake")
    nodeParents["exports"].append("module")
    nodeParents["exports"].append("package")
    nodeParents["exports"].append("dependency")
    nodeParents["exports"].append("target")
    nodeParents["export"].append("exports")
    nodeParents["imports"].append("dependency")
    nodeParents["imports"].append("target")
    nodeParents["import"].append("imports")
    nodeParents["root"].append("search")
    nodeParents["term"].append("search")
    nodeParents["work"].append("shell")
    nodeParents["shells"].append("pre")
    nodeParents["shells"].append("post")
    nodeParents["shells"].append("build")
    nodeParents["shell"].append("shells")
    nodeParents["commands"].append("shell")
    nodeParents["command"].append("commands")
    nodeParents["extract"].append("command")
    nodeParents["copy"].append("command")
    nodeParents["delete"].append("command")
    nodeParents["write"].append("command")
    nodeParents["rename"].append("copy")
    nodeParents["from"].append("copy")
    nodeParents["to"].append("copy")
    nodeParents["destination"].append("write")
    nodeParents["content"].append("write")
    nodeParents["pre"].append("project")
    nodeParents["post"].append("project")
    nodeParents["pre"].append("build")
    nodeParents["post"].append("build")
    nodeParents["pre"].append("target")
    nodeParents["post"].append("target")
    nodeParents["variables"].append("package")
    nodeParents["variable"].append("variables")
    nodeParents["packages"].append("target")
    nodeParents["package"].append("packages")
    nodeParents["modules"].append("target")
    nodeParents["module"].append("modules")
    nodeParents["hints"].append("package")
    nodeParents["hint"].append("hints")
    
    nodeAttributes["json"].append(["key", False])
    nodeAttributes["data"].append(["id", False])
    nodeAttributes["if"].append(["id", False])
    nodeAttributes["if_check"].append(["id", False])
    nodeAttributes["if_check"].append(["check", False])
    nodeAttributes["switch"].append(["id", False])
    nodeAttributes["case"].append(["check", False])
    nodeAttributes["buildster"].append(["directory", False])
    nodeAttributes["buildster"].append(["distribution", False])
    nodeAttributes["project"].append(["directory", False])
    nodeAttributes["project"].append(["cmake_modules", True])
    nodeAttributes["export"].append(["except", True])
    nodeAttributes["export"].append(["type", False])
    nodeAttributes["target"].append(["type", False])
    nodeAttributes["target"].append(["linkage", True])
    nodeAttributes["pre"].append(["timing", True])
    nodeAttributes["post"].append(["timing", True])
    nodeAttributes["search"].append(["type", False])
    nodeAttributes["generator"].append(["architecture", True])
    
    
    self.nodeTags = nodeTags
    self.nodeParents = {}
    self.nodeAttributes = {}
    
    for i in range(len(nodeTags)):
      tag = nodeTags[i]
      if (tag in nodeParents):
        if not (len(nodeParents[tag]) == 0):
          self.nodeParents[tag] = nodeParents[tag]
      if (tag in nodeAttributes):
        if not (len(nodeAttributes[tag]) == 0):
          self.nodeAttributes[tag] = nodeAttributes[tag]
    
    
    self.data = data
    self.debug = debug
    self.tier = 0
    self.root = None
    self.project = None
    self.error = None
    self.work = None
    self.context = self
    self.nodes = {}
    self.logs = []
    self.records = []
    self.projects = []
    self.labels = []
    self.environment = os.environ.copy()
    
    if not ("BUILDSTER_WD" in self.data):
      self.data["BUILDSTER_WD"] = wd()
    if not ("BUILDSTER_OS" in self.data):
      self.data["BUILDSTER_OS"] = platform.system()
      if (("msys" in self.data["BUILDSTER_OS"].lower()) or ("cygwin" in self.data["BUILDSTER_OS"].lower())):
        self.data["BUILDSTER_OS"] = "Windows"
    if not ("BUILDSTER_VARIANT" in self.data):
      self.data["BUILDSTER_VARIANT"] = self.variant
    
  def build(self, owner, variant):
    self.tier = None
    self.log(self.node, "CONTEXT_BUILD_BEGIN\n")
    self.data["BUILDSTER_VARIANT"] = variant
    for i in range(len(self.projects)):
      if (self.projects[i] == None):
        continue
      self.project = self.projects[i]
      if not (self.projects[i].build(self, variant)):
        self.tier = None
        self.log(self.node, "CONTEXT_BUILD_END\n")
        return False
      self.project = None
    self.tier = None
    self.log(self.node, "CONTEXT_BUILD_END\n")
    return True
    
  def distribute(self, owner, distribution, variant):
    self.tier = None
    self.log(self.node, "CONTEXT_DISTRIBUTE_BEGIN\n")
    for i in range(len(self.projects)):
      if (self.projects[i] == None):
        continue
      self.project = self.projects[i]
      if not (self.projects[i].distribute(self, os.path.join(wd(), self.root.directory.getContent(), distribution).replace("\\", "/"), variant)):
        self.tier = None
        self.log(self.node, "CONTEXT_DISTRIBUTE_END\n")
        return False
      self.project = None
    self.tier = None
    self.log(self.node, "CONTEXT_DISTRIBUTE_END\n")
    return True
    
  def check(self, node, parent, parents = None):
    tag = node.tag
    if (tag == "label"):
      if (parent == None):
        return True
    if not (parents == None):
      parents = copy.deepcopy(parents)
      for i in range(len(parents)):
        if (parents[i] == None):
          continue
        parents[i] = parents[i].tag
    if not (tag in self.nodeTags):
      self.record(node, "Node Tag Error @ (\""+str(tag)+"\" | \""+str(parents)+"\")...")
      return False
    if (parent == None):
      if (tag in self.nodeParents):
        self.record(node, "Node Parent Error 1 @ (\""+str(tag)+"\" | \""+str(parents)+"\")...")
        return False
    else:
      if not (tag in self.nodeParents):
        self.record(node, "Node Parent Error 2 @ (\""+str(tag)+"\" | \""+str(parents)+"\")...")
        return False
      if not (self.any in self.nodeParents[tag]):
        if not (parent.tag in self.nodeParents[tag]):
          self.record(node, "Node Parent Error 3 (\""+str(parent.tag)+"\" | \""+str(self.nodeParents[tag])+"\") @ (\""+str(tag)+"\" | \""+str(parents)+"\")...")
          return False
    if (tag in self.nodeAttributes):
      attributes = self.nodeAttributes[tag]
      for attribute in attributes:
        optional = attribute[1]
        attribute = attribute[0]
        if not (attribute in node.attrib):
          if not (optional):
            self.record(node, "Node Attribute Error @ (\""+str(tag)+"\" | \""+str(parents)+"\")...")
            return False
    return True
    
  def optional(self, node, attribute):
    tag = node.tag
    if (tag in self.nodeAttributes):
      attributes = self.nodeAttributes[tag]
      for i in range(len(attributes)):
        optional = attributes[i][1]
        if ((optional) and (attribute == attributes[i][0])):
          return True
    return False
    
  def exclude(self, leaf):
    for exclusion in self.exclusions:
      if (leaf.endswith("."+exclusion)):
        return True
    return False
  
  def find(self, id):
    if not (id in self.data):
      return False
    return True
  
  def get(self, id):
    if not (id in self.data):
      return ""
    return self.data[id]
    
  def log(self, node, message):
    tag = ""
    if not (node == None):
      tag = "\\"+node.tag+"/|"
    now = datetime.now()
    if not (self.debug):
      return
    self.logs.append(tag+now.strftime("%d-%m-%Y@%H:%M:%S")+"\n")
    print(self.logs[len(self.logs)-1])
    if (self.tier == None):
      self.logs.append("\""+str(message.strip())+"\"\n")
      print(self.logs[len(self.logs)-1])
      return
    self.logs.append(("  "*self.tier)+str(self.tier)+": \""+str(message.strip())+"\"")
    print(self.logs[len(self.logs)-1])
  
  def record(self, node, message):
    record = []
    record.append(self.tier)
    record.append(message)
    record.append(node)
    record.append(traceback.format_list(traceback.extract_stack()))
    self.records.append(record)
    
  def report(self):
    self.tier = None
    self.log(None, "CONTEXT_REPORT_BEGIN\n")
    length = len(self.records)
    for i in range(length):
      record = self.records[i]
      stack = record[3]
      self.tier = record[0]
      self.log(record[2], record[1])
      """
      if (self.debug):
        for j in range(len(stack)):
          frame = stack[j]
          self.log(record[2], frame)
      """
    self.tier = None
    self.log(None, "CONTEXT_REPORT_END\n")
    
  def getContext(self):
    return self
    
  def getLogs(self):
    logs = ""
    length = len(self.logs)
    for i in range(length):
      log = self.logs[i]
      logs += log
    return logs

def handle(context, node, tier, parents):
  parent = parents[len(parents)-1]
  quit = False
  result = True
  tag = node.tag.lower()
  output = []
  elements = {}
  element = None
  null = [True, "", {}]
  context.tier = tier
  context.log(node, tag)
  #context.log(node, "NODE_BEGIN\n")
  if (context.check(node, parent, parents)):
    element = None
    if ((tag in context.conditionals) and (("id" in node.attrib) or (context.optional(node, "id")))):
      id = None
      if ("id" in node.attrib):
        id = node.attrib["id"]
      if (tag == "if"):
        if not (context.find(id)):
          context.log(node, id+" does not exist in data!")
          children = False
          for child in node:
            if (child.tag == "else"):
              children = True
              context.tier = tier
              call = handle(context, child, tier+1, parents+[node])
              if not (call[0]):
                result = False
                break
              if (child.tag in context.conditionals):
                output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
              elif (child.tag in context.nonconditionals):
                output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
              for key in call[2]:
                value = call[2][key]
                if not (value == None):
                  for i in range(len(value)):
                    if not (value[i] == None):
                      if (child.tag in context.conditionals):
                        if not (key in elements):
                          elements[key] = []
                        elements[key].append(value[i])
                      else:
                        if not (child.tag in elements):
                          elements[child.tag] = []
                        elements[child.tag].append(value[i])
              break
          if not (children):
            return null
          return [result, output, elements]
      elif (tag == "if_check"):
        check = node.attrib["check"]
        if not (ensure(context.get(id)).strip() == check):
          context.log(node, id+" does not match \""+check+"\" check!")
          children = False
          for child in node:
            if (child.tag == "else"):
              children = True
              context.tier = tier
              call = handle(context, child, tier+1, parents+[node])
              if not (call[0]):
                result = False
                break
              if (child.tag in context.conditionals):
                output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
              elif (child.tag in context.nonconditionals):
                output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
              for key in call[2]:
                value = call[2][key]
                if not (value == None):
                  for i in range(len(value)):
                    if not (value[i] == None):
                      if (child.tag in context.conditionals):
                        if not (key in elements):
                          elements[key] = []
                        elements[key].append(value[i])
                      else:
                        if not (child.tag in elements):
                          elements[child.tag] = []
                        elements[child.tag].append(value[i])
              break
          if not (children):
            return null
          return [result, output, elements]
      elif (tag == "if_exists"):
          exists = None
          for child in parent:
            if (child.tag == "exists"):
              exists = child
              break
          if not (exists == None):
            call = handle(context, exists, tier, parents)
            if not (call[0]):
              context.log(node, "A \"if_exists\" node was blocked by a descendant \"exists\"!\n")
              return null
            else:
              exists = ensure(exists.text).strip()+ensure(call[1]).strip()
              exists = exists.strip()
              if not (os.path.exists(exists)):
                context.log(node, id+" does not match \""+exists+"\" check!")
                children = False
                for child in node:
                  if (child.tag == "else"):
                    children = True
                    context.tier = tier
                    call = handle(context, child, tier+1, parents+[node])
                    if not (call[0]):
                      result = False
                      break
                    if (child.tag in context.conditionals):
                      output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
                    elif (child.tag in context.nonconditionals):
                      output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
                    for key in call[2]:
                      value = call[2][key]
                      if not (value == None):
                        for i in range(len(value)):
                          if not (value[i] == None):
                            if (child.tag in context.conditionals):
                              if not (key in elements):
                                elements[key] = []
                              elements[key].append(value[i])
                            else:
                              if not (child.tag in elements):
                                elements[child.tag] = []
                              elements[child.tag].append(value[i])
                    break
                if not (children):
                  return null
                return [result, output, elements]
          else:
            context.report(node, "No \"exists\" descendant for \"if_exists\" node!\n")
            return null
      elif (tag == "switch"):
        id = node.attrib["id"]
        children = False
        default = None
        for child in node:
          if (child.tag == "case"):
            check = child.attrib["check"]
            if (ensure(context.get(id)).strip() == check):
              children = True
              context.tier = tier
              call = handle(context, child, tier+1, parents+[node])
              if not (call[0]):
                result = False
                break
              if (child.tag in context.conditionals):
                output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
              elif (child.tag in context.nonconditionals):
                output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
              for key in call[2]:
                value = call[2][key]
                if not (value == None):
                  for i in range(len(value)):
                    if not (value[i] == None):
                      if (child.tag in context.conditionals):
                        if not (key in elements):
                          elements[key] = []
                        elements[key].append(value[i])
                      else:
                        if not (child.tag in elements):
                          elements[child.tag] = []
                        elements[child.tag].append(value[i])
              break
          elif (child.tag == "default"):
            default = child
        if not (children):
          if not (default == None):
            context.tier = tier
            call = handle(context, default, tier+1, parents+[node])
            if not (call[0]):
              result = False
            else:
              if (default.tag in context.conditionals):
                output.append([ensure(call[1]).strip(), ensure(default.tail).strip()])
              elif (default.tag in context.nonconditionals):
                output.append([ensure(call[1]).strip(), ensure(default.tail).strip()])
              for key in call[2]:
                value = call[2][key]
                if not (value == None):
                  for i in range(len(value)):
                    if not (value[i] == None):
                      if (default.tag in context.conditionals):
                        if not (key in elements):
                          elements[key] = []
                        elements[key].append(value[i])
                      else:
                        if not (default.tag in elements):
                          elements[default.tag] = []
                        elements[default.tag].append(value[i])
        output = ensure(node.text)+flatten(output).strip()
        return [result, output.strip(), elements]
      else:
        return null
    elif (tag == "else"):
      if (parent.tag in context.conditionals):
        id = None
        if ("id" in parent.attrib):
          id = parent.attrib["id"]
        if (parent.tag == "if"):
          if (context.find(id)):
            context.log(node, str(id)+" does exist in data for else case!")
            return null
        elif (parent.tag == "if_check"):
          check = parent.attrib["check"]
          if (ensure(context.get(id)).strip() == check):
            context.log(node, str(id)+" does match \""+check+"\" check for else case!")
            return null
        elif (parent.tag == "if_exists"):
          exists = None
          for child in parent:
            if (child.tag == "exists"):
              exists = child
              break
          if not (exists == None):
            call = handle(context, exists, tier, parents)
            if not (call[0]):
              context.log(node, "A \"if_exists\" node was blocked by a descendant \"exists\"!\n")
              return null
            else:
              exists = ensure(exists.text).strip()+ensure(call[1]).strip()
              exists = exists.strip()
              if (os.path.exists(exists)):
                context.log(node, str(id)+" does match \""+exists+"\" check for else case!")
                return null
          else:
            context.report(node, "No \"exists\" descendant for \"if_exists\" node!\n")
            return null
        else:
          return null
    elif (tag == "quit"):
      quit = True
      result = False
    elif (tag == "buildster"):
      element = Buildster()
      element.context = context
      if ("directory" in node.attrib):
        element.directory = Path(String(node.attrib["directory"].strip()))
      if ("distribution" in node.attrib):
        element.distribution = Path(String(node.attrib["distribution"].strip()))
      if ("cpp" in node.attrib):
        element.cpp = String(node.attrib["cpp"].strip())
      else:
        element.cpp = String("14")
      context.root = element
    elif (tag == "project"):
      element = Project()
      element.context = context
      if ("directory" in node.attrib):
        element.directory = Path(String(node.attrib["directory"].strip()))
      if ("cmake_modules" in node.attrib):
        element.cmake_modules = Path(String(node.attrib["cmake_modules"].strip()))
      if not (element in context.projects):
        context.projects.append(element)
      context.project = element
    elif (tag == "dependencies"):
      element = DependencyList()
    elif (tag == "targets"):
      element = TargetList()
    elif (tag == "local"):
      element = LocalDependency()
    elif (tag == "remote"):
      element = RemoteDependency()
    elif (tag == "git_repo"):
      element = GitRepoDependency()
    elif (tag == "wget"):
      element = WGetDependency()
    elif (tag == "target"):
      target = node.attrib["type"]
      if (target == "executable"):
        element = ExecutableTarget()
      elif (target == "library"):
        element = LibraryTarget()
      else:
        pass
      if ("linkage" in node.attrib):
        element.linkage = String(node.attrib["linkage"].strip())
    elif (tag == "pre"):
      element = PreBuildInstruction()
      if ("timing" in node.attrib):
        element.timing = String(node.attrib["timing"].strip())
    elif (tag == "post"):
      element = PostBuildInstruction()
      if ("timing" in node.attrib):
        element.timing = String(node.attrib["timing"].strip())
    elif (tag == "build"):
      element = BuildInstruction()
    elif (tag == "arguments"):
      element = ArgumentList()
    elif (tag == "variables"):
      element = VariableList()
    elif (tag == "variable"):
      element = Variable()
    elif (tag == "packages"):
      element = PackageList()
    elif (tag == "package"):
      element = Package()
    elif (tag == "modules"):
      element = ModuleList()
    elif (tag == "module"):
      element = Module()
    elif (tag == "hints"):
      element = HintList()
    elif (tag == "hint"):
      element = Hint()
    elif (tag == "cmake"):
      element = CmakeBuildInstruction()
    elif (tag == "shells"):
      element = ShellsBuildInstruction()
    elif (tag == "shell"):
      element = ShellBuildInstruction()
    elif (tag == "commands"):
      element = CommandsBuildInstruction()
    elif (tag == "command"):
      element = CommandBuildInstruction()
    elif (tag == "destination"):
      element = Destination()
    elif (tag == "content"):
      element = Content()
    elif (tag == "write"):
      element = Writer()
    elif (tag == "delete"):
      element = Deleter()
    elif (tag == "extract"):
      element = Extractor()
    elif (tag == "copy"):
      element = Copier()
    elif (tag == "from"):
      element = CopierSource()
    elif (tag == "to"):
      element = CopierDestination()
    elif (tag == "rename"):
      element = CopierRename()
    elif (tag == "definition"):
      element = Definition()
    elif (tag == "definitions"):
      element = DefinitionList()
    elif (tag == "links"):
      element = LinkList()
    elif (tag == "export"):
      element = Export()
    elif (tag == "exports"):
      element = ExportList()
    elif (tag == "imports"):
      element = ImportList()
    elif (tag == "root"):
      element = Root()
    elif (tag == "term"):
      element = Term()
    children = False
    for child in node:
      if (child.tag == "exists"):
        call = ["", ensure(child.tail).strip()]
        context.log(node, "A \""+str(tag)+"\" had a \"exists\" child that was replaced with \""+str(call)+"\"")
        output.append(call)
        continue
      children = True
      context.tier = tier
      call = handle(context, child, tier+1, parents+[node])
      if not (call[0]):
        result = False
        break
      if (child.tag.lower() in context.conditionals):
        output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
      elif ((child.tag.lower() in context.nonconditionals) or (child.tag.lower() in context.substitutes)):
        if (child.tag.lower() in context.substitutes):
          output.append([ensure(call[1]), ensure(child.tail)])
        else:
          output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
      for key in call[2]:
        value = call[2][key]
        if not (value == None):
          for i in range(len(value)):
            if not (value[i] == None):
              if (child.tag in context.conditionals):
                if not (key in elements):
                  elements[key] = []
                elements[key].append(value[i])
              else:
                if not (child.tag in elements):
                  elements[child.tag] = []
                elements[child.tag].append(value[i])
    context.tier = tier
    context.log(node, tag)
    success = True
    if not (tag in context.nodeAttributes):
      if (tag == "key"):
        output = ensure(node.text)+flatten(output).strip()
        element = Key()
        element.string = String(output.strip())
      elif (tag == "value"):
        output = ensure(node.text)+flatten(output).strip()
        element = Value()
        element.string = String(output.strip())
      elif (tag == "definition"):
        if ("key" in elements):
          for key in elements["key"]:
            element.key = key
            break
          elements["key"] = None
        if ("value" in elements):
          for value in elements["value"]:
            element.value = value
            break
          elements["value"] = None
      elif (tag == "definitions"):
        if ("definition" in elements):
          for definition in elements["definition"]:
            element.addDefinition(definition)
          elements["definition"] = None
      elif (tag == "exports"):
        if ("export" in elements):
          for e in elements["export"]:
            element.addExport(e)
          elements["export"] = None
      elif (tag == "imports"):
        if ("import" in elements):
          for i in elements["import"]:
            element.addImport(i)
          elements["import"] = None
      elif (tag == "links"):
        if ("link" in elements):
          for link in elements["link"]:
            element.addLink(link)
          elements["link"] = None
      elif (tag == "dependencies"):
        if ("dependency" in elements):
          for dependency in elements["dependency"]:
            element.addDependency(dependency)
          elements["dependency"] = None
      elif (tag == "dependency"):
        if ("local" in elements):
          for local in elements["local"]:
            element = local
            break
          elements["local"] = None
        if ("remote" in elements):
          for remote in elements["remote"]:
            element = remote
            break
          elements["remote"] = None
        if ("subpath" in elements):
          for subpath in elements["subpath"]:
            element.subpath = subpath
            break
          elements["subpath"] = None
        if ("label" in elements):
          for label in elements["label"]:
            element.label = label
            break
          elements["label"] = None
        if ("build" in elements):
          for instruction in elements["build"]:
            element.instruction = instruction
            break
          elements["build"] = None
        if ("imports" in elements):
          for imports in elements["imports"]:
            element.imports = imports
            break
          elements["imports"] = None
        if ("exports" in elements):
          for exports in elements["exports"]:
            element.exports = exports
            break
          elements["exports"] = None
        context.log(node, element.toString()+"\n")
      elif (tag == "targets"):
        if ("target" in elements):
          for target in elements["target"]:
            element.addTarget(target)
          elements["target"] = None
        context.log(node, element.toString()+"\n")
      elif (tag == "local"):
        if ("path" in elements):
          for path in elements["path"]:
            element.path = path
            break
          elements["path"] = None
      elif (tag == "remote"):
        if ("git_repo" in elements):
          for git_repo in elements["git_repo"]:
            element = git_repo
            break
          elements["git_repo"] = None
        if ("wget" in elements):
          for w_get in elements["wget"]:
            element = w_get
            break
          elements["wget"] = None
        if ("url" in elements):
          for url in elements["url"]:
            element.url = url
            break
          elements["url"] = None
      elif (tag == "git_repo"):
        if ("branch" in elements):
          element.branch = elements["branch"][0]
          elements["branch"][0] = None
        if ("credentials" in elements):
          element.credentials = elements["credentials"][0]
          elements["credentials"][0] = None
        context.log(node, element.toString()+"\n")
      elif (tag == "wget"):
        output = ensure(node.text)+flatten(output).strip()
        element.string = String(output.strip())
      elif (tag == "branch"):
        output = ensure(node.text)+flatten(output).strip()
        element = Branch()
        element.string = String(output.strip())
      elif (tag == "subpath"):
        output = ensure(node.text)+flatten(output).strip()
        element = Path()
        element.string = String(output.strip())
      elif (tag == "path"):
        output = ensure(node.text)+flatten(output).strip()
        element = Path()
        element.string = String(output.strip())
      elif (tag == "url"):
        output = ensure(node.text)+flatten(output).strip()
        element = URL()
        element.string = String(output.strip())
      elif (tag == "credentials"):
        element = Credentials()
        if ("username" in elements):
          element.username = elements["username"][0]
          elements["username"][0] = None
        if ("password" in elements):
          element.password = elements["password"][0]
          elements["password"][0] = None
      elif (tag == "username"):
        output = ensure(node.text)+flatten(output).strip()
        element = Username()
        element.string = String(output.strip())
      elif (tag == "password"):
        output = ensure(node.text)+flatten(output).strip()
        element = Password()
        element.string = String(output.strip())
      elif (tag == "message"):
        output = ensure(node.text)+flatten(output).strip()
        context.record(node, output.strip()+"\n")
      elif (tag == "quit"):
        pass
      elif (tag == "import"):
        output = ensure(node.text)+flatten(output).strip()
        element = Import()
        element.label = Label(String(output.strip()))
      elif (tag == "link"):
        output = ensure(node.text)+flatten(output).strip()
        element = Link()
        element.string = String(output.strip())
      elif (tag == "label"):
        output = ensure(node.text)+flatten(output).strip()
        element = Label()
        element.string = String(output.strip())
        if not (parent == None):
          if not (element.getContent() in context.labels):
            context.labels.append(element.getContent())
          else:
            context.log(node, "Labels (\""+element.getContent()+"\") must be unique!\n")
            result = False
      elif (tag == "source"):
        output = ensure(node.text)+flatten(output).strip()
        element = Path()
        element.string = String(output.strip())
      elif (tag == "argument"):
        output = ensure(node.text)+flatten(output).strip()
        element = Argument()
        element.string = String(output.strip())
      elif (tag == "hint"):
        output = ensure(node.text)+flatten(output).strip()
        element = Hint()
        element.string = String(output.strip())
      elif (tag == "variable"):
        if ("key" in elements):
          for key in elements["key"]:
            element.key = key
            break
          elements["key"] = None
        if ("value" in elements):
          for value in elements["value"]:
            element.value = value
            break
          elements["value"] = None
      elif (tag == "module"):
        if ("label" in elements):
          for label in elements["label"]:
            element.label = label
            if (label.getContent() in context.labels):
              for i in range(len(context.labels)):
                if (context.labels[i] == label.getContent()):
                  if (i == 0):
                    if (len(context.labels) > 1):
                      context.labels = context.labels[1:]
                    else:
                      context.labels = []
                    break
                  if (i == len(context.labels)-1):
                    context.labels = context.labels[:(len(context.labels)-1)]
                    break
                  context.labels = context.labels[:i]+context.labels[(i+1):]
                  break
            break
          elements["label"] = None
        if ("exports" in elements):
          for exports in elements["exports"]:
            element.exports = exports
            break
          elements["exports"] = None
      elif (tag == "package"):
        if ("label" in elements):
          for label in elements["label"]:
            element.label = label
            if (label.getContent() in context.labels):
              for i in range(len(context.labels)):
                if (context.labels[i] == label.getContent()):
                  if (i == 0):
                    if (len(context.labels) > 1):
                      context.labels = context.labels[1:]
                    else:
                      context.labels = []
                    break
                  if (i == len(context.labels)-1):
                    context.labels = context.labels[:(len(context.labels)-1)]
                    break
                  context.labels = context.labels[:i]+context.labels[(i+1):]
                  break
            break
          elements["label"] = None
        if ("exports" in elements):
          for exports in elements["exports"]:
            element.exports = exports
            break
          elements["exports"] = None
        if ("hints" in elements):
          for hints in elements["hints"]:
            element.hints = hints
            break
          elements["hints"] = None
        if ("variables" in elements):
          for variables in elements["variables"]:
            element.variables = variables
            break
          elements["variables"] = None
      elif (tag == "work"):
        output = ensure(node.text)+flatten(output).strip()
        element = Work()
        element.string = String(output.strip())
      elif (tag == "hints"):
        if ("hint" in elements):
          for hint in elements["hint"]:
            element.addHint(hint)
          elements["hint"] = None
      elif (tag == "variables"):
        if ("variable" in elements):
          for variable in elements["variable"]:
            element.addVariable(variable)
          elements["variable"] = None
      elif (tag == "arguments"):
        if ("argument" in elements):
          for argument in elements["argument"]:
            element.addArgument(argument)
          elements["argument"] = None
      elif (tag == "modules"):
        if ("module" in elements):
          for module in elements["module"]:
            element.addModule(module)
          elements["module"] = None
      elif (tag == "packages"):
        if ("package" in elements):
          for package in elements["package"]:
            element.addPackage(package)
          elements["package"] = None
      elif (tag == "build"):
        if ("cmake" in elements):
          for cmake in elements["cmake"]:
            element = cmake
            break
          elements["cmake"] = None
        if ("shells" in elements):
          for shells in elements["shells"]:
            element = shells
            break
          elements["shells"] = None
        if ("arguments" in elements):
          for arguments in elements["arguments"]:
            element.arguments = arguments
            break
          elements["arguments"] = None
        if ("pre" in elements):
          for pre in elements["pre"]:
            element.pre = pre
            if not (pre.timing == None):
              if (pre.timing.getContent() == "parse"):
                if not (pre.build(context.project, os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), os.path.basename(context.project.directory.getContent())), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent()), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), "install"), {}, context.variant)):
                  context.error = "Parse time pre build stop failure!"
            break
          elements["pre"] = None
        if ("post" in elements):
          for post in elements["post"]:
            element.post = post
            if not (post.timing == None):
              if (post.timing.getContent() == "parse"):
                if not (post.build(context.project, os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), os.path.basename(context.project.directory.getContent())), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent()), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), "install"), {}, context.variant)):
                  context.error = "Parse time post build stop failure!"
            break
          elements["post"] = None
      elif (tag == "cmake"):
        if ("generator" in elements):
          for generator in elements["generator"]:
            element.generator = generator
            break
          elements["generator"] = None
        if ("source" in elements):
          for source in elements["source"]:
            element.source = source
            break
          elements["source"] = None
      elif (tag == "root"):
        output = ensure(node.text)+flatten(output).strip()
        element.string = String(output.strip())
      elif (tag == "term"):
        output = ensure(node.text)+flatten(output).strip()
        element.string = String(output.strip())
      elif (tag == "from"):
        output = ensure(node.text)+flatten(output).strip()
        element.path = Path(String(output.strip()))
      elif (tag == "to"):
        output = ensure(node.text)+flatten(output).strip()
        element.path = Path(String(output.strip()))
      elif (tag == "rename"):
        output = ensure(node.text)+flatten(output).strip()
        element.name = String(output.strip())
      elif (tag == "destination"):
        output = ensure(node.text)+flatten(output).strip()
        element.path = Path(String(output.strip()))
      elif (tag == "content"):
        output = ensure(node.text)+flatten(output).strip()
        element.string = String(output.strip())
      elif (tag == "shells"):
        if ("shell" in elements):
          for shell in elements["shell"]:
            element.shells.append(shell)
          elements["shell"] = None
      elif (tag == "shell"):
        if ("commands" in elements):
          for commands in elements["commands"]:
            element.commands = commands
            break
          elements["commands"] = None
        if ("work" in elements):
          for work in elements["work"]:
            element.work = work
            break
          elements["work"] = None
      elif (tag == "commands"):
        if ("command" in elements):
          for command in elements["command"]:
            element.commands.append(command)
          elements["command"] = None
      elif (tag == "command"):
        output = ensure(node.text)+flatten(output).strip()
        element.string = String(output.strip())
        if ("extract" in elements):
          for extract in elements["extract"]:
            element.extracts.append(extract)
          elements["extract"] = None
        if ("copy" in elements):
          for copy in elements["copy"]:
            element.copies.append(copy)
          elements["copy"] = None
        if ("delete" in elements):
          for delete in elements["delete"]:
            element.deletes.append(delete)
          elements["delete"] = None
        if ("write" in elements):
          for wrote in elements["write"]:
            element.writes.append(wrote)
          elements["write"] = None
        if ("set" in elements):
          for setter in elements["set"]:
            element.writes.append(setter)
          elements["set"] = None
      elif (tag == "write"):
        if ("destination" in elements):
          for destination in elements["destination"]:
            element.destination = destination
            break
          elements["destination"] = None
        if ("content" in elements):
          for content in elements["content"]:
            element.content = content
            break
          elements["content"] = None
      elif (tag == "copy"):
        if ("from" in elements):
          for source in elements["from"]:
            element.source = source
            break
          elements["from"] = None
        if ("to" in elements):
          for destination in elements["to"]:
            element.destination = destination
            break
          elements["to"] = None
        if ("rename" in elements):
          for rename in elements["rename"]:
            element.rename = rename
            break
          elements["rename"] = None
      elif (tag == "extract"):
        output = ensure(node.text)+flatten(output).strip()
        element.path = Path(String(output.strip()))
      elif (tag == "delete"):
        output = ensure(node.text)+flatten(output).strip()
        element.path = Path(String(output.strip()))
      elif (tag == "exists"):
        output = ensure(node.text)+flatten(output).strip()
        output = output.strip()
      elif (tag == "distribution"):
        output = adjust(os.path.join(wd(), context.root.directory.getContent(), context.root.distribution.getContent(), context.variant.lower())).replace("\\", "/")
      elif (tag == "python"):
        output = sys.executable.replace("\\", "/")
      elif (tag == "home"):
        output = str(pathlib.Path.home()).replace("\\", "/")
      elif (tag == "execute"):
        output = ensure(node.text)+flatten(output).strip()
        command = shlex.split(output.strip())
        output = execute_command(command, context.environment).strip()
        print(output)
        if (output == None):
          output = ""
      elif (tag == "escape"):
        output = ensure(node.text)+flatten(output).strip()
        output = repr(output.strip())[1:]
        output = output[:(len(output)-1)]
      elif (tag == "unescape"):
        output = ensure(node.text)+flatten(output).strip()
        output = ast.literal_eval(F'"""{output.strip()}"""')
      elif (tag == "lower"):
        output = ensure(node.text)+flatten(output).strip()
        output = output.strip().lower()
      elif (tag == "upper"):
        output = ensure(node.text)+flatten(output).strip()
        output = output.strip().upper()
      elif (tag == "encode"):
        output = ensure(node.text)+flatten(output).strip()
        output = base64.b64encode(output.strip().encode("ascii")).decode("ascii")
      elif (tag == "decode"):
        output = ensure(node.text)+flatten(output).strip()
        output = base64.b64decode(output.strip().encode("ascii")).decode("ascii")
      elif (tag == "install"):
        dependency = get_parent(parents, "dependency")
        if not (dependency == None):
          label = get_child(dependency, "label")
          if not (label == None):
            project = get_parent(parents, "project")
            if not (project == None):
              temp = handle(context, label, tier, [None])
              output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"], "install", "dependencies", temp[1], context.variant.lower())).replace("\\", "/")
            else:
              context.report(node, "No \"project\" ancestor for \"label\" node!\n")
              result = False
          else:
            context.report(node, "No \"label\" descendant for \"dependency\" node!\n")
            result = False
        else:
          target = get_parent(parents, "target")
          if not (target == None):
            label = get_child(target, "label")
            if not (label == None):
              project = get_parent(parents, "project")
              if not (project == None):
                temp = handle(context, label, tier, [None])
                output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"], "install", "targets", temp[1], context.variant.lower())).replace("\\", "/")
              else:
                context.report(node, "No \"project\" ancestor for \"label\" node!\n")
                result = False
            else:
              context.report(node, "No \"label\" descendant for \"target\" node!\n")
              result = False
          else:
            project = get_parent(parents, "project")
            if not (project == None):
              output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"])).replace("\\", "/")
            else:
              context.report(node, "No \"dependency\", \"target\", or \"project\" ancestor for \"install\" node!\n")
              result = False
      elif (tag == "origin"):
        dependency = get_parent(parents, "dependency")
        if not (dependency == None):
          label = get_child(dependency, "label")
          if not (label == None):
            project = get_parent(parents, "project")
            if not (project == None):
              temp = handle(context, label, tier, [None])
              output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"], "build", "dependencies", temp[1])).replace("\\", "/")
            else:
              context.report(node, "No \"project\" ancestor for \"label\" node!\n")
              result = False
          else:
            context.report(node, "No \"label\" descendant for \"dependency\" node!\n")
            result = False
        else:
          target = get_parent(parents, "target")
          if not (target == None):
            label = get_child(target, "label")
            if not (label == None):
              project = get_parent(parents, "project")
              if not (project == None):
                temp = handle(context, label, tier, [None])
                output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"], temp[1])).replace("\\", "/")
              else:
                context.report(node, "No \"project\" ancestor for \"label\" node!\n")
                result = False
            else:
              context.report(node, "No \"label\" descendant for \"target\" node!\n")
              result = False
          else:
            project = get_parent(parents, "project")
            if not (project == None):
              output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"])).replace("\\", "/")
            else:
              context.report(node, "No \"dependency\", \"target\", or \"project\" ancestor for \"origin\" node!\n")
              result = False
      elif (tag == "default"):
        output = ensure(node.text)+flatten(output).strip()
        output = output.strip()
        context.log(node, output+"\n")
      elif (tag == "log"):
        output = ensure(context.getLogs()).strip()
      elif (tag == "read"):
        output = ensure(node.text)+flatten(output).strip()
        output = output.strip()
        if (os.path.isfile(output)):
          lines = read(output)
          output = flatten(lines)
        else:
          output = ""
        context.log(node, output+"\n")
      elif (tag == "set"):
        element = Setter()
        if ("key" in elements):
          for key in elements["key"]:
            element.key = key
            break
          elements["key"] = None
        if ("value" in elements):
          for value in elements["value"]:
            element.value = value
            break
          elements["value"] = None
      else:
        success = False
    else:
      if (tag == "data"):
        output = ensure(context.get(node.attrib["id"])).strip()
        context.log(node, output+"\n")
      elif (tag == "pre"):
        for key in elements:
          for value in elements[key]:
            element.instructions.append(value)
        if (parent.tag == "project"):
          context.projects[len(context.projects)-1].pre = element
          if not (element.timing == None):
            if (element.timing.getContent() == "discover"):
              context.projects[len(context.projects)-1].buildPre(context.variant)
          else:
            context.projects[len(context.projects)-1].buildPre(context.variant)
        else:
          if not (element.timing == None):
            if (element.timing.getContent() == "discover"):
              if not (element.build(context.project, os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), os.path.basename(context.project.directory.getContent())), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent()), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), "install"), {}, context.variant)):
                context.error = "Discover time pre build stop failure!"
      elif (tag == "post"):
        for key in elements:
          for value in elements[key]:
            element.instructions.append(value)
        if (parent.tag == "project"):
          context.projects[len(context.projects)-1].post = element
          if not (element.timing == None):
            if (element.timing.getContent() == "discover"):
              context.projects[len(context.projects)-1].buildPost(context.variant)
          else:
            context.projects[len(context.projects)-1].buildPost(context.variant)
        else:
          if not (element.timing == None):
            if (element.timing.getContent() == "discover"):
              if not (element.build(context.project, os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), os.path.basename(context.project.directory.getContent())), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent()), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), "install"), {}, context.variant)):
                context.error = "Discover time post build stop failure!"
      elif (tag == "generator"):
        output = ensure(node.text)+flatten(output).strip()
        element = Generator()
        element.string = String(output.strip())
        if ("architecture" in node.attrib):
          architecture = Architecture()
          architecture.string = String(node.attrib["architecture"].strip())
          element.architecture = architecture
      elif (tag == "json"):
        output = ensure(node.text)+flatten(output).strip()
        dictionary = json.loads(output.strip())
        if (node.attrib["key"] in dictionary):
          output = dictionary[node.attrib["key"]]
        else:
          output = ""
        context.log(node, output+"\n")
      elif (tag == "case"):
        output = ensure(node.text)+flatten(output).strip()
        output = output.strip()
        context.log(node, output+"\n")
      elif (tag == "project"):
        if ("dependencies" in elements):
          element.dependencies = elements["dependencies"][0]
          elements["dependencies"][0] = None
        if ("targets" in elements):
          element.targets = elements["targets"][0]
          elements["targets"][0] = None
        if ("pre" in elements):
          for pre in elements["pre"]:
            element.pre = pre
            if not (pre.timing == None):
              if (pre.timing.getContent() == "parse"):
                element.buildPre(context.variant)
            else:
              element.buildPre(context.variant)
            break
          elements["pre"] = None
        if ("post" in elements):
          for post in elements["post"]:
            element.post = post
            if not (post.timing == None):
              if (post.timing.getContent() == "parse"):
                element.buildPost(context.variant)
            else:
              element.buildPost(context.variant)
            break
          elements["post"] = None
        context.log(node, element.toString()+"\n")
      elif (tag == "buildster"):
        context.log(node, element.toString()+"\n")
      elif (tag == "target"):
        if ("subpath" in elements):
          element.subpath = elements["subpath"][0]
          elements["subpath"][0] = None
        if ("label" in elements):
          element.label = elements["label"][0]
          elements["label"][0] = None
        if ("arguments" in elements):
          for arguments in elements["arguments"]:
            element.arguments = arguments
            break
          elements["arguments"] = None
        if ("packages" in elements):
          for packages in elements["packages"]:
            element.packages = packages
            break
          elements["packages"] = None
        if ("modules" in elements):
          for modules in elements["modules"]:
            element.modules = modules
            break
          elements["modules"] = None
        if ("definitions" in elements):
          for definitions in elements["definitions"]:
            element.definitions = definitions
            break
          elements["definitions"] = None
        if ("links" in elements):
          for links in elements["links"]:
            element.links = links
            break
          elements["links"] = None
        if ("imports" in elements):
          for imports in elements["imports"]:
            element.imports = imports
            break
          elements["imports"] = None
        if ("exports" in elements):
          for exports in elements["exports"]:
            element.exports = exports
            break
          elements["exports"] = None
        if ("generator" in elements):
          for generator in elements["generator"]:
            element.generator = generator
            break
          elements["generator"] = None
        if ("pre" in elements):
          for pre in elements["pre"]:
            element.pre = pre
            if not (pre.timing == None):
              if (pre.timing.getContent() == "parse"):
                if not (pre.build(context.project, os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), os.path.basename(context.project.directory.getContent())), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent()), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), "install"), {}, variant)):
                  context.error = "Parse time pre build stop failure!"
            break
          elements["pre"] = None
        if ("post" in elements):
          for post in elements["post"]:
            element.post = post
            if not (post.timing == None):
              if (post.timing.getContent() == "parse"):
                if not (post.build(context.project, os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), os.path.basename(context.project.directory.getContent())), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent()), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), "install"), {}, variant)):
                  context.error = "Parse time post build stop failure!"
            break
          elements["post"] = None
        context.log(node, element.toString()+"\n")
      elif (tag == "export"):
        if ("type" in node.attrib):
          element.export = String(node.attrib["type"])
        if ("except" in node.attrib):
          element.exceptions = String(node.attrib["except"])
        if ("key" in elements):
          for key in elements["key"]:
            element.key = key
            break
          elements["key"] = None
        if ("value" in elements):
          for value in elements["value"]:
            element.value = value
            break
          elements["value"] = None
      elif (tag == "search"):
        types = node.attrib["type"]
        roots = None
        if ("root" in elements):
          for root in elements["root"]:
            roots = root.getContent().strip()
            break
          elements["root"] = None
        if ("term" in elements):
          for term in elements["term"]:
            terms = term.getContent().strip()
            break
          elements["term"] = None
        if not ((roots == None) or (terms == None)):
          output = None
          for root, folders, files in os.walk(roots):
            if (types == "file"):
              for name in files:
                if (name == terms):
                  output = os.path.join(root, name)
                  break
              if not (output == None):
                break
          if (output == None):
            output = ""
        else:
          output = ""
      else:
        success = False
    if (success):
      if not (element == None):
        element.node = node
        if (type(element) == Project):
          if not (element in context.projects):
            context.projects.append(element)
          element.owner = context.root
          element.context = context
          context.record(node, element.toString()+"\n")
        elif (type(element) == Buildster):
          context.root = element
          element.context = context
          context.record(node, element.toString()+"\n")
        else:
          if not (tag in context.conditionals):
            if not (tag in elements):
              elements[tag] = []
            elements[tag].append(element)
    else:
      if not (children):
        if not (tag in context.substitutes):
          output = ensure(node.text)+flatten(output).strip()
          context.log(node, output+"\n")
  else:
    result = False
  if not (context.error == None):
    context.report(node, str(context.error))
    result = False
  if not (result):
    context.log(node, "Error!")
  else:
    context.nodes[node] = element
    if not (element == None):
      parent = get_parent(parents, None)
      if (parent in context.nodes):
        element.parent = context.nodes[parent]
  #context.log(node, "NODE_END\n")
  return [result, output, elements]

def run(target, data, environment):
  variants = []
  variants.append("Debug")
  variants.append("Release")
  for variant in variants:
    dictionary = {}
    for i in range(len(data)):
      element = data[i]
      elements = element.split("=")
      if (len(elements) == 2):
        left = elements[0].strip()
        right = elements[1].strip()
        dictionary[left] = right
    if ("BUILDSTER_VARIANT" in dictionary):
      if not (variant == dictionary["BUILDSTER_VARIANT"]):
        continue
    for key in environment:
      dictionary[key] = environment[key]
    tree = xml_tree.parse(target)
    base = tree.getroot()
    if not (base.tag == "buildster"):
      return False
    context = Context(dictionary, variant)
    if ("directory" in base.attrib):
      context.root = Buildster()
      context.root.node = base
      context.root.context = context
      context.root.directory = Path(String(base.attrib["directory"]))
    for child in base:
      if (child.tag == "project"):
        context.project = Project()
        context.project.node = child
        context.project.context = context
        if ("directory" in child.attrib):
          context.project.diretory = Path(String(child.attrib["directory"]))
        break
    result = handle(context, base, 0, [None])
    if not (result[0]):
      context.report()
      return False
    output = result[1]
    elements = result[2]
    if not (context.build(context, variant)):
      context.report()
      return False
    if not (context.distribute(context, context.root.distribution.getContent(), variant)):
      context.report()
      return False
    context.report()
  return True

def main(environment = None):
  result = 0
  try:
    arguments = sys.argv
    length = len(arguments)
    if (length > 1):
      data = []
      if (length > 2):
        data = arguments[2:]
      if (environment == None):
        environment = os.environ.copy()
      code = run(arguments[1].strip(), data, environment)
      if not (code):
        print("Error! "+str(code))
        result = -1
    else:
      result = -2
  except Exception as exception:
    logging.error(traceback.format_exc())
    result = -3
  return result

if (__name__ == "__main__"):
  sys.exit(main())
