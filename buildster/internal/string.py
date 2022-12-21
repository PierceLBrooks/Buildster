
# Author: Pierce Brooks


from .object import Object


class String(Object):
  def __init__(self, content = None):
    super(String, self).__init__()
    self.content = ""
    if (type(content) == str):
      self.content = content
      
  def getContent(self):
    return self.content
      
  def __str__(self):
    return "<\""+self.content+"\">"
    
