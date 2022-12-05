
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

from .object import Object
from .element import Element
from .content import Content
from .generator import Generator
from .label import Label
from .key import Key
from .value import Value
from .string import String

from .utilities import *

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
    
