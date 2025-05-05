# 🦠 Projeto ETL COVID-19 - Brasil

Este projeto implementa um pipeline **ETL** (Extração, Transformação e Carga) que consome dados públicos da COVID-19 no Brasil, realiza backups e os insere em um banco de dados MySQL. Ele também está preparado para envio dos dados para o **Amazon S3** e para execução de **testes automatizados** com `pytest`.

## 🔧 Funcionalidades

- 📥 **Extração** de dados via API pública
- 🔄 **Transformação** e limpeza dos dados com `pandas`
- 💾 **Backup automático** em arquivos `.csv` com timestamp
- 🐘 **Carga dos dados** no MySQL via `SQLAlchemy ORM`
- ☁️ (Opcional) Upload dos backups para **Amazon S3**
- ✅ Estrutura com suporte a testes usando `pytest`

## 🛠 Tecnologias Utilizadas

- [Python 3](https://www.python.org/)
- [pandas](https://pandas.pydata.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [MySQL](https://www.mysql.com/)
- [boto3 (AWS S3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [pytest](https://docs.pytest.org/)

## 📦 Requisitos

- Python 3.8 ou superior
- MySQL Server instalado
- Conta na AWS (para usar o S3)

## ⚙️ Como Executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/seuusuario/etl-covid-brasil.git
   cd etl-covid-brasil
