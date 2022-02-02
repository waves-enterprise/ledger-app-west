# Boilerplate commands

## Overview

| Command name | INS  | Description                                          |
| --- |------|------------------------------------------------------|
| `GET_VERSION` | 0x06 | Get application version as `MAJOR`, `MINOR`, `PATCH` |
| `GET_APP_NAME` | 0x08 | Get ASCII encoded application name                   |
| `GET_PUBLIC_KEY` | 0x04 | Get public key and address given BIP32 path          |
| `SIGN_TX` | 0x02 | Sign transaction given BIP32 path and tx bytes       |

## GET_VERSION

### Command

| CLA | INS  | P1 | P2 | Lc | CData |
| --- |------| --- | --- | --- | --- |
| 0x80 | 0x06 | 0x00 | 0x00 | 0x00 | - |

### Response

| Response length (bytes) | SW | RData |
| --- | --- | --- |
| 3 | 0x9000 | `MAJOR (1)`  `MINOR (1)`  `PATCH (1)` |

## GET_APP_NAME

### Command

| CLA | INS  | P1 | P2 | Lc | CData |
| --- |------| --- | --- | --- | --- |
| 0x80 | 0x08 | 0x00 | 0x00 | 0x00 | - |

### Response

| Response length (bytes) | SW | RData |
| --- | --- | --- |
| var | 0x9000 | `APPNAME (var)` |

## GET_PUBLIC_KEY

### Command

| CLA | INS  | P1 | P2                | Lc     | CData                                                             |
| --- |------| --- |-------------------|--------|-------------------------------------------------------------------|
| 0x80 | 0x04 | 0x00 (no display) <br> 0x01 (display) | Chain id (1 byte) | 1 + 4n | `len(bip32_path) (1)` <br> `bip32_path{1} (4)` <br>`...`<br>`bip32_path{n} (4)` |

### Response

| Response length (bytes) | SW     | RData               |
|-------------------------|--------|---------------------|
| 67                      | 0x9000 | `public_key (32)`  `address (35)` |

## SIGN_TX

### Command

| CLA | INS  | P1 | P2                | Lc                    | CData                                                                                                      |
| --- |------| --- |-------------------|-----------------------|------------------------------------------------------------------------------------------------------------|
| 0x80 | 0x02 | 0x00 (more) <br> 0x80 (last) | Chain id (1 byte) | 1 + 4n + tx_bytes_len | `len(bip32_path) (1)` <br> `bip32_path{1} (4)` <br>`...`<br>`bip32_path{n} (4)`<br>`tx_bytes(tx_bytes_len)` |

### Response

| Response length (bytes) | SW | RData             |
|-------------------------| --- |-------------------|
| 64                      | 0x9000 | `signature (64)`  |

## Status Words

| SW     | SW name | Description                              |
|--------| --- |------------------------------------------|
| 0x6982 | `SW_SECURITY_STATUS_NOT_SATISFIED` | Security status is not satisfied         |
| 0x6985 | `SW_DENY` | Conditions is not satisfied              |
| 0x6986 | `SW_DEVICE_IS_LOCKED` | Device is locked                         |
| 0x6A86 | `SW_WRONG_P1P2` | Either `P1` or `P2` is incorrect         |
| 0x6A87 | `SW_WRONG_DATA_LENGTH` | `Lc` or minimum APDU lenght is incorrect |
| 0x6D00 | `SW_INS_NOT_SUPPORTED` | No command exists with `INS`             |
| 0x6E00 | `SW_CLA_NOT_SUPPORTED` | Bad `CLA` used for this application      |
| 0xB000 | `SW_DEPRECATED_SIGN_PROTOCOL` | Deprecated sign protocol                 |
| 0x9000 | `OK` | Success                                  |
| 0x9100 | `SW_USER_CANCELLED` | Rejected by user                         |
