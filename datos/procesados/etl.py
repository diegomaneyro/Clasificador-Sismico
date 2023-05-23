# importar libreias necesarias
from selenium import webdriver
import pandas as pd
import time
from bs4 import BeautifulSoup
import requests
import io

<<<<<<< HEAD
class Extraccion_Url:
    def __init__(self,url,navegador):
=======
>>>>>>> 35c93f49c468f0703a00b9d42f22b6823f06ff4b

class Extraccion_Url:
    def __init__(self, url, navegador):
        '''
        Este código utiliza Selenium para abrir la página web especificada en la variable url y esperar a que se cargue la tabla dinámica.
        Luego, se extrae el código HTML de la página y se usa BeautifulSoup y pandas para extraer la tabla y guardarla en un DataFrame
        '''
        # Url de Agencia Meteorologia de japon. Información de Terremotos dinamica
        self.url = url
        
        # Configura el driver de Selenium 
        
        if navegador == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument('--headless') # Ejecuta el navegador en modo headless (sin interfaz gráfica)
            driver = webdriver.Chrome(options=options)
        elif navegador == 'firefox':
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless') # Ejecuta el navegador en modo headless (sin interfaz gráfica)
            driver = webdriver.Firefox(options=options)
        elif navegador == 'edge':
            options = webdriver.EdgeOptions()
            options.add_argument('--headless') # Ejecuta el navegador en modo headless (sin interfaz gráfica)
            driver = webdriver.Edge(options=options)



        # Abre la página web con Selenium
        driver.get(self.url)

# Espera a que se cargue la tabla dinámica (ajusta el tiempo según sea necesario)
time.sleep(5)

# Extrae el código HTML de la página
html = driver.page_source

# Usa BeautifulSoup y pandas para extraer la tabla
soup = BeautifulSoup(html, 'html.parser')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))[0]
print('Descarga exitosa')
# Cierra el driver de Selenium
driver.quit()
df.to_csv('JapanMeteorologicalAgency.csv', index=False)
print('Creacion de archivo csv finalizado')

# query info Science for a changing world EEUU
#realizar consulta formato csv ultimos datos
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&endtime=now'
response = requests.get(url)
df = pd.read_csv(io.StringIO(response.text))
# enviar a csv
df.to_csv('ScienceForChangingWorld.csv', index=False)
print('Creacion de archivo csv finalizado')