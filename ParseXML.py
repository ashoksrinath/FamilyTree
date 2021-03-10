import xml.etree.ElementTree as ET
from   Utils import *


# #############################################################
# CLI: class to parentage relationships file
# -------------------------------------------------------------
class ParseParentages:

    def __init__(self):

        self.ptgRoot = None
        self.sXML ='''
        <parentages>
            <parentage fathersfirst="ffirst1" fatherslast="flast1" mothersfirst="mfirst1" motherslast="mlast1"> 
                <child> 
                    <first>"cfirst1"</first> 
                    <last>"clast1"</last> 
                </child> 
            </parentage> 
        </parentages>
        '''

        return

    def parse(self):
        print("ParseParentages::parse - list of parentages from string:")
        try:
            self.ptgRoot = ET.fromstring(self.sXML)
            for parentage in self.ptgRoot.iter("parentage"):
                for key, value in parentage.attrib.items():
                    print(key + ": " + value)
                for child in parentage[0]:
                    print (child.tag, child.text)

        except ET.ParseError as excParsing:
            print("   ParseParentages: Error parsing string")
        except Exception as excUnhandled:
            print("   ParseParentages: Unhandled exception:", excUnhandled)

        print("ParseParentages::parse - list of parentages from parentages.xml")
        try:
            self.ptgRoot = ET.parse("parentages.xml")
            for parentage in self.ptgRoot.iter("parentage"):
                for key, value in parentage.attrib.items():
                    print(key + ": " + value)
                for child in parentage[0]:
                    print (child.tag, child.text)

        except ET.ParseError as excParsing:
            print("   ParseParentages: Error parsing string")
        except Exception as excUnhandled:
            print("   ParseParentages: Unhandled exception:", excUnhandled)

        return

# end class ParseParentages

class ParsePeople:

    def __init__(self):
        self.sXML ='''
        <people>
            <person first="cfirst1" last="clast1" gender="F" birthymd="19700101">
                <birthcity>"Bengaluru"</birthcity>
                <birthstate>"Karnataka"</birthstate>
                <birthcountry>"India"</birthcountry>
                <birthpostcode>"560001"</birthpostcode>
            </person>
            <person first="cfirst2" last="clast2" gender="F" birthymd="19700202">
                <birthcity>"Bengaluru"</birthcity>
                <birthstate>"Karnataka"</birthstate>
                <birthcountry>"India"</birthcountry>
                <birthpostcode>"560002"</birthpostcode>
            </person>
            <person first="cfirst3" last="clast3" gender="F" birthymd="19700303">
                <birthcity>"Bengaluru"</birthcity>
                <birthstate>"Karnataka"</birthstate>
                <birthcountry>"India"</birthcountry>
                <birthpostcode>"560003"</birthpostcode>
            </person>
            <person first="ffirst1" last="flast1" gender="M" birthymd="19400101">
                <birthcity>"Bengaluru"</birthcity>
                <birthstate>"Karnataka"</birthstate>
                <birthcountry>"India"</birthcountry>
                <birthpostcode>"560001"</birthpostcode>
            </person>
            <person first="ffirst2" last="flast2" gender="M" birthymd="19400202">
                <birthcity>"Bengaluru"</birthcity>
                <birthstate>"Karnataka"</birthstate>
                <birthcountry>"India"</birthcountry>
                <birthpostcode>"560002"</birthpostcode>
            </person>
            <person first="ffirst3" last="flast3" gender="M" birthymd="19400303">
                <birthcity>"Bengaluru"</birthcity>
                <birthstate>"Karnataka"</birthstate>
                <birthcountry>"India"</birthcountry>
                <birthpostcode>"560003"</birthpostcode>
            </person>
            <person first="mfirst1" last="mlast1" gender="F" birthymd="19500101">
                <birthcity>"Bengaluru"</birthcity>
                <birthstate>"Karnataka"</birthstate>
                <birthcountry>"India"</birthcountry>
                <birthpostcode>"560001"</birthpostcode>
            </person>
            <person first="mfirst2" last="mlast2" gender="F" birthymd="19500202">
                <birthcity>"Bengaluru"</birthcity>
                <birthstate>"Karnataka"</birthstate>
                <birthcountry>"India"</birthcountry>
                <birthpostcode>"560002"</birthpostcode>
            </person>
            <person first="mfirst3" last="mlast3" gender="F" birthymd="19500303">
                <birthcity>"Bengaluru"</birthcity>
                <birthstate>"Karnataka"</birthstate>
                <birthcountry>"India"</birthcountry>
                <birthpostcode>"560003"</birthpostcode>
            </person>
        </people>
            '''

        return

    # end def __init__()

    def parse(self):

       print("ParsePeople::parse - list of people from string")
       try:
           self.ptgRoot = ET.fromstring(self.sXML)
           for person in self.ptgRoot.iter("person"):
               for key, value in person.attrib.items():
                   print(key + ": " + value)
               for child in person[0]:
                   print (child.tag, child.text)

       except ET.ParseError as excParsing:
           print("   ParsePeople: Error parsing string")
       except Exception as excUnhandled:
           print("   ParsePeople: Unhandled exception")

       print("ParsePeople::parse - list of people from people.xml")
       try:
           self.ptgRoot = ET.parse("people.xml")
           for person in self.ptgRoot.iter("person"):
               print("***")
               for key, value in person.attrib.items():
                   print(key + ": " + value)
               for child in person.iter():
                   print (child.tag, child.text)

       except ET.ParseError as excParsing:
            print("   ParsePeople: Error parsing string")
       except Exception as excUnhandled:
            print("   ParsePeople: Unhandled exception")

       return

    # end def parse()

# end class ParsePeople

if __name__ == "__main__":

    prsPnt = ParseParentages()
    prsPnt.parse()

    prsPpl = ParsePeople()
    prsPpl.parse()


