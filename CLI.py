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
    def __init__(self, familyTree):

        super(CLI, self).__init__()

        dbgPrint(INF_DBG, "CLI.__init__ - entry")

        self.dctParamCnt = dict()
        self.seedParamsDict()

        self.familyTree = familyTree

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
        if len(lstTokens) == self.dctParamCnt["addperson"]:
            dctPersonInfo = dict()
            dctPersonInfo["first"]      = lstTokens[0]
            dctPersonInfo["last"]       = lstTokens[1]
            dctPersonInfo["gender"]     = lstTokens[2]
            dctPersonInfo["birthymd"]   = lstTokens[3]
            self.familyTree.family.addPerson(dctPersonInfo)
        else:
            print ("addperson: invalid parameters (try help addperson)")
        
        return

    # end do_addperson()

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
        if len(lstTokens) == self.dctParamCnt["delperson"]:
            self.familyTree.family.delPerson(   lstTokens[0],  # First 
                                                lstTokens[1])  # Last
        else:
            print ("delperson: invalid parameters (try 'help delperson')")
              
        return

    # end do_delperson()

    # ------------------------------------------------------------
    # Exits the CLI
    # ------------------------------------------------------------
    def do_exit(self, line):
        """exit
        Exits this application"""

        dbgPrint(INF_DBG, "CLI.do_exit - entry")

        lstTokens = line.split()
        if len(lstTokens) != self.dctParamCnt["exit"]:
            print ("exit: invalid parameters (try help exit)")

        return True

    # end do_exit()

    # ------------------------------------------------------------
    # Lists all parentages in the family
    # ------------------------------------------------------------
    def do_listparentages(self, line):
        """listparentages
        Lists all parentages between people in the family
        e.g., listparentages"""

        dbgPrint(INF_DBG, "CLI.do_listparentages - entry")

        lstTokens = line.split()
        if len(lstTokens) == self.dctParamCnt["listparentages"]:
            self.familyTree.family.listParentages()
        else:
            print ("listparentages: invalid parameters (try help listparentages)")
        
        return

    # end do_listparentages()

    # ------------------------------------------------------------
    # Lists all the people in the family
    # ------------------------------------------------------------
    def do_listpeople(self, line):
        """listpeople
        Lists all the people in the family
        e.g., listpeople"""

        dbgPrint(INF_DBG, "CLI.do_listpeople - entry")

        lstTokens = line.split()
        if len(lstTokens) == self.dctParamCnt["listpeople"]:
            self.familyTree.family.listPeople()
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
        if len(lstTokens) == self.dctParamCnt["loadfile"]:
            self.familyTree.family.loadPeople(lstTokens[0])   # XML file

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
        if len(lstTokens) == self.dctParamCnt["removechildren"]:
            self.familyTree.family.removeChildren(  lstTokens[0],  # Mother's first
                                                    lstTokens[1],  # Mother's last
                                                    lstTokens[2],  # Father's first
                                                    lstTokens[3])  # Father's last
        else:
            print ("removechildren: invalid parameters (try help removechildren)")

    # end do_removechildren()

    # ------------------------------------------------------------
    # Saves data to the people XML file
    # ------------------------------------------------------------
    def do_savefile(self, line):
        """savefile <xml-file>
        Saves XML data for people to <xml-file> if provided.  
        Otherwise it saves the data to the filename specified 
        when the script was started
        e.g., savefile myfamilytree.xml"""

        dbgPrint(INF_DBG, "CLI.do_savefile - entry")

        lstTokens = line.split()
        if len(lstTokens) == self.dctParamCnt["savefile"]:
            self.familyTree.family.saveFile(lstTokens[0])   # Specific XML file
        else:
            self.familyTree.family.saveFile(None)           # Parametric XML file

        return

    # end do_savefile()

    # ------------------------------------------------------------
    # Sets the birthplace for a person
    # ------------------------------------------------------------
    def do_setbirthplc(self, line):
        """setbirthplc <first-name> <last-name> <city> <state> <country> <postcode>
        Sets birthplace information for a person with first-name <first-name>
        and last-name <last-name>
        e.g., setbirthplc Fir Lastman Columbus OH USA 43210"""

        dbgPrint(INF_DBG, "CLI.do_setbirthplc - entry")

        lstTokens = line.split()
        if len(lstTokens) == self.dctParamCnt["setbirthplc"]:
            self.familyTree.family.setBirthPlace( lstTokens[0],    # First-name
                                                  lstTokens[1],    # Last-name
                                                  lstTokens[2],    # City
                                                  lstTokens[3],    # State
                                                  lstTokens[4],    # Country
                                                  lstTokens[5])    # Postal code
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
        if len(lstTokens) == self.dctParamCnt["setbirthymd"]:
            self.familyTree.family.setBirthYMD (lstTokens[0],   # First
                                                lstTokens[1],   # Last
                                                lstTokens[2])   # Birthday as YYYYMMDD
        else:
            print ("setbirthymd: invalid parameters (try help setbirthymd)")
        
        return

    # end do_setbirthymd()

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
        if len(lstTokens) == self.dctParamCnt["setgender"]:
            self.familyTree.family.setGender(  lstTokens[0],    # First
                                                lstTokens[1],   # Last
                                                lstTokens[2])   # Gender
        else:
            print ("setgender: invalid parameters (try help setgender)")
        
        return

    # end do_setgender()

    # ------------------------------------------------------------
    # Sets the parents (father and mother) for a person
    # ------------------------------------------------------------
    def do_setparents(self, line):
        """setparents <first-name> <last-name> <mothers-first> <mothers-last> <fathers-first> <fathers-last>
        Sets the parents of the person with first-name <first-name> and last-name <last-name>. 
        The mother's first-name is set to <mothers-first> and last name to <mothers-last>.
        The father's first-name is set to <fathers-first> and last-name to <father-last>
        e.g., setparents Baby Bear Mamma Bear Papa Bear"""

        dbgPrint(INF_DBG, "CLI.do_setparents - entry")

        lstTokens = line.split()
        if len(lstTokens) == self.dctParamCnt["setparents"]:
            self.familyTree.family.setParents(  lstTokens[0],  # First
                                                lstTokens[1],  # Last
                                                lstTokens[2],  # Mother's first
                                                lstTokens[3],  # Mother's last
                                                lstTokens[4],  # Father's first
                                                lstTokens[5])  # Father's last
        else:
            print ("setparents: invalid parameters (try help setparents)")
        
        return

    # end do_setparents()

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
        if len(lstTokens) == self.dctParamCnt["showchildren"]:
            self.familyTree.family.showChildren(lstTokens[0],  # Mother's first
                                                lstTokens[1],  # Mother's last
                                                lstTokens[2],  # Father's first
                                                lstTokens[3])  # Father's last
        else:
            print ("showchildren: invalid parameters (try help showchildren)")
        
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
        if len(lstTokens) == self.dctParamCnt["showperson"]:
            self.familyTree.family.showPerson(  lstTokens[0],   # First
                                                lstTokens[1])   # Last
        else:
            print ("showperson: invalid parameters (try help showperson)")
        
        return

    # end do_showperson()

    # ------------------------------------------------------------
    # Shows all information about a person
    # ------------------------------------------------------------
    def do_showtree(self, line):
        """showtree
        Shows the family tree
        e.g., showtree"""

        dbgPrint(INF_DBG, "CLI.do_showtree - entry")

        lstTokens = line.split()
        if len(lstTokens) == self.dctParamCnt["showtree"]:
            self.familyTree.showTree()
        else:
            print ("showtree: invalid parameters (try help showtree)")
        
        return

    # end do_showtree()

    # ------------------------------------------------------------
    # Seeds dictionary with CLI verbs and required parameter count
    # ------------------------------------------------------------
    def seedParamsDict(self):

        dbgPrint(INF_DBG, "CLI.seedParamsDict - entry")

        self.dctParamCnt["addperson"]       = 4     # addperson     first last gender birth-date
        self.dctParamCnt["delperson"]       = 2     # delperson     first last

        self.dctParamCnt["setbirthplc"]     = 6     # setbirthplc   first last city state country postcode
        self.dctParamCnt["setbirthymd"]     = 3     # setbirthymd   first last birth-date

        self.dctParamCnt["listpeople"]      = 0     # listpeople
        self.dctParamCnt["listparentages"]  = 0     # listparentages

        self.dctParamCnt["setparents"]      = 6     # setparents    first last motherfirst motherlast fatherfirst fatherlast
        self.dctParamCnt["removechildren"]  = 4     # removechildren motherfirst motherlast fatherfirst fatherlast 

        self.dctParamCnt["showperson"]      = 2     # showperson    first last
        self.dctParamCnt["showchildren"]    = 4     # showchildren  motherfirst motherlast fatherfirst fatherlast 
        self.dctParamCnt["showtree"]        = 0     # showtree

        self.dctParamCnt["loadfile"]        = 1     # loadfile      xml-file-name
        self.dctParamCnt["savefile"]        = 1     # savefile      xml-file-name

        self.dctParamCnt["exit"]            = 0     # exit

        return

    # end def seedParamsDict()

# end class CLI ###############################################




