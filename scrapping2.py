import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Columnas del dataset a construir
columnas = [
    'Categ de trabajos',
    'Nombre de trabajo',
    'Compania',
    'Salario',
    'Categoria',
    'Subcategoria',
    'Localidad',
    'Activo desde',
    'Jornada',
    'Tipo de contrato',
]

# Creando el dataframe
jobs = pd.DataFrame(columns=columnas)

driver = webdriver.Firefox(executable_path="C:/Users/edjav/Desktop/Ultimo semestre/Introduccion al Data Science/PROYECTO/recoleccion data/geckodriver.exe")
driver.get("https://www.mipleo.com.ec/ofertas-de-trabajo/?q=")
time.sleep(5)


#Seleccionar categoria de trabajos
categoria_de_trabajos = []
ctg_jobs = driver.find_elements_by_xpath('//select[@id="category"]/option')
for i in ctg_jobs:
    trabajo = i.text
    categoria_de_trabajos.append(trabajo)


#Navegacion por paginacion
paginacion = []
pages = driver.find_elements_by_xpath('//div[@id="pages"]/a')
for i in pages:
    pagina = i.text
    paginacion.append(pagina)


#Recoleccion de datos
count = 0
for i in range(2,len(categoria_de_trabajos)+1):
    itemCat = driver.find_element_by_xpath('//select[@id="category"]/option[{}]'.format(i)).click()
    time.sleep(5)

    #Verifica el numero de card job en la pagina actual
    numeroTrabajos = []
    numCardJobs = driver.find_elements_by_xpath('//div[@class="item_list"]')
    for j in numCardJobs:
        carta = j.text
        numeroTrabajos.append(carta)

    # Entra a cada card job para adquirir los datos que se necesitan
    for k in range(len(numeroTrabajos)):
        cardJob = driver.find_element_by_xpath('//div[@class="item_list"][{}]/div/span[@class="titleAd"]/a'.format(k+1)).click()
        time.sleep(5)

        try:
            nombreTrabajo = driver.find_element_by_xpath('//div[@class="header_item"]/h1').text
            compania = driver.find_element_by_xpath('//div[@class="box"][1]/span').text
            salario = driver.find_element_by_xpath('//ul[@class="info_item"]/li[1]/b').text
            categoria = driver.find_element_by_xpath('//ul[@class="info_item"]/li[2]/b').text
            subcategoria = driver.find_element_by_xpath('//ul[@class="info_item"]/li[3]/b').text
            localidad = driver.find_element_by_xpath('//ul[@class="info_item"]/li[4]/b').text
            activo_desde = driver.find_element_by_xpath('//ul[@class="info_item"]/li[5]/b').text
            jornada = driver.find_element_by_xpath('//ul[@class="info_item"]/li[6]/b').text
            tipoContrato = driver.find_element_by_xpath('//ul[@class="info_item"]/li[7]/b').text
            #fechaContrat = driver.find_element_by_xpath('//ul[@class="info_item"]/li[8]/b').text
            #cantidadVacantes = driver.find_element_by_xpath('//ul[@class="info_item"]/li[9]/b').text
            
        except:
            pass
        
        #Colocando los datos como registro en el dataframe
        jobs.loc[count] = [categoria_de_trabajos[i-1], nombreTrabajo, compania, salario, categoria, subcategoria, localidad, activo_desde, jornada, tipoContrato]
        count = count + 1
        driver.back()
        time.sleep(5)

#Creando el csv luego de scrapear lo indicado en el codigo de arriba
jobs.to_csv('analyst3.csv')

time.sleep(2)
driver.close()



