
# Author: Pierce Brooks

import os
import ast
import ssl
import sys
import json
import shlex
import base64
import pathlib
import logging
import traceback
import multiprocessing
import xml.etree.ElementTree as xml_tree

try:
  from .internal import *
  from .internal.utilities import *
  from .internal.string import String
  from .internal.key import Key
  from .internal.value import Value
  from .internal.destination import Destination
  from .internal.content import Content
  from .internal.copier_source import CopierSource
  from .internal.copier_destination import CopierDestination
  from .internal.copier_rename import CopierRename
  from .internal.writer import Writer
  from .internal.copier import Copier
  from .internal.deleter import Deleter
  from .internal.extractor import Extractor
  from .internal.downloader import Downloader
  from .internal.branch import Branch
  from .internal.architecture import Architecture
  from .internal.generator import Generator
  from .internal.path import Path
  from .internal.url import URL
  from .internal.label import Label
  from .internal.work import Work
  from .internal.root import Root
  from .internal.term import Term
  from .internal.argument import Argument
  from .internal.argument_list import ArgumentList
  from .internal.native import Native
  from .internal.native_list import NativeList
  from .internal.exception import Exception
  from .internal.exception_list import ExceptionList
  from .internal.component import Component
  from .internal.component_list import ComponentList
  from .internal.hint import Hint
  from .internal.hint_list import HintList
  from .internal.variable import Variable
  from .internal.variable_list import VariableList
  from .internal.package import Package
  from .internal.package_list import PackageList
  from .internal.module import Module
  from .internal.module_list import ModuleList
  from .internal.definition import Definition
  from .internal.definition_list import DefinitionList
  from .internal.link import Link
  from .internal.link_list import LinkList
  from .internal.build import Export
  from .internal.export_list import ExportList
  from .internal.build import Import
  from .internal.import_list import ImportList
  from .internal.build_instruction import BuildInstruction
  from .internal.build_instruction import PreBuildInstruction
  from .internal.build_instruction import PostBuildInstruction
  from .internal.cmake_build_instruction import CmakeBuildInstruction
  from .internal.shells_build_instruction import ShellsBuildInstruction
  from .internal.shell_build_instruction import ShellBuildInstruction
  from .internal.commands_build_instruction import CommandsBuildInstruction
  from .internal.command_build_instruction import CommandBuildInstruction
  from .internal.setter import Setter
  from .internal.remote_dependency import RemoteDependency
  from .internal.dependency_list import DependencyList
  from .internal.local_dependency import LocalDependency
  from .internal.username import Username
  from .internal.password import Password
  from .internal.credentials import Credentials
  from .internal.git_repo_dependency import GitRepoDependency
  from .internal.w_get_dependency import WGetDependency
  from .internal.target_list import TargetList
  from .internal.executable_target import ExecutableTarget
  from .internal.library_target import LibraryTarget
  from .internal.project import Project
  from .internal.base import Buildster
  from .internal.context import Context
except:
  from internal import *
  from internal.utilities import *
  from internal.string import String
  from internal.key import Key
  from internal.value import Value
  from internal.destination import Destination
  from internal.content import Content
  from internal.copier_source import CopierSource
  from internal.copier_destination import CopierDestination
  from internal.copier_rename import CopierRename
  from internal.writer import Writer
  from internal.copier import Copier
  from internal.deleter import Deleter
  from internal.extractor import Extractor
  from internal.downloader import Downloader
  from internal.branch import Branch
  from internal.architecture import Architecture
  from internal.generator import Generator
  from internal.path import Path
  from internal.url import URL
  from internal.label import Label
  from internal.work import Work
  from internal.root import Root
  from internal.term import Term
  from internal.argument import Argument
  from internal.argument_list import ArgumentList
  from internal.native import Native
  from internal.native_list import NativeList
  from internal.exception import Exception
  from internal.exception_list import ExceptionList
  from internal.component import Component
  from internal.component_list import ComponentList
  from internal.hint import Hint
  from internal.hint_list import HintList
  from internal.variable import Variable
  from internal.variable_list import VariableList
  from internal.package import Package
  from internal.package_list import PackageList
  from internal.module import Module
  from internal.module_list import ModuleList
  from internal.definition import Definition
  from internal.definition_list import DefinitionList
  from internal.link import Link
  from internal.link_list import LinkList
  from internal.build import Export
  from internal.export_list import ExportList
  from internal.build import Import
  from internal.import_list import ImportList
  from internal.build_instruction import BuildInstruction
  from internal.build_instruction import PreBuildInstruction
  from internal.build_instruction import PostBuildInstruction
  from internal.cmake_build_instruction import CmakeBuildInstruction
  from internal.shells_build_instruction import ShellsBuildInstruction
  from internal.shell_build_instruction import ShellBuildInstruction
  from internal.commands_build_instruction import CommandsBuildInstruction
  from internal.command_build_instruction import CommandBuildInstruction
  from internal.setter import Setter
  from internal.remote_dependency import RemoteDependency
  from internal.dependency_list import DependencyList
  from internal.local_dependency import LocalDependency
  from internal.username import Username
  from internal.password import Password
  from internal.credentials import Credentials
  from internal.git_repo_dependency import GitRepoDependency
  from internal.w_get_dependency import WGetDependency
  from internal.target_list import TargetList
  from internal.executable_target import ExecutableTarget
  from internal.library_target import LibraryTarget
  from internal.project import Project
  from internal.base import Buildster
  from internal.context import Context

def handle(context, node, tier, parents):
  parent = parents[len(parents)-1]
  quit = False
  result = True
  output = []
  elements = {}
  element = None
  null = [True, "", {}]
  if (node == None):
    return null
  tag = node.tag.lower()
  context.tier = tier
  context.log(node, tag)
  #context.log(node, "NODE_BEGIN\n")
  if (context.check(node, parent, parents)):
    element = None
    if ((tag in context.conditionals) and (("id" in node.attrib) or (context.optional(node, "id")))):
      id = None
      if ("id" in node.attrib):
        id = node.attrib["id"]
      if (tag == "if"):
        if not (context.find(id)):
          context.log(node, id+" does not exist in data!")
          children = False
          for child in node:
            if (child.tag == "else"):
              children = True
              context.tier = tier
              call = handle(context, child, tier+1, parents+[node])
              if not (call[0]):
                result = False
                break
              if (child.tag in context.conditionals):
                output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
              elif (child.tag in context.nonconditionals):
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
              break
          if not (children):
            return null
          return [result, output, elements]
      elif (tag == "if_check"):
        check = node.attrib["check"]
        if not (ensure(context.get(id)).strip() == check):
          context.log(node, id+" does not match \""+check+"\" check!")
          children = False
          for child in node:
            if (child.tag == "else"):
              children = True
              context.tier = tier
              call = handle(context, child, tier+1, parents+[node])
              if not (call[0]):
                result = False
                break
              if (child.tag in context.conditionals):
                output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
              elif (child.tag in context.nonconditionals):
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
              break
          if not (children):
            return null
          return [result, output, elements]
      elif (tag == "if_exists"):
          exists = None
          for child in parent:
            if (child.tag == "exists"):
              exists = child
              break
          if not (exists == None):
            call = handle(context, exists, tier, parents)
            if not (call[0]):
              context.log(node, "A \"if_exists\" node was blocked by a descendant \"exists\"!\n")
              return null
            else:
              exists = ensure(exists.text).strip()+ensure(call[1]).strip()
              exists = exists.strip()
              if not (existence(exists)):
                context.log(node, id+" does not match \""+exists+"\" check!")
                children = False
                for child in node:
                  if (child.tag == "else"):
                    children = True
                    context.tier = tier
                    call = handle(context, child, tier+1, parents+[node])
                    if not (call[0]):
                      result = False
                      break
                    if (child.tag in context.conditionals):
                      output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
                    elif (child.tag in context.nonconditionals):
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
                    break
                if not (children):
                  return null
                return [result, output, elements]
          else:
            context.report(node, "No \"exists\" descendant for \"if_exists\" node!\n")
            return null
      elif (tag == "switch"):
        id = node.attrib["id"]
        children = False
        default = None
        for child in node:
          if (child.tag == "case"):
            check = child.attrib["check"]
            if (ensure(context.get(id)).strip() == check):
              children = True
              context.tier = tier
              call = handle(context, child, tier+1, parents+[node])
              if not (call[0]):
                result = False
                break
              if (child.tag in context.conditionals):
                output.append([ensure(call[1]).strip(), ensure(child.tail).strip()])
              elif (child.tag in context.nonconditionals):
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
              break
          elif (child.tag == "default"):
            default = child
        if not (children):
          if not (default == None):
            context.tier = tier
            call = handle(context, default, tier+1, parents+[node])
            if not (call[0]):
              result = False
            else:
              if (default.tag in context.conditionals):
                output.append([ensure(call[1]).strip(), ensure(default.tail).strip()])
              elif (default.tag in context.nonconditionals):
                output.append([ensure(call[1]).strip(), ensure(default.tail).strip()])
              for key in call[2]:
                value = call[2][key]
                if not (value == None):
                  for i in range(len(value)):
                    if not (value[i] == None):
                      if (default.tag in context.conditionals):
                        if not (key in elements):
                          elements[key] = []
                        elements[key].append(value[i])
                      else:
                        if not (default.tag in elements):
                          elements[default.tag] = []
                        elements[default.tag].append(value[i])
        output = ensure(node.text)+flatten(output).strip()
        return [result, output.strip(), elements]
      else:
        return null
    elif (tag == "else"):
      if (parent.tag in context.conditionals):
        id = None
        if ("id" in parent.attrib):
          id = parent.attrib["id"]
        if (parent.tag == "if"):
          if (context.find(id)):
            context.log(node, str(id)+" does exist in data for else case!")
            return null
        elif (parent.tag == "if_check"):
          check = parent.attrib["check"]
          if (ensure(context.get(id)).strip() == check):
            context.log(node, str(id)+" does match \""+check+"\" check for else case!")
            return null
        elif (parent.tag == "if_exists"):
          exists = None
          for child in parent:
            if (child.tag == "exists"):
              exists = child
              break
          if not (exists == None):
            call = handle(context, exists, tier, parents)
            if not (call[0]):
              context.log(node, "A \"if_exists\" node was blocked by a descendant \"exists\"!\n")
              return null
            else:
              exists = ensure(exists.text).strip()+ensure(call[1]).strip()
              exists = exists.strip()
              if (existence(exists)):
                context.log(node, str(id)+" does match \""+exists+"\" check for else case!")
                return null
          else:
            context.report(node, "No \"exists\" descendant for \"if_exists\" node!\n")
            return null
        else:
          return null
    elif (tag == "quit"):
      quit = True
      result = False
    elif (tag == "buildster"):
      element = Buildster()
      element.context = context
      if ("directory" in node.attrib):
        element.directory = Path(String(node.attrib["directory"].strip()))
      if ("distribution" in node.attrib):
        element.distribution = Path(String(node.attrib["distribution"].strip()))
      if ("cpp" in node.attrib):
        element.cpp = String(node.attrib["cpp"].strip())
      else:
        element.cpp = String("14")
      context.root = element
    elif (tag == "project"):
      element = Project()
      element.context = context
      if ("directory" in node.attrib):
        element.directory = Path(String(node.attrib["directory"].strip()))
      if ("cmake_modules" in node.attrib):
        element.cmake_modules = Path(String(node.attrib["cmake_modules"].strip()))
      if not (element in context.projects):
        context.projects.append(element)
      context.project = element
    elif (tag == "dependencies"):
      element = DependencyList()
    elif (tag == "targets"):
      element = TargetList()
    elif (tag == "local"):
      element = LocalDependency()
    elif (tag == "remote"):
      element = RemoteDependency()
    elif (tag == "git_repo"):
      element = GitRepoDependency()
    elif (tag == "wget"):
      element = WGetDependency()
    elif (tag == "target"):
      target = node.attrib["type"]
      if (target == "executable"):
        element = ExecutableTarget()
      elif (target == "library"):
        element = LibraryTarget()
      else:
        pass
      if ("linkage" in node.attrib):
        element.linkage = String(node.attrib["linkage"].strip())
    elif (tag == "pre"):
      element = PreBuildInstruction()
      if ("timing" in node.attrib):
        element.timing = String(node.attrib["timing"].strip())
    elif (tag == "post"):
      element = PostBuildInstruction()
      if ("timing" in node.attrib):
        element.timing = String(node.attrib["timing"].strip())
    elif (tag == "build"):
      element = BuildInstruction()
    elif (tag == "arguments"):
      element = ArgumentList()
    elif (tag == "natives"):
      element = NativeList()
    elif (tag == "variables"):
      element = VariableList()
    elif (tag == "variable"):
      element = Variable()
    elif (tag == "packages"):
      element = PackageList()
    elif (tag == "package"):
      element = Package()
    elif (tag == "modules"):
      element = ModuleList()
    elif (tag == "module"):
      element = Module()
    elif (tag == "components"):
      element = ComponentList()
    elif (tag == "component"):
      element = Component()
    elif (tag == "hints"):
      element = HintList()
    elif (tag == "hint"):
      element = Hint()
    elif (tag == "exceptions"):
      element = ExceptionList()
    elif (tag == "exception"):
      element = Exception()
    elif (tag == "cmake"):
      element = CmakeBuildInstruction()
    elif (tag == "shells"):
      element = ShellsBuildInstruction()
    elif (tag == "shell"):
      element = ShellBuildInstruction()
    elif (tag == "commands"):
      element = CommandsBuildInstruction()
    elif (tag == "command"):
      element = CommandBuildInstruction()
    elif (tag == "destination"):
      element = Destination()
    elif (tag == "content"):
      element = Content()
    elif (tag == "write"):
      element = Writer()
    elif (tag == "delete"):
      element = Deleter()
    elif (tag == "extract"):
      element = Extractor()
    elif (tag == "download"):
      element = Downloader()
    elif (tag == "copy"):
      element = Copier()
    elif (tag == "from"):
      element = CopierSource()
    elif (tag == "to"):
      element = CopierDestination()
    elif (tag == "rename"):
      element = CopierRename()
    elif (tag == "definition"):
      element = Definition()
    elif (tag == "definitions"):
      element = DefinitionList()
    elif (tag == "links"):
      element = LinkList()
    elif (tag == "export"):
      element = Export()
    elif (tag == "exports"):
      element = ExportList()
    elif (tag == "imports"):
      element = ImportList()
    elif (tag == "root"):
      element = Root()
    elif (tag == "term"):
      element = Term()
    children = False
    for child in node:
      if (child.tag == "exists"):
        call = ["", ensure(child.tail).strip()]
        context.log(node, "A \""+str(tag)+"\" had a \"exists\" child that was replaced with \""+str(call)+"\"")
        output.append(call)
        continue
      children = True
      context.tier = tier
      call = handle(context, child, tier+1, parents+[node])
      if not (call[0]):
        result = False
        break
      if (child.tag.lower() in context.conditionals):
        output.append([ensure(call[1]).strip(), ensure(child.tail)])
      elif ((child.tag.lower() in context.nonconditionals) or (child.tag.lower() in context.substitutes)):
        if (child.tag.lower() in context.substitutes):
          output.append([ensure(call[1]), ensure(child.tail)])
        else:
          output.append([ensure(call[1]).strip(), ensure(child.tail)])
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
    context.log(node, tag)
    success = True
    if not (tag in context.nodeAttributes):
      if (tag == "key"):
        output = ensure(node.text)+flatten(output).strip()
        element = Key()
        element.string = String(output.strip())
      elif (tag == "value"):
        output = ensure(node.text)+flatten(output).strip()
        element = Value()
        element.string = String(output.strip())
      elif (tag == "definition"):
        if ("key" in elements):
          for key in elements["key"]:
            element.key = key
            break
          elements["key"] = None
        if ("value" in elements):
          for value in elements["value"]:
            element.value = value
            break
          elements["value"] = None
      elif (tag == "definitions"):
        if ("definition" in elements):
          for definition in elements["definition"]:
            element.addDefinition(definition)
          elements["definition"] = None
      elif (tag == "exports"):
        if ("export" in elements):
          for e in elements["export"]:
            element.addExport(e)
          elements["export"] = None
      elif (tag == "imports"):
        if ("import" in elements):
          for i in elements["import"]:
            element.addImport(i)
          elements["import"] = None
      elif (tag == "links"):
        if ("link" in elements):
          for link in elements["link"]:
            element.addLink(link)
          elements["link"] = None
      elif (tag == "dependencies"):
        if ("dependency" in elements):
          for dependency in elements["dependency"]:
            element.addDependency(dependency)
          elements["dependency"] = None
      elif (tag == "dependency"):
        if ("local" in elements):
          for local in elements["local"]:
            element = local
            break
          elements["local"] = None
        if ("remote" in elements):
          for remote in elements["remote"]:
            element = remote
            break
          elements["remote"] = None
        if ("subpath" in elements):
          for subpath in elements["subpath"]:
            element.subpath = subpath
            break
          elements["subpath"] = None
        if ("label" in elements):
          for label in elements["label"]:
            element.label = label
            break
          elements["label"] = None
        if ("build" in elements):
          for instruction in elements["build"]:
            element.instruction = instruction
            break
          elements["build"] = None
        if ("imports" in elements):
          for imports in elements["imports"]:
            element.imports = imports
            break
          elements["imports"] = None
        if ("exports" in elements):
          for exports in elements["exports"]:
            element.exports = exports
            break
          elements["exports"] = None
        context.log(node, element.toString()+"\n")
      elif (tag == "targets"):
        if ("target" in elements):
          for target in elements["target"]:
            element.addTarget(target)
          elements["target"] = None
        context.log(node, element.toString()+"\n")
      elif (tag == "local"):
        if ("path" in elements):
          for path in elements["path"]:
            element.path = path
            break
          elements["path"] = None
      elif (tag == "remote"):
        if ("git_repo" in elements):
          for git_repo in elements["git_repo"]:
            element = git_repo
            break
          elements["git_repo"] = None
        if ("wget" in elements):
          for w_get in elements["wget"]:
            element = w_get
            break
          elements["wget"] = None
        if ("url" in elements):
          for url in elements["url"]:
            element.url = url
            break
          elements["url"] = None
      elif (tag == "git_repo"):
        if ("branch" in elements):
          element.branch = elements["branch"][0]
          elements["branch"][0] = None
        if ("credentials" in elements):
          element.credentials = elements["credentials"][0]
          elements["credentials"][0] = None
        context.log(node, element.toString()+"\n")
      elif (tag == "wget"):
        output = ensure(node.text)+flatten(output).strip()
        element.string = String(output.strip())
      elif (tag == "branch"):
        output = ensure(node.text)+flatten(output).strip()
        element = Branch()
        element.string = String(output.strip())
      elif (tag == "subpath"):
        output = ensure(node.text)+flatten(output).strip()
        element = Path()
        element.string = String(output.strip())
      elif (tag == "path"):
        output = ensure(node.text)+flatten(output).strip()
        element = Path()
        element.string = String(output.strip())
      elif (tag == "url"):
        output = ensure(node.text)+flatten(output).strip()
        element = URL()
        element.string = String(output.strip())
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
        element.string = String(output.strip())
      elif (tag == "password"):
        output = ensure(node.text)+flatten(output).strip()
        element = Password()
        element.string = String(output.strip())
      elif (tag == "message"):
        output = ensure(node.text)+flatten(output).strip()
        context.record(node, output.strip()+"\n")
      elif (tag == "quit"):
        pass
      elif (tag == "import"):
        output = ensure(node.text)+flatten(output).strip()
        element = Import()
        element.label = Label(String(output.strip()))
      elif (tag == "label"):
        output = ensure(node.text)+flatten(output).strip()
        element = Label()
        element.string = String(output.strip())
        if not (parent == None):
          if not (element.getContent() in context.labels):
            context.labels.append(element.getContent())
          else:
            context.log(node, "Labels (\""+element.getContent()+"\") must be unique!\n")
            result = False
      elif (tag == "source"):
        output = ensure(node.text)+flatten(output).strip()
        element = Path()
        element.string = String(output.strip())
      elif (tag == "argument"):
        output = ensure(node.text)+flatten(output).strip()
        element = Argument()
        element.string = String(output.strip())
      elif (tag == "native"):
        output = ensure(node.text)+flatten(output).strip()
        element = Native()
        element.string = String(output.strip())
      elif (tag == "exception"):
        output = ensure(node.text)+flatten(output).strip()
        element = Exception()
        element.string = String(output.strip())
      elif (tag == "hint"):
        output = ensure(node.text)+flatten(output).strip()
        element = Hint()
        element.string = String(output.strip())
      elif (tag == "component"):
        output = ensure(node.text)+flatten(output).strip()
        element = Component()
        element.string = String(output.strip())
      elif (tag == "variable"):
        if ("key" in elements):
          for key in elements["key"]:
            element.key = key
            break
          elements["key"] = None
        if ("value" in elements):
          for value in elements["value"]:
            element.value = value
            break
          elements["value"] = None
      elif (tag == "module"):
        if ("label" in elements):
          for label in elements["label"]:
            element.label = label
            if (label.getContent() in context.labels):
              for i in range(len(context.labels)):
                if (context.labels[i] == label.getContent()):
                  if (i == 0):
                    if (len(context.labels) > 1):
                      context.labels = context.labels[1:]
                    else:
                      context.labels = []
                    break
                  if (i == len(context.labels)-1):
                    context.labels = context.labels[:(len(context.labels)-1)]
                    break
                  context.labels = context.labels[:i]+context.labels[(i+1):]
                  break
            break
          elements["label"] = None
        if ("exports" in elements):
          for exports in elements["exports"]:
            element.exports = exports
            break
          elements["exports"] = None
      elif (tag == "package"):
        if ("label" in elements):
          for label in elements["label"]:
            element.label = label
            if (label.getContent() in context.labels):
              for i in range(len(context.labels)):
                if (context.labels[i] == label.getContent()):
                  if (i == 0):
                    if (len(context.labels) > 1):
                      context.labels = context.labels[1:]
                    else:
                      context.labels = []
                    break
                  if (i == len(context.labels)-1):
                    context.labels = context.labels[:(len(context.labels)-1)]
                    break
                  context.labels = context.labels[:i]+context.labels[(i+1):]
                  break
            break
          elements["label"] = None
        if ("exports" in elements):
          for exports in elements["exports"]:
            element.exports = exports
            break
          elements["exports"] = None
        if ("hints" in elements):
          for hints in elements["hints"]:
            element.hints = hints
            break
          elements["hints"] = None
        if ("components" in elements):
          for components in elements["components"]:
            element.components = components
            break
          elements["hints"] = None
        if ("variables" in elements):
          for variables in elements["variables"]:
            element.variables = variables
            break
          elements["variables"] = None
      elif (tag == "work"):
        output = ensure(node.text)+flatten(output).strip()
        element = Work()
        element.string = String(output.strip())
      elif (tag == "exceptions"):
        if ("exception" in elements):
          for exception in elements["exception"]:
            element.addException(exception)
          elements["exception"] = None
      elif (tag == "hints"):
        if ("hint" in elements):
          for hint in elements["hint"]:
            element.addHint(hint)
          elements["hint"] = None
      elif (tag == "components"):
        if ("component" in elements):
          for component in elements["component"]:
            element.addComponent(component)
          elements["component"] = None
      elif (tag == "variables"):
        if ("variable" in elements):
          for variable in elements["variable"]:
            element.addVariable(variable)
          elements["variable"] = None
      elif (tag == "arguments"):
        if ("argument" in elements):
          for argument in elements["argument"]:
            element.addArgument(argument)
          elements["argument"] = None
      elif (tag == "natives"):
        if ("native" in elements):
          for native in elements["native"]:
            element.addNative(native)
          elements["native"] = None
      elif (tag == "modules"):
        if ("module" in elements):
          for module in elements["module"]:
            element.addModule(module)
          elements["module"] = None
      elif (tag == "packages"):
        if ("package" in elements):
          for package in elements["package"]:
            element.addPackage(package)
          elements["package"] = None
      elif (tag == "build"):
        if ("cmake" in elements):
          for cmake in elements["cmake"]:
            element = cmake
            break
          elements["cmake"] = None
        if ("shells" in elements):
          for shells in elements["shells"]:
            element = shells
            break
          elements["shells"] = None
        if ("arguments" in elements):
          for arguments in elements["arguments"]:
            element.arguments = arguments
            break
          elements["arguments"] = None
        if ("pre" in elements):
          for pre in elements["pre"]:
            element.pre = pre
            if not (pre.timing == None):
              if (pre.timing.getContent() == "parse"):
                if not (pre.build(context.project, os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), os.path.basename(context.project.directory.getContent())), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent()), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), "install"), {}, context.variant)):
                  context.error = "Parse time pre build stop failure!"
            break
          elements["pre"] = None
        if ("post" in elements):
          for post in elements["post"]:
            element.post = post
            if not (post.timing == None):
              if (post.timing.getContent() == "parse"):
                if not (post.build(context.project, os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), os.path.basename(context.project.directory.getContent())), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent()), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), "install"), {}, context.variant)):
                  context.error = "Parse time post build stop failure!"
            break
          elements["post"] = None
      elif (tag == "cmake"):
        if ("generator" in elements):
          for generator in elements["generator"]:
            element.generator = generator
            break
          elements["generator"] = None
        if ("source" in elements):
          for source in elements["source"]:
            element.source = source
            break
          elements["source"] = None
        if ("natives" in elements):
          for natives in elements["natives"]:
            element.natives = natives
            break
          elements["natives"] = None
      elif (tag == "root"):
        output = ensure(node.text)+flatten(output).strip()
        element.string = String(output.strip())
      elif (tag == "term"):
        output = ensure(node.text)+flatten(output).strip()
        element.string = String(output.strip())
      elif (tag == "from"):
        output = ensure(node.text)+flatten(output).strip()
        element.path = Path(String(output.strip()))
      elif (tag == "to"):
        output = ensure(node.text)+flatten(output).strip()
        element.path = Path(String(output.strip()))
      elif (tag == "rename"):
        output = ensure(node.text)+flatten(output).strip()
        element.name = String(output.strip())
      elif (tag == "destination"):
        output = ensure(node.text)+flatten(output).strip()
        element.path = Path(String(output.strip()))
      elif (tag == "content"):
        output = ensure(node.text)+flatten(output).strip()
        element.string = String(output.strip())
      elif (tag == "shells"):
        if ("shell" in elements):
          for shell in elements["shell"]:
            element.shells.append(shell)
          elements["shell"] = None
      elif (tag == "shell"):
        if ("commands" in elements):
          for commands in elements["commands"]:
            element.commands = commands
            break
          elements["commands"] = None
        if ("work" in elements):
          for work in elements["work"]:
            element.work = work
            break
          elements["work"] = None
      elif (tag == "commands"):
        if ("command" in elements):
          for command in elements["command"]:
            element.commands.append(command)
          elements["command"] = None
      elif (tag == "command"):
        output = ensure(node.text)+flatten(output).strip()
        element.string = String(output.strip())
        if ("extract" in elements):
          for extract in elements["extract"]:
            element.extracts.append(extract)
          elements["extract"] = None
        if ("download" in elements):
          for download in elements["download"]:
            element.downloads.append(download)
          elements["download"] = None
        if ("copy" in elements):
          for copy in elements["copy"]:
            element.copies.append(copy)
          elements["copy"] = None
        if ("delete" in elements):
          for delete in elements["delete"]:
            element.deletes.append(delete)
          elements["delete"] = None
        if ("write" in elements):
          for wrote in elements["write"]:
            element.writes.append(wrote)
          elements["write"] = None
        if ("set" in elements):
          for setter in elements["set"]:
            element.writes.append(setter)
          elements["set"] = None
      elif (tag == "write"):
        if ("destination" in elements):
          for destination in elements["destination"]:
            element.destination = destination
            break
          elements["destination"] = None
        if ("content" in elements):
          for content in elements["content"]:
            element.content = content
            break
          elements["content"] = None
      elif (tag == "copy"):
        if ("from" in elements):
          for source in elements["from"]:
            element.source = source
            break
          elements["from"] = None
        if ("to" in elements):
          for destination in elements["to"]:
            element.destination = destination
            break
          elements["to"] = None
        if ("rename" in elements):
          for rename in elements["rename"]:
            element.rename = rename
            break
          elements["rename"] = None
      elif (tag == "extract"):
        output = ensure(node.text)+flatten(output).strip()
        element.path = Path(String(output.strip()))
      elif (tag == "download"):
        output = ensure(node.text)+flatten(output).strip()
        element.url = URL(String(output.strip()))
      elif (tag == "delete"):
        output = ensure(node.text)+flatten(output).strip()
        element.path = Path(String(output.strip()))
      elif (tag == "exists"):
        output = ensure(node.text)+flatten(output).strip()
        output = output.strip()
      elif (tag == "distribution"):
        output = adjust(os.path.join(wd(), context.root.directory.getContent(), context.root.distribution.getContent(), context.variant.lower())).replace("\\", "/")
      elif (tag == "python"):
        output = sys.executable.replace("\\", "/")
      elif (tag == "cores"):
        output = str(multiprocessing.cpu_count())
      elif (tag == "home"):
        output = str(pathlib.Path.home()).replace("\\", "/")
      elif (tag == "execute"):
        output = ensure(node.text)+flatten(output).strip()
        command = shlex.split(output.strip())
        output = execute_command(command, context.environment).strip()
        print(output)
        if (output == None):
          output = ""
      elif (tag == "escape"):
        output = ensure(node.text)+flatten(output).strip()
        output = repr(output.strip())[1:]
        output = output[:(len(output)-1)]
      elif (tag == "unescape"):
        output = ensure(node.text)+flatten(output).strip()
        output = ast.literal_eval(F'"""{output.strip()}"""')
      elif (tag == "lower"):
        output = ensure(node.text)+flatten(output).strip()
        output = output.strip().lower()
      elif (tag == "upper"):
        output = ensure(node.text)+flatten(output).strip()
        output = output.strip().upper()
      elif (tag == "encode"):
        output = ensure(node.text)+flatten(output).strip()
        output = base64.b64encode(output.strip().encode("ascii")).decode("ascii")
      elif (tag == "decode"):
        output = ensure(node.text)+flatten(output).strip()
        output = base64.b64decode(output.strip().encode("ascii")).decode("ascii")
      elif (tag == "install"):
        dependency = get_parent(parents, "dependency")
        if not (dependency == None):
          label = get_child(dependency, "label")
          if not (label == None):
            project = get_parent(parents, "project")
            if not (project == None):
              temp = handle(context, label, tier, [dependency])
              output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"], "install", "dependencies", temp[1], context.variant.lower())).replace("\\", "/")
            else:
              context.report(node, "No \"project\" ancestor for \"label\" node!\n")
              result = False
          else:
            context.report(node, "No \"label\" descendant for \"dependency\" node!\n")
            result = False
        else:
          target = get_parent(parents, "target")
          if not (target == None):
            label = get_child(target, "label")
            if not (label == None):
              project = get_parent(parents, "project")
              if not (project == None):
                temp = handle(context, label, tier, [target])
                output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"], "install", "targets", temp[1], context.variant.lower())).replace("\\", "/")
              else:
                context.report(node, "No \"project\" ancestor for \"label\" node!\n")
                result = False
            else:
              context.report(node, "No \"label\" descendant for \"target\" node!\n")
              result = False
          else:
            project = get_parent(parents, "project")
            if not (project == None):
              output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"])).replace("\\", "/")
            else:
              context.report(node, "No \"dependency\", \"target\", or \"project\" ancestor for \"install\" node!\n")
              result = False
      elif (tag == "origin"):
        dependency = get_parent(parents, "dependency")
        if not (dependency == None):
          local = get_child(dependency, "local")
          if not (local == None):
            temp = handle(context, get_child(local, "path"), tier, [local])
            output = flatten(temp[1]).strip().replace("\\", "/")
          else:
            label = get_child(dependency, "label")
            if not (label == None):
              project = get_parent(parents, "project")
              if not (project == None):
                temp = handle(context, label, tier, [dependency])
                output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"], "build", "dependencies", temp[1].strip())).replace("\\", "/")
              else:
                context.report(node, "No \"project\" ancestor for \"label\" node!\n")
                result = False
            else:
              context.report(node, "No \"label\" descendant for \"dependency\" node!\n")
              result = False
        else:
          target = get_parent(parents, "target")
          if not (target == None):
            label = get_child(target, "label")
            if not (label == None):
              project = get_parent(parents, "project")
              if not (project == None):
                temp = handle(context, label, tier, [target])
                output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"], temp[1])).replace("\\", "/")
              else:
                context.report(node, "No \"project\" ancestor for \"label\" node!\n")
                result = False
            else:
              context.report(node, "No \"label\" descendant for \"target\" node!\n")
              result = False
          else:
            project = get_parent(parents, "project")
            if not (project == None):
              output = adjust(os.path.join(wd(), context.root.directory.getContent(), project.attrib["directory"])).replace("\\", "/")
            else:
              context.report(node, "No \"dependency\", \"target\", or \"project\" ancestor for \"origin\" node!\n")
              result = False
      elif (tag == "default"):
        output = ensure(node.text)+flatten(output).strip()
        output = output.strip()
        context.log(node, output+"\n")
      elif (tag == "log"):
        output = ensure(context.getLogs()).strip()
      elif (tag == "read"):
        output = ensure(node.text)+flatten(output).strip()
        output = output.strip()
        if (os.path.isfile(output)):
          lines = read(output)
          output = flatten(lines)
        else:
          output = ""
        context.log(node, output+"\n")
      elif (tag == "set"):
        element = Setter()
        if ("key" in elements):
          for key in elements["key"]:
            element.key = key
            break
          elements["key"] = None
        if ("value" in elements):
          for value in elements["value"]:
            element.value = value
            break
          elements["value"] = None
      else:
        success = False
    else:
      if (tag == "data"):
        output = ensure(context.get(node.attrib["id"])).strip()
        context.log(node, output+"\n")
      elif (tag == "link"):
        output = ensure(node.text)+flatten(output).strip()
        element = Link()
        element.string = String(output.strip())
        if ("linkage" in node.attrib):
          element.linkage = String(node.attrib["linkage"].strip())
        if ("language" in node.attrib):
          element.language = String(node.attrib["language"].strip())
      elif (tag == "pre"):
        for key in elements:
          for value in elements[key]:
            element.instructions.append(value)
        if (parent.tag == "project"):
          context.projects[len(context.projects)-1].pre = element
          if not (element.timing == None):
            if (element.timing.getContent() == "discover"):
              context.projects[len(context.projects)-1].buildPre(context.variant)
          else:
            context.projects[len(context.projects)-1].buildPre(context.variant)
        else:
          if not (element.timing == None):
            if (element.timing.getContent() == "discover"):
              if not (element.build(context.project, os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), os.path.basename(context.project.directory.getContent())), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent()), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), "install"), {}, context.variant)):
                context.error = "Discover time pre build stop failure!"
      elif (tag == "post"):
        for key in elements:
          for value in elements[key]:
            element.instructions.append(value)
        if (parent.tag == "project"):
          context.projects[len(context.projects)-1].post = element
          if not (element.timing == None):
            if (element.timing.getContent() == "discover"):
              context.projects[len(context.projects)-1].buildPost(context.variant)
          else:
            context.projects[len(context.projects)-1].buildPost(context.variant)
        else:
          if not (element.timing == None):
            if (element.timing.getContent() == "discover"):
              if not (element.build(context.project, os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), os.path.basename(context.project.directory.getContent())), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent()), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), "install"), {}, context.variant)):
                context.error = "Discover time post build stop failure!"
      elif (tag == "generator"):
        output = ensure(node.text)+flatten(output).strip()
        element = Generator()
        element.string = String(output.strip())
        if ("architecture" in node.attrib):
          architecture = Architecture()
          architecture.string = String(node.attrib["architecture"].strip())
          element.architecture = architecture
      elif (tag == "json"):
        output = ensure(node.text)+flatten(output).strip()
        dictionary = json.loads(output.strip())
        if (node.attrib["key"] in dictionary):
          output = dictionary[node.attrib["key"]]
        else:
          output = ""
        context.log(node, output+"\n")
      elif (tag == "case"):
        output = ensure(node.text)+flatten(output).strip()
        output = output.strip()
        context.log(node, output+"\n")
      elif (tag == "project"):
        if ("dependencies" in elements):
          element.dependencies = elements["dependencies"][0]
          elements["dependencies"][0] = None
        if ("targets" in elements):
          element.targets = elements["targets"][0]
          elements["targets"][0] = None
        if ("pre" in elements):
          for pre in elements["pre"]:
            element.pre = pre
            if not (pre.timing == None):
              if (pre.timing.getContent() == "parse"):
                element.buildPre(context.variant)
            else:
              element.buildPre(context.variant)
            break
          elements["pre"] = None
        if ("post" in elements):
          for post in elements["post"]:
            element.post = post
            if not (post.timing == None):
              if (post.timing.getContent() == "parse"):
                element.buildPost(context.variant)
            else:
              element.buildPost(context.variant)
            break
          elements["post"] = None
        context.log(node, element.toString()+"\n")
      elif (tag == "buildster"):
        context.log(node, element.toString()+"\n")
      elif (tag == "target"):
        if ("subpath" in elements):
          element.subpath = elements["subpath"][0]
          elements["subpath"][0] = None
        if ("label" in elements):
          element.label = elements["label"][0]
          elements["label"][0] = None
        if ("arguments" in elements):
          for arguments in elements["arguments"]:
            element.arguments = arguments
            break
          elements["arguments"] = None
        if ("natives" in elements):
          for natives in elements["natives"]:
            element.natives = natives
            break
          elements["natives"] = None
        if ("packages" in elements):
          for packages in elements["packages"]:
            element.packages = packages
            break
          elements["packages"] = None
        if ("modules" in elements):
          for modules in elements["modules"]:
            element.modules = modules
            break
          elements["modules"] = None
        if ("exceptions" in elements):
          for exceptions in elements["exceptions"]:
            element.exceptions = exceptions
            break
          elements["exceptions"] = None
        if ("definitions" in elements):
          for definitions in elements["definitions"]:
            element.definitions = definitions
            break
          elements["definitions"] = None
        if ("links" in elements):
          for links in elements["links"]:
            element.links = links
            break
          elements["links"] = None
        if ("imports" in elements):
          for imports in elements["imports"]:
            element.imports = imports
            break
          elements["imports"] = None
        if ("exports" in elements):
          for exports in elements["exports"]:
            element.exports = exports
            break
          elements["exports"] = None
        if ("generator" in elements):
          for generator in elements["generator"]:
            element.generator = generator
            break
          elements["generator"] = None
        if ("pre" in elements):
          for pre in elements["pre"]:
            element.pre = pre
            if not (pre.timing == None):
              if (pre.timing.getContent() == "parse"):
                if not (pre.build(context.project, os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), os.path.basename(context.project.directory.getContent())), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent()), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), "install"), {}, variant)):
                  context.error = "Parse time pre build stop failure!"
            break
          elements["pre"] = None
        if ("post" in elements):
          for post in elements["post"]:
            element.post = post
            if not (post.timing == None):
              if (post.timing.getContent() == "parse"):
                if not (post.build(context.project, os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), os.path.basename(context.project.directory.getContent())), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent()), os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), "install"), {}, variant)):
                  context.error = "Parse time post build stop failure!"
            break
          elements["post"] = None
        context.log(node, element.toString()+"\n")
      elif (tag == "export"):
        if ("type" in node.attrib):
          element.export = String(node.attrib["type"])
        if ("except" in node.attrib):
          element.exceptions = String(node.attrib["except"])
        if ("key" in elements):
          for key in elements["key"]:
            element.key = key
            break
          elements["key"] = None
        if ("value" in elements):
          for value in elements["value"]:
            element.value = value
            break
          elements["value"] = None
        if not (element.key == None):
          key = element.key.getContent()
          if not (key in context.data):
            if not (element.value == None):
              value = element.value.getContent()
              context.data[key] = value
      elif (tag == "search"):
        types = node.attrib["type"]
        roots = None
        if ("root" in elements):
          for root in elements["root"]:
            roots = root.getContent().strip()
            break
          elements["root"] = None
        if ("term" in elements):
          for term in elements["term"]:
            terms = term.getContent().strip()
            break
          elements["term"] = None
        if not ((roots == None) or (terms == None)):
          output = None
          for root, folders, files in os.walk(roots):
            if (types == "file"):
              for name in files:
                if (name == terms):
                  output = os.path.join(root, name)
                  break
              if not (output == None):
                break
          if (output == None):
            output = ""
        else:
          output = ""
      else:
        success = False
    if (success):
      if not (element == None):
        element.node = node
        if (type(element) == Project):
          if not (element in context.projects):
            context.projects.append(element)
          element.owner = context.root
          element.context = context
          context.record(node, element.toString()+"\n")
        elif (type(element) == Buildster):
          context.root = element
          element.context = context
          context.record(node, element.toString()+"\n")
        else:
          if not (tag in context.conditionals):
            if not (tag in elements):
              elements[tag] = []
            elements[tag].append(element)
    else:
      if not (children):
        if not (tag in context.substitutes):
          output = ensure(node.text)+flatten(output).strip()
          context.log(node, output+"\n")
  else:
    result = False
  if not (context.error == None):
    context.report(node, str(context.error))
    result = False
  if not (result):
    context.log(node, "Error!")
  else:
    context.nodes[node] = element
    if not (element == None):
      parent = get_parent(parents, None)
      if (parent in context.nodes):
        element.parent = context.nodes[parent]
  #context.log(node, "NODE_END\n")
  return [result, output, elements]

def run(target, data, environment):
  variants = []
  variants.append("Debug")
  variants.append("Release")
  for variant in variants:
    dictionary = {}
    for i in range(len(data)):
      element = data[i]
      elements = element.split("=")
      if (len(elements) == 2):
        left = elements[0].strip()
        right = elements[1].strip()
        dictionary[left] = right
    if ("BUILDSTER_VARIANT" in dictionary):
      if not (variant == dictionary["BUILDSTER_VARIANT"]):
        continue
    for key in environment:
      dictionary[key] = environment[key]
    tree = xml_tree.parse(target)
    base = tree.getroot()
    if not (base.tag == "buildster"):
      return False
    context = Context(dictionary, variant)
    if ("directory" in base.attrib):
      context.root = Buildster()
      context.root.node = base
      context.root.context = context
      context.root.directory = Path(String(base.attrib["directory"]))
    for child in base:
      if (child.tag == "project"):
        context.project = Project()
        context.project.node = child
        context.project.context = context
        if ("directory" in child.attrib):
          context.project.diretory = Path(String(child.attrib["directory"]))
        break
    result = handle(context, base, 0, [None])
    if not (result[0]):
      context.report()
      return False
    output = result[1]
    elements = result[2]
    if not (context.build(context, variant)):
      context.report()
      return False
    if not (context.distribute(context, context.root.distribution.getContent(), variant)):
      context.report()
      return False
    context.report()
  return True

def main(environment = None):
  ssl._create_default_https_context = ssl._create_unverified_context
  result = 0
  try:
    arguments = sys.argv
    length = len(arguments)
    if (length > 1):
      data = []
      if (length > 2):
        data = arguments[2:]
      if (environment == None):
        environment = os.environ.copy()
      code = run(arguments[1].strip(), data, environment)
      if not (code):
        print("Error! "+str(code))
        result = -1
    else:
      result = -2
  except:
    logging.error(traceback.format_exc())
    result = -3
  return result

if (__name__ == "__main__"):
  sys.exit(main())
