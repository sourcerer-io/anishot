"""Animate a long screenshot."""

__copyright__ = 'Copyright 2018 Sourcerer'
__author__ = 'Sergey Surkov'

import os
import sys

from absl import flags as gflags
import imageio
import numpy

from PIL import Image
from PIL.ImageDraw import Draw

gflags.DEFINE_string('inp', None, 'Input screenshot image')
gflags.DEFINE_string('out', None, 'Output antimated GIF')

gflags.DEFINE_integer('h', 0, 'Window height')
gflags.DEFINE_integer('maxspeed', 200, 'Max speed on scroll px/frame')
gflags.DEFINE_list('stops', [], 'List of stops for scrolling')
gflags.DEFINE_integer('zoom', 0, 'Number of steps on initial zoom in')
gflags.DEFINE_float('zoom_frac', .3, 'Fraction of screenshot to see on zoomout')

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


def make_zoomin(image, frames):
    h, w = image.shape[:2]
    scale = F.h / float(h) / F.zoom_frac
    step = (1 - scale) / (F.zoom + 1)
    original = Image.fromarray(image)
    for i in range(F.zoom):
        small = original.resize(
            (int(w * scale + .5), int(h * scale + .5)), Image.LANCZOS)
        scale += step
        small_w = small.size[0]
        frame = Image.new('RGB', (w, F.h), '#ffffff')
        off = (w - small_w) // 2
        frame.paste(small, (off, 0))
        draw = Draw(frame)
        draw.rectangle([off, 0, off + small_w, F.h], outline='#666666')
        add_frame(frames, numpy.array(frame), .2 if i > 0 else 1)


def make_scroll(image, frames):
    h, w = image.shape[:2]

    stops = [0] + list(map(int, F.stops)) + [h - F.h]
    add_frame(frames, image[stops[0]:stops[0] + F.h, :], 2)
    for i in range(len(stops) - 1):
        s0, s1 = stops[i:i + 2]

        speed = 10
        y = s0 + speed
        while y < s1:
            add_frame(frames, image[y:y + F.h, :], .01)
            y += speed
            speed = min(speed * 2, F.maxspeed)
        add_frame(frames, image[s1:s1 + F.h, :], 2)


def main():
    argv = sys.argv
    try:
        F(argv)

        image = imageio.imread(F.inp)
        frames = []

        if F.zoom:
            make_zoomin(image, frames)
        make_scroll(image, frames)

        imageio.mimwrite(F.out,
                         map(lambda f: f[0], frames),
                         duration=list(map(lambda f: f[1], frames)))
    except TypeError as e:
        print('e: ', e)
        print('Usage: %s' % F)
        return 1
    except gflags.Error as e:
        print('e: ', e)
        print('Usage: %s' % F)
        return 1


if __name__ == '__main__':
    sys.exit(main())
