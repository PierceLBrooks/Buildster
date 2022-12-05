
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

from .internal.build import Build
from .internal.string import String
from .internal.build_instruction import BuildInstruction

from .internal.utilities import *

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
    
