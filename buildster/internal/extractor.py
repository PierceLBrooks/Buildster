
# Author: Pierce Brooks

import os
import logging
import pyunpack
import traceback

from .performer import Performer
from .path import Path

from .utilities import *

class Extractor(Performer):
  def __init__(self, path = None):
    super(Extractor, self).__init__()
    self.path = None
    if (type(path) == Path):
      self.path = path
      
  def getContent(self):
    if (self.path == None):
      return ""
    return self.path.getContent()
    
  def perform(self, context):
    context.log(None, "Extracting \""+self.toString(self.path)+"\"...")
    if (self.path == None):
      return False
    content = self.getContent().strip()
    if (len(content) == 0):
      return False
    if not (os.path.isfile(content)):
      return False
    path = os.path.dirname(content)
    filename = os.path.basename(content)
    index = -1
    for i in range(len(filename)):
      if (filename[i:(i+1)] == "."):
        index = i
        break
    if (index < 0):
      return False
    extension = filename[index:].lower()
    filename = filename[:index]
    if (os.path.exists(os.path.join(path, filename))):
      context.log(None, "Extracted \""+self.toString(self.path)+"\"!")
      return True
    if (extension == ".zip"):
      if not (unzip(content, os.path.join(path, filename))):
        return False
    elif ((extension == ".tgz") or (extension == ".txz") or (extension == ".tbz") or (extension.startswith(".tar"))):
      if not (untar(content, os.path.join(path, filename))):
        return False
    else:
      try:
        os.makedirs(os.path.join(path, filename))
        pyunpack.Archive(content).extractall(os.path.join(path, filename))
      except:
        logging.error(traceback.format_exc())
        index = -1
    if (index < 0):
      return False
    context.log(None, "Extracted \""+self.toString(self.path)+"\"!")
    return True
    
  def __str__(self):
    return "<"+self.toString(self.path)+">"
    
