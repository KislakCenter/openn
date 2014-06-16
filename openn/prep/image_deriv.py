import os
import subprocess
from openn.openn_exception import OPennException

def generate(pkg_dir, master, deriv, max_side):
    """
    Generate the `deriv` from `master` specifying a `-resize` of `max_side`
    pixels. It is expected that master and deriv paths will be relative; e.g.,
    `data/master/0001_0001.tif` and `data/web/0001_0001_web.tif`. The `pkg_dir`
    parameter is used to create the absolute path to the file.
    """
    # only shc
    size = "%dx%d>" % (max_side, max_side)
    infile = os.path.join(pkg_dir, master)
    outfile = os.path.join(pkg_dir, deriv)
    p = subprocess.Popen(["convert", infile,  '-resize', size, outfile],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE)
    out, err = p.communicate()

    if p.returncode is not 0:
        msg = "Error generating derivative %s from master %s: %s" % (deriv, master, err)
        raise OPennException(msg)
