### 4. Random Forest

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