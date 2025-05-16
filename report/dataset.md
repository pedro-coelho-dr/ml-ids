# Dataset: NSL-KDD

## Escolha do Dataset

**Dataset Selecionado**: NSL-KDD

**Links Utilizados**:
- [UNB Official NSL-KDD](https://www.unb.ca/cic/datasets/nsl.html)
- [Kaggle - M. Hassan Zaib](https://www.kaggle.com/datasets/hassan06/nslkdd)



## Justificativas Técnicas

1. **NSL-KDD corrige os principais problemas do KDD'99**, removendo redundâncias e balanceando o nível de dificuldade dos exemplos.
2. **Evita viés de overfitting** presente no KDD'99 devido a exemplos duplicados.
3. **Permite avaliação mais confiável de algoritmos**, com resultados mais comparáveis entre diferentes métodos.
4. **Tamanho manejável** para experimentos locais sem necessidade de amostragem adicional.
5. A versão do **Kaggle** é equivalente à original da **UNB**, mas oferece maior praticidade para download e integração em notebooks.



## Formatos Disponíveis

- `.TXT`: Separado por vírgulas, inclui labels e nível de dificuldade.
- `.ARFF`: Pronto para uso com ferramentas como Weka.
- Subconjuntos disponíveis: `KDDTrain+`, `KDDTrain+_20Percent`, `KDDTest+`, `KDDTest-21`.



## Conclusão

O dataset NSL-KDD foi escolhido por ser uma versão corrigida e validada academicamente do KDD'99, com ampla adoção na comunidade. A versão hospedada no Kaggle por M. Hassan Zaib foi selecionada por conveniência e compatibilidade.
