
# Author: Pierce Brooks


from .element import Element
from .string import String


class Hint(Element):
  def __init__(self, string = None):
    super(Hint, self).__init__()
    self.string = None
    if (type(string) == String):
      self.string = string
      
  def build(self, owner, variant):
    return True
    
  def getContent(self):
    if (self.string == None):
      return ""
    return self.string.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.string)+">"
    
