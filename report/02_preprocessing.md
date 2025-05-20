## Pré-processamento

Notebook: [notebooks/02_preprocessing.ipynb](../notebooks/02_preprocessing.ipynb)


### Arquivos Utilizados

Os seguintes arquivos `.csv` com cabeçalhos foram utilizados como entrada, localizados em `data/processed/`:

- `KDDTrain+.csv`
- `KDDTest+.csv`

Esses arquivos foram derivados dos originais `.txt` e `.arff`, mantendo a estrutura com 43 colunas.

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

