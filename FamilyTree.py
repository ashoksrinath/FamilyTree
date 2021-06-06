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
 
        self.family         = Family()
        self.lstParentRoots = list()

        if len(sPeopleFile.strip()) > 0:
            self.sPeopleFile = sPeopleFile
            self.loadFile()

        self.getInput()

        return

    # end def __init__()

    # ------------------------------------------------------------
    # Adds parents to the family tree display list
    # ------------------------------------------------------------
    def addToRoots(self, sPartnerKey1, sPartnerKey2):

        dbgPrint(INF_DBG, ("FamilyTree.addToRoots: partner keys: %s & %s" % (sPartnerKey1, sPartnerKey2)))

        sParentagesKey = self.family.makeParentageKey(sPartnerKey1, sPartnerKey2)
        if (sParentagesKey == None):
            dbgPrint(INF_DBG, ("FamilyTree.addToRoots: parentage key is None; returning"))
            return

        try:
            lstChildren = self.family.dctParentages[sParentagesKey]
            if len(lstChildren) == 0:
                dbgPrint(INF_DBG, ("FamilyTree.addToRoots: no children; returning"))
                return
        except KeyError:
            dbgPrint(INF_DBG, ("FamilyTree.addToRoots: no parentage entry for %s; returning" % sParentagesKey))
            return

        if not sParentagesKey in self.lstParentRoots:
            dbgPrint(INF_DBG, ("FamilyTree.addToRoots: adding %s" % sParentagesKey))
            self.lstParentRoots.append(sParentagesKey)
        else:
            dbgPrint(INF_DBG, ("FamilyTree.addToRoots: %s already added; returning" % sParentagesKey))
            return

        for sPersonKey in lstChildren:
            if self.family.dctPeople[sPersonKey].getGender() == "F":
                sPartnerKey = self.family.dctPeople[sPersonKey].getPartnerKey()
                if sPartnerKey != None:
                    self.addToRoots(sPersonKey, sPartnerKey)

    # end def addToTree()

    # ------------------------------------------------------------------------
    # Checks all entries for referential integrity, removes unknown references
    # ------------------------------------------------------------------------
    def fixData(self):

        # ------------------------------------------------------------
        # Remove partners, mothers and fathers who aren't in dctPeople
        # ------------------------------------------------------------
        for person in self.family.dctPeople.values():
            if person.sPartnerKey != None:
                if not person.sPartnerKey in self.family.dctPeople:
                    dbgPrint(INF_DBG, ("FamilyTree.fixData: removing unknown partner key '%s' for '%s %s'" %
                        (person.sPartnerKey, person.sFirstName, person.sLastName)))
                    person.sPartnerKey = None

            if person.sMothersKey != None:
                if not person.sMothersKey in self.family.dctPeople:
                    dbgPrint(INF_DBG, ("FamilyTree.fixData: removing unknown mother's key '%s' for '%s %s'") %
                        (person.sMothersKey, person.sFirstName, person.sLastName))
                    person.sMothersKey = None

            if person.sFathersKey != None:
                if not person.sFathersKey in self.family.dctPeople:
                    dbgPrint(INF_DBG, ("FamilyTree.fixData: removing unknown father's key '%s' for '%s %s'") %
                        (person.sFathersKey, person.sFirstName, person.sLastName))
                    person.sFathersKey = None

        # ---------------------------------------------------------------------
        # Remove children from dctParentages values if they aren't in dctPeople
        # ---------------------------------------------------------------------
        for sParentsKey, lstChildren in self.family.dctParentages.items():
            bListModified = False
            for nIdx in range(0, len(lstChildren)):
                if not lstChildren[nIdx] in self.family.dctPeople:
                    dbgPrint(INF_DBG, ("FamilyTree.fixData: removing unknown child '%s %s' for parent's key %s"))
                    lstChildren[nIdx] = None
                    bListModified = True

            if bListModified:
                self.family.dctParents[sParentsKey] = list()
                for nIdx in range(0, len(lstChildren)):
                    if lstChildren[nIdx] != None:
                        self.family.dctParents[sParentsKey].append(lstChildren[nIdx])

        return

    # end def fixData()

    # ------------------------------------------------------------
    # Gets user-input from the command-line
    # ------------------------------------------------------------
    def getInput(self):

        cli = CLI(self)
        cli.cmdloop()

        return

    # end def getInput()

    # ------------------------------------------------------------
    # Finds and returns a list of "roots" in the family tree
    # ------------------------------------------------------------
    def getRoots(self):

        lstRoots = list()
        for sPersonKey, person in self.family.dctPeople.items():
            if (person.sMothersKey == None) and (person.sFathersKey == None):
                lstRoots.append(sPersonKey)
                dbgPrint(INF_DBG, ("Family.getRoots: Found person '%s %s' with no parents" % (person.sFirstName, person.sLastName)))


        dbgPrint(INF_DBG, ("Family.getRoots: Returning %d roots" % len(lstRoots)))

        return lstRoots

    # end def getRoots()

    # ------------------------------------------------------------
    # Loads people from XML data file
    # ------------------------------------------------------------
    def loadFile(self):

        print("Loading file '%s'... " % self.sPeopleFile, end=' ')
        try:
            pplTree = ET.parse(self.sPeopleFile)
            pplRoot = pplTree.getroot()
            personList = list(pplRoot)
            for personInfo in personList:
                self.processPerson(personInfo)

            print("done (%d people added)" % len(self.family.dctPeople))

        except FileNotFoundError:
            print("loadfile - file '%s' not found" % self.sPeopleFile)
        except ET.ParseError as excParsing:
            print("loadfile - error parsing file '%s'" % self.sPeopleFile)
        except Exception as excUnhandled:
            print("loadfile - unhandled exception", excUnhandled)

        return

    # end def loadFile()

    # ------------------------------------------------------------
    # Processes person from XML
    # ------------------------------------------------------------
    def processPerson(self, personXML):

        person      = None
        sMothersKey = None
        sFathersKey = None

        try:
            # --------------------
            # Add person to family
            # --------------------
            if personXML.tag == "person":
                sFirst = None
                if "first" in personXML.attrib:
                    sFirst =personXML.attrib["first"]

                sLast = None
                if "last" in personXML.attrib:
                    sLast = personXML.attrib["last"]

                sGender = None
                if "gender" in personXML.attrib:
                   sGender = personXML.attrib["gender"]

                sBirthYMD = None
                if "birthymd" in personXML.attrib:
                   sBirthYMD = personXML.attrib["birthymd"]

                sPersonKey = self.family.addPerson(sFirst, sLast, sGender, sBirthYMD)
                if sPersonKey == None:
                    return

                # ---------------------------------------
                # Process birthplace & parents for Person
                # ---------------------------------------
                person = self.family.dctPeople[sPersonKey]
                infoList = list(personXML)
                for infoItem in infoList:
                    if infoItem.tag == "birthplc":
                        self.process_birthplc(person, infoItem.attrib)

                    elif infoItem.tag == "father":
                        sFathersKey = self.process_father(person, infoItem.attrib)

                    elif infoItem.tag == "mother":
                        sMothersKey = self.process_mother(person, infoItem.attrib)

                    else:
                        dbgPrint(ERR_DBG, ("Error, skipping unrecognized tag: %s" % infoItem.tag))

                # end for infoItem in infoList

                # -----------------------------------------------------------------
                # Set parents for Person, set partner relationships between parents
                # -----------------------------------------------------------------
                person.setParentsKeys(sMothersKey, sFathersKey)
                self.family.dctPeople[sMothersKey].setPartnerKey(sFathersKey)
                self.family.dctPeople[sFathersKey].setPartnerKey(sMothersKey)

                # ---------------------------------
                # Create/update parentages register
                # ---------------------------------
                sParentsKey = self.family.makeParentageKey(sMothersKey, sFathersKey)
                if sParentsKey != None:
                    try:
                        lstChildren = self.family.dctParentages[sParentsKey]
                    except KeyError:
                        lstChildren = list()
                        self.family.dctParentages[sParentsKey] = lstChildren           

                    lstChildren.append(sPersonKey)

                # end if (person != None) and (MothersKey != None) and (sFathersKeys != None)

        except Exception as extinction:
            dbgPrint(ERR_DBG, ("processPerson - error processing: ", personXML.attrib))
            dbgPrint(ERR_DBG, ("processPerson - unhandled exception: ", extinction))

        return

    # end def processPerson()

    # ------------------------------------------------------------
    # Processes birth-place information for a person
    # ------------------------------------------------------------
    def process_birthplc(self, person, dctBirthPlc):

        sCity = None
        if "city" in dctBirthPlc:
            sCity = dctBirthPlc["city"]

        sState = None
        if "state" in dctBirthPlc:
            sState = dctBirthPlc["state"]

        sPostCode = None
        if "postcode" in dctBirthPlc:
            sPostCode = dctBirthPlc["postcode"]

        sCountry = None
        if "country" in dctBirthPlc:
            sCountry = dctBirthPlc["country"]

        person.setBirthPlace(sCity, sState, sCountry, sPostCode)

        return

    # end def process_birthplc()

    # ------------------------------------------------------------
    # Processes father's information for a person
    # ------------------------------------------------------------
    def process_father(self, person, dctPersonInfo):

        sFirst = None
        if "first" in dctPersonInfo:
            sFirst = dctPersonInfo["first"]

        sLast = None
        if "last" in dctPersonInfo:
            sLast = dctPersonInfo["last"]

        sGender = "M"
        sPersonKey = self.family.makePersonKey(sFirst, sLast)
        if (sPersonKey != None) and (not sPersonKey in self.family.dctPeople):
            self.family.addPerson(sFirst, sLast, sGender, None)

        return sPersonKey

    # end def process_father()

    # ------------------------------------------------------------
    # Processes mother's information for a person
    # ------------------------------------------------------------
    def process_mother(self, person, dctPersonInfo):

        sFirst = None
        if "first" in dctPersonInfo:
            sFirst = dctPersonInfo["first"]

        sLast = None
        if "last" in dctPersonInfo:
            sLast = dctPersonInfo["last"]

        sGender = "F"
        sPersonKey = self.family.makePersonKey(sFirst, sLast)
        if (sPersonKey != None) and (not sPersonKey in self.family.dctPeople):
            self.family.addPerson(sFirst, sLast, sGender, None)

        return sPersonKey

    # end def process_mother()

    # ------------------------------------------------------------
    # Saves people data to file in XML format
    # ------------------------------------------------------------
    def saveFile(self, sXMLfileName):

        # ---------------------------------------
        # Ensure that we have an output file-name
        # ---------------------------------------
        sOutputFilename = None
        if (sXMLfileName != None):
            sOutputFilename = sXMLfileName
        else:
            sOutputFilename = self.sPeopleFile
        if sOutputFilename == None:
            return

        # --------------------------------
        # Create root element <parentages>
        # --------------------------------
        e_people = ET.Element("people")

        # -----------------
        # For all people...
        # -----------------
        for sPersonKey, person in self.family.dctPeople.items():

            # ----------------------------------------------------------------------
            # Create element <person>, set attributes, append it to element <people>
            # ----------------------------------------------------------------------
            e_person = ET.Element("person")
            e_person.attrib["first"]    = person.sFirstName
            e_person.attrib["last"]     = person.sLastName
            e_person.attrib["gender"]   = person.sGender
            e_person.attrib["birthymd"] = person.sBirthYMD

            # -------------------------------------------------------------------------
            # Create subelement <father>, set attributes, append it to element <person>
            # -------------------------------------------------------------------------
            e_people.append(e_person)

            sFathersKey = person.getFathersKey()
            if sFathersKey != None:
                sFirst, sLast = self.family.getPersonNames(sFathersKey)
                e_father = ET.Element("father")
                e_father.attrib["first"] = sFirst
                e_father.attrib["last"]  = sLast
                e_person.append(e_father)

            sMothersKey = person.getMothersKey()
            if sMothersKey != None:
                sFirst, sLast = self.family.getPersonNames(sMothersKey)
                e_mother = ET.Element("mother")
                e_mother.attrib["first"] = sFirst
                e_mother.attrib["last"]  = sLast
                e_person.append(e_mother)

            sBirthCity, sBirthState, sBirthCountry, sBirthPostCode = person.getBirthPlace()
            if (sBirthCity != None) or (sBirthState != None) or (sBirthCountry != None) or (sBirthPostCode != None):
                e_birthplc = ET.Element("birthplc")
                if sBirthCity != None:
                    e_birthplc.attrib["city"] = sBirthCity
                if sBirthState != None:
                    e_birthplc.attrib["state"] = sBirthState
                if sBirthCountry != None:
                    e_birthplc.attrib["country"] = sBirthCountry
                if sBirthPostCode != None:
                    e_birthplc.attrib["postcode"] = sBirthPostCode
                e_person.append(e_birthplc)

        # end for sPersonKey in self.family.dctPeople

        # ---------------------------------
        # Create XML tree, write it to file
        # ---------------------------------
        et_people = ET.ElementTree(e_people)
        with open(sOutputFilename, "wb") as fhOutputfile:
            et_people.write(fhOutputfile)

        return

    # end saveFile()

    # ------------------------------------------------------------
    # Shows the family tree
    # ------------------------------------------------------------
    def showTree(self):
        
        # -----------------------------------------------------------------
        # Remove mothers, fathers and spouses with no entries in dctPeople,
        # create list of people with no father and mother (roots)
        # -----------------------------------------------------------------
        self.fixData()      
        lstRoots = self.getRoots()     

        # ---------------------------------------------------------------------------
        # Find females roots who are in the parentages dictionary with their
        # partners, add them to the list of parent-roots
        # ---------------------------------------------------------------------------
        self.lstParentRoots.clear()
        for sPersonKey in lstRoots:
            if self.family.dctPeople[sPersonKey].getGender() == "F":
                sPartnerKey = self.family.dctPeople[sPersonKey].getPartnerKey()
                if (sPartnerKey != None):
                    self.addToRoots(sPersonKey, sPartnerKey)

        for sParentageKey in self.lstParentRoots:
            sPersonKey1, sPersonKey2 = self.family.getPersonKeys(sParentageKey)
            print ("'%s %s' & '%s %s:" % 
                (self.family.dctPeople[sPersonKey1].sFirstName, self.family.dctPeople[sPersonKey1].sLastName, 
                 self.family.dctPeople[sPersonKey2].sFirstName, self.family.dctPeople[sPersonKey2].sLastName))

        return

    # end def showTree()

# end class FamilyTree ########################################


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
