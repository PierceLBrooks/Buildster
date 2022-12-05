
# Author: Pierce Brooks


from .object import Object
from .path import Path


class CopierSource(Object):
  def __init__(self, path = None):
    super(CopierSource, self).__init__()
    self.path = None
    if (type(path) == Path):
      self.path = path
      
  def getContent(self):
    return self.path.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.path)+">"
    
