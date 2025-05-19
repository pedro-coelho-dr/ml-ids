
## Exploração do Dataset

Notebook: [notebooks/01_exploration.ipynb](../notebooks/01_exploration.ipynb)


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
