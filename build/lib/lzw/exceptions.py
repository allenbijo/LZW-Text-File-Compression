class lzwExc(Exception):
    pass

class NoAccess(lzwExc):

    def __init__(self,message=''):
        self.message = 'Either the file '+message+" doesn't exist or the program is unable to access it"

class LargeFile(lzwExc):
    def __init__(self):
        self.msg = "Files larger than 12MB may take substantial amount of time for compression.\
         Do you want to proceed Y/N ?"

class sizeError(lzwExc):
    def __init__(self,size,m1='',m2=''):
        self.msg = m1+str(size)+m2

class DecompressFileError(lzwExc):
    def __init__(self,msg=''):
        self.msg = msg
