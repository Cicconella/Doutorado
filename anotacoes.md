<!-- Dados que tem odontograma:
- /media/TriHD/Papiron/Panoramicas_Odontograma/pan_odontograma_2025_04_YOLOv11

Dados que tem auditoria:
- /media/TriHD/Papiron/panoramicas_Auditoria/pan_auditoria_25_04_yolov11_crop/yolo_data



Preciso criar um banco de dados em duas versões dos dados mais completos:

- Gabarito = file:///home/aninha/Desktop/Doutorado/Dados/tabela_cpod_larga.csv
- Predições

O que inclui:

- Para cada dente de cada pessoa, colocar (P = Perdido, C = Cariado, O = Obturado)



#### Achados #####

['higido' 'restauracao' (C)  'carie' (C) 'dente semi-incluso' 'condutos obturados' (O)
 'dente impactado' 'dente incluso' 'contencao' 'dente ausente'
 'retentor intraradicular' 'coroa unitaria sobre dente' 'implante'
 'protese fixa sobre dente' 'protese fixa sobre implante'
 'coroa unitaria sobre implante' 'aparelho ortodondico' 'raiz residual'
 'protocolo' 'placa' 'supranumerario']

 Elegíveis como obturados:
- restauração
- condutos obturados
- retentor intraradicular
- coroa unitária sobre dente
- prótese fixa sobre dente


CARIADO
'carie'
 
PERDIDO
'dente ausente'
'implante'
'protese fixa sobre implante'
'coroa unitaria sobre implante'
'protocolo'
raiz residual'
 
OBTURADO
'restauracao'
'coroa unitaria sobre dente'
'protese fixa sobre dente'
 
 
Não dá pra classificar, pois pode ser cariado, ou perdido
'higido' 'dente semi-incluso' 
'dente impactado' 'dente incluso' 'contencao' 
'aparelho ortodondico' 
'placa' 'supranumerario']
'condutos obturados'
'retentor intraradicular'
 
CPOD só classifica dentes erupcionados (incluso, semi-incluso e impactado ficam de fora).]


- CPOD: Calcular o CPOD e verificar o tipo de distribuição - Binomial negativo ou Poisson.
- Modelo: Predizer o número de CPOD com efeito de idade, regiao ou sexo.
- Teste de Kolmogorov para as duas tabelas - pp plot


- Avaliar por dente - qual é o dente que mais contribui para ausente?

- Modelo Binomial para dentes ausentes - individuo como efeito aleatorio.
Resposta: dente ausente 11 = efeito aleatorio (individuo) + dente dentro do individuo + sexo + idade + regiao (glm misto - funcao ligacao logistica - nested)

- Avaliar qual dente tem maior efeito.

- Comparar os resultados das duas distribuições

#### Relate coordinates #####

DENTES="/var/home/aninha/Desktop/Doutorado/Dados/dentes_predictions_all.csv"
MAXILA="/var/home/aninha/Desktop/Doutorado/Dados/maxila_mandibula_predictions_all.csv"
ACHADOS="/home/aninha/Desktop/yolo_data/dataset_boxes_yxyx_filtrado.csv"
RELACIONADOS="/var/home/aninha/Desktop/Doutorado/Dados/anotadas/associacao_com_gabarito.csv"
python /var/home/aninha/Desktop/OdontoPrev/deploy-papiron/papiron/src/functions/relate_coordinates.py $DENTES $MAXILA $ACHADOS $RELACIONADOS

#### Testar para amostras imagens #####

IMGS=/var/home/aninha/Desktop/Doutorado/Dados/amostra-auditoria
OUT=/var/home/aninha/Desktop/Doutorado/Dados/amostra-auditoria-processadas
python /var/home/aninha/Desktop/OdontoPrev/deploy-papiron/local_test_deploy/test_endpoint_local.py -v $IMGS $OUT --debug-images


#### Revisando o cria_dataset ####

- Tenho 2746 exames com os dados de dentes ausentes e caries do banco de dados - sem NAs
- Tenho 2524 exames com pan_auditoria_25_04_yolov11_crop

- Exclusivos:
Só em dados_pc: 231 exames (provavelmente perdidos na associacao)
Só em resultado_obturado: 9 exames

- Resultado final para o gabarito: 2515

#### Melhorias ####

1. Pegar no banco de dados os 9 exames que só tenho no resultado_obturado? ou talvez no /home/aninha/Desktop/yolo_data/dataset_boxes_yxyx_filtrado.csv?

2. Porque tinha 190 exames a mais ao analisar ausentes? 

############################-->

# 🦷 CPOD a partir de panorâmicas

## 📂 Fontes de Dados

### **Odontograma no Triforce**
```
/media/TriHD/Papiron/Panoramicas_Odontograma/pan_odontograma_2025_04_YOLOv11
```

### **Auditoria no Triforce**
```
/media/TriHD/Papiron/panoramicas_Auditoria/pan_auditoria_25_04_yolov11_crop/yolo_data
```

### **Bases de referência**
- **Gabarito:**  
  `file:///home/aninha/Desktop/Doutorado/Dados/tabela_cpod_larga.csv`
- **Predições:**  
  Saída dos modelos YOLOv11 e dos scripts de auditoria.


---

## 🧩 Estrutura desejada do banco consolidado

Para **cada dente de cada pessoa**, incluir as variáveis:

| Coluna | Descrição |
|:-------|:-----------|
| **P** | Dente Perdido |
| **C** | Dente Cariado |
| **O** | Dente Obturado |

As duas versões do banco serão:
1. **Gabarito:** dados anotados manualmente:
    - [Gabarito 1](../Dados/tabela_cpod_larga_gabarito.csv): Para perdido e cariado, foram extraídas as informações do banco de dados. Para as informações de obturados, foram utilizadas as anotações de dentistas.
2. **Predições:** resultados automáticos dos modelos.
    - [Predição 1](../Dados/tabela_cpod_larga_predicao.csv): Todas as imagens foram processados pelo deploy_papiron, utilizei o arquivo [de resultados final ](../Dados/anotadas/results.csv)

---

## 🔍 Classificação dos Achados

### Lista geral de achados
```
['higido', 'restauracao', 'carie', 'dente semi-incluso', 'condutos obturados',
 'dente impactado', 'dente incluso', 'contencao', 'dente ausente',
 'retentor intraradicular', 'coroa unitaria sobre dente', 'implante',
 'protese fixa sobre dente', 'protese fixa sobre implante',
 'coroa unitaria sobre implante', 'aparelho ortodondico', 'raiz residual',
 'protocolo', 'placa', 'supranumerario']
```

---

### **Elegíveis como obturados (O)**
- restauração  
- condutos obturados  
- retentor intraradicular  
- coroa unitária sobre dente  
- prótese fixa sobre dente  

---

### **Elegíveis como cariados (C)**
- cárie

---

### **Elegíveis como perdidos (P)**
- dente ausente  
- implante  
- prótese fixa sobre implante  
- coroa unitária sobre implante  
- protocolo*
- raiz residual  

---

### **Não classificáveis (excluídos do CPOD)**
Podem representar condições sem correspondência direta a P, C ou O:
- hígido  
- dente semi-incluso  
- dente impactado  
- dente incluso  
- contenção  
- aparelho ortodôntico  
- placa  
- supranumerário  
- condutos obturados  
- retentor intraradicular  

> **Nota:** O **CPOD** só considera **dentes erupcionados**.  
> Inclusos, semi-inclusos e impactados ficam **fora do denominador**.


---

## 📊 Análises planejadas

### 1. **Distribuição do CPOD**
- Calcular o **índice CPOD total por indivíduo**.
- Avaliar o tipo de distribuição:
  - **Binomial Negativa** ou **Poisson**.
- Aplicar **teste de Kolmogorov–Smirnov** para ajuste e gerar **PP-plot**.

---

### 2. **Modelagem Estatística**
- Modelo para predizer o **número de dentes CPOD** com:
  - Efeito fixo: `idade`, `região`, `sexo`
  - Efeito aleatório: `indivíduo`
- Função de ligação **log** (GLMM misto)
- Avaliar e comparar o ajuste entre distribuições (Poisson vs Binomial Negativa).

---

### 3. **Modelo específico: dentes ausentes**
Modelo binomial (logístico) com efeitos aleatórios:
```
ausente ~ sexo + idade + regiao + (1 | cd_exame) + (1 | dente)
```

- **Efeito aleatório**: indivíduo (`cd_exame`)
- **Efeito aninhado**: dente dentro do indivíduo
- **Objetivo:** identificar quais dentes contribuem mais para o desfecho “ausente”.

---

## 🧠 Questões a investigar
1. **Por que havia 190 exames a mais** na análise de ausentes?  
2. **Os 9 exames** que aparecem apenas em `resultado_obturado` estão em:  
   `/home/aninha/Desktop/yolo_data/dataset_boxes_yxyx_filtrado.csv`?  
3. Verificar se esses exames faltantes devem ser recuperados do banco de dados.

---

## 🧰 Scripts e Caminhos de Execução

### **Relacionamento de coordenadas**
```bash
DENTES="/var/home/aninha/Desktop/Doutorado/Dados/dentes_predictions_all.csv"
MAXILA="/var/home/aninha/Desktop/Doutorado/Dados/maxila_mandibula_predictions_all.csv"
ACHADOS="/home/aninha/Desktop/yolo_data/dataset_boxes_yxyx_filtrado.csv"
RELACIONADOS="/var/home/aninha/Desktop/Doutorado/Dados/anotadas/associacao_com_gabarito.csv"

python /var/home/aninha/Desktop/OdontoPrev/deploy-papiron/papiron/src/functions/relate_coordinates.py \
  $DENTES $MAXILA $ACHADOS $RELACIONADOS
```

---

### **Teste local com imagens**
```bash
IMGS=/var/home/aninha/Desktop/Doutorado/Dados/amostra-auditoria
OUT=/var/home/aninha/Desktop/Doutorado/Dados/amostra-auditoria-processadas

python /var/home/aninha/Desktop/OdontoPrev/deploy-papiron/local_test_deploy/test_endpoint_local.py \
  -v $IMGS $OUT --debug-images
```

---

## 📈 Revisão de Dataset

| Tabela | Nº de exames | Observação |
|:-------|:--------------|:------------|
| Dados PC (ausentes + cárie) | 2746 | Sem NAs |
| Auditoria (`pan_auditoria_25_04_yolov11_crop`) | 2524 |  |
| Exclusivos em `dados_pc` | 231 | Provável perda na associação |
| Exclusivos em `resultado_obturado` | 9 | Conferir manualmente |
| **Resultado final (gabarito)** | **2515 exames** |  |

---

## Atividades realizadas (11/11)

1. Revisão de artigos de cáries
2. Marcada reunião na quinta para entender cáries no laudo
3. Comparação mais detalhada do laudo com as predições, em caso de pessoas banguelas ou quase, o laudo pode estar incompleto, algumas imagens a predição não encontra nada e estou investigando o motivo (algumas é de rotação).
4. Odontogramas anotados: 600 imagens revisadas
5. Automatização do git/overleaf
6. Criação das variaveis de faixa etaria e região


---

## 🚀 Próximos passos

### Organização
 - [ ] E-mail da Regiane


### Melhorar resultados
- [ ] Buscar no banco de dados os **9 exames** que estão apenas em `resultado_obturado`.  
-[ ] Verificar **diferença de 190 exames** nos dados de ausentes — avaliar duplicatas, erros de associação ou filtragem incorreta.

- [ ] Modelo agrupando faixas etárias

- [ ] Modelo agrupando regiões
- [ ] Comparar saídas do modelo e da associação
- [ ] Escrever os resultados dos modelos
- [ ] Alinhar com a Regiane (ver e-mail)
- [ ] Melhorar o modelo de cáries
- [ ] Separar casos de cáries para a auditoria
- [ ] Escrever a revisão de achados de auditoria
- [ ] Escrever o que já tem da metodologia
- [ ] Atualizar dados de odontograma com o que já foi anotado pela auditoria


### Overleaf 
Senha do Overleaf: olp_7t5Oh5jgOT6iLCeYkKbnzS3e6fMpYh0UeAuH

### Dúvidas com o Luis

- Modelo do odontograma:
* Quais imagens utilizadas? Foi tão pouco mesmo? O banco que tinhamos nao foi usado?
* Avaliamos o resultado com o pós-processamento?
* Usar os dados anotados novos?

- Pós-processamento:
* Adicionar uma etapa para retirar duplicados.

- Modelo de cárie e outros achados:
* Resultado dos modelos?
* Calculo para dente ausente


- Revisão do que foi feito no CVAT


- Corrigi os dados de gabarito, mas ainda não arrumei os da predicao