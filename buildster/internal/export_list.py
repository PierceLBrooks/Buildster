
# Author: Pierce Brooks


from .list import List
from .build import Export


class ExportList(List):
  def __init__(self):
    super(ExportList, self).__init__()
    
  def build(self, owner, variant):
    return True

  def doExport(self, owner, variant):
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Export)):
        if not (self.content[i].doExport(owner, variant)):
          return False
    return True

  def addExport(self, add):
    if not (isinstance(add, Export)):
      return False
    return super(ExportList, self).add(add)
    
