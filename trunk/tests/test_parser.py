from pyrep.parser import XMLParser
from pyrep.pdfrenderer import PDFRenderer
from pyrep import dataproviders

import unittest

simple_xml="""<?xml version="1.0" standalone="no"?>

<!DOCTYPE report SYSTEM "report.dtd">

<report pagesize="A4">
    <font id="font1" face="Helvetica" size="22" italic="true" bold="true" />
    <font id="font2" face="Helvetica" size="10" italic="true" bold="true" />
    
    <title height="3cm" font="font1">
        <text x="0" y="0" height="20" alignment="center">
            "Test Simple"
        </text>
        
        <text x="1cm" y="2.4cm" width="10cm" height="5" font="font2">
            "This is the title band's end"
        </text>
        
        <hline x="0" y="2.9cm" width="10cm" />
    </title> 

    <header height="2cm">
        <text width="10cm" height="0.5cm">
            "Here begins the page header band"
        </text>
        
        <text y="1.4cm" width="30" height="0.5" alignment="right">
            "Column1"
        </text>
        
        <text x="4cm" y="1.4cm" width="30" height="0.5">
            "Column2"
        </text>
        
        <hline y="1.9cm" />
        
    </header>

    <body height="0.5cm">
        <text width="30" height="0.5" alignment="right">
            funcs.str(row)
        </text>
        
        <text x="4cm" width="30" height="0.5">
            "Value %s"%(row+1)
        </text>
    </body>

    <footer height="2cm">
        <hline />
        
        <text x="2cm" y="1cm" width="10" height="0.5">
            "Date: %s"%system.date
        </text>
        
        <text x="17cm" y="1cm" width="10" height="0.5">
            "Page: %s"%system.page
        </text>
    </footer>

    <summary height="5cm">
        <hline y="1cm" />
        <text x="10cm" y="1.5cm" width="5" height="0.5">
            "Summary band"
        </text>
        
        <hline y="2.5cm" />
        
    </summary>        
</report>
"""

wrong_xml="""<?xml version="1.0" standalone="no"?>

<!DOCTYPE report SYSTEM "report.dtd">

<report pagesize="A4">
    <foant id="font1" face="Helvetica" size="22" italic="true" bold="true" />
    <font id="font2" face="Helvetica" size="10" italic="true" bold="true" />
    
    <title height="3cm" font="font1">
        <text x="0" y="0" height="20" alignment="center">
            "Test Simple"
        </text>
        
        <text x="1cm" y="2.4cm" width="10cm" height="5" font="font2">
            "This is the title band's end"
        </text>
        
        <hline x="0" y="2.9cm" width="10cm" />
    </title> 

    <header height="2cm">
        <text width="10cm" height="0.5cm">
            "Here begins the page header band"
        </text>
        
        <text y="1.4cm" width="30" height="0.5" alignment="right">
            "Column1"
        </text>
        
        <text x="4cm" y="1.4cm" width="30" height="0.5">
            "Column2"
        </text>
        
        <hline y="1.9cm" />
        
    </header>

    <body height="0.5cm">
        <text width="30" height="0.5" alignment="right">
            funcs.str(row)
        </text>
        
        <text x="4cm" width="30" height="0.5">
            "Value %s"%(row+1)
        </text>
    </body>

    <footer height="2cm">
        <hline />
        
        <text x="2cm" y="1cm" width="10" height="0.5">
            "Date: %s"%system.date
        </text>
        
        <text x="17cm" y="1cm" width="10" height="0.5">
            "Page: %s"%system.page
        </text>
    </footer>

    <summary height="5cm">
        <hline y="1cm" />
        <text x="10cm" y="1.5cm" width="5" height="0.5">
            "Summary band"
        </text>
        
        <hline y="2.5cm" />
        
    </summary>        
</report>
"""

import sqlite3

class TestParser(unittest.TestCase):
    def testStringParser(self):
        p = XMLParser(xmlcontent = wrong_xml)
        
        p = XMLParser(xmlcontent = simple_xml)
        
        report = p.parse()

        datasource = range(86)

        r = PDFRenderer(report)
        r.render(datasources = [dataproviders.DataProvider(datasource)], outfile = "out/%s.pdf"%self._testMethodName)

    def testFileParser(self):
        conn = sqlite3.connect(":memory:")
        cur = conn.cursor()
        cur.execute("CREATE TABLE test_table(id int not null primary key, description varchar(50))")
        for x in range(50):
            cur.execute("INSERT INTO test_table(id, description) values(?, ?)", (x, "Desc %s"%(x + 1)))
        conn.commit()
        cur.close()
        
        p = XMLParser(filename = "test1.xml")
        
        report = p.parse()

        r = PDFRenderer(report)
        r.render(module = sqlite3, conn = conn, outfile = "out/%s.pdf"%self._testMethodName)

suite = unittest.makeSuite(TestParser)

__all__=["suite"]
