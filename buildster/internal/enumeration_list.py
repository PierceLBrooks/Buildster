
# Author: Pierce Brooks


from .list import List
from .enumeration import Enumeration


class EnumerationList(List):
  def __init__(self):
    super(EnumerationList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addEnumeration(self, enumeration):
    if not (isinstance(enumeration, Enumeration)):
      return False
    return super(EnumerationList, self).add(enumeration)
    
