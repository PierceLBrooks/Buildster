
# Author: Pierce Brooks


from .element import Element
from .string import String


class Buildster(Element):
  def __init__(self, directory = None, distribution = None, cpp = None, sudo = None, context = None):
    super(Buildster, self).__init__()
    self.directory = None
    self.distribution = None
    self.cpp = String("14")
    self.sudo = String("true")
    self.context = None
    if ("Path" in str(type(directory))):
      self.directory = directory
    if ("Path" in str(type(distribution))):
      self.distribution = distribution
    if ("String" in str(type(cpp))):
      self.cpp = cpp
    if ("String" in str(type(sudo))):
      self.sudo = sudo
    if ("Context" in str(type(context))):
      self.context = context
      
  def build(self, owner, variant):
    return True
    
  def getDisribution(self):
    return self.distribution
    
  def __str__(self):
    return "<"+self.toString(self.directory)+", "+self.toString(self.distribution)+">"
