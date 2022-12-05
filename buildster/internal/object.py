
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

from .internal.utilities import *

class Object(object):
  def __init__(self):
    self.node = None
    
  def getContent(self):
    return ""
    
  def toString(self, *arguments):
    if (len(arguments) == 0):
      return "("+self.__class__.__name__+")"+str(self)
    other = arguments[0]
    if (other == None):
      return "/NULL/"
    if (type(other) == str):
      return str(other)
    if (type(other) == list):
      length = len(other)
      string = "["
      for i in range(length):
        string += self.toString(other[i])
        if not (i == length-1):
          string += ", "
      string += "]"
      return string
    if not (isinstance(other, Object)):
      return "/INVALID/"
    return other.toString()
    
