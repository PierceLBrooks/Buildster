
# Author: Pierce Brooks


from .element import Element
from .string import String
from .label import Label
from .export_list import ExportList


class Module(Element):
  def __init__(self, label = None, exports = None):
    super(Module, self).__init__()
    self.label = Label(String(""))
    if (type(label) == Label):
      self.label = label
    self.exports = None
    if (type(exports) == ExportList):
      self.exports = exports
      
  def build(self, owner, variant):
    return True
    
  def getContent(self):
    return self.label.getContent()
    
  def __str__(self):
    return "<"+self.toString(self.label)+", "+self.toString(self.exports)+">"
    
