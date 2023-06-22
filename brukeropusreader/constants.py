HEADER_LEN = 504
UNSIGNED_INT = "<I"
UNSIGNED_CHAR = "<B"
UNSIGNED_SHORT = "<H"
INT = "<i"
DOUBLE = "<d"
NULL_BYTE = b"\x00"
NULL_STR = "\x00"
FIRST_CURSOR_POSITION = 24
META_BLOCK_SIZE = 12
ENCODING_LATIN = "latin-1"
ENCODING_UTF = "utf-8"
PARAM_TYPES = {0: "int", 1: "float", 2: "str", 3: "str", 4: "str"}
RAW0_TYPES = {
    "names": ["XA", "ADC", "OVF", "FWD", "DQEna", "CPLsw", "XAOVF", "XAValid", "XA External Valid"],
    "formats": ["i2"] * 2 + ["?"] * 7,
}
# XXX Only confirmed masks so far are: FWD, CPLsw, XAValid
RAW0_FLAGS = [0x20, 0x10, 0x08, 0x04, 0x02, 0x01, 0x40]
