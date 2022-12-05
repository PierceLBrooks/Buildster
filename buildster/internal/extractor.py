
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

from .internal.performer import Performer
from .internal.string import String
from .internal.content import Content
from .internal.path import Path

from .internal.utilities import *

class Extractor(Performer):
  def __init__(self, path = None):
    super(Extractor, self).__init__()
    self.path = None
    if (type(path) == Path):
      self.path = path
      
  def getContent(self):
    if (self.path == None):
      return ""
    return self.path.getContent()
    
  def perform(self, context):
    context.log(None, "Extracting \""+self.toString(self.path)+"\"...")
    if (self.path == None):
      return False
    content = self.getContent().strip()
    if (len(content) == 0):
      return False
    if not (os.path.isfile(content)):
      return False
    path = os.path.dirname(content)
    filename = os.path.basename(content)
    index = -1
    for i in range(len(filename)):
      if (filename[i:(i+1)] == "."):
        index = i
        break
    if (index < 0):
      return False
    extension = filename[index:].lower()
    filename = filename[:index]
    if (os.path.exists(os.path.join(path, filename))):
      context.log(None, "Extracted \""+self.toString(self.path)+"\"!")
      return True
    if (extension == ".zip"):
      if not (unzip(content, os.path.join(path, filename))):
        return False
    elif ((extension == ".tgz") or (extension == ".txz") or (extension == ".tbz") or (extension.startswith(".tar"))):
      if not (untar(content, os.path.join(path, filename))):
        return False
    else:
      try:
        os.makedirs(os.path.join(path, filename))
        pyunpack.Archive(content).extractall(os.path.join(path, filename))
      except:
        logging.error(traceback.format_exc())
        index = -1
    if (index < 0):
      return False
    context.log(None, "Extracted \""+self.toString(self.path)+"\"!")
    return True
    
  def __str__(self):
    return "<"+self.toString(self.path)+">"
    
