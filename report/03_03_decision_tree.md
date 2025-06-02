### 3. Decision Tree

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