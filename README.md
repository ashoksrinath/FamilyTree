FamilyTree is a Python application to build a family tree interatively.
Usage: python3 FamilyTree.py <people.xml>
       people.xml is an XML file containing information about people in the family

Sample XML:
<people>
  <person first="Firth" last="Laught" gender="M" birthymd="19630614">
    <mother first="Forced" last="Laught" />
    <father first="Furs" last="Laught" />
    <birthplc city="Citadel" state="Estate" country="Cometree" />
  </person>
  <person first="Firs" last="Laught" gender="F" birthymd="19610122">
    <mother first="Forced" last="Laught" />
    <father first="Furs" last="Laught" />
    <birthplc city="Citadel" state="Estate" country="Cometree" />
  </person>
  <person first="Furs" last="Laught" gender="M" birthymd="19270202">
  </person>
  <person first="Forced" last="Laught" gender="F" birthymd="19341111">
    <mother first="Fierce" last="Lost" />
    <father first="Firms" last="Lost" />
    <birthplc city="Bengaluru" state="Shock" country="Countree" />
  </person>
  <person first="Fairest" last="Loss" gender="F" birthymd="19340506">
    <mother first="Fierce" last="Lost" />
    <father first="Firms" last="Lost" />
    <birthplc city="Bengaluru" state="Shock" country="Countree" />
  </person>
  <person first="Furriest" last="Loss" gender="M" birthymd="19270626">
    <birthplc city="Bengaluru" state="Shock" country="Countree" />
  </person>
  <person first="Forts" last="Loss" gender="F" birthymd="19710821">
    <mother first="Fairest" last="Loss" />
    <father first="Furriest" last="Loss" />
    <birthplc city="Bengaluru" state="Shock" country="Countree" />
  </person>
  <person first="Firms" last="Loft" gender="M" birthymd="19730101">
    <mother first="Fairest" last="Loss" />
    <father first="Furriest" last="Loss" />
    <birthplc city="Bengaluru" state="Shock" country="Countree" />
  </person>
  <person first="Firms" last="Lost" gender="M" birthymd="19000101">
  </person>
  <person first="Fierce" last="Lost" gender="F" birthymd="19111111">
  </person>
</people>