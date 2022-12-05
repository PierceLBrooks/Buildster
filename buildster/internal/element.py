
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

from .internal.object import Object
from .internal.content import Content

from .internal.utilities import *

class Element(Object):
  def __init__(self):
    super(Element, self).__init__()
    self.parent = None
    
  def build(self, owner, variant):
    return True
    
  def distribute(self, owner, distribution, variant):
    return True
    
  def move(self, source, destination):
    if (os.path.exists(destination)):
      if (os.path.getmtime(destination) >= os.path.getmtime(source)):
        return True
      os.unlink(destination)
    if not (move(source, destination)):
      return False
    return True
    
  def getParent(self):
    return self.parent
    
  def getContent(self):
    return ""
    
