import sys
from   enum import Enum
from   Family import Family
from   Utils import *


# ############################################################
# MAIN ROUTINE
# -------------------------------------------------------------
# Usage:
#   python3 FamilyTree <people.xml>
#   where: 
#       people.xml = file containing details of people in XML format:
#       <people>
#           <person first="first-name" last="last-name" gender="M|F" birthymd="YYYYMMDD">
#               <mother first="mothers-first" last="mothers-last" />
#               <father first="fathers-first" last="fathers-last" />
#               <birthplace city="city-name" state="state-name" country="country-name" postcode="postcode" />
#           </person>
#           ...
#           <person>
#               ...
#           </person>
#           ...
#       </people>
#

if __name__ == "__main__":
    #
    # Initialize file-names
    #
    sPeopleFile = None

    #
    # Process command-line arguments
    #
    if len(sys.argv) == 2:
        sPeopleFile = sys.argv[1]

    else:
        print("Usage: python3 %s <people.xml>" % sys.argv[0])
        pause ("Press return to end")
        sys.exit ()

    try:
        #
        # Create Family instance; pass it the people file-name
        #
        family = Family(sPeopleFile)

        #
        # Command-line processing
        #
        family.processInput()
    except KeyboardInterrupt:
        print("Thank you for climbing down the tree")
    except Exception as excError:
        print("Unexpected or unhandled exception")
        print(excError)

# end if __name__ == "__main__"
