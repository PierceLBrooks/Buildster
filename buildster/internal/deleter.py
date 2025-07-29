
# Author: Pierce Brooks

import os
import shutil
import pathlib

from .performer import Performer
from .path import Path


class Deleter(Performer):
  def __init__(self, path = None):
    super(Deleter, self).__init__()
    self.path = None
    if (type(path) == Path):
      self.path = path
      
  def getContent(self):
    if (self.path == None):
      return ""
    return self.path.getContent()
    
  def perform(self, context):
    context.log(None, "Deleting \""+self.toString(self.path)+"\"...")
    if (self.path == None):
      return False
    content = self.getContent().strip()
    if (len(content) == 0):
      return False
    if not (os.path.exists(content)):
      context.log(None, "Deleted \""+self.toString(self.path)+"\"!")
      return True
    try:
      if (os.path.isfile(content)):
        pathlib.Path.unlink(content)
      else:
        shutil.rmtree(content)
    except:
      pass
    context.log(None, "Deleted \""+self.toString(self.path)+"\"!")
    return True
    
  def __str__(self):
    return "<"+self.toString(self.path)+">"
    
