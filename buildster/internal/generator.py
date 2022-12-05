
# Author: Pierce Brooks


from .object import Object
from .string import String
from .architecture import Architecture


class Generator(Object):
  def __init__(self, string = None, architecture = None):
    super(Generator, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
    self.architecture = None
    if (type(architecture) == Architecture):
      self.architecture = architecture
      
  def getContent(self):
    if (self.string == None):
      return ""
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+", "+self.toString(self.architecture)+">"

