import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="VOID.TECH",
    page_icon="💳",
    layout="wide"
)

# --- LEITURA DO ARQUIVO EXCEL ---
@st.cache_data
def load_data(sheet_name):
    df = pd.read_excel("financialModel.xlsx", sheet_name=sheet_name, header=None)  # Lê o Excel sem cabeçalho
    return df

df = load_data("CardFinancialModel")

# --- FUNÇÃO PARA CRIAR TABELAS ---
def criar_tabela(nome, intervalo):
    with st.expander(nome, expanded=True):
        # Ajuste no intervalo para incluir a última linha e coluna
        tabela_df = df.iloc[intervalo[0] - 1 : intervalo[1], intervalo[2] - 1 : intervalo[3]]

        # Definir o cabeçalho padrão
        tabela_df.columns = ["Void: Anual Projections", "Unit"] + [f"Year {i}" for i in range(1, 6)]

        # # Formatação condicional
        # for col in tabela_df.columns[2:]:  # Começando da terceira coluna
        #     if tabela_df["Unit"].iloc[0] == "R$":
        #         tabela_df[col] = tabela_df[col].apply(lambda x: f"R$ {x:.2f}")
        #     elif tabela_df["Unit"].iloc[0] == "%":
        #         tabela_df[col] = tabela_df[col].apply(lambda x: f"{x:.2f}%")
        #     else:  # Formatação numérica para outros casos (presumindo que seja um número)
        #         tabela_df[col] = tabela_df[col].apply(lambda x: f"{x:.2f}")  # Duas casas decimais

        # Remover o cabeçalho
        tabela_df = tabela_df.style.hide(axis='columns')

        st.table(tabela_df)

# --- LAYOUT DA PÁGINA ---
st.title("VOID.TECH")

# --- ABAS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["CardFinancialModel", "CriptoFinancialModel", "Account", "Original Projection", "Proposed Account", "Proposed Projection"])

with tab1:  # Conteúdo da aba CardFinancialModel
    #  # --- SELECTS ---
    # col1, col2, col3 = st.columns(3)  # Cria 3 colunas de largura igual
    # with col1:
    #     cenario_usuarios = st.selectbox("Users", ["Base", "Upside", "Downside"], index=0)
    # with col2:
    #     cenario_transacoes = st.selectbox("Transactions", ["Base", "Upside", "Downside"], index=0)
    # with col3:
    #     cenario_valor_transacao = st.selectbox("Transaction", ["Base", "Upside", "Downside"], index=0)

    # # --- Dicionário para mapear as opções dos selects para valores numéricos ---
    # cenario_map = {"Base": 1, "Upside": 2, "Downside": 3}

    # # --- Valores numéricos dos cenários ---
    # cenario_usuarios_value = cenario_map[cenario_usuarios]
    # cenario_transacoes_value = cenario_map[cenario_transacoes]
    # cenario_valor_transacao_value = cenario_map[cenario_valor_transacao]
    # print(cenario_usuarios_value, cenario_transacoes_value, cenario_valor_transacao_value)


    # # --- BOTÃO "BUSCAR" ---
    # if st.button("Buscar"):  # Botão que aciona a criação das tabelas
    #     # --- LABELS PARA OS VALORES DAS CÉLULAS ---
    #     st.write(cenario_usuarios_value, cenario_transacoes_value, cenario_valor_transacao_value)

    #     # --- Atualizar os valores das células C6, C8 e C10 ---
    #     df.iloc[5, 2] = cenario_map[cenario_usuarios]
    #     df.iloc[7, 2] = cenario_map[cenario_transacoes]
    #     df.iloc[9, 2] = cenario_map[cenario_valor_transacao]
        
    #     st.write(df.iloc[5, 2], df.iloc[7, 2], df.iloc[9, 2])


    # --- Dicionário para mapear as opções dos selects para valores numéricos ---
    st.title("Credit Card")
    
    # --- TABELAS ---
    criar_tabela("Total # of Active Cardholders", [14, 17, 2, 8])
    criar_tabela("Total # of Transactions", [19, 22, 2, 8])
    criar_tabela("Total Volume", [24, 27, 2, 8])
    criar_tabela("(+) Interchange Fee", [29, 32, 2, 8])
    criar_tabela("(-) Custos únicos", [34, 40, 2, 8])
    criar_tabela("(-) Processing + BIN Sponsorship", [42, 43, 2, 8])
    criar_tabela("(-) Active Card", [50, 51, 2, 8])
    criar_tabela("(-) Franquia Mínima", [58, 59, 2, 8])
    criar_tabela("(-) Outros", [61, 65, 2, 8])
    criar_tabela("Total Costs:", [67, 68, 2, 8])
    criar_tabela("(=) Result - pré bandeira", [70, 71, 2, 8])
    criar_tabela("(-) Bandeira Costs", [73, 82, 2, 8])
    criar_tabela("(=) Result - pós custos bandeira", [104, 105, 2, 8])

    st.title("Cashback")
    criar_tabela("(=) Premium / Cashback Result", [108, 109, 2, 8])
    criar_tabela("(+) Month Fee - Premium Clients", [110, 111, 2, 8])
    criar_tabela("(-) Cashback - Bipa Plus", [112, 113, 2, 8])
    criar_tabela("(-) Cashback - Bipa 'Normal'", [114, 115, 2, 8])
    criar_tabela("(=) Consolidated Unit Economics", [117, 118, 2, 8])


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
            tabela_df = tabela_df.replace(np.nan, '', regex=True)


        # Define o cabeçalho se fornecido
        if cabecalho:
            tabela_df.columns = cabecalho
            

        # Exibe a tabela
        st.table(tabela_df)

with tab2:  # Conteúdo da aba CriptoFinancialModel (vazia por enquanto)
    st.title("Cripto")
    df_cripto = load_data("CriptoFinancialModel")

    cabecalhoUsers=["Usuários", "Unit"] + [f"Month {i}" for i in range(1, 61)]
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
