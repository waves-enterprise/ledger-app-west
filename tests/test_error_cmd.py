import pytest

from app_client.exception import *


def test_bad_cla(cmd):
    sw, _ = cmd.transport.exchange(cla=0xa0,  # 0xa0 instead of 0x80
                                   ins=0x06,
                                   p1=0x00,
                                   p2=0x00,
                                   cdata=b"")

    assert isinstance(DeviceException(error_code=sw), ClaNotSupportedError)


def test_bad_ins(cmd):
    sw, _ = cmd.transport.exchange(cla=0x80,
                                   ins=0xff,  # bad INS
                                   p1=0x00,
                                   p2=0x00,
                                   cdata=b"")

    assert isinstance(DeviceException(error_code=sw), InsNotSupportedError)


def test_wrong_p1p2(cmd):
    sw, _ = cmd.transport.exchange(cla=0x80,
                                   ins=0x02,
                                   p1=0x01,  # 0x01 instead of 0x00
                                   p2=0x00,
                                   cdata=b"")

    assert isinstance(DeviceException(error_code=sw), WrongP1P2Error)


def test_wrong_data_length(cmd):
    # APDUs must be at least 5 bytes: CLA, INS, P1, P2, Lc.
    sw, _ = cmd.transport.exchange_raw("8002")

    assert isinstance(DeviceException(error_code=sw), WrongDataLengthError)
