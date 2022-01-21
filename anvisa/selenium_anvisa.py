from itertools import count
from operator import index
from time import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd


def instancia_driver():  # INICIALIZACAO do chromedriver
    options = webdriver.ChromeOptions()
    # options.headless = True
    # options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    return driver


# lê o arquivo com os os dados de empresas minerados pela aranha no site da anvisa
df_leitura = pd.read_excel('result.xlsx', sheet_name='Sheet1')

# seleciona somente os registros cujo cnpj foi encontrado no site da anvisa
df_leitura = df_leitura[df_leitura['cnpj'] != 'nao_encontrado']

# cria a flag para indicar se o cnpj foi confirmado como uma empresa de transportes
df_leitura['is_transportes'] = False

lista_encontrados = []


driver = instancia_driver()

for indice in range(len(df_leitura['cnpj'])):
    cnpj = df_leitura['cnpj'].iloc[indice]
    driver.get(
        'https://consultas.anvisa.gov.br/#/empresas/empresas/?cnpj='+cnpj)  # 00676486000182	FEDERAL EXPRESS CORPORATION
    time.sleep(2)
    driver.execute_script("window.stop();")
    driver.find_element(By.XPATH, '//input[@value="Consultar"]').click()
    time.sleep(1)
    try:
        is_transporte = driver.find_element(By.XPATH,
                                            '//div[text() = "Resultado da Consulta de Funcionamento de Empresas"]')
    except:
        is_transporte = None
    if is_transporte != None:  # se é transporte
        lista_encontrados.append(True)  # marca true na lista de encontrados
    else:
        lista_encontrados.append(False)

df_leitura['is_transportes'] = lista_encontrados

# gera o arquivo final
df_leitura.to_excel('result_check.xlsx', index=False)

print('fim da execução')
driver.quit()
