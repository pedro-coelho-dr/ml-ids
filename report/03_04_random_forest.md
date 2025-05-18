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

#### Resultados

