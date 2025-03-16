
# Author: Pierce Brooks

import os

from .object import Object

from .utilities import *

class Element(Object):
  def __init__(self):
    super(Element, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def distribute(self, owner, distribution, variant):
    return True
    
  def move(self, source, destination):
    if (os.path.exists(destination)):
      if (os.path.getmtime(destination) >= os.path.getmtime(source)):
        return True
      os.unlink(destination)
    if not (move(source, destination)):
      return False
    return True
    
  def getContent(self):
    return ""
    
