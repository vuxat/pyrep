# Copyright(c) 2005-2007 Angelantonio Valente
# See LICENSE file for details.

"""
Test runner
"""
import os
import sys
sys.path.append("..")

import unittest

testmodules = [os.path.splitext(x)[0] for x in os.listdir(".") if x.startswith("test_") and x.endswith(".py")]

modules = [__import__(mod,globals(),locals(),mod) for mod in testmodules if mod[0] != '_' ]

suite = unittest.TestSuite([x.suite for x in modules])

unittest.TextTestRunner(verbosity=2).run(suite)
