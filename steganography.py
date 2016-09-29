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
    if len(binary) < 8:
        pre = ''.join('0' for _ in range(8-len(binary)))
        binary = pre+binary
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

def hide(image, payload_file, output):

    if not os.path.exists(image):
        print '[-] Image File not Found'
        return False

    if not os.path.exists(payload_file):
        print '[-] File not Found'
        return False

    im = Image.open(image)
    width,height = im.size
    px = im.load()
    print '[+] Image Loaded'

    max_bytes = max_payload(width,height)/8
    payload_num_bytes = os.path.getsize(payload_file)
    payload_num_bits = payload_num_bytes*8

    if max_bytes < payload_num_bytes:
        print '[-] File too big for the image'
        print '\tMax Payload : ' + str(max_bytes) + ' B\tFile Size: ' + str(payload_num_bytes) +' B'
        quit()
    else:
        print '[+] File is the right size'
        print '\tMax Payload : ' + str(max_bytes) + ' B\tFile Size: ' + str(payload_num_bytes) +' B'

    header = str(payload_num_bytes)+'#!#'
    f = open(payload_file,'rb')
    read = header+f.read()
    payload = bytearray(read)
    print '[+] Payload loaded'
    print '[+] Hide Payload'

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
    print '[+] Saving file'
    im.save(output)
    print '[+] File saved'

def extract_data(image,output):
    im = Image.open(image)
    px = im.load()
    print '[+] Image Loaded'
    width, height = im.size

    payload = ''
    print '[+] Reading binary data'
    for y in range(height):
        for x in range(width):
            r,g,b = map_tuple(dec_to_bin,px[x,y])
            payload += str(r[-2:])+str(g[-2:])+str(b[-2:])

    result = ''
    print '[+] Converting binary data'
    for x in range(0, len(payload), 8):
        byte = payload[x:x+8]
        result += chr(int(byte,2))

    size = result.split('#!#')[0]
    result=result[(len(size)+3):(int(size)+len(size)+3)]

    print '[+] Saving file'
    f=open(output,'wb')
    f.write(result)
    f.close()
    print '[+] File saved'
