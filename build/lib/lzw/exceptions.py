class lzwExc(Exception):
    pass

class NoAccess(lzwExc):

    def __init__(self,message=''):
        self.message = 'Either the file '+message+" doesn't exist or the program is unable to access it"

class LargeFile(lzwExc):
    def __init__(self):
        self.msg = "Files larger than 30MB may take substantial amount of time for compression.\
         Do you want to proceed Y/N ?"

class sizeError(lzwExc):
    def __init__(self,size,m1='',m2=''):
        self.msg = m1+str(size)+m2

class DecompressFileError(lzwExc):
    def __init__(self,msg=''):
        self.msg = msg

class UnicodeRangeError(lzwExc):
    def __init__(self,max_sz):
        self.msg = 'Allowed maximum unicode character size = '+str(max_sz)+'. Allowed minimum size = 0.'

class InvalidEncoding(lzwExc):
    def __init__(self,msg=''):
        self.msg = 'Allowed encodings are ascii_127 or ascii_255 or utf-8.'
