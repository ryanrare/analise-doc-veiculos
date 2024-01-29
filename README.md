# Título: Análise de veículos em leilões do DETRAN

# Descrição:
 Este código Python é usado para analisar veículos em leilões do DETRAN. O código faz o seguinte:

 * Lê um arquivo de texto que contém os dados dos veículos em leilão.
 * Filtra os veículos que estão em condições de recuperação e com preço menor que um determinado valor.
 * Consulta o DETRAN para obter as multas de cada veículo.
 * Adiciona o valor das multas ao preço do veículo.
 * Salva os dados dos veículos com os débitos incluídos em um arquivo CSV.

# Requisitos:
 * Python 3
 * Pacotes `requests`, `csv`, e `pandas`

# Como usar:
#
# 1. Instale os pacotes necessários:
#
# ```
 pip install requests csv pandas
# 
#
# 2. Defina as variáveis `TOKEN_DETRAN_INFO`, `PRECO_CONDICAO_LEILAO`, `CONDICAO_VEICULO_LEILAO`, `PATH_TXT_EDITAL_DETRAN`, e `PATH_CSV_EDITAL_DETRAN` com os valores apropriados.
#
 python
 TOKEN_DETRAN_INFO = "TOKEN DA INFO SIMPLES"
 PRECO_CONDICAO_LEILAO = 2000
 CONDICAO_VEICULO_LEILAO = "Recuperável"
 PATH_TXT_EDITAL_DETRAN = "CAMINHO ARQUIVO DE TEXTO DO PDF DE EDITAL DO DETRAN"
 PATH_CSV_EDITAL_DETRAN = "CAMINHO ONDE SERA SALVO O ARQUIVO CSV"
# ```
#
# 3. Execute o código:
#
# ```
 python analise_veiculos_leilao.py
# ```

# Exemplo de saída:
#
# ```
 {
   "lote": 1,
   "chassi": "9CDNF41LJ7M052106",
   "placa": "HDY8611",
   "marca": "Fiat",
   "ano": 2015,
   "preco": 15.000,
   "multas_total_valor": 1.200,
   "preco_total": 16.200
 }
# ```

# Observações:
#
# * O arquivo de texto que contém os dados dos veículos em leilão deve ter o seguinte formato:
#
# ```
# lote;chassi;placa;marca;ano;preco
# 1;9CDNF41LJ7M052106;HDY8611;Fiat;2015;15.000
# 2;9CDNF42LJ7M052107;HDY8612;Volkswagen;2016;20.000
# 
#
# * O valor do `TOKEN_DETRAN_INFO` deve ser obtido no site da InfoSimples.
# * O valor do `PRECO_CONDICAO_LEILAO` deve ser definido de acordo com o valor máximo que você está disposto a pagar por um veículo em leilão.
# * O valor do `CONDICAO_VEICULO_LEILAO` deve ser definido como "Recuperável" ou "Não Recuperável".
# * O arquivo CSV que contém os dados dos veículos com os débitos incluídos terá o seguinte formato:
#
# 
# lote;chassi;placa;marca;ano;preco;multas_total_valor;preco_total
# 1;9CDNF41LJ7M052106;HDY8611;Fiat;2015;15.000;1.200;16.200
# 2;9CDNF42LJ7M052107;HDY8612;Volkswagen;2016;20.000;2.400;22.400
# ```
