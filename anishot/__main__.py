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
gflags.DEFINE_integer('pad', 0, 'Padding on sides')
gflags.DEFINE_integer('maxspeed', 200, 'Max speed on scroll px/frame')
gflags.DEFINE_list('stops', [], 'List of stops for scrolling')
gflags.DEFINE_integer('zoom_steps', 7, 'Number of steps on initial zoom in')
gflags.DEFINE_float('start_scale', .5, 'Start scale')
gflags.DEFINE_integer('zoom_to', 0, 'Point to zoom to')

gflags.DEFINE_integer('shadow_size', 0, 'Shadow size')
gflags.DEFINE_string('rgb_outline', '#e1e4e8', 'Screenshot outline color')
gflags.DEFINE_string('rgb_bg', '#ffffff', 'Background color')
gflags.DEFINE_string('rgb_shadow', '#999999', 'Screenshot shadow color')
gflags.DEFINE_string('rgb_window', '#e1e4e8', 'Window outline color')

gflags.register_validator('inp', os.path.exists, 'Input screenshot required')
gflags.register_validator('h', lambda v: v > 0, 'Window height required')

F = gflags.FLAGS


def make_blank_frame(width):
    return Image.new('RGB', (width + F.pad * 2, F.h), F.rgb_bg)


def scale_image(image, scale):
    w, h = int(image.width * scale + .5), int(image.height * scale + .5)
    return image.resize((w, h), Image.LANCZOS)


def render_frame(image, y, frame):
    w, h = image.size
    fw, fh = frame.size
    x = (fw - w) // 2

    draw = Draw(frame)

    # Draw shadow and image.
    off = F.shadow_size
    draw.rectangle([x + off, y + off, x + off + w, y + off + h], F.rgb_shadow)
    frame.paste(image, (x, y))
    draw.rectangle([x, y, x + w, y + h], outline=F.rgb_outline)

    # Draw a frame border.
    draw.rectangle([0, 0, fw - 1, fh - 1], outline=F.rgb_window)


def add_frame(frame, duration, frames):
    frames.append((frame, duration))


def make_zoomin(image, frames):
    w, h = image.size
    scale = F.start_scale
    step = (1 - scale) / (F.zoom_steps + 1)
    start_y = -F.h / 10 / scale
    for i in range(F.zoom_steps):
        scaled = scale_image(image, scale)
        frame = make_blank_frame(w)

        progress = (F.zoom_steps - i - 1) / (F.zoom_steps - 1)
        y = -int((progress * start_y + (1 - progress) * F.zoom_to) * scale + .5)
        render_frame(scaled, y, frame)
        add_frame(frame, .1 if i > 0 else 1.5, frames)

        scale += step


def add_scroll_frame(image, y, duration, frames):
    frame = make_blank_frame(image.width)
    render_frame(image, -y, frame)
    add_frame(frame, duration, frames)


def make_scroll(image, frames):
    w, h = image.size

    stops = [F.zoom_to] + list(map(int, F.stops)) + [h - F.h + F.pad]
    add_scroll_frame(image, stops[0], 2, frames)
    for i in range(len(stops) - 1):
        s0, s1 = stops[i:i + 2]
        speed = 10
        y = s0 + speed

        while y < s1:
            add_scroll_frame(image, y, .01, frames)
            y += speed
            speed = min(speed * 2, F.maxspeed)

        add_scroll_frame(image, s1, 2, frames)


def main():
    argv = sys.argv
    try:
        F(argv)

        image = Image.fromarray(imageio.imread(F.inp))
        frames = []

        if F.zoom_steps:
            make_zoomin(image, frames)
        make_scroll(image, frames)

        imageio.mimwrite(F.out,
                         map(lambda f: numpy.array(f[0]), frames),
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
