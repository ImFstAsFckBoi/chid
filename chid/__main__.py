from sys import argv
from chid import main

def bootstrap():
    if len(argv) == 1:
        return main('')
    elif len(argv) == 2:
        return main(argv[1])
    else:
        return main(argv[1], *argv[2:])

if __name__ == "__main__":
    exit(bootstrap())
