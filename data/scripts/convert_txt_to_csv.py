"""
Converte os arquivos .txt do NSL-KDD para .csv com cabeçalho.

O cabeçalho vem do .arff original da UNB (fonte oficial) e tem 43 colunas:
41 features + class + difficulty.

Os .txt não têm cabeçalho, então adicionamos manualmente para facilitar o uso em pandas e ML.
"""

import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)




column_names = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent",
    "hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_host_login","is_guest_login",
    "count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
    "dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","class","difficulty"
]



files = [
    "KDDTrain+.txt",
    "KDDTrain+_20Percent.txt",
    "KDDTest+.txt",
    "KDDTest-21.txt",
]



for file in files:
    raw_path = RAW_DIR / file
    out_path = PROCESSED_DIR / file.replace(".txt", ".csv")

    print(f"Convertendo {raw_path} → {out_path}")
    df = pd.read_csv(raw_path, names=column_names)
    df.to_csv(out_path, index=False)

print("Conversão concluída.")