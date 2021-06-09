import os
import sys
from   lxml import etree
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

        if sPeopleFile != None:
            self.loadFile(sPeopleFile)

        self.getInput()

        return

    # end def __init__()

    # ------------------------------------------------------------
    # Processes birth-place information for a person
    # ------------------------------------------------------------
    def addBirthPlace(self, person, dctBirthPlc):

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

    # end def addBirthPlace()

    # ------------------------------------------------------------
    # Processes father's information for a person
    # ------------------------------------------------------------
    def addFather(self, person, dctAttribs):

        sFirst = None
        if "first" in dctAttribs:
            sFirst = dctAttribs["first"]

        sLast = None
        if "last" in dctAttribs:
            sLast = dctAttribs["last"]

        sFathersKey = self.family.makePersonKey(sFirst, sLast)
        if sFathersKey == None:
            return sFathersKey

        person.setFathersKey(sFathersKey)
        if not sFathersKey in self.family.dctPeople:
            sGender = "M"
            self.family.addPerson(sFirst, sLast, sGender, None)
            dbgPrint(INF_DBG, ("FamilyTree.addFather: added '%s %s'" % (sFirst, sLast)))

        return sFathersKey

    # end def addFather()

    # ------------------------------------------------------------
    # Processes mother's information for a person
    # ------------------------------------------------------------
    def addMother(self, person, dctAttribs):

        sFirst = None
        if "first" in dctAttribs:
            sFirst = dctAttribs["first"]

        sLast = None
        if "last" in dctAttribs:
            sLast = dctAttribs["last"]

        sMothersKey = self.family.makePersonKey(sFirst, sLast)
        if sMothersKey == None:
            return sMothersKey

        person.setMothersKey(sMothersKey)
        if not sMothersKey in self.family.dctPeople:
            sGender = "F"
            self.family.addPerson(sFirst, sLast, sGender, None)
            dbgPrint(INF_DBG, ("FamilyTree.addMother: added '%s %s'" % (sFirst, sLast)))

        return sMothersKey

    # end def addMother()

    # ------------------------------------------------------------
    # Processes information for a person
    # ------------------------------------------------------------
    def addPerson(self, dctAttribs):

        sFirst = None
        if "first" in dctAttribs:
            sFirst = dctAttribs["first"]

        sLast = None
        if "last" in dctAttribs:
            sLast = dctAttribs["last"]

        sGender = None
        if "gender" in dctAttribs:
            sGender = dctAttribs["gender"]

        sBirthYMD = None
        if "birthymd" in dctAttribs:
            sBirthYMD = dctAttribs["birthymd"]

        sPersonKey = self.family.addPerson(sFirst, sLast, sGender, sBirthYMD)
        dbgPrint(INF_DBG, ("FamilyTree.addPerson: added '%s %s'" % (sFirst, sLast)))

        return sPersonKey

    # end def addPerson()

    # ------------------------------------------------------------
    # Adds parents to the family tree display list
    # ------------------------------------------------------------
    def addToRoots(self, sPartnerKey1, sPartnerKey2):

        dbgPrint(INF_DBG, ("FamilyTree.addToRoots: partner keys: %s & %s" % (sPartnerKey1, sPartnerKey2)))

        sParentageKey = self.family.makeParentageKey2(sPartnerKey1, sPartnerKey2)
        if (sParentageKey == None):
            dbgPrint(INF_ERR, ("FamilyTree.addToRoots: parentage key is None; returning"))
            return

        try:
            lstChildren = self.family.dctParentages[sParentageKey]
            if len(lstChildren) == 0:
                dbgPrint(INF_DBG, ("FamilyTree.addToRoots: no children; returning"))
                return
        except KeyError:
            dbgPrint(INF_DBG, ("FamilyTree.addToRoots: no parentage entry for %s; returning" % sParentageKey))
            return

        if not sParentageKey in self.lstParentRoots:
            dbgPrint(INF_DBG, ("FamilyTree.addToRoots: adding %s" % sParentageKey))
            self.lstParentRoots.append(sParentageKey)
        else:
            dbgPrint(INF_DBG, ("FamilyTree.addToRoots: %s already added; returning" % sParentageKey))
            return

        for sPersonKey in lstChildren:
            if self.family.dctPeople[sPersonKey].getGender() == "F":
                sPartnerKey = self.family.dctPeople[sPersonKey].getPartnerKey()
                if sPartnerKey != None:
                    self.addToRoots(sPersonKey, sPartnerKey)

    # end def addToRoots()

    # ------------------------------------------------------------------------
    # Clears all content
    # ------------------------------------------------------------------------
    def clearAll(self):

        self.family.dctPeople.clear()
        self.family.dctParentages.clear()

        return

    # end def clear()

    # ------------------------------------------------------------------------
    # Checks all entries for referential integrity, removes unknown references
    # ------------------------------------------------------------------------
    def fixData(self):

        # ------------------------------------------------------------
        # Remove partners, mothers and fathers who aren't in dctPeople
        # ------------------------------------------------------------
        for person in self.family.dctPeople.values():
            sPartnerKey = person.getPartnerKey()
            if (sPartnerKey != None) and (not sPartnerKey in self.family.dctPeople):
                dbgPrint(INF_DBG, ("FamilyTree.fixData: removing unknown partner key '%s' for '%s %s'" %
                    (sPartnerKey, person.sFirst, person.sLast)))
                person.setPartnerKey(None)

            sMothersKey = person.getMothersKey()
            if (sMothersKey != None) and (not sMothersKey in self.family.dctPeople):
                dbgPrint(INF_DBG, ("FamilyTree.fixData: removing unknown mother's key '%s' for '%s %s'") %
                    (sMothersKey, person.sFirst, person.sLast))
                person.setMothersKey(None)

            sFathersKey = person.getFathersKey()
            if (sFathersKey != None) and (not sFathersKey in self.family.dctPeople):
                dbgPrint(INF_DBG, ("FamilyTree.fixData: removing unknown father's key '%s' for '%s %s'") %
                    (sFathersKey, person.sFirst, person.sLast))
                person.setFathersKey(None)

        # ---------------------------------------------------------------------------
        # Remove children from dctParentages values if their keys aren't in dctPeople
        # ---------------------------------------------------------------------------
        for sParentsKey, lstChildren in self.family.dctParentages.items():
            bListModified = False
            for nIdx in range(0, len(lstChildren)):
                if not lstChildren[nIdx] in self.family.dctPeople:
                    dbgPrint(INF_DBG, ("FamilyTree.fixData: removing unknown child-key %s for parent key %s" %
                        (lstChildren[nIdx], sParentsKey)))
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
        for sParentageKey in self.family.dctParentages.keys():
            sMothersKey, sFathersKey = self.family.getPersonKeys(sParentageKey)
            try:
                mother = self.family.dctPeople[sMothersKey]
                father = self.family.dctPeople[sFathersKey]
                if (mother.sMothersKey == None) and (mother.sFathersKey == None) \
                    and (father.sMothersKey == None) and (father.sFathersKey == None):

                    lstRoots.append(sParentageKey)
                    dbgPrint(INF_DBG, ("Family.getRoots: Found people '%s %s' & '%s %s' with no parents" % 
                        (mother.sFirst, mother.sLast, father.sFirst, father.sLast)))
            except KeyError as expectation:
                dbgPrint(INF_DBG, ("Family.getRoots: could not find '%s %s' or '%s %s' in dctPeople" % 
                    (mother.sFirst, mother.sLast, father.sFirst, father.sLast)))
                dbgPrint(INF_DBG, expectation)

        dbgPrint(INF_DBG, ("Family.getRoots: Returning %d roots" % len(lstRoots)))

        return lstRoots

    # end def getRoots()

    # ------------------------------------------------------------
    # Loads people from XML data file
    # ------------------------------------------------------------
    def loadFile(self, sFileName):

        try:
            parser = etree.XMLParser(remove_blank_text=True)
            pplTree = etree.parse(sFileName, parser)

            pplRoot = pplTree.getroot()
            personList = list(pplRoot)
            for personInfo in personList:
                self.processPerson(personInfo)

        except etree.ParseError as excParsing:
            print("loadfile - error parsing file '%s'" % sFileName)
            print(excParsing)
        except Exception as excUnhandled:
            print("loadfile - unhandled exception", excUnhandled)

        return

    # end def loadFile()

    # ------------------------------------------------------------
    # For pretty-printing
    # ------------------------------------------------------------
    def printSpaces(self, nLevel):

        for nSpace in range (0, nLevel):
            print ("  ", end=' ')

        return

    # end def printSpaces()

    # ------------------------------------------------------------
    # Processes person from XML
    # ------------------------------------------------------------
    def processPerson(self, personXML):

        person      = None
        sMothersKey = None
        sFathersKey = None

        try:
            # --------------------
            # Add Person to Family
            # --------------------
            if personXML.tag == "person":
                sPersonKey = self.addPerson(personXML.attrib)
                if sPersonKey == None:
                    dbgPrint(ERR_DBG, "FamilyTree.processPerson - error, sPersonKey is None")
                    return

            # ---------------------------------------
            # Process birthplace & parents for Person
            # ---------------------------------------
            person = self.family.dctPeople[sPersonKey]
            infoList = list(personXML)
            for infoItem in infoList:
                if infoItem.tag == "birthplc":
                    self.addBirthPlace(person, infoItem.attrib)

                elif infoItem.tag == "father":
                    sFathersKey = self.addFather(person, infoItem.attrib)

                elif infoItem.tag == "mother":
                    sMothersKey = self.addMother(person, infoItem.attrib)

                else:
                    dbgPrint(ERR_DBG, ("FamilyTree.processPerson - error, skipping unrecognized tag: %s" % infoItem.tag))

            # end for infoItem in infoList

            # ----------------------------------------------------------------------------
            # Set partner relationships between parents, add Person to parentages register
            # ----------------------------------------------------------------------------
            if (sMothersKey != None) and (sFathersKey != None):
                self.family.setPartnerKeys(sMothersKey, sFathersKey)
                self.family.addToParentages(sPersonKey, sMothersKey, sFathersKey)

        except Exception as extinction:
            dbgPrint(ERR_DBG, ("FamilyTree.processPerson - error processing: ", personXML.attrib))
            dbgPrint(ERR_DBG, ("FamilyTree.processPerson - unhandled exception: ", extinction))

        return

    # end def processPerson()

    # ------------------------------------------------------------
    # Saves people data to file in XML format
    # ------------------------------------------------------------
    def saveFile(self, sXMLfileName):

        # --------------------------------
        # Create root element <parentages>
        # --------------------------------
        e_people = etree.Element("people")

        # -----------------
        # For all people...
        # -----------------
        for sPersonKey, person in self.family.dctPeople.items():

            # ----------------------------------------------------------------------
            # Create element <person>, set attributes, append it to element <people>
            # ----------------------------------------------------------------------
            e_person = etree.Element("person")
            if person.sFirst != None:
                e_person.attrib["first"] = person.sFirst
            if person.sLast != None:
                e_person.attrib["last"] = person.sLast
            if person.sGender != None:
                e_person.attrib["gender"] = person.sGender
            if person.sBirthYMD != None:
                e_person.attrib["birthymd"] = person.sBirthYMD
            e_people.append(e_person)

            # -------------------------------------------------------------------------
            # Create subelement <father>, set attributes, append it to element <person>
            # -------------------------------------------------------------------------
            sFathersKey = person.getFathersKey()
            if sFathersKey != None:
                sFirst, sLast = self.family.getPersonNames(sFathersKey)
                if (sFirst != None) or (sLast != None):
                    e_father = etree.Element("father")
                    if sFirst != None:
                        e_father.attrib["first"] = sFirst
                    if sLast != None:
                        e_father.attrib["last"] = sLast
                    e_person.append(e_father)

            # -------------------------------------------------------------------------
            # Create subelement <mother>, set attributes, append it to element <person>
            # -------------------------------------------------------------------------
            sMothersKey = person.getMothersKey()
            if sMothersKey != None:
                sFirst, sLast = self.family.getPersonNames(sMothersKey)
                if (sFirst != None) or (sLast != None):
                    e_mother = etree.Element("mother")
                    if sFirst != None:
                        e_mother.attrib["first"] = sFirst
                    if sLast != None:
                        e_mother.attrib["last"]  = sLast
                    e_person.append(e_mother)

            # -------------------------------------------------------------------------
            # Create subelement <birthplc>, set attributes, append it to element <person>
            # -------------------------------------------------------------------------
            sBirthCity, sBirthState, sBirthCountry, sBirthPostCode = person.getBirthPlace()
            if (sBirthCity != None) or (sBirthState != None) or (sBirthCountry != None) or (sBirthPostCode != None):
                e_birthplc = etree.Element("birthplc")
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
        et_people = etree.ElementTree(e_people)
        with open(sXMLfileName, "wb") as fhOutputfile:
            et_people.write(fhOutputfile, encoding='utf-8', pretty_print=True, xml_declaration=True)

        return

    # end saveFile()

    # ------------------------------------------------------------
    # Shows the family tree
    # ------------------------------------------------------------
    def showTree(self):
        
        # -----------------------------------------------------------------
        # Remove mothers, fathers and spouses with no entries in dctPeople.
        # Create list of people with no father and mother (roots)
        # -----------------------------------------------------------------
        self.fixData()      
        lstRoots = self.getRoots()     

        # ---------------------------------------------------------------------------
        # Find roots who are in the parentages dictionary with their partners, show
        # their branches
        # ---------------------------------------------------------------------------
        for sParentageKey in lstRoots:
            sPersonKey1, sPersonKey2 = self.family.getPersonKeys(sParentageKey)
            if self.family.dctPeople[sPersonKey1].sGender == "F":
                mother = self.family.dctPeople[sPersonKey1]
                father = self.family.dctPeople[sPersonKey2]
            else:
                mother = self.family.dctPeople[sPersonKey2]
                father = self.family.dctPeople[sPersonKey1]

            print ("'%s %s' & '%s %s':" % 
                (mother.sFirst, mother.sLast, father.sFirst, father.sLast))

            lstChildren = self.family.dctParentages[sParentageKey]
            self.showBranch(lstChildren, 1)

        return

    # end def showTree()

    # ------------------------------------------------------------
    # Shows all descendants of one root in the family tree
    # ------------------------------------------------------------
    def showBranch(self, lstChildren, nLevel):

        for sPersonKey in lstChildren:

            mother = None
            father = None

            person = self.family.dctPeople[sPersonKey]
            sFirst  = person.getFirst()
            sLast   = person.getLast()
            sGender = person.getGender()
            
            self.printSpaces(nLevel)
            print ("Child: '%s %s' (%s)" % (sFirst, sLast, sGender))

            if sGender == "F":
                mother = self.family.dctPeople[sPersonKey]
                sPartnerKey = mother.getPartnerKey()
                if sPartnerKey != None:
                    father = self.family.dctPeople[sPartnerKey]
            elif sGender == "M":
                father = self.family.dctPeople[sPersonKey]
                sPartnerKey = father.getPartnerKey()
                if sPartnerKey != None:
                    mother = self.family.dctPeople[sPartnerKey]

            if (mother != None) and (father != None):
                self.printSpaces(nLevel)
                print ("'%s %s' & '%s %s'" % (mother.sFirst, mother.sLast, father.sFirst, father.sLast))
                sParentageKey = self.family.makeParentageKey4(mother.sFirst, mother.sLast, father.sFirst, father.sLast)
                if sParentageKey != None:
                    try:
                        lstChildren2 = self.family.dctParentages[sParentageKey]
                        self.showBranch(lstChildren2, nLevel+1)
                    except KeyError:
                        pass

        # end for

        return

    # end def showBranch()

# end class FamilyTree ########################################


if __name__ == "__main__":
    #
    # Initialize file-names
    #
    sPeopleFile = None

    #
    # Process command-line arguments
    #
    if len(sys.argv) <= 2:
        if len(sys.argv) == 2:
            sPeopleFile = sys.argv[1]
    else:
        print("Usage: python3 %s [file-name]" % sys.argv[0])
        print("       where file-name contains XML data about people")
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
