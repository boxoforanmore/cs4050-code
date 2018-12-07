from __future__ import print_function
from sys import argv
import unittest


class Generate(object):
    class tree(object):
        def __init__(self, name=None, weight=None, left=None, right=None, visited=False):
            self.name = name
            self.weight = weight
            self.left = left
            self.right = right
            self.visited = visited

        def set_left(self, left):
            self.left = left

        def set_right(self, right):
            self.right = right

        def is_leaf(self):
            return (self.left == self.right == None)


    def __init__(self, freqs=None):
        self.freqs = freqs
        self.trees = list()
        self.code = dict()

        if self.freqs == None:
            raise Exception("Frequency table must be received upon initialization")

        # Adds trees from frequency document information in order
        for freq in self.freqs:
            temp_tree = self.tree(name=freq, weight=float(self.freqs[freq]))
            self.place_tree(temp_tree)

        self.build_tree()


    # Build the full tree
    def build_tree(self):
        while len(self.trees) != 1:
            tree1 = self.trees.pop(0)
            tree2 = self.trees.pop(0)

            new_weight = tree1.weight + tree2.weight
            self.place_tree(self.tree(weight=new_weight, left=tree1, right=tree2))
            

    # Places trees in order
    def place_tree(self, input_tree):
        position = 0
        while (position < len(self.trees)) and (input_tree.weight > self.trees[position].weight):
            position += 1
        self.trees.insert(position, input_tree)


    # Call another method to recursively generate and return the Huffman Codes
    def generate_code(self):
        root = self.trees[0]
        self.code = dict()
        self.traverse(root)
        return self.code


    # Recursively traverse and add the code at leaves
    def traverse(self, tree, code=''):
        if tree.is_leaf():
            self.code[tree.name] = code
            return
        if tree.left != None:
            self.traverse(tree.left, code+'0')
        if tree.right != None:
            self.traverse(tree.right, code+'1')


# Process an input file and add and return frequencies 
class ProcessFile(object):
    '''
    Fills frequency dictionary for Huffman Encoding
    '''
    def __init__(self, filename=None):
        self.frequencies = dict()
        self.total = 0
        if filename != None:
            self.process_file(filename)
            self.normalize_freqs()
        else:
            raise Exception("Filename cannot be 'None'")

    def process_file(self, filename):
        with open(filename, 'r') as input_file:
            for line in input_file:
                for char in line:
                    if char in self.frequencies:
                        self.frequencies[char] += 1
                    else:
                        self.frequencies[char] = 1
                    self.total += 1

    def normalize_freqs(self):
        for key in self.frequencies:
            self.frequencies[key] /= self.total


# Decode a given huffman code string and print to console
class Decoder(object):
    def __init__(self, encoded='', huffman_code=None):
        if encoded == '':
            raise Exception("Must provide encoded string to decode")
        if huffman_code == None:
            raise Exception("Huffman Code must be provided for decoding")
        new_code = dict()
        for key, value in huffman_code.items():
            new_code[value] = key
        self.decoded = ""
        test = ""
        for char in encoded:
            test += char
            if test in new_code:
                self.decoded += new_code[test]
                test = ""


# Encode a given string with a given huffman code
class Encoder(object):
    def __init__(self, original='', huffman_code={}, filename=None):
        if (original == '') and (filename == None):
            raise Exception("Must provide original string to encode")
        self.original = original
        self.encoded = ""
        self.huffman_code = huffman_code

        if filename != None:
            self.read_file(filename)
            return

        for char in original:
            self.encoded += str(self.huffman_code[char])
        print(len(self.encoded))

    def read_file(self, filename):
        with open(filename, 'r') as input_file:
            for line in input_file:
                for char in line:
                    self.encoded += self.huffman_code[char]



class HuffmanUnitTests(unittest.TestCase):
    pass


if __name__ == '__main__':
    length = len(argv)
    file_num = 1
    print(argv)
    while file_num < length:
        print()
        print('Processing file ' + str(argv[file_num]) + ' for file frequencies')
        freq_finder = ProcessFile(str(argv[file_num]))
        freqs = freq_finder.frequencies
        print()
        print('Generating Huffman Code with Huffman Tree')
        huff = Generate(freqs)
        hcode = huff.generate_code()
        print('Codes: \n', hcode)
        print()
        print('Encoding data from file ' + str(argv[file_num]))
        enc = Encoder(huffman_code=hcode, filename=str(argv[file_num]))
        e_code = str(enc.encoded)
        print(e_code)
        print()
        print('Decoding data')
        dec = Decoder(encoded=e_code, huffman_code=hcode)
        print(dec.decoded)
        file_num += 1
