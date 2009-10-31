from unittest import TestCase
import os
import tempfile
import shutil
import genstatic

def is_dir(path):
    import os
    import stat
    return stat.S_ISDIR(os.stat(path)[stat.ST_MODE])

class Test_prepare_output_dir(TestCase):
    debug = False
    def setUp(self):
        self.scratchdir = tempfile.mkdtemp()

    def tearDown(self):
        if not self.debug:
            shutil.rmtree(self.scratchdir)

    def test_prepare_output_dir(self):
        dir_a = os.path.join(self.scratchdir, 'a')
        self.assertFalse(os.path.exists(dir_a))
        r = genstatic.prepare_output_dir(os.path.join(self.scratchdir, 'a'))
        self.assertTrue(os.path.exists(dir_a))
        self.assertTrue(is_dir(dir_a))
        
if '__main__' == __name__:
    import unittest
    unittest.main()
