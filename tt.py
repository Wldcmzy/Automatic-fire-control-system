from pybase import dataSR
import time
a = dataSR.SR()
a.receive()
c = 0
while True:
    w = a.getData()
    if w != None:
        print(w)
        a.send('ok:' + w[0], w[1])