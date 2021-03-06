/*******************************************************************************
 *   Waves Enterprise Wallet App for Nano Ledger devices
 *   Copyright (c) 2022 Waves Enterprise
 *
 *   Based on Waves Platform Wallet App
 *        and Sample code provided (c) 2016 Ledger and
 *                                 (c) 2017-2018 Jake B. (Burstcoin app)
 *
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 ********************************************************************************/

#ifndef __PRINT_AMOUNT_H__
#define __PRINT_AMOUNT_H__

// borrowed from the Stellar wallet code and modified
bool print_amount(uint64_t amount, int decimals, unsigned char *out, uint8_t len) {
    uint64_t dVal = amount;
    int i, j;

    if (decimals == 0) decimals--;

    memset(ui_context.tmp, 0, len);
    for (i = 0; dVal > 0 || i < decimals + 2; i++) {
        if (dVal > 0) {
            ui_context.tmp[i] = (char) ((dVal % 10) + '0');
            dVal /= 10;
        } else {
            ui_context.tmp[i] = '0';
        }
        if (i == decimals - 1) {
            i += 1;
            ui_context.tmp[i] = '.';
        }
        if (i >= len) {
            return false;
        }
    }
    // reverse order
    for (i -= 1, j = 0; i >= 0 && j < len - 1; i--, j++) {
        out[j] = ui_context.tmp[i];
    }
    if (decimals > 0) {
        // strip trailing 0s
        for (j -= 1; j > 0; j--) {
            if (out[j] != '0') break;
        }
        j += 1;
        if (out[j - 1] == '.') j -= 1;
    }

    out[j] = '\0';
    return true;
}

#endif
