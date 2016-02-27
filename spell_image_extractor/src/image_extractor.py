from PIL import Image
import glob
import DDSImagePlugin #importing this allows pil to handle DDS images
import json
img_w = 231
img_h = 330

def v(i, x, y, bgcolor, card_w, card_h):
    iw, ih = i.size
    if x + min(card_h, card_w) > iw or y + min(card_h, card_w) > ih:
        return 0
    if bgcolor[3] == 0:
        if (i.getpixel((x, y))[3] + 
            i.getpixel((x + 1, y))[3] + 
            i.getpixel((x, y + 1))[3]) == 0 and i.getpixel((x + 1, y + 1))[3] > 0:
            # found bottom left corner
            if x + card_w + 1 < iw and y + card_h + 1 < ih and (
                i.getpixel((x + card_w + 1, y + card_h + 1))[3] +
                i.getpixel((x + card_w, y + card_h + 1))[3] +
                i.getpixel((x + card_w + 1, y + card_h))[3]) == 0 and i.getpixel((x + card_w, y + card_h))[3] > 0:
                return 1
            elif x + card_h + 1 < iw and y + card_w + 1 < ih and (
                i.getpixel((x + card_h + 1, y + card_w + 1))[3] +
                i.getpixel((x + card_h, y + card_w + 1))[3] +
                i.getpixel((x + card_h + 1, y + card_w))[3]) == 0 and i.getpixel((x + card_h, y + card_w))[3] > 0:
                return 2
    elif sum(bgcolor[:3]) < 10:
        print (sum(i.getpixel((x, y))[:3]) +
            sum(i.getpixel((x + 1, y))[:3]) +
            sum(i.getpixel((x, y + 1))[:3]))
        if (sum(i.getpixel((x, y))[:3]) +
            sum(i.getpixel((x + 1, y))[:3]) +
            sum(i.getpixel((x, y + 1))[:3])) < 20 and sum(i.getpixel((x + 1, y + 1))[:3]) > 40: 
            # found bottom left corner
            if x + card_w + 1 < iw and y + card_h + 1 < ih and (
                sum(i.getpixel((x + card_w + 1, y + card_h + 1))[:3]) +
                sum(i.getpixel((x + card_w, y + card_h + 1))[:3]) +
                sum(i.getpixel((x + card_w + 1, y + card_h))[:3])) < 20 and sum(i.getpixel((x + card_w, y + card_h))[:3]) > 40:
                return 1
            elif x + card_h + 1 < iw and y + card_w + 1 < ih and (
                sum(i.getpixel((x + card_h + 1, y + card_w + 1))[:3]) +
                sum(i.getpixel((x + card_h, y + card_w + 1))[3]) +
                sum(i.getpixel((x + card_h + 1, y + card_w))[3])) < 20 and sum(i.getpixel((x + card_h, y + card_w))[3]) > 40:
                return 2
    return 0

img_num = 0
def split(fname, bundle, card_w=231, card_h=330):
    img = Image.open(fname)
    width, height = img.size
    x, y = 0, 0
    global img_num
    bgcolor = img.getpixel((0, 0))
    if bgcolor[3] != 0:
        print 'UHOH', bgcolor,
    for y in range(height - min(card_w, card_h)):
        x = 0
        while x < width - min(card_w, card_h):
            orientation = v(img, x, y, bgcolor, card_w, card_h)
            if orientation == 1:
                subimg = img.crop((x + 1, y + 1, x + card_w + 1, y + card_h + 1))
                subimg_rot = subimg.transpose(Image.ROTATE_180)
                output_name = 'images/' + str(bundle) + '_' + str(img_num) + '.png'
                subimg_rot.save(output_name)
                img_num += 1
                x += card_w + 1
            elif orientation == 2:
                subimg = img.crop((x + 1, y + 1, x + card_h + 1, y + card_w + 1))
                subimg_rot = subimg.transpose(Image.ROTATE_90)
                output_name = 'images/' + str(bundle) + '_' + str(img_num) + '.png'
                subimg_rot.save(output_name)
                img_num += 1
                x += card_h + 1
            else:
                x += 1

bundle_lookup = dict()
apiphp_file = open('apiphp.json')
asset_bundles = json.load(apiphp_file)
apiphp_file.close()
#add in resources from main unity3d file
bundle_lookup['resources'] = '0'
for bundle in asset_bundles.values():
    bundle_lookup[bundle['bundle_name'].rsplit('.', 1)[0]] = bundle['id']


atlases = glob.glob('data/*/Texture2D/atlas*.dds')
#add in resources path
atlases.extend(glob.glob('data/*/*/Texture2D/atlas*.dds'))
for atlas in atlases:
    print 'starting ' + atlas,
    if 'resources' in atlas:
        card_w = 280
        card_h = 400
    else:
        card_w = 231
        card_h = 330
    split(atlas, bundle_lookup[atlas.split('\\', 3)[1]], card_w, card_h)
    print '. . . finished.'

print img_num, ' images saved' 
