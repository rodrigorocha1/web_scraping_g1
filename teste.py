import hashlib

# Opção A: Hash da URL (mais comum e eficaz para GUIDs com permalink)
url_da_noticia = "https://g1.globo.com/sp/ribeirao-preto-franca/noticia/2025/06/29/homem-e-preso-em-flagrante-apos-tentar-furtar-viatura-dos-bombeiros-enquanto-equipe-atendia-ocorrencia-em-sertaozinho-sp.ghtml"
id_unico_hash_url = hashlib.md5(url_da_noticia.encode('utf-8')).hexdigest()
print(f"ID Único (Hash da URL - MD5): {id_unico_hash_url}")
