from Utils import *


# #############################################################
# Person: class containing information on a person
# -------------------------------------------------------------
class Person:
    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self, sFirst, sLast, sGender, sBirthYMD):

        dbgPrint(INF_DBG, ("Person.__init__[%s %s]: (%s) %s" % 
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

        dbgPrint(INF_DBG, ("Person.getBirthPlace[%s %s] - returning %s %s %s %s" % 
            (self.sFirst, self.sLast, self.sBirthCity, self.sBirthState, self.sBirthCountry, self.sBirthPostCode)))

        return self.sBirthCity, self.sBirthState, self.sBirthCountry, self.sBirthPostCode

    # end def getBirthPlace()

    # ------------------------------------------------------------
    # Returns father's key for person
    # ------------------------------------------------------------
    def getFathersKey(self):

        dbgPrint(INF_DBG, ("Person.getFathersKey[%s %s] - returning %s" % 
            (self.sFirst, self.sLast, self.sFathersKey)))

        return self.sFathersKey

    # end def getFathersKey()

    # ------------------------------------------------------------
    # Returns first name for person.
    # ------------------------------------------------------------
    def getFirst(self):

        dbgPrint(INF_DBG, ("Person.getFirst[%s %s]" % 
            (self.sFirst, self.sLast)))

        return self.sFirst

    # end def getFirst()

    # ------------------------------------------------------------
    # Returns gender for person.
    # ------------------------------------------------------------
    def getGender(self):

        dbgPrint(INF_DBG, ("Person.getGender[%s %s] - returning %s" % 
            (self.sFirst, self.sLast, self.sGender)))

        return self.sGender

    # end def getGender()

    # ------------------------------------------------------------
    # Returns all details of a person
    # ------------------------------------------------------------
    def getInfo(self):

        sReturnBuff = ""

        dbgPrint(INF_DBG, ("Person.getInfo[%s %s] - entry" % (self.sFirst, self.sLast)))

        sReturnBuff += ("First name:    %s\n" % self.sFirst)
        sReturnBuff += ("Last name:     %s\n" % self.sLast)
        sReturnBuff += ("Gender:        %s\n" % self.sGender)
        sReturnBuff += ("Date of birth: %s\n" % self.sBirthYMD)

        sReturnBuff += ("---\n")

        sReturnBuff += ("City:          %s\n" % self.sBirthCity)
        sReturnBuff += ("State:         %s\n" % self.sBirthState)
        sReturnBuff += ("Country:       %s\n" % self.sBirthCountry)
        sReturnBuff += ("Postal Code:   %s\n" % self.sBirthPostCode)

        return sReturnBuff

    # end def getInfo()

    # ------------------------------------------------------------
    # Returns last name for person.
    # ------------------------------------------------------------
    def getLast(self):

        dbgPrint(INF_DBG, ("Person.getLast[%s %s]" % 
            (self.sFirst, self.sLast)))

        return self.sLast

    # end def getLast()

    # ------------------------------------------------------------
    # Returns mother's key for person
    # ------------------------------------------------------------
    def getMothersKey(self):

        dbgPrint(INF_DBG, ("Person.getMothersKey[%s %s] - returning %s" % 
            (self.sFirst, self.sLast, self.sMothersKey)))

        return self.sMothersKey

    # end def getMothersKey()

    # ------------------------------------------------------------
    # Gets partner (with whom to beget children) for person. Only
    # one partner per person at this time.
    # ------------------------------------------------------------
    def getPartnerKey(self):

        dbgPrint(INF_DBG, ("Person.getPartnerKey[%s %s] - returning %s" % 
            (self.sFirst, self.sLast, self.sPartnerKey)))

        return self.sPartnerKey

    # end def getPartnerKey()

    # ------------------------------------------------------------
    # Sets birth place for person
    # ------------------------------------------------------------
    def setBirthPlace(self, sCity, sState, sCountry, sPostCode):

        dbgPrint(INF_DBG, ("Person.setBirthPlace[%s %s] - %s %s %s %s" % 
            (self.sFirst, self.sLast, sCity, sState, sCountry, sPostCode)))

        self.sBirthCity     = sCity
        self.sBirthState    = sState
        self.sBirthCountry  = sCountry
        self.sBirthPostCode = sPostCode

        return True

    # end def setBirthPlace()

    # ------------------------------------------------------------
    # Sets birth year, month and date for person
    # ------------------------------------------------------------
    def setBirthYMD(self, sBirthYMD):

        dbgPrint(INF_DBG, ("Person.setBirthYMD[%s %s] - from %s to %s" % 
            (self.sFirst, self.sLast, self.sBirthYMD, sBirthYMD)))

        self.sBirthYMD = sBirthYMD

        return True

    # end def setBirthYMD()

    # ------------------------------------------------------------
    # Sets father's key for person
    # ------------------------------------------------------------
    def setFathersKey(self, sFathersKey):

        dbgPrint(INF_DBG, ("Person.setFathersKey[%s %s] - from %s to %s" %
            (self.sFirst, self.sLast, self.sFathersKey, sFathersKey)))

        self.sFathersKey  = sFathersKey

        return True

    # end def setFathersKey()

    # ------------------------------------------------------------
    # Sets gender for person
    # ------------------------------------------------------------
    def setGender(self, sGender):

        dbgPrint(INF_DBG, ("Person.setGender[%s %s] - from %s to %s" % 
            (self.sFirst, self.sLast, self.sGender, sGender)))

        self.sGender = sGender

        return True

    # end def setGender()

    # ------------------------------------------------------------
    # Sets parents for person
    # ------------------------------------------------------------
    def setMothersKey(self, sMothersKey):

        dbgPrint(INF_DBG, ("Person.setsMothersKey[%s %s] - from %s to %s" %
            (self.sFirst, self.sLast, self.sMothersKey, sMothersKey)))

        self.sMothersKey  = sMothersKey

        return True

    # end def setsMothersKey()

    # ------------------------------------------------------------
    # Sets key for partner (with whom to beget children) for person.
    # Only one partner per person is supported at this time.
    # ------------------------------------------------------------
    def setPartnerKey(self, sPartnerKey):

        dbgPrint(INF_DBG, ("Person.setPartnerKey[%s %s] - from %s to %s" %
            (self.sFirst, self.sLast, self.sPartnerKey, sPartnerKey)))

        self.sPartnerKey  = sPartnerKey

        return True

    # end def setPartnerKey()

# end class Person ############################################

