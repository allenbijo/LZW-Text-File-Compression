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
from sys import maxunicode
from lzw.exceptions import *

def enc_check(infile='',outpath='',sLimit=15000000, max_unic=None,enco=None):
    """This function takes as input the full path of the file
    to be compressed along with the filename and performs some
    checks as to whether the program has access to the said path
    and whether the file is a valid text file or not."""

    if '.' in outpath:
        print("Please provide an output path not a file name. Make sure the path does not have a . in it.")
        exit()

    com_checks(infile,outpath,sLimit,max_unic)


def dec_check(sLimit,infile='',outpath='',max_unic=None,enco=None):

    fn,fext = os.path.splitext(infile)
    if not fext == '.txt':
        raise DecompressFileError('The file to be decompressed must be in the .txt extension/format.')
    if os.stat(infile).st_size > sLimit:
        raise sizeError(sLimit,'File size is greater than ','. Currently unsupported due to very large execution time.')
    com_checks(infile,outpath,sLimit,max_unic)



def com_checks(infile,outpath,sLimit=15000000,max_unic=None,enco=None):

    if not os.access(infile,os.R_OK):
        raise NoAccess(infile)
    if enco:
        if enco is 'ascii_127' or enco is 'ascii_255' or enco is 'utf-8':
            pass
        else:
            try:
                raise InvalidEncoding()
            except InvalidEncoding as ie:
                print(ie.msg)

    if max_unic and (max_unic > maxunicode or max_unic < 0):
        raise UnicodeRangeError(max_unic)
    if not os.access(outpath,os.F_OK):
        raise NoAccess(outpath)
    if os.stat(infile).st_size > sLimit:
        raise sizeError(sLimit,'File size is greater than ','. Currently unsupported due to very large execution time.')

    try:
        if os.stat(infile).st_size > 30000000:
            raise LargeFile
    except LargeFile as lf:
        y = str(input(lf.msg))
        if y == 'y' or y == 'Y':
            pass
        else:
            exit()
