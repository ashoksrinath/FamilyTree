import os
import sys
import threading

from   CLI import CLI
from   Family import Family
from   Utils import *


# ############################################################
# MAIN ROUTINE
# -------------------------------------------------------------
# Usage:
#   python3 FamilyTree.py
#   where: 
#

class FamilyTree:
    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self):
 
        self.family = Family()

        return

    # end def __init__()

    # ------------------------------------------------------------
    # Gets and processes input from the command-line
    # ------------------------------------------------------------
    def cmdProcessor(self):

        cli = CLI(self.family)
        cli.cmdloop()

        return

    # end def cmdProcessor()

    # ------------------------------------------------------------
    # Gets and processes input from socket connections
    # ------------------------------------------------------------
    def sockProcessor(self, nServerPort):

        self.sockit = Sockit(host="localhost", port=nServerPort)

        return

    # end def sockProcessor()

# end class FamilyTree ########################################


if __name__ == "__main__":
    #
    # Initialize port number
    #
    nServerPort = None

    def print_n_sprint(sAppName):
        print("Usage: python3 %s [server-port]" % sAppName)
        print("       runs interactively on the command-line unless server-port is specified, in which case it")
        print("       runs in the background, accepting connections on server-port.  The server receives commands")
        print("       per the CLI syntax on these connections, and returns responses as formatted strings.")
        pause ("Press return to end")
        sys.exit ()


    #
    # Process command-line arguments
    #
    if len(sys.argv) <= 2:
        if len(sys.argv) == 2:
            try:
                nServerPort = int(sys.argv[1])
            except ValueError:
                print_n_sprint(sys.argv[0])
    else:
        print_n_sprint(sys.argv[0])

    try:
        #
        # Create Family-tree instance
        #
        familyTree = FamilyTree()
        if nServerPort == None:
            familyTree.cmdProcessor()
        else:
            familyTree.sockProcessor(nServerPort)

    except KeyboardInterrupt:
        print("Thank you for climbing down the tree")
    except Exception as excError:
        print("Unexpected or unhandled exception")
        print(excError)

# end if __name__ == "__main__"
