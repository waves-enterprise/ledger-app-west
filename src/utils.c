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

#include <stddef.h>

#include "utils.h"

void copy_in_reverse_order(unsigned char *to, const unsigned char *from, const unsigned int len) {
    for (unsigned int i = 0; i < len; i++) {
        to[i] = from[(len - 1) - i];
    }
}
