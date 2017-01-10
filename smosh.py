#! /usr/bin/env python

from wand.image import Image
from wand.display import display
from optparse import OptionParser

def main(opts):
    with Image(filename=opts.filename) as img:
        orig_height = img.height
        orig_width = img.width
        frames = len(img.sequence)

        print "Orig size: %s x %s" % (orig_width, orig_height)
        print "Frames: %i" % (frames,)

        curr_frame = 0
        with Image() as dst_img:
            for frame in img.sequence:
                new_h, new_w = get_resize_dimensions(curr_frame, frames, orig_height, orig_width, opts.maxsmosh)
                frame.liquid_rescale(new_w, new_h)
                print "Frame: %i liquid-resize: %i x %i" % (curr_frame, frame.width, frame.height)
                frame.resize(orig_width, orig_height)
                dst_img.sequence.append(frame)
#                frame.destroy()
                curr_frame += 1
            dst_img.type = 'optimize'
            dst_img.save(filename=opts.outputname)


def get_resize_dimensions(frame, frame_count, orig_h, orig_w, maxsmosh):
    max_smosh_mult = float(maxsmosh) / 100.0
    perc_done = (float(frame) / float(frame_count)) * max_smosh_mult
    new_h = int(float(orig_h) * (1.0 - perc_done))
    new_w = int(float(orig_w) * (1.0 - perc_done))
    return (new_h, new_w)

if __name__ == '__main__':
    # do an option
    p = OptionParser()
    p.add_option('-f', '--file', dest='filename', type='string', default=None, help='File to smosh.')
    p.add_option('-m', '--max', dest='maxsmosh', type='int', default=50, help='Max percentage top smosh.')
    p.add_option('-o', '--output', dest='outputname', type='string', default='smosh.gif', help='output filename')
    
    options, args = p.parse_args()
    main(options)
