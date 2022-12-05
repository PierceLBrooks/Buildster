
# Author: Pierce Brooks


from .object import Object
from .string import String


class Label(Object):
  def __init__(self, string = None):
    super(Label, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def getContent(self):
    if (self.string == None):
      return ""
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
