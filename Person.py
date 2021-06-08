from Utils import *


# #############################################################
# Person: class containing information on a person
# -------------------------------------------------------------
class Person:
    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self, sFirst, sLast, sGender, sBirthYMD):

        dbgPrint(INF_DBG, ("Person[%s %s].__init__: (%s) %s" % 
            (sFirst, sLast, sGender, sBirthYMD)))

        #
        # Store parameters
        #
        self.sFirst     = sFirst
        self.sLast      = sLast
        self.sGender    = sGender
        self.sBirthYMD  = sBirthYMD

        #
        # Initialize class variables
        #
        self.sMothersKey    = None
        self.sFathersKey    = None
        self.sPartnerKey    = None
        self.sBirthCity     = None
        self.sBirthState    = None
        self.sBirthCountry  = None
        self.sBirthPostCode = None

        #
        # Return
        #
        return

    # end def __init__ ()

    # ------------------------------------------------------------
    # Returns birth place for person
    # ------------------------------------------------------------
    def getBirthPlace(self):

        dbgPrint(INF_DBG, ("Person[%s %s].getBirthPlace - returning %s %s %s %s" % 
            (self.sFirst, self.sLast, self.sBirthCity, self.sBirthState, self.sBirthCountry, self.sBirthPostCode)))

        return self.sBirthCity, self.sBirthState, self.sBirthCountry, self.sBirthPostCode

    # end def getBirthPlace()

    # ------------------------------------------------------------
    # Returns father's key for person
    # ------------------------------------------------------------
    def getFathersKey(self):

        dbgPrint(INF_DBG, ("Person[%s %s].getFathersKey - returning %s" % 
            (self.sFirst, self.sLast, self.sFathersKey)))

        return (self.sFathersKey)

    # end def getFathersKey()

    # ------------------------------------------------------------
    # Returns first name for person.
    # ------------------------------------------------------------
    def getFirst(self):

        dbgPrint(INF_DBG, ("Person[%s %s].getFirst - entry" % 
            (self.sFirst, self.sLast)))

        return (self.sFirst)

    # end def getFirst()

    # ------------------------------------------------------------
    # Returns gender for person.
    # ------------------------------------------------------------
    def getGender(self):

        dbgPrint(INF_DBG, ("Person[%s %s].getGender - returning %s" % 
            (self.sFirst, self.sLast, self.sGender)))

        return (self.sGender)

    # end def getGender()

    # ------------------------------------------------------------
    # Returns last name for person.
    # ------------------------------------------------------------
    def getLast(self):

        dbgPrint(INF_DBG, ("Person[%s %s].getLast - entry" % 
            (self.sFirst, self.sLast)))

        return (self.sLast)

    # end def getLast()

    # ------------------------------------------------------------
    # Returns mother's key for person
    # ------------------------------------------------------------
    def getMothersKey(self):

        dbgPrint(INF_DBG, ("Person[%s %s].getMothersKey - returning %s" % 
            (self.sFirst, self.sLast, self.sMothersKey)))

        return (self.sMothersKey)

    # end def getMothersKey()

    # ------------------------------------------------------------
    # Gets partner (with whom to beget children) for person. Only
    # one partner per person at this time.
    # ------------------------------------------------------------
    def getPartnerKey(self):

        dbgPrint(INF_DBG, ("Person[%s %s].getPartnerKey - returning %s" % 
            (self.sFirst, self.sLast, self.sPartnerKey)))

        return (self.sPartnerKey)

    # end def getPartnerKey()

    # ------------------------------------------------------------
    # Sets birth place for person
    # ------------------------------------------------------------
    def setBirthPlace(self, sCity, sState, sCountry, sPostCode):

        dbgPrint(INF_DBG, ("Person[%s %s].setBirthPlace - %s %s %s %s" % 
            (self.sFirst, self.sLast, sCity, sState, sCountry, sPostCode)))

        self.sBirthCity     = sCity
        self.sBirthState    = sState
        self.sBirthCountry  = sCountry
        self.sBirthPostCode = sPostCode

        return

    # end def setBirthPlace()

    # ------------------------------------------------------------
    # Sets birth year, month and date for person
    # ------------------------------------------------------------
    def setBirthYMD(self, sBirthYMD):

        dbgPrint(INF_DBG, ("Person[%s %s].setBirthYMD - from %s to %s" % 
            (self.sFirst, self.sLast, self.sBirthYMD, sBirthYMD)))

        self.sBirthYMD = sBirthYMD

        return

    # end def setBirthYMD()

    # ------------------------------------------------------------
    # Sets father's key for person
    # ------------------------------------------------------------
    def setFathersKey(self, sFathersKey):

        dbgPrint(INF_DBG, ("Person[%s %s].setFathersKey - from %s to %s" %
            (self.sFirst, self.sLast, self.sFathersKey, sFathersKey)))

        self.sFathersKey  = sFathersKey

        return

    # end def setFathersKey()

    # ------------------------------------------------------------
    # Sets gender for person
    # ------------------------------------------------------------
    def setGender(self, sGender):

        dbgPrint(INF_DBG, ("Person[%s %s].setGender - from %s to %s" % 
            (self.sFirst, self.sLast, self.sGender, sGender)))

        self.sGender = sGender

        return

    # end def setGender()

    # ------------------------------------------------------------
    # Sets parents for person
    # ------------------------------------------------------------
    def setMothersKey(self, sMothersKey):

        dbgPrint(INF_DBG, ("Person[%s %s].setsMothersKey - from %s to %s" %
            (self.sFirst, self.sLast, self.sMothersKey, sMothersKey)))

        self.sMothersKey  = sMothersKey

        return

    # end def setsMothersKey()

    # ------------------------------------------------------------
    # Sets partner (with whom to beget children) for person. Only
    # one partner per person at this time.
    # ------------------------------------------------------------
    def setPartnerKey(self, sPartnerKey):

        dbgPrint(INF_DBG, ("Person[%s %s].setPartnerKey - from %s to %s" %
        (self.sFirst, self.sLast, self.sPartnerKey, sPartnerKey)))

        self.sPartnerKey  = sPartnerKey

        return

    # end def setPartner()

    # ------------------------------------------------------------
    # Prints all details of a person
    # ------------------------------------------------------------
    def show(self, dctPeople):

        dbgPrint(INF_DBG, ("Person[%s %s].show - entry" % (self.sFirst, self.sLast)))

        print("***")
        print("First name:    %s" % self.sFirst)
        print("Last name:     %s" % self.sLast)
        print("Gender:        %s" % self.sGender)
        print("Date of birth: %s" % self.sBirthYMD)

        print("---")
        print("City:          %s" % self.sBirthCity)
        print("State:         %s" % self.sBirthState)
        print("Country:       %s" % self.sBirthCountry)
        print("Postal Code:   %s" % self.sBirthPostCode)

        print("---")
        if self.sMothersKey != None:
            try:
                mother = dctPeople[self.sMothersKey]
                print("Mother:        %s %s" % (mother.sFirst, mother.sLast))
            except KeyError:
                print("Mother:        not found")
        else:
            print("Mother:        not known")

        if self.sFathersKey != None:
            try:
                father = dctPeople[self.sFathersKey]
                print("Father:        %s %s" % (father.sFirst, father.sLast))
            except KeyError:
                print("Father:        not found")
        else:
            print("Father:        not known")

        if self.sPartnerKey != None:
            try:
                partner = dctPeople[self.sPartnerKey]
                print("Partner:       %s %s" % (partner.sFirst, partner.sLast))
            except KeyError:
                print("Partner:       not found")
        else:
            print("Partner:       not known")

        return

    # end def show()

# end class Person ############################################

