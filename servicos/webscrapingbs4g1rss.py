from typing import Generator
from models.noticia import Noticia
from servicos.webscrapingbasebs4 import WebScrapingBs4base
from bs4 import BeautifulSoup, Tag
import re
from datetime import datetime


class WebScrapingBs4G1Rss(WebScrapingBs4base):

    def __init__(self, url):

        super().__init__(url=url, parse='xml')
        self.__parser_html = 'html.parser'
        self.__formatado_data_entrada = "%a, %d %b %Y %H:%M:%S %z"

    def _limpar_descricao(self, descricao_html: str):
        """
            Método para limpar o texto da noticia

        Args:
            descricao_html (str): conteúdo do texo HTML da noticia

        Returns:
            str: texto limpo, sem links de whatswapp

        """
        soup_desc = BeautifulSoup(descricao_html, self.__parser_html)

        for img in soup_desc.find_all('img'):
            img.decompose()

        texto_limpo = soup_desc.get_text(separator=' ').strip()

        padroes_a_remover = [
            r'vídeos?.*?(?=\n|$)',
            r'veja\s+mais\s+not[ií]cias.*?(?=\n|$)',
            r'leia\s+mais.*?(?=\n|$)',
            r'receba\s+no\s+whatsapp\s+as\s+not[ií]cias.*?(?=\n|$)',
            r'siga\s+o\s+canal\s+g1\s+ribeir[aã]o\s+e\s+franca\s+no\s+whatsapp.*?(?=\n|$)'

        ]

        for padrao in padroes_a_remover:
            texto_limpo = re.sub(padrao, '', texto_limpo, flags=re.IGNORECASE)

        # Remove espaços extras e quebras de linha
        texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()

        return texto_limpo

    def obter_dados(self, dados: BeautifulSoup) -> Generator[Noticia, None, None]:
        """
            Método para obter os dados

        Args:
            dados (BeautifulSoup): conteúdo da noticia em xml

        Yields:
            Generator[Noticia, None, None]: Gera objetos Noticia extraídos do feed RSS.

        """
        for noticia in dados.find_all('item'):
            if not isinstance(noticia, Tag):
                continue
            titulo_noticia_tag = noticia.find('title')
            titulo_noticia = titulo_noticia_tag.text.strip() \
                if titulo_noticia_tag and isinstance(titulo_noticia_tag, Tag) \
                else ""

            descricao_html = noticia.find('description')
            descricao_noticia = self._limpar_descricao(descricao_html.text) \
                if descricao_html \
                else ""

            media_content_tag = noticia.find('media:content')
            url_imagem = str(media_content_tag['url']) \
                if (isinstance(media_content_tag, Tag) and 'url' in media_content_tag.attrs) \
                else ''

            url_tag = noticia.find('guid')
            url = url_tag.text.strip() if url_tag and isinstance(url_tag, Tag) else ''

            data_pub_tag = noticia.find('pubDate')
            data_publicacao = data_pub_tag.text if isinstance(data_pub_tag, Tag) else ''
            data_publicacao = datetime.strptime(data_publicacao, self.__formatado_data_entrada)
            data_publicacao = data_publicacao.strftime("%d-%m-%Y %H:%M:%S")
            data_publicacao = datetime.strptime(data_publicacao, "%d-%m-%Y %H:%M:%S")

            notica = Noticia(
                titulo_noticia=titulo_noticia,
                descricao_noticia=descricao_noticia,
                url=url,
                url_imagem=url_imagem,
                data_publicacao=data_publicacao
            )

            yield notica


if __name__ == '__main__':
    wsbs4 = WebScrapingBs4G1Rss(url='https://g1.globo.com/rss/g1/sp/ribeirao-preto-franca')

    dados = wsbs4.abrir_conexao()

    for noticia in wsbs4.obter_dados(dados=dados):
        print(noticia)
