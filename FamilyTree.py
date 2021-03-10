import sys
from   enum import Enum
from   Family import Family
from   Utils import *


# ############################################################
# MAIN ROUTINE
# -------------------------------------------------------------
# Usage:
#   python3 FamilyTree <people.xml> <parentages.xml> 
#   where: 
#       people.xml = file containing details of people in XML format:
#       <people>
#           <person first="unknown" last="unknown" gender="unknown" birthymd="unknown">
#               <birthcity>"unknown"</birthcity>
#               <birthstate>"unknown"</birthstate>
#               <birthcountry>"unknown"</birthcountry>
#               <birthpostcode>"unknown"</birthpostcode>
#           </person>
#           ...
#           <person>
#               ...
#           </person>
#           ...
#       </people>
#   and:
#       parentages.xml = file containing details of parentages in XML format:
#       <parentages>
#           <parentage fathersfirst="first" fatherslast="last" mothersfirst="first" motherslast="last">
#               <child>
#                   <first>"Unknown"</first>
#                   <last>"Unknown"</last>
#               </child>
#           </parentage>
#           ...
#           <parentage fathersfirst="first" fatherslast="last" mothersfirst="first" motherslast="last">
#               ...
#           </parentage>
#           ...
#       <parentages>
#

if __name__ == "__main__":
    #
    # Initialize file-names
    #
    sPeopleFile = None
    sParentagesFile = None

    #
    # Process command-line arguments
    #
    if len(sys.argv) == 3:
        sPeopleFile = sys.argv[1]
        sParentagesFile = sys.argv[2]

    else:
        sUsage = "Usage: " + "python3 " + sys.argv[0] + " <people.xml> <parentages.xml>"
        print(sUsage)
        pause ("Press return to end")
        sys.exit ()

    try:
        #
        # Create Family instance; pass it the people and parentages file-names
        #
        family = Family(sPeopleFile, sParentagesFile)

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
