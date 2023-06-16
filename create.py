from lzw.Compress import compress as comp
from lzw.Decompress import decompress as dec
import time
import os

# test to check git

for i in range(1, 4):
    inp = 'SampleTextFiles/words20000/file'+str(i)+'.txt'
    out = 'output/file'+str(i)+'_compressed.txt'
    c = comp(inp,'output')
    starte = time.time()
    c.encode()
    ende = time.time()

    d = dec(out,'output')

    start = time.time()
    d.decode()

    end = time.time()

    print("Encode time: ", (ende - starte) * 10 ** 3, "ms")
    input_file_size = os.path.getsize(inp)
    print("Input file" + str(i) + " size is: ", input_file_size, "bytes")
    output_file_size = os.path.getsize(out)
    print("Decode time: ", (end - start) * 10 ** 3, "ms")
    print("Output file size is: ", output_file_size, "bytes")




    print()