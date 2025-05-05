import pytest
import pandas as pd
from etl import extrair_dados, transformar_dados


def test_extrair_dados():
    df = extrair_dados()
    assert isinstance(df, pd.DataFrame), "extrair_dados deve retornar um DataFrame"
    assert not df.empty, "DataFrame extraído não pode estar vazio"
    assert {'uf', 'state', 'cases', 'deaths', 'suspects', 'refuses', 'datetime'}.issubset(df.columns), "Colunas esperadas não estão presentes"


def test_transformar_dados():
    df_raw = pd.DataFrame([
        {
            "uf": "SP",
            "state": "São Paulo",
            "cases": 100,
            "deaths": 10,
            "suspects": 5,
            "refuses": 2,
            "datetime": "2023-01-01T00:00:00.000Z"
        }
    ])
    df_tratado = transformar_dados(df_raw)

    assert list(df_tratado.columns) == ['uf', 'estado', 'casos', 'mortes', 'suspeitos', 'recusados', 'data'], "Nomes de colunas não foram transformados corretamente"
    assert pd.api.types.is_datetime64_any_dtype(df_tratado['data']), "Coluna 'data' deve estar no formato datetime"
    assert df_tratado.iloc[0]['estado'] == "São Paulo", "Valor da coluna 'estado' não foi mantido corretamente"
