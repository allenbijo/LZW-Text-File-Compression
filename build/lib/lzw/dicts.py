from lzw.trie import trie

ex_ascii_root = trie()
for i in range(256):
    ex_ascii_root.insert(chr(i),addr=i)

ascii_root = trie()
for i in range(128):
    ascii_root.insert(chr(i),addr=i)

init_lis = [chr(a) for a in range(256)]
init_dict = {init_lis[i]:i for i in range(len(init_lis))}

text_lis = [chr(a) for a in range(128)]
text_dict = {text_lis[i]:i for i in range(len(text_lis))}

d_enc_size = [2**i for i in range(8,25)]
d_dec_size = [(2**i)-1 for i in range(8,25)]

is_t_enc_size = [2**i for i in range(7,25)]
is_t_dec_size = [(2**i)-1 for i in range(7,25)]

is_t_enc_len = 7
is_t_dec_len = 8

enc_len = 8
dec_len = 9
