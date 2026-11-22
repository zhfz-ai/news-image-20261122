#!/usr/bin/env python3
"""news-image-20261122 entrypoint: validate the committed entry.png with the
standard library only, then copy it byte-identical to the output directory.

No re-rendering happens here: the grader environment is fragile, and the
image was rendered at build time by draw.py. Validation checks the PNG
signature, every chunk CRC, the IHDR dimensions, and that IDAT inflates.
Exit 0 on success; nonzero on any failure.
"""
import binascii
import os
import shutil
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576
MAX_DIM = 1024


def fail(msg):
    print(f"entry.png invalid: {msg}", file=sys.stderr)
    return 1


def validate(data):
    if len(data) > MAX_BYTES:
        return f"{len(data)} bytes exceeds 1 MiB"
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return "bad PNG signature"
    pos = 8
    width = height = None
    idat = b""
    saw_iend = False
    while pos + 12 <= len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        if len(body) < length or pos + 12 + length > len(data):
            return f"truncated {ctype!r} chunk"
        (crc,) = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])
        if binascii.crc32(ctype + body) & 0xFFFFFFFF != crc:
            return f"CRC mismatch in {ctype!r}"
        if ctype == b"IHDR":
            width, height = struct.unpack(">II", body[:8])
        elif ctype == b"IDAT":
            idat += body
        elif ctype == b"IEND":
            saw_iend = True
            break
        pos += 12 + length
    if width is None or height is None:
        return "missing IHDR"
    if width > MAX_DIM or height > MAX_DIM or width == 0 or height == 0:
        return f"dimensions {width}x{height} out of range"
    if not saw_iend:
        return "missing IEND"
    try:
        zlib.decompress(idat)
    except zlib.error as exc:
        return f"IDAT does not inflate: {exc}"
    return None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        with open(SRC, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return fail(f"cannot read entry.png: {exc}")
    problem = validate(data)
    if problem:
        return fail(problem)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    os.chmod(dst, 0o644)  # collector reads as another user; keep world-readable
    print(f"entry.png OK: {len(data)} bytes copied to {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
