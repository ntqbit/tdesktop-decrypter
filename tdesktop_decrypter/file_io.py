import os

from typing import Tuple
from io import BytesIO

from tdesktop_decrypter.crypto import decrypt_local
from tdesktop_decrypter.tdf import RawTdfFile, parse_raw_tdf
from tdesktop_decrypter.qt import read_qt_byte_array


class TdataFileIo:
    def read_file(self, path: str) -> bytes:
        '''
        Reads a file from filesystem or some other data provider.
        Path is a relative path to the file without leading slash.
        For example, path = 'settings'
        Returns the file's data if the file exists, otherwise raises FileNotFoundError.
        '''
        raise NotImplementedError()
    
    def read_tdf_file(self, path: str) -> RawTdfFile:
        candidates = [path + "s", path]

        for candidate in candidates:
            try:
                return parse_raw_tdf(self.read_file(candidate))
            except FileNotFoundError:
                pass

        raise FileNotFoundError()

    def read_encrypted_file(self, path: str, local_key: bytes) -> Tuple[int, bytes]:
        tdf_file = self.read_tdf_file(path)
        encrpyted_data = read_qt_byte_array(BytesIO(tdf_file.encrypted_data))
        return tdf_file.version, decrypt_local(encrpyted_data, local_key)


class TdataFileSystem(TdataFileIo):
    def __init__(self, base_path: str):
        super().__init__()
        
        self._base_path = base_path
    
    def read_file(self, path: str) -> bytes:
        with open(os.path.join(self._base_path, path), 'rb') as f:
            return f.read()