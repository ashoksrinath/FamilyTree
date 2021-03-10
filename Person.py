from   Utils import *


# #############################################################
# Person: class containing information on a person
# -------------------------------------------------------------
class Person:
    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self, sFirstName, sLastName, sGender, sBirthYMD):
        #
        # Store parameters
        #
        self.sFirstName     = sFirstName
        self.sLastName      = sLastName
        self.sGender        = sGender
        self.sBirthYMD      = sBirthYMD 
        self.sPartnerKey    = None

        #
        # Initialize birthplace properties
        #
        self.setBirthPlace("", "", "", "")

        #
        # Initialize parent names
        #
        self.addParents("", "", "", "")

        #
        # Return
        #
        return

    # end def __init__ ()

    # ------------------------------------------------------------
    # Sets parents for person
    # ------------------------------------------------------------
    def addParents(self, sFathersFirst, sFathersLast, sMothersFirst, sMothersLast):

        self.sFathersFirst  = sFathersFirst
        self.sFathersLast   = sFathersLast 
        self.sMothersFirst  = sMothersFirst
        self.sMothersLast   = sMothersLast 

        return

    # end def addParents()

    # ------------------------------------------------------------
    # Returns key to this object (first-last)
    # ------------------------------------------------------------
    def getKey(self):

        return (self.sFirstName + "#" + self.sLastName)

    # end def getKey()

    # ------------------------------------------------------------
    # Sets partner (with whom to beget children) for person. Only
    # one partner per person at this time.
    # ------------------------------------------------------------
    def getPartnerKey(self, sPartnerKey):

        return (self.sPartnerKey)

    # end def getPartnerKey()

    # ------------------------------------------------------------
    # Sets birth place for person
    # ------------------------------------------------------------
    def setBirthPlace(self, sCity, sState, sCountry, sPostCode):

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

        self.sBirthYMD     = sBirthYMD

        return

    # end def setBirthYMD()

    # ------------------------------------------------------------
    # Sets gender for person
    # ------------------------------------------------------------
    def setGender(self, sGender):

        self.sGender     = sGender

        return

    # end def setGender()

    # ------------------------------------------------------------
    # Sets partner (with whom to beget children) for person. Only
    # one partner per person at this time.
    # ------------------------------------------------------------
    def setPartnerKey(self, sPartnerKey):

        self.sPartnerKey  = sPartnerKey

        return

    # end def setPartner()

    # ------------------------------------------------------------
    # Prints all details of a person
    # ------------------------------------------------------------
    def show(self):

        print("***")
        print("First name: " + self.sFirstName)
        print("Last name: " + self.sLastName)
        print("Gender: " + self.sGender)
        print("Date of birth (Year, Month, Date): " + self.sBirthYMD)

        print("---")
        print("City: " + self.sBirthCity)
        print("State: " + self.sBirthState)
        print("Country: " + self.sBirthCountry)
        print("Postal Code: " + self.sBirthPostCode)

        print("---")
        print("Fathers First: " + self.sFathersFirst)
        print("Fathers Last: " + self.sFathersLast)
        print("Mothers First: " + self.sMothersFirst)
        print("Mothers Last: " + self.sMothersLast)

        return

    # end def show()

# end class Person ############################################

