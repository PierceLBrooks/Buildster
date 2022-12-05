
# Author: Pierce Brooks


from .list import List
from .module import Module


class ModuleList(List):
  def __init__(self):
    super(ModuleList, self).__init__()
    
  def build(self, owner, variant):
    return True
        
  def addModule(self, module):
    if not (isinstance(module, Module)):
      return False
    return super(ModuleList, self).add(module)
    
