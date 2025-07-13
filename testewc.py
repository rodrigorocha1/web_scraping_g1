from servicos.webscrapingbs4g1rss import WebScrapingBs4G1Rss

wsbase = WebScrapingBs4G1Rss(url='https://g1.globo.com/rss/g1/sp/ribeirao-preto-franca')
dados = wsbase.abrir_conexao()
for notica in wsbase.obter_dados(dados=dados):
    print(notica)
