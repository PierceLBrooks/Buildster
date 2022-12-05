
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

from .internal.element import Element
from .internal.string import String
from .internal.list import List
from .internal.content import Content
from .internal.label import Label
from .internal.exporter import Export
from .internal.export_list import ExportList

from .internal.utilities import *

class Module(Element):
  def __init__(self, label = None, exports = None):
    super(Module, self).__init__()
    self.label = Label(String(""))
    if (type(label) == Label):
      self.label = label
    self.exports = None
    if (type(exports) == ExportList):
      self.exports = exports
      
  def build(self, owner, variant):
    return True
    
  def getContent(self):
    return self.label.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.exports)+">"
    
