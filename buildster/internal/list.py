
# Author: Pierce Brooks


from .object import Object
from .element import Element


class List(Element):
  def __init__(self, content = None):
    super(List, self).__init__()
    self.content = []
    if (type(content) == list):
      self.content = content
      
  def build(self, owner, variant):
    return True
    
  def add(self, content):
    if not (content == None):
      if (type(content) == list):
        length = len(content)
        for i in range(length):
          if not (self.add(content[i])):
            return False
        return True
      elif (isinstance(content, Object)):
        self.content.append(content)
        return True
      else:
        return False
    return False
    
  def getContent(self):
    content = []
    length = len(self.content)
    for i in range(length):
      if (isinstance(self.content[i], Object)):
        content.append(self.content[i].getContent())
    return content
    
  def __len__(self):
    return len(self.content)
      
  def __str__(self):
    to = "<["
    length = len(self.content)
    for i in range(length):
      to += self.content[i].toString()
      if not (i == length-1):
        to += ", "
    to += "]>"
    return to

