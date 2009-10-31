import unittest
import os
import tempfile
import shutil
import genstatic

def is_dir(path):
    import os
    import stat
    return stat.S_ISDIR(os.stat(path)[stat.ST_MODE])

class Test_prepare_output_dir(unittest.TestCase):
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

class Test_find_files(unittest.TestCase):
    def test_main(self):
        actual = sorted(genstatic.find_files(os.path.join(os.path.dirname(__file__), 'data', 'a')))
        expected = sorted([
            'a.html',
            'b.html',
            ])
        self.assertEqual(expected, actual)
if '__main__' == __name__:
    unittest.main()
