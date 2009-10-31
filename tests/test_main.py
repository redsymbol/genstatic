import unittest
import os
import tempfile
import shutil
import genstatic

def is_dir(path):
    import os
    import stat
    return stat.S_ISDIR(os.stat(path)[stat.ST_MODE])


class ScratchdirTestCase(unittest.TestCase):
    debug = False
    def setUp(self):
        self.scratchdir = tempfile.mkdtemp()
        if 'DEBUG' in os.environ:
            print "scratch directory: %s" % self.scratchdir

    def tearDown(self):
        if self.debug and 'DEBUG' not in os.environ:
            shutil.rmtree(self.scratchdir)

class Test_prepare_output_dir(ScratchdirTestCase):
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

expected_render_b = '''<html>
  <head>

<style type="text/css">
  body {
  font-size: 18pt;
  font-family: sans-serif;
  background-color: #ccffcc;
  color: #222;
  }
</style>

  </head>
  <body>

<p>Hello Aaron.</p>

  </body>
</html>'''

class Test_dj_render(ScratchdirTestCase):
    def test_main(self):
        dest = os.path.join(self.scratchdir, 'a.html')
        base = os.path.join(os.path.dirname(__file__), 'data', 'b')
        genstatic.init_django(base)
        genstatic.dj_render(base, 'a.html', dest)
        actual = open(dest).read()
        self.assertEqual(expected_render_b, actual)

if '__main__' == __name__:
    unittest.main()
