import os
import pandas as pd
import arff  # do liac-arff

pasta_script = os.path.dirname(os.path.abspath(__file__))
pasta_arff = os.path.join(pasta_script, 'arff_files')

print("Pasta ARFF:", pasta_arff)
print("Arquivos na pasta:", os.listdir(pasta_arff))

for nome_arquivo in os.listdir(pasta_arff):
    if nome_arquivo.endswith('.arff'):
        caminho_completo = os.path.join(pasta_arff, nome_arquivo)

        with open(caminho_completo, 'r') as f:
            arff_data = arff.load(f)
        
        # extrai os dados
        data = arff_data['data']
        attributes = [attr[0] for attr in arff_data['attributes']]
        
        # cria DataFrame
        df = pd.DataFrame(data, columns=attributes)
        
        # Decodifica se houver bytes
        df = df.applymap(lambda x: x.decode() if isinstance(x, bytes) else x)
        
        nome_csv = nome_arquivo.replace('.arff', '.csv')
        caminho_csv = os.path.join(pasta_arff, nome_csv)
        
        df.to_csv(caminho_csv, index=False)
        print(f'Convertido: {nome_arquivo} -> {nome_csv}')
