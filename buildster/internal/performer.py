
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
from .internal.content import Content

from .internal.utilities import *

class Performer(Object):
  def __init__(self):
    super(Performer, self).__init__()
    
  def perform(self, context):
    return True
    
  def getContent(self):
    return ""
    
