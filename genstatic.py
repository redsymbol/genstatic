#!/usr/bin/env python2.6
from __future__ import unicode_literals
import os
import shutil
import sys
from optparse import OptionParser

USAGE_MSG = 'usage: [-c] %s templates_dir dest_dir'

class GSOptionParser(OptionParser):
    '''
    command line option parser
    '''
    def __init__(self):
        OptionParser.__init__(self)
        self.set_usage(USAGE_MSG % '%prog')
        self.add_option('-c', '--clobber', action='store_true', default=False,
                        help='If dest_dir exists, erase it and recreate');
        self.add_option('-d', '--defines', default=None,
                        help='Module with definitions for template');

def write_err(msg):
    '''
    Write an error message to console

    @param msg : The message to report
    @type  msg : str

    '''
    sys.stderr.write(msg)
    sys.stderr.flush()

def find_files(base):
    '''
    Find suitable template files

    Generates a list of paths relative to base.  Starts search under
    base, ignoring any paths starting with underscores, and certain
    other files.

    @param base : Path to base directory to begin search
    @type  base : str

    @return     : List of paths to temmplate files
    @rtype      : list of str

    '''
    def legit(path):
        if path.startswith('_') or path.endswith('~'):
            return False
        return True
    if not base.endswith('/'):
        base += '/'
    for dirpath, dirnames, filenames in os.walk(base):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            assert path.startswith(base)
            path = path.split(base)[-1]
            if legit(path):
                yield path

def init_django(base):
    '''
    Initialize django

    @param base : Path to base directory to begin search
    @type  base : str

    '''
    from django.conf import settings
    settings.configure(TEMPLATE_DIRS=(base,))

def dj_render(base, path, dest, params=None):
    '''
    Render a file using the Django template engine

    @param base   : path to template base directory
    @type  base   : str

    @param path   : path of template RELATIVE to base
    @type  path   : str

    @param dest   : location to write rendered output (path to a file)
    @type  dest   : str

    @param params : Template variables
    @type  params : dict (str -> mixed)

    '''
    from django.template.loader import render_to_string
    if not params:
        params = {}
    rendered = render_to_string(path, params)
    with open(dest, 'w') as outf:
        outf.write(rendered)
        
def mkdir(path):
    '''
    Safely make sure a directory exists, creating it if necessary

    @param path : Path to directory to create
    @type  path : str

    '''
    try:
        os.makedirs(path)
    except OSError, e:
        # Ignore it if the file already exists
        if 17 != e.errno:
            raise

def is_renderable(item):
    endings = (
        '.htm',
        '.html',
        '.php',
        )
    return any(item.endswith(ending)
               for ending in endings)

def process(base, outdir, params):
    '''
    Render and write all output files

    @param base   : path to template base directory
    @type  base   : str

    @param outdir : location to write output files (path to dir)
    @type  outdir : str

    @param params : Template variables
    @type  params : dict (str -> mixed)

    '''
    for item in find_files(base):
        dest = os.path.join(outdir, item)
        mkdir(os.path.dirname(dest))
        try:
            if is_renderable(item):
                dj_render(base, item, dest, params)
            else:
                shutil.copyfile(os.path.join(base, item), dest)
        except Exception, e:
            write_err("ERROR: %s: %s" % (item, e))

def path2mod(filepath):
    '''
    Convert a Python file path to a module name, and its import path

    @param path : Path to python file
    @type  path : str

    @return     : Tuple of module name, and module path
    @rtype      : tuple(str, str)

    '''
    assert filepath.endswith('.py')
    modpath, modname = os.path.split(filepath[:-3])
    if not modpath:
        modpath = '.'
    return modname, modpath

def load_params(modulearg):
    '''
    Load template variables and their values

    The module argument can be a module name (like "foo.bar", or
    "baz"), or a path to a Python file ('/path/to/stuff.py').

    @param modulearg   : Module argument as supplied by user
    @type  modulearg   : str

    @return            : Variables and their values
    @rtype             : dict (str -> mixed)

    @raise ImportError : The module could not be loaded.

    '''
    assert bool(modulearg)
    import imp
    fp = None
    loaded = None
    params = {}
    pythonpath = None
    if modulearg.endswith('.py'):
        module, modpath = path2mod(modulearg)
        pythonpath = [modpath]
    else:
        module = modulearg
    imp.acquire_lock()
    try:
        fp, pathname, description = imp.find_module(module, pythonpath)
        loaded = imp.load_module(module, fp, pathname, description)
    finally:
        # If there is any ImportError, just let it propagate.  but need to clean up first
        imp.release_lock()
        if hasattr(fp, 'close'):
            fp.close()
    assert loaded
    params = dict((k,v) for k, v in loaded.__dict__.iteritems()
                  if not k.startswith('__'))
    return params

def main(opts, base, outdir, params):
    '''
    Main program runner

    @param opts   : options
    @type  opts   : ?

    @param base   : path to template base directory
    @type  base   : str

    @param outdir : location to write output files (path to dir)
    @type  outdir : str

    @param params : Template variables
    @type  params : dict (str -> mixed)

    '''
    init_django(base)
    mkdir(outdir)
    process(base, outdir, params)

def exit_usage(retcode=0):
    '''
    Emit a usage message, then exit.

    @param retcode : Process return code
    @type  retcode : int
    
    '''
    print USAGE_MSG % os.path.basename(sys.argv[0])
    sys.exit(retcode)

if '__main__' == __name__:
    opts, args = GSOptionParser().parse_args()
    try:
        srcdir, outdir = args[0], args[1]
    except IndexError:
        exit_usage()
    params = {}
    if opts.defines:
        try:
            params = load_params(opts.defines)
        except ImportError:
            write_err('genstatic: Cannot import definition module/file "%s"\n' % str(opts.defines))
    main(opts, srcdir, outdir, params)
