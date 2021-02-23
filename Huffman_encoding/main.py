# -*- coding: utf-8 -*-

from collections import Counter
from datetime import datetime
import os, stat

DATA_FOLDER = '../data/'
C_STAT = None

class HuffmanTreeNode:
    def __init__(self, left, right, char, weight=None):
        self.left = left
        self.right = right
        self.char = char
        self.weight = weight
    
    def __repr__(self):
        l = 'NULL' if not self.left else self.left.char
        r = 'NULL' if not self.right else self.right.char
        return f'{self.char}\t\tl:{l}\t\tr:{r}\t\tw:{self.weight}'
    
    def is_leaf(self):
        return not self.char is None
        # return self.left == None and self.right == None

def generate_huffman_tree_old(text: str):
    c_count = Counter(text)
    C_STAT = {char:{'cnt':cnt} for (char, cnt) in c_count.items()}
    lst_c_count = [(char, cnt) for (char, cnt) in c_count.items()]
    lst_c_count.sort(key=lambda x: x[1], reverse=True)
    # print(lst_c_count)
    # [print(e[0], end='') for e in lst_c_count]
    # print()
    root = None
    while lst_c_count:
        node_l, node_r, node_parent = None, None, None
        if len(lst_c_count) >= 1:
            node_l = HuffmanTreeNode(None, None, lst_c_count.pop()[0])
        if len(lst_c_count) >= 1:
            node_r = HuffmanTreeNode(None, None, lst_c_count.pop()[0])

        if node_r:
            node_parent = HuffmanTreeNode(node_l, node_r, None)
        else:
            node_parent = node_l

        if not root:
            root = node_parent
        else:
            root = HuffmanTreeNode(node_parent, root, None)
    return root

def generate_huffman_tree(text: str):
    ### update status of each character 
    global C_STAT
    c_count = Counter(text)
    C_STAT = {char:{'cnt':cnt} for (char, cnt) in c_count.items()}
    lst_c_node = [[HuffmanTreeNode(None, None, char, cnt), cnt] for (char, cnt) in c_count.items()]
    # [print(node) for node in lst_c_node]
    
    if len(lst_c_node) == 1:
        l, l_w = lst_c_node.pop()
        node_tmp = HuffmanTreeNode(l, None, None, l_w)
        lst_c_node.append([node_tmp, l_w])

    ### greedly create Huffman tree
    #### when there're at least 2 nodes in the list, 
    ####    1. pop the 2 nodes with the lowest occurrance
    ####    2. create a parent node, where occurrance equals the sum of the 2 child node occurrance
    ####    3. insert the parent node back to the list w/ binary search or sort
    while len(lst_c_node) > 1:
        lst_c_node.sort(key=lambda x: x[1], reverse=True)
        l, l_w = lst_c_node.pop()
        r, r_w = lst_c_node.pop()
        node_tmp = HuffmanTreeNode(l, r, None, l_w+r_w)
        lst_c_node.append([node_tmp, l_w + r_w])
    # [print(node) for node in lst_c_node]

    return lst_c_node[0][0]

def encode(text: str):
    return ''.join([C_STAT[c]['code'] for c in text])

def decode(code, tree: HuffmanTreeNode):
    if code is None: raise Exception('encoded input cannot be None')
    if not tree: raise Exception('encoding tree is blank')

    if isinstance(code, str):
        set_c = set([c for c in code])
        set_c_invalid = set_c - {'0', '1'}
        if len(set_c_invalid) != 0: raise Exception(f'encoded input contain unexpected character(s): {set_c_invalid}')

        node_temp = tree
        list_c = []
        for i in range(len(code)):
            if code[i] == '0':
                node_temp = node_temp.left
            else: 
                node_temp = node_temp.right

            if node_temp.is_leaf():
                list_c.append(node_temp.char)
                node_temp = tree
        return ''.join(list_c) 

def generate_encoding_dict_from_tree(node: HuffmanTreeNode, path=''):
    global C_STAT
    if node.is_leaf():
        C_STAT[node.char]['code'] = path
    else:
        if node.left is not None: generate_encoding_dict_from_tree(node.left, path+'0')
        if node.right is not None: generate_encoding_dict_from_tree(node.right, path+'1')

def my_encode():
    raise NotImplementedError()

def my_get_tree_degree(root):
    print(root)
    if root is not None:
        if root.is_leaf():
            return 1
        else:
            return 1 + max(my_get_tree_degree(root.left), my_get_tree_degree(root.right))
    else:
        return 0

def my_print_tree(root, indent=0):
    print('\t'*indent, end='')
    print(root.char, root.weight, sep=' ')
    if root.left: my_print_tree(root.left, indent+1)
    if root.right: my_print_tree(root.right, indent+1)

def my_print_tree1(root):
    print(root)
    if root.left: my_print_tree(root.left)
    if root.right: my_print_tree(root.right)

def my_listdir(path):
    if not path: raise Exception(f'path is empty | {path}')
    fmt = '%-10s %27s %14s %s'
    print(fmt % ('Mode', 'LastWriteTime', 'Length', 'Name'))
    print(fmt % ('----', '-------------', '------', '----'))
    with os.scandir(path) as dir_entries:
        for entry in dir_entries:
            print(fmt % (
                        stat.filemode(entry.stat().st_mode), 
                        datetime.fromtimestamp(entry.stat().st_mtime).strftime('%d/%m/%Y  %I:%M %p'), 
                        entry.stat().st_size, 
                        entry.name
                        ))

def test():
    # read file
    file_raw = f'{DATA_FOLDER}/txt/A Tale of Two Cities - Charles Dickens.txt'
    with open(file_raw, 'r') as file:
        text = file.read()

    ### generate huffman tree
    huff_tree = generate_huffman_tree(text)
    my_print_tree(huff_tree)
    print('degree', my_get_tree_degree(huff_tree))

    ### update C_STAT to get all char encoding (optional)
    generate_encoding_dict_from_tree(huff_tree)
    [print(k,v) for k,v in sorted(C_STAT.items(), key=lambda x: x[1]['cnt'])]
    print('final bytes =', sum([c['cnt']*len(c['code']) for c in C_STAT.values()]) / 8)
    
    

    # show result
    my_listdir(f'{DATA_FOLDER}/txt/')

def my_end_to_end_test():
    text = 'abcdabcaba'
    huff_tree = generate_huffman_tree(text)
    generate_encoding_dict_from_tree(huff_tree)
    my_print_tree(huff_tree)
    
    tmp_encoded = encode(text)
    print(tmp_encoded)
    tmp_decoded = decode(tmp_encoded, huff_tree)
    print(tmp_decoded)

if __name__ == '__main__':
    # generate_huffman_tree('abca')
    # my_encode()
    # huff = HuffmanTreeNode()
    
    # test()
    # print(encode('abc'))
    pass
