import cmd
from   Utils import *
from   Person import Person

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
        gender <gender> and birth date <birthymd>.  Gender must be 'M' (male)
        or 'F' (female0.  Birth date must be in YYYYMMDD format.
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




