
# Author: Pierce Brooks


from .list import List
from .build import Import


class ImportList(List):
  def __init__(self):
    super(ImportList, self).__init__()
    
  def build(self, owner, variant):
    return True

  def doImport(self, owner, variant):
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Import)):
        if not (self.content[i].doImport(owner, variant)):
          return False
    return True

  def addImport(self, add):
    if not (isinstance(add, Import)):
      return False
    return super(ImportList, self).add(add)
    
