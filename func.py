import cv2
import numpy as np

funcs = []

class func_info():
    def __init__(self, func, name, argstype=None):
        self.func = func
        self.name = name
        self.argstype = argstype

    def __call__(self, *args):
        return self.func(*args)

# 01
def BGR2RGB(img):
    H,W,C = img.shape
    B = img[:, :, 0].copy()
    G = img[:, :, 1].copy()
    R = img[:, :, 2].copy()

    out = np.zeros((H,W,3))
    out[:, :, 0] = R
    out[:, :, 1] = G
    out[:, :, 2] = B
    return out.astype(np.uint8)

funcs.append(func_info(BGR2RGB, "BGR2RGB"))

# 02
def BGR2GRAY(img):
    H,W,C = img.shape
    B = img[:, :, 0].copy()
    G = img[:, :, 1].copy()
    R = img[:, :, 2].copy()

    outmat = 0.2126 * R + 0.7152 * G + 0.0722 * B
    out = np.zeros((H,W,3))
    out[:, :, 0] = outmat
    out[:, :, 1] = outmat
    out[:, :, 2] = outmat
    return out.astype(np.uint8)

funcs.append(func_info(BGR2GRAY, "BGR2GRAY"))

# 03
def Binarization(img, threshold=128): # for gray-scale image
    img[img < threshold] = 0
    img[img >= threshold] = 255
    return img.astype(np.uint8)

funcs.append(func_info(Binarization, "Binarization"))

# 04
def OTSU_Binarization(img): # for gray-scale image
    max_t=0
    use_t=-1
    for t in range(0,256):
        v0 = img[np.where(img < t)]
        v1 = img[np.where(img >= t)]
        w0 = len(v0)
        w1 = len(v1)
        m0 = np.mean(v0) if w0>0 else 0.
        m1 = np.mean(v1) if w1>0 else 0.
        Sb2 = w0 * w1 * (m0-m1)**2
        if Sb2 > max_t:
            max_t = Sb2
            use_t = t
    img[img < use_t]=0
    img[img >= use_t]=255
    return img.astype(np.uint8)

funcs.append(func_info(OTSU_Binarization, "OTSU_Bin"))

# 05
def BGR2HSV(img):
    img = img.astype(np.float64) / 255.
    height,width,C = img.shape
    B = img[:, :, 0].copy()
    G = img[:, :, 1].copy()
    R = img[:, :, 2].copy()

    max_values = np.max(img,axis=2).copy()
    min_values = np.min(img,axis=2).copy()
    min_index = np.argmin(img,axis=2).copy()

    H = np.zeros((height,width))
    index = np.where(min_values==max_values)
    H[:, :][index]=0
    index = np.where(min_index==0)
    H[:, :][index]=60*(G[:,:][index]-R[:,:][index])/(max_values[:,:][index]-min_values[:,:][index])+60
    index = np.where(min_index==1)
    H[:, :][index]=60*(R[:,:][index]-B[:,:][index])/(max_values[:,:][index]-min_values[:,:][index])+300
    index = np.where(min_index==2)
    H[:, :][index]=60*(B[:,:][index]-G[:,:][index])/(max_values[:,:][index]-min_values[:,:][index])+180

    S = (max_values.copy() - min_values.copy())
    V = max_values.copy()
    return H,S,V

def HSV2BGR(H,S,V):
    height,width = H.shape

    C = S
    Hd = H / 60.
    X = C * (1 - np.abs(Hd % 2 - 1))

    img = np.zeros((height,width,3))
    Z = np.zeros((height,width))
    chv = [[Z,X,C],[Z,C,X],[X,C,Z],[C,X,Z],[C,Z,X],[X,Z,C]]

    for i in range(6):
        index = np.where((i <= Hd) & (Hd < i+1))
        for col in range(3):
            img[:, :, col][index] = (V - C)[index] + chv[i][col][index]
    
    img = np.clip(img,0,1)
    return img*255

def Hue_inversion(img, addition=180):
    H,S,V = BGR2HSV(img)
    Hd = (H + addition) % 360
    out = HSV2BGR(Hd,S,V)
    return out.astype(np.uint8)

funcs.append(func_info(Hue_inversion, "Hue_inversion"))

# 06
def Color_reduction(img, sep=64):
    img = img.astype(np.float64)
    height,width,C = img.shape

    out = (img // sep) *sep + sep//2
    return out.clip(0,255).astype(np.uint8)

funcs.append(func_info(Color_reduction, "Color_reduction"))

# 07
def Mean_pooling(img,pixels=8):
    img = img.astype(np.float64)
    height,width,C = img.shape

    out = np.zeros((height,width,3))
    gridx = width // pixels
    gridy = height // pixels
    for y in range(gridy):
        for x in range(gridx):
            for col in range(3):
                out[y*pixels:(y+1)*pixels, x*pixels:(x+1)*pixels, col] = np.mean(img[y*pixels:(y+1)*pixels, x*pixels:(x+1)*pixels, col])
    return out.astype(np.uint8)

funcs.append(func_info(Mean_pooling, "Mean_pooling"))

# 08
def Max_pooling(img,pixels=8):
    img = img.astype(np.float64)
    height,width,C = img.shape

    out = np.zeros((height,width,3))
    gridx = width // pixels
    gridy = height // pixels
    for y in range(gridy):
        for x in range(gridx):
            for col in range(3):
                out[y*pixels:(y+1)*pixels, x*pixels:(x+1)*pixels, col] = np.max(img[y*pixels:(y+1)*pixels, x*pixels:(x+1)*pixels, col])
    return out.astype(np.uint8)

funcs.append(func_info(Max_pooling, "Max_pooling"))

# 09
def Gaussian_filter(img, k=5, sigma=1.3, padding_type='constant'):
    if len(img.shape)==2:
        img = np.expand_dims(img, axis=-1)
    img = img.astype(np.float64)
    pad_size = k // 2
    padimg = np.pad(img,[(pad_size,pad_size),(pad_size,pad_size),(0,0)],padding_type)
    height,width,C = img.shape
    out = np.zeros((height,width,C))

    mul = np.zeros((k,k))
    for y in range(-pad_size, pad_size+1):
        for x in range(-pad_size, pad_size+1):
            mul[y+pad_size, x+pad_size] = np.exp(-(x**2 + y**2) / (2*(sigma**2)))
    mul /= mul.sum()

    for y in range(pad_size,height+pad_size):
        for x in range(pad_size,width+pad_size):
            for col in range(C):
                out[y-pad_size,x-pad_size,col]=np.sum(mul * padimg[y-pad_size:y+pad_size+1, x-pad_size:x+pad_size+1, col])

    if C==1:
        out = out.reshape((height,width))
    return out.astype(np.uint8)

funcs.append(func_info(Gaussian_filter, "Gaussian_filter"))

# 10
def Median_filter(img):
    img = img.astype(np.float64)
    padimg = np.pad(img,[(1,1),(1,1),(0,0)],'constant')
    height,width,C = img.shape
    out = np.zeros((height,width,3))

    for y in range(1,height+1):
        for x in range(1,width+1):
            for col in range(3):
                out[y-1,x-1,col]=np.median(padimg[y-1:y+2, x-1:x+2, col])

    return out.astype(np.uint8)

funcs.append(func_info(Median_filter, "Median_filter"))