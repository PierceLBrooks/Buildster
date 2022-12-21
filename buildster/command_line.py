import os
import sys
import shlex
import logging
import traceback
from buildster import buildster as build

def main():
    environment = os.environ.copy()
    arguments = sys.argv
    command = []
    environment["BUILDSTER_WD"] = os.getcwd()
    if (len(arguments) > 1):
        arguments = arguments[1:]
        for i in range(len(arguments)):
            argument = arguments[i]
            arguments[i] = "arguments.append(\""+shlex.quote(argument)+"\")"
        if (len(arguments) > 1):
            arguments = "; ".join(arguments)
        else:
            arguments = arguments[0]
        command.append(sys.executable)
        command.append("-c")
        command.append("import sys; from buildster import buildster as build; arguments = []; "+arguments+"; sys.argv += arguments; print(str(sys.argv)); build.main()")
        print(str(command))
        result = ""
        try:
            result = build.execute_command(command, environment)
        except Exception as exception:
            result = ""
            logging.error(traceback.format_exc())
        #print(result.strip())
    else:
        print(str(build.main(environment)))
    return 0
