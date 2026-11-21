
# Author: Pierce Brooks


from .list import List
from .qualifier import Qualifier


class QualifierList(List):
  def __init__(self):
    super(QualifierList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addQualifier(self, qualifier):
    if not (isinstance(qualifier, Qualifier)):
      return False
    return super(QualifierList, self).add(qualifier)
    
