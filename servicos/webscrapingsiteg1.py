from typing import Generator
from bs4 import BeautifulSoup
import requests
from models.noticia import Noticia
from servicos.webscrapingbasebs4 import WebScrapingBs4base

class WebScrapingG1(WebScrapingBs4base):

    def __init__(self, url: str, parse: str):
        super().__init__(url, parse)

    def obter_dados(self, dados: BeautifulSoup) -> Generator[Noticia, None, None]:
        pass


url = 'https://g1.globo.com/sp/ribeirao-preto-franca/noticia/2025/07/01/homem-morre-atropelado-na-rodovia-abrao-assed-em-serrana-sp.ghtml'

response = requests.get(url=url)
conteudo_texto = response.text
soup = BeautifulSoup(conteudo_texto, 'html.parser')
titulo = soup.find('h1', class_='content-head__title')
sub_titulo = soup.find('h2', class_='content-head__subtitle')
data_publi = soup.find('p', class_='content-publication-data__from')
data_up = soup.find('p', class_='content-publication-data__updated')
texto_noticia = soup.find('div', class_='mc-article-body')

print(texto_noticia.get_text().strip())

# print(titulo.get_text())
# print(sub_titulo.get_text())
# print(data_publi.get_text())
# print(data_up.get_text())
