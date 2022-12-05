
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

from .build import Build
from .string import String
from .list import List
from .content import Content
from .generator import Generator
from .path import Path
from .native import Native
from .native_list import NativeList
from .build import Export
from .build_instruction import BuildInstruction

from .utilities import *

class CmakeBuildInstruction(BuildInstruction):
  def __init__(self, arguments = None, generator = None, source = None, natives = None):
    super(CmakeBuildInstruction, self).__init__(arguments)
    self.generator = None
    if (type(generator) == Generator):
      self.generator = generator
    self.source = None
    if (type(source) == Path):
      self.source = source
    self.natives = None
    if (type(natives) == NativeList):
      self.natives = natives
      
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
    natives = None
    generator = None
    architecture = None
    if not (self.generator == None):
      generator = self.generator.getContent()
      if not (self.generator.architecture == None):
        architecture = self.generator.architecture.getContent()
    if not (self.natives == None):
      natives = self.natives.getContent()
      for i in range(len(natives)):
        natives[i] = natives[i].strip()
        if (len(natives[i]) == 0):
          natives[i] = None
      while (None in natives):
        natives.remove(None)
    path = os.path.join(cmake, variant.lower()).replace("\\", "/")
    result = cmake_configure(generator, architecture, arguments+["-DCMAKE_BUILD_TYPE="+variant], os.path.join(path, "..", self.source.getContent()).replace("\\", "/"), path, installation, variant)
    owner.getContext().log(self.node, result)
    result = cmake_build(os.path.join(cmake, variant.lower()).replace("\\", "/"), variant, natives)
    owner.getContext().log(self.node, result)
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    cmake = self.getPath(path, subpath)
    if not (self.installVariant(owner, cmake, installation, variant)):
      return False
    return True

  def installVariant(self, owner, cmake, installation, variant):
    natives = None
    if not (self.natives == None):
      natives = self.natives.getContent()
      for i in range(len(natives)):
        natives[i] = natives[i].strip()
        if (len(natives[i]) == 0):
          natives[i] = None
      while (None in natives):
        natives.remove(None)
    result = cmake_install(os.path.join(cmake, variant.lower()).replace("\\", "/"), variant, os.path.join(installation, variant.lower()).replace("\\", "/"), natives)
    owner.getContext().log(self.node, result)
    return True
    
  def __str__(self):
    return "<"+self.toString(self.arguments)+", "+self.toString(self.generator)+", "+self.toString(self.source)+">"
    
