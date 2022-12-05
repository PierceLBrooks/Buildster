
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

from .internal.list import List
from .internal.definition import Definition

from .internal.utilities import *

class DefinitionList(List):
  def __init__(self):
    super(DefinitionList, self).__init__()
    
  def build(self, owner, variant):
    return True
        
  def addDefinition(self, definition):
    if not (isinstance(definition, Definition)):
      return False
    return super(DefinitionList, self).add(definition)
    
