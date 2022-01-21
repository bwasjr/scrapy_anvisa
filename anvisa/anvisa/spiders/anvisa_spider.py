from urllib import response
import scrapy
import json
import pandas as pd
import traceback
import os
import sys


class AnvisaSpiderSpider(scrapy.Spider):
    name = 'anvisa_spider'
    #allowed_domains = ['consultas.anvisa.gov.br']

    df_leitura = pd.read_excel('BaseDados - Bionexo.xlsx',
                               sheet_name='_SELECT_cnpj_Razão_Social_Nome_')  # lê os registros da primeira aba da planilha

    df_leitura = df_leitura[df_leitura['Tipo de Unidade']
                            == 'Matriz']  # seleciona somente os registros matriz

    # trata o cnpj
    df_leitura['cnpj'] = df_leitura['cnpj'].str.replace(".", "")
    df_leitura['cnpj'] = df_leitura['cnpj'].str.replace("/", "")
    df_leitura['cnpj'] = df_leitura['cnpj'].str.replace("-", "")

    start_urls = [
        f'https://consultas.anvisa.gov.br/api/empresa/{cnpj}' for cnpj in df_leitura['cnpj']]  # define as urls que a aranha vai percorrer

    def parse(self, response):
        try:
            # obtem o response da requisicao
            jsonresponse = json.loads(response.text)
        except Exception as e:
            f = open("exceptions.txt", "a")
            f.write(str(e)+'\n')
            f.close()
            jsonresponse = {'cnpj': 'nao_encontrado',
                            'razaoSocial': 'nao_encontrado'}
        yield{  # gera o json de saída
            'cnpj': jsonresponse["cnpj"],
            'razao_social': jsonresponse["razaoSocial"]
        }
