# Copyright(c) 2005-2007 Angelantonio Valente
# See LICENSE file for details.

"""
Test runner
"""

import unittest

modules=[
         'test_base', 'test_pdf', 'test_parser'
]

modules=[__import__(mod,globals(),locals(),mod) for mod in modules if mod[0] != '_' ]
suite=unittest.TestSuite([x.suite for x in modules])

unittest.TextTestRunner(verbosity=2).run(suite)
