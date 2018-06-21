import os
from lzw.check import dec_check
import lzw.dicts as d
import time
from datetime import timedelta

class decompress():
    """This class provides functionality to decompress the file that was compressed by the
    (encode method of the) compress class of this package. Only .txt format files will be decompressed
    into another .txt file.
    Usage:
    object = decompress('full/path/to/file/to/be/decompressed','path/to/store/decompressed_file/'[[[,limit,is_text,verbose]]])
    limit is an integer which specifies the max size of the file to be decompressed. The default is 20MB.
    The limit can be changed but note that larger files take substantially large times(as of now).
    is_text(default=True) is to be set False iff this same argument was false when the file was compressed.
    See docstring of lzw.Comrpess.compress for details on is_text.
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
    def __init__(self,compressed_file_path='',output_file_path='',limit=10000000,is_text=True,verbose=0,chunks=None):
        self.compressed_file_path = compressed_file_path
        self.output_file_path = output_file_path
        self.output_file_path = self.output_file_path if self.output_file_path[-1] == '/' else self.output_file_path+'/'
        self.sizeLimit = limit
        self.is_text = is_text
        self.chunks = chunks
        self.verbose = verbose
        self.chunksize = 1
        dec_check(infile=self.compressed_file_path,outpath=self.output_file_path,sLimit=self.sizeLimit)

    def decode(self):
        """See help(docstring) for class decompress."""
        if self.is_text:
            dw_len = d.is_t_dec_len
            l_dec = d.text_lis.copy()
            d_dec = d.text_dict.copy()
            dword_size = d.is_t_dec_size
            dict_size = 128
        else:
            dw_len = d.dec_len
            l_dec = d.init_lis.copy()
            d_dec = d.init_dict.copy()
            dword_size = d.d_dec_size
            dict_size = 256

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
                if fsize <= 100000:
                    self.chunks = 1
                elif fsize > 100000 and fsize <= 1000000:
                    self.chunks = 5
                elif fsize > 1000000 and fsize <= 10000000:
                    self.chunks = 10
                elif fsize > 10000000:
                    self.chunks = 15
            self.chunksize = fsize//self.chunks


        ptr = 0;
        with open(inpfile,'rb') as f, open(outpath+nm+'_decompressed.txt','w') as fop:
            print("Beginning to decompress...")
            for chunk in range(self.chunks):
                if chunk == (self.chunks-1):
                    st = time.monotonic()
                    for _ in range(self.chunksize+(fsize%self.chunksize)):
                        bts = format(int.from_bytes(f.read(1),'little'),'08b')
                        for b_count in list(bts):
                            data.append(b_count)

                    if frem:
                        bts = format(int.from_bytes(f.read(1),'little'),'08b')
                        dat = list(bts)
                        for i in dat[8-frem:]:
                            data.append(i)
                    end_t = time.monotonic()
                    print("Pre process time: ",end='')
                    print(timedelta(seconds=end_t -st))
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
                    #print(int(s,2), dict_size)
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
