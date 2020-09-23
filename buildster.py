
# Author: Pierce Brooks

import os
import sys
import shlex
import inspect
import platform
import subprocess
import xml.etree.ElementTree as xml_tree
from datetime import datetime

def wd():
  filename = inspect.getframeinfo(inspect.currentframe()).filename
  path = os.path.dirname(os.path.abspath(filename))
  return path

def write(descriptor, line):
  descriptor.write(line+"\n")
  
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
    result = subprocess.check_output(command, env=environment)
  except:
    return ""
  return result.decode("UTF-8")

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

def cmake_configure(generator, arguments, source, path, installation, environment = None):
  length = len(arguments)
  command = []
  command.append("cmake")
  command.append("-G")
  command.append(generator)
  for i in range(length):
    command.append(arguments[i])
  command.append("-DCMAKE_INSTALL_PREFIX="+installation)
  command.append(source)
  if not (os.path.isdir(path)):
    os.makedirs(path)
  cwd = os.getcwd()
  os.chdir(path)
  result = execute_command(command, environment)
  os.chdir(cwd)
  return result
  
def cmake_build(path, environment = None):
  command = []
  command.append("cmake")
  command.append("--build")
  command.append(path)
  result = execute_command(command, environment)
  return result
  
def cmake_install(path, installation, environment = None):
  command = []
  command.append("cmake")
  command.append("--build")
  command.append(path)
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
    if ((str(type(other)) == "str") or (str(type(other)) == "list")):
      return str(other)
    if not (isinstance(other, Object)):
      return "/INVALID/"
    return other.toString()
    
class Element(Object):
  def __init__(self):
    super(Element, self).__init__()
    self.parent = None
    
  def build(self, owner):
    return True
    
  def getParent(self):
    return self.parent
    
class Build(Element):
  def __init(self):
    super(Build, self).__init__()
    
  def build(self, owner):
    owner.context.record(self.node, str(self.importsContent))
    owner.context.record(self.node, str(self.exportsContent))
    return True
    
  def addExport(self, add):
    if not (isinstance(add, Export)):
      return False
    success = self.doExport(add.key.getContent(), add.value.getContent(), add.export.getContent())
    if not (success):
      return False
    return True
    
  def addImport(self, add):
    if not (isinstance(add, Import)):
      return False
    success = self.doImport(add.getContent())
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export):
    return True
    
  def doImport(self, label):
    return True
    
  def getExports(self):
    return []
    
  def getGenerator(self, owner):
    name = platform.system()
    if (name == "Windows"):
      return "MinGW Makefiles"
    if (name == "Linux"):
      return "Unix Makefiles"
    if (name == "Darwin"):
      return "Unix Makefiles"
    return ""
    
  def getLabel(self):
    return ""
    
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
      
  def build(self, owner):
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

class Generator(Object):
  def __init__(self, string = None):
    super(Generator, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"

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
      
  def build(self, owner):
    return True
    
  def getContent(self):
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
class ArgumentList(List):
  def __init__(self):
    super(ArgumentList, self).__init__()
    
  def build(self, owner):
    return True
        
  def addArgument(self, argument):
    if not (isinstance(argument, Argument)):
      return False
    return super(ArgumentList, self).add(argument)
    
class Definition(Object):
  def __init__(self, key = None, value = None):
    super(Definition, self).__init__()
    self.key = None
    if (type(key) == Key):
      self.key = key
    self.value = None
    if (type(value) == Value):
      self.value = value
      
  def __str__(self):
    return "<"+self.toString(self.key)+", "+self.toString(self.value)+">"
    
class DefinitionList(List):
  def __init__(self):
    super(DefinitionList, self).__init__()
    
  def build(self, owner):
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
    
  def build(self, owner):
    return True
        
  def addLink(self, link):
    if not (isinstance(link, Link)):
      return False
    return super(LinkList, self).add(link)
    
class Export(Object):
  def __init__(self, key = None, value = None, export = None):
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
      
  def doExport(self, owner):
    if not (isinstance(owner, Build)):
      return False
    owner.addExport(self)
    return True
      
  def __str__(self):
    return "<"+self.toString(self.key)+", "+self.toString(self.value)+", "+self.toString(self.export)+">"
    
class ExportList(List):
  def __init__(self):
    super(ExportList, self).__init__()
    
  def build(self, owner):
    return True

  def doExport(self, owner):
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Export)):
        if not (self.content[i].doExport(owner)):
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
    
  def doImport(self, owner):
    if not (isinstance(owner, Build)):
      return False
    owner.addImport(self)
    return True
    
  def __str__(self):
    return "<"+self.toString(self.label)+">"
    
class ImportList(List):
  def __init__(self):
    super(ImportList, self).__init__()
    
  def build(self, owner):
    return True

  def doImport(self, owner):
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Import)):
        if not (self.content[i].doImport(owner)):
          return False
    return True

  def addImport(self, add):
    if not (isinstance(add, Import)):
      return False
    return super(ImportList, self).add(add)
    
class BuildInstruction(Object):
  def __init__(self, arguments = None, pre = None, post = None):
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
    
  def build(self, owner, path, subpath, installation, imports):
    return True
    
  def install(self, owner, path, subpath, installation):
    return True
    
  def getPath(self, path, subpath):
    return os.path.join(path, subpath)
    
  def getPre(self):
    return self.pre
  
  def getPost(self):
    return self.post
    
class PreBuildInstruction(BuildInstruction):
  def __init__(self):
    super(PreBuildInstruction, self).__init__()
    self.instructions = []
      
  def build(self, owner, path, subpath, installation, imports):
    length = len(self.instructions)
    for i in range(length):
      if (isinstance(self.instructions[i], BuildInstruction)):
        if not (self.instructions[i].build(owner, path, subpath, installation, imports)):
          return False
    return True
    
  def install(self, owner, path, subpath, installation):
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
      
  def build(self, owner, path, subpath, installation, imports):
    length = len(self.instructions)
    for i in range(length):
      if (isinstance(self.instructions[i], BuildInstruction)):
        if not (self.instructions[i].build(owner, path, subpath, installation, imports)):
          return False
    return True
    
  def install(self, owner, path, subpath, installation):
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
      
  def build(self, owner, path, subpath, installation, imports):
    if (self.generator == None):
      return False
    if (self.source == None):
      return False
    if (self.arguments == None):
      return False
    cmake = self.getPath(path, subpath)
    arguments = self.arguments.getContent()
    arguments.append("-DCMAKE_BUILD_WITH_INSTALL_RPATH=\"TRUE\"")
    exports = owner.getExports(imports)
    for i in range(len(exports)):
      export = exports[i]
      if (export[0] in imports):
        export = export[1]
        for key in export:
          if (export[key][0] == "other"):
            arguments.append("-D"+key+"=\""+export[key][1].replace("\\", "/")+"\"")
          else:
            arguments.append("-D"+key+"="+export[key][1].replace("\\", "/"))
    if not (self.getPre() == None):
      self.getPre().build(owner, path, subpath, installation, imports)
    result = cmake_configure(self.generator.getContent(), arguments, self.source.getContent(), cmake, installation)
    owner.context.log(self.node, result)
    result = cmake_build(cmake)
    owner.context.log(self.node, result)
    if not (self.getPost() == None):
      self.getPost().build(owner, path, subpath, installation, imports)
    return True
    
  def install(self, owner, path, subpath, installation):
    cmake = self.getPath(path, subpath)
    result = cmake_install(cmake, installation)
    owner.context.log(self.node, result)
    return True
    
  def __str__(self):
    return "<"+self.toString(self.arguments)+", "+self.toString(self.generator)+", "+self.toString(self.source)+">"
    
class ShellsBuildInstruction(BuildInstruction):
  def __init__(self, arguments = None, generator = None, source = None):
    super(ShellsBuildInstruction, self).__init__(arguments)
    self.shells = []
      
  def build(self, owner, path, subpath, installation, imports):
    length = len(self.shells)
    if not (self.getPre() == None):
      self.getPre().build(owner, path, subpath, installation, imports)
    for i in range(length):
      if ("ShellBuildInstruction" in str(type(self.shells[i]))):
        if not (self.shells[i].build(owner, path, subpath, installation, imports)):
          return False
      else:
        owner.context.log(self.node, str(type(self.shells[i])))
        return False
    if not (self.getPost() == None):
      self.getPost().build(owner, path, subpath, installation, imports)
    return True
    
  def install(self, owner, path, subpath, installation):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.shells)+">"
    
class ShellBuildInstruction(BuildInstruction):
  def __init__(self, commands = None, work = None):
    super(ShellBuildInstruction, self).__init__(arguments)
    self.commands = None
    self.work = None
      
  def build(self, owner, path, subpath, installation, imports):
    if (self.commands == None):
      return False
    if not ("CommandsBuildInstruction" in str(type(self.commands))):
      return False
    if (self.work == None):
      return False
    if not ("Work" in str(type(self.work))):
      return False
    if not (self.commands.build(owner, self.getPath(path, subpath), self.work.getContent(), installation, imports)):
      return False
    return True
    
  def install(self, owner, path, subpath, installation):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.commands)+">"

class CommandsBuildInstruction(BuildInstruction):
  def __init__(self, arguments = None, generator = None, source = None):
    super(CommandsBuildInstruction, self).__init__(arguments)
    self.commands = []
      
  def build(self, owner, path, subpath, installation, imports):
    length = len(self.commands)
    for i in range(length):
      if ("CommandBuildInstruction" in str(type(self.commands[i]))):
        if not (self.commands[i].build(owner, path, subpath, installation, imports)):
          return False
      else:
        owner.context.log(self.node, str(type(self.commands[i])))
        return False
    return True
    
  def install(self, owner, path, subpath, installation):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.commands)+">"
    
class CommandBuildInstruction(BuildInstruction):
  def __init__(self, arguments = None, generator = None, source = None):
    super(CommandBuildInstruction, self).__init__(arguments)
    self.string = None
    
  def build(self, owner, path, subpath, installation, imports):
    if (self.string == None):
      return False
    command = shlex.split(self.string.getContent().replace("\\", "/"))
    owner.context.log(self.node, self.string.getContent())
    owner.context.log(self.node, str(command))
    owner.context.log(self.node, subpath)
    if not (os.path.isdir(subpath)):
      os.makedirs(subpath)
    cwd = os.getcwd()
    os.chdir(subpath)
    result = execute_command(command, owner.context.environment)
    os.chdir(cwd)
    owner.context.log(self.node, result)
    return True
    
  def install(self, owner, path, subpath, installation):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
class Setter(BuildInstruction):
  def __init__(self, key = None, value = None):
    super(Setter, self).__init__()
    self.key = None
    if (type(key) == Key):
      self.key = key
    self.value = None
    if (type(value) == Value):
      self.value = value
      
  def build(self, owner, path, subpath, installation, imports):
    if not ((self.key == None) or (self.value == None)):
      owner.context.environment[self.key.getContent()] = self.value.getContent()
      owner.context.log(self.node, "<\""+self.key.getContent()+"\" -> \""+self.value.getContent()+"\">")
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
    
  def build(self, owner):
    success = True
    if not (self.imports == None):
      success = self.imports.doImport(self)
    if not (success):
      return False
    if not (self.exports == None):
      success = self.exports.doExport(self)
    if not (success):
      return False
    success = super(Dependency, self).build(owner)
    if not (success):
      return False
    return True
    
  def getPath(self, owner, purpose):
    return adjust(os.path.join(wd(), owner.context.root.directory.getContent(), owner.directory.getContent(), purpose, "dependencies", self.label.getContent()))
    
  def getLabel(self):
    return self.label.getContent()
    
  def doExport(self, key, value, export):
    return True
    
  def doImport(self, label):
    return True
    
  def getExports(self):
    return []

class RemoteDependency(Dependency):
  def __init__(self, url = None):
    super(RemoteDependency, self).__init__()
    self.url = None
    if (type(url) == URL):
      self.url = url
      
  def build(self, owner):
    success = super(RemoteDependency, self).build(owner)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export):
    return True
    
  def doImport(self, label):
    return True
    
  def getExports(self):
    return []

class DependencyList(List):
  def __init__(self):
    super(DependencyList, self).__init__()
    
  def build(self, owner):
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Dependency)):
        if not (self.content[i].build(owner)):
          return False
    return True
        
  def addDependency(self, dependency):
    if not (isinstance(dependency, Dependency)):
      return False
    return super(DependencyList, self).add(dependency)
    
  def getExports(self, imports):
    exports = []
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Dependency)):
        label = self.content[i].getLabel()
        if (label in imports):
          exports.append([label, self.content[i].getExports()])
    return exports

class LocalDependency(Dependency):
  def __init__(self, path = None):
    super(LocalDependency, self).__init__()
    self.exportsContent = {}
    self.importsContent = []
    self.path = None
    if (type(path) == String):
      self.path = path
    
  def build(self, owner):
    installation = self.getPath(owner, "install")
    path = self.getPath(owner, "build")
    success = super(LocalDependency, self).build(owner)
    if not (success):
      return False
    if (self.instruction == None):
      return False
    success = self.instruction.build(owner, path, self.subpath.getContent(), installation, self.importsContent)
    if not (success):
      return False
    success = self.instruction.install(owner, path, self.subpath.getContent(), installation)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export):
    if (key in self.exportsContent):
      return False
    self.exportsContent[key] = [export, value]
    return True
    
  def doImport(self, label):
    if (label in self.importsContent):
      return False
    self.importsContent.append(label)
    return True
    
  def getExports(self):
    return self.exportsContent

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
    self.importsContent = []
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
      owner.context.log(self.node, result)
    cwd = os.getcwd()
    os.chdir(path)
    result = git_checkout(self.branch.getContent())
    owner.context.log(self.node, result)
    result = git_submodule()
    owner.context.log(self.node, result)
    os.chdir(cwd)
    return True
    
  def build(self, owner):
    installation = self.getPath(owner, "install")
    path = self.getPath(owner, "build")
    success = self.clone(owner, path)
    if not (success):
      return False
    success = super(GitRepoDependency, self).build(owner)
    if not (success):
      return False
    if (self.instruction == None):
      return False
    success = self.instruction.build(owner, path, self.subpath.getContent(), installation, self.importsContent)
    if not (success):
      return False
    success = self.instruction.install(owner, path, self.subpath.getContent(), installation)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export):
    if (key in self.exportsContent):
      return False
    self.exportsContent[key] = [export, value]
    return True
    
  def doImport(self, label):
    if (label in self.importsContent):
      return False
    self.importsContent.append(label)
    return True
    
  def getExports(self):
    return self.exportsContent
    
  def __str__(self):
    return "<"+self.toString(self.subpath)+", "+self.toString(self.url)+", "+self.toString(self.branch)+", "+self.toString(self.credentials)+", "+self.toString(self.instruction)+">"
    
class Target(Build):
  def __init__(self, label = None, definitions = None, links = None, imports = None, exports = None):
    super(Target, self).__init__()
    self.label = None
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
      
  def install(self, owner, path, installation):
    result = cmake_install(path, installation)
    owner.context.log(self.node, result)
    return True
    
  def build(self, owner):
    installation = self.getPath(owner, "install")
    path = self.getPath(owner, "build")
    success = True
    if not (self.imports == None):
      success = self.imports.doImport(self)
    if not (success):
      return False
    if not (self.exports == None):
      success = self.exports.doExport(self)
    if not (success):
      return False
    success = super(Target, self).build(owner)
    if not (success):
      return False
    project = self.getFiles(owner)
    includes = self.getIncludes(owner)
    links = []
    builds = []
    labels = {}
    imports = {}
    exports = {}
    for i in range(len(owner.dependencies.content)):
      dependency = owner.dependencies.content[i]
      if not (dependency == self):
        builds.append(dependency)
    for i in range(len(owner.targets.content)):
      target = owner.targets.content[i]
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
    if not (os.path.isdir(path)):
      os.makedirs(path)
    descriptor = open(os.path.join(path, "CMakeLists.txt"), "w")
    write(descriptor, "cmake_minimum_required(VERSION 3.1.0 FATAL_ERROR)")
    write(descriptor, "set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)")
    write(descriptor, "set(CMAKE_CXX_FLAGS \"${CMAKE_CXX_FLAGS} -std=c++14\")")
    write(descriptor, "set(CMAKE_EXE_LINKER_FLAGS \"${CMAKE_EXE_LINKER_FLAGS} -std=c++14\")")
    write(descriptor, "set(CMAKE_SHARED_LINKER_FLAGS \"${CMAKE_SHARED_LINKER_FLAGS} -std=c++14\")")
    write(descriptor, "project(\""+self.label.getContent()+"Project\")")
    for i in range(len(includes)):
      write(descriptor, "include_directories(\""+includes[i].replace("\\", "/")+"\")")
    for export in exports:
      if (exports[export][1] == "headers"):
        headers = exports[export][0].replace("\\", "/")
        if not (os.path.isdir(headers)):
          os.makedirs(headers)
        write(descriptor, "include_directories(\""+headers.replace("\\", "/")+"\")")
      elif (exports[export][1] == "libraries"):
        libraries = exports[export][0].replace("\\", "/")
        if not (os.path.isdir(libraries)):
          os.makedirs(libraries)
        for root, folders, files in os.walk(libraries):
          for name in files:
            for i in range(len(owner.context.libraries)):
              if (name.endswith("."+owner.context.libraries[i])):
                links.append(str(root).replace("\\", "/"))
                write(descriptor, "link_directories(\""+links[len(links)-1]+"\")")
                name = None
                break
            if (name == None):
              break
      else:
        pass
    if not (self.links == None):
      for i in range(len(self.links.content)):
        link = self.links.content[i].getContent().strip()
        if ("*" in link):
          for j in range(len(links)):
            for root, folders, files in os.walk(links[j]):
              for name in files:
                if (link.replace("*", "") in name):
                  for k in range(len(owner.context.libraries)):
                    if (name.endswith("."+owner.context.libraries[k])):
                      write(descriptor, "link_libraries(\""+name+"\")")
                      break
        else:
          write(descriptor, "link_libraries("+link+")")
    if (len(project) > 0):
      write(descriptor, "set(HEADERS )")
      write(descriptor, "set(FILES )")
      for i in range(len(project)):
        for j in range(len(owner.context.extensions)):
          extension = "."+owner.context.extensions[j]
          if (project[i].endswith(extension)):
            write(descriptor, "list(APPEND FILES \""+project[i].replace("\\", "/")+"\")")
            for k in range(len(owner.context.headers)):
              if (extension == "."+owner.context.headers[k]):
                write(descriptor, "list(APPEND HEADERS \""+project[i].replace("\\", "/")+"\")")
            break
      target = str(type(self))
      if ("Executable" in target):
        write(descriptor, "add_executable("+self.label.getContent()+" ${FILES})")
      elif ("Library" in target):
        write(descriptor, "add_library("+self.label.getContent()+" ${FILES})")
        write(descriptor, "set_target_properties("+self.label.getContent()+" PROPERTIES PUBLIC_HEADER \"${HEADERS}\")")
      else:
        pass
      write(descriptor, "install(TARGETS "+self.label.getContent()+")")
    else:
      print(str(len(files)))
    descriptor.close()
    generator = self.getGenerator(owner)
    arguments = []
    result = cmake_configure(generator, arguments, path, os.path.join(path, "build"), installation)
    owner.context.log(self.node, result)
    result = cmake_build(os.path.join(path, "build"))
    owner.context.log(self.node, result)
    success = self.install(owner, os.path.join(path, "build"), installation)
    if not (success):
      return False
    return True

  def doExport(self, key, value, export):
    return True
    
  def doImport(self, label):
    return True
    
  def getExports(self):
    return []
    
  def getPath(self, owner, purpose):
    return adjust(os.path.join(wd(), owner.context.root.directory.getContent(), owner.directory.getContent(), purpose, "targets", self.label.getContent()))
    
  def getLabel(self):
    return self.label.getContent()
    
  def getFiles(self, owner):
    result = []
    path = adjust(os.path.join(wd(), owner.directory.getContent(), self.label.getContent()))
    for root, folders, files in os.walk(path):
      for name in files:
        result.append(os.path.join(root, name))
    return result

  def getIncludes(self, owner):
    result = []
    path = adjust(os.path.join(wd(), owner.directory.getContent(), self.label.getContent()))
    for root, folders, files in os.walk(path):
      result.append(root)
    return result
    
class TargetList(List):
  def __init__(self):
    super(TargetList, self).__init__()
    
  def build(self, owner):
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Target)):
        if not (self.content[i].build(owner)):
          return False
    return True
        
  def addTarget(self, target):
    if not (isinstance(target, Target)):
      return False
    return super(TargetList, self).add(target)
    
  def getExports(self, imports):
    exports = []
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Target)):
        label = self.content[i].getLabel()
        if (label in imports):
          exports.append([label, self.content[i].getExports()])
    return exports
    
class ExecutableTarget(Target):
  def __init__(self, label = None, definitions = None, links = None, imports = None):
    super(ExecutableTarget, self).__init__(label, definitions, links, imports)
    self.exportsContent = {}
    self.importsContent = []
    
  def build(self, owner):
    success = super(ExecutableTarget, self).build(owner)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export):
    if (key in self.exportsContent):
      return False
    self.exportsContent[key] = [export, value]
    return True
    
  def doImport(self, label):
    if (label in self.importsContent):
      return False
    self.importsContent.append(label)
    return True
    
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.definitions)+", "+self.toString(self.links)+", "+self.toString(self.imports)+">"
    
class LibraryTarget(Target):
  def __init__(self, label = None, definitions = None, links = None, imports = None, exports = None):
    super(LibraryTarget, self).__init__(label, definitions, links, imports, exports)
    self.exportsContent = {}
    self.importsContent = []
    
  def build(self, owner):
    success = super(LibraryTarget, self).build(owner)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export):
    if (key in self.exportsContent):
      return False
    self.exportsContent[key] = [export, value]
    return True
    
  def doImport(self, label):
    if (label in self.importsContent):
      return False
    self.importsContent.append(label)
    return True
    
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.definitions)+", "+self.toString(self.links)+", "+self.toString(self.imports)+", "+self.toString(self.exports)+">"
    
class Project(Element):
  def __init__(self, dependencies = None, targets = None, directory = None, context = None):
    super(Project, self).__init__()
    self.dependencies = None
    self.targets = None
    self.directory = None
    self.context = None
    if (type(dependencies) == DependencyList):
      self.dependencies = dependencies
    if (type(targets) == TargetList):
      self.targets = targets
    if (type(directory) == Path):
      self.directory = directory
    if (str(type(context)) == "Context"):
      self.context = context
      
  def build(self, owner):
    if not (self.dependencies == None):
      if not (self.dependencies.build(self)):
        return False
    if not (self.targets == None):
      if not (self.targets.build(self)):
        return False
    return True
    
  def getExports(self, imports):
    exports = []
    if not (self.dependencies == None):
      exports = exports+self.dependencies.getExports(imports)
    if not (self.targets == None):
      exports = exports+self.targets.getExports(imports)
    return exports
    
  def __str__(self):
    return "<"+self.toString(self.dependencies)+", "+self.toString(self.targets)+", "+self.toString(self.directory)+">"

class Buildster(Element):
  def __init__(self, directory = None, context = None):
    super(Buildster, self).__init__()
    self.directory = None
    self.context = None
    if (str(type(directory)) == "Path"):
      self.directory = directory
    if (str(type(context)) == "Context"):
      self.context = context
      
  def build(self, owner):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.directory)+">"

class Context(Element):
  def __init__(self, data, debug = True):
    super(Context, self).__init__()
    
    
    self.extensions = []
    
    self.extensions.append("c")
    self.extensions.append("cc")
    self.extensions.append("cpp")
    self.extensions.append("h")
    self.extensions.append("hpp")
    self.extensions.append("inl")
    self.extensions.append("dll")
    self.extensions.append("a")
    self.extensions.append("lib")
    self.extensions.append("dylib")
    
    self.headers = []
    
    self.headers.append("h")
    self.headers.append("hpp")
    self.headers.append("inl")
    
    self.sources = []
    
    self.sources.append("c")
    self.sources.append("cc")
    self.sources.append("cpp")
    
    self.libraries = []
    
    self.libraries.append("dll")
    self.libraries.append("a")
    self.libraries.append("lib")
    self.libraries.append("dylib")
    
    self.conditionals = []
    
    self.conditionals.append("if")
    self.conditionals.append("if_check")
    self.conditionals.append("switch")
    
    self.nonconditionals = []
    self.nonconditionals.append("data")
    self.nonconditionals.append("install")
    self.nonconditionals.append("origin")
    self.nonconditionals.append("case")
    self.nonconditionals.append("default")
    self.nonconditionals.append("search")
    self.nonconditionals.append("set")
    
    self.processes = []
    
    self.processes.append("message")
    self.processes.append("quit")
    
    self.any = "any"
    
    
    nodeTags = []
    
    for conditional in self.conditionals:
      nodeTags.append(conditional)
    for process in self.processes:
      nodeTags.append(process)
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
    nodeTags.append("root")
    nodeTags.append("work")
    nodeTags.append("shells")
    nodeTags.append("shell")
    nodeTags.append("commands")
    nodeTags.append("command")
    nodeTags.append("search")
    nodeTags.append("term")
    nodeTags.append("set")
    nodeTags.append("pre")
    nodeTags.append("post")
    
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
    
    nodeParents["set"].append(self.any)
    nodeParents["search"].append(self.any)
    nodeParents["origin"].append(self.any)
    nodeParents["install"].append(self.any)
    nodeParents["message"].append(self.any)
    nodeParents["quit"].append(self.any)
    nodeParents["data"].append(self.any)
    nodeParents["if"].append(self.any)
    nodeParents["if_check"].append(self.any)
    nodeParents["switch"].append(self.any)
    nodeParents["case"].append("switch")
    nodeParents["else"].append("if")
    nodeParents["else"].append("if_check")
    #nodeParents["buildster"].append("")
    nodeParents["project"].append("buildster")
    nodeParents["dependencies"].append("project")
    nodeParents["dependency"].append("dependencies")
    nodeParents["remote"].append("dependency")
    nodeParents["local"].append("dependency")
    nodeParents["subpath"].append("dependency")
    nodeParents["path"].append("local")
    nodeParents["git_repo"].append("remote")
    nodeParents["url"].append("remote")
    nodeParents["branch"].append("git_repo")
    nodeParents["credentials"].append("git_repo")
    nodeParents["username"].append("credentials")
    nodeParents["password"].append("credentials")
    nodeParents["targets"].append("project")
    nodeParents["target"].append("targets")
    nodeParents["label"].append("dependency")
    nodeParents["label"].append("target")
    nodeParents["definitions"].append("target")
    nodeParents["definition"].append("definitions")
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
    nodeParents["argument"].append("arguments")
    nodeParents["cmake"].append("build")
    nodeParents["generator"].append("cmake")
    nodeParents["generator"].append("target")
    nodeParents["source"].append("cmake")
    nodeParents["exports"].append("dependency")
    nodeParents["exports"].append("target")
    nodeParents["export"].append("exports")
    nodeParents["imports"].append("dependency")
    nodeParents["imports"].append("target")
    nodeParents["import"].append("imports")
    nodeParents["root"].append("search")
    nodeParents["term"].append("search")
    nodeParents["work"].append("shell")
    nodeParents["shells"].append("build")
    nodeParents["shell"].append("shells")
    nodeParents["commands"].append("shell")
    nodeParents["command"].append("commands")
    nodeParents["pre"].append("build")
    nodeParents["post"].append("build")
    
    nodeAttributes["data"].append("id")
    nodeAttributes["if"].append("id")
    nodeAttributes["if_check"].append("id")
    nodeAttributes["if_check"].append("check")
    nodeAttributes["switch"].append("id")
    nodeAttributes["case"].append("check")
    nodeAttributes["buildster"].append("directory")
    nodeAttributes["project"].append("directory")
    nodeAttributes["export"].append("type")
    nodeAttributes["target"].append("type")
    nodeAttributes["search"].append("type")
    
    
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
    self.nodes = {}
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
    
  def build(self, owner):
    self.tier = None
    self.log(self.node, "CONTEXT_BUILD_BEGIN\n")
    for i in range(len(self.projects)):
      if not (self.projects[i].build(self)):
        self.tier = None
        self.log(self.node, "CONTEXT_BUILD_END\n")
        return False
    self.tier = None
    self.log(self.node, "CONTEXT_BUILD_END\n")
    return True
    
  def check(self, node, parent):
    tag = node.tag
    if (tag == "label"):
      if (parent == None):
        return True
    if not (tag in self.nodeTags):
      self.record(node, "Node Tag Error...")
      return False
    if (parent == None):
      if (tag in self.nodeParents):
        self.record(node, "Node Parent Error 1...")
        return False
    else:
      if not (tag in self.nodeParents):
        self.record(node, "Node Parent Error 2...")
        return False
      if not (self.any in self.nodeParents[tag]):
        if not (parent.tag in self.nodeParents[tag]):
          self.record(node, "Node Parent Error 3...")
          return False
    if (tag in self.nodeAttributes):
      attributes = self.nodeAttributes[tag]
      for attribute in attributes:
        if not (attribute in node.attrib):
          self.record(node, "Node Attribute Error...")
          return False
    return True
  
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
    print(tag+now.strftime("%d-%m-%Y@%H:%M:%S")+"\n")
    if (self.tier == None):
      print("\""+str(message)+"\"\n")
      return
    print(("  "*self.tier)+str(self.tier)+": \""+str(message)+"\"")
  
  def record(self, node, message):
    self.records.append([self.tier, message, node])
    
  def report(self):
    self.tier = None
    self.log(None, "CONTEXT_REPORT_BEGIN\n")
    for i in range(len(self.records)):
      self.tier = self.records[i][0]
      self.log(self.records[i][2], self.records[i][1])
    self.tier = None
    self.log(None, "CONTEXT_REPORT_END\n")

def handle(context, node, tier, parents):
  parent = parents[len(parents)-1]
  quit = False
  result = True
  tag = node.tag
  output = []
  elements = {}
  element = None
  null = [True, "", {}]
  context.tier = tier
  context.log(node, tag)
  #context.log(node, "NODE_BEGIN\n")
  if (context.check(node, parent)):
    element = None
    if (tag in context.conditionals):
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
        id = parent.attrib["id"]
        if (parent.tag == "if"):
          if (context.find(id)):
            context.log(node, id+" does not exist in data!")
            return null
        elif (parent.tag == "if_check"):
          check = parent.attrib["check"]
          if (ensure(context.get(id)).strip() == check):
            context.log(node, id+" does not match \""+check+"\" check!")
            return null
        else:
          return null
    elif (tag == "quit"):
      quit = True
      result = False
    elif (tag == "buildster"):
      element = Buildster()
      element.directory = Path(String(node.attrib["directory"]))
      context.root = element
    elif (tag == "project"):
      element = Project()
      element.directory = Path(String(node.attrib["directory"]))
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
    elif (tag == "target"):
      target = node.attrib["type"]
      if (target == "executable"):
        element = ExecutableTarget()
      elif (target == "library"):
        element = LibraryTarget()
      else:
        pass
    elif (tag == "pre"):
      element = PreBuildInstruction()
    elif (tag == "post"):
      element = PostBuildInstruction()
    elif (tag == "build"):
      element = BuildInstruction()
    elif (tag == "arguments"):
      element = ArgumentList()
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
    context.tier = tier
    #context.log(tag)
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
      elif (tag == "generator"):
        output = ensure(node.text)+flatten(output).strip()
        element = Generator()
        element.string = String(output.strip())
      elif (tag == "source"):
        output = ensure(node.text)+flatten(output).strip()
        element = Path()
        element.string = String(output.strip())
      elif (tag == "argument"):
        output = ensure(node.text)+flatten(output).strip()
        element = Argument()
        element.string = String(output.strip())
      elif (tag == "work"):
        output = ensure(node.text)+flatten(output).strip()
        element = Work()
        element.string = String(output.strip())
      elif (tag == "arguments"):
        if ("argument" in elements):
          for argument in elements["argument"]:
            element.addArgument(argument)
          elements["argument"] = None
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
            break
          elements["pre"] = None
        if ("post" in elements):
          for post in elements["post"]:
            element.post = post
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
      elif (tag == "install"):
        dependency = get_parent(parents, "dependency")
        if not (dependency == None):
          label = get_child(dependency, "label")
          if not (label == None):
            project = get_parent(parents, "project")
            if not (project == None):
              temp = handle(context, label, tier, [None])
              output = adjust(os.path.join(wd(), context.root.getContent(), project.attrib["directory"], "install", "dependencies", temp[1]))
            else:
              context.log(node, "No \"project\" ancestor for \"label\" node!\n")
              result = False
          else:
            context.log(node, "No \"label\" descendant for \"dependency\" node!\n")
            result = False
        else:
          target = get_parent(parents, "target")
          if not (target == None):
            label = get_child(target, "label")
            if not (label == None):
              project = get_parent(parents, "project")
              if not (project == None):
                temp = handle(context, label, tier, [None])
                output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"], "install", "targets", temp[1]))
              else:
                context.log(node, "No \"project\" ancestor for \"label\" node!\n")
                result = False
            else:
              context.log(node, "No \"label\" descendant for \"target\" node!\n")
              result = False
          else:
            context.log(node, "No \"dependency\" or \"target\" ancestor for \"install\" node!\n")
            result = False
      elif (tag == "origin"):
        dependency = get_parent(parents, "dependency")
        if not (dependency == None):
          label = get_child(dependency, "label")
          if not (label == None):
            project = get_parent(parents, "project")
            if not (project == None):
              temp = handle(context, label, tier, [None])
              output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"], "build", "dependencies", temp[1]))
            else:
              context.log(node, "No \"project\" ancestor for \"label\" node!\n")
              result = False
          else:
            context.log(node, "No \"label\" descendant for \"dependency\" node!\n")
            result = False
        else:
          target = get_parent(parents, "target")
          if not (target == None):
            label = get_child(target, "label")
            if not (label == None):
              project = get_parent(parents, "project")
              if not (project == None):
                temp = handle(context, label, tier, [None])
                output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"], "build", "targets", temp[1]))
              else:
                context.log(node, "No \"project\" ancestor for \"label\" node!\n")
                result = False
            else:
              context.log(node, "No \"label\" descendant for \"target\" node!\n")
              result = False
          else:
            context.log(node, "No \"dependency\" or \"target\" ancestor for \"origin\" node!\n")
            result = False
      elif (tag == "default"):
        output = ensure(node.text)+flatten(output).strip()
        output = output.strip()
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
      elif (tag == "pre"):
        element = PreBuildInstruction()
        for key in elements:
          for value in elements[key]:
            element.instructions.append(value)
      elif (tag == "post"):
        element = PostBuildInstruction()
        for key in elements:
          for value in elements[key]:
            element.instructions.append(value)
      else:
        success = False
    else:
      if (tag == "data"):
        output = ensure(context.get(node.attrib["id"])).strip()
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
        context.log(node, element.toString()+"\n")
      elif (tag == "buildster"):
        context.log(node, element.toString()+"\n")
      elif (tag == "target"):
        if ("label" in elements):
          element.label = elements["label"][0]
          elements["label"][0] = None
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
        context.log(node, element.toString()+"\n")
      elif (tag == "export"):
        element.export = String(node.attrib["type"])
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
          context.projects.append(element)
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
        output = ensure(node.text)+flatten(output).strip()
        context.log(node, output+"\n")
  else:
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

def run(target, data):
  dictionary = {}
  for i in range(len(data)):
    element = data[i]
    elements = element.split("=")
    if (len(elements) == 2):
      left = elements[0].strip()
      right = elements[1].strip()
      dictionary[left] = right
  tree = xml_tree.parse(target)
  base = tree.getroot()
  if not (base.tag == "buildster"):
    return False
  context = Context(dictionary)
  result = handle(context, base, 0, [None])
  if not (result[0]):
    context.report()
    return False
  output = result[1]
  elements = result[2]
  if not (context.build(context)):
    context.report()
    return False
  context.report()
  return True

if (__name__ == "__main__"):
  result = 0
  arguments = sys.argv
  length = len(arguments)
  if (length > 1):
    data = []
    if (length > 2):
      data = arguments[2:]
    code = run(arguments[1].strip(), data)
    if not (code):
      print("Error!")
      result = -1
  sys.exit(result)
