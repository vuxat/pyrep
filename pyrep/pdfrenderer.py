# Copyright(c) 2005-2007 Angelantonio Valente (y3sman@gmail.com)
# See LICENSE file for details.

""" 
PDF renderer 
Renders a report to a PDF file using the ReportLab library (www.reportlab.org)
"""

import os
import tempfile
import sys

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm as rl_mm

from base import *

class PDFRenderer(Renderer):
    """
    Renderer class.
    """
    
    def __init__(self, report):
        """
        Constructor
        @param report: The Report object to render
        """
        
        self.report = report
        
    def render(self, *args, **kwargs):
        """
        Make a PDF file 
        @keyword outfile: Output file name, if not given a temporary file will be created
        @keyword show: If True, the generated PDF file will be shown with the  default system PDF reader
        @keyword show_with: The complete path of the program to use to show the PDF 
        @return: The path of the new PDF file
        """
        super(PDFRenderer, self).render(*args, **kwargs)
        
        # Open out file
        if 'outfile' in kwargs:
            outfile = kwargs['outfile']
        else:
            out = tempfile.mkstemp(".pdf","REP_")
            os.close(out[0])
            outfile = out[1]
            
        c=canvas.Canvas(outfile)

        # Set Page Size
        c.setPageSize((rl_mm*self.report.page.width,rl_mm*self.report.page.height,))
        
        self._canvas=c

        self.report.process(self)
        
        c.save()
        
        if kwargs.get("show", False):
            show_with = kwargs.get("show_with", "")
            if not show_with:
                if sys.platform == "darwin":
                    os.system("open %s"%outfile)
                elif sys.platform == "win32":
                    os.startfile(outfile)
                else:
                    raise ReportError("Please pass the show_with parameter - I don't know how to open your file!")
                
            else:
                os.system("%s %s"%(show_with, outfile))
        
        return outfile
    
    def finalize_page(self):
        """
        Called on page end
        """
        self._canvas.showPage()
        
    def _translate_coords(self, obj):
        """
        Translates coordinates from PyRep's convention (left to right and top to bottom) to ReportMan's
        """
        
        x = obj.parent.x + obj.x
        y = self.report.page.height - obj.parent.y - obj.y
        
        if hasattr(obj, "font"):
            y -= obj.font.size / rl_mm

        return tuple(n*rl_mm for n in (x,y))

    def _set_font(self, font):
        """
		Sets the current font
        """

        for face in font.faces:
            try:
                if Font.BOLD and Font.ITALIC in font.style:
                    face+="-BoldOblique"
                elif Font.BOLD in font.style:
                    face+="-Bold"
                elif Font.ITALIC in font.style:
                    face+="-Oblique"
                    
                self._canvas.setFont(face,font.size)
            except KeyError:
                continue
            else:
                font.face=face
                break
        else:
            raise ReportError("No available fonts. Font list: %s"%font.faces)

    def draw_text(self, text, environment = None):
        """
        Draws a text object
        """
        
        x, y = self._translate_coords(text)
        
        txt = str(self.safe_eval(text.value, environment))
        
        self._set_font(text.font)

        if text.alignment == Text.ALIGN_LEFT:
            self._canvas.drawString(x,y,txt)
        elif text.alignment == Text.ALIGN_CENTER:
            self._canvas.drawCentredString(x + (text.width * rl_mm * 0.5), y, txt)
        elif text.alignment == Text.ALIGN_RIGHT:
            self._canvas.drawRightString( x + text.width * rl_mm, y, txt)

    def draw_hline(self, shape, environment = None):
        """
        Draws an horizontal line
        """
        
        x, y = self._translate_coords(shape)
        
        self._canvas.setLineWidth(shape.linewidth * rl_mm)
        
        x2, y2 = ((x + shape.width * rl_mm), y)
        
        self._canvas.line(x, y, x2, y2)

    def draw_vline(self, shape, environment = None):
        """
        Draws a vertical line
        """

        x, y = self._translate_coords(shape)

        self._canvas.setLineWidth(shape.linewidth * rl_mm)
        
        x2, y2 = (x, (y + shape.height * rl_mm))
        
        self._canvas.line(x, y, x2, y2)