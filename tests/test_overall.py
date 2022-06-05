import os
import re
import sys
import unittest
import tabnanny
import compileall

class TestOverall(unittest.TestCase):

    """
    Test overall package health by compiling and checking
    code style.
    """

    def testModules(self):
        """Testing all modules by compiling them"""
        src = f'.{os.sep}slixmpp'
        rx = re.compile('/[.]svn|.*26.*')
        self.assertTrue(compileall.compile_dir(src, rx=rx, quiet=True))

    def testTabNanny(self):
        """Testing that indentation is consistent"""
        self.assertFalse(tabnanny.check(f'..{os.sep}slixmpp'))


suite = unittest.TestLoader().loadTestsFromTestCase(TestOverall)
