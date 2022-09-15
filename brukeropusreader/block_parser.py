from brukeropusreader.constants import (
    UNSIGNED_SHORT,
    PARAM_TYPES,
    INT,
    DOUBLE,
    NULL_BYTE,
    ENCODING_LATIN,
    ENCODING_UTF,
    NULL_STR,
)
from brukeropusreader.opus_reader import read_chunk
from struct import unpack, error
import numpy as np


def parse_param(data: bytes, block_meta):
    """parse data blocks of parameters

    BLOCK_23, BLOCK_27"""
    cursor = 0
    chunk = read_chunk(data, block_meta)
    params = {}
    while True:
        param_name = chunk[cursor : cursor + 3].decode(ENCODING_UTF)
        if param_name == "END":
            break
        type_index = unpack(UNSIGNED_SHORT, chunk[cursor + 4 : cursor + 6])[0]
        param_type = PARAM_TYPES[type_index]
        param_size = unpack(UNSIGNED_SHORT, chunk[cursor + 6 : cursor + 8])[0]
        param_bytes = chunk[cursor + 8 : cursor + 8 + 2 * param_size]

        if param_type == "int":
            try:
                param_val = unpack(INT, param_bytes)[0]
            except error:
                return params
        elif param_type == "float":
            param_val = unpack(DOUBLE, param_bytes)[0]
        elif param_type == "str":
            p_end = param_bytes.find(NULL_BYTE)
            param_val = param_bytes[:p_end].decode(ENCODING_LATIN)
        else:
            param_val = param_bytes
        params[param_name] = param_val
        cursor = cursor + 8 + 2 * param_size
    return params


def parse_text(data: bytes, block_meta):
    chunk = read_chunk(data, block_meta)
    return chunk.decode(ENCODING_LATIN).strip(NULL_STR)


def parse_series(data: bytes, block_meta):
    chunk = read_chunk(data, block_meta)
    fmt = f"<{block_meta.chunk_size}f"
    values = unpack(fmt, chunk)
    return np.array(values)
