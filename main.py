#!/usr/bin/env python3
"""Entry-point for THE WORLD TODAY — Monday 23 November 2026 (31 stories).

Validates the bundled entry.png and writes it to
os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png").
Stdlib only (no PIL). The PNG is parsed manually with struct: signature,
IHDR (must be 1024x1024, 8-bit, colour type 2 or 6), per-chunk CRC walk,
non-empty IDAT payload, IEND as the final chunk with no trailing data.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "79467c8f59761a72112532669a0bb8bf5c379e4d323df76ad39b8b0b7196ac14"
EXPECTED_SIZE = 154042
MIN_SIZE = 10000
MAX_SIZE = 1024 * 1024
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def fail(msg):
    print("ERROR: %s" % msg, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    if os.path.isfile(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file: %s" % out_dir)
    if os.path.commonpath([out_dir_abs, here]) == here:
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repo: %s" % out_dir)
    if not os.path.isfile(src):
        return fail("entry.png not found next to main.py: %s" % src)
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source entry.png")

    data = open(src, "rb").read()
    if len(data) < MIN_SIZE:
        return fail("entry.png too small: %d bytes" % len(data))
    if len(data) > MAX_SIZE:
        return fail("entry.png too large: %d bytes" % len(data))
    if len(data) != EXPECTED_SIZE:
        return fail("entry.png size mismatch: got %d, expected %d"
                    % (len(data), EXPECTED_SIZE))
    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SHA256:
        return fail("entry.png sha256 mismatch: got %s" % sha)

    # --- manual PNG validation (stdlib only, no PIL) ---
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("bad PNG signature")
    pos = 8
    first = True
    idat_total = 0
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            return fail("truncated chunk header at offset %d" % pos)
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + length > len(data):
            return fail("truncated chunk %r at offset %d" % (ctype, pos))
        chunk_data = data[pos + 8:pos + 8 + length]
        # CRC covers chunk type + data (not the length field), per PNG spec.
        crc_stored = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        crc_calc = zlib.crc32(ctype)
        crc_calc = zlib.crc32(chunk_data, crc_calc) & 0xFFFFFFFF
        if crc_calc != crc_stored:
            return fail("CRC mismatch in chunk %r" % ctype)
        if first:
            if ctype != b"IHDR":
                return fail("first chunk must be IHDR, got %r" % ctype)
            if length != 13:
                return fail("IHDR must be 13 bytes, got %d" % length)
            w, h, depth, ctype_n, comp, filt, inter = struct.unpack(
                ">IIBBBBB", chunk_data)
            if (w, h) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
                return fail("IHDR size %dx%d, expected %dx%d"
                            % (w, h, EXPECTED_WIDTH, EXPECTED_HEIGHT))
            if depth != 8:
                return fail("bit depth %d, expected 8" % depth)
            if ctype_n not in (2, 6):
                return fail("colour type %d, expected 2 or 6" % ctype_n)
            if comp != 0 or filt != 0 or inter != 0:
                return fail("compression/filter/interlace must be 0")
            first = False
        if ctype == b"IDAT":
            if length == 0:
                return fail("empty IDAT chunk")
            idat_total += length
        if ctype == b"IEND":
            if length != 0:
                return fail("IEND must be 0 bytes")
            if pos + 12 + length != len(data):
                return fail("trailing data after IEND")
            seen_iend = True
            break
        pos += 12 + length
    if first:
        return fail("no IHDR chunk found")
    if not seen_iend:
        return fail("no IEND chunk found")
    if idat_total < 1000:
        return fail("IDAT payload too small: %d bytes" % idat_total)

    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    # re-read the output and confirm it is byte-identical
    back = open(dst, "rb").read()
    if back != data:
        return fail("output differs from source after write")
    print("OK: entry.png %dx%d, %d bytes, sha256 %s"
          % (EXPECTED_WIDTH, EXPECTED_HEIGHT, len(data), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main())
