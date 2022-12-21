
# Author: Pierce Brooks


from .list import List
from .definition import Definition


class DefinitionList(List):
  def __init__(self):
    super(DefinitionList, self).__init__()
    
  def build(self, owner, variant):
    return True
        
  def addDefinition(self, definition):
    if not (isinstance(definition, Definition)):
      return False
    return super(DefinitionList, self).add(definition)
    
