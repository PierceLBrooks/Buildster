
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

from .internal.build import Build
from .internal.string import String
from .internal.content import Content
from .internal.path import Path
from .internal.work import Work
from .internal.build_instruction import BuildInstruction
from .internal.commands_build_instruction import CommandsBuildInstruction

from .internal.utilities import *

class ShellBuildInstruction(BuildInstruction):
  def __init__(self, commands = None, work = None):
    super(ShellBuildInstruction, self).__init__()
    self.commands = None
    self.work = None
      
  def build(self, owner, path, subpath, installation, imports, variant):
    if (self.commands == None):
      return False
    if not ("CommandsBuildInstruction" in str(type(self.commands))):
      return False
    if (self.work == None):
      return False
    if not ("Work" in str(type(self.work))):
      return False
    owner.getContext().work = self.work.getContent()
    if not (self.commands.build(owner, self.getPath(path, subpath), self.work.getContent(), installation, imports, variant)):
      return False
    owner.getContext().work = None
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.commands)+">"

