
# Author: Pierce Brooks


from .object import Object


class Performer(Object):
  def __init__(self):
    super(Performer, self).__init__()
    
  def perform(self, context):
    return True
    
  def getContent(self):
    return ""
    
