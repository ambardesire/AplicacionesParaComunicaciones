# Aplicaciones para comunicaciones en red
# Autores:
#         Martell Fuentes Ambar Desirée
#         Mendoza Morales Aldo Daniel

import speech_recognition as sr
from Maquina import *

maquinas = []
main()

def CargarMaquinas():
    maquinas.append( Maquina("Carla", "127.0.0.1", "8001") )
    maquinas.append( Maquina("Matilda", "127.0.0.2", "8002") )
    maquinas.append( Maquina("Maria", "127.0.0.3", "8003") )
    
def MostrarMaquinas():
    for maquina in maquinas:
        maquina.DescripcionMaquina()

def ObtenerMensajeVoz():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        os.system( "clear" )
        MostrarMaquinas()
        print( "Escuchando ")
        audio = r.listen(source)

        try:    
            return r.recognize_google(audio)	
        except Exception as e:
            return ""


def ObtenerMaquina( texto ):
    texto = texto.lower()
    nombres = ["Carla","Matilda","Maria"]   
           
    for nombre in nombres:
       if( nombre.lower() in texto):
        return ["nombre", nombre]
    
    return ""


def main():

    CargarMaquinas()
    MostrarMaquinas()
    
    texto = ObtenerMensajeVoz()
       if (texto != ""):
          destinatario = ObtenerMaquina( texto )
             print("Se enviara a la maquina de:\t" + destinatario + "\n")
              break
                print(texto)
                input( "Intentalo de nuevo. Pulsa enter para continuar ..." )
        else:
            os.system( "clear" )
            MostrarMaquinas()
    os.system( "clear" )
    MostrarMaquinas()

    mensaje = ObtenerMensajeVoz()
	if (mesaje != ""):
             print("Tu mensaje es:\t" + mensaje + "\n")
              break
                input( "Intentalo de nuevo. Pulsa enter para continuar ..." )
        else:
            os.system( "clear" )
            MostrarMaquinas()
    os.system( "clear" )
    MostrarMaquinas()
    
    
   
