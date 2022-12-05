
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

from .performer import Performer
from .string import String
from .content import Content
from .path import Path

from .utilities import *

class Deleter(Performer):
  def __init__(self, path = None):
    super(Deleter, self).__init__()
    self.path = None
    if (type(path) == Path):
      self.path = path
      
  def getContent(self):
    if (self.path == None):
      return ""
    return self.path.getContent()
    
  def perform(self, context):
    context.log(None, "Deleting \""+self.toString(self.path)+"\"...")
    if (self.path == None):
      return False
    content = self.getContent().strip()
    if (len(content) == 0):
      return False
    if not (os.path.exists(content)):
      context.log(None, "Deleted \""+self.toString(self.path)+"\"!")
      return True
    if (os.path.isfile(content)):
      os.unlink(content)
    else:
      shutil.rmtree(content)
    context.log(None, "Deleted \""+self.toString(self.path)+"\"!")
    return True
    
  def __str__(self):
    return "<"+self.toString(self.path)+">"
    
