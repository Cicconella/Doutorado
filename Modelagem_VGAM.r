library(readxl)
dados <- read_xlsx("/home/aninha/Desktop/Doutorado/Doutorado/Banco_de_dados.xlsx")
dados <- data.frame(dados)

## TRATAMENTO DOS DADOS ##

names(dados) #verificar os nomes das variáveis
#Alterar os nomes das variáveis
names(dados)[2:103] <- c("Idade", "Sexo", "Gênero", "Assiduidade_escolar", "Cor_Raça", 
                         "Religião", "Importância_religião",
                         "Nascido_SP", "Coabitação", "Coabitação1", "Coabitação2",
                         "Coabitação3", "Coabitação4", "Coabitação5", "Coabitação6",
                         "Coabitação7", "Coabitação8", "Coabitação997", "Coabitação999",
                         "Coabitação996", "Relacionamento_pais", "Frequência_pai",
                         "Frequência_mãe", "Trabalho_pai", "Trabalho_mãe", "Responsável",
                         "Preocupação_responsável", "Intimidade_responsável",
                         "Num_irmãos", "Num_irmãos_velhos", "Num_irmãs",
                         "Num_irmãs_velhas", "Ouvir_HIV", "Ouvir_preservativo",
                         "Saber_preservativo", "Saber_contracepção", "Relação_sexual", 
                         "Gravidez", "Contracepção", "HIV", "Conversar_sexo",
                         "Conversar_sexo1", "Conversar_sexo2", "Conversar_sexo3",
                         "Conversar_sexo4", "Conversar_sexo5", "Conversar_sexo6",
                         "Conversar_sexo7", "Conversar_sexo8", "Conversar_sexo997",
                         "Conversar_sexo996", "Conversar_gravidez", "Conversar_gravidez1",
                         "Conversar_gravidez2", "Conversar_gravidez3", "Conversar_gravidez4",
                         "Conversar_gravidez5", "Conversar_gravidez6", "Conversar_gravidez7",
                         "Conversar_gravidez8", "Conversar_gravidez997", "Conversar_gravidez996",
                         "Conversar_contracepção", "Conversar_contracepção1", "Conversar_contracepção2",
                         "Conversar_contracepção3", "Conversar_contracepção4", "Conversar_contracepção5",
                         "Conversar_contracepção6", "Conversar_contracepção7", "Conversar_contracepção8",
                         "Conversar_contracepção997", "Conversar_contracepção996", 
                         "Conversar_HIV", "Conversar_HIV1", "Conversar_HIV2", "Conversar_HIV3",
                         "Conversar_HIV4", "Conversar_HIV5", "Conversar_HIV6", "Conversar_HIV7",
                         "Conversar_HIV8", "Conversar_HIV997", "Conversar_HIV996",
                         "L1", "L2", "L3", "L4", "L5", "L6", "V1", "V2", "V3",
                         "V4", "V5", "V6", "V7", "P1", "P2", "P3", "P4",
                         "Indice_riqueza")
dados <- dados[, -1] #retirar a coluna de identificação
summary(dados) #resumo dos dados

#Verificação das variáveis
unique(dados$Sexo) #ver os níveis da variável
dados$Sexo <- as.factor(dados$Sexo) #transformar em fator
#Reagrupar os níveis
levels(dados$Sexo) <- c("Masculino", "Feminino")

unique(dados$Gênero) #ver os níveis da variável
dados$Gênero <- as.factor(dados$Gênero) #transformar em fator
#Reagrupar os níveis
levels(dados$Gênero) <- c("Menino", "Menina", "Outro/a")

unique(dados$Assiduidade_escolar) #ver os níveis da variável
dados$Assiduidade_escolar <- as.factor(dados$Assiduidade_escolar) #transformar em fator
#Reagrupar os níveis
levels(dados$Assiduidade_escolar) <- c("Não", "Sim", 
                                       "Escola fechada devido à COVID-19",
                                       "Recuso a responder")

unique(dados$Cor_Raça) #ver os níveis da variável
dados$Cor_Raça <- as.factor(dados$Cor_Raça) #transformar em fator
levels(dados$Cor_Raça) <- c("Branca", "Parda", "Preta", "Amarela", "Indígena",
                            "Recuso a responder")

unique(dados$Religião) #ver os níveis da variável
#Transformar NA em Não resposta
dados$Religião <- ifelse(is.na(dados$Religião), 
                         "Não resposta", dados$Religião)
dados$Religião <- as.factor(dados$Religião) #transformar em fator
levels(dados$Religião) <- c("Nenhuma", "Católica", "Evangélica pentecostal", 
                            "Evangélica protestante", "Espírita",
                            "Afro-brasileira", "Recuso a responder", "Outra",
                            "Não resposta")

unique(dados$Importância_religião) #ver os níveis da variável
#Transformar NA em Não resposta
dados$Importância_religião <- ifelse(is.na(dados$Importância_religião), 
                                     "Não resposta", dados$Importância_religião)
dados$Importância_religião <- as.factor(dados$Importância_religião) #transformar em fator
levels(dados$Importância_religião) <- c("Não é importante", "Pouco importante",
                                        "Importante", "Muito importante", 
                                        "Recuso a responder", "Não sei",
                                        "Não resposta")

unique(dados$Nascido_SP) #ver os níveis da variável
dados$Nascido_SP <- as.factor(dados$Nascido_SP) #transformar em fator
levels(dados$Nascido_SP) <- c("Não", "Sim", "Recuso a responder", "Não sei")

unique(dados$Relacionamento_pais)
#Transformar NA em Não resposta
dados$Relacionamento_pais <- ifelse(is.na(dados$Relacionamento_pais), 
                                    "Não resposta", dados$Relacionamento_pais)
dados$Relacionamento_pais <- as.factor(dados$Relacionamento_pais) #transformar em fator
levels(dados$Relacionamento_pais) <- c("Não estão juntos", 
                                       "Atualmente casados ou vivendo juntos",
                                       "Recuso a responder", "Não sei", 
                                       "Não resposta")

unique(dados$Frequência_pai)
#Transformar NA em Não resposta
dados$Frequência_pai <- ifelse(is.na(dados$Frequência_pai), 
                               "Não resposta", dados$Frequência_pai)
dados$Frequência_pai <- as.factor(dados$Frequência_pai) #transformar em fator
levels(dados$Frequência_pai) <- c("Nunca me encontrei com meu pai",
                                  "Algumas vezes no ano", "Pelo menos uma vez ao mês",
                                  "Toda semana", "Recuso a responder", "Não sei", 
                                  "Não resposta")

unique(dados$Frequência_mãe)
#Transformar NA em Não resposta
dados$Frequência_mãe <- ifelse(is.na(dados$Frequência_mãe), 
                               "Não resposta", dados$Frequência_mãe)
dados$Frequência_mãe <- as.factor(dados$Frequência_mãe) #transformar em fator
levels(dados$Frequência_mãe) <- c("Algumas vezes no ano", "Pelo menos uma vez ao mês",
                                  "Toda semana", "Recuso a responder", "Não sei", 
                                  "Não resposta")

unique(dados$Trabalho_pai)
#Transformar NA em Não resposta
dados$Trabalho_pai <- ifelse(is.na(dados$Trabalho_pai), 
                             "Não resposta", dados$Trabalho_pai)
dados$Trabalho_pai <- as.factor(dados$Trabalho_pai) #transformar em fator
levels(dados$Trabalho_pai) <- c("Remunerado ou aposentado", 
                                "Não trabalha e à procura de emprego",
                                "Não trabalha e não está à procura de emprego", 
                                "Recuso a responder", "Não sei", 
                                "Não resposta")

unique(dados$Trabalho_mãe)
#Transformar NA em Não resposta
dados$Trabalho_mãe <- ifelse(is.na(dados$Trabalho_mãe), 
                             "Não resposta", dados$Trabalho_mãe)
dados$Trabalho_mãe <- as.factor(dados$Trabalho_mãe) #transformar em fator
levels(dados$Trabalho_mãe) <- c("Remunerada ou aposentada", 
                                "Não trabalha e à procura de emprego",
                                "Não trabalha e não está à procura de emprego", 
                                "Recuso a responder", "Não sei", 
                                "Não resposta")

unique(dados$Responsável)
dados$Responsável <- as.factor(dados$Responsável) #transformar em fator
levels(dados$Responsável) <- c("Ninguém", "Mãe", "Pai", "Madrasta", "Padrasto",
                               "Irmão", "Irmã", "Avó", "Avô", "Tia", "Tio",
                               "Outro familiar adulto",
                               "Outro adulto que não é da família",
                               "Recuso a responder")

unique(dados$Preocupação_responsável)
dados$Preocupação_responsável <- ifelse(is.na(dados$Preocupação_responsável), 
                                        "Não resposta", dados$Preocupação_responsável)
dados$Preocupação_responsável <- as.factor(dados$Preocupação_responsável) #transformar em fator
levels(dados$Preocupação_responsável) <- c("Nada", "Pouco", "Mais ou menos", "Muito",
                                           "Recuso a responder", "Não sei",
                                           "Não resposta")

unique(dados$Intimidade_responsável)
dados$Intimidade_responsável <- ifelse(is.na(dados$Intimidade_responsável), 
                                       "Não resposta", dados$Intimidade_responsável)
dados$Intimidade_responsável <- as.factor(dados$Intimidade_responsável) #transformar em fator
levels(dados$Intimidade_responsável) <- c("Nada", "Pouco", "Mais ou menos", "Muito",
                                          "Recuso a responder", "Não sei",
                                          "Não resposta")

unique(dados$Num_irmãos)
dados$Num_irmãos <- as.factor(dados$Num_irmãos) #transformar em fator
levels(dados$Num_irmãos) <- c("0", "1", "2", "3", "4", "5", "6 ou mais", "Recuso a responder",
                              "Não sei")

unique(dados$Num_irmãos_velhos)
dados$Num_irmãos_velhos <- ifelse(is.na(dados$Num_irmãos_velhos), 
                                  "Não resposta", dados$Num_irmãos_velhos)
dados$Num_irmãos_velhos <- as.factor(dados$Num_irmãos_velhos) #transformar em fator
levels(dados$Num_irmãos_velhos) <- c("0", "1", "2", "3", "4", "5", "6 ou mais", "Recuso a responder",
                                     "Não sei", "Não resposta")

unique(dados$Num_irmãs)
dados$Num_irmãs <- as.factor(dados$Num_irmãs) #transformar em fator
levels(dados$Num_irmãs) <- c("0", "1", "2", "3", "4", "5", "6 ou mais", "Recuso a responder",
                             "Não sei")

unique(dados$Num_irmãs_velhas)
dados$Num_irmãs_velhas <- ifelse(is.na(dados$Num_irmãs_velhas), 
                                 "Não resposta", dados$Num_irmãs_velhas)
dados$Num_irmãs_velhas <- as.factor(dados$Num_irmãs_velhas) #transformar em fator
levels(dados$Num_irmãs_velhas) <- c("0", "1", "2", "3", "4", "5", "6 ou mais", "Recuso a responder",
                                    "Não sei", "Não resposta")

dados$Coabitação <- ifelse(is.na(dados$Coabitação), 
                           "Não resposta", dados$Coabitação)
dados$Conversar_sexo <- ifelse(is.na(dados$Conversar_sexo), 
                               "Não resposta", dados$Conversar_sexo)
dados$Conversar_gravidez <- ifelse(is.na(dados$Conversar_gravidez), 
                                   "Não resposta", dados$Conversar_gravidez)
dados$Conversar_contracepção <- ifelse(is.na(dados$Conversar_contracepção), 
                                       "Não resposta", dados$Conversar_contracepção)
dados$Conversar_HIV <- ifelse(is.na(dados$Conversar_HIV), 
                              "Não resposta", dados$Conversar_HIV)

unique(dados$Ouvir_HIV)
dados$Ouvir_HIV <- as.factor(dados$Ouvir_HIV) #transformar em fator
levels(dados$Ouvir_HIV) <- c("Não", "Sim", "Recuso a responder", "Não sei")

unique(dados$Ouvir_preservativo)
dados$Ouvir_preservativo <- as.factor(dados$Ouvir_preservativo) #transformar em fator
levels(dados$Ouvir_preservativo) <- c("Não", "Sim", "Recuso a responder", "Não sei")

unique(dados$Saber_preservativo)
dados$Saber_preservativo <- as.factor(dados$Saber_preservativo) #transformar em fator
levels(dados$Saber_preservativo) <- c("Não", "Sim", "Não entendi a pergunta",
                                      "Recuso a responder", "Não sei")

unique(dados$Saber_contracepção)
dados$Saber_contracepção <- ifelse(is.na(dados$Saber_contracepção), 
                                   "Não resposta", dados$Saber_contracepção)
dados$Saber_contracepção <- as.factor(dados$Saber_contracepção) #transformar em fator
levels(dados$Saber_contracepção) <- c("Não", "Sim", "Não entendi a pergunta",
                                      "Recuso a responder", "Não sei",
                                      "Não resposta")

unique(dados$Relação_sexual)
dados$Relação_sexual <- as.factor(dados$Relação_sexual) #transformar em fator
levels(dados$Relação_sexual) <- c("Não", "Sim", "Não entendi a pergunta",
                                  "Recuso a responder", "Não sei")

unique(dados$Gravidez)
dados$Gravidez <- as.factor(dados$Gravidez) #transformar em fator
levels(dados$Gravidez) <- c("Não", "Sim", "Não entendi a pergunta",
                            "Recuso a responder", "Não sei")

unique(dados$Contracepção)
dados$Contracepção <- as.factor(dados$Contracepção) #transformar em fator
levels(dados$Contracepção) <- c("Não", "Sim", "Não entendi a pergunta",
                                "Recuso a responder", "Não sei")

unique(dados$HIV)
dados$HIV <- as.factor(dados$HIV) #transformar em fator
levels(dados$HIV) <- c("Não", "Sim", "Não entendi a pergunta",
                       "Recuso a responder", "Não sei")

dados$Indice_riqueza <- as.factor(dados$Indice_riqueza) #transformar em fator
levels(dados$Indice_riqueza) <- c("Abaixo de 20%", "20%-40%", "40%-60%",
                                  "60%-80%", "Acima de 80%", "Não resposta")

liberdade <- dados[, c("L1", "L2", "L3", "L4", "L5", "L6")]
voz <- dados[, c("V1", "V2", "V3", "V4", "V5", "V6", "V7")]
decisão <- dados[, c("P1", "P2", "P3", "P4")]
resps <- data.frame(liberdade, voz, decisão)

liberdade <- replace(liberdade, liberdade == 996, NA)
liberdade <- replace(liberdade, liberdade == 999, NA)

voz <- replace(voz, voz == 996, NA)
voz <- replace(voz, voz == 999, NA)

decisão <- replace(decisão, decisão == 996, NA)
decisão <- replace(decisão, decisão == 999, NA)

dados$Escore_liberdade <- rowMeans(liberdade, na.rm = TRUE)
dados$Escore_voz <- rowMeans(voz, na.rm = TRUE)
dados$Escore_decisão <- rowMeans(decisão, na.rm = TRUE)
dados$Escore_geral <- rowMeans(dados[, 103:105], na.rm = TRUE)

dados2 <- dados

library(dplyr)
dados2$Num_irmãos <- as.character(dados2$Num_irmãos)
dados2$Num_irmãos[dados2$Num_irmãos %in% c("Recuso a responder", "Não sei")] <- NA
dados2$Num_irmãos[dados2$Num_irmãos == "6 ou mais"] <- "6"
dados2$Num_irmãos <- as.numeric(dados2$Num_irmãos)

dados2$Num_irmãs <- as.character(dados2$Num_irmãs)
dados2$Num_irmãs[dados2$Num_irmãs %in% c("Recuso a responder", "Não sei")] <- NA
dados2$Num_irmãs[dados2$Num_irmãs == "6 ou mais"] <- "6"
dados2$Num_irmãs <- as.numeric(dados2$Num_irmãs)

## IMPUTAÇÃO ##
library(VIM)
library(MASS)
library(forcats)
dados3 = dados2[, c(1:8, 21, 24:40, 108:110)]
is.na(dados3)
dados3[dados3 == "Não resposta"] <- NA

dados3_m = subset(dados3, Sexo == "Feminino")
dados3_h = subset(dados3, Sexo == "Masculino")

set.seed(123)
dados3_imp_m <- kNN(dados3_m, k = 17, imp_var = FALSE)
dados3_imp_m <- droplevels(dados3_imp_m)
set.seed(123)
dados3_imp_h <- kNN(dados3_h, k = 17, imp_var = FALSE)
dados3_imp_h <- droplevels(dados3_imp_h)
dados3_imp = rbind(dados3_imp_h, dados3_imp_m)

unique(dados3_imp$Relação_sexual)
dados3_imp$Relação_sexual <- fct_other(
  dados3_imp$Relação_sexual,
  keep = c("Sim", "Não"),   # níveis que você quer manter
  other_level = "Outros"    # nome do novo nível
)

unique(dados3_imp$Gravidez)
dados3_imp$Gravidez <- fct_other(
  dados3_imp$Gravidez,
  keep = c("Sim", "Não"),   # níveis que você quer manter
  other_level = "Outros"    # nome do novo nível
)

unique(dados3_imp$Contracepção)
dados3_imp$Contracepção <- fct_other(
  dados3_imp$Contracepção,
  keep = c("Sim", "Não"),   # níveis que você quer manter
  other_level = "Outros"    # nome do novo nível
)

unique(dados3_imp$HIV)
dados3_imp$HIV <- fct_other(
  dados3_imp$HIV,
  keep = c("Sim", "Não"),   # níveis que você quer manter
  other_level = "Outros"    # nome do novo nível
)

#Trocando níveis porque as estimativas estão muito altas
dados3_imp$Ouvir_HIV <- fct_other(
  dados3_imp$Ouvir_HIV,
  keep = c("Sim", "Não"),   # níveis que você quer manter
  other_level = "Outros"    # nome do novo nível
)

dados3_imp$Ouvir_preservativo <- fct_other(
  dados3_imp$Ouvir_preservativo,
  keep = c("Sim", "Não"),   # níveis que você quer manter
  other_level = "Outros"    # nome do novo nível
)

print("#####################################################################################")
print("Cheguei aqui")

print("Os dados são assim:")

print(head(dados3_imp))


## MODELAGEM VGLM - TRINOMIAL##
library(VGAM)
library(gamlss)
options(scipen = 999)
# Variável resposta Gravidez
#Separando os dados para a abordagem marginal
dados3_imp_grav_sim = subset(dados3_imp, Gravidez != "Outros")
dados3_imp_grav_sim = droplevels(dados3_imp_grav_sim)
dados3_imp_grav_outros = subset(dados3_imp, Gravidez != "Sim")
dados3_imp_grav_outros = droplevels(dados3_imp_grav_outros)

#Primeiro modelo trinomial com todos os dados
fit1 = vglm(Gravidez ~. - Contracepção - HIV - Relação_sexual,
            multinomial(refLevel = 1), data = dados3_imp)
#obs: refLevel = 1 dentro da função multinomial() coloca o nível 1 como referência, nesse caso o Não
#Abaixo a função stepaic do pacote VGAM
fit2 = step4vglm(fit1, direction = "both")
fit2@call
#A saída da função da linha 351 se encontra abaixo
fit2 = vglm(Gravidez ~ Sexo + Intimidade_responsável + Ouvir_HIV + 
              Ouvir_preservativo + Saber_preservativo + Saber_contracepção + 
              Escore_liberdade + Escore_voz, family = multinomial(refLevel = 1), data = dados3_imp)
summary(fit2)
#Razão de chances
exp(coef(fit2, matrix=TRUE))
deviance(fit2)
df.residual(fit2)

stop()

#Modelos binomiais (marginais) apenas para fins de diagnóstico
#Modelo Não/Sim
fit2.1 = gamlss(formula = Gravidez ~ Sexo + Intimidade_responsável + 
                  Ouvir_HIV + Ouvir_preservativo + Saber_preservativo + Saber_contracepção + 
                  Escore_liberdade + Escore_voz, family = BI, data = dados3_imp_grav_sim)
summary(fit2.1)
#Resíduos quantílicos
plot(fit2.1)
#Wormplot
wp(fit2.1)

#Modelo Não/Outros
fit2.2 = gamlss(formula = Gravidez ~ Sexo + Intimidade_responsável + 
                  Ouvir_HIV + Ouvir_preservativo + Saber_preservativo + Saber_contracepção + 
                  Escore_liberdade + Escore_voz, family = BI, data = dados3_imp_grav_outros)
summary(fit2.2)
plot(fit2.2)
wp(fit2.2)

#Resíduos de Pearson
rp2 <- residuals(fit2, type = "pearson")
par(mfrow = c(1, 2))
plot(rp2[,1], pch=20, xlab="Índice", ylab="Resíduos de Pearson")
abline(h=0, col = "red")
title("Logito 1")
plot(rp2[,2], pch=20, xlab="Índice", ylab="Resíduos de Pearson")
abline(h=0, col = "red")
title("Logito 2")
par(mfrow = c(1, 1))

#Calculando as previsões do modelo
pred_class2 = predict(fit2, newdata = dados3_imp, type = "response")
predicted_labels2 <- factor(apply(pred_class2, 1, which.max),
                            levels = 1:nlevels(dados3_imp$Gravidez),
                            labels = levels(dados3_imp$Gravidez))
actual_labels2 <- dados3_imp$Gravidez

#Matriz de confusão
library(caret)
confusion_matrix_result2 <- confusionMatrix(data = predicted_labels2, reference = actual_labels2)
confusion_matrix_result2