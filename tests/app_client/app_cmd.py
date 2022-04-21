import struct
from typing import Tuple

from app_client.app_cmd_builder import AppCommandBuilder, InsType
from app_client.button import Button
from app_client.exception import DeviceException
from ledgercomm import Transport


class AppCommand:
    def __init__(self,
                 transport: Transport,
                 debug: bool = False) -> None:
        self.transport = transport
        self.builder = AppCommandBuilder(debug=debug)
        self.debug = debug

    def get_version(self) -> Tuple[int, int, int]:
        sw, response = self.transport.exchange_raw(
            self.builder.get_version()
        )  # type: int, bytes

        if sw != 0x9000:
            raise DeviceException(error_code=sw, ins=InsType.INS_GET_VERSION)

        # response = MAJOR (1) || MINOR (1) || PATCH (1)
        assert len(response) == 3

        major, minor, patch = struct.unpack(
            "BBB",
            response
        )  # type: int, int, int

        return major, minor, patch

    def get_app_name(self) -> str:
        sw, response = self.transport.exchange_raw(
            self.builder.get_app_name()
        )  # type: int, bytes

        if sw != 0x9000:
            raise DeviceException(error_code=sw, ins=InsType.INS_GET_APP_NAME)

        return response.decode("ascii")

    def get_public_key(self, bip32_path: str, model: str, button: Button = None, network_byte: str = b'V', display: bool = False) -> Tuple[
        bytes, bytes]:
        self.transport.send_raw(
            self.builder.get_public_key(bip32_path=bip32_path, network_byte=network_byte, display=display)
        )  # type: int, bytes

        if button:
            # Verify address
            button.right_click()

            # Address, 1/1 for Nano X, 1/2 for Nano S
            button.right_click()
            if model == "nanos":
                # 2/2 for Nano S
                button.right_click()

            # Approve
            button.both_click()

        sw, response = self.transport.recv()  # type: int, bytes

        if sw != 0x9000:
            raise DeviceException(error_code=sw, ins=InsType.INS_GET_PUBLIC_KEY)

        pub_key: bytes = response[0:32]
        address: bytes = response[32:67]

        return pub_key, address

    def sign_tx(self, bip32_path: str, network_byte: str, tx_bytes: bytes, button: Button, model: str) -> Tuple[int, bytes]:
        sw: int = 0
        response: bytes = b""

        for is_last, chunk in self.builder.sign_tx(bip32_path=bip32_path, network_byte=network_byte, tx_bytes=tx_bytes):
            self.transport.send_raw(chunk)

            if is_last:
                # Review Transaction
                button.right_click()

                # Amount
                button.right_click()

                # Asset
                button.right_click()

                # To address, 1/1 for Nano X, 1/2 for Nano S
                button.right_click()
                if model == "nanos":
                    # 2/2 for Nano S
                    button.right_click()

                # Fee
                button.right_click()

                # Fee asset
                button.right_click()

                # From address, 1/1 for Nano X, 1/2 for Nano S
                button.right_click()
                if model == "nanos":
                    # 2/2 for Nano S
                    button.right_click()

                # From address, 1/1 for Nano X, 1/3 for Nano S
                button.right_click()
                if model == "nanos":
                    # 2/3 and 3/3 for Nano S
                    button.right_click()
                    button.right_click()

                # Approve
                button.both_click()

            sw, response = self.transport.recv()  # type: int, bytes

            if sw != 0x9000:
                raise DeviceException(error_code=sw, ins=InsType.INS_SIGN_TX)

        assert len(response) == 64

        return sw, response
