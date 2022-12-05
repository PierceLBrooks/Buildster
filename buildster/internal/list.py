
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
from .internal.element import Element
from .internal.string import String
from .internal.content import Content

from .internal.utilities import *

class List(Element):
  def __init__(self, content = None):
    super(List, self).__init__()
    self.content = []
    if (type(content) == list):
      self.content = content
      
  def build(self, owner, variant):
    return True
    
  def add(self, content):
    if not (content == None):
      if (type(content) == list):
        length = len(content)
        for i in range(length):
          if not (self.add(content[i])):
            return False
        return True
      elif (isinstance(content, Object)):
        self.content.append(content)
        return True
      else:
        return False
    return False
    
  def getContent(self):
    content = []
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Object)):
        content.append(self.content[i].getContent())
    return content
    
  def __len__(self):
    return len(self.content)
      
  def __str__(self):
    to = "<["
    length = len(self.content)
    for i in range(length):
      to += self.content[i].toString()
      if not (i == length-1):
        to += ", "
    to += "]>"
    return to

