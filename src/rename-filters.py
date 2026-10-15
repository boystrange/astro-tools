import sys
from xisf import XISF
from pathlib import Path

dry_run = False

if len(sys.argv) < 2:
    print('XISF Rename Filters v1.0 (2026) Luca Padovani')
    print('Usage: rename-filters file...')
    sys.exit(-1)

filter_map = dict(
    [ ('L',    'Lum'),
      ('R',    'Red'),
      ('B',    'Blue'),
      ('G',    'Green'),
      ('Ha',   'Ha'),
      ('Sii',  'SII'),
      ('Oiii', 'OIII') ]
)

def update(file_name):
    xisf = XISF(file_name)
    file_meta = xisf.get_file_metadata()
    ims_meta = xisf.get_images_metadata()
    im_data = xisf.read_image(0)
    old_filter = ims_meta[0]['XISFProperties']['Instrument:Filter:Name']['value']
    new_filter = filter_map.get(old_filter, old_filter)
    print('>>', old_filter, '=>', new_filter)
    if old_filter != new_filter and not dry_run:
        ims_meta[0]['XISFProperties']['Instrument:Filter:Name']['value'] = new_filter
        XISF.write(
            file_name, im_data,
            image_metadata = ims_meta[0],
            xisf_metadata = file_meta,
            codec = 'lz4hc', shuffle = True
        )

for p in Path(sys.argv[1]).rglob('*.xisf'):
    print('Processing', p, '... ')
    update(p)
