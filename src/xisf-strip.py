import sys
from xisf import XISF
from pathlib import Path

dry_run = False

if len(sys.argv) < 2:
    print('XISF Strip v1.0 (2026) Luca Padovani')
    print('Usage: xisf-strip path')
    sys.exit(-1)

def strip(file_name):
    xisf = XISF(file_name)
    file_meta = xisf.get_file_metadata()
    ims_meta = xisf.get_images_metadata()
    im_data = xisf.read_image(0)

    if len(ims_meta) > 1 or 'compression' not in ims_meta[0]:
        if dry_run:
            if len(ims_meta) > 1:
                print('stripping', end = ' ')
            if 'compression' not in ims_meta[0]:
                print('compressing', end = ' ')
        else:
            XISF.write(
                file_name, im_data,
                creator_app = "XISF Strip",
                image_metadata = ims_meta[0],
                xisf_metadata = file_meta,
                codec = 'zstd', shuffle = True
            )
        return True
    else:
        return False

for p in Path(sys.argv[1]).rglob('*.xisf'):
    print('Processing', p, '... ', end = '')
    res = strip(p)
    if res:
        print('done')
    else:
        print('nothing to do')
