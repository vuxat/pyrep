from pyrep import *

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

        self.assertEqual( Color.BLACK, Color(0,0,0))
        self.assertEqual( Color.WHITE, Color(255,255,255))
    
        c = Color(11, 22, 33)
        
        self.assertEqual(c[0], 11)
        self.assertEqual(c[1], 22)
        self.assertEqual(c[2], 33)
        
        self.assertEqual(tuple(c), (11, 22, 33))
    
    def testSize(self):
        s = Size(19, 82)
        
        self.assertEqual(len(s), 2)
        self.assertEqual(tuple(s), (19, 82))
        self.assertEqual(s.width, 19)
        self.assertEqual(s.height, 82)
        self.assertEqual(s[0], s.width, 19)
        self.assertEqual(s[1], s.height, 82)
        
        s.width = 82
        s.height = 19
        
        self.assertEqual(len(s), 2)
        self.assertEqual(tuple(s), (82, 19))
        self.assertEqual(s.width, 82)
        self.assertEqual(s.height, 19)
        self.assertEqual(s[0], s.width, 82)
        self.assertEqual(s[1], s.height, 19)
        
        s[0] = 19
        s[1] = 82

        self.assertEqual(len(s), 2)
        self.assertEqual(tuple(s), (19, 82))
        self.assertEqual(s.width, 19)
        self.assertEqual(s.height, 82)
        self.assertEqual(s[0], s.width, 19)
        self.assertEqual(s[1], s.height, 82)
        
        self.assertEqual(s - 1, (18, 81))
        self.assertEqual(s - (2, 3,), (17, 79))
        
        s -= 1
        self.assertEqual(s.width, 18)
        self.assertEqual(s.height, 81)

        s -= (1, 2,)
        self.assertEqual(s.width, 17)
        self.assertEqual(s.height, 79)
        
    def testUnits(self):
        self.assertEqual(mm(123), 123)
        self.assertEqual(mm(123,456), (123, 456))
        
        self.assertEqual(cm(123), 1230)
        self.assertEqual(cm(123,456), (1230,4560))
        
suite = unittest.makeSuite(TestBaseClasses)

__all__=["suite"]

