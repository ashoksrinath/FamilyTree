from   lxml import etree
from Family import Family
from  Utils import *

class XMLParser(object):
    """description of class"""

    # ------------------------------------------------------------
    # Initializes object
    # ------------------------------------------------------------
    def __init__(self):
 
        return

    # end def __init__()

    # ------------------------------------------------------------
    # Processes father's information for a person
    # ------------------------------------------------------------
    def proc_father(self, family, person, dctAttribs):

        bSuccess = False

        sFirst = None
        if "first" in dctAttribs:
            sFirst = dctAttribs["first"]

        sLast = None
        if "last" in dctAttribs:
            sLast = dctAttribs["last"]

        sFathersKey = family.makePersonKey(sFirst, sLast)
        if sFathersKey == None:
            return False, sFathersKey

        if not sFathersKey in family.dctPeople:
            bSuccess, sPersonKey, sError = family.addPerson(sFirst, sLast, "M", None)
            if bSuccess:
                dbgPrint(INF_DBG, ("XMLParser.proc_father: added '%s %s'" % (sFirst, sLast)))
                person.setFathersKey(sFathersKey)
            else:
                dbgPrint(ERR_DBG, ("XMLParser.proc_father: error '%s'" % (sResponse)))


        return bSuccess, sFathersKey

    # end def proc_father()

    # ------------------------------------------------------------
    # Processes mother's information for a person
    # ------------------------------------------------------------
    def proc_mother(self, family, person, dctAttribs):

        bSuccess = False

        sFirst = None
        if "first" in dctAttribs:
            sFirst = dctAttribs["first"]

        sLast = None
        if "last" in dctAttribs:
            sLast = dctAttribs["last"]

        sMothersKey = family.makePersonKey(sFirst, sLast)
        if sMothersKey == None:
            return bSuccess, sMothersKey

        if not sMothersKey in family.dctPeople:
            bSuccess, sPersonKey, sError = family.addPerson(sFirst, sLast, "F", None)
            if bSuccess:
                dbgPrint(INF_DBG, ("XMLParser.proc_mother: added '%s %s'" % (sFirst, sLast)))
            else:
                dbgPrint(ERR_DBG, ("XMLParser.proc_mother: error '%s'" % (sResponse)))

        person.setMothersKey(sMothersKey)

        return True, sMothersKey

    # end def proc_mother()

    # ------------------------------------------------------------
    # Processes attributes for a person.  Returns a tuple of (bool, 
    # success-string, error-string), with the success string set to
    # the person-key
    # ------------------------------------------------------------
    def proc_person(self, family, dctAttribs):

        sError      = ""
        bSuccess    = True

        sFirst = None
        if "first" in dctAttribs:
            sFirst = dctAttribs["first"]

        sLast = None
        if "last" in dctAttribs:
            sLast = dctAttribs["last"]

        sGender = None
        if "gender" in dctAttribs:
            sGender = dctAttribs["gender"]

        sBirthYMD = None
        if "birthymd" in dctAttribs:
            sBirthYMD = dctAttribs["birthymd"]

        if (sFirst != None) and (sLast != None) and (sGender != None):
            bSuccess, sPersonKey, sError = family.addPerson(sFirst, sLast, sGender, sBirthYMD)
            if bSuccess:
                dbgPrint(INF_DBG, ("XMLParser.proc_person: added '%s %s'" % (sFirst, sLast)))
        else:
            sError = ("loadfile: person's first-name, last-name and gender are required\n")

        return(bSuccess, sPersonKey, sError)

    # end def proc_person()

    # ------------------------------------------------------------
    # Loads people from XML data file
    # ------------------------------------------------------------
    def loadFile(self, sFileName, family):

        sReturnBuff = ""
        bSuccess    = True

        try:
            parser = etree.XMLParser(remove_blank_text=True)
            pplTree = etree.parse(sFileName, parser)

            pplRoot = pplTree.getroot()
            personXmlList = list(pplRoot)
            for personXml in personXmlList:
                self.processPersonXml(family, personXml)

        except etree.ParseError as excParsing:
            bSuccess = False
            sLine = ("XMLParser.loadFile - error parsing file '%s'" % sFileName)
            sReturnBuff += sLine
            sReturnBuff += repr(excParsing)
        except Exception as excUnhandled:
            bSuccess = False
            sLine = ("XMLParser.loadFile - unhandled exception ")
            sLine += repr(excUnhandled)
            sReturnBuff += sLine

        if bSuccess:
            return(bSuccess, "OK\n", None)
        else:
            return(bSuccess, None, sReturnBuff)

    # end def loadFile()

    # ------------------------------------------------------------
    # Processes birth-place information for a person
    # ------------------------------------------------------------
    def proc_birthplc(self, family, person, dctBirthPlc):

        sCity = None
        if "city" in dctBirthPlc:
            sCity = dctBirthPlc["city"]

        sState = None
        if "state" in dctBirthPlc:
            sState = dctBirthPlc["state"]

        sPostCode = None
        if "postcode" in dctBirthPlc:
            sPostCode = dctBirthPlc["postcode"]

        sCountry = None
        if "country" in dctBirthPlc:
            sCountry = dctBirthPlc["country"]

        bStatus = person.setBirthPlace(sCity, sState, sCountry, sPostCode)
        dbgPrint(INF_DBG, ("XMLParser.proc_birthplc: set '%s %s %s %s'" % (sCity, sState, sCountry, sPostCode)))

        return(bStatus)

    # end def proc_birthplc()

    # ------------------------------------------------------------
    # Processes person from XML
    # ------------------------------------------------------------
    def processPersonXml(self, family, personXML):

        person      = None
        sPersonKey  = ""
        sError      = ""
        sMothersKey = None
        sFathersKey = None
        bSuccess    = False

        try:
            # --------------------
            # Add Person to Family
            # --------------------
            if personXML.tag == "person":
                bSuccess, sPersonKey, sError = self.proc_person(family, personXML.attrib)
                if not bSuccess:
                    dbgPrint(ERR_DBG, sResponse)
                    return False

            # ---------------------------------------
            # Process birthplace & parents for Person
            # ---------------------------------------
            person = family.dctPeople[sPersonKey]
            infoList = list(personXML)
            for infoItem in infoList:
                if infoItem.tag == "birthplc":
                    bSuccess = self.proc_birthplc(family, person, infoItem.attrib)

                elif infoItem.tag == "father":
                    bSuccess, sFathersKey = self.proc_father(family, person, infoItem.attrib)

                elif infoItem.tag == "mother":
                    bSuccess, sMothersKey = self.proc_mother(family, person, infoItem.attrib)

                else:
                    dbgPrint(ERR_DBG, ("XMLParser.processPersonXml - error, skipping unrecognized tag: %s" % infoItem.tag))

            # end for infoItem in infoList

            # ----------------------------------------------------------------------------
            # Set partner relationships between parents, add Person to parentages register
            # ----------------------------------------------------------------------------
            if (sMothersKey != None) and (sFathersKey != None):
                bSuccess = family.addToParentages(sPersonKey, sMothersKey, sFathersKey)

        except Exception as extinction:
            dbgPrint(ERR_DBG, ("XMLParser.processPersonXml - error processing: ", personXML.attrib))
            dbgPrint(ERR_DBG, ("XMLParser.processPersonXml - unhandled exception: ", extinction))
            return False

        return True

    # end def processPersonXml()

    # ------------------------------------------------------------
    # Saves family data to file in XML format
    # ------------------------------------------------------------
    def saveFile(self, sXMLfileName, family):

        # --------------------------------
        # Create root element <parentages>
        # --------------------------------
        e_people = etree.Element("people")

        # -----------------
        # For all people...
        # -----------------
        for sPersonKey, person in family.dctPeople.items():

            # ----------------------------------------------------------------------
            # Create element <person>, set attributes, append it to element <people>
            # ----------------------------------------------------------------------
            e_person = etree.Element("person")
            if person.sFirst != None:
                e_person.attrib["first"] = person.sFirst
            if person.sLast != None:
                e_person.attrib["last"] = person.sLast
            if person.sGender != None:
                e_person.attrib["gender"] = person.sGender
            if person.sBirthYMD != None:
                e_person.attrib["birthymd"] = person.sBirthYMD
            e_people.append(e_person)

            # -------------------------------------------------------------------------
            # Create subelement <father>, set attributes, append it to element <person>
            # -------------------------------------------------------------------------
            sFathersKey = person.getFathersKey()
            if sFathersKey != None:
                sFirst, sLast = family.getPersonNames(sFathersKey)
                if (sFirst != None) or (sLast != None):
                    e_father = etree.Element("father")
                    if sFirst != None:
                        e_father.attrib["first"] = sFirst
                    if sLast != None:
                        e_father.attrib["last"] = sLast
                    e_person.append(e_father)

            # -------------------------------------------------------------------------
            # Create subelement <mother>, set attributes, append it to element <person>
            # -------------------------------------------------------------------------
            sMothersKey = person.getMothersKey()
            if sMothersKey != None:
                sFirst, sLast = family.getPersonNames(sMothersKey)
                if (sFirst != None) or (sLast != None):
                    e_mother = etree.Element("mother")
                    if sFirst != None:
                        e_mother.attrib["first"] = sFirst
                    if sLast != None:
                        e_mother.attrib["last"]  = sLast
                    e_person.append(e_mother)

            # -------------------------------------------------------------------------
            # Create subelement <birthplc>, set attributes, append it to element <person>
            # -------------------------------------------------------------------------
            sBirthCity, sBirthState, sBirthCountry, sBirthPostCode = person.getBirthPlace()
            if (sBirthCity != None) or (sBirthState != None) or (sBirthCountry != None) or (sBirthPostCode != None):
                e_birthplc = etree.Element("birthplc")
                if sBirthCity != None:
                    e_birthplc.attrib["city"] = sBirthCity
                if sBirthState != None:
                    e_birthplc.attrib["state"] = sBirthState
                if sBirthCountry != None:
                    e_birthplc.attrib["country"] = sBirthCountry
                if sBirthPostCode != None:
                    e_birthplc.attrib["postcode"] = sBirthPostCode
                e_person.append(e_birthplc)

        # end for sPersonKey in family.dctPeople

        # ---------------------------------
        # Create XML tree, write it to file
        # ---------------------------------
        et_people = etree.ElementTree(e_people)
        with open(sXMLfileName, "wb") as fhOutputfile:
            et_people.write(fhOutputfile, encoding='utf-8', pretty_print=True, xml_declaration=True)

        return

    # end saveFile()

# end class XMLParser
