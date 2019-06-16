import numpy as np
import math
import random
from scipy.fftpack import dct
from scipy.fftpack import dctn
from scipy.fftpack import idct
from datetime import datetime
import matplotlib.pyplot as plt

#***************************************************************DCT di tipo 2
def mydct(f):
    N = f.size
    y = np.zeros(N)

    for k in range(N):
        #normalization factor
        if k==0:
            a = np.sqrt(1/N)
        else:
            a = np.sqrt(2/N)
        sum = 0
        for i in range(N):
            c = k * math.pi * (2*i + 1) / (2*N)
            sum = sum + f[i] * np.cos(c)
        y[k] = a * sum

    return y

def myidct(f):
    N = f.size
    y = np.zeros(N)

    for j in range(N):
        sum = 0
        for k in range(N):
            #normalization factor
            if k==0:
                a = np.sqrt(1/N)
            else:
                a = np.sqrt(2/N)
            c = k * math.pi * (2*j + 1) / (2*N)
            sum = sum + f[k] * a * np.cos(c)
        y[j] = sum

    return y

#***************************************************************DCT2
def mydct2(F):
    N = F.shape[0]
    M = F.shape[1]
    Y = np.zeros((N,M))

    for k in range(N):
        for l in range(M):
            #normalization factor
            if(k==0 and l==0):
                a = np.sqrt(1/(N*M))
            elif(l==0 or k==0):
                a = np.sqrt(2/(N*M))
            else:
                a = 2/np.sqrt(N*M)
            sum=0
            for i in range(N):
                for j in range(M):
                    c1 = k * math.pi * (2*i + 1) / (2*N)
                    c2 = l * math.pi * (2*j + 1) / (2*M)
                    sum = sum + F[i,j] * np.cos(c1) * np.cos(c2)
            Y[k,l] = a * sum

    return Y

def mydct2_2(F):
    N = F.shape[0]
    M = F.shape[1]

    F = F.T
    for i in range(M):
        F[i,:] = mydct(F[i,:])

    F = F.T
    for i in range(N):
        F[i,:] = mydct(F[i,:])

    return F

def myidct2(F):
    N = F.shape[0]
    M = F.shape[1]
    Y = np.zeros((N,M))

    for i in range(N):
        for j in range(M):
            sum=0
            for k in range(N):
                for l in range(M):
                    #normalization factor
                    if(k==0 and l==0):
                        a = np.sqrt(1/(N*M))
                    elif(l==0 or k==0):
                        a = np.sqrt(2/(N*M))
                    else:
                        a = 2/np.sqrt(N*M)
                    c1 = k * math.pi * (2*i + 1) / (2*N)
                    c2 = l * math.pi * (2*j + 1) / (2*M)
                    sum = sum + F[k,l] * a * np.cos(c1) * np.cos(c2)
            Y[i,j] = sum
    return Y

def myidct2_2(F):
    N = F.shape[0]
    M = F.shape[1]

    F = F.T
    for i in range(M):
        F[i,:] = myidct(F[i,:])

    F = F.T
    for i in range(N):
        F[i,:] = myidct(F[i,:])

    return F

def generatorM (N):
    X = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            X[i,j] = random.randrange(0, 255).real

    return X

#----------MAIN------------
if __name__ == "__main__":
    # numpy array
    x = np.array([231., 32., 233., 161., 24., 71., 140., 245.])
    print("x:\t",x)

    # apply scipy.fftpack.dct function on array x
    y = dct(x, norm='ortho') #type=2
    print("\nscipy.fftpack.dct(x):\t",y)

    w = idct(y, norm='ortho') #type=2
    print("\nscipy.fftpack.idct(y):\t",w)

    # apply mydct function on array x
    z = mydct(x)
    print("\nmydct(x):\t",z)

    w = myidct(z)
    print("\nmyidct(x):\t",w)

    # bidimensional numpy array
    X=np.array([[231., 32., 233., 161., 24., 71., 140., 245.],
               [247., 40., 248., 245., 124., 204., 36., 107.],
               [234., 202., 245., 167., 9., 217., 239., 173.],
               [193., 190., 100., 167., 43., 180., 8., 70.],
               [11., 24., 210., 177., 81., 243., 8., 112.],
               [97., 195., 203., 47., 125., 114., 165., 181.],
               [193., 70., 174., 167., 41., 30., 127., 245.],
               [87., 149., 57., 192., 65., 129., 178., 228.]])
    print("\n************************************\n\n")
    print("X:\n",X)

    Y = dct(dct(X.T, norm='ortho').T, norm='ortho') #type=2
    print("\ndct(X):\n",Y)

    W = idct(idct(Y.T, norm='ortho').T, norm='ortho') #type=2
    print("\nscipy.fftpack.idct(y):\t",W)

    # apply mydct2 function on bidimensional array X
    Z = mydct2(X)
    print("\nmydct2(X):\n",Z)

    Z = mydct2_2(X)
    print("\nmydct2_2(X):\n",Z)

    W = myidct2(Z)
    print("\nmyidct2(Z):\n",W)

    W = myidct2_2(Z)
    print("\nmyidct2_2(Z):\n",W)

    print("\n************************************\n")

    N=20
    T1 = np.zeros(N) #
    T2 = np.zeros(N)
    for n in range (1,N+1):
        X = generatorM(n)
        #print("\nMatrix ",n,"x",n)

        begin = datetime.now()
        Y = dctn(X, norm='ortho') #type=2
        #Y = dct(dct(X.T, norm='ortho').T, norm='ortho')
        end = datetime.now() - begin
        #print("DCT2 - Execution time: " + str(end)[6:] + " s")
        T1[n-1] = float(str(end)[6:]) * 1000

        begin = datetime.now()
        Z = mydct2(X)
        end = datetime.now() - begin
        #print("MYDCT2 - Execution time: " + str(end)[6:] + " s")
        T2[n-1] = float(str(end)[6:]) * 1000

    print("\nMatrix DIM 1-",N)
    print(T1)
    print(T2)


    plt.plot(T1, marker='.', color='r')
    plt.plot(T2, marker='.', color='b')
    plt.legend(['DCT2 scipy', 'DCT2 mine'], loc='upper left')

    plt.title('DCT comparison on random matrixes')
    plt.xlabel('Matrix dimension')
    plt.ylabel('Time (ms)')
    plt.show()
