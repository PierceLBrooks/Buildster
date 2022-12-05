
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
from .content import Content
from .build_instruction import BuildInstruction
from .shell_build_instruction import ShellBuildInstruction

from .utilities import *

class ShellsBuildInstruction(BuildInstruction):
  def __init__(self, arguments = None, generator = None, source = None):
    super(ShellsBuildInstruction, self).__init__(arguments)
    self.shells = []
    
  def build(self, owner, path, subpath, installation, imports, variant):
    length = len(self.shells)
    if not (self.getPre() == None):
      if not (self.getPre().timing == None):
        if (self.getPre().timing.getContent() == "build"):
          if not (self.getPre().build(owner, path, subpath, installation, imports, variant)):
            return False
      else:
        if not (self.getPre().build(owner, path, subpath, installation, imports, variant)):
          return False
    for i in range(length):
      if ("ShellBuildInstruction" in str(type(self.shells[i]))):
        if not (self.shells[i].build(owner, path, subpath, installation, imports, variant)):
          return False
      else:
        owner.getContext().log(self.node, str(type(self.shells[i])))
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
    
  def install(self, owner, path, subpath, installation, variant):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.shells)+">"
    
