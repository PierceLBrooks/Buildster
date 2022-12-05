
# Author: Pierce Brooks

import os
import stat
import platform

from .element import Element
from .path import Path
from .dependency_list import DependencyList
from .target_list import TargetList

from .utilities import *

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
    if ("Context" in str(type(context))):
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
    if not (os.path.isdir(path)):
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
          chmod(target, status.st_mode|stat.S_IEXEC)
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

