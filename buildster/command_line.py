import sys
import buildster
import subprocess

def main():
    arguments = sys.argv
    command = []
    if (len(arguments) > 1):
        arguments = arguments[1:]
        for i in range(len(arguments)):
            argument = arguments[i]
            arguments[i] = "arguments.append(\""+argument+"\")"
        if (len(arguments) > 1):
            arguments = "; ".join(arguments)
        else:
            arguments = arguments[0]+"; "
        command.append(sys.executable)
        command.append("-c")
        command.append("import sys; import buildster; arguments = []; "+arguments+"sys.argv += arguments; print(str(sys.argv)); buildster.main()")
        print(str(command))
        result = subprocess.check_output(command, stderr=subprocess.STDOUT)
        print(result.decode())
    else:
        buildster.main()
    return 0
