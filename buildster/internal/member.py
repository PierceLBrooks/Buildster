
# Author: Pierce Brooks


from .object import Object
from .key import Key
from .value import Value
from .qualifier_list import QualifierList


class Member(Object):
  def __init__(self, key = None, value = None, qualifiers = None):
    super(Member, self).__init__()
    self.key = None
    self.value = None
    self.qualifiers = None
    if (type(key) == Key):
      self.key = key
    if (type(value) == Value):
      self.value = value
    if (type(qualifiers) == QualifierList):
      self.qualifiers = qualifiers
      
  def __str__(self):
    return "<"+self.toString(self.key)+", "+self.toString(self.value)+", "+self.toString(self.qualifiers)+">"
    
