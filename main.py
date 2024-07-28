import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="VOID.TECH",
    page_icon="💳",
    layout="wide"
)

# --- LEITURA DO ARQUIVO EXCEL ---
@st.cache_data
def load_data(sheet_name, file_name="financialModel.xlsx"):
    df = pd.read_excel(file_name, sheet_name=sheet_name, header=None)  # Lê o Excel sem cabeçalho
    return df

df = load_data("CardFinancialModel")

ticker = yf.Ticker("BRL=X")
todays_data = ticker.history(period='1d')
dollar = todays_data['Close'].iloc[0]

# --- FUNÇÃO PARA CRIAR TABELAS ---
def criar_tabela(nome, intervalo):
    with st.expander(nome, expanded=True):
        # Ajuste no intervalo para incluir a última linha e coluna
        tabela_df = df.iloc[intervalo[0] - 1 : intervalo[1], intervalo[2] - 1 : intervalo[3]]

        # Definir o cabeçalho padrão
        tabela_df.columns = ["Void: Anual Projections", "Unit"] + [f"Year {i}" for i in range(1, 6)]

        colunas_multiplicar = tabela_df.columns[2:]  # Terceira coluna em diante

        for col in colunas_multiplicar:
            tabela_df[col] = tabela_df.apply(
                lambda row: f"{row[col] * 100:.2f}%"
                if row["Unit"] == "%"
                else f"{row[col] / dollar:,.2f} USD"
                if row["Unit"] == "R$"
                else f"{row[col] / dollar:,.2f}",
                axis=1,
            )
        tabela_df['Unit'] = tabela_df['Unit'].apply(lambda x: 'USD' if x == 'R$' else x)
        st.dataframe(tabela_df, use_container_width=True)

def criar_tabela_aba(df, nome, intervalo, cabecalho=None, remove_blank=False):
    """
    Cria uma tabela Streamlit para dados de criptomoedas, com um expander.

    Args:
        df: DataFrame contendo os dados.
        nome: Título do expander da tabela.
        intervalo: Lista [linha_inicial, linha_final, coluna_inicial, coluna_final].
        cabecalho: Lista com os nomes das colunas (opcional).
    """
    with st.expander(nome, expanded=True):
        # Ajuste no intervalo para incluir a última linha e coluna
        tabela_df = df.iloc[intervalo[0] - 1 : intervalo[1], intervalo[2] - 1 : intervalo[3]]
        

        if remove_blank:
            print("remove")
            tabela_df = tabela_df.replace(np.nan, '', regex=True)

        # Define o cabeçalho se fornecido
        if cabecalho:
            tabela_df.columns = cabecalho

        colunas_multiplicar = tabela_df.columns[2:]  # Terceira coluna em diante

        for col in colunas_multiplicar:
            tabela_df[col] = tabela_df.apply(
                lambda row: (
                    f"{row[col] * 100:.2f}%"
                    if row["Unit"] == "%"
                    else f"{row[col] / 5.66:,.2f} USD"
                    if row["Unit"] == "R$"
                    else (f"{row[col]:,.2f}" if isinstance(row[col], (int, float)) else row[col])
                ),
                axis=1,
            )
            

        # Exibe a tabela
        def highlight_negatives(val):
            color = "lightcoral" if str(val).startswith("-") else ""
            return f"color: {color}"
        tabela_df['Unit'] = tabela_df['Unit'].apply(lambda x: 'USD' if x == 'R$' else x)

        # tabela_formatada = tabela_df.style.applymap(highlight_negatives, subset=colunas_multiplicar)
        tabela_formatada = tabela_df.style.map(highlight_negatives, subset=colunas_multiplicar)  # Substituição do applymap por map
        

        st.dataframe(tabela_formatada, use_container_width=True)

# --- LAYOUT DA PÁGINA ---
st.title("VOID.TECH")

# --- ABAS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["CardFinancialModel", "CriptoFinancialModel", "Account", "Original Projection", "Proposed Account", "Proposed Projection"])

with tab1:  # Conteúdo da aba CardFinancialModel  
    # cenario_usuarios = st.selectbox("Select Scenario", ["Base", "Upside", "Downside"], index=0)
    # cenario_map = {"Base": 1, "Upside": 2, "Downside": 3}

    # if st.button("Atualizar"):  # Botão que aciona a criação das tabelas
    #     st.write("Você clicou no botão!")

    # --- Dicionário para mapear as opções dos selects para valores numéricos ---
    st.title("Credit Card")
    
    # --- TABELAS ---
    criar_tabela("Total # of Active Cardholders", [14, 17, 2, 8])
    criar_tabela("Total # of Transactions", [19, 22, 2, 8])
    criar_tabela("Total Volume", [24, 27, 2, 8])
    criar_tabela("(+) Interchange Fee", [29, 32, 2, 8])
    criar_tabela("(-) Unique Costs", [34, 40, 2, 8])  # "Custos únicos" traduzido
    criar_tabela("(-) Processing + BIN Sponsorship", [42, 43, 2, 8])
    criar_tabela("(-) Active Card", [50, 51, 2, 8])
    criar_tabela("(-) Minimum Franchise", [58, 59, 2, 8])  # "Franquia Mínima" traduzido
    criar_tabela("(-) Others", [61, 65, 2, 8])
    criar_tabela("Total Costs:", [67, 68, 2, 8])
    criar_tabela("(=) Result - pre flag", [70, 71, 2, 8])  # "pré bandeira" traduzido
    criar_tabela("(-) Flag Costs", [73, 82, 2, 8])  # "Bandeira Costs" traduzido
    criar_tabela("(=) Result - post flag costs", [104, 105, 2, 8])  # "pós custos bandeira" traduzido

    st.title("Cashback")
    criar_tabela("(=) Premium / Cashback Result", [108, 109, 2, 8])
    criar_tabela("(+) Month Fee - Premium Clients", [110, 111, 2, 8])
    criar_tabela("(-) Cashback - Bipa Plus", [112, 113, 2, 8])
    criar_tabela("(-) Cashback - Bipa 'Normal'", [114, 115, 2, 8])
    criar_tabela("(=) Consolidated Unit Economics", [117, 118, 2, 8])

with tab2:  # Conteúdo da aba CriptoFinancialModel (vazia por enquanto)
    st.title("Crypto")
    df_cripto = load_data("CriptoFinancialModel")

    cabecalhoUsers=["Users", "Unit"] + [f"Month {i}" for i in range(1, 61)]
    criar_tabela_aba(df_cripto, "Users", [11, 13, 2, 63], cabecalho=cabecalhoUsers)

    cabecalhoCriptoT=["Cripto Transactions", "Unit"] + [f"Month {i}" for i in range(1, 61)]
    criar_tabela_aba(df_cripto, "Cripto Transactions", [16, 16, 2, 63], cabecalho=cabecalhoCriptoT)

    cabecalhoCriptoF=["% Cripto Fee", "Unit"] + [f"Month {i}" for i in range(1, 61)]
    criar_tabela_aba(df_cripto, "% Cripto Fee", [24, 24, 2, 63], cabecalho=cabecalhoCriptoF)

    cabecalhoTotal=["Total", "Unit"] + [f"Month {i}" for i in range(1, 61)]
    criar_tabela_aba(df_cripto, "Total", [29, 31, 2, 63], cabecalho=cabecalhoTotal)
  

with tab3:
    st.title("Account")

    df_cripto = load_data("Conta")

    cabecalhoUsers=["Title", "Unit"] + [f"Month {i}" for i in range(1, 61)]
    criar_tabela_aba(df_cripto, "Users", [10, 22, 2, 63], cabecalho=cabecalhoUsers, remove_blank=True)
with tab4:
    st.title("Original Projection")

    df_cripto = load_data("Projecao-Original")

    cabecalhoUsers=["Title", "Unit"] + [f"Year {i}" for i in range(1, 6)]
    criar_tabela_aba(df_cripto, "Users", [5, 19, 2, 8], cabecalho=cabecalhoUsers, remove_blank=True)
with tab5:
    st.title("Proposed Account")

    df_cripto = load_data("Conta-Proposta")

    cabecalhoUsers=["Title", "Unit"] + [f"Month {i}" for i in range(1, 61)]
    criar_tabela_aba(df_cripto, "Users", [10, 22, 2, 63], cabecalho=cabecalhoUsers, remove_blank=True)
with tab6:
    st.title("Proposed Projection")

    df_cripto = load_data("Projecao-Proposta")

    cabecalhoUsers=["Title", "Unit"] + [f"Year {i}" for i in range(1, 6)]
    criar_tabela_aba(df_cripto, "Users", [4, 18, 2, 8], cabecalho=cabecalhoUsers, remove_blank=True)
