import os
import speech_recognition as sr
import sys
import time
from Maquina import *
from MyOwnPeer2PeerNode import MyOwnPeer2PeerNode

maquinas = []
NOMBRE = 0
IP = 1
PUERTO = 2

def CargarMaquinas():
    maquinas.append( Maquina("Carla", "127.0.0.1", "8001") )
    maquinas.append( Maquina("Lalo", "127.0.0.1", "8002") )
    maquinas.append( Maquina("Maria", "127.0.0.1", "8003") )
    
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
        print( "Escuchando\n")
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
        input( "El usuario no se ha encontrado, intentalo de nuevo. Pulsa enter para continuar ...\n" )
    return destinatario.nombre, mensaje

def main():
    maria = MyOwnPeer2PeerNode("127.0.0.1", 8003)
    time.sleep(1)

    maria.start()
    print("Conectando ...\n")
    time.sleep(5)

    while(True):
        os.system("clear")
        CargarMaquinas()
        destino, mns = EnviarMensaje()
        
        if("Carla" in destino):
            print("Conectando con Carla\n")
            maria.connect_with_node('127.0.0.1', 8001)
            time.sleep(2)
            print("Enviando mensaje a " + destino + "\n")
            maria.send_to_nodes( "Maria: " + mns )
            time.sleep(5) #Menu de ciclos de la aplicacion

            opc = input("Quieres enviar otro mensaje? S/n\n")
        if("Lalo" in destino):
            print("Conectando con Lalo\n")
            maria.connect_with_node('127.0.0.1', 8002)
            time.sleep(2)
            print("Enviando mensaje a " + destino + "\n")
            maria.send_to_nodes( "Maria: " + mns )
            time.sleep(5) #Menu de ciclos de la aplicacion
            
            opc = input("Quieres enviar otro mensaje? S/n\n")

            if(opc.lower() == "n"):
                break
        else:
            input("Presiona enter para intentarlo de nuevo\n\n")

    maria.stop()

main()
