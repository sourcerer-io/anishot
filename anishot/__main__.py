"""Animate a long screenshot."""

__copyright__ = 'Copyright 2018 Sourcerer'
__author__ = 'Sergey Surkov'

import argparse
import sys

import imageio
import numpy

from PIL import Image
from PIL.ImageDraw import Draw


ARGS = None


def argparser():
    parser = argparse.ArgumentParser(
        description='Animates a long screenshot into a GIF')
    parser.add_argument('input', type=argparse.FileType(),
                        help='Input screenshot image')
    parser.add_argument('output', type=str,
                        help='Output animated GIF')
    parser.add_argument('height', type=int,
                        help='Window height')
    parser.add_argument('-p', '--pad', default=0, type=int,
                        help='Padding on sides')
    parser.add_argument('-m', '--maxspeed', default=200, type=int,
                        help='Max speed on scroll px/frame')
    parser.add_argument('-s', '--stops', nargs='*', default=[],
                        help='Max speed on scroll px/frame')
    parser.add_argument('--zoom-steps', default=7, type=int,
                        help='Number of steps on initial zoom in')
    parser.add_argument('--start-scale', default=5, type=int,
                        help='Start scale')
    parser.add_argument('--zoom-to', default=0, type=int,
                        help='Point to zoom to')
    parser.add_argument('--shadow-size', default=0, type=int,
                        help='Shadow size')
    parser.add_argument('--rgb-outline', default='#e1e4e8', type=str,
                        help='Screenshot outline color')
    parser.add_argument('--rgb-background', default='#ffffff', type=str,
                        help='Background color')
    parser.add_argument('--rgb-shadow', default='#999999', type=str,
                        help='Screenshot shadow color')
    parser.add_argument('--rgb-window', default='#e1e4e8', type=str,
                        help='Window outline color')
    global ARGS
    ARGS = parser.parse_args()


def make_blank_frame(width):
    return Image.new('RGB',
                     (width + ARGS.pad * 2, ARGS.height), ARGS.rgb_background)


def scale_image(image, scale):
    w, h = int(image.width * scale + .5), int(image.height * scale + .5)
    return image.resize((w, h), Image.LANCZOS)


def render_frame(image, y, frame):
    w, h = image.size
    fw, fh = frame.size
    x = (fw - w) // 2

    draw = Draw(frame)

    # Draw shadow and image.
    off = ARGS.shadow_size
    draw.rectangle(
        [x + off, y + off, x + off + w, y + off + h], ARGS.rgb_shadow)
    frame.paste(image, (x, y))
    draw.rectangle([x, y, x + w, y + h], outline=ARGS.rgb_outline)

    # Draw a frame border.
    draw.rectangle([0, 0, fw - 1, fh - 1], outline=ARGS.rgb_window)


def add_frame(frame, duration, frames):
    frames.append((frame, duration))


def make_zoomin(image, frames):
    w, h = image.size
    scale = ARGS.start_scale
    step = (1 - scale) / (ARGS.zoom_steps + 1)
    start_y = -ARGS.height / 10 / scale
    for i in range(ARGS.zoom_steps):
        scaled = scale_image(image, scale)
        if not scaled:
            continue
        frame = make_blank_frame(w)

        progress = (ARGS.zoom_steps - i - 1) / (ARGS.zoom_steps - 1)
        y = -int((progress * start_y + (1 - progress) * ARGS.zoom_to) *
                 scale + .5)
        render_frame(scaled, y, frame)
        add_frame(frame, .1 if i > 0 else 1.5, frames)
        scale += step


def add_scroll_frame(image, y, duration, frames):
    frame = make_blank_frame(image.width)
    render_frame(image, -y, frame)
    add_frame(frame, duration, frames)


def make_scroll(image, frames):
    w, h = image.size

    stops = [ARGS.zoom_to] + \
        list(map(int, ARGS.stops)) + [h - ARGS.height + ARGS.pad]
    add_scroll_frame(image, stops[0], 2, frames)
    for i in range(len(stops) - 1):
        s0, s1 = stops[i:i + 2]
        speed = 10
        y = s0 + speed

        while y < s1:
            add_scroll_frame(image, y, .01, frames)
            y += speed
            speed = min(speed * 2, ARGS.maxspeed)

        add_scroll_frame(image, s1, 2, frames)


def process():
    image = Image.fromarray(imageio.imread(ARGS.input.name))
    frames = []

    if ARGS.zoom_steps:
        make_zoomin(image, frames)
    make_scroll(image, frames)

    imageio.mimwrite(ARGS.output,
                     map(lambda f: numpy.array(f[0]), frames),
                     duration=list(map(lambda f: f[1], frames)))


def check():
    if ARGS.output[-4:] != '.gif':
        raise ValueError("output must be a gif file")


def finish():
    msg = "Done! Generated file will be available at {}".format(ARGS.output)
    print(msg)


def main():
    try:
        argparser()
        check()
        process()
        finish()
    except ValueError:
        print("Invalid output filename")
        return 127


if __name__ == '__main__':
    sys.exit(main())
