import os
import lzw.dicts as d
from lzw.check import enc_check
import time
from datetime import timedelta

class compress():
    """This class provides compression of an 'utf-8' encoded file. Please note that no
    other formats are supported and may lead to catastrophic errors.
    Usage:
    obj = compress('full/path/to/input_file','path/for/storing/output_file'[[,limit,verbose])
    limit is an integer which specifies the max input file size. The default is 20MB.
    The limit can be changed but note that larger files take terribly large times(as of now).
    is_text is to be set as False iff the file to be compressed is not a plain English text file.
    Basically, the program uses a initial dictionary of ASCII chars 0-255 if is_text=False.
    is_text is True by default, and the initial dictionary contains ASCII chars 0-127.
    The verbose input, if set to 2, the program displays percent execution per chunk.
    verbose=1 shows the execution time per chunk of input file processed.
    Note: The verbose=2 option may generate large amounts of output on stdout and is 0
    by default.
    chunks(default=None) is an integer type argument used to specify the number of chunks in which the file is divided in
    during compression. By default, the program adoptively decides this number. chunks are useful
    for very large files as a single chunk is loaded into RAM during compression. The maximum
    value allowed is 100 chunks.

    Once instantiated, call the encode method(without any arguments) on the object to begin compression.
    """
    def __init__(self,input_file_path='',output_file_path='',limit=20000000,is_text=True,verbose=0,chunks=None):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.sizeLimit = limit
        self.is_text = is_text
        self.verbose = verbose
        enc_check(infile=self.input_file_path,outpath=self.output_file_path,sLimit=self.sizeLimit)
        infilesize = os.stat(self.input_file_path).st_size
        self.chunks = chunks
        if not self.chunks or self.chunks > 100:
            if infilesize <= 100000:
                self.chunks = 1;
            elif infilesize <= 4000000 and infilesize > 100000:
                self.chunks = 4;
            elif infilesize > 4000000 and infilesize <= 10000000:
                self.chunks = 6;
            elif infilesize > 10000000 and infilesize <= 20000000:
                self.chunks = 8;
            elif infilesize > 20000000:
                self.chunks = 10;

        self.chunksize = infilesize//self.chunks

    def encode(self):
        """See help(docstring) for class compress."""
        infile = self.input_file_path
        outpath = self.output_file_path
        wr_path = outpath if outpath[len(outpath)-1] == '/' else outpath+'/'
        fpath,fname = os.path.split(infile)
        fn,fext = os.path.splitext(infile)

        bit_stream = []
        sym_stream = str()
        ssptr = 0
        fsize = 0       #Number of bits in generated bit_stream
        address = int()

        temp_path = fpath+'/'+'compress_temp.txt'

        with open(wr_path+fname.split('.')[0]+'_compressed.txt','w') as f:
            pass

        with open(infile,'rb') as fin:
            print("Reading file and preparing to compress...")
            s1 = str()
            skip  = False
            flag = bool()
            if self.is_text:
                w_len = d.is_t_enc_len
                root = d.ascii_root
                address = 128
                word_size = d.is_t_enc_size
            else:
                w_len = d.enc_len
                root = d.ex_ascii_root
                address = 256
                word_size = d.d_enc_size
            m = 1
            for chunk in range(self.chunks):
                if chunk == (self.chunks-1):
                    sym_stream = sym_stream[ssptr:] + fin.read().decode('utf-8')
                    ssptr = 0
                    if sym_stream[len(sym_stream)-1] == '\n':
                        sym_stream =  sym_stream[:len(sym_stream)-1]
                else:
                    sym_stream = sym_stream[ssptr:] + fin.read(self.chunksize).decode('utf-8')
                    ssptr = 0

                if self.verbose in [0,1]:
                    print("Processing file in chunks of {0}bytes. Working on chunk{1}/{2}".format(self.chunksize,chunk+1,self.chunks))
                if self.verbose == 1:
                    st = time.monotonic()
                lss = len(sym_stream)
                while True:
                    if address in word_size:
                        w_len += 1

                    if self.verbose == 2:
                        print("Proccessing...part {0}/{1} of input file: ".format(chunk+1,self.chunks),end='')
                        print("{:.2f}".format(ssptr*100/lss)+"% done")

                    if lss-ssptr <= m+1:
                        if chunk < self.chunks-1:
                            break
                    if ssptr >= lss or lss-ssptr <= m:
                        if chunk == (self.chunks-1) and not skip:
                            s = sym_stream[ssptr:]
                            skip = True
                            s1 = s

                    if not skip:
                        s = sym_stream[ssptr:ssptr+m]
                        ssptr += m
                        s1 = str(s)

                    flag = False
                    match = ''
                    for i in range(len(s1),0,-1):
                        match_node = root.find(s1[:i])
                        if match_node:
                            if match_node.addr:
                                match = match_node.value
                                val = bin(match_node.addr)
                                flag = True  #Match found!
                                break

                    if len(val[2:]) < w_len:
                        for j in range(w_len - len(val[2:])):
                            bit_stream.append('0')
                    for sing_bit in val[2:]:
                        bit_stream.append(sing_bit)

                    if not skip:
                        if len(match) == len(s1):
                            match = match + sym_stream[ssptr:ssptr+1]
                        else:
                            match = s1[:len(match)+1]
                            temp = int()
                            temp = (-1)*(len(s1)-len(match)+1)
                            ssptr += temp

                    if skip:
                        if len(match) == len(s1):
                            break
                        else:
                            match = s1[:len(match)+1]
                            s1 = s1[len(match)-1:]

                    if len(match) > m:
                        m = len(match)

                    root.insert(match,address)
                    address += 1

                if self.verbose == 1:
                    end_t = time.monotonic()
                    print("Chunk {0}/{1}: Execution time: ".format(chunk+1,self.chunks),end='')
                    print(timedelta(seconds=end_t - st))
                lbs = len(bit_stream)
                if lbs:
                    fsize += lbs//8
                    with open(wr_path+fname.split('.')[0]+'_compressed.txt','ab') as f:
                        for bptr in range(0,(lbs//8)*8,8):
                            r = bit_stream[bptr:bptr+8]
                            f.write(int("".join(r),2).to_bytes(1,'little'))
                        if chunk == (self.chunks-1):
                            r = bit_stream[bptr+8:]
                            frem = len(r)
                            if frem:
                                f.write(int("".join(r),2).to_bytes(1,'little'))
                            f.write(fsize.to_bytes(4,'little'))
                            f.write(frem.to_bytes(1,'little'))
                        else:
                            bit_stream = bit_stream[bptr+8:]

        root.self_destruct()
        del bit_stream
        del sym_stream
