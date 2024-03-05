import heapq
import collections

mp = {}
class Node:
    def __init__(self,  weight,data):
        self.data = data
        self.weight = weight
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.weight > other.weight

def ltrim(s):
    return s.lstrip()

def rtrim(s):
    return s.rstrip()

def trim(s):
    return s.strip()

def find_freq(data):
    freq = collections.defaultdict(int)
    for ch in data:
        freq[ch] += 1
    return freq

def build_pq(freq):
    pq = []
    for char, weight in freq.items():
        heapq.heappush(pq, (weight + ord(char)%7, Node(weight, char)))
    return pq

def build_tree(pq):
    while len(pq) > 1:
        left = heapq.heappop(pq)[1]
        right = heapq.heappop(pq)[1]
        weight = left.weight + right.weight
        temp = Node(weight, '.')
        temp.left = left
        temp.right = right
        heapq.heappush(pq, (weight, temp))
    return pq[0][1]

def get_codes(root, path, mp):
    if root is not None:
        if root.data != '.':
            mp[root.data] = ''.join(path)
        path.append('0')
        get_codes(root.left, path, mp)
        path.pop()
        path.append('1')
        get_codes(root.right, path, mp)
        path.pop()

def apply_changes(mp, data):
    encoded_str = ''
    for char in data:
        encoded_str += mp[char]
    return encoded_str

def write_to_file(data):
    try:
        with open('Encoded_git.txt', 'w') as outfile:
            outfile.write(data)
    except Exception as e:
        pass

def encode(data):
    freq = find_freq(data)
    pq = build_pq(freq)
    tree_root = build_tree(pq)
    global mp
    path = []
    get_codes(tree_root, path, mp)
    encoded_str = apply_changes(mp, data)
    write_to_file(encoded_str)

def main():
    data = "000000_____3333CCCCDDDDNNNN44477UU5AFHKRTVWYahisw{}"
    data = trim(data)
    encode(data)
    print(mp)
    l = 0
    r = 1
    enc = '110111011011111110101110001110111110110000100011011110111011110011010110001111011011101000101000110011101000000101111101000000000101101000111001011000100010011010010110000101000010110100110111111101101011011111101110001000111001011011001'
    dec = ''
    imp = dict()
    for i in mp:
        imp[mp[i]] = i
    while r<=len(enc):
        if enc[l:r] in imp:
            dec+=imp[enc[l:r]]
            l=r
        r+=1
    print(dec)

if __name__ == '__main__':
    main()
