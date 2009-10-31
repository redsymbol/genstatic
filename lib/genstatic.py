import os
from optparse import OptionParser
__all__ = [
    'main',
    'GSOptionParser',
    'prepare_output_dir',
    ]
class GSOptionParser(OptionParser):
    def __init__(self):
        OptionParser.__init__(self)
        self.set_usage('usage: [-c] %prog templates_dir dest_dir')
        self.add_option('-c', '--clobber', action='store_true', default=False,
                        help='If dest_dir exists, erase it and recreate');

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

def dj_render(base, path, dest):
    '''
    Render a file using the Django template engine

    base: template base directory
    path: path of template RELATIVE to base
    dest: location to write rendered output
    '''
    from django.template.loader import render_to_string
    rendered = render_to_string(path)
    with open(dest, 'w') as outf:
        outf.write(rendered)
        
def main(opts, args):
    base, out = args[0], args[1]
    init_django(base)
    prepare_output_dir(out)
    for item in find_files(base):
        dest = os.path.join(out, item)
        mkdir(os.path.dirname(dest))
        dj_render(base, item, dest)

def mkdir(path):
    try:
        os.makedirs(path)
    except OSError, e:
        # Ignore it if the file already exists
        if 17 != e.errno:
            raise
    
def prepare_output_dir(path):
    mkdir(path)
