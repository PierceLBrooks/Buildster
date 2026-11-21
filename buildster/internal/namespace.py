
# Author: Pierce Brooks


from .element import Element
from .string import String
from .enumeration_list import EnumerationList


class Namespace(Element):
  def __init__(self, string = None, enumerations = None):
    super(Namespace, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
    self.enumerations = None
    if (type(enumerations) == EnumerationList):
      self.enumerations = enumerations
      
  def build(self, owner, variant):
    return True
    
  def getContent(self):
    if (self.string == None):
      return ""
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
