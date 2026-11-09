from pathlib import Path
import struct
import sys


def read_num(fmt, data, pos):
    return struct.unpack_from(fmt, data, pos)[0], pos + struct.calcsize(fmt)


def read_lp(fmt, data, pos):
    size, pos = read_num(fmt, data, pos)
    return data[pos:pos + size], pos + size


data = Path(sys.argv[1]).read_bytes()
pos = None
for header_pos in range(8, 0xD0, 8):
    candidate = struct.unpack_from("<Q", data, header_pos)[0]
    candidate_size = struct.unpack_from("<Q", data, header_pos + 8)[0]
    if candidate and candidate_size and candidate + candidate_size == len(data):
        pos = candidate
        print(f"index_offset={candidate:#x} index_size={candidate_size:#x}")
        break
if pos is None:
    raise RuntimeError("index offset not found")
count, pos = read_num("<I", data, pos)
print(f"count={count}")
for index in range(count):
    logical, pos = read_lp("<H", data, pos)
    dtype = data[pos]
    pos += 1
    language, pos = read_num("<H", data, pos)
    flags, pos = read_num("<H", data, pos)
    offset, pos = read_num("<Q", data, pos)
    expected, pos = read_num("<I", data, pos)
    storage = data[pos]
    pos += 1
    stored, pos = read_lp("<H", data, pos)
    description, pos = read_lp("<H", data, pos)
    if index + 1 < count:
        reserved, pos = read_num("<I", data, pos)
    print(f"{index}\t{dtype}\t{language}\t{expected}\t{offset:#x}\t{logical.decode('utf-8', 'replace')}")
