
# Author: Pierce Brooks

import os
import copy
import platform
import traceback
from datetime import datetime

from .element import Element

from .utilities import *

class Context(Element):
  def __init__(self, data, variant, debug = True):
    super(Context, self).__init__()
    

    self.variant = variant
    
    
    self.exclusions = []
    
    self.exclusions.append("o")
    self.exclusions.append("obj")
    self.exclusions.append("lo")
    self.exclusions.append("la")
    self.exclusions.append("d")
    self.exclusions.append("in")
    self.exclusions.append("ac")
    self.exclusions.append("cmake")
    self.exclusions.append("txt")
    self.exclusions.append("log")
    self.exclusions.append("bin")
    self.exclusions.append("make")
    self.exclusions.append("internal")

    self.extensions = []
    
    self.extensions.append("exe")
    
    self.headers = []
    
    self.headers.append("h")
    self.headers.append("hh")
    self.headers.append("hpp")
    self.headers.append("hxx")
    self.headers.append("h++")
    self.headers.append("i")
    self.headers.append("ii")
    self.headers.append("ipp")
    self.headers.append("ixx")
    self.headers.append("i++")
    self.headers.append("inl")
    self.headers.append("inc")
    self.headers.append("t")
    self.headers.append("tt")
    self.headers.append("tpp")
    self.headers.append("txx")
    self.headers.append("t++")
    self.headers.append("tpl")
    
    self.sources = []
    
    self.sources.append("c")
    self.sources.append("cc")
    self.sources.append("cpp")
    self.sources.append("cxx")
    self.sources.append("c++")
    self.sources.append("cs")
    self.sources.append("m")
    self.sources.append("objc")
    self.sources.append("swift")
    
    self.scripts = []
    
    self.scripts.append("java")
    self.scripts.append("py")
    self.scripts.append("rb")
    self.scripts.append("sh")
    self.scripts.append("bat")
    
    self.libraries = []
    
    self.libraries.append("dll")
    self.libraries.append("a")
    self.libraries.append("lib")
    self.libraries.append("dylib")
    self.libraries.append("so")
    self.libraries.append("jar")
    
    self.statics = []
    
    self.statics.append("a")
    self.statics.append("lib")
    
    self.shares = []
    
    self.shares.append("dll")
    self.shares.append("dylib")
    self.shares.append("so")
    
    self.extensions = self.headers+self.sources+self.scripts+self.libraries+self.extensions
    
    self.substitutes = []
    
    self.substitutes.append("distribution")
    self.substitutes.append("origin")
    self.substitutes.append("install")
    self.substitutes.append("python")
    self.substitutes.append("cores")
    self.substitutes.append("home")
    self.substitutes.append("execute")
    self.substitutes.append("encode")
    self.substitutes.append("decode")
    self.substitutes.append("escape")
    self.substitutes.append("unescape")
    self.substitutes.append("base")
    self.substitutes.append("directory")
    self.substitutes.append("lower")
    self.substitutes.append("upper")
    self.substitutes.append("exists")
    
    self.conditionals = []
    
    self.conditionals.append("if")
    self.conditionals.append("if_check")
    self.conditionals.append("if_exists")
    self.conditionals.append("switch")
    self.conditionals.append("else")
    self.conditionals.append("case")
    self.conditionals.append("default")
    
    self.nonconditionals = []
    
    self.nonconditionals.append("log")
    self.nonconditionals.append("read")
    self.nonconditionals.append("json")
    self.nonconditionals.append("data")
    self.nonconditionals.append("case")
    self.nonconditionals.append("default")
    self.nonconditionals.append("search")
    self.nonconditionals.append("set")
    for substitute in self.substitutes:
      if not (substitute in self.nonconditionals):
        self.nonconditionals.append(substitute)
    
    self.processes = []
    
    self.processes.append("message")
    self.processes.append("quit")
    
    self.any = "any"
    
    
    nodeTags = []
    
    nodeTags.append("case")
    nodeTags.append("default")
    nodeTags.append("else")
    nodeTags.append("data")
    nodeTags.append("buildster")
    nodeTags.append("project")
    nodeTags.append("dependencies")
    nodeTags.append("dependency")
    nodeTags.append("local")
    nodeTags.append("remote")
    nodeTags.append("path")
    nodeTags.append("subpath")
    nodeTags.append("git_repo")
    nodeTags.append("wget")
    nodeTags.append("url")
    nodeTags.append("branch")
    nodeTags.append("credentials")
    nodeTags.append("username")
    nodeTags.append("password")
    nodeTags.append("targets")
    nodeTags.append("target")
    nodeTags.append("executable")
    nodeTags.append("library")
    nodeTags.append("label")
    nodeTags.append("definitions")
    nodeTags.append("definition")
    nodeTags.append("key")
    nodeTags.append("value")
    nodeTags.append("links")
    nodeTags.append("link")
    nodeTags.append("build")
    nodeTags.append("arguments")
    nodeTags.append("argument")
    nodeTags.append("natives")
    nodeTags.append("native")
    nodeTags.append("cmake")
    nodeTags.append("generator")
    nodeTags.append("source")
    nodeTags.append("exports")
    nodeTags.append("export")
    nodeTags.append("imports")
    nodeTags.append("import")
    nodeTags.append("install")
    nodeTags.append("origin")
    nodeTags.append("distribution")
    nodeTags.append("root")
    nodeTags.append("work")
    nodeTags.append("shells")
    nodeTags.append("shell")
    nodeTags.append("commands")
    nodeTags.append("command")
    nodeTags.append("write")
    nodeTags.append("extract")
    nodeTags.append("download")
    nodeTags.append("copy")
    nodeTags.append("rename")
    nodeTags.append("delete")
    nodeTags.append("from")
    nodeTags.append("to")
    nodeTags.append("destination")
    nodeTags.append("content")
    nodeTags.append("search")
    nodeTags.append("term")
    nodeTags.append("set")
    nodeTags.append("pre")
    nodeTags.append("post")
    nodeTags.append("variables")
    nodeTags.append("variable")
    nodeTags.append("packages")
    nodeTags.append("package")
    nodeTags.append("modules")
    nodeTags.append("module")
    nodeTags.append("components")
    nodeTags.append("component")
    nodeTags.append("hints")
    nodeTags.append("hint")
    nodeTags.append("exceptions")
    nodeTags.append("exception")
    nodeTags.append("python")
    nodeTags.append("cores")
    nodeTags.append("home")
    nodeTags.append("execute")
    nodeTags.append("encode")
    nodeTags.append("decode")
    nodeTags.append("escape")
    nodeTags.append("unescape")
    nodeTags.append("lower")
    nodeTags.append("upper")
    nodeTags.append("base")
    nodeTags.append("directory")
    for conditional in self.conditionals:
      if not (conditional in nodeTags):
        nodeTags.append(conditional)
    for nonconditional in self.nonconditionals:
      if not (nonconditional in nodeTags):
        nodeTags.append(nonconditional)
    for process in self.processes:
      if not (process in nodeTags):
        nodeTags.append(process)
    
    nodeParents = {}
    nodeAttributes = {}
    
    for i in range(len(nodeTags)):
      tag = nodeTags[i]
      parents = []
      attributes = []
      if not (tag == "buildster"):
        for conditional in self.conditionals:
          parents.append(conditional)
        for process in self.processes:
          parents.append(process)
      nodeParents[tag] = parents
      nodeAttributes[tag] = attributes
    
    nodeParents["base"].append(self.any)
    nodeParents["directory"].append(self.any)
    nodeParents["lower"].append(self.any)
    nodeParents["upper"].append(self.any)
    nodeParents["python"].append(self.any)
    nodeParents["cores"].append(self.any)
    nodeParents["home"].append(self.any)
    nodeParents["execute"].append(self.any)
    nodeParents["encode"].append(self.any)
    nodeParents["decode"].append(self.any)
    nodeParents["escape"].append(self.any)
    nodeParents["unescape"].append(self.any)
    nodeParents["set"].append(self.any)
    nodeParents["search"].append(self.any)
    nodeParents["distribution"].append(self.any)
    nodeParents["origin"].append(self.any)
    nodeParents["install"].append(self.any)
    nodeParents["message"].append(self.any)
    nodeParents["quit"].append(self.any)
    nodeParents["data"].append(self.any)
    nodeParents["json"].append(self.any)
    nodeParents["read"].append(self.any)
    nodeParents["log"].append(self.any)
    nodeParents["if"].append(self.any)
    nodeParents["if_check"].append(self.any)
    nodeParents["if_exists"].append(self.any)
    nodeParents["switch"].append(self.any)
    nodeParents["case"].append("switch")
    nodeParents["else"].append("if")
    nodeParents["else"].append("if_check")
    nodeParents["else"].append("if_exists")
    #nodeParents["buildster"].append("")
    nodeParents["project"].append("buildster")
    nodeParents["dependencies"].append("project")
    nodeParents["dependency"].append("dependencies")
    nodeParents["remote"].append("dependency")
    nodeParents["local"].append("dependency")
    nodeParents["subpath"].append("dependency")
    nodeParents["subpath"].append("target")
    nodeParents["path"].append("local")
    nodeParents["git_repo"].append("remote")
    nodeParents["wget"].append("remote")
    nodeParents["url"].append("remote")
    nodeParents["branch"].append("git_repo")
    nodeParents["credentials"].append("git_repo")
    nodeParents["username"].append("credentials")
    nodeParents["password"].append("credentials")
    nodeParents["targets"].append("project")
    nodeParents["target"].append("targets")
    nodeParents["label"].append("dependency")
    nodeParents["label"].append("target")
    nodeParents["label"].append("package")
    nodeParents["label"].append("module")
    nodeParents["definitions"].append("target")
    nodeParents["definition"].append("definitions")
    nodeParents["key"].append("variable")
    nodeParents["value"].append("variable")
    nodeParents["key"].append("definition")
    nodeParents["value"].append("definition")
    nodeParents["key"].append("export")
    nodeParents["value"].append("export")
    nodeParents["key"].append("set")
    nodeParents["value"].append("set")
    nodeParents["links"].append("target")
    nodeParents["link"].append("links")
    nodeParents["build"].append("pre")
    nodeParents["build"].append("post")
    nodeParents["build"].append("dependency")
    nodeParents["arguments"].append("build")
    nodeParents["arguments"].append("target")
    nodeParents["argument"].append("arguments")
    nodeParents["natives"].append("cmake")
    nodeParents["natives"].append("target")
    nodeParents["native"].append("natives")
    nodeParents["cmake"].append("build")
    nodeParents["generator"].append("cmake")
    nodeParents["generator"].append("target")
    nodeParents["source"].append("cmake")
    nodeParents["exports"].append("module")
    nodeParents["exports"].append("package")
    nodeParents["exports"].append("dependency")
    nodeParents["exports"].append("target")
    nodeParents["export"].append("exports")
    nodeParents["imports"].append("dependency")
    nodeParents["imports"].append("target")
    nodeParents["import"].append("imports")
    nodeParents["root"].append("search")
    nodeParents["term"].append("search")
    nodeParents["work"].append("shell")
    nodeParents["shells"].append("pre")
    nodeParents["shells"].append("post")
    nodeParents["shells"].append("build")
    nodeParents["shell"].append("shells")
    nodeParents["commands"].append("shell")
    nodeParents["command"].append("commands")
    nodeParents["extract"].append("command")
    nodeParents["download"].append("command")
    nodeParents["copy"].append("command")
    nodeParents["delete"].append("command")
    nodeParents["write"].append("command")
    nodeParents["rename"].append("copy")
    nodeParents["from"].append("copy")
    nodeParents["to"].append("copy")
    nodeParents["destination"].append("write")
    nodeParents["content"].append("write")
    nodeParents["pre"].append("project")
    nodeParents["post"].append("project")
    nodeParents["pre"].append("build")
    nodeParents["post"].append("build")
    nodeParents["pre"].append("target")
    nodeParents["post"].append("target")
    nodeParents["exceptions"].append("target")
    nodeParents["exception"].append("exceptions")
    nodeParents["variables"].append("package")
    nodeParents["variable"].append("variables")
    nodeParents["packages"].append("target")
    nodeParents["package"].append("packages")
    nodeParents["modules"].append("target")
    nodeParents["module"].append("modules")
    nodeParents["hints"].append("package")
    nodeParents["hint"].append("hints")
    nodeParents["components"].append("package")
    nodeParents["component"].append("components")
    
    nodeAttributes["json"].append(["key", False])
    nodeAttributes["data"].append(["id", False])
    nodeAttributes["if"].append(["id", False])
    nodeAttributes["if_check"].append(["id", False])
    nodeAttributes["if_check"].append(["check", False])
    nodeAttributes["switch"].append(["id", False])
    nodeAttributes["case"].append(["check", False])
    nodeAttributes["buildster"].append(["directory", False])
    nodeAttributes["buildster"].append(["distribution", False])
    nodeAttributes["project"].append(["directory", False])
    nodeAttributes["project"].append(["cmake_modules", True])
    nodeAttributes["export"].append(["except", True])
    nodeAttributes["export"].append(["type", False])
    nodeAttributes["target"].append(["type", False])
    nodeAttributes["target"].append(["linkage", True])
    nodeAttributes["link"].append(["linkage", True])
    nodeAttributes["link"].append(["language", True])
    nodeAttributes["pre"].append(["timing", True])
    nodeAttributes["post"].append(["timing", True])
    nodeAttributes["search"].append(["type", False])
    nodeAttributes["generator"].append(["architecture", True])
    nodeAttributes["origin"].append(["label", True])
    nodeAttributes["install"].append(["label", True])
    
    
    self.nodeTags = nodeTags
    self.nodeParents = {}
    self.nodeAttributes = {}
    
    for i in range(len(nodeTags)):
      tag = nodeTags[i]
      if (tag in nodeParents):
        if not (len(nodeParents[tag]) == 0):
          self.nodeParents[tag] = nodeParents[tag]
      if (tag in nodeAttributes):
        if not (len(nodeAttributes[tag]) == 0):
          self.nodeAttributes[tag] = nodeAttributes[tag]
    
    
    self.data = data
    self.debug = debug
    self.tier = 0
    self.root = None
    self.project = None
    self.error = None
    self.work = None
    self.context = self
    self.nodes = {}
    self.logs = []
    self.records = []
    self.projects = []
    self.labels = {}
    self.environment = os.environ.copy()
    
    if not ("BUILDSTER_WD" in self.data):
      self.data["BUILDSTER_WD"] = wd()
    if not ("BUILDSTER_OS" in self.data):
      self.data["BUILDSTER_OS"] = platform.system()
      if (("msys" in self.data["BUILDSTER_OS"].lower()) or ("cygwin" in self.data["BUILDSTER_OS"].lower())):
        self.data["BUILDSTER_OS"] = "Windows"
    if not ("BUILDSTER_VARIANT" in self.data):
      self.data["BUILDSTER_VARIANT"] = self.variant
    if not ("BUILDSTER_ARCH" in self.data):
      self.data["BUILDSTER_ARCH"] = platform.machine().lower()
    
  def build(self, owner, variant):
    self.tier = None
    self.log(self.node, "CONTEXT_BUILD_BEGIN\n")
    self.data["BUILDSTER_VARIANT"] = variant
    for i in range(len(self.projects)):
      if (self.projects[i] == None):
        continue
      self.project = self.projects[i]
      if not (self.projects[i].build(self, variant)):
        self.tier = None
        self.log(self.node, "CONTEXT_BUILD_END\n")
        return False
      self.project = None
    self.tier = None
    self.log(self.node, "CONTEXT_BUILD_END\n")
    return True
    
  def distribute(self, owner, distribution, variant):
    self.tier = None
    self.log(self.node, "CONTEXT_DISTRIBUTE_BEGIN\n")
    for i in range(len(self.projects)):
      if (self.projects[i] == None):
        continue
      self.project = self.projects[i]
      if not (self.projects[i].distribute(self, os.path.join(wd(), self.root.directory.getContent(), distribution).replace("\\", "/"), variant)):
        self.tier = None
        self.log(self.node, "CONTEXT_DISTRIBUTE_END\n")
        return False
      self.project = None
    self.tier = None
    self.log(self.node, "CONTEXT_DISTRIBUTE_END\n")
    return True
    
  def check(self, node, parent, parents = None):
    tag = node.tag
    if (tag == "label"):
      if (parent == None):
        return True
    if not (parents == None):
      parents = copy.deepcopy(parents)
      for i in range(len(parents)):
        if (parents[i] == None):
          continue
        parents[i] = parents[i].tag
    if not (tag in self.nodeTags):
      self.record(node, "Node Tag Error @ (\""+str(tag)+"\" | \""+str(parents)+"\")...")
      return False
    if (parent == None):
      if (tag in self.nodeParents):
        self.record(node, "Node Parent Error 1 @ (\""+str(tag)+"\" | \""+str(parents)+"\")...")
        return False
    else:
      if not (tag in self.nodeParents):
        self.record(node, "Node Parent Error 2 @ (\""+str(tag)+"\" | \""+str(parents)+"\")...")
        return False
      if not (self.any in self.nodeParents[tag]):
        if not (parent.tag in self.nodeParents[tag]):
          self.record(node, "Node Parent Error 3 (\""+str(parent.tag)+"\" | \""+str(self.nodeParents[tag])+"\") @ (\""+str(tag)+"\" | \""+str(parents)+"\")...")
          return False
    if (tag in self.nodeAttributes):
      attributes = self.nodeAttributes[tag]
      for attribute in attributes:
        optional = attribute[1]
        attribute = attribute[0]
        if not (attribute in node.attrib):
          if not (optional):
            self.record(node, "Node Attribute Error @ (\""+str(tag)+"\" | \""+str(parents)+"\")...")
            return False
    return True
    
  def optional(self, node, attribute):
    tag = node.tag
    if (tag in self.nodeAttributes):
      attributes = self.nodeAttributes[tag]
      for i in range(len(attributes)):
        optional = attributes[i][1]
        if ((optional) and (attribute == attributes[i][0])):
          return True
    return False
    
  def exclude(self, leaf):
    for exclusion in self.exclusions:
      if (leaf.endswith("."+exclusion)):
        return True
    return False
  
  def find(self, id):
    if not (id in self.data):
      return False
    return True
  
  def get(self, id):
    if not (id in self.data):
      return ""
    return self.data[id]
    
  def log(self, node, message):
    tag = ""
    if not (node == None):
      tag = "\\"+node.tag+"/|"
    now = datetime.now()
    if not (self.debug):
      return
    self.logs.append(tag+now.strftime("%d-%m-%Y@%H:%M:%S")+"\n")
    print(self.logs[len(self.logs)-1])
    if (self.tier == None):
      self.logs.append("\""+str(message.strip())+"\"\n")
      print(self.logs[len(self.logs)-1])
      return
    self.logs.append(("  "*self.tier)+str(self.tier)+": \""+str(message.strip())+"\"")
    print(self.logs[len(self.logs)-1])
  
  def record(self, node, message):
    record = []
    record.append(self.tier)
    record.append(message)
    record.append(node)
    record.append(traceback.format_list(traceback.extract_stack()))
    self.records.append(record)
    
  def report(self):
    self.tier = None
    self.log(None, "CONTEXT_REPORT_BEGIN\n")
    length = len(self.records)
    for i in range(length):
      record = self.records[i]
      stack = record[3]
      self.tier = record[0]
      self.log(record[2], record[1])
      """
      if (self.debug):
        for j in range(len(stack)):
          frame = stack[j]
          self.log(record[2], frame)
      """
    self.tier = None
    self.log(None, "CONTEXT_REPORT_END\n")
    
  def getContext(self):
    return self
    
  def getLogs(self):
    logs = ""
    length = len(self.logs)
    for i in range(length):
      log = self.logs[i]
      logs += log
    return logs
