from PIL import Image
import random
import os

def pixel_coord(index,width):
    return((index%width), int(index/width))

def get_next_4_pixels(index,img):
    px_list = []
    for _ in range(0,4):
        px = img.getpixel(pixel_coord(index,img.size[1]))
        px_list.append(px)
        index+=1
    return px_list

def char_to_bin(c):
    binary = bin(ord(c))[2:]
    if len(binary) < 8:
        pre = ''.join('0' for _ in range(8-len(binary)))
        binary = pre+binary
    return binary

def bit_generator(string):
    payload = ''.join(char_to_bin(c) for c in string)
    for _ in payload:
        bit,payload = payload[:1],payload[1:]
        yield str(bit)
    while True:
        yield '0'

def dec_to_bin(x):
    return bin(x)[2:]

def map_tuple(func, tpl):
    new_tuple = ()
    for itup in tpl:
        new_tuple += (func(itup),)
    return new_tuple


im = Image.open('image.png')
px = im.load()
print '[+] Image Loaded'

width,height = im.size
max_payload = ((width*height)*3)/8
paylod_size = os.path.getsize('payload.txt')
payload_size_in_bits = paylod_size*8+8

if max_payload < paylod_size:
    print '[-] Payload too big for the image'
    print '\tMax Payload: ' + str(max_payload) + ' Bytes\tPayload Size: ' + str(paylod_size) + ' Bytes'
    quit()

print '\tMax Payload: ' + str(max_payload) + ' Bytes\tPayload Size: ' + str(paylod_size) + ' Bytes'

f = open('payload.txt','r')
payload = f.read()
print '[+] Opened payload file'

bit_stream = bit_generator(payload)
print '[+] Bit Stream Created'

i=0
print '[+] Modifying image'
for y in range(height):
    if i > payload_size_in_bits:
        break
    for x in range(width):
        if i > payload_size_in_bits:
            break
        print i
        i+=6
        r,g,b = map_tuple(dec_to_bin,px[x,y])

        rb = r[:-2]+bit_stream.next()+bit_stream.next()
        gb = g[:-2]+bit_stream.next()+bit_stream.next()
        bb = g[:-2]+bit_stream.next()+bit_stream.next()

        px[x,y] = (int(rb,2),int(gb,2),int(bb,2))
print  '[+] Image Modified'

im.save('steno.png')
print '[+] Image Saved'
