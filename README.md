# Mini-Projeto Avaliativo - Análise Exploratória (Base Varejo)

Este repositório contém a entrega da atividade prática avaliativa referente ao Módulo 1 (Semana 07) da disciplina de **Visualização de Dados e Business Intelligence [Turma T3]**.

## 👤 Identificação do Autor e Turma
* **Nome:** Amilcar
* **Turma:** T3
* **Projeto:** Análise Exploratória da Base Varejo
* **Data:** Agosto de 2026

---

## 📁 Estrutura da Pasta do Projeto
A pasta `Miniprojeto_Amilcar_T3/` está organizada da seguinte forma:
* `analise_varejo.ipynb`: Jupyter Notebook contendo toda a análise, explicações passo a passo e gráficos para visualização de dados.
* `README_Amilcar_T3.md`: Este arquivo com as instruções de execução e reflexão teórica.

---

## 🛠️ Tecnologias e Dependências Utilizadas
O projeto foi desenvolvido em Python 3 utilizando as seguintes bibliotecas:
* **Pandas**: Para a manipulação estruturada do DataFrame (limpeza, filtros, tratamentos e agrupamentos).
* **NumPy**: Para cálculos e operações estatísticas rápidas.
* **Matplotlib**: Para renderização gráfica básica e customização de plotagens.
* **Seaborn**: Para plotagem de gráficos com estilos estatísticos modernos e atraentes.

### Como instalar as dependências:
Abra o seu terminal/prompt de comando na pasta do projeto e execute:
```bash
pip install pandas numpy matplotlib seaborn
```

---

## 🚀 Como Executar o Projeto

### Opção 1: Executando o Script Python (.py)
Para rodar a análise inteira e visualizar o relatório formatado no terminal:
1. Garanta que o arquivo `Base Varejo.csv` esteja localizado na sua pasta de `Downloads` do sistema (`C:\Users\amilcar\Downloads\Base Varejo.csv`) ou no mesmo diretório do script.
2. Execute o comando:
   ```bash
   python analise_varejo.py
   ```
3. O script exportará automaticamente uma base limpa e unificada chamada `df_limpo.csv` no mesmo diretório do arquivo original.

### Opção 2: Executando o Jupyter Notebook (.ipynb)
1. Abra o VS Code (com a extensão *Jupyter* instalada) ou faça upload do arquivo `analise_varejo.ipynb` no **Google Colab**.
2. Certifique-se de que a base de dados esteja acessível.
3. Clique em **Executar Tudo** (*Run All*) para carregar o dataframe, executar as etapas de limpeza e renderizar as visualizações gráficas de vendas.

---

## 🧠 Sprints e Reflexão Teórica da AED

### Sprint 1: Importação e Visão Geral
* **Lógica**: A carga foi feita com a função `pd.read_csv()` do pandas especificando o separador `;` já que o arquivo foi construído com a formatação padrão latino-americana.
* **Diagnóstico Inicial**: A base de varejo original possui mais de 830 mil registros e 13 colunas originais (incluindo algumas colunas vazias sem nome no final do arquivo).

### Sprint 2: Análise de Problemas e Inconsistências
* **Problemas Identificados**:
  1. *Nulos*: Identificação de valores ausentes em colunas como gênero (`CL_GENERO`), número de filhos (`CL_FHL`), estado civil (`CL_EC`) e segmento do cliente (`CL_SEG`).
  2. *Duplicidade*: Mais de 50 mil registros redundantes ou repetidos 100% iguais.
  3. *Formatação de Colunas*: Delimitadores sobressalentes no arquivo CSV criaram colunas fantasmas e sem nome ao final de cada linha (`Unnamed: 10`, etc.).
  4. *Incompatibilidade de Tipos*: A coluna `DATA` armazenava dados textuais, impedindo análises cronológicas/sazonais nativas.

### Sprint 3: Limpeza de Dados
* **Decisão de Limpeza**:
  * As colunas sem nome extras foram excluídas sumariamente para poupar recursos de memória.
  * Registros duplicados foram expurgados para evitar distorção nos volumes de transações reais.
  * A variável discreta `CL_FHL` (número de filhos) teve seus nulos preenchidos com a **mediana** (1), preservando a tendência sem introduzir ruídos significativos como faria a média (que geraria frações de filhos).
  * Variáveis categóricas nulas (`CL_GENERO`, `CL_SEG`, `CL_EC`) receberam a string `"DESCONHECIDO"` para não perdermos outras informações da transação e manter a integridade estatística do cliente.
  * A coluna `DATA` foi convertida com sucesso para `datetime` no formato `%d/%m/%Y`.

### Sprint 4: Estatísticas Descritivas da coluna `CL_FHL` (Número de Filhos)
* **Resultados Obtidos**:
  * **Média**: ~1.39
  * **Mediana**: 1.0
  * **Moda**: 1
  * **Desvio Padrão**: ~1.30
  * **Mínimo**: 0 | **Máximo**: 5
* **Reflexão**: O desvio padrão próximo de 1.30 indica que a maioria dos clientes varia entre 0 e 3 filhos, com comportamento altamente concentrado em famílias menores.

### Sprint 5: Agrupamentos e Insights Principais
* **Agrupamento 1 (Gênero)**: Mostra qual gênero apresenta maior representação no volume de compras no varejo.
* **Agrupamento 2 (Categoria)**: Revela que as categorias de **Alimentos** e **Higiene** são os carros-chefes de movimentação física do varejo analisado.
* **Agrupamento 3 (Temporal)**: Analisa o volume de vendas consolidado por Mês/Ano para monitoramento de sazonalidades.

### Sprint 6: Versionamento
* Envio estruturado de todo o código-fonte, dados tratados (`df_limpo.csv`), notebook e documentação para o GitHub do aluno em repositório público.

