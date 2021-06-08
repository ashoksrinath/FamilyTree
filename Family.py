from Utils import *
from Person import Person


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
    def addPerson(self, sFirst, sLast, sGender, sBirthYMD):

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey != None:
            try:
                person = self.dctPeople[sPersonKey]
                person.setGender(sGender)
                person.setBirthYMD(sBirthYMD)
                dbgPrint (INF_DBG, ("Family.addPerson: updated %s %s %s %s" % 
                                    (person.sFirst, person.sLast, person.sGender, person.sBirthYMD)))
            except KeyError:
                person = Person(sFirst, sLast, sGender, sBirthYMD)
                self.dctPeople[sPersonKey] = person
                dbgPrint (INF_DBG, ("Family.addPerson: added %s %s %s %s" % 
                                    (person.sFirst, person.sLast, person.sGender, person.sBirthYMD)))
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
    # Lists all people in the family
    # ------------------------------------------------------------
    def listPeople(self):

        for sPersonKey in self.dctPeople:
            print("'%s %s' (%s), born: %s" % 
                  (self.dctPeople[sPersonKey].sFirst, self.dctPeople[sPersonKey].sLast, 
                   self.dctPeople[sPersonKey].sGender, self.dctPeople[sPersonKey].sBirthYMD))

        return

    # end def listPeople()

    # ------------------------------------------------------------
    # Lists all parentages in the family
    # ------------------------------------------------------------
    def listParentages(self):

        for sParentageKey, lstChildren in self.dctParentages.items():
            sMotherKey, sFathersKey = self.getPersonKeys(sParentageKey)
            print("'%s %s' & '%s %s':" % (self.dctPeople[sMotherKey].sFirst, self.dctPeople[sMotherKey].sLast,
                                          self.dctPeople[sFathersKey].sFirst, self.dctPeople[sFathersKey].sLast))
            for sPersonKey in lstChildren:
                sFirst, sLast = self.getPersonNames(sPersonKey)
                print ("    '%s %s'" % (sFirst, sLast))

        return

    # end def listParentages()

    # ------------------------------------------------------------
    # Creates dictionary key for a person
    # ------------------------------------------------------------
    def makePersonKey(self, sFirst, sLast):

        if (sFirst == None) or (sLast == None):
            return None

        sPersonKey = sFirst.strip() + "#" + sLast.strip()
        if sPersonKey == "#":
            return None

        return sPersonKey

    # end def makePersonKey()

    # ------------------------------------------------------------
    # Creates dictionary key for parentages
    # ------------------------------------------------------------
    def makeParentageKey2(self, sMothersKey, sFathersKey):

        if (sMothersKey == None) or (sFathersKey == None):
            return None

        sParentageKey = sMothersKey.strip() + "&" + sFathersKey.strip()
        if sParentageKey == "&":
            return None

        return sParentageKey

    # end def makeParentageKey2()

    # ------------------------------------------------------------
    # Creates dictionary key for parentages
    # ------------------------------------------------------------
    def makeParentageKey4(self, sMothersFirst, sMothersLast, sFathersFirst, sFathersLast):

        sMothersKey = self.makePersonKey(sMothersFirst, sMothersLast)
        sFathersKey = self.makePersonKey(sFathersFirst, sFathersLast)
        if (sMothersKey != None) and (sFathersKey != None):
            return self.makeParentageKey2(sMothersKey, sFathersKey)
        else:
            return None

    # end def makeParentageKey4()

    # ------------------------------------------------------------
    # Creates dictionary key for parentages
    # ------------------------------------------------------------
    def makeParentageKeyEx(self, person1, person2):

        sParentageKey = None

        if (person1.sGender == "F") and (person2.sGender == "M"):
            sParentageKey = self.makeParentageKey4(person1.sFirst, person1.sLast, person2.sFirst, person2.sLast)
        elif (person2.sGender == "F") and (person1.sGender == "M"):
            sParentageKey = self.makeParentageKey4(person2.sFirst, person2.sLast, person1.sFirst, person1.sLast)

        return sParentageKey

    # end def makeParentageKeyEx()

    # -------------------------------------------------------------------
    # Removes all children of the specified parents
    # -------------------------------------------------------------------
    def removeChildren(self, sMothersFirst, sMothersLast, sFathersFirst, sFathersLast):

        sParentageKey = self.makeParentageKey4(sMothersFirst, sMothersLast, sFathersFirst, sFathersLast)
        try:
            lstChildren = self.dctParentages[sParentageKey]
            
            # --------------------------------------------------
            # For all children, clear the values for the parents
            # --------------------------------------------------
            while len(lstChildren) > 0:
                sPersonKey = lstChildren.pop()
                try:
                    person = self.dctPeople[sPersonKey]
                    person.setMothersKey(None)
                    person.setFathersKey(None)
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
    # Sets father for person
    # ------------------------------------------------------------
    def setFather(self, sFirst, sLast, sFathersFirst, sFathersLast):

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey != None:
            try:
                person = self.dctPeople[sPersonKey]
                sFathersKey = self.makePersonKey(sFathersFirst, sFathersLast)
                if sFathersKey != None:
                    person.setFathersKey(sFathersKey)
                    sMothersKey = person.getMothersKey()
                    if sMothersKey != None:
                        self.addToParentages(sPersonKey, sMothersKey, sFathersKey)
                else:
                    print("setfather - father's first and last name required")
            except KeyError:
                print("setfather - person '%s %s' not found" % (sFirst, sLast))
        else:
            print("setfather - person's first and last name required")

        return sPersonKey

    # end def setFather()

    # ------------------------------------------------------------
    # Adds person to parentages dictionary
    # ------------------------------------------------------------
    def addToParentages(self, sPersonKey, sMothersKey, sFathersKey):

        sParentageKey = self.makeParentageKey2(sMothersKey, sFathersKey)
        try:
            lstChildren = self.dctParentages[sParentageKey]
        except KeyError:
            lstChildren = list()
            self.dctParentages[sParentageKey] = lstChildren

        lstChildren.append(sPersonKey)

        return sParentageKey

    # end def addToParentages()

    # ------------------------------------------------------------
    # Sets mother for person
    # ------------------------------------------------------------
    def setMother(self, sFirst, sLast, sMothersFirst, sMothersLast):

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey != None:
            try:
                person = self.dctPeople[sPersonKey]
                sMothersKey = self.makePersonKey(sMothersFirst, sMothersLast)
                if sMothersKey != None:
                    person.setMothersKey(sMothersKey)
                    sFathersKey = person.getFathersKey()
                    if sFathersKey != None:
                        self.addToParentages(sPersonKey, sMothersKey, sFathersKey)
                else:
                    print("setmother - mother's first and last name required")
            except KeyError:
                print("setmother - person '%s %s' not found" % (sFirst, sLast))
        else:
            print("setmother - person's first and last name required")

        return sPersonKey

    # end def setMother()

    # ------------------------------------------------------------
    # Sets partner relationships between parents
    # ------------------------------------------------------------
    def setPartnerKeys(self, sMothersKey, sFathersKey):

        if sMothersKey in self.dctPeople:
            self.dctPeople[sMothersKey].setPartnerKey(sFathersKey)

        if sFathersKey in self.dctPeople:
            self.dctPeople[sFathersKey].setPartnerKey(sMothersKey)

        return

    # end def setPartnerKeys()

    # ------------------------------------------------------------
    # Shows the children of parents based on parent names
    # ------------------------------------------------------------
    def showChildren(self, sMothersFirst, sMothersLast, sFathersFirst, sFathersLast):

        sMothersKey = self.makePersonKey(sMothersFirst, sMothersLast)
        sFathersKey = self.makePersonKey(sFathersFirst, sFathersLast)

        if (sMothersKey != None) and (sFathersKey != None):
            self.showChildren(sMothersKey, sFathersKey)
        else:
            print("showchildren: mother's and father's first and last names are required")

        return

    # def showChildren()

    # ------------------------------------------------------------
    # Shows the children of parents based on parent keys
    # ------------------------------------------------------------
    def showChildren(self, sMothersKey, sFathersKey):

        sMothersFirst, sMothersLast = self.getPersonNames(sMothersKey)
        sFathersFirst, sFathersLast = self.getPersonNames(sFathersKey)

        if (sMothersKey in self.dctPeople) and (sFathersKey in self.dctPeople):
            sParentageKey = self.makeParentageKey2(sMothersKey, sFathersKey)
            if sParentageKey == None:
                dbgPrint(ERR_DBG, ("Family.showChildren: unable to form parentage key"))
                return

            try:
                lstChildren = self.dctParentages[sParentageKey]
                for sPersonKey in lstChildren:
                    person = self.dctPeople[sPersonKey]
                    print("'%s %s' (%s), born: %s" % (person.sFirst, person.sLast, person.sGender, person.sBirthYMD))
            except KeyError as noKids:
                print("showchildren: no children found for mother '%s %s' & father '%s %s'" % 
                        (sMothersFirst, sMothersLast, sFathersFirst, sFathersLast))
        else:
            print("showchildren: mother '%s %s' or father '%s %s' not known" %
                    (sMothersFirst, sMothersLast, sFathersFirst, sFathersLast))

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


# end class Family ############################################

