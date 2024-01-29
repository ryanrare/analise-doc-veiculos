import requests
import csv
import pandas as pd

TOKEN_DETRAN_INFO = "TOKEN DA INFO SIMPLES"
PRECO_CONDICAO_LEILAO = 2000
CONDICAO_VEICULO_LEILAO = 'Recuperável'
PATH_TXT_EDITAL_DETRAN = 'CAMINHO ARQUIVO DE TEXTO DO PDF DE EDITAL DO DETRAN'
PATH_CSV_EDITAL_DETRAN = 'CAMINHO ONDE SERA SALVO O ARQUIVO CSV'

LOTE_DF = 1
CHASSI_DF = 4
PLACA_DF = 5
MARCA_DF = 6
ANO_DF = 8
PRECO_DF = 10

dados_veiculo = {
    "placa": "HDY8611",
    "chassi": "9CDNF41LJ7M052106",
}


def consulta_multas_mg(dados_para_consulta):
    url = 'https://api.infosimples.com/api/v2/consultas/detran/mg/multas-descritivos'
    args = {
        "placa": dados_para_consulta['placa'],
        "chassi": dados_para_consulta['chassi'],
        "token": TOKEN_DETRAN_INFO,
        "timeout": 300
    }

    response = requests.post(url, args)
    response_json = response.json()
    response.close()

    if response_json['code'] == 200:
        return response_json['data'][0]['multas']
    else:
        return None


def create_csv_veiculos_from_txt(path):
    # path ex path_txt = '/home/ryan/estudos/projeto_leilao/exemplopdf.txt'
    with open(path, "r") as f:
        dados = f.readlines()

    with open("dados.csv", "w") as f:
        writer = csv.writer(f)
        for linha in dados:
            linha = linha.replace("R$,", "PRECO ")
            linha = linha.replace("\n", "")
            writer.writerow(linha.split(" "))


def get_recuperavel_preco_csv(path_csv, condicao_veiculo_leilao, preco_maximo_leilao):
    df = pd.read_csv(path_csv)

    veiculos_recuperavel = df[df["CONDIÇÃO"] == condicao_veiculo_leilao]
    lista_veiculos = []

    for veiculo in veiculos_recuperavel.itertuples():
        preco_str = veiculo[PRECO_DF]
        preco = int(preco_str.split(',')[0].replace('.', ''))
        if preco < preco_maximo_leilao:
            dicionario = {
                "lote": veiculo[LOTE_DF],
                "chassi": veiculo[CHASSI_DF],
                "placa": veiculo[PLACA_DF],
                "marca": veiculo[MARCA_DF],
                "ano": veiculo[ANO_DF],
                "preco": preco_str.split(',')[0],
            }
            lista_veiculos.append(dicionario)

    return lista_veiculos

def get_debitos_veiculos(veiculos):
    debitos_veiculo = []
    for veiculo in veiculos:
        multas = consulta_multas_mg(veiculo)
        if multas:
            multas_df = pd.DataFrame(multas)
            total_multas = multas_df['normalizado_valor'].sum().round(0) if multas_df['normalizado_valor'].any() > 0 else 0
            preco_total = float(veiculo['preco'].replace('.', '')) + total_multas
            veiculo['multas_total_valor'] = total_multas
            veiculo['preco_total'] = preco_total.round(2)
            debitos_veiculo.append(veiculo)

    return debitos_veiculo


def run():
    create_csv_veiculos_from_txt(PATH_TXT_EDITAL_DETRAN)
    veiculos_precos_edital = get_recuperavel_preco_csv(PATH_CSV_EDITAL_DETRAN, CONDICAO_VEICULO_LEILAO, PRECO_CONDICAO_LEILAO)
    veiculos_precos_debitos = get_debitos_veiculos(veiculos_precos_edital)
    try:
        precos_veiculos_csv = pd.DataFrame(veiculos_precos_debitos)
        precos_veiculos_csv.to_csv('dados_automotizados')
    except:
        print('deu erro com o csv final de veiculos')
    finally:
        for veiculo in veiculos_precos_debitos:
            print(veiculo)

run()