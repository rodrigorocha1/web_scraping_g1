from bs4 import BeautifulSoup
import requests

url = 'https://g1.globo.com/rss/g1/sp/ribeirao-preto-franca'

response = requests.get(url)
xml_content = response.text

# Use o parser 'xml' em vez de 'html.parser' para processar XML
soup = BeautifulSoup(xml_content, 'lxml-xml')

print(type(soup))


def abrir_conexao():
    url = 'https://g1.globo.com/rss/g1/sp/ribeirao-preto-franca'
    respose = requests.get(url)
    conteudo_xml = respose.text
    soup = BeautifulSoup(conteudo_xml, 'lxml-xml')
    return soup


soup = abrir_conexao()


def extrair_dados_g1():
    pass


def obter_dados_noticia(soup):
    soup = abrir_conexao()
    itens = soup.find_all('item')
    for noticia in itens:
        titulo = noticia.title.text
        link = noticia.link.text
        data_publicacao = noticia.pubDate.text

        # Pega a descrição em HTML
        descricao_html = noticia.description.text.strip()

        # Usa BeautifulSoup novamente para limpar HTML da descrição
        descricao_limpa = BeautifulSoup(descricao_html, "html.parser").get_text(separator=' ', strip=True)
        print('titulo')
        print(titulo)
        print('link')
        print(link)
        print('descricao')
        print(descricao_limpa)
        print(data_publicacao)

        media_content = noticia.find("media:content")
        url_media = media_content.get('url') if media_content and media_content.has_attr('url') else None
        print(url_media)

        print('=' * 1000)


obter_dados_noticia(soup=soup)
