"""
This python module is not to be directly imported in your
application for compression or decompression purposes. This module
simply provides helper functionality to the encode/decode process.
For instructions on using the compression algorithm see the README file.
The prime objective of this module is to perform quick sanity checks
on the target file to be compressed/decompressed and thereby avoid any
runtime anamolies.
"""

import os
from lzw.exceptions import *

def enc_check(infile='',outpath='',sLimit=10000000):
    """This function takes as input the full path of the file
    to be compressed along with the filename and performs some
    checks as to whether the program has access to the said path
    and whether the file is a valid text file or not."""

    if '.' in outpath:
        print("Please provide an output path not a file name. Make sure the path does not have a . in it.")
        exit()

    com_checks(infile,outpath,sLimit)


def dec_check(sLimit,infile='',outpath=''):

    fn,fext = os.path.splitext(infile)
    if not fext == '.txt':
        raise DecompressFileError('The file to be decompressed must be in the .txt extension/format.')
    if os.stat(infile).st_size > sLimit:
        raise sizeError(sLimit,'File size is greater than ','. Currently unsupported due to very large execution time.')
    com_checks(infile,outpath,sLimit)



def com_checks(infile,outpath,sLimit=10000000):

    if not os.access(infile,os.R_OK):
        raise NoAccess(infile)
    if not os.access(outpath,os.F_OK):
        raise NoAccess(outpath)
    if os.stat(infile).st_size > sLimit:
        raise sizeError(sLimit,'File size is greater than ','. Currently unsupported due to very large execution time.')

    try:
        if os.stat(infile).st_size > 12000000:
            raise LargeFile
    except LargeFile as lf:
        y = str(input(lf.msg))
        if y == 'y' or y == 'Y':
            pass
        else:
            exit()
