import sys
from typing import List, Optional

__version__ = "1.0.0"

def main(args: Optional[List[str]] = None) -> int:
    if (len(sys.argv) > 1):
        if (sys.argv[0] == "-c"):
            return 0
    from buildster.command_line import main as _main
    return _main()
