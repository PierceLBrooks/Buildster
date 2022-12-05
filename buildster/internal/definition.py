
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
from .string import String
from .key import Key
from .value import Value
from .content import Content

from .utilities import *

class Definition(Object):
  def __init__(self, key = None, value = None):
    super(Definition, self).__init__()
    self.key = Key(String(""))
    if (type(key) == Key):
      self.key = key
    self.value = Value(String(""))
    if (type(value) == Value):
      self.value = value
      
  def getContent(self):
    return self.key.getContent()+"="+self.value.getContent()
      
  def __str__(self):
    return "<"+self.toString(self.key)+", "+self.toString(self.value)+">"
    
