
# Author: Pierce Brooks

import os

from .branch import Branch
from .remote_dependency import RemoteDependency
from .credentials import Credentials

from .utilities import *

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
    
