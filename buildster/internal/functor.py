
# Author: Pierce Brooks


from .object import Object
from .label import Label
from .qualifier_list import QualifierList
from .argument_list import ArgumentList
from .returner import Returner
from .body import Body

from .utilities import *


class Functor(Object):
  def __init__(self, label = None, qualifiers = None, arguments = None, returner = None, body = None):
    super(Functor, self).__init__()
    self.label = None
    self.qualifiers = None
    self.arguments = None
    self.returner = None
    self.body = None
    if (type(label) == Label):
      self.label = label
    if (type(qualifiers) == QualifierList):
      self.qualifiers = qualifiers
    if (type(arguments) == ArgumentList):
      self.arguments = arguments
    if (type(returner) == Returner):
      self.returner = returner
    if (type(body) == Body):
      self.body = body
      
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.qualifiers)+", "+self.toString(self.arguments)+", "+self.toString(self.returner)+", "+textualize(str(self.toString(self.body)))+">"
    
