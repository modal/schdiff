"""
schdiff.py takes two images and produces a differenced output

Usage:
schdiff.py old.jpg new.jpg diff.png

"""

from PIL import Image, ImageMath
import sys

if len(sys.argv) != 4:
    print "schdiff.py old.jpg new.jpg diff.png"
    sys.exit()
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

#Must issue load method for split method to work
pim = im.load()
pom = om.load()

R, G, B = 0, 1, 2   #RGB Band indices
invertband=lambda i : 255 - i

#src0=om.split()
#rb=src0[R].point(lambda i: 0)
#src0[R].paste(rb, None, None)
#gb=src0[G].point(invertband)
#src0[G].paste(gb, None, None)
#bb=src0[B].point(invertband)
#src0[B].paste(bb, None, None)
#om = Image.merge(om.mode, src0)
#om.save("tmpn.jpg")
##del om              #Free Up Memory
#
#src1=im.split()
#gb=src1[G].point(lambda i: 255)
#src1[G].paste(gb, None, None)
#im = Image.merge(im.mode, src1)
#im.save("tmpo.jpg")
##del im              #Free Up Memory

#nm = ImageMath.eval("int(a^b)", a=im, b=om)
#nm = ImageMath.eval("convert(a^b, 'L')", a=im, b=om)

#rTmp = ImageMath.eval("a^b", a=src0[R], b=src1[R])
#gTmp = ImageMath.eval("a^b", a=src0[G], b=src1[G])
#bTmp = ImageMath.eval("a^b", a=src0[B], b=src1[B])
#nm = Image.merge("RGB", (rTmp, gTmp, bTmp))


#Slow Method using direct pixel access
#ptm = tm.load()
nm = Image.new("RGB", im.size)      #Difference Image
tm = Image.new("RGB", im.size)
pnm = nm.load()
ptm = tm.load()
for x in range(width):
    for y in range(height):
        r0, g0, b0 = pim[x,y]
        r1, g1, b1 = pom[x,y]
        g0 = 255

        r1 = 0
        g1 = 255 - g1
        b1 = 255 - b1

        pnm[x, y] = (r0 ^ r1, g0 ^ g1, b0 ^ b1)
        #ptm[x, y] = (r1, g1, b1)
        #pnm[x,y]= (r, 255, b) #Make green
        #pnm[x,y]= (255, g, b) #Make red

nm.save(sys.argv[3])
