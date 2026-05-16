import heapq
import pickle
from bitarray import bitarray
from collections import defaultdict, Counter

class HuffmanNode:

    def __init__(self, char=None, freq=None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq
    
    def build_frequency_fn(self, data):
        return Counter(data)
    
    def build_huffman_tree(self, freqTable):
        priority_queue = [HuffmanNode(char, freq) for char, freq in freqTable.items()]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(priority_queue, merged)
        
        return priority_queue[0]
    
    def generate_huffman_codes(self, tree):

        huffman_codes = {}

        def traverse(node, current_code = ""):
            if node:
                if node.char is not None:
                    huffman_codes[node.char] = current_code
                
                traverse(node.left, current_code + "0")
                traverse(node.right, current_code + "1")
        
        traverse(tree)
        return huffman_codes
    
    def compress_fn(self, input_path, output_path):
        
        with open(input_path, 'rb') as f:
            data = f.read()
        
        freqTable = self.build_frequency_fn(data)
        huffman_tree = self.build_huffman_tree(freqTable)
        huffman_codes = self.generate_huffman_codes(huffman_tree)
        
        encoded_data = bitarray()
        encoded_data = "".join(huffman_codes[byte] for byte in data)

        with open(output_path, 'wb') as f:
            pickle.dump((encoded_data, huffman_tree), f)

        return encoded_data, huffman_tree
    
    def decompress_fn(self, encoded_data, huffman_tree):
        if not encoded_data or not huffman_tree:
            return ""
        
        decoded_data = []
        current_node = huffman_tree

        for bit in encoded_data:
            current_node = current_node.left if bit == "0" else current_node.right

            if current_node.char is not None:
                decoded_data.append(current_node.char)
                current_node = huffman_tree
        
        return "".join(decoded_data)
    


if __name__ == "__main__":
    A = HuffmanNode()

    encoded_data, huffman_tree = A.compress_fn("large_text_file.txt", "a.huff")
    