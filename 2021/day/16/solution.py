from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from functools import reduce


def read_bits(bit_iter, n):
    val = 0
    for _ in range(n):
        val <<= 1
        val += next(bit_iter)
    return val


class BitArray:
    """Left to right bit access"""
    def __init__(self, val: int, n: int = None):
        self.val = val
        if n is None:
            self.n = val.bit_length()
        else:
            self.n = n

        self.pos = 0

    @classmethod
    def from_bytes(cls, data: bytes) -> BitArray:
        val = int.from_bytes(data, byteorder="big")
        n = len(data)*8
        return cls(val, n)

    def __getitem__(self, key) -> BitArray:
        if isinstance(key, slice):
            if key.step:
                raise IndexError("Don't support stepping")
            start = key.start
            if start is None:
                start = 0
            elif start < 0:
                start = self.n + start
            stop = key.stop
            if stop is None:
                stop = self.n
            elif stop < 0:
                stop = self.n + stop
            elif stop > self.n:
                stop = self.n

            if stop <= start:
                return BitArray(0, 0)

            mask = (2**(stop-start))-1
            shift = self.n - start - (stop-start)
            return BitArray((self.val & (mask << shift)) >> shift, (stop-start))
        elif isinstance(key, int):
            if key < 0:
                key = self.n + key
            if key >= self.n:
                raise IndexError
            shift = self.n - key - 1
            return BitArray((self.val & (1 << shift)) >> shift, 1)
        else:
            raise TypeError

    def __iter__(self):
        return self

    def __next__(self):
        val = self[self.pos].val
        self.pos += 1
        return val

    def __str__(self):
        return f"{self.val:0{self.n}b}"

    def __repr__(self):
        return f"BitArray({self.val}, {self.n})"


@dataclass(frozen=True)
class Packet:
    version: int
    type_id: int
    sub_packets: list[Packet]
    literal: Optional[int]

    @classmethod
    def from_bits(cls, bits: BitArray):
        version = read_bits(bits, 3)
        type_id = read_bits(bits, 3)
        if type_id == 4:
            literal = 0
            cont = True
            while cont:
                final = next(bits)
                for _ in range(4):
                    literal <<= 1
                    literal += next(bits)
                cont = final == 1

            return cls(version, type_id, sub_packets=[], literal=literal)

        sub_packets = []
        length_type_id = next(bits)
        if length_type_id == 0:
            length = read_bits(bits, 15)
            initial_pos = bits.pos
            while bits.pos < initial_pos + length:
                sub_packets.append(cls.from_bits(bits))
        else:
            num_packets = read_bits(bits, 11)
            while len(sub_packets) < num_packets:
                sub_packets.append(cls.from_bits(bits))
        return cls(version, type_id, sub_packets=sub_packets, literal=None)

    def total_version_numbers(self):
        total = self.version
        for packet in self.sub_packets:
            total += packet.total_version_numbers()
        return total

    def value(self):
        if self.type_id == 0:   # sum
            return sum(packet.value() for packet in self.sub_packets)
        if self.type_id == 1:   # product
            return reduce(lambda a, b: a*b, (packet.value() for packet in self.sub_packets))
        if self.type_id == 2:   # min
            return min(packet.value() for packet in self.sub_packets)
        if self.type_id == 3:   # max
            return max(packet.value() for packet in self.sub_packets)
        if self.type_id == 4:   # literal
            return self.literal
        if self.type_id == 5:   # greater than
            return int(self.sub_packets[0].value() > self.sub_packets[1].value())
        if self.type_id == 6:   # less than
            return int(self.sub_packets[0].value() < self.sub_packets[1].value())
        if self.type_id == 7:   # equal to
            return int(self.sub_packets[0].value() == self.sub_packets[1].value())


with open("input") as fin:
    hex_string = next(fin).strip()
bits = BitArray.from_bytes(bytes.fromhex(hex_string))
packet = Packet.from_bits(bits)
print(packet)
print(packet.total_version_numbers())
print(packet.value())
