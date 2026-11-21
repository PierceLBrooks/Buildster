
# Author: Pierce Brooks


from .list import List
from .header import Header


class HeaderList(List):
  def __init__(self):
    super(HeaderList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addHeader(self, header):
    if not (isinstance(header, Header)):
      return False
    return super(HeaderList, self).add(header)
    
