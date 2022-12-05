
# Author: Pierce Brooks


from .object import Object
from .string import String


class CopierRename(Object):
  def __init__(self, name = None):
    super(CopierRename, self).__init__()
    self.name = None
    if (type(name) == String):
      self.name = name
      
  def getContent(self):
    return self.name.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.name)+">"
    
