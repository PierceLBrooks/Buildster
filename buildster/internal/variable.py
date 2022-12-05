
# Author: Pierce Brooks


from .element import Element
from .key import Key
from .value import Value


class Variable(Element):
  def __init__(self, key = None, value = None):
    super(Variable, self).__init__()
    self.key = None
    self.value = None
    if (type(key) == Key):
      self.key = key
    if (type(value) == Value):
      self.value = value
      
  def build(self, owner, variant):
    return True
    
  def getContent(self):
    return self.key.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.key)+", "+self.toString(self.value)+">"
    
