
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
from .string import String
from .content import Content
from .url import URL

from .utilities import *

class Downloader(Performer):
  def __init__(self, url = None):
    super(Downloader, self).__init__()
    self.url = None
    if (type(url) == URL):
      self.url = url
      
  def getContent(self):
    if (self.url == None):
      return ""
    return self.url.getContent()
    
  def perform(self, context):
    context.log(None, "Downloading \""+self.toString(self.url)+"\"...")
    if (self.url == None):
      return False
    content = self.getContent().strip()
    if (len(content) == 0):
      return False
    if not (retrieve(context, content)):
       return False
    context.log(None, "Downloaded \""+self.toString(self.url)+"\"!")
    return True
    
  def __str__(self):
    return "<"+self.toString(self.url)+">"
    
