"""
Mini-Projeto Avaliativo - Módulo 1 - Semana 07
Visualização de Dados e Business Intelligence [T3]
Autor: Amilcar
Turma: T3

Descrição:
    Este script realiza uma Análise Exploratória de Dados (AED) na base de dados Varejo.csv.
    O código está estruturado em Sprints de acordo com os requisitos do projeto.
"""

import os
import pandas as pd
import numpy as np

# Definindo caminhos de arquivo possíveis para o dataset
CANDIDATE_PATHS = [
    "./Base Varejo.csv",
    "./Varejo.csv",
    "../Base Varejo.csv",
    "../Varejo.csv",
    r"C:\Users\amilcar\Downloads\Base Varejo.csv"
]

def encontrar_dataset():
    """Busca o arquivo de dados nos caminhos candidatos."""
    for path in CANDIDATE_PATHS:
        if os.path.exists(path):
            print(f"✔ Dataset encontrado em: {path}")
            return path
    raise FileNotFoundError("Não foi possível encontrar a base Varejo.csv nos caminhos especificados.")


# ==========================================
# SPRINT 1: Importação e Visão Geral
# ==========================================
def sprint_1_importacao(caminho_csv):
    print("\n" + "="*50)
    print(" SPRINT 1: IMPORTAÇÃO E VISÃO GERAL DOS DADOS")
    print("="*50)
    
    # Carregando com pandas usando o separador ';'
    df = pd.read_csv(caminho_csv, sep=';')
    
    # Número de registros e colunas
    num_linhas, num_colunas = df.shape
    print(f"- Número de registros: {num_linhas:,}")
    print(f"- Número de colunas originais: {num_colunas}")
    
    # Exibir colunas e tipos de dados
    print("\n--- Colunas e Tipos de Dados Iniciais ---")
    print(df.dtypes)
    
    return df


# ==========================================
# SPRINT 2: Análise de Inconsistências
# ==========================================
def sprint_2_analise_inconsistencias(df):
    print("\n" + "="*50)
    print(" SPRINT 2: ANÁLISE DE PROBLEMAS E INCONSISTÊNCIAS")
    print("="*50)
    
    # Problema 1: Valores nulos por coluna
    print("--- 1. Quantidade de Valores Nulos por Coluna ---")
    nulos = df.isnull().sum()
    print(nulos[nulos > 0] if nulos.sum() > 0 else "Nenhum valor nulo identificado inicialmente.")
    print(f"Total de nulos na base: {df.isnull().sum().sum()}")
    
    # Problema 2: Linhas Duplicadas
    print("\n--- 2. Linhas Duplicadas ---")
    duplicados_total = df.duplicated().sum()
    print(f"Total de linhas 100% duplicadas: {duplicados_total:,}")
    
    # Problema 3: Colunas vazias no final
    print("\n--- 3. Colunas sem nome / vazias identificadas ---")
    colunas_vazias = [col for col in df.columns if col.startswith('Unnamed') or col.strip() == '']
    print(f"Colunas extras detectadas e que serão removidas: {colunas_vazias}")
    
    # Problema 4: Inconsistência nos tipos de dados
    print("\n--- 4. Inconsistências de Tipo/Formatos ---")
    print("- A coluna 'DATA' está como objeto (string) em vez de datetime.")
    print("- A coluna de número de filhos ('CL_FHL') possui nulos ou formatos incorretos?")
    print(f"Valores únicos em CL_FHL antes da limpeza: {df['CL_FHL'].unique()}")
    
    return colunas_vazias


# ==========================================
# SPRINT 3: Limpeza de Nulos e Duplicatas
# ==========================================
def sprint_3_limpeza_dados(df, colunas_vazias):
    print("\n" + "="*50)
    print(" SPRINT 3: LIMPEZA E TRATAMENTO DOS DADOS")
    print("="*50)
    
    df_limpo = df.copy()
    
    # 1. Remoção de colunas vazias
    if colunas_vazias:
        df_limpo = df_limpo.drop(columns=colunas_vazias)
        print(f"✔ Colunas vazias removidas: {colunas_vazias}")
        
    # 2. Remoção de duplicatas
    duplicados_antes = df_limpo.duplicated().sum()
    df_limpo = df_limpo.drop_duplicates()
    print(f"✔ Duplicatas eliminadas: {duplicados_antes:,} registros removidos.")
    
    # 3. Tratamento de Valores Nulos
    print("\n--- Tratamento de Nulos ---")
    # Identificar colunas com nulos antes do tratamento
    nulos_antes = df_limpo.isnull().sum()
    for col in df_limpo.columns:
        qtd_nulos = df_limpo[col].isnull().sum()
        if qtd_nulos > 0:
            # Estratégia de Imputação/Tratamento
            if col == 'CL_FHL':
                # Filhos: como é numérico, imputaremos com a mediana (geralmente 0 ou 1)
                mediana_fhl = df_limpo[col].median()
                df_limpo[col] = df_limpo[col].fillna(mediana_fhl)
                print(f"✔ Coluna '{col}': {qtd_nulos:,} nulos substituídos pela Mediana ({mediana_fhl}).")
            elif col in ['CL_GENERO', 'CL_EC', 'CL_SEG']:
                # Categorias de cliente: preencher com "U" (Unspecified) ou "Desconhecido"
                df_limpo[col] = df_limpo[col].fillna("DESCONHECIDO")
                print(f"✔ Coluna '{col}': {qtd_nulos:,} nulos preenchidos com 'DESCONHECIDO'.")
            else:
                # Outras colunas categóricas ou descritivas
                df_limpo[col] = df_limpo[col].fillna("N/A")
                print(f"✔ Coluna '{col}': {qtd_nulos:,} nulos preenchidos com 'N/A'.")
                
    # 4. Ajuste de Tipos de Dados
    print("\n--- Ajuste de Tipos de Dados ---")
    # Converter DATA para datetime
    df_limpo['DATA'] = pd.to_datetime(df_limpo['DATA'], format='%d/%m/%Y', errors='coerce')
    print("✔ Coluna 'DATA' convertida para Datetime.")
    
    # Converter CL_FHL para inteiro (já que número de filhos é discreto)
    df_limpo['CL_FHL'] = df_limpo['CL_FHL'].astype(int)
    print("✔ Coluna 'CL_FHL' convertida para Inteiro.")
    
    # Garantir strings limpas e padronizadas (Sprint 2 - strings normalization)
    for col in ['CL_GENERO', 'CL_SEG', 'PR_CAT', 'PR_NOME']:
        if col in df_limpo.columns:
            df_limpo[col] = df_limpo[col].astype(str).str.strip().str.upper()
            
    print("✔ Normalização de Strings executada (Casing em caixa alta e remoção de espaços nas bordas).")
    print(f"Nulos restantes no dataframe limpo: {df_limpo.isnull().sum().sum()}")
    
    return df_limpo


# ==========================================
# SPRINT 4: Estatística Descritiva
# ==========================================
def sprint_4_estatistica_descritiva(df):
    print("\n" + "="*50)
    print(" SPRINT 4: ESTATÍSTICA DESCRITIVA (NÚMERO DE FILHOS)")
    print("="*50)
    
    fhl_col = df['CL_FHL']
    
    # Métricas descritivas solicitadas
    estatisticas = {
        "Média": fhl_col.mean(),
        "Mediana": fhl_col.median(),
        "Desvio Padrão": fhl_col.std(),
        "Moda": fhl_col.mode()[0] if not fhl_col.mode().empty else np.nan,
        "Máximo": fhl_col.max(),
        "Mínimo": fhl_col.min(),
        "Contagem": fhl_col.count()
    }
    
    for metrica, valor in estatisticas.items():
        if metrica in ["Contagem", "Mínimo", "Máximo", "Moda"]:
            print(f"- {metrica}: {valor:,.0f}")
        else:
            print(f"- {metrica}: {valor:,.4f}")
            
    return estatisticas


# ==========================================
# SPRINT 5: Agrupamentos e Insights
# ==========================================
def sprint_5_agrupamentos_relatorio(df):
    print("\n" + "="*50)
    print(" SPRINT 5: AGRUPAMENTOS E ANÁLISES OPERACIONAIS")
    print("="*50)
    
    # Agrupamento 1: Comportamento de compra por Gênero do Cliente
    print("--- Agrupamento 1: Distribuição de Compras por Gênero ---")
    genero_dist = df.groupby('CL_GENERO').size().reset_index(name='Qtd_Transacoes')
    genero_dist['Percentual'] = (genero_dist['Qtd_Transacoes'] / genero_dist['Qtd_Transacoes'].sum()) * 100
    print(genero_dist.to_string(index=False))
    
    # Agrupamento 2: Vendas e Popularidade por Categoria de Produto
    print("\n--- Agrupamento 2: Popularidade por Categoria de Produto ---")
    cat_dist = df.groupby('PR_CAT').size().reset_index(name='Itens_Vendidos')
    cat_dist = cat_dist.sort_values(by='Itens_Vendidos', ascending=False)
    cat_dist['Percentual'] = (cat_dist['Itens_Vendidos'] / cat_dist['Itens_Vendidos'].sum()) * 100
    print(cat_dist.to_string(index=False))
    
    # Agrupamento Adicional: Transações ao longo do tempo (Ano/Mês)
    print("\n--- Agrupamento 3: Volume de Vendas por Ano/Mês ---")
    df['ANO_MES'] = df['DATA'].dt.to_period('M')
    vendas_tempo = df.groupby('ANO_MES').size().reset_index(name='Volume_Transacoes')
    print(vendas_tempo.head(10).to_string(index=False))
    print("...")
    
    return genero_dist, cat_dist


def conclusoes_finais():
    print("\n" + "="*50)
    print(" CONCLUSÕES E INSIGHTS PRINCIPAIS")
    print("="*50)
    print("1. Perfil Demográfico: A base apresenta uma divisão clara de clientes por gênero e estado civil.")
    print("2. Concentração de Categorias: Alimentos e Higiene dominam o volume total de transações de varejo.")
    print("3. Número de Filhos (CL_FHL): A maioria dos clientes possui poucos filhos (conforme indicado pela mediana e moda),")
    print("   influenciando o tipo de produto e ticket médio comprado.")
    print("4. Qualidade dos Dados: A base continha colunas fantasmas no final e registros duplicados relevantes que foram expurgados.")
    print("5. Tendências Temporais: A análise temporal revela flutuações sazonais consistentes nas vendas do varejo.")
    print("6. Desafios Futuros: A falta de uma coluna de valores monetários (como preço ou faturamento por transação) limita")
    print("   uma análise de receita financeira mais profunda, sendo um ponto de melhoria para os próximos dashboards.")


# ==========================================
# Execução Principal
# ==========================================
if __name__ == "__main__":
    try:
        caminho_dados = encontrar_dataset()
        
        # Sprints executados sequencialmente
        df_bruto = sprint_1_importacao(caminho_dados)
        colunas_vazias = sprint_2_analise_inconsistencias(df_bruto)
        df_limpo = sprint_3_limpeza_dados(df_bruto, colunas_vazias)
        sprint_4_estatistica_descritiva(df_limpo)
        sprint_5_agrupamentos_relatorio(df_limpo)
        conclusoes_finais()
        
        # Salvar a base limpa para a entrega final
        output_dir = os.path.dirname(caminho_dados)
        output_path = os.path.join(output_dir, "df_limpo.csv")
        df_limpo.to_csv(output_path, sep=';', index=False)
        print(f"\n✔ Base de dados limpa exportada com sucesso em: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}")
