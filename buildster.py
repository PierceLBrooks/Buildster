
# Author: Pierce Brooks

import os
import sys
import xml.etree.ElementTree as xml_tree

class Object(object):
	def __init__(self):
		pass
		
	def toString(self, *arguments):
		if (len(arguments) == 0):
			return "("+self.__class__.__name__+")"+str(self)
		other = arguments[0]
		if (other == None):
			return "/NULL/"
		if not (isinstance(other, Object)):
			return "/INVALID/"
		return other.toString()
		
class Element(Object):
	def __init__(self):
		super(Element, self).__init__()
		
	def build(self):
		pass
		
class String(Object):
	def __init__(self, content = None):
		super(String, self).__init__()
		self.content = ""
		if (type(content) == str):
			self.content = content
			
	def __str__(self):
		return "<\""+self.content+"\">"
		
class List(Element):
	def __init__(self, content = None):
		super(Element, self).__init__()
		self.content = []
		if (type(content) == list):
			self.content = content
			
	def build(self):
		pass
		
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
			
	def __str__(self):
		to = "<["
		length = len(self.content)
		for i in range(length):
			to += self.content[i].toString()
			if not (i == length-1):
				to += ", "
		to += "]>"
		return to

class Dependency(Element):
	def __init__(self):
		super(Dependency, self).__init__()
		
	def build(self):
		pass
		
class DependencyList(List):
	def __init__(self):
		super(DependencyList, self).__init__()
		
	def build(self):
		length = len(self.content)
		for i in range(length):
			if (isinstance(self.content[i], Dependency)):
				self.content[i].build()
				
	def addDependency(self, dependency):
		if not (isinstance(dependency, Dependency)):
			return False
		return super(DependencyList, self).add(dependency)
		
class LibraryDependency(Dependency):
	def __init__(self, path = None):
		super(LibraryDependency, self).__init__()
		self.path = None
		if (type(path) == String):
			self.path = path
		
	def build(self):
		pass
		
class Username(Object):
	def __init__(self, string = None):
		super(Username, self).__init__()
		self.string = None
		if (type(string) == String):
			self.string = string
		
	def __str__(self):
		return "<"+self.toString(self.string)+">"
		
class Password(Object):
	def __init__(self, string = None):
		super(Password, self).__init__()
		self.string = None
		if (type(string) == String):
			self.string = string
		
	def __str__(self):
		return "<"+self.toString(self.string)+">"

class Credentials(Object):
	def __init__(self, username = None, password = None):
		super(Credentials, self).__init__()
		self.username = None
		self.password = None
		if (type(username) == Username):
			self.username = username
		if (type(password) == Password):
			self.password = password
		
	def __str__(self):
		return "<"+self.toString(self.username)+", "+self.toString(self.password)+">"
		
class URL(Object):
	def __init__(self, string = None):
		super(URL, self).__init__()
		self.string = None
		if (type(string) == String):
			self.string = string
		
	def __str__(self):
		return "<"+self.toString(self.string)+">"
		
class GitRepoDependency(Dependency):
	def __init__(self, url = None, credentials = None):
		super(GitRepoDependency, self).__init__()
		self.url = None
		self.credentials = None
		if (type(url) == URL):
			self.url = url
		if (type(credentials) == Credentials):
			self.credentials = credentials
		
	def build(self):
		pass
		
	def __str__(self):
		return "<"+self.toString(self.url)+", "+self.toString(self.credentials)+">"
		
class Target(Element):
	def __init__(self):
		super(Target, self).__init__()
		
	def build(self):
		pass
		
class TargetList(List):
	def __init__(self):
		super(TargetList, self).__init__()
		
	def build(self):
		length = len(self.content)
		for i in range(length):
			if (isinstance(self.content[i], Target)):
				self.content[i].build()
				
	def addTarget(self, target):
		if not (isinstance(target, Target)):
			return False
		return super(TargetList, self).add(target)
		
		
class Label(Object):
	def __init__(self, string = None):
		super(Label, self).__init__()
		self.string = None
		if (type(string) == String):
			self.string = string
		
	def __str__(self):
		return "<"+self.toString(self.string)+">"
		
class ExecutableTarget(Target):
	def __init__(self, label = None):
		super(ExecutableTarget, self).__init__()
		self.label = None
		if (type(label) == Label):
			self.label = label
		
	def build(self):
		pass
		
	def __str__(self):
		return "<"+self.toString(self.label)+">"
		
class LibraryTarget(Target):
	def __init__(self, label = None):
		super(LibraryTarget, self).__init__()
		self.label = None
		if (type(label) == Label):
			self.label = label
		
	def build(self):
		pass
		
	def __str__(self):
		return "<"+self.toString(self.label)+">"
		
class Project(Element):
	def __init__(self, dependencies = None, targets = None):
		super(Project, self).__init__()
		self.dependencies = None
		self.targets = None
		if (type(dependencies) == DependencyList):
			self.dependencies = dependencies
		if (type(targets) == TargetList):
			self.targets = targets
			
	def build(self):
		pass
		
	def __str__(self):
		return "<"+self.toString(self.dependencies)+", "+self.toString(self.targets)+">"

class Context(Element):
	def __init__(self, data, debug = True):
		super(Context, self).__init__()
		
		
		self.conditionals = []
		
		self.conditionals.append("if")
		self.conditionals.append("if_check")
		
		self.any = "any"
		
		
		nodeTags = []
		
		for conditional in self.conditionals:
			nodeTags.append(conditional)
		nodeTags.append("data")
		nodeTags.append("buildster")
		nodeTags.append("project")
		nodeTags.append("dependencies")
		nodeTags.append("git_repo")
		nodeTags.append("url")
		nodeTags.append("credentials")
		nodeTags.append("username")
		nodeTags.append("password")
		nodeTags.append("targets")
		nodeTags.append("executable")
		nodeTags.append("library")
		nodeTags.append("label")
		nodeTags.append("preprocessor")
		nodeTags.append("definition")
		nodeTags.append("key")
		nodeTags.append("value")
		nodeTags.append("linker")
		nodeTags.append("target")
		
		
		nodeParents = {}
		nodeAttributes = {}
		
		for i in range(len(nodeTags)):
			tag = nodeTags[i]
			parents = []
			attributes = []
			if not (tag == "buildster"):
				for conditional in self.conditionals:
					parents.append(conditional)
			nodeParents[tag] = parents
			nodeAttributes[tag] = attributes
		
		nodeParents["data"].append(self.any)
		nodeParents["if"].append(self.any)
		nodeParents["if_check"].append(self.any)
		#nodeParents["buildster"].append("")
		nodeParents["project"].append("buildster")
		nodeParents["dependencies"].append("project")
		nodeParents["git_repo"].append("dependencies")
		nodeParents["url"].append("git_repo")
		nodeParents["credentials"].append("git_repo")
		nodeParents["username"].append("credentials")
		nodeParents["password"].append("credentials")
		nodeParents["targets"].append("project")
		nodeParents["executable"].append("targets")
		nodeParents["library"].append("dependencies")
		nodeParents["library"].append("targets")
		nodeParents["label"].append("executable")
		nodeParents["label"].append("library")
		nodeParents["preprocessor"].append("executable")
		nodeParents["preprocessor"].append("library")
		nodeParents["definition"].append("preprocessor")
		nodeParents["key"].append("definition")
		nodeParents["value"].append("definition")
		nodeParents["linker"].append("executable")
		nodeParents["linker"].append("library")
		nodeParents["target"].append("linker")
		
		nodeAttributes["data"].append("id")
		nodeAttributes["if"].append("id")
		nodeAttributes["if_check"].append("id")
		nodeAttributes["if_check"].append("check")
		nodeAttributes["buildster"].append("directory")
		nodeAttributes["project"].append("directory")
		#nodeAttributes["dependency"].append("")
		#nodeAttributes["git_repo"].append("")
		#nodeAttributes["credentials"].append("")
		#nodeAttributes["username"].append("")
		#nodeAttributes["password"].append("")
		#nodeAttributes["executable"].append("")
		#nodeAttributes["library"].append("")
		#nodeAttributes["preprocessor"].append("")
		#nodeAttributes["definition"].append("")
		#nodeAttributes["key"].append("")
		#nodeAttributes["value"].append("")
		#nodeAttributes["linker"].append("")
		#nodeAttributes["target"].append("")
		
		
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
		self.records = []
		self.projects = []
		
	def build(self):
		pass
		
	def check(self, node, parent):
		tag = node.tag
		if not (tag in self.nodeTags):
			self.record("Node Tag Error...")
			return False
		if (parent == None):
			if (tag in self.nodeParents):
				self.record("Node Parent Error 1...")
				return False
		else:
			if not (tag in self.nodeParents):
				self.record("Node Parent Error 2...")
				return False
			if not (self.any in self.nodeParents[tag]):
				if not (parent.tag in self.nodeParents[tag]):
					self.record("Node Parent Error 3...")
					return False
		if (tag in self.nodeAttributes):
			attributes = self.nodeAttributes[tag]
			for attribute in attributes:
				if not (attribute in node.attrib):
					self.record("Node Attribute Error...")
					return False
		return True
	
	def find(self, id):
		if not (id in self.data):
			return False
		return True
	
	def get(self, id):
		if not (id in self.data):
			return ""
		return self.data[id]
		
	def log(self, message):
		if not (self.debug):
			return
		print(("  "*self.tier)+str(self.tier)+": "+message)
	
	def record(self, message):
		self.records.append([self.tier, message])
		
	def report(self):
		for i in range(len(self.records)):
			self.tier = self.records[i][0]
			self.log(self.records[i][1])

def flatten(output, prefix = "", suffix = ""):
	final = ""
	for i in range(len(output)):
		temp = output[i]
		final += prefix
		for j in range(len(temp)):
			final += temp[j]
		final += suffix
	return final

def ensure(string):
	if (string == None):
		return ""
	if not (type(string) == str):
		return ""
	return string

def handle(context, node, tier, parent):
	result = True
	tag = node.tag
	output = []
	elements = {}
	null = [True, "", {}]
	context.tier = tier
	context.log(tag)
	#context.log("NODE_BEGIN\n")
	if (context.check(node, parent)):
		element = None
		if (tag in context.conditionals):
			id = node.attrib["id"]
			if (tag == "if"):
				if not (context.find(id)):
					context.log(id+" does not exist in data!")
					return null
			else:
				check = node.attrib["check"]
				if not (ensure(context.get(id)).strip() == check):
					context.log(id+" does not match \""+check+"\" check!")
					return null
		elif (tag == "project"):
			element = Project()
		elif (tag == "dependencies"):
			element = DependencyList()
		elif (tag == "targets"):
			element = TargetList()
		elif (tag == "git_repo"):
			element = GitRepoDependency()
		elif (tag == "executable"):
			element = ExecutableTarget()
		elif (tag == "library"):
			if (parent.tag == "targets"):
				element = LibraryTarget()
			else:
				element = LibraryDependency()
		children = False
		for child in node:
			children = True
			context.tier = tier
			call = handle(context, child, tier+1, node)
			if not (call[0]):
				result = False
				break
			if (child.tag == "data"):
				output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
			for key in call[2]:
				value = call[2][key]
				if not (value == None):
					for i in range(len(value)):
						if not (value[i] == None):
							if (child.tag in context.conditionals):
								if not (key in elements):
									elements[key] = []
								elements[key].append(value[i])
							else:
								if not (child.tag in elements):
									elements[child.tag] = []
								elements[child.tag].append(value[i])
		context.tier = tier
		#context.log(tag)
		success = True
		if not (tag in context.nodeAttributes):
			if ((tag == "definition") or (tag == "key") or (tag == "value")):
				output = ensure(node.text)+flatten(output).strip()
				context.log(output+"\n")
			elif (tag == "dependencies"):
				if ("git_repo" in elements):
					for git_repo in elements["git_repo"]:
						element.addDependency(git_repo)
					elements["git_repo"] = None
				if ("library" in elements):
					for library in elements["library"]:
						element.addDependency(library)
					elements["library"] = None
				context.log(element.toString())
			elif (tag == "targets"):
				if ("executable" in elements):
					for executable in elements["executable"]:
						element.addTarget(executable)
					elements["executable"] = None
				if ("library" in elements):
					for library in elements["library"]:
						element.addTarget(library)
					elements["library"] = None
				context.log(element.toString())
			elif (tag == "git_repo"):
				if ("url" in elements):
					element.url = elements["url"][0]
					elements["url"][0] = None
				if ("credentials" in elements):
					element.credentials = elements["credentials"][0]
					elements["credentials"][0] = None
				context.log(element.toString())
			elif (tag == "url"):
				output = ensure(node.text)+flatten(output).strip()
				element = URL()
				element.string = String(output)
			elif (tag == "credentials"):
				element = Credentials()
				if ("username" in elements):
					element.username = elements["username"][0]
					elements["username"][0] = None
				if ("password" in elements):
					element.password = elements["password"][0]
					elements["password"][0] = None
			elif (tag == "username"):
				output = ensure(node.text)+flatten(output).strip()
				element = Username()
				element.string = String(output)
			elif (tag == "password"):
				output = ensure(node.text)+flatten(output).strip()
				element = Password()
				element.string = String(output)
			elif (tag == "executable"):
				if ("label" in elements):
					element.label = elements["label"][0]
					elements["label"][0] = None
			elif (tag == "label"):
				output = ensure(node.text)+flatten(output).strip()
				element = Label()
				element.string = String(output)
			else:
				success = False
		else:
			if (tag == "data"):
				output = ensure(context.get(node.attrib["id"])).strip()
				context.log(output+"\n")
			elif (tag == "project"):
				if ("dependencies" in elements):
					element.dependencies = elements["dependencies"][0]
					elements["dependencies"][0] = None
				if ("targets" in elements):
					element.targets = elements["targets"][0]
					elements["targets"][0] = None
				context.log(element.toString())
			else:
				success = False
		if (success):
			if not (element == None):
				if (type(element) == Project):
					context.projects.append(element)
				else:
					if not (tag in context.conditionals):
						if not (tag in elements):
							elements[tag] = []
						elements[tag].append(element)
		else:
			if not (children):
				output = ensure(node.text)+flatten(output).strip()
				context.log(output+"\n")
	else:
		result = False
	if not (result):
		context.log("Error!")
	#context.log("NODE_END\n")
	return [result, output, elements]

def run(target, data):
	dictionary = {}
	for i in range(len(data)):
		element = data[i]
		elements = element.split("=")
		if (len(elements) == 2):
			left = elements[0].strip()
			right = elements[1].strip()
			dictionary[left] = right
	tree = xml_tree.parse(target)
	base = tree.getroot()
	if not (base.tag == "buildster"):
		return False
	context = Context(dictionary)
	result = handle(context, base, 0, None)
	print("CONTEXT-REPORT_BEGIN\n")
	context.report()
	print("CONTEXT-REPORT_END\n")
	return result[0]

if (__name__ == "__main__"):
	result = 0
	arguments = sys.argv
	length = len(arguments)
	if (length > 1):
		data = []
		if (length > 2):
			data = arguments[2:]
		code = run(arguments[1], data)
		if not (code):
			result = -1
	sys.exit(result)
