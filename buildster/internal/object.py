
# Author: Pierce Brooks



class Object(object):
  def __init__(self):
    self.node = None
    self.parent = None
    
  def getContent(self):
    return ""
    
  def getParent(self):
    return self.parent
    
  def toString(self, *arguments):
    if (len(arguments) == 0):
      return "("+self.__class__.__name__+")"+str(self)
    other = arguments[0]
    if (other == None):
      return "/NULL/"
    if (type(other) == str):
      return str(other)
    if (type(other) == list):
      length = len(other)
      string = "["
      for i in range(length):
        string += self.toString(other[i])
        if not (i == length-1):
          string += ", "
      string += "]"
      return string
    if not (isinstance(other, Object)):
      return "/INVALID/"
    return other.toString()
    
