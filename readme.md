# Avaliação de Algoritmos de Machine Learning de IDS com NSL-KDD

**CESAR School**  
Aprendizado de Máquina – 2025.1  
Professor: Diego Bezerra

**Equipe:**  
Caio Cesar [@Kal-0](https://github.com/Kal-0)  
Diogo Henrique [@DiogoHMC](https://github.com/DiogoHMC)  
Pedro Coelho [@pedro-coelho-dr](https://github.com/pedro-coelho-dr)  
Virna Amaral [@virnaamaral](https://github.com/virnaamaral)  

## Introdução

Este projeto reproduz e amplia os experimentos do artigo [*Evaluation of Machine Learning Algorithms for Intrusion Detection System* (Almseidin et al., 2018)](/references/evaluation_ml_ids_nslkdd_2018.pdf), que compara algoritmos supervisionados aplicados à detecção de intrusões utilizando o dataset KDD.

Para a reprodução, foi empregada a versão corrigida do conjunto de dados, o **NSL-KDD**, que preserva a estrutura e os ataques originais, mas elimina redundâncias críticas que comprometem a generalização. Os modelos implementados incluem Regressão Logística, k-NN, Decision Tree, Random Forest e MLP. Os testes foram conduzidos com validação estratificada e avaliação final no conjunto real `KDDTest+`.

A análise compara os resultados obtidos com os do artigo original, tanto em métricas agregadas quanto por categoria (normal, DoS, Probe, R2L, U2R), destacando os limites de generalização em cenários com classes raras e amostras não vistas durante o treinamento.


## Dataset

O NSL-KDD é uma versão corrigida do KDD'99 criada pelo ISCX (University of New Brunswick) para resolver problemas como redundância e viés em modelos de detecção de intrusão.

A versão **oficial hospedada no site da UNB** não está mais disponível para download direto. Por isso, foi utilizada a versão publicada no **Kaggle** por M. Hassan Zaib, que contém exatamente os mesmos arquivos descritos na documentação original (KDDTrain+, KDDTest+, etc.), com estrutura, colunas e conteúdo idênticos.

A equivalência foi confirmada comparando:
- Arquivos `.txt` e `.arff` (mesmo número de colunas e registros)
- Atributos categóricos (`protocol_type`, `service`, `flag`)
- Colunas numéricas e campo `difficulty`

Essa versão do Kaggle mantém total compatibilidade com o formato referenciado no artigo original (Tavallaee et al., 2009).

Portanto, ela é adequada para reprodução acadêmica e prática dos experimentos, sendo amplamente utilizada por trabalhos atuais na ausência de um mirror oficial ativo.


**Links:**
- Site oficial: https://www.unb.ca/cic/datasets/nsl.html
- Kaggle (utilizado): https://www.kaggle.com/datasets/hassan06/nslkdd

### Formatos e Subconjuntos Disponíveis

| Arquivo                   | Descrição                                                                 | Uso Típico                          |
|---------------------------|---------------------------------------------------------------------------|-------------------------------------|
| `KDDTrain+.txt`           | Conjunto completo de treino com rótulos e nível de dificuldade.           | Treinamento do modelo.              |
| `KDDTrain+_20Percent.txt` | Subconjunto de 20% do treino, balanceado.                                 | Testes rápidos ou tuning.           |
| `KDDTest+.txt`            | Conjunto completo de teste.                                               | Avaliação padrão do modelo.         |
| `KDDTest-21.txt`          | Subconjunto sem registros de dificuldade máxima.                          | Avaliação simplificada.             |

> Os arquivos `.txt` são separados por vírgula, **sem cabeçalho**.  
> Os arquivos `.arff` são equivalentes, prontos para uso no Weka.  
> Cada arquivo possui **43 colunas**:  
> - 41 variáveis (numéricas e categóricas)  
> - 1 rótulo de classe (`class`)  
> - 1 coluna de dificuldade (`difficulty`)  
> Os principais atributos categóricos são `protocol_type`, `service` e `flag`.  
> A coluna `difficulty` é auxiliar e **não será usada na modelagem**.


## Exploração

Notebook: [notebooks/01_exploration.ipynb](/notebooks/01_exploration.ipynb)


### Agrupamento de Ataques

As classes do NSL-KDD foram agrupadas em 5 categorias principais, conforme metodologia do artigo base. Isso reduz a complexidade do problema e facilita a comparação entre modelos.

#### Categorias e Classes

| Categoria | Descrição | Classes incluídas |
|-----------|-----------|------------------|
| **normal** | Tráfego legítimo | normal |
| **DoS**    | Ataques de negação de serviço | back, land, neptune, pod, smurf, teardrop, apache2, udpstorm, processtable, mailbomb |
| **Probe**  | Escaneamento/reconhecimento | satan, ipsweep, nmap, portsweep, mscan, saint |
| **R2L**    | Remote to Local | ftp_write, guess_passwd, imap, multihop, phf, spy, warezclient, warezmaster, xlock, xsnoop, snmpguess, snmpgetattack, httptunnel, sendmail, named |
| **U2R**    | User to Root | buffer_overflow, loadmodule, perl, rootkit, ps, sqlattack, xterm |

> Nota: Todas as classes do NSL-KDD estão cobertas pelo mapeamento.

##### Distribuição das Categorias

| Categoria | Total de Amostras |
|-----------|-------------------|
| normal    | 67.343            |
| DoS       | 45.927            |
| Probe     | 11.656            |
| R2L       | 995               |
| U2R       | 52                |

![](/report/img/exp/1.png)

### Colunas Categóricas

Durante a análise exploratória, foram identificadas três variáveis categóricas relevantes para modelagem:

| Coluna         | Valores Únicos | Observações                                         | Decisão de Pré-processamento        |
|----------------|----------------|-----------------------------------------------------|-------------------------------------|
| protocol_type  | 3              | tcp (82%), udp (12%), icmp (6%)                     | One-hot direto                      |
| service        | 70             | Top 10 >50%, cauda longa                            | Top-N + "other", depois one-hot     |
| flag           | 11             | SF/S0 >85%, demais relevantes                       | One-hot direto                      |

> **Justificativa:**  
> - Reduzir dimensionalidade e ruído em `service` usando agrupamento dos menos frequentes em "other".
> - `protocol_type` e `flag` são adequados para one-hot sem pré-agrupamento.


![](/report/img/exp/3.png)

### Algoritmos Selecionados

1. **Logistic Regression**  
   - Linear, interpretável, útil para limitações de dados não-lineares.  
   - `sklearn.linear_model.LogisticRegression`

2. **k-Nearest Neighbors (k-NN)**  
   - Baseline simples, sem fase de treino.  
   - `sklearn.neighbors.KNeighborsClassifier`

3. **Decision Tree**  
   - Interpretação fácil, lógica explícita.  
   - `sklearn.tree.DecisionTreeClassifier`

4. **Random Forest**  
   - Ensemble robusto, bom desempenho, resistente a overfitting.  
   - `sklearn.ensemble.RandomForestClassifier`

5. **MLP (Multilayer Perceptron)**  
   - Rede neural simples, avalia capacidade de generalização.  
   - `sklearn.neural_network.MLPClassifier`

##### Algoritmos do artigo original não utilizados

| Algoritmo       | Motivo do Descarte                         |
|-----------------|--------------------------------------------|
| J48             | Específico do Weka (C4.5)                  |
| Random Tree     | Fraco e redundante                         |
| Decision Table  | Não implementado no `sklearn`              |
| BayesNet        | Sem suporte direto em Python               |


### Estatísticas Gerais do Dataset

- Total de amostras: 125.973
- Total de colunas: 43
- Features numéricas: 38
- Features categóricas: 5
- Classes originais distintas (`class`): 23
- Categorias agrupadas (`attack_category`): 5


### Diferença entre Conjuntos de Treinamento e Teste

Durante a exploração do dataset, foi identificado que o conjunto de teste (`KDDTest+`) contém **mais classes originais** na coluna `class` do que o conjunto de treino (`KDDTrain+`).

| Conjunto     | Classes distintas (`class`) |
|--------------|-----------------------------|
| Treinamento  | 23                          |
| Teste        | 38                          |

As 15 classes extras no conjunto de teste não aparecem no treino e representam ataques que o modelo **nunca viu** durante o aprendizado supervisionado.

#### Classes exclusivas do conjunto de teste

`apache2`, `httptunnel`, `mailbomb`, `mscan`, `named`, `processtable`, `ps`, `saint`, `sendmail`, `snmpgetattack`, `snmpguess`, `sqlattack`, `udpstorm`, `worm`, `xlock`, `xsnoop`, `xterm`

> Essas classes foram devidamente mapeadas para uma das 5 categorias principais (`DoS`, `Probe`, `R2L`, `U2R`), mas sua ausência no treinamento **impacta negativamente o desempenho do modelo**, especialmente no **recall das categorias R2L e U2R**.

Essa diferença reflete um cenário mais desafiador e realista de generalização, e deve ser considerada ao interpretar as métricas de avaliação no conjunto de teste.


![](/report/img/exp/4.png)

## Pré-processamento

Notebook: [notebooks/02_preprocessing.ipynb](/notebooks/02_preprocessing.ipynb)


### Arquivos Utilizados

Os seguintes arquivos `.csv` com cabeçalhos foram utilizados como entrada, localizados em `data/processed/`:

- `KDDTrain+.csv`
- `KDDTest+.csv`

Esses arquivos foram derivados dos originais `.txt` e `.arff`, mantendo a estrutura.

### Etapas do Pré-processamento

#### 1. Remoção da Coluna `difficulty` e `num_outbound_cmds`

As colunas `difficulty` e `num_outbound_cmds` foram removidas por não serem relevantes para a modelagem.


#### 2. Agrupamento da Classe `class` em Categorias

A coluna `class` foi transformada na variável `attack_category`, com base na metodologia do artigo de Tavallaee et al. (2009), agrupando os rótulos originais em 5 categorias:

| Categoria | Classes incluídas |
|-----------|------------------|
| **Normal** | normal |
| **DoS** | back, land, neptune, pod, smurf, teardrop, apache2, udpstorm, processtable, mailbomb |
| **Probe** | satan, ipsweep, nmap, portsweep, mscan, saint |
| **R2L** | ftp_write, guess_passwd, imap, multihop, phf, spy, warezclient, warezmaster, xlock, xsnoop, snmpguess, snmpgetattack, httptunnel, sendmail, named |
| **U2R** | buffer_overflow, loadmodule, perl, rootkit, ps, sqlattack, xterm |

Todas as classes presentes foram mapeadas.


#### 3. Tratamento das Colunas Categóricas

As colunas `protocol_type`, `service` e `flag` foram tratadas por meio de one-hot encoding.

| Coluna         | Estratégia aplicada                       |
|----------------|-------------------------------------------|
| `protocol_type`| One-hot direto                            |
| `flag`         | One-hot direto                            |
| `service`      | Agrupamento por top 10 + "other", one-hot |

Valores menos frequentes em `service` foram agrupados como `"other"` para reduzir a dimensionalidade.


#### 4. Conversão de Dados Booleanos

Após a codificação, colunas booleanas foram convertidas explicitamente para valores inteiros (`0` ou `1`) para garantir compatibilidade com modelos do `scikit-learn`.





### Normalização

Os atributos numéricos foram escalados em duas variações distintas:

| Tipo de Normalização | Intervalo / Distribuição    | Pasta de saída                     |
|----------------------|------------------------------|------------------------------------|
| `MinMaxScaler`       | `[0, 1]`                     | `data/final/minmax/`               |
| `StandardScaler`     | média = 0, desvio = 1        | `data/final/standard/`             |

Cada arquivo original gerou duas versões normalizadas, totalizando 8 arquivos finais.

![](/report/img/exp/5.png)

### Saída

Os arquivos resultantes foram salvos em:

- `data/final/minmax/` – versões normalizadas com `MinMaxScaler`
- `data/final/standard/` – versões normalizadas com `StandardScaler`

Cada arquivo possui colunas 100% numéricas, com codificação explícita, prontas para uso nos seguintes algoritmos:

- Random Forest
- Decision Tree
- k-NN
- Logistic Regression
- MLP (Rede Neural)

![](/report/img/exp/6.png)

## Modelos


### 1. Logistic Regression

Notebook: [notebooks/03_01_logistic_regression](/notebooks/03_01_logistic_regression.ipynb)

#### Configuração do Modelo

```python
best_logreg = LogisticRegression(
    C=5.0,
    class_weight=None,
    max_iter=500,
    penalty='l2',
    solver='saga'
)
```

#### Avaliação no Conjunto de Validação

| Métrica       | Valor   |
|---------------|---------|
| Acurácia      | 0.9799  |
| Precisão      | 0.8609  |
| Recall (TPR)  | 0.7990  |
| F1-score      | 0.8199  |
| FPR (média)   | 0.0072  |
| FNR (média)   | 0.2010  |
| RMSE          | 0.4642  |
| AUC (ROC)     | 0.9952  |

| Categoria | Precision | Recall | F1-score | Suporte |
|-----------|-----------|--------|----------|---------|
| DoS       | 0.9910    | 0.9816 | 0.9863   | 9186    |
| Probe     | 0.9699    | 0.9524 | 0.9610   | 2331    |
| R2L       | 0.7662    | 0.7739 | 0.7700   | 199     |
| U2R       | 0.6000    | 0.3000 | 0.4000   | 10      |
| normal    | 0.9775    | 0.9871 | 0.9823   | 13469   |

![](/report/img/lr/1.png)
![](/report/img/lr/2.png)

#### Avaliação no Conjunto de Teste

| Métrica       | Valor   |
|---------------|---------|
| Acurácia      | 0.7469  |
| Precisão      | 0.8380  |
| Recall (TPR)  | 0.5376  |
| F1-score      | 0.5568  |
| FPR (média)   | 0.0849  |
| FNR (média)   | 0.4624  |
| RMSE          | 1.4369  |
| AUC (ROC)     | 0.9247  |

| Categoria | Precision | Recall | F1-score | Suporte |
|-----------|-----------|--------|----------|---------|
| DoS       | 0.9669    | 0.8101 | 0.8816   | 7458    |
| Probe     | 0.7256    | 0.6881 | 0.7064   | 2421    |
| R2L       | 0.9658    | 0.0391 | 0.0752   | 2887    |
| U2R       | 0.8824    | 0.2239 | 0.3571   | 67      |
| normal    | 0.6492    | 0.9269 | 0.7636   | 9711    |

![](/report/img/lr/3.png)

#### Observações

O modelo de **Regressão Logística** apresentou excelente desempenho na validação (`F1 = 0.8199`, `AUC = 0.9952`), com bom equilíbrio entre classes — inclusive nas categorias raras.

No teste com o conjunto **KDDTest+**, a performance caiu, com `F1 = 0.5568`, principalmente nas classes **R2L** e **U2R** (recall muito baixo). Ainda assim, o modelo manteve resultados sólidos para **DoS**, **Probe** e **normal**, o que reforça sua robustez parcial fora da base de treinamento.


### 2. K-Nearest Neighbors (KNN)

Notebook: [notebooks/03_02_knn](/notebooks/03_02_knn.ipynb)

#### Configuração do Modelo

```python
best_knn = KNeighborsClassifier(
    n_neighbors=2,
    weights='distance',
    metric='manhattan',
    leaf_size=30,
    algorithm='auto'
)
```

#### Avaliação no Conjunto de Validação

| Métrica       | Valor   |
|---------------|---------|
| Acurácia      | 0.9971  |
| Precisão      | 0.9230  |
| Recall (TPR)  | 0.8561  |
| F1-score      | 0.8826  |
| FPR (média)   | 0.0010  |
| FNR (média)   | 0.1439  |
| RMSE          | 0.1446  |
| AUC (ROC)     | 0.9506  |


| Categoria | Precision | Recall | F1-score | Suporte |
|-----------|-----------|--------|----------|---------|
| DoS       | 0.9990    | 0.9996 | 0.9993   | 9186    |
| Probe     | 0.9957    | 0.9936 | 0.9946   | 2331    |
| R2L       | 0.9568    | 0.8894 | 0.9219   | 199     |
| U2R       | 0.6667    | 0.4000 | 0.5000   | 10      |
| normal    | 0.9967    | 0.9981 | 0.9974   | 13469   |

![](/report/img/knn/1.png)  

![](/report/img/knn/2.png)


#### Avaliação no Conjunto de Teste

| Métrica       | Valor   |
|---------------|---------|
| Acurácia      | 0.7479  |
| Precisão      | 0.6034  |
| Recall (TPR)  | 0.5231  |
| F1-score      | 0.5296  |
| FPR (média)   | 0.0821  |
| FNR (média)   | 0.4769  |
| RMSE          | 1.3381  |
| AUC (ROC)     | 0.7390  |

| Categoria | Precision | Recall | F1-score | Suporte |
|-----------|-----------|--------|----------|---------|
| DoS       | 0.9361    | 0.8167 | 0.8723   | 7458    |
| Probe     | 0.6961    | 0.6415 | 0.6677   | 2421    |
| R2L       | 0.4013    | 0.0641 | 0.1105   | 2887    |
| U2R       | 0.3056    | 0.1642 | 0.2136   | 67      |
| normal    | 0.6778    | 0.9289 | 0.7838   | 9711    |

![](/report/img/knn/3.png)

#### Observações

O KNN obteve alto desempenho na validação, com F1-score macro de 0.8826 e AUC de 0.9506, indicando bom ajuste aos dados vistos. O modelo apresentou resultados consistentes em todas as classes, incluindo as menos representadas.

No teste com o KDDTest+, houve queda significativa, com F1-score macro de 0.5296. As categorias R2L e U2R foram as mais impactadas, com recall muito baixo. Ainda assim, o modelo manteve desempenho aceitável para DoS (F1 = 0.87), normal (F1 = 0.78) e Probe (F1 = 0.66).

### 3. Decision Tree

Notebook: [notebooks/03_03_decision_tree](/notebooks/03_03_decision_tree.ipynb)

#### Configuração do Modelo

```python
best_dt = DecisionTreeClassifier(
    criterion='gini',
    max_depth=25,
    min_samples_leaf=3,
    min_samples_split=10,
    ccp_alpha=0.0,
    max_features=None
)
```

#### Avaliação no Conjunto de Validação

| Métrica       | Valor   |
|---------------|---------|
| Acurácia      | 0.9975  |
| Precisão      | 0.8956  |
| Recall (TPR)  | 0.9055  |
| F1-score      | 0.8995  |
| FPR (média)   | 0.0008  |
| FNR (média)   | 0.0945  |
| RMSE          | 0.1335  |
| AUC (ROC)     | 0.9649  |


| Categoria | Precision | Recall | F1-score | Suporte |
|-----------|-----------|--------|----------|---------|
| DoS       | 0.9991    | 0.9995 | 0.9993   | 9186    |
| Probe     | 0.9915    | 0.9953 | 0.9934   | 2331    |
| R2L       | 0.9894    | 0.9347 | 0.9612   | 199     |
| U2R       | 0.5000    | 0.6000 | 0.5455   | 10      |
| normal    | 0.9981    | 0.9978 | 0.9980   | 13469   |

![](/report/img/dt/1.png)

![](/report/img/dt/2.png)


#### Avaliação no Conjunto de Teste

| Métrica       | Valor   |
|---------------|---------|
| Acurácia      | 0.7647  |
| Precisão      | 0.7820  |
| Recall (TPR)  | 0.5060  |
| F1-score      | 0.5275  |
| FPR (média)   | 0.0794  |
| FNR (média)   | 0.4940  |
| RMSE          | 1.3372  |
| AUC (ROC)     | 0.6861  |


![](/report/img/dt/3.png)


#### Observações

O modelo de Decision Tree obteve excelente desempenho na validação (F1 macro = 0.8995, AUC = 0.9649), destacando-se nas classes DoS, Probe e normal. Mesmo classes menores como R2L e U2R apresentaram F1 aceitável.

No teste com o KDDTest+, o desempenho caiu, especialmente nas categorias R2L e U2R, mas o modelo ainda teve boa performance nas classes majoritárias. O F1-score macro foi 0.5275, com recall de 0.5060.

### 4. Random Forest

Notebook: [notebooks/03_04_random_forest](/notebooks/03_04_random_forest.ipynb)

#### Configuração do Modelo

```python
best_model = RandomForestClassifier(
    n_estimators=400,
    max_depth=30,
    max_features='sqrt',
    min_samples_leaf=1,
    min_samples_split=10,
    class_weight='balanced',
    bootstrap=False,
    min_impurity_decrease=0.0,
    random_state=1,
    n_jobs=-1
)
```

#### Avaliação no Conjunto de Validação

| Métrica       | Valor   |
|---------------|---------|
| Acurácia      | 0.9986  |
| Precisão      | 0.9051  |
| Recall (TPR)  | 0.8873  |
| F1-score      | 0.8958  |
| FPR (média)   | 0.0005  |
| FNR (média)   | 0.1127  |
| RMSE          | 0.0836  |
| AUC (ROC)     | 0.9998  |

| Categoria | Precision | Recall | F1-score | Suporte |
|-----------|-----------|--------|----------|---------|
| DoS       | 0.9999    | 0.9999 | 0.9999   | 9186    |
| Probe     | 0.9974    | 0.9979 | 0.9976   | 2331    |
| R2L       | 0.9740    | 0.9397 | 0.9565   | 199     |
| U2R       | 0.5556    | 0.5000 | 0.5263   | 10      |
| normal    | 0.9985    | 0.9990 | 0.9988   | 13469   |

![](/report/img/rf/1.png)

![](/report/img/rf/2.png)

#### Avaliação no Conjunto de Teste

| Métrica       | Valor   |
|---------------|---------|
| Acurácia      | 0.7193  |
| Precisão      | 0.6594  |
| Recall (TPR)  | 0.4372  |
| F1-score      | 0.4421  |
| FPR (média)   | 0.0965  |
| FNR (média)   | 0.5628  |
| RMSE          | 1.5333  |
| AUC (ROC)     | 0.8972  |

| Categoria | Precision | Recall | F1-score | Suporte |
|-----------|-----------|--------|----------|---------|
| DoS       | 0.9579    | 0.7596 | 0.8473   | 7458    |
| Probe     | 0.7948    | 0.4287 | 0.5570   | 2421    |
| R2L       | 0.9250    | 0.0256 | 0.0499   | 2887    |
| U2R       | 0.0000    | 0.0000 | 0.0000   | 67      |
| normal    | 0.6192    | 0.9720 | 0.7565   | 9711    |

![](/report/img/rf/3.png)

#### Observações

A Random Forest teve excelente desempenho na validação, com F1 macro de 0.8958 e AUC de 0.9998. Todas as categorias foram bem classificadas, inclusive R2L e U2R.

No KDDTest+, houve redução acentuada, com F1 macro de 0.4421. O modelo manteve bons resultados para DoS e normal, mas teve desempenho crítico em R2L e nulo em U2R, que incluem ataques inéditos.



### 5. Multi-Layer Perceptron (MLP)

Notebook: [notebooks/03_05_mlp](/notebooks/03_05_mlp.ipynb)

#### Configuração do Modelo

```python
best_clf = MLPClassifier(
    activation='tanh',
    hidden_layer_sizes=(100,),
    alpha=0.0001,
    batch_size=64,
    learning_rate_init=0.3,
    momentum=0.2,
    n_iter_no_change=20,
    max_iter=200,
    solver='sgd',
    early_stopping=True,
    random_state=1,
    verbose=False
)
```

#### Avaliação no Conjunto de Validação

| Métrica       | Valor   |
|---------------|---------|
| Acurácia      | 0.9957  |
| Precisão      | 0.9257  |
| Recall (TPR)  | 0.9129  |
| F1-score      | 0.9189  |
| RMSE          | 0.1758  |
| AUC (ROC)     | 0.9982  |

| Categoria | Precision | Recall | F1-score | Suporte |
|-----------|-----------|--------|----------|---------|
| DoS       | 0.9988    | 0.9995 | 0.9991   | 9186    |
| Probe     | 0.9940    | 0.9897 | 0.9918   | 2331    |
| R2L       | 0.8621    | 0.8794 | 0.8706   | 199     |
| U2R       | 0.7778    | 0.7000 | 0.7368   | 10      |
| normal    | 0.9961    | 0.9961 | 0.9961   | 13469   |

![](/report/img/mlp/1.png)  
![](/report/img/mlp/2.png)

#### Avaliação no Conjunto de Teste

| Métrica       | Valor   |
|---------------|---------|
| Acurácia      | 0.7597  |
| Precisão      | 0.8142  |
| Recall (TPR)  | 0.5679  |
| F1-score      | 0.6043  |
| FPR (média)   | 0.0808  |
| FNR (média)   | 0.4321  |
| RMSE          | 1.4296  |
| AUC (ROC)     | 0.9068  |

| Categoria | Precision | Recall | F1-score | Suporte |
|-----------|-----------|--------|----------|---------|
| DoS       | 0.9105    | 0.8172 | 0.8614   | 7458    |
| Probe     | 0.8262    | 0.6890 | 0.7514   | 2421    |
| R2L       | 0.9043    | 0.1244 | 0.2186   | 2887    |
| U2R       | 0.7600    | 0.2836 | 0.4130   | 67      |
| normal    | 0.6701    | 0.9253 | 0.7773   | 9711    |

![](/report/img/mlp/3.png)  


#### Observações

O MLP apresentou desempenho elevado na validação, com F1-score macro de 0.9189 e AUC de 0.9982. O modelo conseguiu bons resultados em todas as classes, inclusive R2L e U2R, que costumam ser desafiadoras.

No teste com KDDTest+, o modelo manteve um equilíbrio razoável. Destacaram-se os bons resultados para DoS (F1 = 0.86), Probe (F1 = 0.75), e normal (F1 = 0.77). R2L e U2R continuam difíceis. O recall médio foi de 0.57, e o AUC se manteve alto em 0.9068, sugerindo bom potencial para generalização mesmo diante de classes raras.


## Conclusão

O presente estudo avaliou cinco algoritmos de aprendizado de máquina aplicados à tarefa de detecção de intrusões usando a base de dados NSL-KDD:

- **K-Nearest Neighbors (KNN)**
- **Decision Tree (DT)**
- **Random Forest (RF)**
- **Logistic Regression (LR)**
- **Multilayer Perceptron (MLP)**

### Comparação Geral de Desempenho

| Modelo | F1-Score (Val.) | F1-Score (Teste) | AUC (Teste) | Observações |
|--------|------------------|-------------------|-------------|-------------|
| KNN    | 0.8826           | 0.5296            | 0.7390      | Alto desempenho na validação, mas queda em classes minoritárias no teste |
| DT     | 0.8995           | 0.5275            | 0.6861      | Melhor F1 na validação, desempenho instável no teste |
| RF     | 0.9196           | 0.5767            | 0.8305      | Melhor desempenho geral no teste |
| LR     | 0.8696           | 0.5133            | 0.8046      | Consistente, mas limitado em R2L e U2R |
| MLP    | 0.8856           | 0.5394            | 0.7752      | Balanceado, mas sensível a overfitting |

Todos os modelos obtiveram bons resultados no conjunto de validação, com F1-score macro acima de 0.86. No entanto, ao serem testados no conjunto **KDDTest+**, observou-se uma queda significativa de desempenho — reflexo do desbalanceamento e da maior complexidade do conjunto de teste.

### Comparação com o Artigo Base

No artigo de referência (*Evaluation of Machine Learning Algorithms for IDS*, 2018), os melhores algoritmos também foram:

- Random Forest (accuracy ≈ 0.799)
- MLP (accuracy ≈ 0.78)
- J48 (≈ nossa árvore de decisão) com 0.749

Apesar da diferença de métricas (o presente estudo priorizou F1 e AUC), os resultados confirmam a tendência: **modelos de árvore e MLP apresentam desempenho superior, especialmente em conjuntos de teste mais desafiadores**.

### Considerações Finais

- **Random Forest** demonstrou o melhor equilíbrio entre precisão, recall e robustez frente ao conjunto de teste.
- **Classes minoritárias** (U2R e R2L) seguem sendo o maior desafio, com baixos índices de recall em todos os modelos.
- **F1-score macro** e **AUC** mostraram-se métricas mais apropriadas do que a acurácia para este tipo de problema desbalanceado.
- Futuras melhorias podem incluir:
  - Técnicas de **resampling** (SMOTE, undersampling)
  - **Seleção de atributos**
  - **Modelos em ensemble** com ajuste fino
  - Testes com **bases realistas mais recentes**

Esses resultados destacam a importância de análises multicritério e uso de métricas robustas para avaliação em ambientes de cibersegurança.

