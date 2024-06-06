/*
 * @licstart The following is the entire license notice for the JavaScript code in this file.
 *
 * Copyright (C) 2024 Ari Archer
 *
 * This file is part of ari.lt.
 *
 * The JavaScript code in this file is free software: you can redistribute it
 * and/or modify it under the terms of the GNU Affero General Public License
 * (AGPL) as published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version. The code is distributed WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.
 *
 * As additional permission under AGPL version 3 section 7, you may distribute non-source
 * (e.g., minimized or compacted) forms of that code without the copy of the AGPL normally
 * required by section 4, provided you include this license notice and a URL through which
 * recipients can access the Corresponding Source.
 *
 * @licend The above is the entire license notice for the JavaScript code in this file.
 */

"use strict";

function rc4(b64_ct, b64_key) {
    let ciphertext = base64_to_array_buffer(b64_ct);
    let key = base64_to_array_buffer(b64_key);

    let S = Array(256);
    let j = 0,
        temp;
    for (let i = 0; i < 256; ++i) S[i] = i;
    for (let i = 0; i < 256; ++i) {
        j = (j + S[i] + key[i % key.length]) % 256;
        temp = S[i];
        S[i] = S[j];
        S[j] = temp;
    }

    let i = 0;
    j = 0;
    let decrypted = new Uint8Array(ciphertext.length);
    for (let y = 0; y < ciphertext.length; y++) {
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;
        temp = S[i];
        S[i] = S[j];
        S[j] = temp;
        decrypted[y] = ciphertext[y] ^ S[(S[i] + S[j]) % 256];
    }

    return new TextDecoder().decode(decrypted);
}

function base64_to_array_buffer(base64) {
    let bin = window.atob(base64);
    let bytes = new Uint8Array(bin.length);

    for (let idx = 0; idx < bin.length; ++idx) bytes[idx] = bin.charCodeAt(idx);

    return bytes;
}
