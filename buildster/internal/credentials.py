
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

from .object import Object
from .string import String
from .username import Username
from .password import Password

from .utilities import *

class Credentials(Object):
  def __init__(self, username = None, password = None):
    super(Credentials, self).__init__()
    self.username = None
    self.password = None
    if (type(username) == Username):
      self.username = username
    if (type(password) == Password):
      self.password = password
    
  def __str__(self):
    return "<"+self.toString(self.username)+", "+self.toString(self.password)+">"
    
