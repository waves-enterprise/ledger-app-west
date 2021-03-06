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

#ifndef __UI_H__
#define __UI_H__

#include "os.h"
#include "cx.h"
#include <stdbool.h>
#include "../main.h"
#include "../crypto/ledger_crypto.h"
#include "os_io_seproxyhal.h"

#ifdef HAVE_BOLOS_UX
extern ux_state_t G_ux;
extern bolos_ux_params_t G_ux_params;
#endif

enum UI_STATE { UI_IDLE, UI_VERIFY };
extern enum UI_STATE ui_state;

static const unsigned char WEST_CONST[] = "WEST";

void menu_sign_init();
void ui_idle();

extern int ux_step;
extern int ux_step_count;

void make_allowed_ui_steps(bool is_last);
void show_sign_ui();
void menu_address_init();
void show_processing();

void try_to_fill_buffer(uint8_t chunk_data_start_index, uint8_t chunk_data_size);

#define MAX_CHARS_PER_LINE 49
#define DEFAULT_FONT       BAGL_FONT_OPEN_SANS_LIGHT_16px | BAGL_FONT_ALIGNMENT_LEFT
#define TEXT_HEIGHT        15
#define TEXT_SPACE         4

#define COLOR_WAVES 0x0055FF
#define COLOR_WHITE 0xF9F9F9
#endif
