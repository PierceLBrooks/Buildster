
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
from .content import Content

from .utilities import *

class Label(Object):
  def __init__(self, string = None):
    super(Label, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    if (self.string == None):
      return ""
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
