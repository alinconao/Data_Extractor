import re
import requests
from bs4 import BeautifulSoup

#Web Data Extractor
#Alejandro J. Linconao -> alejandro.jose.linconao@gmail.com
#------------------------------------------
#Graba en un archivo el nombre de la URL y los enlaces encontrados en la misma
#Usa Soup con el html.parser para el texto obtenido
#lee luego el archivo linea por linea

direccion_base = str(input("What url do you want to extract the emails and links from?: "))


#------PARAMETROS------------
enlace_cont = 0
enlace_bruto=""
email_cont  = 0 
cont2 = 0
direccion_txt = ""
archivo_probado = False
sopita1 = ""
salida = ""
salida2 = ""
url = ""
url_ok = False
linea_limpia = ""
linea_pos= 0
linea_limpia_len = 0
#navegadorm es un diccionario CAMBIAR
navegadorm = {"user-agente" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"} 
#------FIN_PARAMETROS------------

#------OBJETOS------------------
class Limpiar_url: 
    #Nota: existe una libreria que limpia las urls es urlparse. No la uso
    def __init__(self, url):
            self.url = url
            self.dire_limpia= ""
            self.url_limpia = ""
            self.url_sola = ""
        
    def correccion_0(self):
               
        self.url = self.url.replace(" ","")
        #Tupla con texto a borrar
        claves=(":", "/", " ")
        for x in range(len(self.url)):
            if self.url[x] not in claves:
                self.url_limpia = self.url_limpia + self.url[x]
        
        if self.url_limpia[0:5] == "https":
            self.url_limpia = self.url_limpia[5:]
            #print("comienza con https")
            #print(self.url_limpia)
        elif self.url_limpia[0:4] == "http":
                self.url_limpia = self.url_limpia[4:]
                #print("comienza con http")
                #print(self.url_limpia)
        else:
            pass
            #print(self.url_limpia)
            #print("no entro")
        #Aca reeemplazo punto por guion para el nombre de archivo
        self.url_arch = self.url_limpia.replace(".","-")
                                                
    #Metodo que valida si tiene o no www
    def correccion_1(self):
        self.dire_limpia = self.url.lower()
        self.dire_limpia = self.dire_limpia.strip()
        #print("Comienza con www?: ", self.dire_limpia.startswith("www" or "WWW"))
        
#------Fin de Objetos------------

#------FUNCIONES------------------
            
def procesar_url(direccion_base):
    global direccion_limpia
    direccion_limpia = direccion_base.lower()
    direccion_limpia = direccion_limpia.strip()
    #print("Comienza con www?: ", direccion_limpia.startswith("www" or "WWW"))
    #print("hay puntos?: ", "." in direccion_limpia)
    direccion_limpia = direccion_limpia.replace(".","-")
    direccion_limpia = direccion_limpia.replace(" ","")
    #print("Dire Limpia1: ", direccion_limpia)
    global solo_url
    solo_url = direccion_limpia.replace("https","")
    #print("Dire Limpia2: ", solo_url)
    solo_url = solo_url.replace("http","")
    #print("Dire Limpia3: ", solo_url)
    return direccion_limpia
    
     
def grabar_resultados(nombrearch, textoagrabar):
    #primero veo si el archivo existe
    global archivo_probado
    if archivo_probado == False:
        try:
            test_file = open(nombrearch, 'rt', encoding='utf-8')
            print("El archivo: ", nombrearch, " Existe. Se procede a Abrirlo")
            #print("Primera Linea: ", test_file.readline())
            #print(test_file.find(nombrearch))
            test_file.close()
            archivo_probado = True
        except:
            print("El archivo: ", nombrearch, " NO Existe Sera Creado")
            archivo_probado = True
            
    if archivo_probado == True:   
    #Grabo el archivo testenando por las dudas.
        try:
            with open(nombrearch, 'at', encoding='utf-8') as file1:
                file1.write(textoagrabar)
                file1.close()
                archivo_probado = True
        except:
            print("Error al abrir el archivo")  
#------FIN_FUNCIONES--------------


#------gestion de nombre de archivo---------
#Validacion de la direccion y adpatacion para el nombre de archivo
#direccion_base  = "https://httpbin.org/"
#   direccion_base = str(input("Ingrese direccion: "))

clase_1 = Limpiar_url(direccion_base)
clase_1.correccion_0()
clase_1.correccion_1()


#Asigno el nombre del archivo
archivo_name = clase_1.url_arch + ".txt"
#------FIN de gestion de nombre de archivo-----

#Validacion de la direccion y adpatacion para el nombre de archivo
#direccion_base  = HERE_URL_FOR_TEST
procesar_url(direccion_base)

archivo_name = clase_1.url_arch + ".txt"


salida = requests.get(direccion_base, headers = navegadorm, timeout = 1)
sopita1 = BeautifulSoup(salida.text, "html.parser")
#Grabo titulo en archivo
grabar_resultados(archivo_name, "**Web** " + str(salida.url) + "\n \n")

#Muestro titulo y datos
print("=" * 20)
print("URL:", str(salida.url))
print("-" * 20)
print("Web Titulo: ", sopita1.title.text)
print("-" * 20)
print("Status:", salida.status_code , "Reason: ", salida.reason)
print("=" * 20)
#Buscar los emails
buscar = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._%+-]+.[a-zA-Z0-9._%+-]"
emailsencontrados = str(re.findall(buscar, salida.text))
#Uso los espacios para separar los emails
emailsencontrados = emailsencontrados.split() 

for emails in emailsencontrados:
    emails_cont = email_cont + 1
    #Save emails in file
    grabar_resultados(archivo_name, "**Emails** " + str(emailsencontrados) + "\n \n +-+-+-+-+\n \n")

#Dont work with "sopita1.find_all('href', recursive = True)"
for enlace in sopita1.find_all('a', recursive = True):
    enlace_bruto = enlace.get('href')
    enlace_cont = enlace_cont + 1
    
    #look if the first character is "/"
    if enlace_bruto[0:1] == "/":
        #se concatena dominio con enlace que comienza con barra quitando esta
        enlace_bruto = str(salida.url) + enlace_bruto[1:] 
            
    #Save in file
    grabar_resultados(archivo_name, "**Enlace** " + str(enlace_cont) + " " + enlace_bruto + "\n \n")


#Read each line in file
print("Imprimo Archivo Linea por linea")
file1 = open(archivo_name, "r", encoding='utf-8')
while(True):
    linea = file1.readline()
    if not linea:
        break
    print(linea.strip())
file1.close()
