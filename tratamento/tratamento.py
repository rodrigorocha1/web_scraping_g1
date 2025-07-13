from bs4 import BeautifulSoup
import re


class Tratamento:

    def limpar_descricao(self, descricao_html: str, parser_html: str):
        """
            Método para limpar o texto da noticia

        Args:
            descricao_html (str): conteúdo do texo HTML da noticia

        Returns:
            str: texto limpo, sem links de whatswapp

        """
        soup_desc = BeautifulSoup(descricao_html, parser_html)

        for img in soup_desc.find_all('img'):
            img.decompose()

        texto_limpo = soup_desc.get_text(separator=' ').strip()

        padroes_a_remover = [
            r'vídeos?.*?(?=\n|$)',
            r'veja\s+mais\s+not[ií]cias.*?(?=\n|$)',
            r'leia\s+mais.*?(?=\n|$)',
            r'receba\s+no\s+whatsapp\s+as\s+not[ií]cias.*?(?=\n|$)',
             r'siga\s+o\s+canal\s+g1\s+ribeir[aã]o\s+e\s+franca\s+no\s+whatsapp[,\.]*\s*',

        ]

        for padrao in padroes_a_remover:
            texto_limpo = re.sub(padrao, '', texto_limpo, flags=re.IGNORECASE)

        # Remove espaços extras e quebras de linha
        texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()

        return texto_limpo
