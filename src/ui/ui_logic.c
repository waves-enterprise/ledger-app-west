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

#include "ui_logic.h"
#include "main.h"
#include "ui.h"

// UI
unsigned int io_seproxyhal_touch_address_ok() {
    uint32_t tx = set_result_get_address();
    unsigned short sw = SW_OK;

    G_io_apdu_buffer[tx++] = sw >> 8;
    G_io_apdu_buffer[tx++] = sw;

    // Send back the response, do not restart the event loop
    io_exchange(CHANNEL_APDU | IO_RETURN_AFTER_TX, tx);

    init_context();

    // Display back the original UX
    ui_idle();
    return 0;  // do not redraw the widget
}

unsigned int io_seproxyhal_cancel() {
    uint32_t tx = 0;

    unsigned short sw = SW_USER_CANCELLED;

    G_io_apdu_buffer[tx++] = sw >> 8;
    G_io_apdu_buffer[tx++] = sw;

    // Send back the response, do not restart the event loop
    io_exchange(CHANNEL_APDU | IO_RETURN_AFTER_TX, 2);

    init_context();

    // Display back the original UX
    ui_idle();
    return 0;  // do not redraw the widget
}

unsigned int io_seproxyhal_touch_sign_approve() {
    // first 64 byte - signature
    unsigned short sw = SW_CONDITIONS_NOT_SATISFIED;
    uint32_t tx = 0;

    BEGIN_TRY {
        TRY {
            tx = set_result_sign();
            sw = SW_OK;
        }
        CATCH_OTHER(e) {
            sw = e;
        }
        FINALLY {
        }
    }
    END_TRY;

    G_io_apdu_buffer[tx++] = sw >> 8;
    G_io_apdu_buffer[tx++] = sw;

    io_exchange(CHANNEL_APDU | IO_RETURN_AFTER_TX, tx);

    init_context();

    ui_idle();

    return 0;  // do not redraw the widget
}

unsigned int io_seproxyhal_touch_exit() {
    // Go back to the dashboard
    os_sched_exit(0);
    return 0;  // do not redraw the widget
}
