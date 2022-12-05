
# Author: Pierce Brooks


from .list import List
from .exception import Exception


class ExceptionList(List):
  def __init__(self):
    super(ExceptionList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addException(self, exception):
    if not (isinstance(exception, Exception)):
      return False
    return super(ExceptionList, self).add(exception)
    
