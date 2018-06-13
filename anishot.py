"""Animate a long screenshot."""

__copyright__ = 'Copyright 2018 Sourcerer'
__author__ = 'Sergey Surkov'

import os
import sys

import gflags
import imageio
import numpy

from PIL import Image
from PIL.ImageDraw import Draw

gflags.DEFINE_string('inp', None, 'Input screenshot image')
gflags.DEFINE_string('out', None, 'Output antimated GIF')

gflags.DEFINE_integer('h', 0, 'Window height')
gflags.DEFINE_integer('maxspeed', 200, 'Max speed on scroll px/frame')
gflags.DEFINE_list('stops', [], 'List of stops for scrolling')

gflags.register_validator('inp', os.path.exists, 'Input screenshot required')
gflags.register_validator('h', lambda v: v > 0, 'Window height required')

F = gflags.FLAGS

def add_frame(frames, frame, duration):
    frames.append((prettify(frame), duration))

def prettify(frame):
    off = 5
    h, w = frame.shape[:2]
    pretty = Image.new('RGB', (w + off, h + off), '#ffffff')
    draw = Draw(pretty)
    draw.rectangle([off, off, w + off, h + off], '#cccccc', '#cccccc')
    pretty.paste(Image.fromarray(frame), (0, 0))
    draw.rectangle([0, 0, w, h], outline='#666666')
    return numpy.array(pretty)


def main(argv):
    try:
        F(argv)

        image = imageio.imread(F.inp)
        h, w = image.shape[:2]

        frames = []

        stops = [0] + list(map(int, F.stops)) + [h - F.h]
        y_pos = []
        add_frame(frames, image[stops[0]:stops[0] + F.h, :], 2)
        for i in range(len(stops) - 1):
            s0, s1 = stops[i:i + 2]
            speed = 10
            y = s0 + speed
            while y < s1:
                add_frame(frames, image[y:y + F.h, :], .01)
                y += speed
                print(speed)
                speed = min(speed * 2, F.maxspeed)
            add_frame(frames, image[s1:s1 + F.h, :], 2)

        imageio.mimwrite('foo.gif',
                         map(lambda f: f[0], frames),
                         duration=list(map(lambda f: f[1], frames)))
    except gflags.FlagsError as e:
        print('e: ', e)
        print('Usage: %s' % F)
        return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
