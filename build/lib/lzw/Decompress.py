import os
from lzw.check import dec_check
import lzw.dicts as d
import time
from math import log2
from datetime import timedelta

class decompress():
    """This class provides functionality to decompress the file that was compressed by the
    (encode method of the) compress class of this package. Only .txt format files will be decompressed
    into another .txt file.
    Usage:
    object = decompress('full/path/to/file/to/be/decompressed','path/to/store/decompressed_file/'[[[[,limit,encoding,max_utf_char,verbose,chunks]]]])
    limit is an integer which specifies the max size of the file to be decompressed. The default is 20MB.
    The limit can be changed but note that larger files take substantially large times(as of now).

    encoding(default=ascii_255) is the encoding used while compression of the original file.
    See docstring for lzw.Compress.compress for details.
    max_utf_char(default=None) is to be used only for encoding='utf-8'. This value must match
    the one used for compressing the file.

    The verbose input, if set to 2, the program displays percent execution per chunk.
    verbose=1 shows the execution time per chunk of input file processed.
    Note: The verbose=2 option may generate large amounts of output on stdout and is 0
    by default.

    chunks(default=None) is an integer type argument used to specify the number of chunks in which the file is divided in
    during decompression. By default, the program adoptively decides this number. chunks are useful
    for very large files as a single chunk is loaded into RAM during decompression. The maximum
    value allowed is 100 chunks.

    Once initiated, call the decode method(without any arguments) on the object of this class to begin decompression.
    """
    def __init__(self,compressed_file_path='',output_file_path='',limit=20000000,encoding='ascii_255',max_utf_char=None,verbose=0,chunks=None):
        self.compressed_file_path = compressed_file_path
        self.output_file_path = output_file_path
        self.output_file_path = self.output_file_path if self.output_file_path[-1] == '/' else self.output_file_path+'/'
        self.sizeLimit = limit
        self.encoding = encoding
        self.max_utf_char = max_utf_char
        if self.encoding is 'utf-8' and self.max_utf_char is None:
            print('For utf-8 encoding max utf char is required')
            exit(1)
        self.chunks = chunks
        self.verbose = verbose
        self.chunksize = 1
        dec_check(infile=self.compressed_file_path,outpath=self.output_file_path,sLimit=self.sizeLimit,max_unic=self.max_utf_char,enco=self.encoding)

        if self.encoding is 'ascii_127':
            self.__dw_len = d.is_t_enc_len
            self.__l_dec = d.text_lis.copy()
            self.__d_dec = d.text_dict.copy()
            self.__dword_size = d.is_t_enc_size
            self.__dict_size = 128
        elif self.encoding is 'ascii_255':
            self.__dw_len = d.enc_len
            self.__l_dec = d.init_lis.copy()
            self.__d_dec = d.init_dict.copy()
            self.__dword_size = d.d_enc_size
            self.__dict_size = 256
        elif self.encoding == 'utf-8':
            enc = int(log2(self.max_utf_char))
            self.__dw_len = enc + 1
            self.__l_dec = [chr(a) for a in range(self.max_utf_char+1)]
            self.__d_dec = {self.__l_dec[i]:i for i in range(self.max_utf_char+1)}
            self.__dword_size = [2**i for i in range(enc,enc+31)]
            self.__dict_size = self.max_utf_char + 1

    def decode(self):
        """See help(docstring) for class decompress."""

        dw_len = self.__dw_len
        l_dec = self.__l_dec
        d_dec = self.__d_dec
        dword_size = self.__dword_size
        dict_size = self.__dict_size

        inpfile = self.compressed_file_path
        outpath = self.output_file_path
        s = ''
        curr_phr =  ''

        fpath,fname = os.path.split(inpfile)
        nm = fname.split('.')[0]
        data = []
        btsize=0

        with open(inpfile,'rb') as f:
            f.seek(-5,2)
            fsize = int.from_bytes(f.read(4),'little')
            frem = int.from_bytes(f.read(1),'little')
            btsize = (8*fsize)+frem

            if not self.chunks or self.chunks > 100:
                if fsize <= 1000000:
                    self.chunks = 1
                elif fsize > 1000000 and fsize <= 4000000:
                    self.chunks = 5
                elif fsize > 4000000 and fsize <= 10000000:
                    self.chunks = 10
                elif fsize > 10000000:
                    self.chunks = 15
            self.chunksize = fsize//self.chunks


        ptr = 0;
        with open(inpfile,'rb') as f, open(outpath+nm+'_decompressed.txt','w') as fop:
            print("Beginning to decompress...")
            for chunk in range(self.chunks):
                if chunk == (self.chunks-1):
                    for _ in range(self.chunksize+(fsize%self.chunksize)):
                        bts = format(int.from_bytes(f.read(1),'little'),'08b')
                        for b_count in list(bts):
                            data.append(b_count)

                    if frem:
                        bts = format(int.from_bytes(f.read(1),'little'),'08b')
                        dat = list(bts)
                        for i in dat[8-frem:]:
                            data.append(i)
                else:
                    for _ in range(self.chunksize):
                        bts = format(int.from_bytes(f.read(1),'little'),'08b')
                        for b_count in list(bts):
                            data.append(b_count)
                if self.verbose in [0,1]:
                    print("Processing file in chunks of {0}bytes. Working on chunk{1}/{2}".format(self.chunksize,chunk+1,self.chunks))
                if self.verbose == 1:
                    st = time.monotonic()
                data_len = len(data)
                dict_size = len(l_dec)

                while True:
                    if ptr >= data_len:
                        break

                    if (data_len - ptr) <= dw_len:
                        if chunk < (self.chunks-1):
                            data = data[ptr:]
                            ptr = 0
                            break

                    s = data[ptr:ptr+dw_len]
                    ptr += dw_len
                    s = ''.join(s)
                    if self.verbose == 2:
                        print("Decompressing...part {0}/{1} of input file: ".format(chunk+1,self.chunks),end='')
                        print("{:.2f}".format(ptr*100/data_len)+"% done")

                    if int(s,2) > (dict_size - 1):
                        l_dec.append(curr_phr+curr_phr[0])
                        dict_size += 1
                        d_dec[curr_phr+curr_phr[0]] = dict_size - 1
                        fop.write(curr_phr+curr_phr[0])
                        curr_phr = curr_phr+curr_phr[0]
                    else:
                        fop.write(l_dec[int(s,2)])
                        if curr_phr:
                            l_dec.append(curr_phr+l_dec[int(s,2)][0])
                            dict_size += 1
                            d_dec[curr_phr+l_dec[int(s,2)][0]] = dict_size - 1
                        curr_phr = l_dec[int(s,2)]

                    if dict_size in dword_size:
                        dw_len += 1

                if self.verbose == 1:
                    end_t = time.monotonic()
                    print("Chunk {0}/{1}: Execution time: ".format(chunk+1,self.chunks),end='')
                    print(timedelta(seconds=end_t - st))
        del l_dec
        del d_dec
        del data
        del dw_len
        del dict_size
        del ptr
        del dword_size
        del self.__l_dec
        del self.__d_dec
        del self.__dw_len
        del self.__dict_size
        del self.__dword_size
