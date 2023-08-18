import sys
import time
import hotswap
import coloredlogs
from b import function


@hotswap.main
def main():
    sys.stdout.reconfigure(encoding="utf-8")
    coloredlogs.install(level="DEBUG")
    while True:
        function()
        time.sleep(1)


if __name__ == "__main__":
    main()
