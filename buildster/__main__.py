import os
import sys
import warnings

# Remove '' and current working directory from the first entry
# of sys.path, if present to avoid using current directory
if sys.path[0] in ("", os.getcwd()):
    sys.path.pop(0)

# If we are running from a wheel, add the wheel to sys.path
if __package__ == "":
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

if __name__ == "__main__":
    from buildster.command_line import main as _main
    result = _main()
    print(str(result))
    sys.exit(result)
