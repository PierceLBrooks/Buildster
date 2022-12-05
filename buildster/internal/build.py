
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

from .internal.element import Element
from .internal.content import Content
from .internal.generator import Generator
from .internal.label import Label
from .internal.exporter import Export
from .internal.importer import Import

from .internal.utilities import *

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
    
