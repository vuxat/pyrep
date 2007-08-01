from pyrep.base import *

import unittest

class TestBaseClasses(unittest.TestCase):
    def testColor(self):
        
        c = Color(0, 0, 0)
        c = Color(255, 255, 255)
        
        try:
            c = Color( -1, 0, 0 )
            c = Color( 0, -1, 0 )
            c = Color( 0, 0, -1 )
            c = Color( 256, 0, 0 )
            c = Color( 0, 256, 0 )
            c = Color( 0, 0, 256 )
        except ReportError:
            pass
        else:
            raise AssertionError("Invalid color accepted")

        self.assert_( Color.BLACK == Color(0,0,0))
        self.assert_( Color.WHITE == Color(255,255,255))
    
    def testUnits(self):
        self.assert_(mm(123) == 123)
        self.assert_(mm(123,456) == (123, 456))
        
        self.assert_(cm(123) == 1230)
        self.assert_(cm(123,456) == (1230,4560))
        
suite = unittest.makeSuite(TestBaseClasses)

__all__=["suite"]

