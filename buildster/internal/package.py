
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
from .internal.component import Component
from .internal.component_list import ComponentList
from .internal.hint import Hint
from .internal.hint_list import HintList
from .internal.variable import Variable
from .internal.variable_list import VariableList
from .internal.exporter import Export
from .internal.export_list import ExportList

from .internal.utilities import *

class Package(Element):
  def __init__(self, label = None, exports = None, hints = None, variables = None, components = None):
    super(Package, self).__init__()
    self.label = Label(String(""))
    if (type(label) == Label):
      self.label = label
    self.exports = None
    if (type(exports) == ExportList):
      self.exports = exports
    self.hints = None
    if (type(hints) == HintList):
      self.hints = hints
    self.variables = None
    if (type(variables) == VariableList):
      self.variables = variables
    self.components = None
    if (type(components) == ComponentList):
      self.components = components
      
  def build(self, owner, variant):
    return True
    
  def getContent(self):
    return self.label.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.exports)+", "+self.toString(self.hints)+", "+self.toString(self.variables)+", "+self.toString(self.components)+">"
    
