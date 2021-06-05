from   Utils import *


# #############################################################
# Person: class containing information on a person
# -------------------------------------------------------------
class Person:
    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self, sFirstName, sLastName, sGender, sBirthYMD):

        dbgPrint(INF_DBG, ("Person[%s %s].__init__: (%s) %s" % 
            (sFirstName, sLastName, sGender, sBirthYMD)))

        #
        # Store parameters
        #
        self.sFirstName     = sFirstName
        self.sLastName      = sLastName
        self.sGender        = sGender
        self.sBirthYMD      = sBirthYMD 
        self.sMothersKey    = None
        self.sFathersKey    = None
        self.sPartnerKey    = None

        #
        # Initialize birthplace properties
        #
        self.setBirthPlace(None, None, None, None)

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
            (self.sFirstName, self.sLastName, self.sBirthCity, self.sBirthState, self.sBirthCountry, self.sBirthPostCode)))

        return self.sBirthCity, self.sBirthState, self.sBirthCountry, self.sBirthPostCode

    # end def getBirthPlace()

    # ------------------------------------------------------------
    # Returns gender for person.
    # ------------------------------------------------------------
    def getGender(self):

        dbgPrint(INF_DBG, ("Person[%s %s].getGender - returning %s" % 
            (self.sFirstName, self.sLastName, self.sGender)))

        return (self.sGender)

    # end def getGender()

    # ------------------------------------------------------------
    # Returns key to this object (first-last)
    # ------------------------------------------------------------
    def getKey(self):

        dbgPrint(INF_DBG, ("Person[%s %s].getKey - returning %s" % 
            (self.sFirstName, self.sLastName, self.sFirstName + "#" + self.sLastName)))

        return (self.sFirstName + "#" + self.sLastName)

    # end def getKey()

    # ------------------------------------------------------------
    # Gets partner (with whom to beget children) for person. Only
    # one partner per person at this time.
    # ------------------------------------------------------------
    def getPartnerKey(self):

        dbgPrint(INF_DBG, ("Person[%s %s].getPartnerKey - returning %s" % 
            (self.sFirstName, self.sLastName, self.sPartnerKey)))

        return (self.sPartnerKey)

    # end def getPartnerKey()

    # ------------------------------------------------------------
    # Sets birth place for person
    # ------------------------------------------------------------
    def setBirthPlace(self, sCity, sState, sCountry, sPostCode):

        dbgPrint(INF_DBG, ("Person[%s %s].setBirthPlace - %s %s %s %s" % 
            (self.sFirstName, self.sLastName, sCity, sState, sCountry, sPostCode)))

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
            (self.sFirstName, self.sLastName, self.sBirthYMD, sBirthYMD)))

        self.sBirthYMD = sBirthYMD

        return

    # end def setBirthYMD()

    # ------------------------------------------------------------
    # Sets gender for person
    # ------------------------------------------------------------
    def setGender(self, sGender):

        dbgPrint(INF_DBG, ("Person[%s %s].setGender - from %s to %s" % 
            (self.sFirstName, self.sLastName, self.sGender, sGender)))

        self.sGender = sGender

        return

    # end def setGender()

    # ------------------------------------------------------------
    # Sets parents for person
    # ------------------------------------------------------------
    def setParentsKeys(self, sMothersKey, sFathersKey):

        dbgPrint(INF_DBG, ("Person[%s %s].setParentsKeys - mother's: %s father's: %s" %
            (self.sFirstName, self.sLastName, sMothersKey, sFathersKey)))

        self.sMothersKey  = sMothersKey
        self.sFathersKey  = sFathersKey

        return

    # end def setParents()

    # ------------------------------------------------------------
    # Sets partner (with whom to beget children) for person. Only
    # one partner per person at this time.
    # ------------------------------------------------------------
    def setPartnerKey(self, sPartnerKey):

        dbgPrint(INF_DBG, ("Person[%s %s].setPartnerKey - from %s to %s" %
        (self.sFirstName, self.sLastName, self.sPartnerKey, sPartnerKey)))

        self.sPartnerKey  = sPartnerKey

        return

    # end def setPartner()

    # ------------------------------------------------------------
    # Prints all details of a person
    # ------------------------------------------------------------
    def show(self, dctPeople):

        dbgPrint(INF_DBG, ("Person[%s %s].show - entry" % (self.sFirstName, self.sLastName)))

        print("***")
        print("First name:    %s" % self.sFirstName)
        print("Last name:     %s" % self.sLastName)
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
                print("Mother:        %s %s" % (mother.sFirstName, mother.sLastName))
            except KeyError:
                print("Mother:        not found")
        else:
            print("Mother:        not known")

        if self.sFathersKey != None:
            try:
                father = dctPeople[self.sFathersKey]
                print("Father:        %s %s" % (father.sFirstName, father.sLastName))
            except KeyError:
                print("Father:        not found")
        else:
            print("Father:        not known")

        if self.sPartnerKey != None:
            try:
                partner = dctPeople[self.sPartnerKey]
                print("Partner:       %s %s" % (partner.sFirstName, partner.sLastName))
            except KeyError:
                print("Partner:       not found")
        else:
            print("Partner:       not known")

        return

    # end def show()

# end class Person ############################################

