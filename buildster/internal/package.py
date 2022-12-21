
# Author: Pierce Brooks


from .element import Element
from .string import String
from .label import Label
from .component_list import ComponentList
from .hint_list import HintList
from .variable_list import VariableList
from .export_list import ExportList


class Package(Element):
  def __init__(self, label = None, exports = None, hints = None, variables = None, components = None):
    super(Package, self).__init__()
    self.label = Label(String(""))
    if (type(label) == Label):
      self.label = label
    self.exports = None
    if (type(exports) == ExportList):
      self.exports = exports
    self.hints = None
    if (type(hints) == HintList):
      self.hints = hints
    self.variables = None
    if (type(variables) == VariableList):
      self.variables = variables
    self.components = None
    if (type(components) == ComponentList):
      self.components = components
      
  def build(self, owner, variant):
    return True
    
  def getContent(self):
    return self.label.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.exports)+", "+self.toString(self.hints)+", "+self.toString(self.variables)+", "+self.toString(self.components)+">"
    
