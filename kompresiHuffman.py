# Impor pustaka
import heapq
from collections import defaultdict
import sys

# Tentukan kelas Node
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Bangun pohon Huffman
def build_huffman_tree(frequencies):
    heap = [[weight, Node(char, weight)] for char, weight in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        merged_freq = lo[0] + hi[0]
        merged_node = Node(None, merged_freq)
        merged_node.left = lo[1]
        merged_node.right = hi[1]
        heapq.heappush(heap, [merged_freq, merged_node])

    return heap[0][1]

# Kompresi Huffman
def huffman_compress(text):
    try:
        text.encode('ascii')
    except UnicodeEncodeError:
        print("Teks mengandung karakter non-ASCII. Program ini hanya mendukung teks ASCII.")
        sys.exit()

    frequencies = defaultdict(int)
    for char in text:
        frequencies[char] += 1

    huffman_tree = build_huffman_tree(frequencies)

    huffman_codes = {}
    def generate_codes(node, code):
        if node.char:
            huffman_codes[node.char] = code
        else:
            generate_codes(node.left, code + '0')
            generate_codes(node.right, code + '1')
    generate_codes(huffman_tree, '')

    compressed_text = ''.join(huffman_codes[char] for char in text)

    return compressed_text, huffman_codes

if __name__ == "__main__":
    # Dapatkan teks input
    input_text = input("Masukkan teks: ")

    if not input_text:
        print("Teks kosong. Masukkan teks yang valid.")
        sys.exit()

    try:
        compressed_result, huffman_codes = huffman_compress(input_text)
    except Exception as e:
        print(f"Terjadi kesalahan saat mengompres teks: {e}")
        sys.exit()

    # Tampilkan teks asli, teks terkompresi, dan tabel kode Huffman
    print("Teks Asli:", input_text)
    print("Teks Terkompresi:", compressed_result)
    print("Tabel Kode Huffman:", huffman_codes)

    # Hitung ukuran teks asli dan teks terkompresi dalam bytes
    original_size_bytes = sys.getsizeof(input_text)
    compressed_size_bytes = sys.getsizeof(compressed_result)

    # Tampilkan ukuran teks asli dan teks terkompresi dalam bytes
    print("Ukuran Teks Asli:", original_size_bytes, "bytes")
    print("Ukuran Teks Terkompresi:", compressed_size_bytes, "bytes")