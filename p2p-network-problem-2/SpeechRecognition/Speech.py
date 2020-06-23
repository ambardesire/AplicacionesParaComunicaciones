# Aplicaciones para comunicaciones en red
# Autores:
#         Martell Fuentes Ambar Desirée
#         Mendoza Morales Aldo Daniel

import os
import speech_recognition as sr
from Maquina import *

maquinas = []
NOMBRE = 0
IP = 1
PUERTO = 2

def CargarMaquinas():
    maquinas.append( Maquina("Carla", "127.0.0.1", "8001") )
    maquinas.append( Maquina("Matilda", "127.0.0.2", "8002") )
    maquinas.append( Maquina("Maria", "127.0.0.3", "8003") )
    
def MostrarMaquinas():
    for maquina in maquinas:
        maquina.DescripcionMaquina()

def ObtenerMensajeVoz( mensaje ):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        
        os.system( "clear" )
        MostrarMaquinas()
        
        print( mensaje )
        print( "Escuchando ")
        audio = r.listen(source)

        try:
            return r.recognize_google(audio)	
        except Exception as e:
            return ""


def ObtenerMaquina( texto ):
    texto = texto.lower()

    for maquina in maquinas:
       if( maquina.nombre.lower() in texto):
            return maquina
    
    return ""

def EnviarMensaje():
    while(True):
        os.system( "clear" )
        
        texto = ObtenerMensajeVoz("A quien le enviaras el mensaje?")
        if (texto != ""):
            destinatario = ObtenerMaquina( texto.lower() )         
            if(destinatario != ""):
                while(True):
                    os.system( "clear" )
                    print("Se enviara un mensaje a: \t" + destinatario.nombre + "\n")
                    mensaje = ObtenerMensajeVoz("Cual es tu mensaje?")
                    if (mensaje != ""):
                        print("Tu mensaje es: \t" + mensaje + "\n")
                        break
                    else:
                        input( "Intentalo de nuevo. Pulsa enter para continuar ..." )
                break
        input( "El usuario no se ha encontrado, intentalo de nuevo. Pulsa enter para continuar ..." )
def main():
    CargarMaquinas()
    EnviarMensaje()

main()
