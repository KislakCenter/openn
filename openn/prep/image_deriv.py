import os
import subprocess
from PIL import Image
from openn.openn_exception import OPennException

def generate(pkg_dir, master, deriv, max_side):
    """
    Generate the `deriv` from `master` specifying a `-resize` of `max_side`
    pixels. It is expected that master and deriv paths will be relative; e.g.,
    `data/master/0001_0001.tif` and `data/web/0001_0001_web.tif`. The `pkg_dir`
    parameter is used to create the absolute path to the file.
    """
    # only shc
    size = (max_side, max_side)
    infile = os.path.join(pkg_dir, master)
    outfile = os.path.join(pkg_dir, deriv)
    im = Image.open(infile)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(outfile)
    return details(pkg_dir, deriv)

def details(pkg_dir, img_path):
    """
    Return a dictionary of the image size in bytes, and width and height in
    pixels:

      {
          'path':   'data/web/0001_0001_web.jpg',
          'bytes':  177552,
          'width':  147,
          'height': 200
      }
    """
    path = os.path.join(pkg_dir, img_path)
    bytes = os.stat(path).st_size
    im = Image.open(path)
    width, height = im.size
    return {
            'path': img_path,
            'bytes': bytes,
            'width': width,
            'height': height 
            }
