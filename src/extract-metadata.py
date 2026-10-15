import sys
from xisf import XISF
from pathlib import Path
from itertools import groupby
from operator import itemgetter

if len(sys.argv) < 2:
    print('Extract Metadata v1.0 (2026) Luca Padovani')
    print('Usage: extract-metadata path')
    sys.exit(-1)

data = []

def go(file_name):
    xisf = XISF(file_name)
    file_meta = xisf.get_file_metadata()
    ims_meta = xisf.get_images_metadata()
    im_data = xisf.read_image(0)
    fits = dict([ (key, l[0]['value']) for key, l in ims_meta[0]['FITSKeywords'].items() ])
    if fits['IMAGETYP'] == 'LIGHT':
        frame = (fits['DATE-OBS'][:10],
                 fits['FILTER'],
                 1,
                 float(fits['EXPOSURE']),
                 '', # ISO
                 max(int(float(fits['XBINNING'])), int(float(fits['YBINNING']))),
                 fits['GAIN'],
                 fits['CCD-TEMP'])
        data.insert(0, frame)

for p in Path(sys.argv[1]).rglob('*.xisf'):
    go(p)

def group(l, f):
    return [ (k, list(g)) for k, g in groupby(sorted(l, key = f), key = f) ]

# by_date   = group(data, itemgetter(0))
by_filter = group(data, itemgetter(1))

for f, l in by_filter:
    exp = sum(map(itemgetter(3), l))
    h = exp // 3600
    m = (exp - h * 3600) // 60
    print("%10s %d:%02d" % (f, h, m))
