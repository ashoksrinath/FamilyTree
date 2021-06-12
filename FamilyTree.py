import os
import sys
import threading

from   CLI import CLI
from   Family import Family
from   Utils import *


# ############################################################
# MAIN ROUTINE
# -------------------------------------------------------------
# Usage:
#   python3 FamilyTree.py
#   where: 
#

class FamilyTree:
    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self):
 
        self.family         = Family()
        self.lstParentRoots = list()

        return

    # end def __init__()

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

    # ------------------------------------------------------------
    # Gets and processes input from the command-line
    # ------------------------------------------------------------
    def cmdProcessor(self):

        cli = CLI(self)
        cli.cmdloop()

        return

    # end def cmdProcessor()

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
    # For pretty-printing
    # ------------------------------------------------------------
    def printSpaces(self, nLevel, bDash = False):

        nSpaces = nLevel * 2
        for nSpace in range (0, nSpaces-1):
            print (" ", end=' ')

        print ("-", end=' ') if bDash else print (" ", end=' ')

        return

    # end def printSpaces()

    # ------------------------------------------------------------
    # Shows the family tree
    # ------------------------------------------------------------
    def showTree(self):
        
        # -----------------------------------------------------------------
        # Remove mothers, fathers and spouses with no entries in dctPeople.
        # Create list of people with no father and mother (roots)
        # -----------------------------------------------------------------
        self.family.fixData()      
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
            
            self.printSpaces(nLevel, True)
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
                print ("'%s %s' & '%s %s':" % (mother.sFirst, mother.sLast, father.sFirst, father.sLast))
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

    # ------------------------------------------------------------
    # Gets and processes input from socket connections
    # ------------------------------------------------------------
    def sockProcessor(self, nServerPort):

        self.sockit = Sockit(host="localhost", port=nServerPort)

        return

    # end def sockProcessor()

# end class FamilyTree ########################################


if __name__ == "__main__":
    #
    # Initialize port number
    #
    nServerPort = None

    def print_n_sprint(sAppName):
        print("Usage: python3 %s [server-port]" % sAppName)
        print("       runs interactively on the command-line unless server-port is specified, in which case it")
        print("       runs in the background, accepting connections on server-port.  The server receives commands")
        print("       per the CLI syntax on these connections, and returns responses as formatted strings.")
        pause ("Press return to end")
        sys.exit ()


    #
    # Process command-line arguments
    #
    if len(sys.argv) <= 2:
        if len(sys.argv) == 2:
            try:
                nServerPort = int(sys.argv[1])
            except ValueError:
                print_n_sprint(sys.argv[0])
    else:
        print_n_sprint(sys.argv[0])

    try:
        #
        # Create Family-tree instance
        #
        familyTree = FamilyTree()
        if nServerPort == None:
            familyTree.cmdProcessor()
        else:
            familyTree.sockProcessor(nServerPort)

    except KeyboardInterrupt:
        print("Thank you for climbing down the tree")
    except Exception as excError:
        print("Unexpected or unhandled exception")
        print(excError)

# end if __name__ == "__main__"
