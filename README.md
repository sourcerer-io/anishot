# anishot
[![Build Status](https://travis-ci.com/sourcerer-io/anishot.svg?branch=master)](https://travis-ci.com/sourcerer-io/anishot)
![PyPI](https://img.shields.io/pypi/v/anishot.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/anishot.svg)
![PyPI - License](https://img.shields.io/pypi/l/anishot.svg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/anishot.svg)

Animates a long screenshot into a GIF. Use it to show off long screenshots in your GitHub README.

![clean look](https://user-images.githubusercontent.com/20287615/42131345-5e13bb52-7cb5-11e8-93d3-d448684dc1c5.gif)

## Install

```
$ pip install anishot
```

## Usage
```
$ anishot --help
usage: anishot [-h] [--pad PAD] [--maxspeed MAXSPEED] [--stops [STOPS [STOPS ...]]]
               [--zoom-steps ZOOM_STEPS] [--start-scale START_SCALE]
               [--zoom-to ZOOM_TO] [--shadow-size SHADOW_SIZE]
               [--rgb-outline RGB_OUTLINE] [--rgb-background RGB_BACKGROUND]
               [--rgb-shadow RGB_SHADOW] [--rgb-window RGB_WINDOW]
               input output height

Animates a long screenshot into a GIF

positional arguments:
  input                 Input screenshot image
  output                Output animated GIF
  height                Window height

optional arguments:
  -h, --help            show this help message and exit
  --pad PAD     Padding on sides
  --maxspeed MAXSPEED
                        Max speed on scroll px/frame
  --stops [STOPS [STOPS ...]]
                        Stops between scrolls, px
  --zoom-steps ZOOM_STEPS
                        Number of steps on initial zoom in
  --start-scale START_SCALE
                        Start scale
  --zoom-to ZOOM_TO     Point to zoom to
  --shadow-size SHADOW_SIZE
                        Shadow size
  --rgb-outline RGB_OUTLINE
                        Screenshot outline color
  --rgb-background RGB_BACKGROUND
                        Background color
  --rgb-shadow RGB_SHADOW
                        Screenshot shadow color
  --rgb-window RGB_WINDOW
                        Window outline color
```

The anishot at the top of this README was generated by:
``anishot --stops 290 640 940 --zoom-to 150 --start-scale .7 anishot.png anishot.gif 450``

You can also experiment with styles. For example, you can go for a retro look:

``anishot --stops 290 640 940 --zoom-to 150 --start-scale .7 --pad 50 --shadow-size 5 --rgb-bg #cccccc --rgb-window #666666 anishot.png anishot.gif 450 `` 

![retro look](https://user-images.githubusercontent.com/20287615/42131349-64488250-7cb5-11e8-863f-b3156e709ddc.gif)

## Contributing
Contributions are welcome!

[![](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/images/0)](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/links/0)
[![](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/images/1)](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/links/1)
[![](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/images/2)](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/links/2)
[![](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/images/3)](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/links/3)
[![](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/images/4)](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/links/4)
[![](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/images/5)](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/links/5)
[![](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/images/6)](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/links/6)
[![](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/images/7)](https://sourcerer.io/fame/sergey48k/sourcerer-io/anishot/links/7)
