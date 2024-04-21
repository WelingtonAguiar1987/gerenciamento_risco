# BIBLIOTECAS IMPORTADAS:
import pandas as pd
import numpy as np
import pandas as pd
import datetime
from datetime import timedelta
import streamlit as st
import time


# SIGLA E NOME DO ATIVO ANALISADO:
sigla_ativo = "MNQ=F"
nome_ativo = "NASDAQ 100 FUTUROS"

# CONFIGURAÇÃO DA PÁGINA:
st.set_page_config(page_title='GERENCIAMENTO DE RISCO', page_icon='	:warning:', layout='wide')

 

# DICIONÁRIO DOS ATIVOS FUTUROS OPERADOS:
futuros = {
    'MICRO NASDAQ': {'sigla': 'MNQ=F', 'tick': 0.25, 'valor tick': 0.50},
    'MINI NASDAQ': {'sigla': 'NQ=F', 'tick': 0.25, 'valor tick': 5.00},
    'MICRO S&P500': {'sigla': 'MES=F', 'tick': 0.25, 'valor tick': 1.25},
    'MINI S&P500': {'sigla': 'ES=F', 'tick': 0.25, 'valor tick': 12.50},
    'MICRO DOW JONES': {'sigla': 'MYM=F', 'tick': 1.00, 'valor tick': 0.50},
    'MINI DOW JONES': {'sigla': 'YM=F', 'tick': 1.00, 'valor tick': 5.00},   
    'MICRO RUSSELL2000': {'sigla': 'M2K=F', 'tick': 0.10, 'valor tick': 0.50},
    'MINI RUSSELL2000': {'sigla': 'RTY=F', 'tick': 0.10, 'valor tick': 5.00},  
    'MICRO OURO': {'sigla': 'MGC=F', 'tick': 0.10, 'valor tick': 1.00},
    'MINI OURO': {'sigla': 'GC=F', 'tick': 0.10, 'valor tick': 10.00},
    'MICRO PETRÓLEO WTI': {'sigla': 'MCL=F', 'tick': 0.01, 'valor tick': 100.00}
  
}

# Criação e configuração das variáveis
st.markdown("<h1 style='text-align: center; color: white;'>GERENCIAMENTO DE RISCO ⚠️</h1>", unsafe_allow_html=True)
ativo = st.selectbox("Ativo Operado:", list(futuros.keys()))
tipo_operacao = st.selectbox("Posição Aberta:", ["COMPRA", "VENDA"])
preco_abertura_posicao = float(st.number_input("Preço Abertura de Posição:", format="%.2f"))
preco_stop = float(st.number_input("Preço do Stop:", format="%.2f"))
preco_alvo = float(st.number_input("Preço do Alvo:", format="%.2f"))

# CONDICIONAL PARA SELECIONAR CONTRATOS, BARRIS OU ONÇAS TROY:
if ativo == 'MICRO NASDAQ':
    total_contratos = int(st.number_input("Quantidade Contratos:", min_value=0, max_value=85))
    
elif ativo == 'MINI NASDAQ':
    total_contratos = int(st.number_input("Quantidade Contratos:", min_value=0, max_value=17))
 
elif ativo == 'MICRO S&P500':
    total_contratos = int(st.number_input("Quantidade Contratos:", min_value=0, max_value=85)) 
    
elif ativo == 'MINI S&P500':
    total_contratos = int(st.number_input("Quantidade Contratos:", min_value=0, max_value=17))
    
elif ativo == 'MICRO DOW JONES':
    total_contratos = int(st.number_input("Quantidade Contratos:", min_value=0, max_value=17)) 
    
elif ativo == 'MINI DOW JONES':
    total_contratos = int(st.number_input("Quantidade Contratos:", min_value=0, max_value=17))   

elif ativo == 'MICRO RUSSELL2000':
    total_contratos = int(st.number_input("Quantidade Contratos:", min_value=0, max_value=17))
    
elif ativo == 'MINI RUSSELL2000':
    total_contratos = int(st.number_input("Quantidade Contratos:", min_value=0, max_value=17))   
   
elif ativo == 'MICRO OURO':
    total_contratos = float(st.number_input("Quantidade Fracionada da Onças Troy:", min_value=0.01, max_value=1.000))
    
elif ativo == 'MINI OURO':
    total_contratos = float(st.number_input("Quantidade Fracionada da Onças Troy:", min_value=0.01, max_value=1.000))
    
elif ativo == 'MICRO PETRÓLEO WTI':
    total_contratos = float(st.number_input("Quantidade Fracionada do Barril:", min_value=0.01, max_value=1.000))    
         
if total_contratos == 0:
    st.error('SELECIONE UMA QUANTIDADE DE CONTRATOS PARA GERAR O CÁLCULO!')

       
capital_total = float(st.number_input("Capital Total da Conta:", format="%.2f"))



# Função para calcular e exibir os resultados
def calculate():
    ativo_detalhes = futuros[ativo]
    ponto_tick = 4  # Ajuste conforme necessário

    # Calcula os alvos e stops
    if tipo_operacao == 'COMPRA':
        alvo = preco_alvo - preco_abertura_posicao
        stop = preco_abertura_posicao - preco_stop
    elif tipo_operacao == 'VENDA':
        alvo = preco_abertura_posicao - preco_alvo
        stop = preco_stop - preco_abertura_posicao

    # Calcula o lucro e a perda
    lucro = ((ativo_detalhes['valor tick'] * ponto_tick) * abs(alvo)) * total_contratos
    perda = ((ativo_detalhes['valor tick'] * ponto_tick) * abs(stop)) * total_contratos

    # Calcula a variação de lucro e perda com base no capital total
    var_lucro = (lucro / capital_total) * 100
    var_perda = (perda / capital_total) * 100

    # Calcula o Payoff
    try:
        payoff = lucro / perda
    except ZeroDivisionError:
        payoff = "indefinido"

    # Exibe os resultados
    st.write(f'Nesta {tipo_operacao.upper()} o seu ALVO é de {abs(alvo):.2f} pontos, com LUCRO de US$ {lucro:.2f}.')
    st.write(f'Nesta {tipo_operacao.upper()} o seu STOP é de {abs(stop):.2f} pontos, com PERDA de US$ {perda:.2f}.')
    st.write(f'O PAYOFF desta operação é {payoff:.2f}.')
    st.write(f'A variação de LUCRO em relação ao capital total é de {var_lucro:.2f}%.')
    st.write(f'A variação de PERDA em relação ao capital total é de {var_perda:.2f}%.')
   

# Botão para calcular
if st.button('Calcular'):
    calculate()
    

    

    

