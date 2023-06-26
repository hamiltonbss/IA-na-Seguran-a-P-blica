
lista = ['site:*.leg.br', 'site:*.jus.br', 'site:*.mp.br', 'site:*.gov.br', 
         'site:*.gov.br/pf', 'site:*.gov.br/prf', 'site:*.gov.br/mj', 'site:*.gov.br/mcti',
         "site:*.ac.gov.br", "site:*.al.gov.br", "site:*.ap.gov.br", 
         "site:*.am.gov.br", "site:*.ba.gov.br", "site:*.ce.gov.br", "site:*.df.gov.br", "site:*.es.gov.br", "site:*.go.gov.br",
         "site:*.ma.gov.br", "site:*.mt.gov.br", "site:*.ms.gov.br", "site:*.mg.gov.br", "site:*.pa.gov.br", "site:*.pb.gov.br", "site:*.pr.gov.br",
         "site:*.pe.gov.br", "site:*.pi.gov.br", "site:*.rj.gov.br", "site:*.rn.gov.br", "site:*.rs.gov.br", "site:*.ro.gov.br", "site:*.rr.gov.br", 
         "site:*.sc.gov.br", "site:*.sp.gov.br", "site:*.se.gov.br", "site:*.to.gov.br"]


for i in lista:
    Busca_api('dados/termos.csv', i, paginas=10).buscador()

#pip install google-api-python-client
#pip install colorama


import datetime
import time
from googleapiclient import discovery
import pandas as pd
import colorama
import json

# Leitura das chaves de API do arquivo JSON
with open('login_config.json') as json_file:
    data = json.load(json_file)
    my_api_key = data['my_api_key']
    my_cse_id = data['my_cse_id']

tempo = time.time()
timestamp = datetime.datetime.fromtimestamp(tempo).strftime('%d-%m_%H#%M#%S')

class Busca_api():

    def __init__(self, entrada, expressao=None, paginas=None, pag_inicial=None):
        """Essa clase permite que se obtenha resultados de uma busca no google.

            Args:
            entrada (str): arquivo .txt com termos a serem pesquisados
            expressao (str): expressão a ser adicionada em cada pesquisa. Constará no
                nome do arquivo gerado.
            paginas (int): número de páginas a serem buscadas, máximo de 10
            pag_inicial (int): página a partir da qual serão extraídos os resultados"""

        self.termos = []
        self.resultados = []
        self.expressao = expressao
        self.paginas = paginas
        self.total = []
        self.limite = 0

        if pag_inicial:
            self.pag_inicial = pag_inicial - 1
        else:
            self.pag_inicial = 0

        with open(entrada, newline='', encoding='UTF-8') as f:
            termos0 = f.read().splitlines()

        if expressao:
            for i in termos0:
                self.termos.append(f"{i} {expressao}")
        else:
            self.termos = termos0

    def buscador(self):
        service = discovery.build("customsearch", "v1", developerKey=my_api_key)
        id_ini = 1
        n_termo = 1

        try:
            for i in self.termos:
                self.limite = 100 

                for pag in range(self.paginas):
                    id_primeiro = pag
                    pag = pag + self.pag_inicial 
                    time.sleep(1)
                    n_item = 1
                    id_ini = (1**pag)+(pag*10)

                    k = len(str(self.expressao))
                    termo_limpo = i[:-(k+1)]

                    res = service.cse().list(q=i, cx=my_cse_id, start=id_ini).execute()

                    if id_primeiro == 0:
                        cache = []
                        cache.append(termo_limpo)
                        cache.append(self.expressao)
                        total = int(res['searchInformation']['totalResults'])
                        cache.append(total)
                        self.total.append(cache)

                        self.limite = total

                    if 'items' not in res:
                        break

                    print(id_ini)
                    todos = res['items']
                    cache = []

                    for g in todos:

                        if 'title' not in g:
                            title = "Sem título"
                        else:
                            title = g['title']
                            title = " ".join(title.split())
                        link = g['link']
                        if 'snippet' in g:
                            desc = g['snippet']
                            desc = " ".join(desc.split())
                        else:
                            desc = ""

                        cache = []
                        cache.append(termo_limpo)
                        cache.append(self.expressao)
                        cache.append(title)
                        cache.append(link)
                        cache.append(desc)
                        self.resultados.append(cache)

                        num_item = n_item+(id_ini-1)

                        print(f"{colorama.Fore.GREEN}Termo {n_termo}.{num_item} coletado")

                        n_item = n_item + 1

                n_termo = n_termo + 1

        except:
            print(f"{colorama.Fore.RED}ERRO!! {n_termo}.{num_item}")

        finally:
            df = pd.DataFrame(self.resultados)
            df = df.drop_duplicates(subset=3)
            df2 = pd.DataFrame(self.total)

            nome = self.expressao[7:]

           
            df.to_csv(f"dados/{nome.replace('/', '_')}_{timestamp}.csv", sep=';', header=None)
            df2.to_csv(f"dados/{nome.replace('/', '_')}_resultados_{timestamp}.csv", sep=';', header=None)
