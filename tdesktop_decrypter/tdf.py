import hashlib

TDF_MAGIC = b"TDF$"


class TdfParserError(Exception):
    pass


class WrongMagicTdfParserError(Exception):
    pass


class WrongHashsumTdfParserError(Exception):
    pass


class RawTdfFile:
    def __init__(self):
        self.version = None
        self.encrypted_data = None
        self.hashsum = None


def parse_raw_tdf(data: bytes) -> RawTdfFile:
    if data[:4] != TDF_MAGIC:
        raise WrongMagicTdfParserError("Wrong magic. Not a TDF file?")

    tdf = RawTdfFile()

    tdf.version = int.from_bytes(data[4:8], "little")
    tdf.encrypted_data = data[8:-16]
    tdf.hashsum = data[-16:]

    actual_md5 = hashlib.md5(
        tdf.encrypted_data
        + len(tdf.encrypted_data).to_bytes(4, "little")
        + tdf.version.to_bytes(4, "little")
        + TDF_MAGIC
    ).digest()

    if actual_md5 != tdf.hashsum:
        raise WrongHashsumTdfParserError("Wrong hashsum. Corrupted file?")

    return tdf
