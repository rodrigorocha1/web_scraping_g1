from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
from models.noticia import Noticia
from datetime import datetime
from servicos.manipulador.arquivo_docx import ArquivoDOCX

noticia_exemplo = Noticia(
    id_noticia='1',
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
print(noticia_exemplo)

arquivo_docx = ArquivoDOCX()
arquivo_docx.nome_arquivo = 'teste.docx'
arquivo_docx.noticia = noticia_exemplo
arquivo_docx.gerar_documento()
