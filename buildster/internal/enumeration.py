
# Author: Pierce Brooks

from .object import Object
from .label import Label
from .member_list import MemberList


class Enumeration(Object):
  def __init__(self, label = None, members = None):
    super(Enumeration, self).__init__()
    self.label = None
    if (type(label) == Label):
      self.label = label
    self.members = None
    if (type(members) == MemberList):
      self.members = members
    
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.members)+">"

