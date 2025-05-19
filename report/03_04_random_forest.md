### 4. Random Forest

#### Hiperparâmetros testados

| Hiperparâmetro           | Valores testados                                    |
|--------------------------|-----------------------------------------------------|
| `n_estimators`           | [100, 200, 300, 400, 500]                           |
| `max_depth`              | [None, 10, 20, 30, 40, 50]                          |
| `min_samples_leaf`       | [1, 2, 5, 10]                                       |
| `min_samples_split`      | [2, 5, 10, 20]                                      |
| `max_features`           | ['sqrt', 'log2', 0.5]                               |
| `class_weight`           | [None, 'balanced']                                 |
| `bootstrap`              | [True, False]                                      |
| `min_impurity_decrease`  | [0.0, 0.001, 0.01]                                  |


##### Iterações e Resultados

###### Iteração 1: Grid amplo inicial
- Testou combinações padrão (sem bootstrap/min_impurity)
- `n_estimators=100`, `max_depth=None`, `min_samples_leaf=1`, `min_samples_split=5`, `max_features='sqrt'`, `class_weight='balanced'`

###### Iteração 2: Expansão para estimators e max_depth
- Foco em `n_estimators` maiores e `max_depth`
- `n_estimators=400`, `max_depth=40`, `min_samples_leaf=1`, `min_samples_split=5`, `max_features=0.5`, `class_weight='balanced'`

###### Iteração 3: Foco em `sqrt`, `max_depth` e `n_estimators`
- Ajuste fino com `max_depth ∈ [30, 40, 50]`
- `n_estimators=500`, `max_depth=30`, `min_samples_leaf=1`, `min_samples_split=5`, `class_weight='balanced'`

###### Iteração 4: Ajuste de `min_samples_leaf` e `min_samples_split`
- Teste combinado dos dois
- Melhor resultado com `min_samples_leaf=1`, `min_samples_split=5`

###### Iteração 5: `bootstrap` e `min_impurity_decrease`
- Teste de regularização


- **Melhor combinação final:**
  ```python
  bootstrap=False
  min_impurity_decrease=0.0
  class_weight='balanced'
  max_depth=30
  max_features='sqrt'
  min_samples_leaf=1
  min_samples_split=10
  n_estimators=400
  ```

#### Avaliação com Hiperparâmetros Otimizados

O modelo com a melhor configuração foi treinado e validado com 20% dos dados (`KDDTrain+`) separados via `train_test_split` estratificado.

##### Métricas globais de desempenho:

| Métrica     | Valor   |
|-------------|---------|
| Acurácia    | 0.9986  |
| F1-score    | 0.8958  |
| Recall (TPR)| 0.8873  |
| Precisão    | 0.9051  |
| FPR média   | 0.0005  |
| FNR média   | 0.1127  |
| RMSE        | 0.0836  |
| AUC (ROC)   | 0.9998  |

##### Desempenho por categoria (F1-score):

- **DoS:** 0.9999  
- **Probe:** 0.9976  
- **R2L:** 0.9565  
- **U2R:** 0.5263  
- **normal:** 0.9988  

> O modelo tem desempenho excelente nas categorias majoritárias (DoS, Probe, normal) e bom desempenho em R2L. A categoria U2R, por ter poucos exemplos, permanece desafiadora.

##### Avaliação binária (normal vs. ataque):

- **Precisão ataque:** 0.9989  
- **Recall ataque:** 0.9983  
- **F1-score ataque:** 0.9986  

> O modelo apresenta altíssimo desempenho para a tarefa binária de detecção de intrusão, com apenas 33 erros em mais de 25 mil amostras.

#### Avaliação com `KDDTest+` (Conjunto de Teste Real)

O modelo final, treinado com os melhores hiperparâmetros e todo o conjunto `KDDTrain+`, foi avaliado com o conjunto de teste real `KDDTest+`, que contém **classes adicionais não presentes no treino**.

##### Métricas globais de desempenho:

| Métrica     | Valor   |
|-------------|---------|
| Acurácia    | 0.7193  |
| F1-score    | 0.4421  |
| Recall (TPR)| 0.4372  |
| Precisão    | 0.6594  |
| FPR média   | 0.0965  |
| FNR média   | 0.5628  |
| RMSE        | 1.5333  |
| AUC (ROC)   | 0.8972  |

> Comparado à validação com `train_test_split`, o desempenho caiu consideravelmente — reflexo direto da presença de 15 classes inéditas no teste e da diferença de distribuição entre treino e teste.

##### Desempenho por categoria:

| Categoria | Precisão | Recall | F1-score | Suporte |
|-----------|----------|--------|----------|---------|
| **DoS**   | 0.958    | 0.760  | 0.847    | 7458    |
| **Probe** | 0.795    | 0.429  | 0.557    | 2421    |
| **R2L**   | 0.925    | 0.026  | 0.050    | 2887    |
| **U2R**   | 0.000    | 0.000  | 0.000    | 67      |
| **normal**| 0.619    | 0.972  | 0.756    | 9711    |

> O modelo se mantém forte em **DoS** e **normal**, mas falha gravemente em **R2L** e **U2R**. Isso evidencia a dificuldade em generalizar para classes raras não vistas no treino.

##### Interpretação:

- A **queda nas métricas é esperada** e alinhada com o comportamento de modelos supervisionados expostos a novas classes no teste.
- A alta taxa de **falsos negativos (FNR = 56%)** mostra que muitos ataques passaram despercebidos.
- A matriz de confusão indica que o modelo tende a classificar ataques raros como `normal`, o que reduz o recall.

##### Conclusão:

O modelo se mostra robusto para ataques comuns e tráfego legítimo, mas sua capacidade de generalização ainda é limitada para classes com baixa ou nenhuma representação no treino. Esse comportamento reforça a importância de avaliar não apenas com `train_test_split`, mas com conjuntos de teste reais e desbalanceados como o `KDDTest+`.

