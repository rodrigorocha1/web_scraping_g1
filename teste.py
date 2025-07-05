import hashlib

# Opção A: Hash da URL (mais comum e eficaz para GUIDs com permalink)
url_da_noticia = "https://g1.globo.com/sp/ribeirao-preto-franca/noticia/2025/06/29/homem-e-preso-em-flagrante-apos-tentar-furtar-viatura-dos-bombeiros-enquanto-equipe-atendia-ocorrencia-em-sertaozinho-sp.ghtml"
id_unico_hash_url = hashlib.md5(url_da_noticia.encode('utf-8')).hexdigest()
print(f"ID Único (Hash da URL - MD5): {id_unico_hash_url}")

# Opção B: Hash de uma combinação de atributos (útil se a URL não for sempre um permalink)
titulo = "Homem é preso em flagrante após tentar furtar viatura dos bombeiros enquanto equipe atendia ocorrência em Sertãozinho, SP"
data_publicacao = "2025-06-29"
fonte = "G1 Ribeirão Preto e Franca"


# 265617cbd1d8c2c3c9a638187498da1b
string_para_hash = f"{titulo}-{data_publicacao}-{fonte}"
id_unico_hash_combinado = hashlib.sha256(string_para_hash.encode('utf-8')).hexdigest()
print(f"ID Único (Hash Combinado - SHA256): {id_unico_hash_combinado}")