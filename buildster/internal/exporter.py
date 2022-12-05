
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
from .internal.build import Build
from .internal.string import String
from .internal.key import Key
from .internal.value import Value
from .internal.content import Content
from .internal.label import Label

from .internal.utilities import *

class Export(Object):
  def __init__(self, key = None, value = None, export = None, exceptions = None):
    super(Export, self).__init__()
    self.key = None
    if (type(key) == Key):
      self.key = key
    self.value = None
    if (type(value) == Value):
      self.value = value
    self.export = None
    if (type(export) == String):
      self.export = export
    self.exceptions = None
    if (type(exceptions) == String):
      self.exceptions = exceptions
      
  def doExport(self, owner, variant):
    exceptions = None
    if not (self.exceptions == None):
      exceptions = self.exceptions.getContent()
    if not (isinstance(owner, Build)):
      return False
    if not (exceptions == None):
      if (owner.getLabel() in exceptions):
        return True
    owner.addExport(self, variant, exceptions)
    return True
      
  def __str__(self):
    return "<"+self.toString(self.key)+", "+self.toString(self.value)+", "+self.toString(self.export)+">"
    
