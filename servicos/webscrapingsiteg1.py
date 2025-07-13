from typing import Generator
from bs4 import BeautifulSoup
from models.noticia import Noticia
from servicos.webscrapingbasebs4 import WebScrapingBs4base
from datetime import datetime


class WebScrapingG1(WebScrapingBs4base):

    def __init__(self, url: str, parse: str):
        super().__init__(url, parse)

    def obter_dados(self, dados: BeautifulSoup) -> Generator[Noticia, None, None]:
        titulo_elem = dados.find('h1', class_='content-head__title')
        titulo = titulo_elem.get_text(strip=True) if titulo_elem else ""

        sub_titulo_elem = dados.find('h2', class_='content-head__subtitle')
        sub_titulo = sub_titulo_elem.get_text(strip=True) if sub_titulo_elem else ""

        data_publi = dados.find('p', class_='content-publication-data__from')
        data_publicacao = None
        if data_publi:
            try:
                data_str = data_publi.text.strip()
                data_publicacao = datetime.strptime(data_str, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                data_publicacao = datetime.now()  # fallback

        texto_noticia_elem = dados.find('div', class_='mc-article-body')
        texto_noticia = texto_noticia_elem.get_text(strip=True) if texto_noticia_elem else ''

        autor_elem = dados.find('p', class_='content-publication-data__from')
        autor = autor_elem.get_text(strip=True) if autor_elem else ''

        noticia = Noticia(
            titulo_noticia=titulo,
            url=self._url,
            descricao_noticia=None,
            data_publicacao=data_publicacao,
            url_imagem=None,
            subtitulo=sub_titulo,
            texto_noticia=texto_noticia,
            autor=autor
        )
        yield noticia


if __name__ == '__main__':
    url = 'https://g1.globo.com/sp/ribeirao-preto-franca/noticia/2025/07/01/homem-morre-atropelado-na-rodovia-abrao-assed-em-serrana-sp.ghtml'

    wsteste = WebScrapingG1(url=url, parse='html.parser')
    dados = wsteste.abrir_conexao()
    for noticia in wsteste.obter_dados(dados=dados):
        print(noticia)
