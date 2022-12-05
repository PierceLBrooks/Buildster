
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

from .url import URL
from .build import Export
from .build import Import
from .dependency import Dependency

from .utilities import *

class RemoteDependency(Dependency):
  def __init__(self, url = None):
    super(RemoteDependency, self).__init__()
    self.url = None
    if (type(url) == URL):
      self.url = url
      
  def build(self, owner, variant):
    success = super(RemoteDependency, self).build(owner, variant)
    if not (success):
      return False
    return True
    
  def doExport(self, key, value, export, variant, exceptions):
    return True
    
  def doImport(self, label, variant):
    return True
    
  def getExports(self, variant, need):
    return {}

