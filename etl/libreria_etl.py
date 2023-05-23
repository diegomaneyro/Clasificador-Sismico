import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import io
import seaborn as sns
import numpy as np
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Extraccion_Url:
    def __init__(self,pais,navegador):

        if pais=='chile':
            self.url = 'http://ds.iris.edu/ieb/index.html?format=text&nodata=404&starttime=1970-01-01&endtime=2025-01-01&orderby=time-desc&src=usgs&limit=5000&maxlat=-17.411&minlat=-56.811&maxlon=-67.223&minlon=-79.528&sbl=1&pbl=1&caller=self&zm=3&mt=ter'
        elif pais=='japon':
            self.url = 'http://ds.iris.edu/ieb/index.html?format=text&nodata=404&starttime=2021-05-06&endtime=2025-01-01&orderby=time-desc&src=usgs&limit=5000&maxlat=56.000&minlat=22.000&maxlon=159.000&minlon=127.000&sbl=1&pbl=1&caller=self&name=Japan%20Region&zm=4&mt=ter'
        elif pais == 'estados unidos':
            self.url= 'http://ds.iris.edu/ieb/index.html?format=text&nodata=404&starttime=1970-01-01&endtime=2025-01-01&orderby=time-desc&src=usgs&limit=5000&maxlat=49.655&minlat=25.227&maxlon=-59.489&minlon=-127.516&sbl=1&pbl=1&caller=self&zm=3&mt=ter'
        ''' 
        Este código utiliza Selenium para abrir la página web especificada en la variable url y esperar a que se cargue la tabla dinámica.
        Luego, se extrae el código HTML de la página y se usa BeautifulSoup y pandas para extraer la tabla y guardarla en un DataFrame
        '''
        # Url de Agencia Meteorologia de japon. Información de Terremotos dinamica
        
        
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
        time.sleep(10)
        
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a.links ga-click'.replace(' ', '.')))).click()
                                            
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#end_checkbox'.replace(' ', '.')))).click()
                                        
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[6]/div[1]/form/div[5]/div[1]/a'.replace(' ', '.')))).click()
                                    
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#mag_all_checkbox'.replace(' ', '.')))).click()
                                        
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#mag_min_text'))).send_keys('5')
                                        
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button#apply_button'))).click()
                                    
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[6]/div[2]/div[5]/div[1]/a'))).click()
                                            
        driver.switch_to.window(driver.window_handles[1])

        driver.current_url

        time.sleep(8)

        html = driver.page_source

        # Usa BeautifulSoup y pandas para extraer la tabla
        soup = BeautifulSoup(html, 'html.parser')
        time.sleep(8)
        table = soup.find_all('table')[0]

        self.df = pd.read_html(str(table))[0]
        time.sleep(6)


        # Cierra el driver de Selenium
        driver.quit()

    def informacion_6_datos(self,p=None):
        
        if p==1: 
            print('Visualizar Data Frame.')
            return self.df.head(5)
        elif p==2:
            print('Tamaño del Data Frame.')
            return self.df.shape
        elif p==3:
            print('Resumen estadistico del Data Frame.')
            return self.df.describe()
        elif p==4:
            print('Hallar valores nulos en el Data Frame.')
            return self.df.isnull().sum()
        elif p==5:
            print('Informacion sobre el tipo de datos y cantidad de valores no nulos del Data Frame.')
            return self.df.info()
        elif p==6:
            print('Resumen estadistico del Data Frame que excluye los numeros.')
            return self.df.describe(exclude='number')
        elif p==None:
            print('(1)Visualizar Data Frame.')
            print('(2)Tamaño del Data Frame.')
            print('(3)Resumen estadistico del Data Frame.')
            print('(4)Hallar valores nulos en el Data Frame.')
            print('(5)Informacion sobre el tipo de datos y cantidad de valores no nulos del Data Frame.')
            print('(6)Resumen estadistico del Data Frame que excluye los numeros.')

            return

        




"""class Extraccion_Url:
    def __init__(self,url,navegador):

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
        self.df = pd.read_html(str(table))[0]
        
        
        # Cierra el driver de Selenium
        driver.quit()

        
    def informacion_6_datos(self,p=None):
        

        if p==1: 
            print('Visualizar Data Frame.')
            return self.df.head(5)
        elif p==2:
            print('Tamaño del Data Frame.')
            return self.df.shape
        elif p==3:
            print('Resumen estadistico del Data Frame.')
            return self.df.describe()
        elif p==4:
            print('Hallar valores nulos en el Data Frame.')
            return self.df.isnull().sum()
        elif p==5:
            print('Informacion sobre el tipo de datos y cantidad de valores no nulos del Data Frame.')
            return self.df.info()
        elif p==6:
            print('Resumen estadistico del Data Frame que excluye los numeros.')
            return self.df.describe(exclude='number')
        elif p==None:
            print('(1)Visualizar Data Frame.')
            print('(2)Tamaño del Data Frame.')
            print('(3)Resumen estadistico del Data Frame.')
            print('(4)Hallar valores nulos en el Data Frame.')
            print('(5)Informacion sobre el tipo de datos y cantidad de valores no nulos del Data Frame.')
            print('(6)Resumen estadistico del Data Frame que excluye los numeros.')

            return
            
        
        

    def matriz_correlacion(self,pais,variables):
        print('grafico para ver la relación entre las variable')
        # Seleccionar las columnas a incluir en la matriz de correlación
        cols = variables

        # Crear la matriz de correlación
        corr = self.df[cols].corr()

        # Crear el gráfico de correlación utilizando la biblioteca Seaborn
        sns.set(style="white")
        mask = np.triu(np.ones_like(corr, dtype=np.bool_))
        fig, ax = plt.subplots(figsize=(10, 8))
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
        square=True, linewidths=.5, cbar_kws={"shrink": .5})
        plt.title('Matriz de correlación de los datos de sismos en '+pais)
        return plt.show()"""