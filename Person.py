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
        self.setParents(None, None)

        #
        # Return
        #
        return

    # end def __init__ ()

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
    # Sets parents for person
    # ------------------------------------------------------------
    def setParents(self, sFatherKey, sMotherKey):

        self.sFatherKey  = sFatherKey
        self.sMotherKey  = sMotherKey

        return

    # end def setParents()

    # ------------------------------------------------------------
    # Sets partner (with whom to beget children) for person. Only
    # one partner per person at this time.
    # ------------------------------------------------------------
    def setPartner(self, sPartnerKey):

        self.sPartnerKey  = sPartnerKey

        return

    # end def setPartner()

    # ------------------------------------------------------------
    # Prints all details of a person
    # ------------------------------------------------------------
    def show(self, dctPeople):

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
        if self.sMotherKey != None:
            try:
                mother = dctPeople[self.sMotherKey]
                print("Mother: %s %s" % (mother.sFirstName, mother.sLastName))
            except KeyError:
                print("Mother: not found")
        else:
            print("Mother: not known")

        if self.sFatherKey != None:
            try:
                father = dctPeople[self.sFatherKey]
                print("Father: %s %s" % (father.sFirstName, father.sLastName))
            except KeyError:
                print("Father: not found")
        else:
            print("Father: not known")

        if self.sPartnerKey != None:
            try:
                partner = dctPeople[self.sPartnerKey]
                print("Partner: %s %s" % (partner.sFirstName, partner.sLastName))
            except KeyError:
                print("Partner: not found")
        else:
            print("Partner: not known")

        return

    # end def show()

# end class Person ############################################

