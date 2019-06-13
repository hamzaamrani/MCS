import numpy as np
import math
from PIL import Image
from PIL import ImageChops
from scipy.fftpack import dct
from scipy.fftpack import idct
from flask import Flask, render_template, request
import io
import base64
from io import BytesIO
import sys

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



@app.route("/")
def index():
    return render_template("index.html")

@app.route('/compress', methods=['POST'])
def classify_upload():
    try:
        print("Uploaded image.")
        imagefile = request.files['imagefile']
        img = Image.open(imagefile).convert('L')
        #img.show()

        F = int( request.form.get('F') )
        d = int( request.form.get('d') )

        if (d<0 or d>(2*F-2)):
            print("Error on d.")
            return render_template(
                'index.html', has_result=True,
                result=(False, 'Error on d: 0 < d < 2F-2.')
            )

        compressed = compressionDCT(img, F, d)
        diff = ImageChops.difference(img, compressed)
    except Exception as err:
        print("Cannot open uploaded image.")
        return render_template(
            'index.html', has_result=True,
            result=(False, 'Cannot open uploaded image or incorrect parameters')
        )

    w, h = img.size

    img_file = BytesIO()
    img.save(img_file, 'png')
    sO = round( int(img_file.tell()) / 1024, 2)

    img_file = BytesIO()
    compressed.save(img_file, 'png')
    sC = round( int( img_file.tell()) /1024, 2)
    p = round( sC/sO, 2)
    return render_template(
        'index.html', has_result=True,
        result=(True, 'Image uploaded. Correct parameters.', F, d, w, h, sO, sC, p),
        imagesrc = embed_image_html(img),
        imagesrccompressed = embed_image_html( compressed ),
        difference = embed_image_html( diff )
    )

def embed_image_html(image):
    """Creates an image embedded in HTML base64 format."""
    string_buf = io.BytesIO()
    image.save(string_buf, format='bmp')
    data = base64.b64encode( string_buf.getvalue())
    data = str(data).replace('\n', '').replace('\'', '')
    return 'data:image/bmp;base64,' + data[1:]

if __name__ == "__main__":
    app.run(debug=True)
