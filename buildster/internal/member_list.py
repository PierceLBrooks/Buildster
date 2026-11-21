
# Author: Pierce Brooks


from .list import List
from .member import Member


class MemberList(List):
  def __init__(self):
    super(MemberList, self).__init__()
    
  def build(self, owner, variant):
    return True
    
  def addMember(self, member):
    if not (isinstance(member, Member)):
      return False
    return super(MemberList, self).add(member)
    
