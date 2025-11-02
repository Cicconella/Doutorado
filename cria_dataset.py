import re
import unicodedata
import pandas as pd
import sys

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


achados_ausente_norm = {
    "dente ausente"
}

achados_carie_norm = {
    "carie"
}

achados_obturado_norm = {
    "restauracao",
    "condutos obturados",
    "coroa unitaria sobre dente",
    "protese fixa sobre dente"
}

todos_dentes = list(range(11, 19)) + list(range(21, 29)) + list(range(31, 39)) + list(range(41, 49))

##### Dados extraidos do banco de dados - versao larga ##### 

dados_pc = pd.read_csv("/home/aninha/Desktop/Doutorado/Dados/tabela_cpd_larga.csv")
# print(dados_pc)
# print(dados_pc.isna().any().any())
# print(dados_pc.shape)

dados_auditoria = pd.read_csv("/home/aninha/Desktop/Doutorado/Dados/anotadas/associacao_com_gabarito_dente_achado.csv")
# print(dados_auditoria.head())

achado_norm = (
    dados_auditoria["Achado"]
    .astype(str)
    .str.lower()
    .map(strip_accents)
    .str.strip()
)

df_obturado = dados_auditoria[achado_norm.isin(achados_obturado_norm)].copy()

df_obturado["cd_exame"] = df_obturado["filename"].map(extrair_cd_exame)

# Marca uma ocorrência de "obturado" por linha
df_obturado["obturado"] = 1
# print(df_obturado.head())

# Tabela dinâmica (somando ocorrências por exame x dente)
wide_obturado = (
    df_obturado
    .pivot_table(index="cd_exame", columns="Dente", values="obturado", aggfunc="sum", fill_value=0)
    .sort_index(axis=1)
)

# Garante a grade completa de dentes (11–18, 21–28, 31–38, 41–48) e renomeia colunas
wide_obturado = wide_obturado.reindex(columns=todos_dentes, fill_value=0)

wide_obturado.columns = [f"obturado_{d}" for d in wide_obturado.columns]

# # 6) Limita o valor máximo a 2 por dente, como você pediu
# wide_obturado = wide_obturado.clip(upper=2)

# Resultado final
resultado_obturado = wide_obturado.reset_index()
# print(resultado_obturado.head())
print(resultado_obturado.shape)


### Testando se estou com os mesmos exames ###
set_pc = set(dados_pc["cd_exame"].unique())
set_obt = set(resultado_obturado["cd_exame"].unique())
# Só em dados_pc
so_pc = set_pc - set_obt

# Só em resultado_obturado
so_obt = set_obt - set_pc

print(f"Só em dados_pc: {len(so_pc)} exames")
print(f"Só em resultado_obturado: {len(so_obt)} exames")

dados_pc_exclusivos = dados_pc[dados_pc["cd_exame"].isin(so_pc)]
resultado_obturado_exclusivos = resultado_obturado[resultado_obturado["cd_exame"].isin(so_obt)]

print(dados_pc_exclusivos.cd_exame)
print(resultado_obturado_exclusivos.cd_exame)

# print("Exames analisados:")
# print(len(resultado_obturado.cd_exame.unique()))

final = pd.merge(dados_pc, resultado_obturado, on="cd_exame", how="inner")
print(final)
# print(dados_pc.isna().any().any())

print("Exames analisados - final:")
print(len(final.cd_exame.unique()))


infos = pd.read_csv("/var/home/aninha/Desktop/Doutorado/Dados/resultados_com_origem_idade_sexo.csv")

print(infos.shape)
print(final.shape)

final = pd.merge(infos, final, on="cd_exame", how="right")
print(final.shape)

final.to_csv("/home/aninha/Desktop/Doutorado/Dados/tabela_cpod_larga_gabarito.csv", index=False)


##### Dados extraidos do CVAT de auditoria e processados pela Papiron ##### 

dados_preditos = pd.read_csv("/home/aninha/Desktop/Doutorado/Dados/anotadas/results.csv")
# print(dados_preditos.head())
# print(dados_preditos.shape)
# print(dados_preditos.achado.unique())
# print("Exames analisados:")
# print(len(dados_preditos.cd_exame.unique()))

# Normaliza "achado" 
achado_norm = (
    dados_preditos["achado"]
    .astype(str)
    .str.lower()
    .map(strip_accents)
    .str.strip()
)

# Criando tabela para ausentes

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
wide_ausente = wide_ausente.reindex(columns=todos_dentes, fill_value=0)

wide_ausente.columns = [f"ausente_{d}" for d in wide_ausente.columns]

# 6) Limita o valor máximo a 1 por dente
wide_ausente = wide_ausente.clip(upper=1)

# Resultado
resultado_ausente = wide_ausente.reset_index()
print(resultado_ausente)

# print(resultado_ausente.isna().any().any())

print("Exames analisados:")
print(len(resultado_ausente.cd_exame.unique())) # Aqui.. se não tiver dente ausente, nao vai estar na tabela


# ### Testando se estou com os mesmos exames ###
# set_final = set(final["cd_exame"].unique())
# set_aus = set(resultado_ausente["cd_exame"].unique())
# # Só em dados_final
# so_final = set_final - set_aus

# # Só em resultado_ausente
# so_aus = set_aus - set_final

# print(f"Só em dados_final: {len(so_final)} exames")
# print(f"Só em resultado_ausente: {len(so_aus)} exames")

# dados_final_exclusivos = final[final["cd_exame"].isin(so_final)]
# resultado_ausente_exclusivos = resultado_ausente[resultado_ausente["cd_exame"].isin(so_obt)]

# print(dados_final_exclusivos.cd_exame)
# print(resultado_ausente_exclusivos.cd_exame)

# Conjuntos únicos
set_final = set(final["cd_exame"].unique())
set_ausente = set(resultado_ausente["cd_exame"].unique())

faltando = set_final - set_ausente
sobrando = set_ausente - set_final

print(f"Exames faltando: {len(faltando)} | Exames sobrando: {len(sobrando)}")

# Cria DataFrame com linhas novas
if faltando:
    # cria DataFrame com as mesmas colunas, preenchido com 0
    novos = pd.DataFrame(columns=resultado_ausente.columns)
    novos["cd_exame"] = list(faltando)
    # preenche 0 em todas as colunas restantes
    for col in novos.columns:
        if col != "cd_exame":
            novos[col] = 0
    # concatena com o original
    resultado_ausente_corrigido = pd.concat([resultado_ausente, novos], ignore_index=True)
else:
    resultado_ausente_corrigido = resultado_ausente.copy()

# Filtra novamente (para eliminar os "sobrando", se quiser garantir consistência)
resultado_ausente_corrigido = resultado_ausente_corrigido[
    resultado_ausente_corrigido["cd_exame"].isin(set_final)
].copy()

# Resumo final
print(f"Linhas finais: {len(resultado_ausente_corrigido)}")
print(f"Agora contém todos os {len(set_final)} exames da tabela 'final'")

print(resultado_ausente_corrigido)
# (Opcional) salvar
# resultado_ausente_corrigido.to_csv("resultado_ausente_corrigido.csv", index=False)

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
# print(wide_carie)

wide_carie.columns = [f"carie_{d}" for d in wide_carie.columns]

# # Limita o valor máximo a 2 por dente, como você pediu
# wide_carie = wide_carie.clip(upper=2)

# Resultado final
resultado_carie = wide_carie.reset_index()
# print(resultado_carie)
print("Exames analisados:")
print(len(resultado_carie.cd_exame.unique()))

# Faz o merge entre resultado_ausente_corrigido e resultado_carie com base em cd_exame
resultado_merged = pd.merge(
    resultado_ausente_corrigido,
    resultado_carie,
    on="cd_exame",
    how="left"
)

# Substitui valores NaN por 0 em todas as colunas
resultado_merged = resultado_merged.fillna(0)

print(f"Linhas finais: {len(resultado_merged)}")
print(f"Colunas finais: {list(resultado_merged.columns)}")


# Criando a tabela para obturados

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
resultado_obturado = wide_obturado.reset_index()

print("Exames analisados:")
print(len(resultado_obturado.cd_exame.unique()))

# Faz o merge entre resultado_ausente_corrigido e resultado_carie com base em cd_exame
resultado_merged2 = pd.merge(
    resultado_merged,
    resultado_obturado,
    on="cd_exame",
    how="left"
)

# Substitui valores NaN por 0 em todas as colunas
resultado_merged2 = resultado_merged2.fillna(0)

print(f"Linhas finais: {len(resultado_merged)}")
print(f"Colunas finais: {list(resultado_merged.columns)}")


# ##### Adicionar infos do paciente

print(infos.shape)
print(resultado_merged2.shape)

resultado_merged2 = pd.merge(infos, resultado_merged2, on="cd_exame", how="right")
print(resultado_merged2.shape)

resultado_merged2.to_csv("/home/aninha/Desktop/Doutorado/Dados/tabela_cpod_larga_predicao.csv", index=False)