
# Author: Pierce Brooks

import os

from .string import String
from .remote_dependency import RemoteDependency

from .utilities import *

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
      if not (retrieve(owner.getContext(), self.url.getContent(), os.path.join(path, content))):
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
    
    
