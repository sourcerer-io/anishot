"""Animate a long screenshot."""

__copyright__ = 'Copyright 2018 Sourcerer'
__author__ = 'Sergey Surkov'

import os
import sys

import gflags

gflags.DEFINE_string('in', None, 'Input screenshot image')
gflags.DEFINE_string('out', None, 'Output antimated GIF')

gflags.DEFINE_integer('h', 0, 'Window height')

gflags.register_validator('in', os.path.exists, 'Input screenshot required')
gflags.register_validator('h', lambda v: v > 0, 'Window height required')

F = gflags.FLAGS

def main(argv):
    try:
        F(argv)
    except gflags.FlagsError as e:
        print('e: ', e)
        print('Usage: %s' % F)
        return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
