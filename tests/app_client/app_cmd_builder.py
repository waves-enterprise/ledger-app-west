import enum
import logging
import struct
from typing import Tuple, Union, Iterator, cast

from app_client.utils import expand_path, path_to_bytes

MAX_APDU_LEN: int = 128


def chunkify(data: bytes, chunk_len: int) -> Iterator[Tuple[bool, bytes]]:
    size: int = len(data)

    if size <= chunk_len:
        yield True, data
        return

    chunk: int = size // chunk_len
    remaining: int = size % chunk_len
    offset: int = 0

    for i in range(chunk):
        yield False, data[offset:offset + chunk_len]
        offset += chunk_len

    if remaining:
        yield True, data[offset:]


class InsType(enum.IntEnum):
    INS_GET_VERSION = 0x06
    INS_GET_APP_NAME = 0x08
    INS_GET_PUBLIC_KEY = 0x04
    INS_SIGN_TX = 0x02


class AppCommandBuilder:
    """APDU command builder for the Boilerplate application.

    Parameters
    ----------
    debug: bool
        Whether you want to see logging or not.

    Attributes
    ----------
    debug: bool
        Whether you want to see logging or not.

    """
    CLA: int = 0x80

    def __init__(self, debug: bool = False):
        """Init constructor."""
        self.debug = debug

    def serialize(self,
                  cla: int,
                  ins: Union[int, enum.IntEnum],
                  p1: int = 0,
                  p2: int = 0,
                  cdata: bytes = b"") -> bytes:
        """Serialize the whole APDU command (header + data).

        Parameters
        ----------
        cla : int
            Instruction class: CLA (1 byte)
        ins : Union[int, IntEnum]
            Instruction code: INS (1 byte)
        p1 : int
            Instruction parameter 1: P1 (1 byte).
        p2 : int
            Instruction parameter 2: P2 (1 byte).
        cdata : bytes
            Bytes of command data.

        Returns
        -------
        bytes
            Bytes of a complete APDU command.

        """
        ins = cast(int, ins.value) if isinstance(ins, enum.IntEnum) else cast(int, ins)

        header: bytes = struct.pack("BBBBB",
                                    cla,
                                    ins,
                                    p1,
                                    p2,
                                    len(cdata))  # add Lc to APDU header

        if self.debug:
            logging.info("header: %s", header.hex())
            logging.info("cdata:  %s", cdata.hex())

        return header + cdata

    def get_version(self) -> bytes:
        """Command builder for GET_VERSION.

        Returns
        -------
        bytes
            APDU command for GET_VERSION.

        """
        return self.serialize(cla=self.CLA,
                              ins=InsType.INS_GET_VERSION,
                              p1=0x00,
                              p2=0x00,
                              cdata=b"")

    def get_app_name(self) -> bytes:
        """Command builder for GET_APP_NAME.

        Returns
        -------
        bytes
            APDU command for GET_APP_NAME.

        """
        return self.serialize(cla=self.CLA,
                              ins=InsType.INS_GET_APP_NAME,
                              p1=0x00,
                              p2=0x00,
                              cdata=b"")

    def get_public_key(self, bip32_path: str, network_byte: str, display: bool = False) -> bytes:
        """Command builder for GET_PUBLIC_KEY.

        Parameters
        ----------
        bip32_path: str
            String representation of bip32 path.
        network_byte: str
            Network byte needed to calculate wallet address.
        display : bool
            Whether you want to display the address on the device.

        Returns
        -------
        bytes
            APDU command for GET_PUBLIC_KEY.

        """

        cdata: bytes = path_to_bytes(expand_path(bip32_path))

        return self.serialize(cla=self.CLA,
                              ins=InsType.INS_GET_PUBLIC_KEY,
                              p1=(0x00 if not display else 0x80),
                              p2=ord(network_byte),
                              cdata=cdata)

    def sign_tx(self, bip32_path: str, network_byte: str, tx_bytes: bytes) -> Iterator[Tuple[bool, bytes]]:
        """Command builder for INS_SIGN_TX.

        Parameters
        ----------
        bip32_path : str
            String representation of bip32 path.
        network_byte : str
            Network byte needed to calculate wallet address.
        tx_bytes : bytes
            Transaction bytes to be signed.

        Yields
        -------
        bytes
            APDU command chunk for INS_SIGN_TX.

        """

        cdata: bytes = path_to_bytes(expand_path(bip32_path)) + tx_bytes

        for (is_last, chunk) in chunkify(cdata, MAX_APDU_LEN):
            if is_last:
                yield True, self.serialize(cla=self.CLA,
                                           ins=InsType.INS_SIGN_TX,
                                           p1=0x80,
                                           p2=ord(network_byte),
                                           cdata=chunk)
                return
            else:
                yield False, self.serialize(cla=self.CLA,
                                            ins=InsType.INS_SIGN_TX,
                                            p1=0x00,
                                            p2=ord(network_byte),
                                            cdata=chunk)
