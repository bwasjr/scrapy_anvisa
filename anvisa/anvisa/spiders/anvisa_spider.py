from urllib import response
import scrapy
import json
import pandas as pd


class AnvisaSpiderSpider(scrapy.Spider):
    name = 'anvisa_spider'
    #allowed_domains = ['consultas.anvisa.gov.br']

    df_leitura = pd.read_excel('BaseDados - Bionexo.xlsx',
                               sheet_name='_SELECT_cnpj_Razão_Social_Nome_')  # lê os registros da primeira aba da planilha

    df_leitura = df_leitura[df_leitura['Tipo de Unidade']
                            == 'Matriz']  # seleciona somente os registros matriz

    df_leitura['cnpj'] = df_leitura['cnpj'].str.replace(".", "")
    df_leitura['cnpj'] = df_leitura['cnpj'].str.replace("/", "")
    df_leitura['cnpj'] = df_leitura['cnpj'].str.replace("-", "")

    start_urls = [
        f'https://consultas.anvisa.gov.br/api/empresa/{cnpj}' for cnpj in df_leitura['cnpj']]

    def parse(self, response):
        jsonresponse = json.loads(response.text)

        cnpj = jsonresponse["cnpj"]
        razao_social = jsonresponse["razaoSocial"]

        yield{
            'cnpj': cnpj,
            'razao_social': razao_social
        }
