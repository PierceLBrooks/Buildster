
# Author: Pierce Brooks

import re
import os
import ast
import ssl
import sys
import copy
import json
import stat
import shlex
import shutil
import base64
import urllib
import fnmatch
import pathlib
import zipfile
import tarfile
import inspect
import logging
import pyunpack
import platform
import importlib
import traceback
import subprocess
import multiprocessing
import xml.etree.ElementTree as xml_tree
from urllib.parse import urlparse, unquote
from urllib.request import urlretrieve
from datetime import datetime

from .list import List
from .content import Content
from .path import Path
from .label import Label
from .build import Export
from .build import Import
from .dependency import Dependency

from .utilities import *

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
        installation = self.content[i].getPath(owner, variant, "install").replace("\\", "/")
        if (os.path.isdir(installation)):
          for root, folders, files in os.walk(installation):
            for name in files:
              target = os.path.join(root, name).replace("\\", "/")
              status = os.stat(target)
              chmod(target, status.st_mode|stat.S_IEXEC)
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

