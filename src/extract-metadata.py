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
        frame = (fits['DATE-OBS'][:10], fits['FILTER'], int(float(fits['EXPOSURE'])))
        data.insert(0, frame)

for p in Path(sys.argv[1]).rglob('*.xisf'):
    go(p)

def group(l):
    return [ (k, len(list(g))) for k, g in groupby(sorted(l)) ]

code_of_filter = {
    'Lum'   : 4452,
    'Red'   : 4457,
    'Green' : 4447,
    'Blue'  : 4442,
    'Ha'    : 4410,
    'OIII'  : 4415,
    'SII'   : 4420,
}

print('date,filter,number,duration,bortle')
for k, n in group(data):
    date, filterName, exposure = k
    print(f"{date},{code_of_filter[filterName]:d},{n:d},{exposure:d},7")
    # exp = sum(map(itemgetter(3), l))
    # h = exp // 3600
    # m = (exp - h * 3600) // 60
    # print("%10s %d:%02d" % (f, h, m))
