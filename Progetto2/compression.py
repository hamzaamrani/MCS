import numpy as np
import math
from PIL import Image
from PIL import ImageChops
from scipy.fftpack import dct
from scipy.fftpack import idct
from flask import Flask, render_template, request

app = Flask(__name__)

def compressionDCT(img, F, d):
    im = np.array(img)
    compressed = im
    N = im.shape[0]
    M = im.shape[1]

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

    imm = Image.fromarray(im)
    return Image.fromarray(compressed)



@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        if request.form.get('Encrypt') == 'Encrypt':
            # pass
            print("Encrypted")
        elif  request.form.get('Decrypt') == 'Decrypt':
            # pass # do something else
            print("Decrypted")
        else:
            # pass # unknown
            return render_template("index.html")
    elif request.method == 'GET':
        # return render_template("index.html")
        print("No Post Back Call")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
    #img = Image.open('images/big_tree.bmp').convert('L')
    #compress = compressionDCT(img, 10, 7)
