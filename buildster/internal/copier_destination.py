
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
from .internal.string import String
from .internal.destination import Destination
from .internal.content import Content
from .internal.copier import Copier
from .internal.path import Path

from .internal.utilities import *

class CopierDestination(Object):
  def __init__(self, path = None):
    super(CopierDestination, self).__init__()
    self.path = None
    if (type(path) == Path):
      self.path = path
      
  def getContent(self):
    return self.path.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.path)+">"
    
