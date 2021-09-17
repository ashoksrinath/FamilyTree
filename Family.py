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
        self.lstParentRoots = list()

        return

    # end def __init__()

    # ------------------------------------------------------------
    # Adds person to family.  Returns a tuple of (bool, 
    # success-string, error-string), with the success string set to
    # the person-key
    # ------------------------------------------------------------
    def addPerson(self, sFirst, sLast, sGender, sBirthYMD):

        sErrorInfo = ""

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey == None:
            sErrorInfo = "addperson: first and last names are required (try help addperson)\n"
            return (False, sPersonKey, sErrorInfo)

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

        return (True, sPersonKey, None)

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

        sParentageKey = self._makeParentageKey2(sMothersKey, sFathersKey)
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

    # ------------------------------------------------------------
    # Adds parents to the family tree display list
    # ------------------------------------------------------------
    def _addToRoots(self, sPartnerKey1, sPartnerKey2):

        dbgPrint(INF_DBG, ("FamilyTree.addToRoots: partner keys: %s & %s" % (sPartnerKey1, sPartnerKey2)))

        sParentageKey = self._makeParentageKey2(sPartnerKey1, sPartnerKey2)
        if (sParentageKey == None):
            dbgPrint(INF_ERR, ("FamilyTree.addToRoots: parentage key is None; returning"))
            return

        try:
            lstChildren = self.dctParentages[sParentageKey]
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
            if self.dctPeople[sPersonKey].getGender() == "F":
                sPartnerKey = self.dctPeople[sPersonKey].getPartnerKey()
                if sPartnerKey != None:
                    self._addToRoots(sPersonKey, sPartnerKey)

    # end def _addToRoots()

    # ------------------------------------------------------------------------
    # Clears all content
    # ------------------------------------------------------------------------
    def clearAll(self):

        self.dctPeople.clear()
        self.dctParentages.clear()

        return(True, "OK", None)

    # end def clearAll()

    # ------------------------------------------------------------
    # Removes person from family
    # ------------------------------------------------------------
    def delPerson(self, sFirst, sLast):

        sReturnBuff = ""

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey == None:
            sReturnBuff = "delperson: first and last names are required (try help delperson)"
            return(False, None, sReturnBuff)

        if sPersonKey not in self.dctPeople:
            sReturnBuff = "delperson: '%s %s' not found" % (sFirst, sLast)
            return(False, None, sReturnBuff)

        person = self.dctPeople[sPersonKey]

        sMothersKey = person.getMothersKey()
        sFathersKey = person.getFathersKey()
        if (sMothersKey != None) and (sFathersKey != None):
            sParentageKey = self._makeParentageKey2(sMothersKey, sFathersKey)
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

        return(True, "OK", None)

    # end def delPerson()

    # ------------------------------------------------------------------------
    # Checks all entries for referential integrity, removes unknown references
    # ------------------------------------------------------------------------
    def _fixData(self):

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

    # end def _fixData()

    # ------------------------------------------------------------
    # Extracts and returns the person-keys from a parents-key
    # ------------------------------------------------------------
    def _getPersonKeys(self, sParentageKey):

        sPersonKeys = sParentageKey.split('&')

        return sPersonKeys

    # end def _getPersonKeys()

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
    def _getRoots(self):

        lstRoots = list()
        for sParentageKey in self.dctParentages.keys():
            sMothersKey, sFathersKey = self._getPersonKeys(sParentageKey)
            try:
                mother = self.dctPeople[sMothersKey]
                father = self.dctPeople[sFathersKey]
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

    # end def _getRoots()

    # ------------------------------------------------------------
    # Lists all parentages in the family
    # ------------------------------------------------------------
    def listParentages(self):

        sResultBuff = ""

        for sParentageKey, lstChildren in self.dctParentages.items():
            sMotherKey, sFathersKey = self._getPersonKeys(sParentageKey)
            sLine = ("'%s %s' & '%s %s':\n" % (self.dctPeople[sMotherKey].sFirst, self.dctPeople[sMotherKey].sLast,
                                          self.dctPeople[sFathersKey].sFirst, self.dctPeople[sFathersKey].sLast))
            sResultBuff += sLine
            for sPersonKey in lstChildren:
                sFirst, sLast = self.getPersonNames(sPersonKey)
                sLine = ("    '%s %s'\n" % (sFirst, sLast))
                sResultBuff += sLine

        return(True, sResultBuff, None)

    # end def listParentages()

    # ------------------------------------------------------------
    # Lists all people in the family
    # ------------------------------------------------------------
    def listPeople(self):

        sResultBuff = ""

        for sPersonKey in self.dctPeople:
            sLine = ("'%s %s' (%s), born: %s\n" % 
                      (self.dctPeople[sPersonKey].sFirst, self.dctPeople[sPersonKey].sLast, 
                       self.dctPeople[sPersonKey].sGender, self.dctPeople[sPersonKey].sBirthYMD))
            sResultBuff += sLine

        return(sResultBuff)

    # end def listPeople()

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
    def _makeParentageKey2(self, sMothersKey, sFathersKey):

        if (sMothersKey == None) or (sFathersKey == None):
            return None

        sParentageKey = sMothersKey.strip() + "&" + sFathersKey.strip()
        if sParentageKey == "&":
            return None

        return sParentageKey

    # end def _makeParentageKey2()

    # ------------------------------------------------------------
    # Creates dictionary key for parentages
    # ------------------------------------------------------------
    def _makeParentageKey4(self, sMothersFirst, sMothersLast, sFathersFirst, sFathersLast):

        sMothersKey = self.makePersonKey(sMothersFirst, sMothersLast)
        sFathersKey = self.makePersonKey(sFathersFirst, sFathersLast)
        if (sMothersKey != None) and (sFathersKey != None):
            return self._makeParentageKey2(sMothersKey, sFathersKey)
        else:
            return None

    # end def _makeParentageKey4()

    # ------------------------------------------------------------
    # For pretty-printing
    # ------------------------------------------------------------
    def _prettyIndent(self, nLevel, bDash = False):

        sSpaces = ""
        nSpaces = nLevel * 2
        for nSpace in range (0, nSpaces-1):
            sSpaces += " "

        if bDash:
            sSpaces += "-"
        else:
            sSpaces += " "

        return sSpaces

    # end def _printSpaces()

    # -------------------------------------------------------------------
    # Removes all children of the specified parents
    # -------------------------------------------------------------------
    def removeChildren(self, sMothersFirst, sMothersLast, sFathersFirst, sFathersLast):

        sErrorInfo = ""

        sParentageKey = self._makeParentageKey4(sMothersFirst, sMothersLast, sFathersFirst, sFathersLast)
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

            return(True, None, None)
        except KeyError as noKids:
            bSuccess = False
            sLine = ("removechildren: no parentage entry found for mother '%s %s' & father '%s %s'\n" %
                    (sMothersFirst, sMothersLast, sFathersFirst, sFathersLast))
            sErrorInfo += sLine
            return(False, None, sErrorInfo)

        return

    # end def removeChildren()

    # ------------------------------------------------------------
    # Sets birth place for a person
    # ------------------------------------------------------------
    def setBirthPlace(self, sFirst, sLast, sCity, sState, sCountry, sPostCode):

        try:
            person = self.dctPeople[self.makePersonKey(sFirst, sLast)]
            person.setBirthPlace(sCity, sState, sCountry, sPostCode)
            return(True, "OK\n", None)

        except KeyError as noPersonErr:
            sErrorInfo = ("setbirthplc: person '%s %s' not found\n" % (sFirst, sLast))
            return(False, None, sErrorInfo)

    # end def setBirthPlace()

    # ------------------------------------------------------------
    # Sets birthdate for person. Format should be YYYYMMDD
    # ------------------------------------------------------------
    def setBirthYMD(self, sFirst, sLast, sBirthYMD):

        try:
            person = self.dctPeople[self.makePersonKey(sFirst, sLast)]
            person.setBirthYMD(sBirthYMD)
            return(True, "OK\n", None)

        except KeyError as noPersonErr:
            sErrorInfo = ("setbirthymd: person '%s %s' not found\n" % (sFirst, sLast))
            return(False, None, sErrorInfo)

    # end def setBirthYMD()

    # ------------------------------------------------------------
    # Sets father for person
    # ------------------------------------------------------------
    def setFather(self, sFirst, sLast, sFathersFirst, sFathersLast):

        sPersonKey  = None
        sFathersKey = None
        sErrorInfo  = ""

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey == None:
            sErrorInfo = ("setfather - person's first and last name required\n")
            return(False, sErrorInfo, None)

        sFathersKey = self.makePersonKey(sFathersFirst, sFathersLast)
        if sFathersKey == None:
            sErrorInfo = ("setfather - father's first and last name required\n")
            return(False, sErrorInfo, None)

        if not sPersonKey in self.dctPeople:
            sErrorInfo = ("setfather - person '%s %s' not found\n" % (sFirst, sLast))
            return(False, sErrorInfo, None)

        if not sFathersKey in self.dctPeople:
            sErrorInfo = ("setfather - father '%s %s' not found\n" % (sFathersFirst, sFathersLast))
            return(False, sErrorInfo, None)

        person = self.dctPeople[sPersonKey]
        person.setFathersKey(sFathersKey)
        sMothersKey = person.getMothersKey()
        if sMothersKey != None:
            self.addToParentages(sPersonKey, sMothersKey, sFathersKey)

        return(True, sPersonKey, None)

    # end def setFather()

    # ------------------------------------------------------------
    # Sets mother for person
    # ------------------------------------------------------------
    def setMother(self, sFirst, sLast, sMothersFirst, sMothersLast):

        sPersonKey  = None
        sMothersKey = None
        sErrorInfo  = ""

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey == None:
            sErrorInfo = ("setmother - person's first and last name required\n")
            return(False, sErrorInfo, None)

        sMothersKey = self.makePersonKey(sMothersFirst, sMothersLast)
        if sMothersKey == None:
            sErrorInfo = ("setmother - mother's first and last name required\n")
            return(False, sErrorInfo, None)

        if not sPersonKey in self.dctPeople:
            sErrorInfo = ("setmother - person '%s %s' not found\n" % (sFirst, sLast))
            return(False, sErrorInfo, None)

        if not sMothersKey in self.dctPeople:
            sErrorInfo = ("setmother - father '%s %s' not found\n" % (sMothersFirst, sMothersLast))
            return(False, sErrorInfo, None)

        person = self.dctPeople[sPersonKey]
        person.setMothersKey(sMothersKey)
        sFathersKey = person.getFathersKey()
        if sFathersKey != None:
            self.addToParentages(sPersonKey, sMothersKey, sFathersKey)

        return(True, sPersonKey, None)

    # end def setMother()

    # ------------------------------------------------------------
    # Sets partner relationships between parents
    # ------------------------------------------------------------
    def setPartners(self, sMothersFirst, sMothersLast, sFathersFirst, sFathersLast):

        sError = ""

        sMothersKey = self.makePersonKey(sMothersFirst, sMothersLast)
        sFathersKey = self.makePersonKey(sFathersFirst, sFathersLast)
        if (sMothersKey == None) or (sFathersKey == None):
            sError = ("setpartners: mother's and father's first and last names must be specified\n")
            return(False, None, sError)

        if sMothersKey in self.dctPeople:
            self.dctPeople[sMothersKey].setPartnerKey(sFathersKey)
        else:
            sError = ("setpartners: '%s %s' not known\n" %s (sMothersFirst, sMothersLast))
            return(False, None, sError)

        if sFathersKey in self.dctPeople:
            self.dctPeople[sFathersKey].setPartnerKey(sMothersKey)
        else:
            sError = ("setpartners: '%s %s' not known\n" %s (sFathersFirst, sFathersLast))
            return(False, None, sError)

        return(True, "OK\n", None)

    # end def setPartners()

    # ------------------------------------------------------------
    # Shows all descendants of one root in the family tree
    # ------------------------------------------------------------
    def showBranch(self, lstChildren, nLevel, sReturnBuff):

        for sPersonKey in lstChildren:
            mother = None
            father = None

            person = self.dctPeople[sPersonKey]
            sFirst  = person.getFirst()
            sLast   = person.getLast()
            sGender = person.getGender()
            
            sLine = self._prettyIndent(nLevel, True)
            sLine += ("Child: '%s %s' (%s)\n" % (sFirst, sLast, sGender))
            sReturnBuff += sLine

            if sGender == "F":
                mother = self.dctPeople[sPersonKey]
                sPartnerKey = mother.getPartnerKey()
                if sPartnerKey != None:
                    father = self.dctPeople[sPartnerKey]
            elif sGender == "M":
                father = self.dctPeople[sPersonKey]
                sPartnerKey = father.getPartnerKey()
                if sPartnerKey != None:
                    mother = self.dctPeople[sPartnerKey]

            if (mother != None) and (father != None):
                sLine = self._prettyIndent(nLevel)
                sLine += ("'%s %s' & '%s %s':\n" % (mother.sFirst, mother.sLast, father.sFirst, father.sLast))
                sReturnBuff += sLine

                sParentageKey = self._makeParentageKey4(mother.sFirst, mother.sLast, father.sFirst, father.sLast)
                if sParentageKey != None:
                    try:
                        lstChildren2 = self.dctParentages[sParentageKey]
                        sReturnBuff = self.showBranch(lstChildren2, nLevel+1, sReturnBuff)
                    except KeyError:
                        pass

            # end if (mother != None) and (father != None)
        # end for sPersonKey in lstChildren

        return(sReturnBuff)

    # end def showBranch()

    # ------------------------------------------------------------
    # Shows the children of parents based on parent names
    # ------------------------------------------------------------
    def showChildren(self, sMothersFirst, sMothersLast, sFathersFirst, sFathersLast):

        sReturnBuff = ""

        sMothersKey = self.makePersonKey(sMothersFirst, sMothersLast)
        sFathersKey = self.makePersonKey(sFathersFirst, sFathersLast)
        if (not sMothersKey in self.dctPeople) or (not sFathersKey in self.dctPeople):
            sLine = ("showchildren: mother '%s %s' or father '%s %s' not known\n" % \
                (sMothersFirst, sMothersLast, sFathersFirst, sFathersLast))
            sReturnBuff += sLine
            return (False, None, sReturnBuff)

        try:
            lstChildren = self.dctParentages[sParentageKey]
            for sPersonKey in lstChildren:
                person = self.dctPeople[sPersonKey]
                sLine = ("'%s %s' (%s), born: %s\n" % \
                    (person.sFirst, person.sLast, person.sGender, person.sBirthYMD))
                sReturnBuff += sLine

            return (True, sReturnBuff, None)

        except KeyError:
            sLine = ("showchildren: no children found for mother '%s %s' & father '%s %s'\n" % \
                (sMothersFirst, sMothersLast, sFathersFirst, sFathersLast))
            sReturnBuff += sLine
            return (False, None, sReturnBuff)

    # def showChildren()

    # ------------------------------------------------------------
    # Shows all information about a person
    # ------------------------------------------------------------
    def showPerson(self, sFirst, sLast):

        sReturnBuff = ""

        sPersonKey = self.makePersonKey(sFirst, sLast)
        if sPersonKey != None:
            try:
                person = self.dctPeople[sPersonKey]
                sReturnBuff += "****\n"
                sReturnBuff += person.getInfo()
                if person.sMothersKey != None:
                    try:
                        mother = self.dctPeople[person.sMothersKey]
                        sReturnBuff += ("Mother:        %s %s\n" % (mother.sFirst, mother.sLast))
                    except KeyError:
                        sReturnBuff += ("Mother:        not found\n")
                else:
                    sReturnBuff += ("Mother:        not known\n")

                if person.sFathersKey != None:
                    try:
                        father = self.dctPeople[person.sFathersKey]
                        sReturnBuff += ("Father:        %s %s\n" % (father.sFirst, father.sLast))
                    except KeyError:
                        sReturnBuff += ("Father:        not found\n")
                else:
                    sReturnBuff += ("Father:        not known\n")

                if person.sPartnerKey != None:
                    try:
                        partner = self.dctPeople[person.sPartnerKey]
                        sReturnBuff += ("Partner:       %s %s\n" % (partner.sFirst, partner.sLast))
                    except KeyError:
                        sReturnBuff += ("Partner:       not found\n")
                else:
                    sReturnBuff += ("Partner:       not known\n")

                sReturnBuff += "****\n"
            except KeyError:
                sReturnBuff += "showperson: '%s %s' not found\n" % (sFirst, sLast)
        else:
            sReturnBuff += "showperson: first and last names are required\n"

        return sReturnBuff

    # end def showPerson()

    # ------------------------------------------------------------
    # Shows the family tree
    # ------------------------------------------------------------
    def showTree(self):
        
        sReturnBuff = ""

        # -----------------------------------------------------------------
        # Remove mothers, fathers and spouses with no entries in dctPeople.
        # Create list of people with no father and mother (roots)
        # -----------------------------------------------------------------
        self._fixData()      
        lstRoots = self._getRoots()     

        # ---------------------------------------------------------------------------
        # Find roots who are in the parentages dictionary with their partners, show
        # their branches
        # ---------------------------------------------------------------------------
        for sParentageKey in lstRoots:
            sPersonKey1, sPersonKey2 = self._getPersonKeys(sParentageKey)
            if self.dctPeople[sPersonKey1].sGender == "F":
                mother = self.dctPeople[sPersonKey1]
                father = self.dctPeople[sPersonKey2]
            else:
                mother = self.dctPeople[sPersonKey2]
                father = self.dctPeople[sPersonKey1]

            sLine = ("'%s %s' & '%s %s':\n" % 
                (mother.sFirst, mother.sLast, father.sFirst, father.sLast))
            sReturnBuff += sLine

            lstChildren = self.dctParentages[sParentageKey]
            sReturnBuff = self.showBranch(lstChildren, 1, sReturnBuff)

        return(sReturnBuff)

    # end def showTree()

# end class Family ############################################

