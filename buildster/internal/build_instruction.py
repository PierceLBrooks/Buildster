
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
from .build import Build
from .string import String
from .list import List
from .path import Path
from .argument import Argument
from .argument_list import ArgumentList

from .utilities import *

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
    
