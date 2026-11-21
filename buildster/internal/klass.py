
# Author: Pierce Brooks

from .object import Object
from .label import Label
from .functor_list import FunctorList
from .namespace_list import NamespaceList
from .enumeration_list import EnumerationList
from .member_list import MemberList
from .header_list import HeaderList
from .parent_list import ParentList
#from .klass_list import KlassList


class Klass(Object):
  def __init__(self, label = None, parents = None, functors = None, namespaces = None, enumerations = None, members = None, headers = None, klasses = None):
    super(Klass, self).__init__()
    self.label = None
    if (type(label) == Label):
      self.label = label
    self.parents = None
    if (type(parents) == ParentList):
      self.parents = parents
    self.functors = None
    if (type(functors) == FunctorList):
      self.functors = functors
    self.namespaces = None
    if (type(namespaces) == NamespaceList):
      self.namespaces = namespaces
    self.enumerations = None
    if (type(enumerations) == EnumerationList):
      self.enumerations = enumerations
    self.members = None
    if (type(members) == MemberList):
      self.members = members
    self.headers = None
    if (type(headers) == HeaderList):
      self.headers = headers
    self.klasses = klasses
    #if (type(klasses) == KlassList):
      #self.klasses = klasses
    #else:
      #self.klasses = None
    
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.parents)+", "+self.toString(self.functors)+", "+self.toString(self.namespaces)+", "+self.toString(self.enumerations)+", "+self.toString(self.members)+", "+self.toString(self.headers)+", "+self.toString(self.klasses)+">"

