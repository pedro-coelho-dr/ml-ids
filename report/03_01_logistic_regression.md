
### 1. Logistic Regression

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
