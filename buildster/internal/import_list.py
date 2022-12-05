
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

from .list import List
from .build import Import

from .utilities import *

class ImportList(List):
  def __init__(self):
    super(ImportList, self).__init__()
    
  def build(self, owner, variant):
    return True

  def doImport(self, owner, variant):
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Import)):
        if not (self.content[i].doImport(owner, variant)):
          return False
    return True

  def addImport(self, add):
    if not (isinstance(add, Import)):
      return False
    return super(ImportList, self).add(add)
    
