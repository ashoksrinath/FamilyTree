import cmd
import sys
import xml.etree.ElementTree as ET 
from enum import Enum



# ############################################################
# Debugging
# ------------------------------------------------------------
# Debug levels:
#   0 - No debug messages
#   1 - Some debug messages
#   2 - Many debug messages
NO_DBG  = 0
ERR_DBG = 1
TRC_DBG = 2

DBGLVL  = NO_DBG

def dbgPrint(sDbgMsg, nDbgLvl):
    if (DBGLVL >= nDbgLvl):
        print (sDbgMsg)

    return

# end def dbgPrint



# ############################################################
# Wait for it...
# -------------------------------------------------------------
def pause(sPrompt):
    sReturn = input (sPrompt)
    return;

# end def pause() ############################################



# #############################################################
# CLI: class to process command line input
# -------------------------------------------------------------
class CLI(cmd.Cmd):
    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self, family):

        super(CLI, self).__init__()

        dbgPrint("CLI.init - entry", TRC_DBG)

        self.dctParams = dict()
        self.seedParamsDict()

        self.family     = family
        self.lstTokens  = None

        return

    # end def __init__()

    # ------------------------------------------------------------
    # Adds a person to the family
    # ------------------------------------------------------------
    def do_addperson(self, line):
        """addperson <first-name> <last-name> <gender> <birthymd>
        Adds a person with first-name <first-name>, last-name <last-name>,
        gender <gender> and birth date <birthymd>.  Gender must be 'M'
        or 'F'.  Birth date must be in YYYYMMDD format.
        e.g., addperson Fir Lastman M 19700101"""

        dbgPrint("CLI.do_addperson - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["addperson"]:
            self.family.addPerson(self.lstTokens[0],    # First  
                                  self.lstTokens[1],    # Last
                                  self.lstTokens[2],    # Gender
                                  self.lstTokens[3])    # Date of birth
        else:
            print ("addperson: invalid parameters (try help)")
        
        return

    # end do_addperson()

    # ------------------------------------------------------------
    # Removes a person from the children for two parents
    # ------------------------------------------------------------
    def do_delparents(self, line):
        """delparents <fathers-first> <fathers-last> <mothers-first> <mothers-last>
        Removes all children of the father of first-name <fathers-first> and last-
        name <fathers-last> with the mother of first-name <mothers-first> and
        last-name <mothers-last>
        e.g., delparents Barack Obama Michelle Obama"""

        dbgPrint("CLI.do_delparents - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["delparents"]:
            self.family.delParents( self.lstTokens[0],  # Father's first
                                    self.lstTokens[1],  # Father's last
                                    self.lstTokens[2],  # Mother's first
                                    self.lstTokens[3])  # Mother's last
        else:
            print ("delparents: invalid parameters (try help)")

    # end do_delparents()

    # ------------------------------------------------------------
    # Deletes a person from the family
    # ------------------------------------------------------------
    def do_delperson(self, line):
        """delperson <first-name> <last-name>
        Deletes all information about a person with first-name
        <first-name> and last-name <last-name>
        e.g., delperson Fir Lastman"""
    
        dbgPrint("CLI.do_delperson - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["delperson"]:
            self.family.delPerson(self.lstTokens[0],  # First 
                                  self.lstTokens[1])  # Last
        else:
            print ("delperson: invalid parameters (try help)")
              
        return

    # end do_delperson()

    # ------------------------------------------------------------
    # Sets the birthplace for a person
    # ------------------------------------------------------------
    def do_setbirthplc(self, line):
        """setbirthplc <first-name> <last-name> <city> <state> <country> <postcode>
        Sets birthplace information for a person with first-name <first-name>
        and last-name <last-name>
        e.g., setbirthplc Fir Lastman Columbus OH USA 43210"""

        dbgPrint("CLI.do_setbirthplc - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["setbirthplc"]:
            self.family.setBirthPlace(self.lstTokens[0],    # First
                                      self.lstTokens[1],    # Last
                                      self.lstTokens[2],    # City
                                      self.lstTokens[3],    # State
                                      self.lstTokens[4],    # Country
                                      self.lstTokens[5])    # Postal code
        else:
            print ("setbirthplc: invalid parameters (try help)")
        
        return

    # end do_setbirthplc()

    # ------------------------------------------------------------
    # Sets the birth date (as YYYYMMDD) for a person
    # ------------------------------------------------------------
    def do_setbirthymd(self, line):
        """setbirthymd <first-name> <last-name> <date-of-birth>
        Sets the birth date (in YYYYMMDD format) for a person with  
        first-name <first-name> and last-name <last-name>.
        e.g., setbirthymd Fir Lastman 20000101"""

        dbgPrint("CLI.do_setbirthymd - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["setbirthymd"]:
            self.family.setBirthYMD (self.lstTokens[0], # First
                                     self.lstTokens[1], # Last
                                    self.lstTokens[2])  # Birthday as YYYYMMDD
        else:
            print ("setbirthymd: invalid parameters (try help)")
        
        return

    # end do_setbirthymd()

    # ------------------------------------------------------------
    # Sets the gender for a person
    # ------------------------------------------------------------
    def do_setgender(self, line):
        """setgender <first-name> <last-name> <gender>
        Sets gender for a person with first-name <first-name> and 
        last-name <last-name> to <gender>, which must be 'M' or 'F'
        e.g., setgender Fir Lastman M"""

        dbgPrint("CLI.do_setbirthplc - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["setgender"]:
            self.family.setGender(  self.lstTokens[0],    # First
                                    self.lstTokens[1],    # Last
                                    self.lstTokens[2])    # Gender
        else:
            print ("setgender: invalid parameters (try help)")
        
        return

    # end do_setgender()

    # ------------------------------------------------------------
    # Shows the children for two parents (father and mother) 
    # ------------------------------------------------------------
    def do_showchildren(self, line):
        """showchildren <fathers-first> <fathers-last> <mothers-first> <mothers-last>
        Shows the children of the father having the first-name <fathers-first> and last-
        name <fathers-last> with the mother having the first-name of <mothers-first> and
        last name of <mothers-last>
        e.g., showchildren Barack Obama Michelle Obama"""

        dbgPrint("CLI.do_showchildren - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["showchildren"]:
            self.family.showChildren(self.lstTokens[0],         # Father's first
                                    self.lstTokens[1],          # Father's last
                                    self.lstTokens[2],          # Mother's first
                                    self.lstTokens[3])          # Mother's last
        else:
            print ("showchildren: invalid parameters (try help)")
        
        return

    # end do_showchildren()

    # ------------------------------------------------------------
    # Shows all parentages
    # ------------------------------------------------------------
    def do_showparentages(self, line):
        """showparentages
        Shows all parentages between people in the family
        e.g., showparentages"""

        dbgPrint("CLI.do_showparentages - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["showparentages"]:
            self.family.showParentages()
        else:
            print ("showparentages: invalid parameters (try help)")
        
        return

    # end do_showparentages()

    # ------------------------------------------------------------
    # Shows all the people in the family
    # ------------------------------------------------------------
    def do_showpeople(self, line):
        """showpeople
        Shows all the people in the family
        e.g., showpeople"""

        dbgPrint("CLI.do_showpeople - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["showpeople"]:
            self.family.showPeople()
        else:
            print ("showpeople: invalid parameters (try help)")
        
        return

    # end do_showpeople()

    # ------------------------------------------------------------
    # Shows all information about a person
    # ------------------------------------------------------------
    def do_showperson(self, line):
        """showperson <first-name> <last-name>
        Shows all information about a person with first-name
        <first-name> and last-name <last-name>
        e.g., showperson Fir Lastman"""

        dbgPrint("CLI.do_showperson - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["showperson"]:
            self.family.showPerson(self.lstTokens[0],   # First
                                   self.lstTokens[1])   # Last
        else:
            print ("showperson: invalid parameters (try help)")
        
        return

    # end do_showperson()

    # ------------------------------------------------------------
    # Sets the parents (father and mother) for a person
    # ------------------------------------------------------------
    def do_addparents(self, line):
        """addparents <first-name> <last-name> <fathers-first> <fathers-last> <mothers-first> <mothers-last>
        Sets the parents of the person with first-name <first-name> and last-name <last-name>. The
        father's first-name is set to <fathers-first> and last name to <father-last>.
        The mother's first-name is set to <mothers-first> and last-name to <mothers-last>
        e.g., addparents Fir Lastman Barack Obama Michelle Obama"""

        dbgPrint("CLI.do_addparents - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["addparents"]:
            self.family.addParents( self.lstTokens[0],  # First
                                    self.lstTokens[1],  # Last
                                    self.lstTokens[2],  # Father's first
                                    self.lstTokens[3],  # Father's last
                                    self.lstTokens[4],  # Mother's first
                                    self.lstTokens[5])  # Mother's last
        else:
            print ("addparents: invalid parameters (try help)")
        
        return

    # end do_addparents()

    # ------------------------------------------------------------
    # Loads data from the parentages XML file
    # ------------------------------------------------------------
    def do_loadparentages(self, line):
        """loadparentages <parentages-xml-file>
        Loads XML data for parentages from <parentages-xml-file>.
        Loading the file is idempotent. Thus, if data for any person
        already exists it will be overwritten. """

        dbgPrint("CLI.do_loadparentages - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["loadparentages"]:
            self.family.loadParentages(self.lstTokens[0])   # XML file

        return

    # end do_loadparentages()

    # ------------------------------------------------------------
    # Loads data from the people XML file
    # ------------------------------------------------------------
    def do_loadpeople(self, line):
        """loadpeople <people-xml-file>
        Loads XML data for people from <people-xml-file>.
        Loading the file is idempotent. Thus, if data for any person
        already exists it will be overwritten. """

        dbgPrint("CLI.do_loadpeople - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["loadpeople"]:
            self.family.loadPeople(self.lstTokens[0])   # XML file

        return

    # end do_loadpeople()

    # ------------------------------------------------------------
    # Loads data from the parentages XML file
    # ------------------------------------------------------------
    def do_saveparentages(self, line):
        """saveparentages <parentages-xml-file>
        Saves XML data for parentages to parentages-xml-file
        if specified.  Otherwise it saves the data to the filename
        specified when the script was started"""

        dbgPrint("CLI.do_saveparentages - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["saveparentages"]:
            self.family.saveParentages(self.lstTokens[0])   # XML file

        return

    # end do_saveparentages()

    # ------------------------------------------------------------
    # Loads data from the parentages XML file
    # ------------------------------------------------------------
    def do_savepeople(self, line):
        """savepeople <people-xml-file>
        Saves XML data for people to <people-xml-file>
        if specified.  Otherwise it saves the data to the filename
        specified when the script was started"""

        dbgPrint("CLI.do_savepeople - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["savepeople"]:
            self.family.savePeople(self.lstTokens[0])   # Specific XML file
        else:
            self.family.savePeople(None)                # Parametric XML file

        return

    # end do_savepeople()

    # ------------------------------------------------------------
    # Exits the CLI
    # ------------------------------------------------------------
    def do_exit(self, line):
        """exit
        Exits this application"""

        dbgPrint("CLI.do_exit - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) != self.dctParams["exit"]:
            print ("exit: invalid parameters (try help)")

        return True

    # end do_exit()

    def do_saveparentages(self, line):
        """saveparentages   parentages-xml-file
        Saves XML data for parentages to a file"""

        dbgPrint("CLI.do_saveparentages - entry", TRC_DBG)

        self.lstTokens = line.split()
        if len(self.lstTokens) == self.dctParams["saveparentages"]:
            self.family.saveParentages(self.lstTokens[0])   # Specific XML file
        else:
            self.family.saveParentages(None)                # Parametric XML file
 
    # end do_saveparentages()

    # ------------------------------------------------------------
    # Seeds dictionary with CLI verbs and required parameter count
    # ------------------------------------------------------------
    def seedParamsDict(self):
        self.dctParams["addperson"]     = 4     # addperson     first last gender birth-date
        self.dctParams["delperson"]     = 2     # delperson     first last
        self.dctParams["showperson"]    = 2     # showperson    first last

        self.dctParams["setbirthplc"]   = 6     # setbirthplc   first last city state country postcode
        self.dctParams["setbirthymd"]   = 3     # setbirthymd   first last birth-date

        self.dctParams["showpeople"]    = 0     # showpeople

        self.dctParams["addparents"]    = 6     # addparents    first last fatherfirst fatherlast motherfirst motherlast
        self.dctParams["delparents"]    = 4     # delparents    fatherfirst fatherlast motherfirst motherlast

        self.dctParams["showparentages"] = 0    # showparentages
        self.dctParams["showchildren"]  = 4     # showchildren  fatherfirst fatherlast motherfirst motherlast

        self.dctParams["loadparentages"] = 1    # loadparentages xml-file-name
        self.dctParams["loadpeople"]    = 1     # loadpeople    xml-file-name

        self.dctParams["saveparentages"] = 1    # saveparentages xml-file-name
        self.dctParams["savepeople"]    = 1     # savepeople    xml-file-name

        self.dctParams["exit"]          = 0     # exit

        return

    # end def seedParamsDict()

# end class CLI ###############################################



# #############################################################
# Person: class containing information on people
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
    # Returns key to this object (first-last)
    # ------------------------------------------------------------
    def getKey(self):

        return (self.sFirstName + "#" + self.sLastName)

    # end def getKey()

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
    def addParents(self, sFathersFirst, sFathersLast, sMothersFirst, sMothersLast):

        self.sFathersFirst  = sFathersFirst
        self.sFathersLast   = sFathersLast 
        self.sMothersFirst  = sMothersFirst
        self.sMothersLast   = sMothersLast 

        return

    # end def addParents()

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



# #############################################################
# Family: class containing information on a family
# -------------------------------------------------------------
class Family:
    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self, sPeopleFile, sParentageFile):
 
        self.sPeopleFile    = sPeopleFile
        self.sParentageFile = sParentageFile

        self.xmlPeople      = None
        self.xmlParentages  = None

        self.dctPeople      = dict()
        self.dctParentages  = dict()

        return

    # end def __init__()

    # ------------------------------------------------------------
    # Adds person to family
    # ------------------------------------------------------------
    def addPerson(self, sFirst, sLast, sGender, sBirthYMD):

        person = Person(sFirst, sLast, sGender, sBirthYMD);

        self.dctPeople[self.makePersonKey(sFirst, sLast)] = person

        return

    # end def addPerson()

    # ------------------------------------------------------------
    # Deletes all children for the specified parents
    # ------------------------------------------------------------
    def delParents(self, sFathersFirst, sFathersLast, sMothersFirst, sMothersLast):

        # ----------------------------
        # Get the parentage dictionary
        # ----------------------------
        sParentageKey = self.makeParentageKey(sFathersFirst, sFathersLast, sMothersFirst, sMothersLast)
        try:
            dctChildren = self.dctParentages[sParentageKey]
            
            # --------------------------------------------------
            # For all children, clear the values for the parents
            # --------------------------------------------------
            for sPersonKey, person in dctChildren.items():
                try:
                    person.addParents("", "", "", "")
                except KeyError as noKid:
                    print("delparents: no parentage entry found for father '" + sFathersFirst + " " + sFathersLast + \
                        "' & mother '" + sMothersFirst + " " + sMothersLast + "'")

            # -------------------------------
            # Delete the parentage dictionary
            # -------------------------------
            del self.dctParentages[sParentageKey]

        except KeyError as noKids:
            print("delparents: no children found for father '" + sFathersFirst + " " + sFathersLast + \
                "' & mother '" + sMothersFirst + " " + sMothersLast + "'")

        return

    # end def delParents()

    # ------------------------------------------------------------
    # Removes person from family
    # ------------------------------------------------------------
    def delPerson(self, sFirst, sLast):

        try:
            del self.dctPeople[self.makePersonKey(sFirst, sLast)]
        except KeyError as noPersonErr:
            print("Person '" + sFirst + " " + sLast + "' not found")

        return

    # end def delPerson()

    # ------------------------------------------------------------
    # Gets user-input from the command-line
    # ------------------------------------------------------------
    def getInput(self):

        cli = CLI(self)
        cli.cmdloop()

        return

    # end def getInput()

    # ------------------------------------------------------------
    # Extracts and returns the person-keys from a parentage-key
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
    # Loads parentages from an XML data file
    # ------------------------------------------------------------
    def loadParentages(self, sXMLfileName):

        try:
            self.ptgRoot = ET.parse("parentages.xml")
            for parentage in self.ptgRoot.iter("parentage"):
                sFathersFirst   = ""
                sFathersLast    = ""
                sMothersFirst   = ""
                sMothersLast    = ""
                for sKey, sValue in parentage.attrib.items():
                    if sKey == "fathersfirst":
                        sFathersFirst = sValue
                    elif sKey == "fatherslast":
                        sFathersLast = sValue
                    elif sKey == "mothersfirst":
                        sMothersFirst = sValue
                    elif sKey == "motherslast":
                        sMothersLast = sValue
                    else:
                        print("loadparentages - unrecognized pair: " + sKey + ": " + sValue)
                sFirstName      = ""
                sLastName       = ""
                for child in parentage[0]:
                    if (child.tag == "first"):
                        sFirstName = child.text
                    elif (child.tag == "last"):
                        sLastName = child.text

                if (len(sFirstName.strip()) > 0) and (len(sLastName.strip()) > 0) and \
                    (len(sFathersFirst.strip()) > 0) and (len(sFathersLast.strip()) > 0) and \
                    (len(sMothersFirst.strip()) > 0) and (len(sMothersLast.strip()) > 0):

                    self.addParents(sFirstName, sLastName, sFathersFirst, sFathersLast, sMothersFirst, sMothersLast)
                else:
                    print("loadpeople - skipping entry first: '" + sFirstName + "' last: '" + sLastName + \
                        "' fathersfirst: '" + sFathersFirst + "' fathersfirst: '" + sFathersLast + \
                        "' mothersfirst: '" + sMothersFirst + "' mothersfirst: '" + sMothersLast + "'")
            # end for parentage in self.ptgRoot.iter("parentage"):
        except FileNotFoundError:
            print("   Parentages-file '" + sXMLfileName + "' not found")
        except ET.ParseError as excParsing:
            print("   Error parsing '" + sXMLfileName + "', skipping")
        except Exception as excUnhandled:
            print("   Unhandled exception parsing '" + sXMLfileName + "', skipping")

        return

    # end def loadParentages()

    # ------------------------------------------------------------
    # Loads people from an XML data file
    # ------------------------------------------------------------
    def loadPeople(self, sXMLfileName):

        try:
            pplRoot = ET.parse(sXMLfileName)
            for person in pplRoot.iter("person"):
                sFirstName  = ""
                sLastName   = ""
                sGender     = ""
                sBirthYMD   = ""
                for sKey, sValue in person.attrib.items():
                    if sKey == "first":
                        sFirstName = sValue
                    elif sKey == "last":
                        sLastName = sValue
                    elif sKey == "gender":
                        sGender = sValue
                    elif sKey == "birthymd":
                        sBirthYMD = sValue
                    else:
                        print("loadpeople - unrecognized pair: " + sKey + ": " + sValue)
        
                if (len(sFirstName.strip()) > 0) and (len(sLastName.strip()) > 0) and (len(sGender.strip()) > 0) and (len(sBirthYMD.strip()) > 0):
                    self.addPerson(sFirstName, sLastName, sGender, sBirthYMD)
                else:
                    print("loadpeople - skipping entry first: '" + sFirstName + "' last: '" + sLastName + \
                        "' gender: '" + sGender + "' birthymd: '" + sBirthYMD + "'")
            # end for person in ptgRoot.iter("person")
        except FileNotFoundError:
            print("loadpeople - file: '" + sXMLfileName + "' not found")
        except ET.ParseError as excParsing:
            print("loadpeople - error parsing file: '" + sXMLfileName + "', skipping")
        except Exception as excUnhandled:
            print("loadpeople - unhandled exception parsing file: '" + sXMLfileName + "', skipping")

        return

    # end def loadPeople()

    # ------------------------------------------------------------
    # Creates key for a person (first-last)
    # ------------------------------------------------------------
    def makePersonKey(self, sFirst, sLast):

        sPersonKey = sFirst + "#" + sLast

        return sPersonKey

    # end def makePersonKey()

    # ------------------------------------------------------------
    # Makes a union key
    # ------------------------------------------------------------
    def makeParentageKey(self, sFatherFirst, sFatherLast, sMotherFirst, sMotherLast):

        sParentageKey = self.makePersonKey(sFatherFirst, sFatherLast) + "&" + self.makePersonKey(sMotherFirst, sMotherLast)

        return sParentageKey

    # end def makeParentageKey()

    # ------------------------------------------------------------
    # Processes input
    # ------------------------------------------------------------
    def processInput(self):

        print("Processing people-file " + self.sPeopleFile + " and parentage-file " + self.sParentageFile + "...")

        self.loadPeople(self.sPeopleFile)

        self.loadParentages(self.sParentageFile)

        self.getInput()

        return

    # end def processInput()

    # ------------------------------------------------------------
    # Saves parentage data to file in XML format
    # ------------------------------------------------------------
    def saveParentages(self, sXMLfileName):

        # ---------------------------------------
        # Ensure that we have an output file-name
        # ---------------------------------------
        sOutputFilename = None
        if (sXMLfileName != None):
            sOutputFilename = sXMLfileName
        else:
            sOutputFilename = self.sParentageFile
        if sOutputFilename == None:
            return

        # --------------------------------
        # Create root element <parentages>
        # --------------------------------
        parentages = ET.Element("parentages")

        # --------------------------------------------------------------------------------------
        # For all parentages, get the keys for the parents, and the dictionary of their children
        # --------------------------------------------------------------------------------------
        for sParentageKey, dctChildren in self.dctParentages.items():
            sFatherKey, sMotherKey = self.getPersonKeys(sParentageKey)

            # -------------------------------------------------------------------------------------------
            # Create subelement <parentage fathersfirst="" fatherslast="" mothersfirst="" motherslast="">
            # -------------------------------------------------------------------------------------------
            parentage = ET.Element("parentage")
            parentage.set("fathersfirst", self.dctPeople[sFatherKey].sFirstName)
            parentage.set("fatherslast", self.dctPeople[sFatherKey].sLastName)
            parentage.set("mothersfirst", self.dctPeople[sMotherKey].sFirstName)
            parentage.set("motherslast", self.dctPeople[sMotherKey].sLastName)
            parentages.append(parentage)

            # ---------------------------------
            # For all children of these parents
            # ---------------------------------
            for sPersonKey in dctChildren:

                child = ET.Element("child")

                # ----------------------------------------------------
                # Set the first, last, gender and birthymd subelements
                # ----------------------------------------------------
                first = ET.SubElement(child, "first")
                first.text = self.dctPeople[sPersonKey].sFirstName

                last = ET.SubElement(child, "last")
                last.text = self.dctPeople[sPersonKey].sLastName

                parentage.append(child)

            # end for sPersonKey in dctChildren
        # end for sParentageKey, dctChildren in self.dctParentages.items()

        # ---------------------------------
        # Create XML tree, write it to file
        # ---------------------------------
        tree = ET.ElementTree(parentages)
        with open(sOutputFilename, "wb") as fhOutputfile:
            tree.write(fhOutputfile)

        return

    # end saveParentages()

    # ------------------------------------------------------------
    # Saves people data to file in XML format
    # ------------------------------------------------------------
    def savePeople(self, sXMLfileName):

        # ---------------------------------------
        # Ensure that we have an output file-name
        # ---------------------------------------
        sOutputFilename = None
        if (sXMLfileName != None):
            sOutputFilename = sXMLfileName
        else:
            sOutputFilename = self.sPeopleFile
        if sOutputFilename == None:
            return

        # --------------------------------
        # Create root element <parentages>
        # --------------------------------
        people = ET.Element("people")

        # -----------------
        # For all people...
        # -----------------
        for sPersonKey in self.dctPeople:

            # ---------------------------------------------------------
            # Create subelement <person>, append it to element <people>
            # ---------------------------------------------------------
            person = ET.Element("person")
            people.append(person)

            # -----------------------------------------------------------------
            # Set the first, last, gender and birthymd subelements for <person>
            # -----------------------------------------------------------------
            first = ET.SubElement(person, "first")
            first.text = self.dctPeople[sPersonKey].sFirstName

            last = ET.SubElement(person, "last")
            last.text = self.dctPeople[sPersonKey].sLastName

            gender = ET.SubElement(person, "gender")
            gender.text = self.dctPeople[sPersonKey].sGender
                
            birthymd = ET.SubElement(person, "birthymd")
            birthymd.text = self.dctPeople[sPersonKey].sBirthYMD

        # end for sPersonKey in self.dctPeople

        # ---------------------------------
        # Create XML tree, write it to file
        # ---------------------------------
        tree = ET.ElementTree(people)
        with open(sOutputFilename, "wb") as fhOutputfile:
            tree.write(fhOutputfile)

        return

    # end savePeople()

    # ------------------------------------------------------------
    # Sets birthdate for person. Format should be YYYYMMDD
    # ------------------------------------------------------------
    def setBirthYMD(self, sFirst, sLast, sBirthYMD):

        try:
            person = self.dctPeople[self.makePersonKey(sFirst, sLast)]
            person.setBirthYMD(sBirthYMD)
        except KeyError as noPersonErr:
            print("setbirthymd: person '" + sFirst + " " + sLast + "' not found")

        return

    # end def setBirthYMD()

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
    # Sets parents for a person
    # ------------------------------------------------------------
    def addParents(self, sFirst, sLast, sFatherFirst, sFatherLast, sMotherFirst, sMotherLast):

        # --------------------------------------------
        # Validate parameters, get reference to person
        # --------------------------------------------
        sPersonKey = self.makePersonKey(sFirst, sLast)
        sFatherKey = self.makePersonKey(sFatherFirst, sFatherLast)
        sMotherKey = self.makePersonKey(sMotherFirst, sMotherLast)
        try:
            person = self.dctPeople[sPersonKey]
            if (not sFatherKey in self.dctPeople) or (not sMotherKey in self.dctPeople):
                print("addparents: one or more parents are not known (try addperson, showpeople)")
            elif (self.dctPeople[sFatherKey].sGender != "M") or (self.dctPeople[sMotherKey].sGender != "F"):
                print("addparents: warning: father's gende is not 'M' or mother's gender is not 'F'")
                return

        except KeyError as noPersonErr:
            print ("addparents: person '" + sFirst + " " + sLast + "' not found")

            return
       
        # ------------------------------------------------------------------------------------------
        # Set/update parents in Person instance.  Find/create Parentage dictionary, add/update child
        # ------------------------------------------------------------------------------------------
        person.addParents(sFatherFirst, sFatherLast, sMotherFirst, sMotherLast)
        sParentageKey = self.makeParentageKey(sFatherFirst, sFatherLast, sMotherFirst, sMotherLast)
        try:
            dctChildren = self.dctParentages[sParentageKey]
        except KeyError as noKids:
            dctChildren = dict()
            self.dctParentages[sParentageKey] = dctChildren           

        dctChildren[sPersonKey] = self.dctPeople[sPersonKey]
 
        return

    # end def addParents()

    # ------------------------------------------------------------
    # Shows the children of two parents 
    # ------------------------------------------------------------
    def showChildren(self, sFatherFirst, sFatherLast, sMotherFirst, sMotherLast):

        # -------------------
        # Validate parameters
        # -------------------
        if  (not self.makePersonKey(sFatherFirst, sFatherLast) in self.dctPeople) or \
            (not self.makePersonKey(sMotherFirst, sMotherLast) in self.dctPeople):
                print("showchildren: father '" + sFatherFirst + " " + sFatherLast + \
                    "' or mother '" + sMotherFirst + " " + sMotherLast + "' not known")

                return

        # --------------------------------------------------------------------------    
        # Create union-key, search for union in dictionary, list children from union
        # --------------------------------------------------------------------------    
        sParentageKey = self.makeParentageKey(sFatherFirst, sFatherLast, sMotherFirst, sMotherLast)
        try:
            dctChildren = self.dctParentages[sParentageKey]
            for sPersonKey in dctChildren:
                print("'" + self.dctPeople[sPersonKey].sFirstName + " " + self.dctPeople[sPersonKey].sLastName + \
                    "' (" + self.dctPeople[sPersonKey].sGender + "), born: " + self.dctPeople[sPersonKey].sBirthYMD)
        except KeyError as noKids:
            print("showchildren: no children found for father '" + sFatherFirst + " " + sFatherLast + \
                "' & mother '" + sMotherFirst + " " + sMotherLast + "'")

        return

    # def showChildren()

    # ------------------------------------------------------------
    # Shows all information about a person
    # ------------------------------------------------------------
    def showPerson(self, sFirst, sLast):

        try:
            person = self.dctPeople[self.makePersonKey(sFirst, sLast)]
            person.show()
        except KeyError as noPersonErr:
            print("Person '" + sFirst + " " + sLast + "' not found")

        return

    # end def showPerson()

    # ------------------------------------------------------------
    # Shows all people in the family
    # ------------------------------------------------------------
    def showPeople(self):

        for sPersonKey in self.dctPeople:
            print("'" + self.dctPeople[sPersonKey].sFirstName + " " + self.dctPeople[sPersonKey].sLastName + \
                "' (" + self.dctPeople[sPersonKey].sGender + "), born: " + self.dctPeople[sPersonKey].sBirthYMD)

        return

    # end def showPeople()

    # ------------------------------------------------------------
    # Shows all unions in the family
    # ------------------------------------------------------------
    def showParentages(self):

        for sParentageKey, dctChildren in self.dctParentages.items():
            sFatherKey, sMotherKey = self.getPersonKeys(sParentageKey)
            print("'" + self.dctPeople[sFatherKey].sFirstName + " " + self.dctPeople[sFatherKey].sLastName + "' & '" + \
                        self.dctPeople[sMotherKey].sFirstName + " " + self.dctPeople[sMotherKey].sLastName + "'")

        return

    # end def showUnions()

# end class Family ############################################



# ############################################################
# MAIN ROUTINE
# -------------------------------------------------------------
# Usage:
#   python3 FamilyTree <people.xml> <parentages.xml> 
#   where: 
#       people.xml = file containing details of people in XML format:
#       <people>
#           <person first="unknown" last="unknown" gender="unknown" birthymd="unknown">
#               <birthcity>"unknown"</birthcity>
#               <birthstate>"unknown"</birthstate>
#               <birthcountry>"unknown"</birthcountry>
#               <birthpostcode>"unknown"</birthpostcode>
#           </person>
#           ...
#           <person>
#               ...
#           </person>
#           ...
#       </people>
#   and:
#       parentages.xml = file containing details of parentages in XML format:
#       <parentages>
#           <parentage fathersfirst="first" fatherslast="last" mothersfirst="first" motherslast="last">
#               <child>
#                   <first>"Unknown"</first>
#                   <last>"Unknown"</last>
#               </child>
#           </parentage>
#           ...
#           <parentage fathersfirst="first" fatherslast="last" mothersfirst="first" motherslast="last">
#               ...
#           </parentage>
#           ...
#       <parentages>
#

if __name__ == "__main__":
    #
    # Initialize file-names
    #
    sPeopleFile = None
    sParentagesFile = None

    #
    # Process command-line arguments
    #
    if len(sys.argv) == 3:
        sPeopleFile = sys.argv[1]
        sParentagesFile = sys.argv[2]

    else:
        sUsage = "Usage: " + "python3 " + sys.argv[0] + " <people.xml> <parentages.xml>"
        print(sUsage)
        pause ("Press return to end")
        sys.exit ()

    try:
        #
        # Create Family instance; pass it the parentages file-name
        #
        family = Family(sPeopleFile, sParentagesFile)

        #
        # Command-line processing
        #
        family.processInput()
    except KeyboardInterrupt:
        print("Thank you for climbing down the tree")
    except Exception as excError:
        print("Unexpected or unhandled exception")
        print(excError)

# end if __name__ == "__main__"
