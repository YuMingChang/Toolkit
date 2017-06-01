from PIL import Image
import re
import os

img = Image.open('icon.png')
pf = open('iconPosition.txt', 'r', encoding='utf8')
nf = open('poke.txt', 'r', encoding='utf8')

if not os.path.exists('icon'):
    os.makedirs('icon')

pokeName = nf.readline()
for line in reversed(pf.readlines()):
    num = line.rstrip().split(' ')
    img2 = img.crop(
        (
            int(num[1]),
            int(num[2]),
            int(num[1]) + 40,
            int(num[2]) + 40
        )
    )
    if num[0] == '000':
        img2.save("icon/{}.png".format(num[0]))
        continue
    elif num[0][:3] == pokeName[1:4]:
        pass
    else:
        pokeName = nf.readline()
    img2.save("icon/{}{}.png".format(num[0],
                                     pokeName[5:].replace(':', '').rstrip()))
    print("{}{}".format(num[0], pokeName[5:].rstrip()))

pf.close()
nf.close()
