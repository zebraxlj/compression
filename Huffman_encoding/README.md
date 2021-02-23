Outline:
    1. preparing: create a binary tree such that 
        1. each leaf node is a character
        2. character, which has higher occurrance, has lower degree in the tree
            str: a a a b b a c c c d e e a
            occurance: a=5 b=2 c=3 d=1 e=3
            occurance(ordered): a=5 c=3 e=3 b=2 d=1
                 root
               0/    \1
            a(5)      node
                    0/    \1
                node        node
               0/  \1      0/  \1
             c(3)  e(3)  b(2)  d(1)

    2. encoding: for each character in the string to be encoded, we record the path to the char leaf node from the root (left child=0 right=1)
        a=0, b=110, c=100, d=111, e=101
        str.encode('Huffman') = 0 0 0 110 110 0 100 100 100 111 101 101 0
    3. decoding: triverse the tree from the root based on the encoded string/binary. Each time reaching a leaf node, take that char and go back to the root
Note: 
    1. because all characters {c_n} are in the leaf nodes, encoding of any character {c_1} will not be part of {c_2}
    2. core: character with higher occurrance has lower degree in the tree, which enhence them to have shorter encoding
    3. this encoding requires to have the stat of characters to build the tree, which works good for compressing documents/text files, where we have the access to the entire file at the begining. It might not work with realtime network transaction.


Reference:
[bilibili](https://www.bilibili.com/video/BV1dE411Z7Zw?from=search&seid=4362378879392483366)
[Huffman Coding Compression Algorithm](https://www.techiedelight.com/huffman-coding/)
