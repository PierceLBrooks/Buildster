
# Author: Pierce Brooks


from .object import Object
from .string import String
from .key import Key
from .value import Value


class Definition(Object):
  def __init__(self, key = None, value = None):
    super(Definition, self).__init__()
    self.key = Key(String(""))
    if (type(key) == Key):
      self.key = key
    self.value = Value(String(""))
    if (type(value) == Value):
      self.value = value
      
  def getContent(self):
    return self.key.getContent()+"="+self.value.getContent()
      
  def __str__(self):
    return "<"+self.toString(self.key)+", "+self.toString(self.value)+">"
    
