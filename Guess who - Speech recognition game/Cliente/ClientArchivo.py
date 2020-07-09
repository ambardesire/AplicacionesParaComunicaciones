import socket
import pickle
import os
from os import stat
from array import array

host = "127.0.0.1"
port = 8500

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, int(port)))
    print("Socket conectado")

    print("Abriendo archivo de audio")
    arr = array('B')
    result = stat("Ojos_azules.wav")
    f = open("Ojos_azules.wav", 'rb')
    arr.fromfile(f, result.st_size)
    au = os.path.getsize('Ojos_azules.wav')
    tamEnvi=str(au)
    print("Debe enviar " + tamEnvi)
    s.sendall("{}-{}".format(tamEnvi, "a").encode())
    #audio=open(self.archivo, "rb"
    s.sendall(arr)  # Envia audio
    #audio.close()
    print("Enviado...")