from lzw.trie import trie
from sys import maxunicode
from math import log2

ex_ascii_root = trie()
for i in range(256):
    ex_ascii_root.insert(chr(i),addr=i)

ascii_root = trie()
for i in range(128):
    ascii_root.insert(chr(i),addr=i)

unic_root = trie()
unic_list = []
unic_dict = dict()
unic_enc_size = list()
unic_dec_size = list()
unic_enc_len = int()
unic_dec_len = int()
def utf_8_trie(max_char):
    global unic_root
    global unic_list
    global unic_dict
    global unic_enc_size
    global unic_dec_size
    global unic_enc_len
    global unic_dec_len
    for i in range(max_char+1):
        unic_root.insert(chr(i),addr=i)
    unic_list = [chr(a) for a in range(max_char+1)]
    unic_dict = {unic_list[i]:i for i in range(max_char+1)}
    enc = int(log2(max_char))
    unic_enc_size = [2**i for i in range(enc+1,enc+31)]
    unic_dec_size = [(2**i)-1 for i in range(enc+1,enc+31)]
    unic_enc_len = enc + 1
    unic_dec_len = enc + 2


init_lis = [chr(a) for a in range(256)]
init_dict = {init_lis[i]:i for i in range(256)}

text_lis = [chr(a) for a in range(128)]
text_dict = {text_lis[i]:i for i in range(128)}

d_enc_size = [2**i for i in range(8,25)]
d_dec_size = [(2**i)-1 for i in range(8,25)]

is_t_enc_size = [2**i for i in range(7,25)]
is_t_dec_size = [(2**i)-1 for i in range(7,25)]

is_t_enc_len = 7
is_t_dec_len = 8

enc_len = 8
dec_len = 9
