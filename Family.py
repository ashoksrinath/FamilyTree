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
        if sPersonKey == None:
            print("addperson: first and last names are required (try help addperson)")
            return None

        if sPersonKey in self.dctPeople:
            person = self.dctPeople[sPersonKey]
            person.setGender(sGender)
            person.setBirthYMD(sBirthYMD)
            dbgPrint (INF_DBG, ("Family.addPerson: updated %s %s %s %s" % 
                                (person.sFirst, person.sLast, person.sGender, person.sBirthYMD)))
        else:
            person = Person(sFirst, sLast, sGender, sBirthYMD)
            self.dctPeople[sPersonKey] = person
            dbgPrint (INF_DBG, ("Family.addPerson: added %s %s %s %s" % 
                                (person.sFirst, person.sLast, person.sGender, person.sBirthYMD)))

        return sPersonKey

    # end def addPerson()

    # ------------------------------------------------------------
    # Adds person to parentages dictionary
    # ------------------------------------------------------------
    def addToParentages(self, sPersonKey, sMothersKey, sFathersKey):

        try:
            mother = self.dctPeople[sMothersKey]
        except KeyError:
            dbgPrint(ERR_DBG, ("Family.addToParentages - error %s not found in dctPeople" % sMothersKey))
            return None

        try:
            father = self.dctPeople[sFathersKey]
        except KeyError:
            dbgPrint(ERR_DBG, ("Family.addToParentages - error %s not found in dctPeople" % sFathersKey))
            return None

        sParentageKey = self.makeParentageKey2(sMothersKey, sFathersKey)
        if sParentageKey == None:
            return None

        mother.setPartnerKey(sFathersKey)
        father.setPartnerKey(sMothersKey)
        if sParentageKey in self.dctParentages:
            lstChildren = self.dctParentages[sParentageKey]
        else:
            lstChildren = list()
            self.dctParentages[sParentageKey] = lstChildren

        lstChildren.append(sPersonKey)

        return sParentageKey

    # end def addToParentages()

    # ------------------------------------------------------------------------
    # Clears all content
    # ------------------------------------------------------------------------
    def clearAll(self):

        self.dctPeople.clear()
        self.dctParentages.clear()

        return

    # end def clearAll()

    # ------------------------------------------------------------
    # Removes person from family
    # ------------------------------------------------------------
    def delPerson(self, sFirst, sLast):

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey == None:
            print("delperson: first and last names are required (try help delperson)")
            return

        if sPersonKey not in self.dctPeople:
            print("delperson: '%s %s' not found" % (sFirst, sLast))
            return

        person = self.dctPeople[sPersonKey]

        sMothersKey = person.getMothersKey()
        sFathersKey = person.getFathersKey()
        if (sMothersKey != None) and (sFathersKey != None):
            sParentageKey = self.makeParentageKey2(sMothersKey, sFathersKey)
            if (sParentageKey != None):
                try:
                    lstChildren = self.dctParentages[sParentageKey]
                    if sPersonKey in lstChildren:
                        lstChildren.remove(sPersonKey)
                        if len(lstChildren) == 0:
                            del self.dctParentages[sParentageKey]
                except KeyError:
                    pass

        del self.dctPeople[sPersonKey]

        return

    # end def delPerson()

    # ------------------------------------------------------------------------
    # Checks all entries for referential integrity, removes unknown references
    # ------------------------------------------------------------------------
    def fixData(self):

        # ------------------------------------------------------------
        # Remove partners, mothers and fathers who aren't in dctPeople
        # ------------------------------------------------------------
        for person in self.dctPeople.values():
            sPartnerKey = person.getPartnerKey()
            if (sPartnerKey != None) and (not sPartnerKey in self.dctPeople):
                dbgPrint(INF_DBG, ("Family.fixData: removing unknown partner key '%s' for '%s %s'" %
                    (sPartnerKey, person.sFirst, person.sLast)))
                person.setPartnerKey(None)

            sMothersKey = person.getMothersKey()
            if (sMothersKey != None) and (not sMothersKey in self.dctPeople):
                dbgPrint(INF_DBG, ("Family.fixData: removing unknown mother's key '%s' for '%s %s'") %
                    (sMothersKey, person.sFirst, person.sLast))
                person.setMothersKey(None)

            sFathersKey = person.getFathersKey()
            if (sFathersKey != None) and (not sFathersKey in self.dctPeople):
                dbgPrint(INF_DBG, ("Family.fixData: removing unknown father's key '%s' for '%s %s'") %
                    (sFathersKey, person.sFirst, person.sLast))
                person.setFathersKey(None)

        # ---------------------------------------------------------------------------
        # Remove children from dctParentages values if their keys aren't in dctPeople
        # ---------------------------------------------------------------------------
        for sParentsKey, lstChildren in self.dctParentages.items():
            bListModified = False
            for nIdx in range(0, len(lstChildren)):
                if not lstChildren[nIdx] in self.dctPeople:
                    dbgPrint(INF_DBG, ("Family.fixData: removing unknown child-key %s for parent key %s" %
                        (lstChildren[nIdx], sParentsKey)))
                    lstChildren[nIdx] = None
                    bListModified = True

            if bListModified:
                self.dctParents[sParentsKey] = list()
                for nIdx in range(0, len(lstChildren)):
                    if lstChildren[nIdx] != None:
                        self.dctParents[sParentsKey].append(lstChildren[nIdx])

        return

    # end def fixData()

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
                if sPersonKey in self.dctPeople:
                    self.dctPeople[sPersonKey].setMothersKey(None)
                    self.dctPeople[sPersonKey].setFathersKey(None)
                else:
                    dbgPrint(ERR_DBG, ("Family.removeChildren - error sPersonKey %s not found" % sPersonKey))

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

        sPersonKey  = None
        sFathersKey = None

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey == None:
            print("setfather - person's first and last name required")
            return None

        sFathersKey = self.makePersonKey(sFathersFirst, sFathersLast)
        if sFathersKey == None:
            print("setfather - father's first and last name required")
            return None

        if not sPersonKey in self.dctPeople:
            print("setfather - person '%s %s' not found" % (sFirst, sLast))
            return None

        if not sFathersKey in self.dctPeople:
            print("setfather - father '%s %s' not found" % (sFathersFirst, sFathersLast))
            return None

        person = self.dctPeople[sPersonKey]
        person.setFathersKey(sFathersKey)
        sMothersKey = person.getMothersKey()
        if sMothersKey != None:
            self.addToParentages(sPersonKey, sMothersKey, sFathersKey)

        return sPersonKey

    # end def setFather()

    # ------------------------------------------------------------
    # Sets mother for person
    # ------------------------------------------------------------
    def setMother(self, sFirst, sLast, sMothersFirst, sMothersLast):

        sPersonKey  = None
        sMothersKey = None

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey == None:
            print("setmother - person's first and last name required")
            return None

        sMothersKey = self.makePersonKey(sMothersFirst, sMothersLast)
        if sMothersKey == None:
            print("setmother - mother's first and last name required")
            return None

        if not sPersonKey in self.dctPeople:
            print("setmother - person '%s %s' not found" % (sFirst, sLast))
            return None

        if not sMothersKey in self.dctPeople:
            print("setmother - father '%s %s' not found" % (sMothersFirst, sMothersLast))
            return None

        person = self.dctPeople[sPersonKey]
        person.setMothersKey(sMothersKey)
        sFathersKey = person.getFathersKey()
        if sFathersKey != None:
            self.addToParentages(sPersonKey, sMothersKey, sFathersKey)

        return sPersonKey

    # end def setMother()

    # ------------------------------------------------------------
    # Sets partner relationships between parents
    # ------------------------------------------------------------
    def setPartners(self, sMothersFirst, sMothersLast, sFathersFirst, sFathersLast):

        sMothersKey = self.makePersonKey(sMothersFirst, sMothersLast)
        sFathersKey = self.makePersonKey(sFathersFirst, sFathersLast)
        if (sMothersKey == None) or (sFathersKey == None):
            print("setpartners: mother's and father's first and last names must be specified")
            return

        if sMothersKey in self.dctPeople:
            self.dctPeople[sMothersKey].setPartnerKey(sFathersKey)
        else:
            print("setpartners: '%s %s' not known" %s (sMothersFirst, sMothersLast))
            return

        if sFathersKey in self.dctPeople:
            self.dctPeople[sFathersKey].setPartnerKey(sMothersKey)
        else:
            print("setpartners: '%s %s' not known" %s (sFathersFirst, sFathersLast))
            return


        return

    # end def setPartners()

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

