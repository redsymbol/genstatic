#!/usr/bin/env python2.6
from __future__ import unicode_literals
import os
import shutil
import sys
from optparse import OptionParser

class GSOptionParser(OptionParser):
    def __init__(self):
        OptionParser.__init__(self)
        self.set_usage('usage: [-c] %prog templates_dir dest_dir')
        self.add_option('-c', '--clobber', action='store_true', default=False,
                        help='If dest_dir exists, erase it and recreate');
        self.add_option('-d', '--defines', default=None,
                        help='Module with definitions for template');

def find_files(base):
    '''
    Find suitable template files

    Generates a list of paths relative to base.  Starts search under
    base, ignoring any paths starting with underscores, and certain
    other files.
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
    from django.conf import settings
    settings.configure(TEMPLATE_DIRS=(base,))

def dj_render(base, path, dest, params=None):
    '''
    Render a file using the Django template engine

    base: template base directory
    path: path of template RELATIVE to base
    dest: location to write rendered output
    '''
    from django.template.loader import render_to_string
    if not params:
        params = {}
    rendered = render_to_string(path, params)
    with open(dest, 'w') as outf:
        outf.write(rendered)
        
def mkdir(path):
    try:
        os.makedirs(path)
    except OSError, e:
        # Ignore it if the file already exists
        if 17 != e.errno:
            raise
    
def prepare_output_dir(path):
    mkdir(path)

def main(opts, base, out, params):
    init_django(base)
    prepare_output_dir(out)
    process(base, out, params)

def process(base, out, params):
    for item in find_files(base):
        dest = os.path.join(out, item)
        mkdir(os.path.dirname(dest))
        try:
            if item.endswith('.htm') or item.endswith('.html') or item.endswith('.php'):
                dj_render(base, item, dest, params)
            else:
                shutil.copyfile(os.path.join(base, item), dest)
        except Exception, e:
            print "ERROR: %s: %s" % (item, e)

def path2mod(path):
    assert path.endswith('.py')
    return path[:-3].split('/')[-1]

def load_params(module):
    if module.endswith('.py'):
        module = path2mod(module)
    import imp
    fp = None
    loaded = None
    params = {}
    imp.acquire_lock()
    try:
        fp, pathname, description = imp.find_module(module)
        loaded = imp.load_module(module, fp, pathname, description)
    except ImportError:
        pass
    finally:
        imp.release_lock()
        if hasattr(fp, 'close'):
            fp.close()
    if loaded:
        params = dict((k,v) for k, v in loaded.__dict__.iteritems()
                     if not k.startswith('__'))
    else:
        sys.stderr.write('\ngenstatic: Cannot import definition module "%s"\n' % str(module))
    return params

if '__main__' == __name__:
    # TODO: make genstatic be able to use external apps' filters/tags
    opts, args = GSOptionParser().parse_args()
    base, out = args[0], args[1]
    if opts.defines:
        params = load_params(opts.defines)
    else:
        params = {}
    main(opts, base, out, params)
