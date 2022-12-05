
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
from .internal.content import Content
from .internal.label import Label

from .internal.utilities import *

class Import(Object):
  def __init__(self, label = None):
    super(Import, self).__init__()
    self.label = None
    if (type(label) == Label):
      self.label = label
      
  def getContent(self):
    return self.label.getContent()
    
  def doImport(self, owner, variant):
    if not (isinstance(owner, Build)):
      return False
    owner.addImport(self, variant)
    return True
    
  def __str__(self):
    return "<"+self.toString(self.label)+">"
    
