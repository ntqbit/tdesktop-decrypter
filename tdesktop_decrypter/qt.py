from io import BytesIO


def _read_bytes(data: BytesIO, size: int) -> bytes:
    b = data.read(size)
    if len(b) != size:
        raise StopIteration()

    return b


def read_qt_integer(data: BytesIO, size: int, signed: bool) -> int:
    return int.from_bytes(_read_bytes(data, size), "big", signed=signed)


def read_qt_int32(data: BytesIO) -> int:
    return read_qt_integer(data, 4, True)


def read_qt_uint32(data: BytesIO) -> int:
    return read_qt_integer(data, 4, False)


def read_qt_int64(data: BytesIO) -> int:
    return read_qt_integer(data, 8, True)


def read_qt_uint64(data: BytesIO) -> int:
    return read_qt_integer(data, 8, False)


def read_qt_byte_array(data: BytesIO) -> bytes:
    length = read_qt_int32(data)
    if length <= 0:
        return b""

    return _read_bytes(data, length)


def read_qt_utf8(data: BytesIO) -> str:
    return read_qt_byte_array(data).decode("utf16")
