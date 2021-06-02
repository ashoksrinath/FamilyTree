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
    # Adds person to family
    # ------------------------------------------------------------
    def addPerson(self, dctPersonInfo):

        sFirst = ""
        if "first" in dctPersonInfo:
            sFirst = dctPersonInfo["first"].strip()

        sLast = ""
        if "last" in dctPersonInfo:
            sLast = dctPersonInfo["last"].strip()

        sGender = None
        if "gender" in dctPersonInfo:
            sGender = dctPersonInfo["gender"].strip()

        sBirthYMD = None
        if "birthymd" in dctPersonInfo:
            sBirthYMD = dctPersonInfo["birthymd"].strip()
            
        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey != None:
            try:
                person = self.dctPeople[sPersonKey]
                person.setGender(sGender)
                person.setBirthYMD(sBirthYMD)
                dbgPrint (INF_DBG, ("Family.addPerson: updated %s %s %s %s" % 
                                    (person.sFirstName, person.sLastName, person.sGender, person.sBirthYMD)))
            except KeyError:
                person = Person(sFirst, sLast, sGender, sBirthYMD)
                self.dctPeople[sPersonKey] = person
                dbgPrint (INF_DBG, ("Family.addPerson: added %s %s %s %s" % 
                                    (person.sFirstName, person.sLastName, person.sGender, person.sBirthYMD)))
        else:
            print("addperson: first and last names are required (try help addperson)")

        return sPersonKey

    # end def addPerson()

    # ------------------------------------------------------------
    # Removes person from family
    # ------------------------------------------------------------
    def delPerson(self, sFirst, sLast):

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey != None:
            try:
                del self.dctPeople[self.makePersonKey(sFirst, sLast)]
            except KeyError as noPersonErr:
                print("delperson: '%s %s' not found" % (sFirst, sLast))
        else:
            print("delperson: first and last names are required (try help delperson)")

        return

    # end def delPerson()

    # ------------------------------------------------------------
    # Extracts and returns the person-keys from a parents-key
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
    # Finds and returns a list of "roots" in the family tree
    # ------------------------------------------------------------
    def getRoots(self):

        lstRoots = list()
        for sPersonKey, person in self.dctPeople.items():
            if (person.sMothersKey == None) and (person.sFathersKey == None):
                if person.sPartnersKey != None:
                    try:
                        partner = self.dctPeople[person.sPartnersKey]
                        if (partner.sMothersKey == None) and (partner.sFathersKey == None):
                            lstRoots.append(sPersonKey)
                            dbgPrint(INF_DBG, ("getRoots: Found person '%s %s' with no parents" % (person.sFirstName, person.sLastName)))
                    except KeyError:
                        print("showtree: warning, key '%s' not found in people" % sPartnersKey)

        return (lstRoots)

    # end def getRoots()

    # ------------------------------------------------------------
    # Lists all people in the family
    # ------------------------------------------------------------
    def listPeople(self):

        for sPersonKey in self.dctPeople:
            print("'%s %s' (%s), born: %s" % 
                  (self.dctPeople[sPersonKey].sFirstName, self.dctPeople[sPersonKey].sLastName, 
                   self.dctPeople[sPersonKey].sGender, self.dctPeople[sPersonKey].sBirthYMD))

        return

    # end def listPeople()

    # ------------------------------------------------------------
    # Lists all parentages in the family
    # ------------------------------------------------------------
    def listParentages(self):

        for sParentageKey, lstChildren in self.dctParentages.items():
            sMotherKey, sFathersKey = self.getPersonKeys(sParentageKey)
            print("'%s %s' & '%s %s':" % (self.dctPeople[sMotherKey].sFirstName, self.dctPeople[sMotherKey].sLastName,
                                          self.dctPeople[sFathersKey].sFirstName, self.dctPeople[sFathersKey].sLastName))
            for sPersonKey in lstChildren:
                sFirst, sLast = self.getPersonNames(sPersonKey)
                print ("    '%s %s'" % (sFirst, sLast))

        return

    # end def listParentages()

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
    def makeParentageKey(self, sMotherKey, sFathersKey):

        sParentsKey = sMotherKey + "&" + sFathersKey
        if sParentsKey != "&":
            return sParentsKey
        else:
            return None

    # end def makeParentageKey()

    # -------------------------------------------------------------------
    # Removes all children of the specified parents
    # -------------------------------------------------------------------
    def removeChildren(self, sMothersFirst, sMothersLast, sFathersFirst, sFathersLast):

        sParentageKey = self.makeParentageKey(self.makePersonKey(sMothersFirst, sMothersLast), 
                                              self.makePersonKey(sFathersFirst, sFathersLast))
        try:
            lstChildren = self.dctParentages[sParentageKey]
            
            # --------------------------------------------------
            # For all children, clear the values for the parents
            # --------------------------------------------------
            while len(lstChildren) > 0:
                sPersonKey = lstChildren.pop()
                try:
                    person = self.dctPeople[sPersonKey]
                    person.setParents(None, None)
                except KeyError:
                    sFirst, sLast = self.getPersonNames(sPersonKey)
                    print("removechildren: person '%s %s' not found" % (sFirst, sLast))

            # -------------------------------
            # Delete the parentage dictionary
            # -------------------------------
            del self.dctParentages[sParentageKey]

        except KeyError as noKids:
            print("removechildren: no parentage entry found for mother '%s %s' & father '%s %s'" %
                    (sMothersFirst, sMothersLast, sFathersFirst, sFathersLast))

        return

    # end def removeChildren()

    # ------------------------------------------------------------
    # Sets birthdate for person. Format should be YYYYMMDD
    # ------------------------------------------------------------
    def setBirthYMD(self, sFirst, sLast, sBirthYMD):

        try:
            person = self.dctPeople[self.makePersonKey(sFirst, sLast)]
            person.setBirthYMD(sBirthYMD)
        except KeyError as noPersonErr:
            print("setbirthymd: person '%s %s' not found" % (sFirst, sLast))

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
    # Sets parents for person
    # ------------------------------------------------------------
    def setParents(self, sFirst, sLast, sMothersFirst, sMothersLast, sFathersFirst, sFathersLast):

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey != None:
            try:
                person = self.dctPeople[sPersonKey]
                sMothersKey = self.makePersonKey(sMothersFirst, sMothersLast)
                sFathersKey = self.makePersonKey(sFathersFirst, sFathersLast)

                if not (sMothersKey == None and sFathersKey == None):
                    person.setParents(sMothersKey, sFathersKey)
                else:
                    print("setparents - mother's and father's names required")
            except KeyError:
                print("setparents - person '%s %s' not found" % (sFirst, sLast))
        else:
            print("setparents - person's first and last name required")

        return sPersonKey

    # end def setParents()

    # ------------------------------------------------------------
    # Shows the children of parents 
    # ------------------------------------------------------------
    def showChildren(self, sMothersFirst, sMothersLast, sFathersFirst, sFathersLast):

        sMothersKey = self.makePersonKey(sMothersFirst, sMothersLast)
        sFathersKey = self.makePersonKey(sFathersFirst, sFathersLast)
        if (sMothersKey != None) and (sFathersKey != None):
            if  (sMothersKey in self.dctPeople) and (sFathersKey in self.dctPeople):

                # -------------------------------------------------------------------
                # Create parents key, search for parents in dictionary, list children
                # -------------------------------------------------------------------
                sParentsKey = self.makeParentageKey(sMothersKey, sFathersKey)
                try:
                    dctChildren = self.dctParentages[sParentsKey]
                    for sPersonKey in dctChildren:
                        print("'%s %s' (%s), born: %s" % (self.dctPeople[sPersonKey].sFirstName, self.dctPeople[sPersonKey].sLastName, 
                                                self.dctPeople[sPersonKey].sGender, self.dctPeople[sPersonKey].sBirthYMD))
                except KeyError as noKids:
                    print("showchildren: no children found for mother '%s %s' & father '%s %s'" % 
                          (sMothersFirst, sMothersLast, sFathersFirst, sFathersLast))
            else:
                print("showchildren: mother '%s %s' or father '%s %s' not known" %
                     (sMothersFirst, sMothersLast, sFathersFirst, sFathersLast))
        else:
            print("showchildren: mother's and father's first and last names are required")

        return

    # def showChildren()

    # ------------------------------------------------------------
    # Shows all information about a person
    # ------------------------------------------------------------
    def showPerson(self, sFirst, sLast):

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey != None:
            try:
                person = self.dctPeople[sPersonKey]
                person.show(self.dctPeople)
            except KeyError:
                print("showperson: '%s %s' not found" % (sFirst, sLast))
        else:
            print("showperson: first and last names are required")

        return

    # end def showPerson()

    # ------------------------------------------------------------
    # Shows the family tree
    # ------------------------------------------------------------
    def showTree(self):

        partner1 = None
        partner2 = None
        lstRoots = self.getRoots()

        for sPersonKey in lstRoots:
            partner1 = self.dctPeople[sPersonKey]
            if (partner1.sGender == "F") and (partner1.sPartnersKey != None):
                partner2 = self.dctPeople[partner1.sPartnersKey]

                if (partner1 != None) and (partner2 != None):
                    print ("'%s %s' and '%s %s'" % (partner1.sFirstName, partner1.sLastName, partner2.sFirstName, partner2.sLastName))

        return

    # end def showTree()

# end class Family ############################################

