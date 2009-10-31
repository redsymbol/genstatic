import os
from optparse import OptionParser
__all__ = [
    'main',
    'GSOptionParser',
    'prepare_output_dir',
    ]
class GSOptionParser(OptionParser):
    def __init__(self):
        super(GSOptionParser, self).__init__()
        self.set_usage('usage: [-c] %prog templates_dir dest_dir')
        self.add_option('-c', '--clobber', action='store_true', default=False,
                        help='If dest_dir exists, erase it and recreate');

def main(opts, args):
    pass

def prepare_output_dir(path):
    os.makedirs(path)

