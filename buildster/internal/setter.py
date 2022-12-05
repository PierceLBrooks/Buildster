
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

from .performer import Performer
from .build import Build
from .string import String
from .key import Key
from .value import Value
from .content import Content
from .build_instruction import BuildInstruction

from .utilities import *

class Setter(BuildInstruction, Performer):
  def __init__(self, key = None, value = None):
    super(Setter, self).__init__()
    self.key = None
    if (type(key) == Key):
      self.key = key
    self.value = None
    if (type(value) == Value):
      self.value = value
      
  def build(self, owner, path, subpath, installation, imports, variant):
    return self.perform(owner.getContext())
    
  def perform(self, context):
    if not ((self.key == None) or (self.value == None)):
      context.data[self.key.getContent()] = self.value.getContent()
      context.environment[self.key.getContent()] = self.value.getContent()
      context.log(self.node, "<\""+self.key.getContent()+"\" -> \""+self.value.getContent()+"\">")
      return True
    return False
    
  def install(self, owner, path, subpath, installation):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.key)+", "+self.toString(self.value)+">"

