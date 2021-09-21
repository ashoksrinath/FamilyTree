import cmd
from   Person import Person
from   Utils import *
from   XMLParser import XMLParser

# #############################################################
# CLI: class to process command line input
# -------------------------------------------------------------
class CLI(cmd.Cmd):
    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self, family):

        super(CLI, self).__init__()

        dbgPrint(INF_DBG, "CLI.__init__ - entry")

        self.family = family

        return

    # end def __init__()

    # ------------------------------------------------------------
    # Adds a person to the family
    # ------------------------------------------------------------
    def do_addperson(self, line):
        """addperson <first-name> <last-name> <gender> <birthymd>
        Adds a person with first-name <first-name>, last-name <last-name>,
        gender <gender> and birth date <birthymd>.  Gender must be 'M' (male)
        or 'F' (female).  Birth date must be in YYYYMMDD format.
        e.g., addperson Baby Bear M 19700101"""

        dbgPrint(INF_DBG, "CLI.do_addperson - entry")

        lstTokens = line.split()
        if len(lstTokens) == 4:
            bSuccess, sPersonKey, sError = self.family.addPerson(lstTokens[0],  # First
                                                                lstTokens[1],   # Last
                                                                lstTokens[2],   # Gender
                                                                lstTokens[3])   # BirthYMD
            if not bSuccess:
                print(sError, end='')
        else:
            print ("addperson: invalid parameters (try help addperson)")
        
        return

    # end do_addperson()

    # ------------------------------------------------------------
    # Clears all content
    # ------------------------------------------------------------
    def do_clearall(self, line):
        """clearall
        Clears all content - people, partnerships, etc.
        e.g., clearall"""

        dbgPrint(INF_DBG, "CLI.do_clearall - entry")

        lstTokens = line.split()
        if len(lstTokens) == 0:
            bSuccess, sSuccess, sFailure = self.family.clearAll()
        else:
            print ("clearall: invalid parameters (try help clearall)")

        return

    # end do_clearall()

    # ------------------------------------------------------------
    # Deletes a person from the family
    # ------------------------------------------------------------
    def do_delperson(self, line):
        """delperson <first-name> <last-name>
        Deletes all information about a person with first-name
        <first-name> and last-name <last-name>
        e.g., delperson Baby Bear"""
    
        dbgPrint(INF_DBG, "CLI.do_delperson - entry")

        lstTokens = line.split()
        if len(lstTokens) == 2:
            bSuccess, sSuccess, sFailure = self.family.delPerson(lstTokens[0],  # First 
                                                                lstTokens[1])   # Last
            print(sSuccess) if bSuccess else print(sFailure)
        else:
            print ("delperson: invalid parameters (try 'help delperson')")
              
        return

    # end do_delperson()

    # ------------------------------------------------------------
    # Exits the CLI
    # ------------------------------------------------------------
    def do_exit(self, line):
        """exit
        Exits this application
        e.g., exit"""

        dbgPrint(INF_DBG, "CLI.do_exit - entry")

        lstTokens = line.split()
        if len(lstTokens) != 0:
            print ("exit: invalid parameters (try help exit)")

        return True

    # end do_exit()

    # ------------------------------------------------------------
    # Lists all partners in the family
    # ------------------------------------------------------------
    def do_listpartners(self, line):
        """listpartners
        Lists all partners between people in the family
        e.g., listpartners"""

        dbgPrint(INF_DBG, "CLI.do_listpartners - entry")

        lstTokens = line.split()
        if len(lstTokens) == 0:
            bSuccess, sSuccess, sFailure = self.family.listPartnerships()
            print(sSuccess) if bSuccess else print(sFailure)
        else:
            print ("listpartners: invalid parameters (try help listpartners)")
        
        return

    # end do_listpartners()

    # ------------------------------------------------------------
    # Lists all the people in the family
    # ------------------------------------------------------------
    def do_listpeople(self, line):
        """listpeople
        Lists all the people in the family
        e.g., listpeople"""

        dbgPrint(INF_DBG, "CLI.do_listpeople - entry")

        lstTokens = line.split()
        if len(lstTokens) == 0:
            sResult = self.family.listPeople()
            print(sResult)
        else:
            print ("listpeople: invalid parameters (try help listpeople)")
        
        return

    # end do_listpeople()

    # ------------------------------------------------------------
    # Loads data from the people XML file
    # ------------------------------------------------------------
    def do_loadfile(self, line):
        """loadfile <xml-file>
        Loads XML data for people from <xml-file>.
        Loading the file is idempotent. Thus, if data for any person
        already exists it will be overwritten.
        e.g., loadfile myfamilytree.xml"""

        dbgPrint(INF_DBG, "CLI.do_loadfile - entry")

        lstTokens = line.split()
        if len(lstTokens) == 1:
            xmlParser = XMLParser()
            bSuccess, sSuccess, sFailure = xmlParser.loadFile(  lstTokens[0],  # XML file 
                                                                self.family)   # Family instance to populate from XML file
            print(sSuccess) if bSuccess else print(sFailure)
        else:
            print ("loadfile: invalid parameters (try help loadfile)")

        return

    # end do_loadfile()

    # ------------------------------------------------------------
    # Removes the children for specified parents
    # ------------------------------------------------------------
    def do_removechildren(self, line):
        """removechildren <mothers-first> <mothers-last> <fathers-first> <fathers-last>
        Removes all children of the mother named '<mothers-first>, <mothers-last>' and 
        father named '<fathers-first> <fathers-last>'
        e.g., removechildren Mamma Bear Papa Bear"""

        dbgPrint(INF_DBG, "CLI.do_removechildren - entry")

        lstTokens = line.split()
        if len(lstTokens) == 4:
            bSuccess, sSuccess, sFailure = self.family.removeChildren(  lstTokens[0],  # Mother's first
                                                                        lstTokens[1],  # Mother's last
                                                                        lstTokens[2],  # Father's first
                                                                        lstTokens[3])  # Father's last
            print(sSuccess) if bSuccess else print(sFailure)
        else:
            print ("removechildren: invalid parameters (try help removechildren)")

    # end do_removechildren()

    # ------------------------------------------------------------
    # Saves data to the people XML file
    # ------------------------------------------------------------
    def do_savefile(self, line):
        """savefile <xml-file>
        Saves XML data for people to specified <xml-file>
        e.g., savefile familytree.xml"""

        lstTokens = line.split()
        if len(lstTokens) == 1:
            dbgPrint(INF_DBG, ("CLI.do_savefile - %s" % lstTokens[0]))
            xmlParser = XMLParser()
            bSuccess, sSuccess, sFailure = xmlParser.saveFile(  lstTokens[0],  # Output XML filename
                                                                self.family)   # Family instance to populate from XML file
            print(sSuccess) if bSuccess else print(sFailure)
        else:
            print ("savefile: invalid parameters (try 'help savefile')")

        return

    # end do_savefile()

    # ------------------------------------------------------------
    # Sets the birthplace for a person
    # ------------------------------------------------------------
    def do_setbirthplc(self, line):
        """setbirthplc <first-name> <last-name> <city> <state> <country> <postcode>
        Sets birthplace information for a person with first-name <first-name>
        and last-name <last-name>
        e.g., setbirthplc Baby Bear Goldieloque CA USA 12345
        Parameters with white spaces must be enclose within double quotes.
        e.g., setbirthplc Baby Bear "Goldie Loch" CA USA 12345

        """

        dbgPrint(INF_DBG, "CLI.do_setbirthplc - entry")

        if '"' in line:
            lstTmp = line.split()
            lstTokens = list()

            sFullString = None
            for sToken in lstTmp:
                if sToken.startswith('"'):
                    sFullString = sToken[1:]
                elif sToken.endswith('"'):
                    sFullString = sFullString + " " + sToken[:-1]
                    lstTokens.append(sFullString)
                else:
                    lstTokens.append(sToken)
        else:
            lstTokens = line.split()

        if len(lstTokens) == 6:
            bSuccess, sSuccess, sFailure = self.family.setBirthPlace(lstTokens[0],   # First-name
                                                                    lstTokens[1],    # Last-name
                                                                    lstTokens[2],    # City
                                                                    lstTokens[3],    # State
                                                                    lstTokens[4],    # Country
                                                                    lstTokens[5])    # Postal code
            print(sSuccess) if bSuccess else print(sFailure)
        else:
            print ("setbirthplc: invalid parameters (try 'help setbirthplc')")
        
        return

    # end do_setbirthplc()

    # ------------------------------------------------------------
    # Sets the birth date (as YYYYMMDD) for a person
    # ------------------------------------------------------------
    def do_setbirthymd(self, line):
        """setbirthymd <first-name> <last-name> <date-of-birth>
        Sets the birth date (in YYYYMMDD format) for a person with  
        first-name <first-name> and last-name <last-name>.
        e.g., setbirthymd Baby Bear 20000101"""

        dbgPrint(INF_DBG, "CLI.do_setbirthymd - entry")

        lstTokens = line.split()
        if len(lstTokens) == 3:
            bSuccess, sSuccess, sFailure = self.family.setBirthYMD (lstTokens[0],  # First
                                                                    lstTokens[1],   # Last
                                                                    lstTokens[2])   # Birthday as YYYYMMDD
            print(sSuccess) if bSuccess else print(sFailure)
        else:
            print ("setbirthymd: invalid parameters (try help setbirthymd)")
        
        return

    # end do_setbirthymd()

    # ------------------------------------------------------------
    # Sets the father for a person
    # ------------------------------------------------------------
    def do_setfather(self, line):
        """setfather <first-name> <last-name> <fathers-first> <fathers-last>
        Sets the father for the person with first-name <first-name> and last-name <last-name>. 
        The father's first-name is set to <fathers-first> and last-name to <father-last>
        e.g., setfather Baby Bear Papa Bear"""

        dbgPrint(INF_DBG, "CLI.do_setfather - entry")

        lstTokens = line.split()
        if len(lstTokens) == 4:
            bSuccess, sSuccess, sFailure = self.family.setFather(lstTokens[0],  # First
                                                                lstTokens[1],   # Last
                                                                lstTokens[2],   # Father's first
                                                                lstTokens[3])   # Father's last
            print(sSuccess) if bSuccess else print(sFailure)
        else:
            print ("setfather: invalid parameters (try help setfather)")
        
        return

    # end do_setfather()

    # ------------------------------------------------------------
    # Sets the gender for a person
    # ------------------------------------------------------------
    def do_setgender(self, line):
        """setgender <first-name> <last-name> <gender>
        Sets gender for a person with first-name <first-name> and 
        last-name <last-name> to <gender>, which must be 'M' or 'F'
        e.g., setgender Baby Bear M"""

        dbgPrint(INF_DBG, "CLI.do_setgender - entry")

        lstTokens = line.split()
        if len(lstTokens) == 3:
            bSuccess, sSuccess, sFailure = self.family.setGender(lstTokens[0],   # First
                                                                lstTokens[1],   # Last
                                                                lstTokens[2])   # Gender
            print(sSuccess) if bSuccess else print(sFailure)
        else:
            print ("setgender: invalid parameters (try help setgender)")
        
        return

    # end do_setgender()

    # ------------------------------------------------------------
    # Sets the mother for a person
    # ------------------------------------------------------------
    def do_setmother(self, line):
        """setmother <first-name> <last-name> <mothers-first> <mothers-last>
        Sets the mother for the person with first-name <first-name> and last-name <last-name>. 
        The mother's first-name is set to <mothers-first> and last name to <mothers-last>.
        e.g., setmother Baby Bear Mamma Bear"""

        dbgPrint(INF_DBG, "CLI.do_setmother - entry")

        lstTokens = line.split()
        if len(lstTokens) == 4:
            bSuccess, sSuccess, sFailure = self.family.setMother(lstTokens[0],  # First
                                                                lstTokens[1],  # Last
                                                                lstTokens[2],  # Mother's first
                                                                lstTokens[3])  # Mother's last
            print(sSuccess) if bSuccess else print(sFailure)
        else:
            print ("setmother: invalid parameters (try help setmother)")
        
        return

    # end do_setmother()

    # ------------------------------------------------------------
    # Sets a partnering relationship between two people
    # ------------------------------------------------------------
    def do_setpartners(self, line):
        """setpartners <mothers-first> <mothers-last> <fathers-first> <fathers-last>
        Sets a partnering relationship between a woman with first-name <mothers-last>
         and last-name <mothers-last> and a man with first-name <fathers-last> and 
        last-name <fathers-last>
        e.g., setpartners Mamma Bear Papa Bear"""

        dbgPrint(INF_DBG, "CLI.do_setpartners - entry")

        lstTokens = line.split()
        if len(lstTokens) == 4:
            bSuccess, sSuccess, sFailure = self.family.setPartners( lstTokens[0],  # Mother's first
                                                                    lstTokens[1],  # Mother's last
                                                                    lstTokens[2],  # Father's first
                                                                    lstTokens[3])  # Father's last
            print(sSuccess) if bSuccess else print(sFailure)
        else:
            print("setpartners: invalid parameters (try help setpartners)")
        
        return

    # end do_setpartners()

    # ------------------------------------------------------------
    # Shows the children for two parents (father and mother) 
    # ------------------------------------------------------------
    def do_showchildren(self, line):
        """showchildren <mothers-first> <mothers-last> <fathers-first> <fathers-last> 
        Shows the children of the mother with first name <mothers-first> and last
        name <mothers-last> with the father with first-name <fathers-first> and last-
        name <fathers-last> 
        e.g., showchildren Mamma Bear Papa Bear"""

        dbgPrint(INF_DBG, "CLI.do_showchildren - entry")

        lstTokens = line.split()
        if len(lstTokens) == 4:
            bSuccess, sSuccess, sFailure = self.family.showChildren(lstTokens[0],  # Mother's first
                                                                    lstTokens[1],  # Mother's last
                                                                    lstTokens[2],  # Father's first
                                                                    lstTokens[3])  # Father's last
            print(sSuccess) if bSuccess else print(sFailure)
        else:
            print("showchildren: invalid parameters (try help showchildren)")
        
        return

    # end do_showchildren()

    # ------------------------------------------------------------
    # Shows all information about a person
    # ------------------------------------------------------------
    def do_showperson(self, line):
        """showperson <first-name> <last-name>
        Shows all information about a person with first-name
        <first-name> and last-name <last-name>
        e.g., showperson Baby Bear"""

        dbgPrint(INF_DBG, "CLI.do_showperson - entry")

        lstTokens = line.split()
        if len(lstTokens) == 2:
            sResult = self.family.showPerson(lstTokens[0],  # First
                                            lstTokens[1])   # Last
            print(sResult, end='')
        else:
            print ("showperson: invalid parameters (try help showperson)")
        
        return

    # end do_showperson()

    # ------------------------------------------------------------
    # Shows the family tree
    # ------------------------------------------------------------
    def do_showtree(self, line):
        """showtree
        Shows the family tree
        e.g., showtree"""

        dbgPrint(INF_DBG, "CLI.do_showtree - entry")

        lstTokens = line.split()
        if len(lstTokens) == 0:
            sResult = self.family.showTree()
            print(sResult)
        else:
            print ("showtree: invalid parameters (try help showtree)")
        
        return

    # end do_showtree()

# end class CLI ###############################################
