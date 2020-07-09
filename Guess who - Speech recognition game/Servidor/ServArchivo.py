import socket
import pickle
from os import path

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind(("127.0.0.1", int(8500)))
    s.listen(1)
    conn, addr = s.accept()
    print("Conectado a ", addr)

    print("Esperando audio")
    f=open("respuesta.wav", "wb")     # Se crea un archivo de audio donde se guardará el archivo
    # Si hay datos a recibir, seguir escribiendo
    dato=conn.recv(8).decode()
    dato = dato.split('-')
    tamReciv=int(dato[0])
    datoAud=bytearray()

    #datoAud=conn.recv(tamReciv)

    while len(datoAud) < tamReciv:
        packet = conn.recv(tamReciv-len(datoAud))
        if not packet:
            break
        datoAud.extend(packet)
    f.write(datoAud)
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "respuesta.wav")
    print("archivo generado")