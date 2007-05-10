from pyrep.base import *
from pyrep.pdfrenderer import PDFRenderer
from pyrep import dataproviders

import unittest

class TestPDFProcessor(unittest.TestCase):
    def testSimple(self):
        c = Report()
        
        c.title.size = (-1, cm(3))
        c.header.size = (-1, cm(2))
        c.body.size = (-1, cm(0.5))
        c.footer.size = (-1, cm(2))
        c.summary.size = (-1, cm(5))
        
        c.title.default_font = Font(None, "Helvetica", 22, style=[Font.ITALIC, Font.BOLD])

        c.title.add_child( cm(0,0), Text( (-1, 20), value = "'Test Simple'", alignment = Text.ALIGN_CENTER))
        c.title.add_child( cm(1,2.4), Text( (cm(10), 5), value = """ "This is the title band's end" """, font = Font(None, "Helvetica", 10, style=[Font.ITALIC, Font.BOLD])))
        c.title.add_child( cm(0,2.9), HLine(cm(10)))
        
        c.header.add_child( cm(0,0), Text( (10, 0.5), value = """ "Here begins the page header band" """))
        c.header.add_child( cm(0, 1.4), Text( (30, 0.5), value = "\"Column1\"", alignment = Text.ALIGN_RIGHT))
        c.header.add_child( cm(4, 1.4), Text( (30, 0.5), value = "\"Column2\""))
        c.header.add_child( cm(0, 1.9), HLine() )
        
        c.body.add_child(cm(0,0), Text( (30,0.5), value = "funcs.str(row)", alignment = Text.ALIGN_RIGHT))
        c.body.add_child(cm(4,0), Text( (30,0.5), value = """ "Value %s"%(row+1) """))

        c.footer.add_child( cm(0, 0), HLine() )
        c.footer.add_child(cm(2,1), Text( (10,0.5), value = """ "Date: %s"%system.date """ ))
        c.footer.add_child(cm(17,1), Text( (10,0.5), value = """ "Page: %s"%system.page """ ))
        
        c.summary.add_child( cm(0, 1), HLine())
        c.summary.add_child( cm(10,1.5), Text( (5, 0.5), value = """ "Summary band" """))
        c.summary.add_child( cm(0, 2.5), HLine())
        
        datasource = range(86)
        
        r = PDFRenderer(c)
        r.render(datasources = [dataproviders.DataProvider(datasource)], outfile = "test1.pdf")

    def testCalcs(self):
        c = Report()
        
        c.add_variable( Variable('test', "string", 'Testing') )
        c.add_variable( Variable('csum', "integer", 0) )
        c.add_variable( Variable('psum', "integer", 0) )

        c.add_calculation( Calculation("sum", c.variables['csum'], "row") )
        c.add_calculation( Calculation("sum", c.variables['psum'], "row", "page") )
        
        c.title.size = (-1, cm(3))
        c.header.size = (-1, cm(2))
        c.body.size = (-1, cm(0.5))
        c.footer.size = (-1, cm(2))
        c.summary.size = (-1, cm(5))
        
        c.title.default_font = Font(None, "Helvetica", 22, style=[Font.ITALIC, Font.BOLD])

        c.title.add_child( cm(0,0), Text( (-1, 20), value = "'Test Simple'", alignment = Text.ALIGN_CENTER))
        
        c.header.add_child( cm(0, 1.4), Text( (30, 0.5), value = "\"Column1\"", alignment = Text.ALIGN_RIGHT))
        c.header.add_child( cm(4, 1.4), Text( (30, 0.5), value = "\"Column2\""))

        c.header.add_child( cm(0, 1.9), HLine() )
        
        c.body.add_child(cm(0,0), Text( (30,0.5), value = "funcs.str(row)", alignment = Text.ALIGN_RIGHT))
        c.body.add_child( cm(3.5, 0) , VLine(cm(0.5)))
        c.body.add_child(cm(4,0), Text( (30,0.5), value = "'Value %s'%(row+1)"))
        
        c.footer.add_child(cm(17,1), Text( (10,0.5), value = "system.page" ))
        c.footer.add_child(cm(1,1), Text( (5,0.5), value = "vars.test" ))
        c.footer.add_child(cm(5,1.5), Text( (5,0.5), value = "'Sum of args: %s'%vars.psum"))
        
        c.summary.add_child( cm(0, 1), HLine())
        c.summary.add_child( cm(10,1.5), Text( (5, 0.5), value = """ "Summary: %s"%vars.csum """))
        c.summary.add_child( cm(0, 2.5), HLine())
        
        datasource = range(86)
        
        r = PDFRenderer(c)
        r.render(datasources = [dataproviders.DataProvider(datasource)], outfile = "test2.pdf")
            
suite = unittest.makeSuite(TestPDFProcessor)

__all__=["suite"]

