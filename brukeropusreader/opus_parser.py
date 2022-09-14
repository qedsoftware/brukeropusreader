from typing import List

from brukeropusreader.block_data import BlockMeta, UnknownBlockType
from brukeropusreader.constants import (
    HEADER_LEN,
    FIRST_CURSOR_POSITION,
    META_BLOCK_SIZE,
)
from brukeropusreader.opus_data import OpusData
from brukeropusreader.opus_reader import (
    read_data_type,
    read_channel_type,
    read_text_type,
    read_additional_type,
    read_chunk_size,
    read_offset,
)


def read_file(file_path: str) -> OpusData:
    with open(file_path, "rb") as opus_file:
        data = opus_file.read()
    meta_data = parse_meta(data)
    opus_data = parse_data(data, meta_data)
    return opus_data


def parse_meta(data: bytes) -> List[BlockMeta]:
    """Parse the header of the opus file.

    Returns a list of metadata (BlockMeta) for each block to be read,

    :parameter:
        data: bytes content of the opus file
    :returns:
        parse_meta: list of BlockMeta
    """
    header = data[:HEADER_LEN]
    spectra_meta = []
    cursor = FIRST_CURSOR_POSITION
    while True:
        if cursor + META_BLOCK_SIZE > HEADER_LEN:
            break

        data_type = read_data_type(header, cursor)
        channel_type = read_channel_type(header, cursor)
        text_type = read_text_type(header, cursor)
        additional_type = read_additional_type(header, cursor)
        chunk_size = read_chunk_size(header, cursor)
        offset = read_offset(header, cursor)

        if offset <= 0:
            break

        block_meta = BlockMeta(data_type, channel_type, text_type, additional_type, chunk_size, offset)

        spectra_meta.append(block_meta)

        next_offset = offset + 4 * chunk_size
        if next_offset >= len(data):
            break
        cursor += META_BLOCK_SIZE
    return spectra_meta


def parse_data(data: bytes, blocks_meta: List[BlockMeta]) -> OpusData:
    """parse the data of the opus file using the file header's informations
    parame"""
    opus_data = OpusData()
    for block_meta in blocks_meta:
        try:
            name, parser = block_meta.get_name_and_parser()
        except UnknownBlockType:
            continue
        parsed_data = parser(data, block_meta)
        # in some instances, multiple entries - in particular 'AB' are
        # present. they are added with a key ending by '_(1)', '_(2)', etc...
        if name in opus_data.keys():
            i = 1
            while name + '_(' + str(i) + ')' in opus_data.keys():
                i += 1
            name = name + '_(' + str(i) + ')'
        opus_data[name] = parsed_data
    return opus_data
