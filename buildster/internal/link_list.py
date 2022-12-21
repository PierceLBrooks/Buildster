
# Author: Pierce Brooks


from .list import List
from .link import Link


class LinkList(List):
  def __init__(self):
    super(LinkList, self).__init__()
    
  def build(self, owner, variant):
    return True
        
  def addLink(self, link):
    if not (isinstance(link, Link)):
      return False
    return super(LinkList, self).add(link)
    
