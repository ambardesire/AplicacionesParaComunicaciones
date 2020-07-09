# Aplicaciones para comunicaciones en red
# Autores:
#         Martell Fuentes Ambar Desirée
#         Mendoza Morales Aldo Daniel
import socket
import pickle
import os
import datetime
import threading
import sys
import speech_recognition as sr
import pyaudio
import wave
from Personaje import *
from os import path
from array import array
from os import stat

personajes = []
BUFFER_SIZE = 1024
HOST, PORT = sys.argv[1:3]
archivo="entrada.wav"

def CargarPersonajes():
    personajes.append( Personaje("Carla", "Negro", "Cafes", "Blanca", "Nada", "Mujer") )
    personajes.append( Personaje("Matilda", "Rubio", "Azules", "Morena", "Nada", "Mujer") )
    personajes.append( Personaje("Maria", "Rubio", "Azules", "Blanca", "Lentes", "Mujer") )
    personajes.append( Personaje("Samuel", "Negro", "Cafes", "Morena", "Nada", "Hombre") )
    personajes.append( Personaje("Eduardo", "Negro", "Azules", "Blanca", "Sombrero", "Hombre") )
    personajes.append( Personaje("Bob", "Rubio", "Azules", "Blanca", "Corbata", "Hombre") )
    personajes.append( Personaje("Patricio", "Rojo", "Cafes", "Morena", "Nada", "Hombre") )
    personajes.append( Personaje("Jorge", "Rubio", "Verdes", "Morena", "Sombrero", "Hombre") )
    personajes.append( Personaje("Jessica", "Rojo", "Verdes", "Blanca", "Nada", "Mujer") )
    personajes.append( Personaje("Camila", "Negro", "Cafes", "Morena", "Lentes", "Mujer") )
    personajes.append( Personaje("Paulina", "Rojo", "Azules", "Morena", "Sombrero", "Mujer") )

def MostrarPersonajes():
    for personaje in personajes:
        personaje.DescripcionPersonaje()

def ObtenerMensajeVoz():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        os.system( "clear" )
        MostrarPersonajes()
        MostrarTiros(tiros_anteriores)
        print( "Es tu turno de adivinar el personaje\nEscuchando ... ")
        audio = r.listen(source)

        try:    
            return r.recognize_google(audio)	
        except Exception as e:
            return ""

def ObtenerCaracteristica( texto ):
    texto = texto.lower()
    accesorios = ["nada", "lentes", "sombrero", "corbata"] # "tu personaje tiene <accesorio>"
    nombres = ["Carla","Matilda","Maria","Samuel","Eduardo","Bob","Patricio","Jorge","Jessica", "Camila", "Paulina"] #"tu personaje es <genero_nombre>"
    generos = ["mujer", "hombre"]

    caracteristicas = [" ojo", " cabello", " piel", " genero"]
    
    i = 0
    for caracteristica in caracteristicas:
        if( caracteristica in texto):
            t = texto.split( caracteristica )
            color = t[1].split(" ")
            if( i == 0):
                caracteristica = caracteristica + "s"
            response = [caracteristica.replace(" ",""), color[1]]
            return response

        i = i + 1
    
    if( "tiene" in texto):
        t = texto.split("tiene")
        acc = t[1]
        for accesorio in accesorios:           
            if( accesorio in acc):
             return ["accesorio", accesorio]             
        return ["accesorio", "nada"]
    else:
        for genero in generos:
            if( genero in texto):
                return ["genero", genero]
        
        for nombre in nombres:
            if( nombre.lower() in texto):
                return ["nombre", nombre]
    return ""

def MostrarTiros(tiros):
    if(len(tiros) > 0):
        print( "\tTiros hasta el momento: ")
        for tiro in tiros:
            print( "\t\t" + tiro[0] + " " + tiro[1] + ": " + tiro[2] )

def ObtenerAudio():
    FORMAT=pyaudio.paInt16
    CHANNELS=2
    RATE=44100
    CHUNK=1024
    duracion=7 #duracion de la grabacion 7 segundos
 
    #Iniciamos pyaudio
    audio=pyaudio.PyAudio()

    stream=audio.open(format=FORMAT, channels=CHANNELS,
                       rate=RATE, input=True,
                       frames_per_buffer=CHUNK)
    #Inicia grabación
    print("Escuchando...")
    frames=[]

    for i in range(0, int(RATE/CHUNK*duracion)):
        data=stream.read(CHUNK)
        frames.append(data)
    print("Terminando de escuchar")
  
    #Deteniendo grabación
    stream.stop_stream()
    stream.close()
    audio.terminate()
  
    #Creamos el archivo de audio
    waveFile = wave.open(archivo, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

if len(sys.argv) != 3:
    print( "usage:", sys.argv[0], "<host> <port>" )
    sys.exit(1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:    
    TCPClientSocket.connect((HOST, int(PORT) ))

    CargarPersonajes()

    while(True):
        jugadoresFaltantes = TCPClientSocket.recv(100)
        os.system( "clear" )
        if(  jugadoresFaltantes.decode() == "0"):
            print( "Todos los jugadores se han unido ..." )
            break
        else:
            print( "Esperando a " + jugadoresFaltantes.decode() + " jugadores ..." )
    
    tiros_anteriores = []
    
    while(True):
        print( "Esperando datos del servidor" )
        dato = pickle.loads( TCPClientSocket.recv(BUFFER_SIZE) ) # [MI_TURNO?, QUIEN_TIENE_TURNO, TIRO_ANTERIOR, JUEGO_TERMINADO, RESULTADO, PERSONAJE]

        if ( dato[3] ):
            break
        
        if( dato[2] != ""):
            tiros_anteriores = dato[2]
        
        if( dato[0] ):
            #while(True):
            res = ObtenerAudio()
            arr = array('B')
            result = stat("entrada.wav")
            f = open("entrada.wav", 'rb')
            arr.fromfile(f, result.st_size)
            au = os.path.getsize('entrada.wav')
            tamEnvi=str(au)
            print("Enviando...")
            TCPClientSocket.sendall("{}-{}".format(tamEnvi, "a").encode())
            TCPClientSocket.sendall(arr)  
            resultado = TCPClientSocket.recv(BUFFER_SIZE)
                # if (texto != ""):
                #     tiroCliente = ObtenerCaracteristica( texto )
                #     if( tiroCliente != ""):
                #         TCPClientSocket.sendall( pickle.dumps(tiroCliente) )
                #         resultado = TCPClientSocket.recv(BUFFER_SIZE)
                #         break
                # print(texto)
                # input( "Intentalo de nuevo. Pulsa enter para continuar ..." )
        else:
            os.system( "clear" )
            MostrarPersonajes()
            MostrarTiros(tiros_anteriores)
            print( "Esperando a que el jugador " + str(dato[1]) + " termine su turno." )
    os.system( "clear" )
    MostrarPersonajes()
    print( "El personaje era: " + dato[5] )
    print( dato[4] )
