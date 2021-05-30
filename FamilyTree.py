import sys
import xml.etree.ElementTree as ET 
from   enum import Enum
from   CLI import CLI
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

class FamilyTree:
    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self, sPeopleFile):
 
        self.family = Family()

        if len(sPeopleFile.strip()) > 0:
            self.sPeopleFile = sPeopleFile
            print("Loading file '%s'..." % self.sPeopleFile)
            self.loadFile()

            self.getInput()

        return

    # end def __init__()

    # ------------------------------------------------------------
    # Gets user-input from the command-line
    # ------------------------------------------------------------
    def getInput(self):

        cli = CLI(self.family)
        cli.cmdloop()

        return

    # end def getInput()

    # ------------------------------------------------------------
    # Loads people from XML data file
    # ------------------------------------------------------------
    def loadFile(self):

        try:
            pplTree = ET.parse(self.sPeopleFile)
            pplRoot = pplTree.getroot()
            personList = pplRoot.getchildren()
            for person in personList:
                self.processPerson(person)

        except FileNotFoundError:
            print("loadFile - file '%s' not found" % self.sPeopleFile)
        except ET.ParseError as excParsing:
            print("loadFile - error parsing file '%s'" % self.sPeopleFile)
        except Exception as excUnhandled:
            print("loadFile - unhandled exception parsing file '%s'" % self.sPeopleFile)
            print(excUnhandled)

        return

    # end def loadFile()

    # ------------------------------------------------------------
    # Processes person from XML
    # ------------------------------------------------------------
    def processPerson(self, personXML):
        if personXML.tag == "person":
            sPersonKey = self.family.addPerson(personXML.attrib)
            if sPersonKey != None:
                infoList = personXML.getchildren()
                if len(infoList) > 0:
                    self.processInfo(sPersonKey, infoList)

        return

    # end def processPerson()

    # ------------------------------------------------------------
    # Processes parents for a person
    # ------------------------------------------------------------
    def processInfo(self, sPersonKey, infoList):

        for infoItem in infoList:
            if infoItem.tag == "father":
                sFatherFirst = ""
                if "first" in infoItem.attrib:
                    sFatherFirst = infoItem.attrib["first"]
                sFatherLast = ""
                if "last" in infoItem.attrib:
                    sFatherLast = infoItem.attrib["last"]

                sFatherKey = self.family.makePersonKey(sFatherFirst, sFatherLast)
                if (sFatherKey != None) and (not sFatherKey in self.family.dctPeople):
                    dctFatherInfo = dict()
                    dctFatherInfo["first"]  = sFatherFirst
                    dctFatherInfo["last"]   = sFatherLast
                    dctFatherInfo["gender"] = "M"
                    self.family.addPerson(dctFatherInfo)
            elif infoItem.tag == "mother":
                sMotherFirst = ""
                if "first" in infoItem.attrib:
                    sMotherFirst = infoItem.attrib["first"]
                sMotherLast = ""
                if "last" in infoItem.attrib:
                    sMotherLast = infoItem.attrib["last"]

                sMotherKey = self.family.makePersonKey(sMotherFirst, sMotherLast)
                if (sMotherKey != None) and (not sMotherKey in self.family.dctPeople):
                    dctMotherInfo = dict()
                    dctMotherInfo["first"]  = sMotherFirst
                    dctMotherInfo["last"]   = sMotherLast
                    dctMotherInfo["gender"] = "F"
                    self.family.addPerson(dctMotherInfo)
            else:
                print("Error, skipping unrecognized tag:" + infoItem.tag)

        # end for parent in parentList

        # ------------------------------------------------
        # Set/update parents in Person instance, add child
        # ------------------------------------------------
        if (sFatherKey != None) and (sMotherKey != None):
            try:
                person = self.family.dctPeople[sPersonKey]
                person.setParents(sFatherKey, sMotherKey)

                sParentsKey = self.family.makeParentsKey(sFatherKey, sMotherKey)
                if sParentsKey != None:
                    try:
                        lstChildren = self.family.dctParentages[sParentsKey]
                    except KeyError:
                        lstChildren = list()
                        self.family.dctParentages[sParentsKey] = lstChildren           

                    lstChildren.append(sPersonKey)
            except KeyError as noPerson:
                print ("Failed to find person to add parents for (key: %s)" % sPersonKey)
                print (noPerson)

            # -----------------------------------------
            # Set partner relationships between parents
            # -----------------------------------------
            try:
                self.family.dctPeople[sFatherKey].setPartner (sMotherKey)
            except KeyError:
                print ("Failed to update partner key for father (first: %s, last: %s)" % sFatherFirst, sFatherLast)

            try:
                self.family.dctPeople[sMotherKey].setPartner (sFatherKey)
            except KeyError:
                print ("Failed to update partner key for mother (first: %s, last: %s)" % sMotherFirst, sMotherLast)

        # end if (sFatherKey != None) and (sMotherKey != None)

        return sParentsKey

    # end def addParents()


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
        # Create Family-tree instance; pass it the people file-name
        #
        familyTree = FamilyTree(sPeopleFile)

    except KeyboardInterrupt:
        print("Thank you for climbing down the tree")
    except Exception as excError:
        print("Unexpected or unhandled exception")
        print(excError)

# end if __name__ == "__main__"
