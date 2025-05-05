import os
import pandas as pd
import requests
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, Date, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import boto3

# --- Configuração ---
USUARIO = 'root'
SENHA = 'ggzin'
HOST = 'localhost'
PORTA = '3306'
BANCO = 'ETL'
BUCKET_S3 = 'meu-bucket-s3'

# --- Engine SQLAlchemy ---
engine = create_engine(f'mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}')
Session = sessionmaker(bind=engine)

# --- Base ORM ---
Base = declarative_base()

class CovidEstado(Base):
    __tablename__ = 'covid_estados'

    uf = Column(String(2), primary_key=True)
    estado = Column(String(100))
    casos = Column(Integer)
    mortes = Column(Integer)
    suspeitos = Column(Integer)
    recusados = Column(Integer)
    data = Column(Date, primary_key=True)
    carga_timestamp = Column(DateTime)

# --- Extração ---
def extrair_dados():
    url = "https://covid19-brazil-api.now.sh/api/report/v1"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        return pd.DataFrame(dados['data'])
    else:
        raise Exception(f"Erro ao acessar API: {response.status_code}")

# --- Transformação ---
def transformar_dados(df):
    df = df[['uf', 'state', 'cases', 'deaths', 'suspects', 'refuses', 'datetime']].copy()
    df.columns = ['uf', 'estado', 'casos', 'mortes', 'suspeitos', 'recusados', 'data']
    df['data'] = pd.to_datetime(df['data']).dt.date
    df['carga_timestamp'] = datetime.now()
    return df

# --- Backup CSV ---
def salvar_backup_csv(df):
    os.makedirs("backups", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = f"backups/backup_covid_{timestamp}.csv"
    df.to_csv(caminho, index=False)
    print(f"Backup salvo: {caminho}")
    return caminho, timestamp

# --- Upload para S3 ---
def salvar_backup_s3(arquivo_csv, bucket, nome_arquivo):
    s3 = boto3.client('s3')
    s3.upload_file(arquivo_csv, bucket, nome_arquivo)
    print(f"Enviado para S3: s3://{bucket}/{nome_arquivo}")

# --- Carga com ORM ---
def carregar_com_orm(df):
    session = Session()
    for _, row in df.iterrows():
        if not session.query(CovidEstado).filter_by(uf=row['uf'], data=row['data']).first():
            registro = CovidEstado(
                uf=row['uf'],
                estado=row['estado'],
                casos=row['casos'],
                mortes=row['mortes'],
                suspeitos=row['suspeitos'],
                recusados=row['recusados'],
                data=row['data'],
                carga_timestamp=row['carga_timestamp']
            )
            session.add(registro)
    session.commit()
    session.close()
    print("Carga concluída com SQLAlchemy ORM.")

# --- Execução principal ---
if __name__ == "__main__":
    try:
        print("Extraindo dados...")
        df_bruto = extrair_dados()

        print("Transformando...")
        df_tratado = transformar_dados(df_bruto)

        print("Salvando backup...")
        caminho_csv, timestamp = salvar_backup_csv(df_tratado)

        #print("Enviando para S3...")
        #salvar_backup_s3(caminho_csv, BUCKET_S3, f"covid/{os.path.basename(caminho_csv)}")

        print("Carregando no banco de dados...")
        Base.metadata.create_all(engine)
        carregar_com_orm(df_tratado)

    except Exception as e:
        print("Erro no ETL:", e)
