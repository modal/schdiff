"""
schdiff.py takes two schematic images and produces a differenced output.

The script was intended for use with Mentor Design Capture schematic images
taken with PDFFILL.

Prerequistes:
Python 2.7.10
Python Image Library 1.7

Command Line Usage:
schdiff.py old.jpg new.jpg diff.png
"""
from PIL import Image, ImageMath
import sys
import time

if len(sys.argv) != 4:
    print "schdiff.py old.jpg new.jpg diff.png"
    sys.exit()
##############################################################################
R, G, B = 0, 1, 2   #RGB Band indices
invertband=lambda i : 255 - i
##############################################################################
def split_process_old(im=None):
    "This forces red band to 0 and inverts green/blue bands"
    src=im.split()
    rb=src[R].point(lambda i: 0)
    src[R].paste(rb, None, None)
    gb=src[G].point(invertband)
    src[G].paste(gb, None, None)
    bb=src[B].point(invertband)
    src[B].paste(bb, None, None)
    return src

def split_process_new(im=None):
    "Set green band in image to maximum"
    src=im.split()
    gb=src[G].point(lambda i: 255)
    src[G].paste(gb, None, None)
    return src

def xor_using_image_math(src0=None, src1=None):
    rTmp = ImageMath.eval("a^b", a=src0[R], b=src1[R]).convert('L')
    gTmp = ImageMath.eval("a^b", a=src0[G], b=src1[G]).convert('L')
    bTmp = ImageMath.eval("a^b", a=src0[B], b=src1[B]).convert('L')
    merged = Image.merge("RGB", (rTmp, gTmp, bTmp))
    return merged

##############################################################################
om = Image.open(sys.argv[1])        #Old Image
im = Image.open(sys.argv[2])        #Lastest Image

if im.size != om.size:
    print "ERROR:  Images to difference must have same number of pixels"
    print argv[1], " is ", im.size
    print argv[2], " is ", om.size
    sys.exit()

width, height = im.size
print sys.argv[1]
print sys.argv[2]
print "Image Size:  %dx%d" % (width, height)
print "Image Mode:  %s" % im.mode

#Must issue load method for split methods to work
pim = im.load()
pom = om.load()


start_time = time.time()
src0 = split_process_old(om)
#om = Image.merge(om.mode, src0)
#om.save("tmp_new.jpg")
del om
del pom
src1 = split_process_new(im)
#im = Image.merge(im.mode, src1)
#im.save("tmp_old.jpg")
del im
del pim

nm = xor_using_image_math(src0, src1)
print "Fast Method Time %8.3f" % (time.time() - start_time,)
tbn_size= (int(width/4), int(height/4))
nm.thumbnail(tbn_size, Image.ANTIALIAS)
nm.save(sys.argv[3], compress_level=9) #optimize=True)

#Slow Method using direct pixel access
#start_time = time.time()
#ptm = tm.load()
#nm = Image.new("RGB", im.size)      #Difference Image
#tm = Image.new("RGB", im.size)
#pnm = nm.load()
#ptm = tm.load()
#for x in range(width):
#    for y in range(height):
#        r0, g0, b0 = pim[x,y]
#        r1, g1, b1 = pom[x,y]
#        g0 = 255
#
#        r1 = 0
#        g1 = 255 - g1
#        b1 = 255 - b1
#
#        pnm[x, y] = (r0 ^ r1, g0 ^ g1, b0 ^ b1)
#        #ptm[x, y] = (r1, g1, b1)
#        #pnm[x,y]= (r, 255, b) #Make green
#        #pnm[x,y]= (255, g, b) #Make red
#print time.time() - start_time
#nm.save(sys.argv[3], optimize=1)
