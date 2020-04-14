import logging
import threading
import time
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-2s) %(message)s')
class Taller(object):
    def __init__(self, start=0):
        self.condicionMangasMAX = threading.Condition()
        self.condicionMangasMIN = threading.Condition()
        self.condicionCuerposMAX = threading.Condition()
        self.condicionCuerposMIN = threading.Condition()        
        self.TotalMangas = 0
        self.TotalCuerpos = 0
        self.mangas = 0
        self.cuerpos = 0
        self.prenda = 0 #prenda

    def incrementarManga(self):
        with self.condicionMangasMAX:
            if self.mangas >= 10:
                logging.debug("No hay espacio para mangas")
                self.condicionMangasMAX.wait()
            else:
                self.mangas += 1
                self.TotalMangas += 1
                logging.debug("Manga creada, mangas=%s",self.mangas)

        with self.condicionMangasMIN:
            if self.mangas >= 2:
                logging.debug("Existen suficientes mangas")
                self.condicionMangasMIN.notify()

    def decrementarManga(self):
        with self.condicionMangasMIN:
            while not self.mangas>=2:
                logging.debug("Esperando mangas%s",self.mangas)
                self.condicionMangasMIN.wait()
            self.mangas -= 2
            logging.debug("Mangas tomadas, mangas=%s",self.mangas)
        with self.condicionMangasMAX:
            logging.debug("Hay espacio para mangas")
            self.condicionMangasMAX.notify()
    
    def getMangas(self):
        return (self.TotalMangas)
    
    def incrementarPrenda(self):
        self.prenda += 1

    def getPrendas(self):
        return (self.prenda)   

    def incrementarCuerpo(self):
	#Verifica que la cesta de cuerpos no esté llena
	 with self.condicionCuerposMAX:
            if self.cuerpos >= 5:
                logging.debug("No hay espacio para Cuerpos")
                self.condicionCuerposMAX.wait()
            else:
                self.cuerpos += 1
                self.TotalCuerpos += 1
                logging.debug("Cuerpo creado, cuerpos=%s",self.cuerpos)
	#Notifica que existe más de un cuerpo en la cesta
        with self.condicionCuerposMIN:
            if self.cuerpos >= 1:
                logging.debug("Existen suficientes cuerpos")
                self.condicionCuerposMIN.notify()

    def decrementarCuerpo(self):
        with self.condicionCuerposMIN:
            while not self.cuerpos>=1:
                logging.debug("Esperando cuerpos")
                self.condicionCuerposMIN.wait()
            self.cuerpos -= 1
            logging.debug("Cuerpo tomado, cuerpos=%s",self.cuerpos)
        with self.condicionCuerposMAX:
            logging.debug("Hay espacio para cuerpos")
            self.condicionCuerposMAX.notify()

    def getCuerpos(self):
        return (self.TotalCuerpos)

def crearManga(Taller):
    while (Taller.getMangas() < 10):
        Taller.incrementarManga()
        time.sleep(2)
    logging.debug("Salir  = %s",Taller.getMangas())

def crearCuerpo(Taller):
    while (Taller.getCuerpos() < 5):
        #incrementarCuerpo (antes de decrementar
        #manga se debe validar que haya cupo en
        #la canasta de cuerpos)
        Taller.incrementarCuerpo()
        #Taller.decrementarManga()
        time.sleep(1)
    logging.debug("Salir cuerpo = %s",Taller.getCuerpos())

def ensamblaPrenda(Taller):
    while (Taller.getPrendas() < 5):
        logging.debug("Ensamblando todo")
	Taller.decrementarManga()
        Taller.decrementarCuerpo()
        	time.sleep(3)
        Taller.incrementarPrenda()
       	logging.debug("Total de prendas ensambladas = %s", Taller.getPrendas())
    	logging.debug("Total de mangas creadas = %s", Taller.getMangas())
	logging.debug("Total de cuerpos creados = %s", Taller.getCuerpos())
    	
taller = Taller()
Lupita = threading.Thread(name='Lupita(mangas)', target=crearManga, args=(taller,))
Sofia = threading.Thread(name='Sofía(cuerpos)', target=crearCuerpo, args=(taller,))
persona3 = threading.Thread(name='persona(ensamble)', target=ensamblaPrenda,args=(taller,))
Lupita.start()
Sofia.start()
persona3.start()
Lupita.join()
Sofia.join()
persona3.join()
