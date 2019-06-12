import numpy as np
import math
from PIL import Image
from scipy.fftpack import dct
from scipy.fftpack import idct



img = Image.open('images/artificial.bmp').convert('L')
im = np.array(img)
compressed = im
N = im.shape[0]
M = im.shape[1]

F = 10
d = 7
#d
NF = int((N/F)//1)
MF = int((M/F)//1)
f = NF * MF
#suddividere l'immagine in blocchi quadrati f di pixel di dimensioni F F
blocks = {}
k=0
for i in range (NF):
    for j in range(MF):
        blocks[k] = im[i*F:i*F+F, j*F:j*F+F]
        #per ogni blocco f applicare la DCT2
        blocks[k] = dct(dct(blocks[k].T, norm='ortho').T, norm='ortho')
        k=k+1

for i in range(f):
    for k in range(F):
        for l in range(F):
            #per ogni blocco eliminare le frequenze ck con k+l>=d
            if k+l >= d:
                blocks[i][k,l] = 0
    #per ogni blocco f applicare la IDCT2
    blocks[i] = idct(idct(blocks[i].T, norm='ortho').T, norm='ortho')

#arrotondare ff all'intero piu vicino, mettere a zero i valori negativi e a 255
#quelli maggiori di 255 in modo da avere dei valori ammissibili
for i in range(f):
    for k in range(F):
        for l in range(F):
            if blocks[i][k,l] < 0:
                blocks[i][k,l] = 0
            if blocks[i][k,l] > 255:
                blocks[i][k,l] = 255

#ricomporre l'immagine mettendo insieme i blocchi ff nell'ordine giusto.
k=0
for i in range (NF):
    for j in range(MF):
        compressed[i*F:i*F+F, j*F:j*F+F] = blocks[k]
        k = k + 1

compress = Image.fromarray(compressed)
compress.save('images/artificialC.bmp','bmp')
