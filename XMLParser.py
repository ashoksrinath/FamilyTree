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

        sFirst = None
        if "first" in dctAttribs:
            sFirst = dctAttribs["first"]

        sLast = None
        if "last" in dctAttribs:
            sLast = dctAttribs["last"]

        sFathersKey = family.makePersonKey(sFirst, sLast)
        if sFathersKey == None:
            return sFathersKey

        if not sFathersKey in family.dctPeople:
            sGender = "M"
            family.addPerson(sFirst, sLast, sGender, None)
            dbgPrint(INF_DBG, ("XMLParser.proc_father: added '%s %s'" % (sFirst, sLast)))

        person.setFathersKey(sFathersKey)

        return sFathersKey

    # end def proc_father()

    # ------------------------------------------------------------
    # Processes mother's information for a person
    # ------------------------------------------------------------
    def proc_mother(self, family, person, dctAttribs):

        sFirst = None
        if "first" in dctAttribs:
            sFirst = dctAttribs["first"]

        sLast = None
        if "last" in dctAttribs:
            sLast = dctAttribs["last"]

        sMothersKey = family.makePersonKey(sFirst, sLast)
        if sMothersKey == None:
            return sMothersKey

        if not sMothersKey in family.dctPeople:
            sGender = "F"
            family.addPerson(sFirst, sLast, sGender, None)
            dbgPrint(INF_DBG, ("XMLParser.proc_mother: added '%s %s'" % (sFirst, sLast)))

        person.setMothersKey(sMothersKey)

        return sMothersKey

    # end def proc_mother()

    # ------------------------------------------------------------
    # Processes information for a person
    # ------------------------------------------------------------
    def proc_person(self, family, dctAttribs):

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

        sPersonKey = family.addPerson(sFirst, sLast, sGender, sBirthYMD)
        dbgPrint(INF_DBG, ("XMLParser.proc_person: added '%s %s'" % (sFirst, sLast)))

        return sPersonKey

    # end def proc_person()

    # ------------------------------------------------------------
    # Loads people from XML data file
    # ------------------------------------------------------------
    def loadFile(self, sFileName, family):

        try:
            parser = etree.XMLParser(remove_blank_text=True)
            pplTree = etree.parse(sFileName, parser)

            pplRoot = pplTree.getroot()
            personXmlList = list(pplRoot)
            for personXml in personXmlList:
                self.processPersonXml(family, personXml)

        except etree.ParseError as excParsing:
            print("XMLParser.loadFile - error parsing file '%s'" % sFileName)
            print(excParsing)
        except Exception as excUnhandled:
            print("XMLParser.loadFile - unhandled exception", excUnhandled)

        return

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

        person.setBirthPlace(sCity, sState, sCountry, sPostCode)
        dbgPrint(INF_DBG, ("XMLParser.proc_birthplc: set '%s %s %s %s'" % (sCity, sState, sCountry, sPostCode)))

        return

    # end def proc_birthplc()

    # ------------------------------------------------------------
    # Processes person from XML
    # ------------------------------------------------------------
    def processPersonXml(self, family, personXML):

        person      = None
        sMothersKey = None
        sFathersKey = None

        try:
            # --------------------
            # Add Person to Family
            # --------------------
            if personXML.tag == "person":
                sPersonKey = self.proc_person(family, personXML.attrib)
                if sPersonKey == None:
                    dbgPrint(ERR_DBG, "XMLParser.processPersonXml - error, sPersonKey is None")
                    return False

            # ---------------------------------------
            # Process birthplace & parents for Person
            # ---------------------------------------
            person = family.dctPeople[sPersonKey]
            infoList = list(personXML)
            for infoItem in infoList:
                if infoItem.tag == "birthplc":
                    self.proc_birthplc(family, person, infoItem.attrib)

                elif infoItem.tag == "father":
                    sFathersKey = self.proc_father(family, person, infoItem.attrib)

                elif infoItem.tag == "mother":
                    sMothersKey = self.proc_mother(family, person, infoItem.attrib)

                else:
                    dbgPrint(ERR_DBG, ("XMLParser.processPersonXml - error, skipping unrecognized tag: %s" % infoItem.tag))

            # end for infoItem in infoList

            # ----------------------------------------------------------------------------
            # Set partner relationships between parents, add Person to parentages register
            # ----------------------------------------------------------------------------
            if (sMothersKey != None) and (sFathersKey != None):
                family.addToParentages(sPersonKey, sMothersKey, sFathersKey)

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
