# Original code by Sergio Díaz, sergiodiaz.eu
# Example file for the xisf package (https://github.com/sergio-dr/xisf)
# fits2xisf: command line tool for converting FITS to XISF
# (only the first image HDU!)

from xisf import XISF
from astropy.io import fits
import numpy as np
import argparse
from pathlib import Path

APP_NAME = "fits2xisf"

help_desc = (
    "Command line tool to convert (potentially compressed) FITS files "
    "to XISF (only first image HDU!). "
    f"Based on {XISF._creator_module}."
)
parser = argparse.ArgumentParser(description=help_desc)
parser.add_argument("path", help="Input path")
parser.add_argument(
    "-c",
    "--compression",
    choices=["zstd", "zlib", "lz4", "lz4hc", "none"],
    default="zstd",
    help="Compression type",
)
args = parser.parse_args()

def fetch(input_file):
    print(f"Fetching {input_file}...")
    fits.open(input_file)

def convert(input_file):
    output_file = input_file.with_suffix('.xisf')

    print(f"Opening {input_file}...")
    hdul = fits.open(input_file)
    # Searchs for the first HDU with image data
    for hdu in hdul:
        if isinstance(hdu.data, np.ndarray):
            native_endian = hdu.data.dtype.newbyteorder("=")  # dtype to native endianness
            img_data = np.atleast_3d(hdu.data.astype(native_endian))  # Ensure 3D array and native byte order
            fits_header = hdu.header  # Header assumed in the same HDU

    print(f"Image dimensions: {img_data.shape}")
    print(f"Image data dtype: {img_data.dtype}")

    print("Header:")
    fits_keyw = {}
    for k, v in fits_header.items():
        if not k:
            continue
        c = fits_header.comments[k]
        # print(f"{k:9s}: {v} [{c}]")
        entry = fits_keyw.setdefault(k, [])
        fits_keyw[k] = entry + [{"value": str(v), "comment": str(c)}]

    # Here we may attempt to populate XISF image properties from FITS headers,
    # (see section '11.5.3 Astronomical Image Properties' of XISF spec.),
    # but PixInsight does this anyway.
    img_meta = {"FITSKeywords": fits_keyw}
    codec = None if args.compression == "none" else args.compression
    XISF.write(output_file, img_data, APP_NAME, img_meta, codec=codec, shuffle=True)
    input_file.unlink()

for p in Path(args.path).rglob('*.fit'):
    fetch(p)
for p in Path(args.path).rglob('*.fits'):
    fetch(p)

for p in Path(args.path).rglob('*.fit'):
    convert(p)
for p in Path(args.path).rglob('*.fits'):
    convert(p)
