from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

url = 'https://g1.globo.com/rss/g1/sp/ribeirao-preto-franca'

# extração rss
response = requests.get(url)
xml_content = response.text

# Use o parser 'xml' em vez de 'html.parser' para processar XML
soup = BeautifulSoup(xml_content, 'lxml-xml')

print(type(soup))


def abrir_conexao():
    url = 'https://g1.globo.com/rss/g1/sp/ribeirao-preto-franca'
    respose = requests.get(url)
    conteudo_xml = respose.content

    soup = BeautifulSoup(conteudo_xml, 'xml')

    return soup


soup = abrir_conexao()


def extrair_dados_g1():
    pass


def limpar_descricao(descricao_html):
    # Faz um soup para manipular a descrição em HTML
    soup_desc = BeautifulSoup(descricao_html, 'html.parser')

    # Remove a tag <img>
    for img in soup_desc.find_all('img'):
        img.decompose()

    texto_limpo = soup_desc.get_text(separator=' ').strip()

    # Remove frases específicas usando regex (ignore case)
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


def obter_dados_noticia(soup):
    formato_entrada = "%a, %d %b %Y %H:%M:%S %z"

    for noticia in soup.find_all('item'):
        print(noticia.title.text)
        print(noticia.guid.text)
        descricao_html = noticia.description.text

        descricao_limpa = limpar_descricao(descricao_html)
        print(descricao_limpa)

        media_content_tag = noticia.find('media:content')
        media_content = media_content_tag['url'] if media_content_tag else None
        print(media_content)
        data = noticia.pubDate.text
        data = datetime.strptime(data, formato_entrada)
        data = data.strftime("%d-%m-%Y %H:%M:%S")
        print(data)
        print('=' * 100)


obter_dados_noticia(soup=soup)
