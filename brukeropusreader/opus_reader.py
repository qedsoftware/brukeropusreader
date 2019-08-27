from struct import unpack

from brukeropusreader.constants import UNSIGNED_INT, UNSIGNED_CHAR


def read_data_type(header: bytes, cursor: int) -> int:
    p1 = cursor
    p2 = cursor + 1
    return unpack(UNSIGNED_CHAR, header[p1:p2])[0]


def read_channel_type(header: bytes, cursor: int) -> int:
    p1 = cursor + 1
    p2 = cursor + 2
    return unpack(UNSIGNED_CHAR, header[p1:p2])[0]


def read_text_type(header: bytes, cursor: int) -> int:
    p1 = cursor + 2
    p2 = cursor + 3
    return unpack(UNSIGNED_CHAR, header[p1:p2])[0]


def read_chunk_size(header: bytes, cursor: int) -> int:
    p1 = cursor + 4
    p2 = cursor + 8
    return unpack(UNSIGNED_INT, header[p1:p2])[0]


def read_offset(header: bytes, cursor: int) -> int:
    p1 = cursor + 8
    p2 = cursor + 12
    return unpack(UNSIGNED_INT, header[p1:p2])[0]


def read_chunk(data: bytes, block_meta):
    p1 = block_meta.offset
    p2 = p1 + 4 * block_meta.chunk_size
    return data[p1:p2]
