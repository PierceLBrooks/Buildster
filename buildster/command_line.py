import os
import sys
import shlex
import logging
import traceback
import subprocess
from buildster import buildster

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
        command.append("import sys; from buildster import buildster; arguments = []; "+arguments+"; sys.argv += arguments; print(str(sys.argv)); buildster.main()")
        print(str(command))
        result = ""
        try:
            result = subprocess.check_output(command, env=environment, stderr=subprocess.STDOUT)
            result = result.decode("UTF-8")
        except Exception as exception:
            result = ""
            logging.error(traceback.format_exc())
        print(result.strip())
    else:
        print(str(buildster.main(environment)))
    return 0
