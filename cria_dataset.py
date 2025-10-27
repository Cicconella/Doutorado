import re
import unicodedata
import pandas as pd


#####  Código para construir o dataset ##### 

def strip_accents(s: str) -> str:
    if pd.isna(s):
        return s
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

#Extrai cd_exame do início de "imagem" (antes do primeiro "-") e coloca em minúsculas
def extrair_cd_exame(nome_arquivo: str) -> str:
    # pega o primeiro segmento antes de '-' (ex.: "ALP.026080-pan..." -> "ALP.026080")
    m = re.match(r"^([^-\s]+)", str(nome_arquivo))
    base = m.group(1) if m else str(nome_arquivo)
    return base.lower()


##### Dados extraidos do banco de dados - versao larga ##### 

dados_pc = pd.read_csv("/home/aninha/Desktop/Doutorado/Dados/tabela_cpd_larga.csv")
# print(dados_pc.head())

# print(dados_pc.shape)


##### Dados extraidos do CVAT de auditoria e processados pela Papiron ##### 

dados_preditos = pd.read_csv("/home/aninha/Desktop/Doutorado/Dados/anotadas/results.csv")
# print(dados_preditos.head())

# print(dados_preditos.shape)

# print(dados_preditos.achado.unique())


# 1) Normaliza "achado" e define o conjunto que será considerado "obturado"

achados_ausente_norm = {
    "dente ausente"
}

achados_carie_norm = {
    "carie"
}

achados_obturado_norm = {
    "restauracao",
    "condutos obturados",  
    "retentor intraradicular",
    "coroa unitaria sobre dente",
    "protese fixa sobre dente"
}

achado_norm = (
    dados_preditos["achado"]
    .astype(str)
    .str.lower()
    .map(strip_accents)
    .str.strip()
)


#Criando tabela para ausentes

df_ausente = dados_preditos[achado_norm.isin(achados_ausente_norm)].copy()

df_ausente["cd_exame"] = df_ausente["imagem"].map(extrair_cd_exame)

df_ausente["ausente"] = 1

# Tabela dinâmica (somando ocorrências por exame x dente)
wide_ausente = (
    df_ausente
    .pivot_table(index="cd_exame", columns="dente", values="ausente", aggfunc="sum", fill_value=0)
    .sort_index(axis=1)
)

# Garante a grade completa de dentes (11–18, 21–28, 31–38, 41–48) e renomeia colunas
todos_dentes = list(range(11, 19)) + list(range(21, 29)) + list(range(31, 39)) + list(range(41, 49))
wide_ausente = wide_ausente.reindex(columns=todos_dentes, fill_value=0)

wide_ausente.columns = [f"ausente_{d}" for d in wide_ausente.columns]

# 6) Limita o valor máximo a 2 por dente, como você pediu
wide_ausente = wide_ausente.clip(upper=2)

# Resultado
resultado_ausente = wide_ausente.reset_index()
print(resultado_ausente)

# Salvar em CSV
# resultado.to_csv("ausentes_por_dente.csv", index=False

# #Criando tabela para caries

df_carie = dados_preditos[achado_norm.isin(achados_carie_norm)].copy()

df_carie["cd_exame"] = df_carie["imagem"].map(extrair_cd_exame)

df_carie["carie"] = 1

# Tabela dinâmica (somando ocorrências por exame x dente)
wide_carie = (
    df_carie
    .pivot_table(index="cd_exame", columns="dente", values="carie", aggfunc="sum", fill_value=0)
    .sort_index(axis=1)
)

# Garante a grade completa de dentes (11–18, 21–28, 31–38, 41–48) e renomeia colunas
wide_carie = wide_carie.reindex(columns=todos_dentes, fill_value=0)
print(wide_carie)


wide_carie.columns = [f"carie_{d}" for d in wide_carie.columns]

# 6) Limita o valor máximo a 2 por dente, como você pediu
wide_carie = wide_carie.clip(upper=2)

# Resultado final
resultado_carie = wide_carie.reset_index()
print(resultado_carie)


#Criando a tabela para obturados

df_obturado = dados_preditos[achado_norm.isin(achados_obturado_norm)].copy()

df_obturado["cd_exame"] = df_obturado["imagem"].map(extrair_cd_exame)

# Marca uma ocorrência de "obturado" por linha
df_obturado["obturado"] = 1

# Tabela dinâmica (somando ocorrências por exame x dente)
wide_obturado = (
    df_obturado
    .pivot_table(index="cd_exame", columns="dente", values="obturado", aggfunc="sum", fill_value=0)
    .sort_index(axis=1)
)

# Garante a grade completa de dentes (11–18, 21–28, 31–38, 41–48) e renomeia colunas
wide_obturado = wide_obturado.reindex(columns=todos_dentes, fill_value=0)

wide_obturado.columns = [f"obturado_{d}" for d in wide_obturado.columns]

# 6) Limita o valor máximo a 2 por dente, como você pediu
wide_obturado = wide_obturado.clip(upper=2)

# Resultado final
resultado_obturado = wide_obturado.reset_index()  # colunas: cd_exame, obturado_11, ..., obturado_48

# (Opcional) salvar em CSV
# resultado.to_csv("obturados_por_dente.csv", index=False)

# print(resultado_obturado.head())

#Junta as duas tabelas

# print(resultado_ausente)

final = pd.merge(resultado_ausente, resultado_carie, on="cd_exame")
final = pd.merge(final, resultado_obturado, on="cd_exame") 

print(final.head())

# print(final.shape)

final.to_csv("/home/aninha/Desktop/Doutorado/Dados/tabela_cpod_larga_predicao.csv")