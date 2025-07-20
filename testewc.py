from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

from models.noticia import Noticia
from datetime import datetime

noticia_exemplo = Noticia(
    titulo="Tecnologia Revoluciona o Mercado em 2025",
    subtitulo="Inovações disruptivas transformam indústrias ao redor do mundo",
    texto=(
        "O ano de 2025 está sendo marcado por avanços tecnológicos sem precedentes. "
        "Inteligência artificial, automação e tecnologias verdes estão mudando a forma como as empresas operam. "
        "Especialistas afirmam que essas inovações podem impulsionar o crescimento econômico global e criar milhões de empregos."
    ),
    autor="Rodrigo Rocha",
    data_hora=datetime.now()
)


class ArquivoDocx:
    pass
