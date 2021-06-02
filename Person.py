from   Utils import *


# #############################################################
# Person: class containing information on a person
# -------------------------------------------------------------
class Person:
    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self, sFirstName, sLastName, sGender, sBirthYMD):

        dbgPrint(TRC_DBG, ("Person.__init__: %s %s (%s) %s" % (sFirstName, sLastName, sGender, sBirthYMD)))

        #
        # Store parameters
        #
        self.sFirstName     = sFirstName
        self.sLastName      = sLastName
        self.sGender        = sGender
        self.sBirthYMD      = sBirthYMD 
        self.sMothersKey    = None
        self.sFathersKey    = None
        self.sPartnersKey   = None

        #
        # Initialize birthplace properties
        #
        self.setBirthPlace("", "", "", "")

        #
        # Return
        #
        return

    # end def __init__ ()

    # ------------------------------------------------------------
    # Returns key to this object (first-last)
    # ------------------------------------------------------------
    def getKey(self):

        dbgPrint(TRC_DBG, "Person.getKey - entry")

        return (self.sFirstName + "#" + self.sLastName)

    # end def getKey()

    # ------------------------------------------------------------
    # Gets partner (with whom to beget children) for person. Only
    # one partner per person at this time.
    # ------------------------------------------------------------
    def getPartnersKey(self):

        dbgPrint(TRC_DBG, "Person.getPartnersKey - entry")

        return (self.sPartnersKey)

    # end def getPartnersKey()

    # ------------------------------------------------------------
    # Sets birth place for person
    # ------------------------------------------------------------
    def setBirthPlace(self, sCity, sState, sCountry, sPostCode):

        dbgPrint(TRC_DBG, "Person.setBirthPlace - entry")

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

        dbgPrint(TRC_DBG, "Person.setBirthYMD - entry")

        if sBirthYMD != None:
            dbgPrint(TRC_DBG, ("Person.setBirthYMD - changing %s to %s % (self.sBirthYMD, sBirthYMD"))
            self.sBirthYMD = sBirthYMD

        return

    # end def setBirthYMD()

    # ------------------------------------------------------------
    # Sets gender for person
    # ------------------------------------------------------------
    def setGender(self, sGender):

        dbgPrint(TRC_DBG, "Person.setGender - entry")

        self.sGender = sGender

        return

    # end def setGender()

    # ------------------------------------------------------------
    # Sets parents for person
    # ------------------------------------------------------------
    def setParents(self, sMothersKey, sFathersKey):

        dbgPrint(TRC_DBG, "Person.setParents - entry")

        self.sMothersKey  = sMothersKey
        self.sFathersKey  = sFathersKey

        return

    # end def setParents()

    # ------------------------------------------------------------
    # Sets partner (with whom to beget children) for person. Only
    # one partner per person at this time.
    # ------------------------------------------------------------
    def setPartner(self, sPartnersKey):

        dbgPrint(TRC_DBG, "Person.setPartner - entry")

        self.sPartnersKey  = sPartnersKey

        return

    # end def setPartner()

    # ------------------------------------------------------------
    # Prints all details of a person
    # ------------------------------------------------------------
    def show(self, dctPeople):

        dbgPrint(TRC_DBG, "Person.show - entry")

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

        if self.sPartnersKey != None:
            try:
                partner = dctPeople[self.sPartnersKey]
                print("Partner:       %s %s" % (partner.sFirstName, partner.sLastName))
            except KeyError:
                print("Partner:       not found")
        else:
            print("Partner:       not known")

        return

    # end def show()

# end class Person ############################################

