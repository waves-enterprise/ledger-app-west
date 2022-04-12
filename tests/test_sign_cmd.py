import struct
from time import time

import axolotl_curve25519 as curve
import base58


def transfer_bytes(
        public_key,
        address,
        amount,
        asset='',
        attachment='',
        feeAsset='',
        txFee=100000,
        timestamp=0,
):
    if timestamp == 0:
        timestamp = int(time() * 1000)

    # tx type
    cdata = b'\4'

    # version
    cdata += b'\2'

    # public key
    cdata += public_key

    # asset assetId bytes, \0
    cdata += (b'\1' + base58.b58decode(asset) if asset else b'\0')

    # fee asset bytes, \0
    cdata += (b'\1' + base58.b58decode(feeAsset) if feeAsset else b'\0')

    # timestamp
    cdata += struct.pack(">Q", timestamp)

    # amount
    cdata += struct.pack(">Q", amount)

    # txFee
    cdata += struct.pack(">Q", txFee)

    # recipient address
    cdata += base58.b58decode(address)

    # attachment len
    cdata += struct.pack(">H", len(attachment))

    # attachment
    cdata += attachment.encode('latin-1')

    return cdata


def test_sign_tx(cmd, button, model):
    bip32_path: str = "44'/5741565'/0'/0'/1'"

    public_key, address = cmd.get_public_key(
        bip32_path=bip32_path,
        network_byte='V',
        display=False,
        model=model
    )  # type: bytes, bytes

    tx_bytes = transfer_bytes(public_key=public_key, address=address, amount=100000000)

    binary_data: bytes = b''

    # tx amount asset decimals
    binary_data += b'\x08'

    # fee amount asset decimals
    binary_data += b'\x08'

    binary_data += b'\4\2'
    binary_data += struct.pack(">I", len(tx_bytes))
    binary_data += tx_bytes
    binary_data += tx_bytes

    sw, signature = cmd.sign_tx(
        bip32_path=bip32_path,
        network_byte='V',
        tx_bytes=binary_data,
        button=button,
        model=model
    )

    # valid
    assert curve.verifySignature(public_key, tx_bytes, signature) == 0
