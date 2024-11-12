
# Author: Pierce Brooks


from .object import Object
from .string import String


class Link(Object):
  def __init__(self, string = None, linkage = None, language = None):
    super(Link, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
    self.linkage = None
    if (type(linkage) == String):
      self.linkage = linkage
    self.language = None
    if (type(language) == String):
      self.language = language
      
  def getContent(self):
    if (self.string == None):
      return ""
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
