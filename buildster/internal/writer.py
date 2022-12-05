
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

from .internal.performer import Performer
from .internal.string import String
from .internal.destination import Destination
from .internal.content import Content

from .internal.utilities import *

class Writer(Performer):
  def __init__(self, destination = None, content = None):
    super(Writer, self).__init__()
    self.destination = None
    self.content = None
    if (type(destination) == Destination):
      self.destination = destination
    if (type(content) == Content):
      self.content = content
      
  def getContent(self):
    return self.destination.getContent()
    
  def perform(self, context):
    context.log(None, "Writing \""+self.toString(self.destination)+"\"...")
    if ((self.destination == None) or (self.content == None)):
      return False
    content = self.getContent().strip()
    if (len(content) == 0):
      return False
    descriptor = open(content, "w")
    if not (write(descriptor, self.content.getContent())):
      return False
    descriptor.close()
    context.log(None, "Wrote \""+self.toString(self.destination)+"\"!")
    return True
    
  def __str__(self):
    return "<"+self.toString(self.destination)+", "+self.toString(self.content)+">"

