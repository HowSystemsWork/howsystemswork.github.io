# pip install mmh3
import math
import mmh3
from typing import List


class BloomFilter:
    def __init__(self, n: int, p: int):
        self.p = p
        self.n = n
        self.array_size = self._determine_array_size(self.n, self.p)
        self.bit_array = [0] * self.array_size
        self.num_hash_funcs = self._determine_num_hash_funcs(self.array_size, self.n)
        self.size = 0

    def _determine_num_hash_funcs(self, m: int, n: int) -> int:
        k = (m / n) * math.log(2)
        return math.ceil(k)

    def _determine_array_size(self, n: int, p: int) -> int:
        m = -(n * math.log(p) / math.log(2) ** 2)
        return math.ceil(m)

    def _get_hashes(self, s: str) -> List[int]:
        hashes = []
        for hc in range(self.num_hash_funcs):
            hash = mmh3.hash(s, hc) % self.array_size
            hashes.append(hash)
        return hashes

    def add(self, word: str):
        hash_values = self._get_hashes(word)
        for hv in hash_values:
            self.bit_array[hv] = 1
        self.size += 1

    def contains(self, word: str) -> bool:
        hash_values = self._get_hashes(word)
        return all(self.bit_array[hash_val] == 1 for hash_val in hash_values)


if __name__ == "__main__":
    n = 1000
    p = 0.01  # 1%
    bloom_filter = BloomFilter(n, p)
    bloom_filter.add("foo")
    bloom_filter.add("bar")
    bloom_filter.add("dog")
    bloom_filter.add("apple")
    print(bloom_filter.contains("tiger"))
    print(bloom_filter.contains("dog"))
    print(bloom_filter.contains("sheep"))
    print(bloom_filter.contains("bar"))
