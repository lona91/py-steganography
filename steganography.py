from PIL import Image
import os

def map_tuple(func, tpl):
    new_tuple = ()
    for itup in tpl:
        new_tuple += (func(itup),)
    return new_tuple

def max_payload(width, height, bits=2):
    total_pixels = width*height
    payload = total_pixels*(3*bits)
    return payload

def str_to_bin(str):
    return ''.join(chr_to_bin(c) for c in str)

def chr_to_bin(c):
    binary = bin(ord(c))[2:]
    if len(binary)<8:
        for _ in range(8-len(binary)):
            binary = '0'+binary
    return binary

def bin_to_str(binary):
    return ''.join(chr(binary[x:x+8]) for x in range(0,len(binary),8))

def dec_to_bin(x):
    return bin(x)[2:]

def bin_to_dec(x):
    return int(x,2)

def pixel_coord(index,width):
    return((index%width), int(index/width))

def modify_pixel(px,_6bits):
    r,g,b = map_tuple(dec_to_bin,px)
    r = r[:-2]+_6bits[0:2]
    g = g[:-2]+_6bits[2:4]
    b = b[:-2]+_6bits[4:6]
    return map_tuple(bin_to_dec,(r,g,b))


im = Image.open('test.png')
width,height = im.size
px = im.load()
print '[+] Image Loaded'

f = open('macbeth.txt','rb')
payload = bytearray(f.read())
print '[+] Payload loaded'


max_bytes = max_payload(width,height)/8
payload_num_bytes = os.path.getsize('macbeth.txt')
payload_num_bits = payload_num_bytes*8
if max_bytes < payload_num_bytes:
    print '[-] File too big for the image'
    print '\tMax Payload : ' + str(max_bytes) + ' B\tFile Size: ' + str(payload_num_bytes) +' B'
    quit()
else:
    print '[+] File is the right size'
    print '\tMax Payload : ' + str(max_bytes) + ' B\tFile Size: ' + str(payload_num_bytes) +' B'

i = 0
for index in range(0 , len(payload), 3):
    chars = map_tuple(chr_to_bin,map_tuple(chr,(payload[index],payload[index+1],payload[index+2])))
    _24bitpayload = ''.join(x for x in chars )
    for imgindex in range(0,4):
        _6bits,_24bitpayload = _24bitpayload[:6],_24bitpayload[6:]
        coor = pixel_coord(i+imgindex, width)
        pixel = px[pixel_coord(i+imgindex,width)]
        new_pixel = modify_pixel(pixel,_6bits)
        px[pixel_coord(i+imgindex,width)] = new_pixel
    i+=4


print '[+] Process Completed'
im.save('steno.png')
print '[+] File saved'
