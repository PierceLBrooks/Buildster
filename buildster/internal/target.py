
# Author: Pierce Brooks

import re
import os
import ast
import ssl
import sys
import copy
import json
import stat
import shlex
import shutil
import base64
import urllib
import fnmatch
import pathlib
import zipfile
import tarfile
import inspect
import logging
import pyunpack
import platform
import importlib
import traceback
import subprocess
import multiprocessing
import xml.etree.ElementTree as xml_tree
from urllib.parse import urlparse, unquote
from urllib.request import urlretrieve
from datetime import datetime

from .internal.build import Build
from .internal.string import String
from .internal.list import List
from .internal.content import Content
from .internal.generator import Generator
from .internal.path import Path
from .internal.label import Label
from .internal.argument import Argument
from .internal.argument_list import ArgumentList
from .internal.native import Native
from .internal.native_list import NativeList
from .internal.exception import Exception
from .internal.exception_list import ExceptionList
from .internal.package import Package
from .internal.package_list import PackageList
from .internal.module import Module
from .internal.module_list import ModuleList
from .internal.definition import Definition
from .internal.definition_list import DefinitionList
from .internal.link import Link
from .internal.link_list import LinkList
from .internal.exporter import Export
from .internal.export_list import ExportList
from .internal.importer import Import
from .internal.import_list import ImportList
from .internal.build_instruction import BuildInstruction
from .internal.pre_build_instruction import PreBuildInstruction
from .internal.post_build_instruction import PostBuildInstruction
from .internal.project import Project

from .internal.utilities import *

class Target(Build):
  def __init__(self, label = None, subpath = None, definitions = None, links = None, imports = None, exports = None, generator = None, pre = None, post = None, arguments = None, packages = None, modules = None, exceptions = None, natives = None, linkage = None):
    super(Target, self).__init__()
    self.label = None
    self.subpath = None
    self.importsContent = {}
    self.exportsContent = {}
    if (type(label) == Label):
      self.label = label
    self.definitions = None
    if (type(definitions) == DefinitionList):
      self.definitions = definitions
    self.links = None
    if (type(links) == LinkList):
      self.links = links
    self.imports = None
    if (type(imports) == ImportList):
      self.imports = imports
    self.exports = None
    if (type(exports) == ExportList):
      self.exports = exports
    self.generator = None
    if (type(generator) == Generator):
      self.generator = generator
    self.pre = None
    if (type(pre) == PreBuildInstruction):
      self.pre = pre
    self.post = None
    if (type(post) == PostBuildInstruction):
      self.post = post
    self.arguments = None
    if (type(arguments) == ArgumentList):
      self.arguments = arguments
    self.packages = None
    if (type(packages) == PackageList):
      self.packages = packages
    self.modules = None
    if (type(modules) == ModuleList):
      self.modules = modules
    self.exceptions = None
    if (type(exceptions) == ExceptionList):
      self.exceptions = exceptions
    self.natives = None
    if (type(natives) == NativeList):
      self.natives = natives
    self.linkage = None
    if (type(linkage) == String):
      self.linkage = linkage
      
  def install(self, owner, path, installation, variant, natives):
    result = cmake_install(path, variant, installation, natives)
    owner.getContext().log(self.node, result)
    return True
    
  def build(self, owner, variant):
    context = owner.owner.getContext()
    installation = self.getPath(owner.owner, variant, "install")
    subpath = self.getPath(owner.owner, variant, None)
    path = self.getPath(owner.owner, variant, "build")
    success = True
    if not (self.imports == None):
      success = self.imports.doImport(self, variant)
    if not (success):
      context.log(self.node, "Import failure!")
      return False
    if not (self.exports == None):
      success = self.exports.doExport(self, variant)
    if not (success):
      context.log(self.node, "Export failure!")
      return False
    success = super(Target, self).build(owner.owner, variant)
    if not (success):
      context.log(self.node, "Super build failure!")
      return False
    links = []
    builds = []
    labels = {}
    imports = {}
    exports = {}
    includes = []
    linkages = []
    project = []
    packages = []
    definitions = []
    modules = []
    arguments = []
    generator = None
    architecture = None
    if (self.generator == None):
      generator = self.getGenerator(owner)
    else:
      generator = self.generator.getContent().strip()
      if not (self.generator.architecture == None):
        architecture = self.generator.architecture.getContent().strip()
    for i in range(len(owner.getDependencies().getContent())):
      dependency = owner.getDependencies().getContent()[i]
      if not (dependency == self):
        builds.append(dependency)
    for i in range(len(owner.getTargets().getContent())):
      target = owner.getTargets().getContent()[i]
      if not (target == self):
        builds.append(target)
    for i in range(len(builds)):
      if not ("Executable" in str(type(builds[i]))):
        label = builds[i].label.getContent()
        labels[label] = builds[i]
      else:
        builds[i] = None
    for label in labels:
      if not (self.imports == None):
        for i in range(len(self.imports.content)):
          if (label == self.imports.content[i].getContent()):
            if not (label in imports):
              if ("Target" in str(type(labels[label]))):
                linkages = linkages+labels[label].getLinkages(owner, variant)
                includes = includes+labels[label].getIncludes(owner)
              imports[label] = []
              if not (labels[label].exports == None):
                for j in range(len(labels[label].exports.content)):
                  export = labels[label].exports.content[j]
                  imports[label].append(export)
    for label in imports:
      for i in range(len(imports[label])):
        export = imports[label][i]
        key = export.key.getContent()
        value = export.value.getContent()
        if not (key in exports):
          exports[key] = [value, export.export.getContent()]
    if not (self.pre == None):
      if not (self.pre.timing == None):
        if not (self.pre.timing.getContent() == "build"):
          success = False
      if (success):
        success = self.pre.build(owner, subpath, path, installation, imports, variant)
      else:
        success = True
    if not (success):
      context.log(self.node, "Pre build step failure!")
      return False
    if not (os.path.isdir(path)):
      if (contains(wd(), path)):
        os.makedirs(path)
    if not (self.packages == None):
      packages = packages+self.packages.content
    if not (self.modules == None):
      modules = modules+self.modules.content
    if not (self.definitions == None):
      definitions = definitions+self.definitions.getContent()
    if not (self.arguments == None):
      arguments = arguments+self.arguments.getContent()
    project = unique(project+self.getFiles(owner))
    includes = unique(includes+self.getIncludes(owner))
    files = self.getFiles(owner, "CMakeLists\\.txt")
    temp = "."
    if not (self.subpath == None):
      temp = self.subpath.getContent()
    if not (os.path.realpath(os.path.join(self.getPath(owner, None, None), temp, "CMakeLists.txt")).replace("\\", "/") in files):
      descriptor = open(os.path.join(path, "CMakeLists.txt"), "w")
      base = path
      write(descriptor, "cmake_minimum_required(VERSION 3.12.0 FATAL_ERROR)")
      if not (context == None):
        if not (context.project == None):
          if not (context.project.cmake_modules == None):
            if not (context.project.directory == None):
              cmake_modules = os.path.join(wd(), context.root.directory.getContent(), context.project.directory.getContent(), context.project.cmake_modules.getContent()).replace("\\", "/")
              if (os.path.isdir(cmake_modules)):
                if (contains(wd(), cmake_modules)):
                  cmake_modules = "${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, cmake_modules).replace("\\", "/")
                else:
                  cmake_modules = cmake_modules.replace("\\", "/")
                write(descriptor, "set(CMAKE_MODULE_PATH \""+cmake_modules+"\")")
      write(descriptor, "project(\""+self.label.getContent()+"Project\")")
      write(descriptor, "set(BUILDSTER_HEADERS )")
      write(descriptor, "set(BUILDSTER_FILES )")
      for i in range(len(arguments)):
        argument = arguments[i]
        if (len(argument) > 2):
          if (argument[:2] == "-D"):
            argument = argument[2:].split("=")
            if (len(argument) > 1):
              key = argument[0]
              value = ""
              argument = argument[1:]
              for j in range(len(argument)):
                value += argument[j]
              write(descriptor, "set("+key+" "+value+")")
      for i in range(len(modules)):
        module = modules[i]
        if (module == None):
          continue
        if not (module.exports == None):
          for j in range(len(module.exports.content)):
            export = module.exports.content[j]
            if (export == None):
              continue
            if (export.key == None):
              continue
            if (len(export.key.getContent()) == 0):
              continue
            write(descriptor, "set("+export.key.getContent()+" )")
        if (os.path.isfile(module.getContent().strip())):
          if (contains(wd(), module.getContent().strip())):
            write(descriptor, "include(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, module.getContent().strip()).replace("\\", "/")+"\")")
          else:
            write(descriptor, "include(\""+module.getContent().strip().replace("\\", "/")+"\")")
        else:
          write(descriptor, "include("+module.getContent().strip()+")")
        if not (module.exports == None):
          for j in range(len(module.exports.content)):
            export = module.exports.content[j]
            if (export == None):
              continue
            if (export.export == None):
              continue
            if (export.key == None):
              continue
            if (export.export.getContent() == "headers"):
              if not (export.value == None):
                if not (len(export.value.getContent().strip()) == 0):
                  if (os.path.isdir(export.value.getContent().strip())):
                    if (contains(wd(), export.value.getContent().strip())):
                      write(descriptor, "include_directories(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, export.value.getContent().strip()).replace("\\", "/")+"\")")
                    else:
                      write(descriptor, "include_directories(\""+export.value.getContent().strip().replace("\\", "/")+"\")")
                  else:
                    write(descriptor, "include_directories("+export.value.getContent().strip()+")")
                else:
                  write(descriptor, "include_directories(${"+export.key.getContent()+"})")
              else:
                write(descriptor, "include_directories(${"+export.key.getContent()+"})")
            elif (export.export.getContent() == "libraries"):
              if not (export.value == None):
                if not (len(export.value.getContent().strip()) == 0):
                  if (os.path.isdir(export.value.getContent().strip())):
                    if (contains(wd(), export.value.getContent().strip())):
                      write(descriptor, "link_libraries(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, export.value.getContent().strip()).replace("\\", "/")+"\")")
                    else:
                      write(descriptor, "link_libraries(\""+export.value.getContent().strip().replace("\\", "/")+"\")")
                  else:
                    write(descriptor, "link_libraries("+export.value.getContent().strip()+")")
                else:
                  write(descriptor, "link_libraries(${"+export.key.getContent()+"})")
              else:
                write(descriptor, "link_libraries(${"+export.key.getContent()+"})")
            elif (export.export.getContent() == "files"):
              write(descriptor, "list(APPEND BUILDSTER_FILES ${"+export.key.getContent()+"})")
            else:
              pass
      for i in range(len(definitions)):
        definition = definitions[i]
        write(descriptor, "add_definitions(-D"+definition+")")
      for i in range(len(includes)):
        include = includes[i]
        if (contains(wd(), include)):
          write(descriptor, "include_directories(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, include.replace("\\", "/"))+"\")")
        else:
          write(descriptor, "include_directories(\""+include.replace("\\", "/")+"\")")
      for export in exports:
        if (exports[export][1] == "headers"):
          headers = exports[export][0].replace("\\", "/")
          if not (os.path.isdir(headers)):
            if (contains(wd(), headers)):
              try:
                os.makedirs(headers)
              except:
                pass
          if (contains(wd(), headers)):
            write(descriptor, "include_directories(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, headers.replace("\\", "/"))+"\")")
          else:
            write(descriptor, "include_directories(\""+headers.replace("\\", "/")+"\")")
        elif (exports[export][1] == "libraries"):
          libraries = exports[export][0].replace("\\", "/")
          if not (os.path.isdir(libraries)):
            if (contains(wd(), libraries)):
              try:
                os.makedirs(libraries)
              except:
                pass
          for root, folders, files in os.walk(libraries):
            for name in files:
              for i in range(len(owner.getContext().libraries)):
                if (name.endswith("."+owner.getContext().libraries[i])):
                  links.append(str(root).replace("\\", "/"))
                  if (contains(wd(), links[len(links)-1])):
                    write(descriptor, "link_directories(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, links[len(links)-1])+"\")")
                  else:
                    write(descriptor, "link_directories(\""+links[len(links)-1]+"\")")
                  name = None
                  break
              if (name == None):
                break
        else:
          pass
      for i in range(len(linkages)):
        linkage = linkages[i]
        links.append(linkage.replace("\\", "/"))
        if (contains(wd(), links[len(links)-1])):
          write(descriptor, "link_directories(\"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, links[len(links)-1])+"\")")
        else:
          write(descriptor, "link_directories(\""+links[len(links)-1]+"\")")
      if not (self.links == None):
        for i in range(len(self.links.content)):
          link = self.links.content[i].getContent().strip()
          linkage = self.links.content[i].linkage
          if not (linkage == None):
            linkage = linkage.getContent().strip()
          if ("*" in link):
            for j in range(len(links)):
              for root, folders, files in os.walk(links[j]):
                for name in files:
                  if (fnmatch.fnmatch(name, link)):
                    for k in range(len(owner.getContext().libraries)):
                      if ("visual studio" in str(generator).lower()):
                        if not ((owner.getContext().libraries[k] == "dll") or (owner.getContext().libraries[k] == "lib")):
                          continue
                      if not (linkage == None):
                        if (linkage == "static"):
                          if not (owner.getContext().libraries[k] in owner.getContext().statics):
                            continue
                        else:
                          if (linkage == "shared"):
                            if not (owner.getContext().libraries[k] in owner.getContext().shares):
                              continue
                      if (name.endswith("."+owner.getContext().libraries[k])):
                        write(descriptor, "link_libraries(\""+name+"\")")
                        break
          else:
            write(descriptor, "link_libraries("+link+")")
      if (platform.system() == "Linux"):
        write(descriptor, "find_package(PkgConfig REQUIRED)")
      for i in range(len(packages)):
        package = packages[i]
        if (package == None):
          continue
        hints = None
        variables = None
        components = None
        if not (package.components == None):
          components = ""
          for j in range(len(package.components.content)):
            component = package.components.content[j]
            if (component == None):
              continue
            component = component.getContent()
            if (len(component.strip()) == 0):
              continue
            components += component
            components += " "
          if (len(components.strip()) == 0):
            components = None
        if not (package.hints == None):
          hints = ""
          for j in range(len(package.hints.content)):
            if (j+1 < len(package.hints.content)):
              hints += " "
            hint = package.hints.content[j]
            if (hint == None):
              continue
            hint = hint.getContent()
            if (len(hint.strip()) == 0):
              continue
            hints += hint
          if (len(hints.strip()) == 0):
            hints = None
        if not (package.variables == None):
          variables = []
          for j in range(len(package.variables.content)):
            variable = package.variables.content[j]
            if (variable == None):
              continue
            if ((variable.key == None) or (variable.value == None)):
              continue
            variable = "set("+variable.key.getContent()+" "+variable.value.getContent()+")"
            variables.append(variable)
          if (len(variables) == 0):
            variables = None
        if (hints == None):
          if (components == None):
            write(descriptor, "find_package("+package.getContent()+" REQUIRED)")
          else:
            write(descriptor, "find_package("+package.getContent()+" COMPONENTS "+components.strip()+" REQUIRED)")
        else:
          write(descriptor, "pkg_search_module("+package.getContent()+" REQUIRED "+hints+")")
        if not (variables == None):
          for variable in variables:
            write(descriptor, variable)
        if not (package.exports == None):
          for j in range(len(package.exports.content)):
            export = package.exports.content[j]
            if (export == None):
              continue
            if (export.export == None):
              continue
            if (export.key == None):
              continue
            if (export.export.getContent() == "headers"):
              write(descriptor, "include_directories(${"+export.key.getContent()+"})")
            elif (export.export.getContent() == "libraries"):
              write(descriptor, "link_libraries(${"+export.key.getContent()+"})")
            else:
              pass
      if (platform.system() == "Linux"):
        write(descriptor, "find_package(Threads REQUIRED)")
        write(descriptor, "link_libraries(${CMAKE_THREAD_LIBS_INIT})")
      if (len(project) > 0):
        target = str(type(self))
        for i in range(len(project)):
          if not (self.exceptions == None):
            for j in range(len(self.exceptions.content)):
              exception = self.exceptions.content[j].getContent().strip()
              if ("*" in exception):
                if (fnmatch.fnmatch(os.path.basename(project[i]), exception)):
                  project[i] = None
                  break
              else:
                if not (os.path.exists(exception)):
                  continue
                if not (contains(self.getPath(owner, None, None), exception)):
                  continue
                left = relativize(base, exception.replace("\\", "/"))
                right = relativize(base, project[i].replace("\\", "/"))
                if (left == right):
                  project[i] = None
                  break
          if (project[i] == None):
            continue
          for j in range(len(owner.getContext().extensions)):
            extension = "."+owner.getContext().extensions[j]
            if (project[i].endswith(extension)):
              write(descriptor, "list(APPEND BUILDSTER_FILES \"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, project[i].replace("\\", "/"))+"\")")
              if ("Library" in target):
                for k in range(len(owner.getContext().headers)):
                  if (extension == "."+owner.getContext().headers[k]):
                    write(descriptor, "list(APPEND BUILDSTER_HEADERS \"${CMAKE_CURRENT_LIST_DIR}/"+relativize(base, project[i].replace("\\", "/"))+"\")")
                    break
              break
        if ("Executable" in target):
          write(descriptor, "add_executable("+self.label.getContent()+" ${BUILDSTER_FILES})")
          if (platform.system() == "Darwin"):
            write(descriptor, "add_custom_command(TARGET "+self.label.getContent()+" POST_BUILD COMMAND ${CMAKE_INSTALL_NAME_TOOL} -add_rpath \"@executable_path/\" $<TARGET_FILE:"+self.label.getContent()+"> || :)")
          write(descriptor, "target_compile_features("+self.label.getContent()+" PRIVATE cxx_std_"+context.root.cpp.getContent()+")")
        elif ("Library" in target):
          if (self.linkage == None):
            write(descriptor, "add_library("+self.label.getContent()+" ${BUILDSTER_FILES})")
          else:
            write(descriptor, "add_library("+self.label.getContent()+" "+self.linkage.getContent().upper()+" "+"${BUILDSTER_FILES})")
          write(descriptor, "set_target_properties("+self.label.getContent()+" PROPERTIES PUBLIC_HEADER \"${BUILDSTER_HEADERS}\")")
          write(descriptor, "target_compile_features("+self.label.getContent()+" PRIVATE cxx_std_"+context.root.cpp.getContent()+")")
        else:
          pass
        write(descriptor, "install(TARGETS "+self.label.getContent()+")")
      else:
        context.log(self.node, "Source failure!")
        return False
      descriptor.close()
    else:
      path = self.getPath(owner, variant, None)
    if (generator == None):
      context.log(self.node, "Generator failure!")
      return False
    exports = owner.getExports(self.importsContent, variant, [self])
    if (variant in self.importsContent):
      for i in range(len(exports)):
        export = exports[i]
        if (export[0] in self.importsContent[variant]):
          export = export[1]
          for key in export:
            if (export[key][0] == "other"):
              arguments.append("-D"+key+"=\""+export[key][1].replace("\\", "/")+"\"")
            else:
              arguments.append("-D"+key+"="+export[key][1].replace("\\", "/"))
    success = self.buildVariant(owner, generator, architecture, arguments, path, installation, variant)
    if not (success):
      context.log(self.node, "Build failure!")
      return False
    if not (self.post == None):
      if not (self.post.timing == None):
        if not (self.post.timing.getContent() == "build"):
          success = False
      if (success):
        success = self.post.build(owner, subpath, path, installation, imports, variant)
      else:
        success = True
    if not (success):
      context.log(self.node, "Post build step failure!")
      return False
    return True

  def buildVariant(self, owner, generator, architecture, arguments, path, installation, variant):
    natives = None
    if not (self.natives == None):
      natives = self.natives.getContent()
      for i in range(len(natives)):
        natives[i] = natives[i].strip()
        if (len(natives[i]) == 0):
          natives[i] = None
      while (None in natives):
        natives.remove(None)
    files = self.getFiles(owner, "CMakeLists\\.txt")
    temp = ""
    subpath = "."
    if not (self.subpath == None):
      subpath = self.subpath.getContent()
    if not (os.path.realpath(os.path.join(self.getPath(owner, None, None), subpath, "CMakeLists.txt")).replace("\\", "/") in files):
      temp += os.path.realpath(os.path.join(path, "build")).replace("\\", "/")
    else:
      temp += os.path.realpath(os.path.join(path, "build", variant.lower())).replace("\\", "/")
    result = cmake_configure(generator, architecture, arguments+["-DCMAKE_BUILD_TYPE="+variant], os.path.realpath(os.path.join(path, subpath)).replace("\\", "/"), temp, installation, None)
    owner.getContext().log(self.node, result)
    result = cmake_build(temp, variant, natives)
    owner.getContext().log(self.node, result)
    success = self.install(owner, temp, installation.replace("\\", "/"), variant, natives)
    return success
    
  def distribute(self, owner, distribution, variant):
    target = str(type(self))
    prefixes = [""]
    if ("Library" in target):
      prefixes = prefixes+["lib"]
    installation = find(os.path.join(self.getPath(owner, variant, "install")).replace("\\", "/"), self.label.getContent(), prefixes)
    if (installation == None):
      return False
    source = installation.replace("\\", "/")
    destination = os.path.join(distribution, variant.lower(), os.path.basename(installation)).replace("\\", "/")
    if not (self.move(source, destination)):
      return False
    if not (platform.system() == "Linux"):
      return True
    success = True
    if ("Executable" in target):
      if (os.path.exists(destination)):
        if (os.path.isfile(destination)):
          patcher = None
          try:
            patcher = importlib.import_module("pypatchelf")
          except:
            patcher = None
          if not (patcher == None):
            try:
              command = []
              command.append(patcher.PATCHELF)
              command.append("--set-rpath")
              command.append("$ORIGIN")
              command.append(destination)
              result = execute_command(command)
              #owner.getContext().log(self.node, result)
              success = True
            except:
              success = False
          else:
            success = False
    return success

  def doExport(self, key, value, export, variant, exceptions):
    if not (variant in self.exportsContent):
      self.exportsContent[variant] = {}
    if (key in self.exportsContent[variant]):
      return False
    self.exportsContent[variant][key] = [export, value, exceptions]
    return True
    
  def doImport(self, label, variant):
    if not (variant in self.importsContent):
      self.importsContent[variant] = []
    if (label in self.importsContent[variant]):
      return False
    self.importsContent[variant].append(label)
    return True
    
  def getExports(self, variant, need):
    if not (variant in self.exportsContent):
      self.exportsContent[variant] = {}
    exportsContent = self.filterExports(self.exportsContent[variant], need)
    return exportsContent
    
  def getPath(self, owner, variant, purpose):
    if (purpose == None):
      return adjust(os.path.join(wd(), owner.getContext().root.directory.getContent(), owner.directory.getContent(), self.label.getContent()))
    if (variant == None):
      return adjust(os.path.join(wd(), owner.getContext().root.directory.getContent(), owner.directory.getContent(), purpose, "targets", self.label.getContent()))
    return adjust(os.path.join(wd(), owner.getContext().root.directory.getContent(), owner.directory.getContent(), purpose, "targets", self.label.getContent(), variant.lower()))
    
  def getLabel(self):
    return self.label.getContent()
    
  def getFiles(self, owner, pattern = None):
    result = []
    path = self.getPath(owner, None, None)
    for root, folders, files in os.walk(path):
      for name in files:
        if not (pattern == None):
          match = re.search(pattern, name)
          if (match == None):
            continue
          if not (match.group() == name):
            continue
        result.append(os.path.realpath(os.path.join(root, name)).replace("\\", "/"))
    return result

  def getIncludes(self, owner):
    result = []
    path = self.getPath(owner, None, None)
    for root, folders, files in os.walk(path):
      result.append(root)
    return result
    
  def getLinkages(self, owner, variant):
    result = []
    path = self.getPath(owner, variant, "install")
    for root, folders, files in os.walk(path):
      result.append(root)
    return result
    
