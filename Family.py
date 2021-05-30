import xml.etree.ElementTree as ET 
from   Utils import *
from   Person import Person


# #############################################################
# Family: class containing information on a family
# -------------------------------------------------------------
class Family:
    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self):
 
        self.dctPeople      = dict()
        self.dctParentages  = dict()

        return

    # end def __init__()

    # ------------------------------------------------------------
    # Sets parents for a person
    # ------------------------------------------------------------
    def addParents(self, sPersonKey, parentList):

        for parent in parentList:
            if parent.tag == "father":
                sFatherFirst = ""
                if "first" in parent.attrib:
                    sFatherFirst = parent.attrib["first"]
                sFatherLast = ""
                if "last" in parent.attrib:
                    sFatherLast = parent.attrib["last"]
                sFatherKey = self.makePersonKey(sFatherFirst, sFatherLast)
                if (sFatherKey != None) and (not sFatherKey in self.dctPeople):
                    dctFatherInfo = dict()
                    dctFatherInfo["first"] = sFatherFirst
                    dctFatherInfo["last"] = sFatherLast
                    dctFatherInfo["gender"] = "M"
                    self.addPerson(dctFatherInfo)
            elif parent.tag == "mother":
                sMotherFirst = ""
                if "first" in parent.attrib:
                    sMotherFirst = parent.attrib["first"]
                sMotherLast = ""
                if "last" in parent.attrib:
                    sMotherLast = parent.attrib["last"]
                sMotherKey = self.makePersonKey(sMotherFirst, sMotherLast)
                if (sMotherKey != None) and (not sMotherKey in self.dctPeople):
                    dctMotherInfo = dict()
                    dctMotherInfo["first"] = sMotherFirst
                    dctMotherInfo["last"] = sMotherLast
                    dctMotherInfo["gender"] = "F"
                    self.addPerson(dctMotherInfo)
            else:
                print("Error, unrecognized tag:" + parent.tag)
                return None

        # end for parent in parentList

        # ------------------------------------------------
        # Set/update parents in Person instance, add child
        # ------------------------------------------------
        if (sFatherKey != None) and (sMotherKey != None):
            try:
                person = self.dctPeople[sPersonKey]
                person.setParents(sFatherKey, sMotherKey)

                sParentsKey = self.makeParentsKey(sFatherKey, sMotherKey)
                if sParentsKey != None:
                    try:
                        lstChildren = self.dctParentages[sParentsKey]
                    except KeyError:
                        lstChildren = list()

                    self.dctParentages[sParentsKey] = lstChildren           

                    lstChildren.append(sPersonKey)
            except KeyError as noPerson:
                print ("addparents: failed to find person to add parents for (key: %s)" % sPersonKey)
                print (noPerson)

            # -----------------------------------------
            # Set partner relationships between parents
            # -----------------------------------------
            try:
                self.dctPeople[sFatherKey].setPartner (sMotherKey)
            except KeyError:
                print ("addparents: failed to update partner key for father (first: %s, last: %s)" % sFatherFirst, sFatherLast)

            try:
                self.dctPeople[sMotherKey].setPartner (sFatherKey)
            except KeyError:
                print ("addparents: failed to update partner key for mother (first: %s, last: %s)" % sMotherFirst, sMotherLast)

        # end if (sFatherKey != None) and (sMotherKey != None)

        return sParentsKey

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
            try:
                person = self.dctPeople[sPersonKey]
                person.setBirthYMD(sBirthYMD)
                print ("Updated %s %s" % (sFirst, sLast))
            except KeyError:
                person = Person(sFirst, sLast, sGender, sBirthYMD)
                self.dctPeople[sPersonKey] = person
                print("Added %s %s" % (sFirst, sLast))
        else:
            print("Insufficient data to add person '%s %s'" % (sFirst, sLast))

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
    # Creates dictionary key for parents
    # ------------------------------------------------------------
    def makeParentsKey(self, sFatherKey, sMotherKey):

        sParentsKey = sFatherKey + "&" + sMotherKey
        if sParentsKey != "&":
            return sParentsKey
        else:
            return None

    # end def makeParentsKey()

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
    # Shows the children of parents 
    # ------------------------------------------------------------
    def showChildren(self, sFatherFirst, sFatherLast, sMotherFirst, sMotherLast):

        sMotherKey = self.makePersonKey(sMotherFirst, sMotherLast)
        sFatherKey = self.makePersonKey(sFatherFirst, sFatherLast)
        if (sMotherKey != None) and (sFatherKey != None):
            if  (sMotherKey in self.dctPeople) and (sFatherKey in self.dctPeople):

                # -------------------------------------------------------------------
                # Create parents key, search for parents in dictionary, list children
                # -------------------------------------------------------------------
                sParentsKey = self.makeParentsKey(sMotherKey, sFatherKey)
                try:
                    dctChildren = self.dctParentages[sParentsKey]
                    for sPersonKey in dctChildren:
                        print("'%s %s' (%s), born: %s" % (self.dctPeople[sPersonKey].sFirstName, self.dctPeople[sPersonKey].sLastName, 
                                                self.dctPeople[sPersonKey].sGender, self.dctPeople[sPersonKey].sBirthYMD))
                except KeyError as noKids:
                    print("showchildren: no children found for mother '%s %s' & father '%s %s'" % 
                          (sFatherFirst, sFatherLast, sMotherFirst, sMotherLast))
            else:
                print("showchildren: mother '%s %s' or father '%s %s' not known" %
                     (sMotherFirst, sMotherLast, sFatherFirst, sFatherLast))
        else:
            print("showchildren: mother and/or father not known")

        return

    # def showChildren()

    # ------------------------------------------------------------
    # Shows all information about a person
    # ------------------------------------------------------------
    def showPerson(self, sFirst, sLast):

        try:
            person = self.dctPeople[self.makePersonKey(sFirst, sLast)]
            person.show(self.dctPeople)
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

