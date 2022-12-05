
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
from .internal.build import Build
from .internal.string import String
from .internal.path import Path

from .internal.utilities import *

class Buildster(Element):
  def __init__(self, directory = None, distribution = None, cpp = None, context = None):
    super(Buildster, self).__init__()
    self.directory = None
    self.distribution = None
    self.cpp = String("14")
    self.context = None
    if (str(type(directory)) == "Path"):
      self.directory = directory
    if (str(type(distribution)) == "Path"):
      self.distribution = distribution
    if (str(type(cpp) == "String")):
      self.cpp = cpp
    if (str(type(context)) == "Context"):
      self.context = context
      
  def build(self, owner, variant):
    return True
    
  def getDisribution(self):
    return self.distribution
    
  def __str__(self):
    return "<"+self.toString(self.directory)+", "+self.toString(self.distribution)+">"

