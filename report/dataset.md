## Dataset Utilizado

O NSL-KDD é uma versão corrigida do KDD'99 criada pelo ISCX (University of New Brunswick) para resolver problemas como redundância e viés em modelos de detecção de intrusão.

A versão **oficial hospedada no site da UNB** não está mais disponível para download direto. Por isso, foi utilizada a versão publicada no **Kaggle** por [M. Hassan Zaib](https://www.kaggle.com/datasets/hassan06/nslkdd), que contém exatamente os mesmos arquivos descritos na documentação original (KDDTrain+, KDDTest+, etc.), com estrutura, colunas e conteúdo idênticos.

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

