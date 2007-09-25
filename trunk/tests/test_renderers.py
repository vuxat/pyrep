from pyrep import *
from pyrep.pdfrenderer import PDFRenderer
from pyrep.htmlrenderer import HTMLRenderer
from pyrep import dataproviders

import unittest

class TestRenderers(unittest.TestCase):
    def _run_report(self, report, datasrc = None):
        
        renderers = (
            (PDFRenderer, "pdf"),
            (HTMLRenderer, "html")
        )
        
        for class_, ext in renderers:
            r = class_(report)
        
            kwargs = dict(outfile = "out/%s.%s"%(self._testMethodName, ext))
        
            if datasrc is not None:
                kwargs['datasources'] = datasrc
        
            r.render(**kwargs)
        
    def _test_section(self, section):
        section.size = (None, cm(4))

        section.default_font = Font(None, "Helvetica", 20)

        section.add_child( (1, 1), Box(section.size - 2, bordercolor = Color.RED, fillcolor = Color(255, 255, 245)) )

        for x in range(10):
            section.add_child((section.size.width / 10 * x , 0), VLine(section.size.height, linecolor = Color.random()))

        for y in range(section.height / cm(1)):
            section.add_child((cm(0, y)), HLine(section.size.width, linecolor = Color.random()))

        for x in range(10):
            for y in range(section.height / cm(1)):
                section.add_child((section.size.width / 10 * x , cm(y)), Text( (section.size.width / 10, 10), value = "\"%s, %s\""%(x, y), alignment = Text.ALIGN_CENTER, color = Color.random()))
        
        section.add_child((0, 0), Text(section.size, value = "\"%s\""%section.name, alignment = Text.ALIGN_CENTER, font = Font(None, "Helvetica", 50, style = [Font.BOLD])))
        
        if section == section.parent.body:
            section.add_child( cm(0, 3), Text( (section.size.width, cm(1)), value = "\"Row %s\"%row", alignment = Text.ALIGN_CENTER, font = Font(None, "Helvetica", 30, style = [Font.BOLD, Font.ITALIC])))
            
    def testSections(self):
        r = Report()
        
        self._test_section(r.title)
        self._test_section(r.header)
        self._test_section(r.body)
        self._test_section(r.footer)
        self._test_section(r.summary)

        self._run_report(r, [dataproviders.DataProvider(range(10))])
        
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
        c.footer.add_child(cm(2,1), Text( (10,0.5), value = """ "Date: %s"%system.date.strftime("%m/%d/%Y")""" ))
        c.footer.add_child(cm(17,1), Text( (10,0.5), value = """ "Page: %s"%system.page """ ))
        
        c.summary.add_child( cm(0, 1), HLine())
        c.summary.add_child( cm(10,1.5), Text( (5, 0.5), value = """ "Summary band" """))
        c.summary.add_child( cm(0, 2.5), HLine())
        
        self._run_report(c, [dataproviders.DataProvider(range(86))])

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
        
        self._run_report(c, [dataproviders.DataProvider(range(86))])
    
    def testBox(self):
        c = Report()
        
        c.title.size = (-1, cm(5))
        
        c.title.default_font = Font(None, "Helvetica", 26, style = [Font.ITALIC, Font.BOLD])

        c.register_font(Font("small", "Helvetica", 9))
        
        c.title.add_child( cm(2, 1), Box(c.title.size - (40, 10), round = 10, fillcolor = Color(250, 240, 200), bordercolor = Color(100, 100, 100)))
        c.title.add_child( cm(0, 2), Text(c.title.size - (0, 20), value = "'Box Test'", alignment= Text.ALIGN_CENTER))
        c.title.add_child( cm(0, 4.5), Text( (10, 0.4), value = quote("The box should be on the title band, at coordinates (2cm, 1cm). The text inside should be centered, and its upper-left corner should be at 2 cm"), font = "small"))

        self._run_report(c, [dataproviders.DataProvider(range(1))])
        
suite = unittest.makeSuite(TestRenderers)

__all__=["suite"]

