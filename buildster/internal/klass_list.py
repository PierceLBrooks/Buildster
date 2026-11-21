
# Author: Pierce Brooks


from .list import List
from .klass import Klass


class KlassList(List):
  def __init__(self):
    super(KlassList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addKlass(self, klass):
    if not (isinstance(klass, Klass)):
      return False
    return super(KlassList, self).add(klass)
    
