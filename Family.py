import xml.etree.ElementTree as ET 
from   Utils import *
from   CLI import CLI
from   Person import Person


# #############################################################
# Family: class containing information on a family
# -------------------------------------------------------------
class Family:
    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self, sPeopleFile):
 
        self.sPeopleFile    = sPeopleFile

        self.dctPeople      = dict()
        self.dctParentages  = dict()

        return

    # end def __init__()

    # ------------------------------------------------------------
    # Sets parents for a person
    # ------------------------------------------------------------
    def addParents(self, sPersonKey, parentList):

        for parent in parentList:
            print (parent.tag, parent.attrib)

            if parent.tag == "father":
                sFatherFirst = ""
                if "first" in parent.attrib:
                    sFatherFirst = parent.attrib["first"]
                sFatherLast = ""
                if "last" in parent.attrib:
                    sFatherLast = parent.attrib["last"]
                sFatherKey = self.makePersonKey(sFatherFirst, sFatherLast)
                if not sFatherKey in self.dctPeople:
                    self.dctPeople[sFatherKey] = None
                    print("addparents: added place-holder for father to people dictionary (first: %s, last: %s) " % (sFatherFirst, sFatherLast))
            elif parent.tag == "mother":
                sMotherFirst = ""
                if "first" in parent.attrib:
                    sMotherFirst = parent.attrib["first"]
                sMotherLast = ""
                if "last" in parent.attrib:
                    sMotherLast = parent.attrib["last"]
                sMotherKey = self.makePersonKey(sMotherFirst, sMotherLast)
                if not sMotherKey in self.dctPeople:
                    self.dctPeople[sMotherKey] = None
                    print("addparents: added place-holder for mother to people dictionary (first: %s, last: %s) " % (sMotherFirst, sMotherLast))
            else:
                print("Error, unrecognized tag:" + parent.tag)

        # ------------------------------------------------------------------------------------------
        # Set/update parents in Person instance.  Find/create Parentage dictionary, add/update child
        # ------------------------------------------------------------------------------------------
        try:
            person = self.dctPeople[sPersonKey]
            person.setParents(sFatherKey, sMotherKey)

            sParentsKey = self.makeParentsKey(sFatherKey, sMotherKey)
            try:
                lstChildren = self.dctParentages[sParentsKey]
            except KeyError as noKids:
                lstChildren = list()
                self.dctParentages[sParentsKey] = lstChildren           

            lstChildren.append(sPersonKey)
 
        # -----------------------------------------
        # Set partner relationships between parents
        # -----------------------------------------
        try:
            self.dctPeople[sFatherKey].setPartner (sMotherKey)
        except KeyError as noKids:
            print ("addparents: failed to update partner key for father (first: %s, last: %s)" % sFatherFirst, sFatherLast)

        try:
            self.dctPeople[sMotherKey].setPartner (sFatherKey)
        except KeyError as noKids:
            print ("addparents: failed to update partner key for mother (first: %s, last: %s)" % sMotherFirst, sMotherLast)

 
        except KeyError as noPersonErr:
            print ("addparents: person with key '%s' not found" % sPersonKey)

        return

    # end def addParents()

    # ------------------------------------------------------------
    # Adds person to family
    # ------------------------------------------------------------
    def addPerson(self, dctPersonInfo):

        sFirst = ""
        if "first" in dctPersonInfo:
            sFirst = dctPersonInfo["first"].strip()

        sLast = ""
        if "last" in dctPersonInfo:
            sLast = dctPersonInfo["last"].strip()

        sGender = ""
        if "gender" in dctPersonInfo:
            sGender = dctPersonInfo["gender"].strip()

        sBirthYMD = ""
        if "birthymd" in dctPersonInfo:
            sBirthYMD = dctPersonInfo["birthymd"].strip()
            
        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey != None:
            person = Person(sFirst, sLast, sGender, sBirthYMD);
            self.dctPeople[sPersonKey] = person

        return sPersonKey

    # end def addPerson()

    # ------------------------------------------------------------
    # Deletes all children for the specified parents
    # ------------------------------------------------------------
    def delParents(self, sFathersFirst, sFathersLast, sMothersFirst, sMothersLast):

        # ----------------------------
        # Get the parentage dictionary
        # ----------------------------
        sParentageKey = self.makeParentsKey(sFathersFirst, sFathersLast, sMothersFirst, sMothersLast)
        try:
            dctChildren = self.dctParentages[sParentageKey]
            
            # --------------------------------------------------
            # For all children, clear the values for the parents
            # --------------------------------------------------
            for sPersonKey, person in dctChildren.items():
                try:
                    person.setParents(None, None)
                except KeyError as noKid:
                    print("delparents: no parentage entry found for father '" + sFathersFirst + " " + sFathersLast + \
                        "' & mother '" + sMothersFirst + " " + sMothersLast + "'")

            # -------------------------------
            # Delete the parentage dictionary
            # -------------------------------
            del self.dctParentages[sParentageKey]

        except KeyError as noKids:
            print("delparents: no children found for father '" + sFathersFirst + " " + sFathersLast + \
                "' & mother '" + sMothersFirst + " " + sMothersLast + "'")

        return

    # end def delParents()

    # ------------------------------------------------------------
    # Removes person from family
    # ------------------------------------------------------------
    def delPerson(self, sFirst, sLast):

        try:
            del self.dctPeople[self.makePersonKey(sFirst, sLast)]
        except KeyError as noPersonErr:
            print("Person '" + sFirst + " " + sLast + "' not found")

        return

    # end def delPerson()

    # ------------------------------------------------------------
    # Gets user-input from the command-line
    # ------------------------------------------------------------
    def getInput(self):

        cli = CLI(self)
        cli.cmdloop()

        return

    # end def getInput()

    # ------------------------------------------------------------
    # Extracts and returns the person-keys from a parentage-key
    # ------------------------------------------------------------
    def getPersonKeys(self, sParentageKey):

        sPersonKeys = sParentageKey.split('&')

        return sPersonKeys

    # end def getPersonKeys()

    # ------------------------------------------------------------
    # Extracts and returns the person names from a person-key
    # ------------------------------------------------------------
    def getPersonNames(self, sPersonKey):

        sPersonNames = sPersonKey.split('#')

        return sPersonNames

    # end def getPersonNames()

    # ------------------------------------------------------------
    # Loads people from an XML data file
    # ------------------------------------------------------------
    def loadPeople(self, sXMLfileName):

        try:
            pplTree = ET.parse(sXMLfileName)
            pplRoot = pplTree.getroot()
            personList = pplRoot.getchildren()
            for person in personList:
                if person.tag == "person":
                    sPersonKey = self.addPerson(person.attrib)
                    if sPersonKey != None:
                        parentList = person.getchildren()
                        if len(parentList) > 0:
                            self.addParents(sPersonKey, parentList)

            # end for person in personList
        except FileNotFoundError:
            print("loadpeople - file '" + sXMLfileName + "' not found")
        except ET.ParseError as excParsing:
            print("loadpeople - error parsing file '" + sXMLfileName + "', skipping")
        except Exception as excUnhandled:
            print("loadpeople - unhandled exception parsing file '" + sXMLfileName + "':", excUnhandled)

        return

    # end def loadPeople()

    # ------------------------------------------------------------
    # Creates dictionary key for a person
    # ------------------------------------------------------------
    def makePersonKey(self, sFirst, sLast):

        sPersonKey = sFirst + "#" + sLast
        if sPersonKey != "#":
            return sPersonKey
        else:
            return None

    # end def makePersonKey()

    # ------------------------------------------------------------
    # Makes a union key
    # ------------------------------------------------------------
    def makeParentsKey(self, sFatherKey, sMotherKey):

        sParentsKey = sFatherKey + "&" + sMotherKey

        return sParentsKey

    # end def makeParentsKey()

    # ------------------------------------------------------------
    # Processes input
    # ------------------------------------------------------------
    def processInput(self):

        print("Processing people-file " + self.sPeopleFile + "...")

        self.loadPeople(self.sPeopleFile)

        self.getInput()

        return

    # end def processInput()

    # ------------------------------------------------------------
    # Saves parentage data to file in XML format
    # ------------------------------------------------------------
    def saveParentages(self, sXMLfileName):

        # --------------------------------
        # Create root element <parentages>
        # --------------------------------
        parentages = ET.Element("parentages")

        # --------------------------------------------------------------------------------------
        # For all parentages, get the keys for the parents, and the dictionary of their children
        # --------------------------------------------------------------------------------------
        for sParentageKey, dctChildren in self.dctParentages.items():
            sFatherKey, sMotherKey = self.getPersonKeys(sParentageKey)

            # -------------------------------------------------------------------------------------------
            # Create subelement <parentage fathersfirst="" fatherslast="" mothersfirst="" motherslast="">
            # -------------------------------------------------------------------------------------------
            parentage = ET.Element("parentage")
            parentage.set("fathersfirst", self.dctPeople[sFatherKey].sFirstName)
            parentage.set("fatherslast", self.dctPeople[sFatherKey].sLastName)
            parentage.set("mothersfirst", self.dctPeople[sMotherKey].sFirstName)
            parentage.set("motherslast", self.dctPeople[sMotherKey].sLastName)
            parentages.append(parentage)

            # ---------------------------------
            # For all children of these parents
            # ---------------------------------
            for sPersonKey in dctChildren:

                child = ET.Element("child")

                # ----------------------------------------------------
                # Set the first, last, gender and birthymd subelements
                # ----------------------------------------------------
                first = ET.SubElement(child, "first")
                first.text = self.dctPeople[sPersonKey].sFirstName

                last = ET.SubElement(child, "last")
                last.text = self.dctPeople[sPersonKey].sLastName

                parentage.append(child)

            # end for sPersonKey in dctChildren
        # end for sParentageKey, dctChildren in self.dctParentages.items()

        return

    # end saveParentages()

    # ------------------------------------------------------------
    # Saves people data to file in XML format
    # ------------------------------------------------------------
    def savePeople(self, sXMLfileName):

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
        people = ET.Element("people")

        # -----------------
        # For all people...
        # -----------------
        for sPersonKey in self.dctPeople:

            # ---------------------------------------------------------
            # Create subelement <person>, append it to element <people>
            # ---------------------------------------------------------
            person = ET.Element("person")
            people.append(person)

            # -----------------------------------------------------------------
            # Set the first, last, gender and birthymd subelements for <person>
            # -----------------------------------------------------------------
            first = ET.SubElement(person, "first")
            first.text = self.dctPeople[sPersonKey].sFirstName

            last = ET.SubElement(person, "last")
            last.text = self.dctPeople[sPersonKey].sLastName

            gender = ET.SubElement(person, "gender")
            gender.text = self.dctPeople[sPersonKey].sGender
                
            birthymd = ET.SubElement(person, "birthymd")
            birthymd.text = self.dctPeople[sPersonKey].sBirthYMD

        # end for sPersonKey in self.dctPeople

        # ---------------------------------
        # Create XML tree, write it to file
        # ---------------------------------
        tree = ET.ElementTree(people)
        with open(sOutputFilename, "wb") as fhOutputfile:
            tree.write(fhOutputfile)

        return

    # end savePeople()

    # ------------------------------------------------------------
    # Sets birthdate for person. Format should be YYYYMMDD
    # ------------------------------------------------------------
    def setBirthYMD(self, sFirst, sLast, sBirthYMD):

        try:
            person = self.dctPeople[self.makePersonKey(sFirst, sLast)]
            person.setBirthYMD(sBirthYMD)
        except KeyError as noPersonErr:
            print("setbirthymd: person '" + sFirst + " " + sLast + "' not found")

        return

    # end def setBirthYMD()

    # ------------------------------------------------------------
    # Sets birth place for a person
    # ------------------------------------------------------------
    def setBirthPlace(self, sFirst, sLast, sCity, sState, sCountry, sPostCode):

        try:
            person = self.dctPeople[self.makePersonKey(sFirst, sLast)]
            person.setBirthPlace(sCity, sState, sCountry, sPostCode)
        except KeyError as noPersonErr:
            print ("setbirthplc: person '" + sFirst + " " + sLast + "' not found")

        return

    # end def setBirthPlace()

    # ------------------------------------------------------------
    # Shows the children of two parents 
    # ------------------------------------------------------------
    def showChildren(self, sFatherFirst, sFatherLast, sMotherFirst, sMotherLast):

        # -------------------
        # Validate parameters
        # -------------------
        if  (not self.makePersonKey(sFatherFirst, sFatherLast) in self.dctPeople) or \
            (not self.makePersonKey(sMotherFirst, sMotherLast) in self.dctPeople):
                print("showchildren: father '" + sFatherFirst + " " + sFatherLast + \
                    "' or mother '" + sMotherFirst + " " + sMotherLast + "' not known")

                return

        # --------------------------------------------------------------------------    
        # Create union-key, search for union in dictionary, list children from union
        # --------------------------------------------------------------------------    
        sParentageKey = self.makeParentsKey(sFatherFirst, sFatherLast, sMotherFirst, sMotherLast)
        try:
            dctChildren = self.dctParentages[sParentageKey]
            for sPersonKey in dctChildren:
                print("'" + self.dctPeople[sPersonKey].sFirstName + " " + self.dctPeople[sPersonKey].sLastName + \
                    "' (" + self.dctPeople[sPersonKey].sGender + "), born: " + self.dctPeople[sPersonKey].sBirthYMD)
        except KeyError as noKids:
            print("showchildren: no children found for father '" + sFatherFirst + " " + sFatherLast + \
                "' & mother '" + sMotherFirst + " " + sMotherLast + "'")

        return

    # def showChildren()

    # ------------------------------------------------------------
    # Shows all information about a person
    # ------------------------------------------------------------
    def showPerson(self, sFirst, sLast):

        try:
            person = self.dctPeople[self.makePersonKey(sFirst, sLast)]
            person.show()
        except KeyError as noPersonErr:
            print("Person '" + sFirst + " " + sLast + "' not found")

        return

    # end def showPerson()

    # ------------------------------------------------------------
    # Shows all people in the family
    # ------------------------------------------------------------
    def showPeople(self):

        for sPersonKey in self.dctPeople:
            print("'" + self.dctPeople[sPersonKey].sFirstName + " " + self.dctPeople[sPersonKey].sLastName + \
                "' (" + self.dctPeople[sPersonKey].sGender + "), born: " + self.dctPeople[sPersonKey].sBirthYMD)

        return

    # end def showPeople()

    # ------------------------------------------------------------
    # Shows all unions in the family
    # ------------------------------------------------------------
    def showParentages(self):

        for sParentageKey, dctChildren in self.dctParentages.items():
            sFatherKey, sMotherKey = self.getPersonKeys(sParentageKey)
            print("'" + self.dctPeople[sFatherKey].sFirstName + " " + self.dctPeople[sFatherKey].sLastName + "' & '" + \
                        self.dctPeople[sMotherKey].sFirstName + " " + self.dctPeople[sMotherKey].sLastName + "'")

        return

    # end def showUnions()

# end class Family ############################################

