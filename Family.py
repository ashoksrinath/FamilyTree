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
    def __init__(self, sPeopleFile, sParentageFile):
 
        self.sPeopleFile    = sPeopleFile
        self.sParentageFile = sParentageFile

        self.xmlPeople      = None
        self.xmlParentages  = None

        self.dctPeople      = dict()
        self.dctParentages  = dict()

        return

    # end def __init__()

    # ------------------------------------------------------------
    # Sets parents for a person
    # ------------------------------------------------------------
    def addParents(self, sFirst, sLast, sFatherFirst, sFatherLast, sMotherFirst, sMotherLast):

        # --------------------------------------------
        # Validate parameters, get reference to person
        # --------------------------------------------
        sPersonKey = self.makePersonKey(sFirst, sLast)
        sFatherKey = self.makePersonKey(sFatherFirst, sFatherLast)
        sMotherKey = self.makePersonKey(sMotherFirst, sMotherLast)
        try:
            person = self.dctPeople[sPersonKey]
            if (not sFatherKey in self.dctPeople) or (not sMotherKey in self.dctPeople):
                print("addparents: one or more parents are not known (try addperson, showpeople)")
            elif (self.dctPeople[sFatherKey].sGender != "M") or (self.dctPeople[sMotherKey].sGender != "F"):
                print("addparents: warning: father's gender is not 'M' or mother's gender is not 'F'")
                return

        except KeyError as noPersonErr:
            print ("addparents: person '" + sFirst + " " + sLast + "' not found")

            return
       
        # ------------------------------------------------------------------------------------------
        # Set/update parents in Person instance.  Find/create Parentage dictionary, add/update child
        # ------------------------------------------------------------------------------------------
        person.addParents(sFatherFirst, sFatherLast, sMotherFirst, sMotherLast)
        sParentageKey = self.makeParentageKey(sFatherFirst, sFatherLast, sMotherFirst, sMotherLast)
        try:
            dctChildren = self.dctParentages[sParentageKey]
        except KeyError as noKids:
            dctChildren = dict()
            self.dctParentages[sParentageKey] = dctChildren           

        dctChildren[sPersonKey] = self.dctPeople[sPersonKey]
 
        # -----------------------------------------
        # Set partner relationships between parents
        # -----------------------------------------
        try:
            self.dctPeople[sFatherKey].setPartnerKey (sMotherKey)
        except KeyError as noKids:
            print ("addparents: failed to update partner key for father '" + sFatherFirst + " " + sFatherLast + "'")
        try:
            self.dctPeople[sMotherKey].setPartnerKey (sFatherKey)
        except KeyError as noKids:
            print ("addparents: failed to update partner key for mother '" + sMotherFirst + " " + sMotherLast + "'")

        return

    # end def addParents()

    # ------------------------------------------------------------
    # Adds person to family
    # ------------------------------------------------------------
    def addPerson(self, sFirst, sLast, sGender, sBirthYMD):

        person = Person(sFirst, sLast, sGender, sBirthYMD);

        self.dctPeople[self.makePersonKey(sFirst, sLast)] = person

        return

    # end def addPerson()

    # ------------------------------------------------------------
    # Deletes all children for the specified parents
    # ------------------------------------------------------------
    def delParents(self, sFathersFirst, sFathersLast, sMothersFirst, sMothersLast):

        # ----------------------------
        # Get the parentage dictionary
        # ----------------------------
        sParentageKey = self.makeParentageKey(sFathersFirst, sFathersLast, sMothersFirst, sMothersLast)
        try:
            dctChildren = self.dctParentages[sParentageKey]
            
            # --------------------------------------------------
            # For all children, clear the values for the parents
            # --------------------------------------------------
            for sPersonKey, person in dctChildren.items():
                try:
                    person.addParents("", "", "", "")
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
    # Loads parentages from an XML data file
    # ------------------------------------------------------------
    def loadParentages(self, sXMLfileName):

        try:
            self.ptgRoot = ET.parse("parentages.xml")
            for parentage in self.ptgRoot.iter("parentage"):
                sFathersFirst   = ""
                sFathersLast    = ""
                sMothersFirst   = ""
                sMothersLast    = ""
                for sKey, sValue in parentage.attrib.items():
                    if sKey == "fathersfirst":
                        sFathersFirst = sValue
                    elif sKey == "fatherslast":
                        sFathersLast = sValue
                    elif sKey == "mothersfirst":
                        sMothersFirst = sValue
                    elif sKey == "motherslast":
                        sMothersLast = sValue
                    else:
                        print("loadparentages - unrecognized pair: " + sKey + ": " + sValue)
                sFirstName      = ""
                sLastName       = ""
                for child in parentage[0]:
                    if (child.tag == "first"):
                        sFirstName = child.text
                    elif (child.tag == "last"):
                        sLastName = child.text

                if (len(sFirstName.strip()) > 0) and (len(sLastName.strip()) > 0) and \
                    (len(sFathersFirst.strip()) > 0) and (len(sFathersLast.strip()) > 0) and \
                    (len(sMothersFirst.strip()) > 0) and (len(sMothersLast.strip()) > 0):

                    self.addParents(sFirstName, sLastName, sFathersFirst, sFathersLast, sMothersFirst, sMothersLast)
                else:
                    print("loadpeople - skipping entry first: '" + sFirstName + "' last: '" + sLastName + \
                        "' fathersfirst: '" + sFathersFirst + "' fathersfirst: '" + sFathersLast + \
                        "' mothersfirst: '" + sMothersFirst + "' mothersfirst: '" + sMothersLast + "'")
            # end for parentage in self.ptgRoot.iter("parentage"):
        except FileNotFoundError:
            print("   Parentages-file '" + sXMLfileName + "' not found")
        except ET.ParseError as excParsing:
            print("   Error parsing '" + sXMLfileName + "', skipping")
        except Exception as excUnhandled:
            print("   Unhandled exception parsing '" + sXMLfileName + "', skipping")

        return

    # end def loadParentages()

    # ------------------------------------------------------------
    # Loads people from an XML data file
    # ------------------------------------------------------------
    def loadPeople(self, sXMLfileName):

        try:
            pplRoot = ET.parse(sXMLfileName)
            for person in pplRoot.iter("person"):
                sFirstName  = ""
                sLastName   = ""
                sGender     = ""
                sBirthYMD   = ""
                for sKey, sValue in person.attrib.items():
                    if sKey == "first":
                        sFirstName = sValue
                    elif sKey == "last":
                        sLastName = sValue
                    elif sKey == "gender":
                        sGender = sValue
                    elif sKey == "birthymd":
                        sBirthYMD = sValue
                    else:
                        print("loadpeople - unrecognized pair: " + sKey + ": " + sValue)
        
                if (len(sFirstName.strip()) > 0) and (len(sLastName.strip()) > 0) and (len(sGender.strip()) > 0) and (len(sBirthYMD.strip()) > 0):
                    self.addPerson(sFirstName, sLastName, sGender, sBirthYMD)
                else:
                    print("loadpeople - skipping entry first: '" + sFirstName + "' last: '" + sLastName + \
                        "' gender: '" + sGender + "' birthymd: '" + sBirthYMD + "'")
            # end for person in ptgRoot.iter("person")
        except FileNotFoundError:
            print("loadpeople - file '" + sXMLfileName + "' not found")
        except ET.ParseError as excParsing:
            print("loadpeople - error parsing file '" + sXMLfileName + "', skipping")
        except Exception as excUnhandled:
            print("loadpeople - unhandled exception parsing file '" + sXMLfileName + "':", excUnhandled)

        return

    # end def loadPeople()

    # ------------------------------------------------------------
    # Creates key for a person (first-last)
    # ------------------------------------------------------------
    def makePersonKey(self, sFirst, sLast):

        sPersonKey = sFirst + "#" + sLast

        return sPersonKey

    # end def makePersonKey()

    # ------------------------------------------------------------
    # Makes a union key
    # ------------------------------------------------------------
    def makeParentageKey(self, sFatherFirst, sFatherLast, sMotherFirst, sMotherLast):

        sParentageKey = self.makePersonKey(sFatherFirst, sFatherLast) + "&" + self.makePersonKey(sMotherFirst, sMotherLast)

        return sParentageKey

    # end def makeParentageKey()

    # ------------------------------------------------------------
    # Processes input
    # ------------------------------------------------------------
    def processInput(self):

        print("Processing people-file " + self.sPeopleFile + " and parentage-file " + self.sParentageFile + "...")

        self.loadPeople(self.sPeopleFile)

        self.loadParentages(self.sParentageFile)

        self.getInput()

        return

    # end def processInput()

    # ------------------------------------------------------------
    # Saves parentage data to file in XML format
    # ------------------------------------------------------------
    def saveParentages(self, sXMLfileName):

        # ---------------------------------------
        # Ensure that we have an output file-name
        # ---------------------------------------
        sOutputFilename = None
        if (sXMLfileName != None):
            sOutputFilename = sXMLfileName
        else:
            sOutputFilename = self.sParentageFile
        if sOutputFilename == None:
            return

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

        # ---------------------------------
        # Create XML tree, write it to file
        # ---------------------------------
        tree = ET.ElementTree(parentages)
        with open(sOutputFilename, "wb") as fhOutputfile:
            tree.write(fhOutputfile)

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
        sParentageKey = self.makeParentageKey(sFatherFirst, sFatherLast, sMotherFirst, sMotherLast)
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

