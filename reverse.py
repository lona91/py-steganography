from PIL import Image
import os

def map_tuple(func, tpl):
    new_tuple = ()
    for itup in tpl:
        new_tuple += (func(itup),)
    return new_tuple

def dec_to_bin(x):
    return bin(x)[2:]


def bin_to_dec(x):
    return int(x,2)

im = Image.open('steno.png')
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
f=open('result.txt','wb')
f.write(result)
f.close()

print '[+] File saved'
