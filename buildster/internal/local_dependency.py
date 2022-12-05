
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

from .internal.string import String
from .internal.content import Content
from .internal.path import Path
from .internal.exporter import Export
from .internal.importer import Import
from .internal.dependency import Dependency

from .internal.utilities import *

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
    return "<"+self.toString(self.subpath)+", "+self.toString(self.path)+", "+self.toString(self.instruction)+", "+self.toString(self.imports)+", "+self.toString(self.exports)+">"

