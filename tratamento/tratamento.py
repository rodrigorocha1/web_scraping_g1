from bs4 import BeautifulSoup
import re

class Tratamento:

    def limpar_descricao(self, descricao_html: str, parser_html: str = "html.parser") -> str:
        """
        Método para limpar o texto da notícia e criar parágrafos a cada ponto.

        Args:
            descricao_html (str): Conteúdo do texto HTML da notícia.
            parser_html (str): Parser a ser usado pelo BeautifulSoup (padrão: html.parser).

        Returns:
            str: Texto limpo, com parágrafos separados por pontos.
        """
        # Cria objeto BeautifulSoup
        soup_desc = BeautifulSoup(descricao_html, parser_html)

        # Remove todas as imagens
        for img in soup_desc.find_all('img'):
            img.decompose()

        # Remove listas relacionadas a "leia também"
        for lista in soup_desc.find_all(['ul', 'ol']):
            if lista.find_previous(string=re.compile(r'leia\s+tamb[eé]m', re.IGNORECASE)):
                lista.decompose()

        # Extrai o texto, mantendo quebras de linha
        texto_limpo = soup_desc.get_text(separator='\n').strip()

        # Padrões a remover
        padroes_a_remover = [
            r'vídeos?.*?(?=\n|$)',
            r'veja\s+mais\s+not[ií]cias.*?(?=\n|$)',
            r'leia\s+mais.*?(?=\n|$)',
            r'leia\s+tamb[eé]m.*?(?=\n|$)',  # <- Remove explicitamente o "leia também"
            r'receba\s+no\s+whatsapp\s+as\s+not[ií]cias.*?(?=\n|$)',
            r'siga\s+o\s+canal\s+g1\s+ribeir[aã]o\s+e\s+franca\s+no\s+whatsapp[,\.]*\s*',
            r'✅\s*clique\s*aqui\s*para\s*seguir\s*o\s*canal\s*do\s*g1\s*ribeir[aã]o\s*e\s*franca\s*no\s*whatsapp[,\.]*\s*',
            r'veja\s+mais\s+not[ií]cias\s+da\s+regi[aã]o\s+no\s+g1\s+ribeir[aã]o\s*e\s*franca.*?(?=\n|$)',
            r'vídeos:\s*tudo\s+sobre\s+ribeir[aã]o\s+preto,\s+franca\s+e\s+regi[aã]o.*?(?=\n|$)'
        ]

        # Remove os padrões detectados
        for padrao in padroes_a_remover:
            texto_limpo = re.sub(padrao, '', texto_limpo, flags=re.IGNORECASE)

        # Remove espaços e quebras de linha excessivas
        texto_limpo = re.sub(r'\n+', '\n', texto_limpo)
        texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()

        # Divide o texto em parágrafos a cada ponto final
        paragrafos = [p.strip() for p in texto_limpo.split('.') if p.strip()]
        texto_formatado = '\n\n'.join([p + '.' for p in paragrafos])

        return texto_formatado
