import numpy as np
import cv2 as cv

def get_x(hue, c):
    return c[:,:,0] * (np.ones(c[:,:,0].shape) - np.absolute(np.subtract(np.mod(np.divide(hue[:,:,0], 60.0),2), 1)))

def rgb1(hcx):
    hue = hcx[0]
    c = hcx[1]
    x = hcx[2]
    if 0 <= hue < 60 or hue == 360.0:
        return [0,x,c]
    elif 60 <= hue < 120:
        return [0,c,x]
    elif 120 <= hue < 180:
        return [x,c,0]
    elif 180 <= hue < 240:
        return [c,x,0]
    elif 240.0 <= hue < 300.0:
        return [c,0,x]
    elif 300 <= hue < 360:
        return [x,0,c]
    else:
        return [0,0,1]

def to_rgb(h,s,v):
    sv = np.stack([s,v],-1)
    c = np.multiply(s,v)
    x = get_x(h, c)
    m = v - c
    pre = np.stack([h[:,:,0], c[:,:,0], x], -1)
    img_rgb1 = np.apply_along_axis(rgb1, -1, pre)
    return np.multiply(np.add(img_rgb1, m), 255)


def equalize(img):
    values, counts = np.unique(img[:,:], return_counts=True)

    for i in range(1,len(counts)):      # make it cumulative
        counts[i] = counts[i-1] + counts[i]
        # cumulative = counts/float(counts.max())  # <-- between 0 to 1

    pix_num = counts.max()
    pix_in_bin = pix_num / 255  # number of pixels in any given bin = total num of pixels / number of intervals(bins)
    #count_per_bin = np.zeros(256)
    for pixel in np.nditer(img, op_flags=['readwrite']):
        # basically find out which new bin the pixel should belong to
        pixel[...] = counts[pixel]/pix_in_bin
    return img/255.0 # return brightness values to [0,1]



concertval = cv.imread('dark.jpg',0)
concertval = equalize(concertval)
cv2.imwrite('darkeq.jpg', concertval)
#cv.imwrite('concert_hsv2rgb.jpg', concert_rgb)
# cv.imwrite('concert_histeq.jpg', to_rgb(concerthue,concertsat,concertval))
# cv.imwrite('sea1_histeq.jpg', to_rgb(sea1hue,sea1sat,sea1val))
# cv.imwrite('sea2_histeq.jpg', to_rgb(sea2hue,sea2sat,sea2val))
