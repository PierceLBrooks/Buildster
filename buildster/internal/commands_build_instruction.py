
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
from .internal.build_instruction import BuildInstruction
from .internal.command_build_instruction import CommandBuildInstruction

from .internal.utilities import *

class CommandsBuildInstruction(BuildInstruction):
  def __init__(self, arguments = None, generator = None, source = None):
    super(CommandsBuildInstruction, self).__init__(arguments)
    self.commands = []
      
  def build(self, owner, path, subpath, installation, imports, variant):
    length = len(self.commands)
    for i in range(length):
      if ("CommandBuildInstruction" in str(type(self.commands[i]))):
        if not (self.commands[i].build(owner, path, subpath, installation, imports, variant)):
          return False
      else:
        owner.getContext().log(self.node, str(type(self.commands[i])))
        return False
    return True
    
  def install(self, owner, path, subpath, installation, variant):
    return True
    
  def __str__(self):
    return "<"+self.toString(self.commands)+">"
    
