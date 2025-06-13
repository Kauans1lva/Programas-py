import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Solicitar caminho do arquivo ao usuário
caminho_csv = input("📂 Digite o caminho do arquivo CSV (ex: C:\\Users\\Usuario\\Documentos\\base.csv): ").strip()

# Carregar a base com separador tab
df = pd.read_csv(caminho_csv, sep="\t", encoding="utf-8")

# Corrigir colunas numéricas
colunas_numericas = ["Vendas", "Quantidade", "Desconto", "Lucro"]
for col in colunas_numericas:
    df[col] = df[col].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Estatísticas descritivas
estatisticas = pd.DataFrame({
    "Média": df[colunas_numericas].mean(),
    "Mediana": df[colunas_numericas].median(),
    "Moda": df[colunas_numericas].mode().iloc[0],
    "Desvio Padrão": df[colunas_numericas].std(),
    "Variância": df[colunas_numericas].var(),
    "Mínimo": df[colunas_numericas].min(),
    "Máximo": df[colunas_numericas].max(),
    "Amplitude": df[colunas_numericas].max() - df[colunas_numericas].min(),
    "Coef. Variação (%)": (df[colunas_numericas].std() / df[colunas_numericas].mean()) * 100
}).round(2)
print("\nEstatísticas Descritivas:\n", estatisticas)

# Tabelas de frequência completas para variáveis qualitativas
qualitativas = df.select_dtypes(include='object').columns.tolist()
for col in qualitativas:
    print(f"\n📊 Tabela de Frequência para '{col}':")
    freq_abs = df[col].value_counts()
    freq_rel = (df[col].value_counts(normalize=True) * 100).round(2)
    freq_acum = freq_abs.cumsum()
    freq_rel_acum = freq_rel.cumsum()
    tabela_freq = pd.DataFrame({
        "Frequência Absoluta": freq_abs,
        "Frequência Relativa (%)": freq_rel,
        "Frequência Acumulada": freq_acum,
        "Frequência Relativa Acumulada (%)": freq_rel_acum
    })
    print(tabela_freq)

# Gráficos padrão
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x="Categoria", y="Vendas", estimator=sum, ci=None)
plt.title("Total de Vendas por Categoria")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(data=df, x="Segmento", y="Lucro", estimator=sum, ci=None)
plt.title("Total de Lucro por Segmento")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(data=df, x="Modo de Envio", y="Quantidade", estimator=sum, ci=None)
plt.title("Quantidade por Modo de Envio")
plt.tight_layout()
plt.show()

# Histogramas
df[colunas_numericas].hist(bins=30, figsize=(12, 8))
plt.suptitle("Histogramas das Variáveis Quantitativas")
plt.tight_layout()
plt.show()

# Converter datas para linha do tempo
df["Data do Pedido"] = pd.to_datetime(df["Data do Pedido"], errors="coerce")
df_tempo = df.groupby("Data do Pedido")[["Vendas", "Lucro"]].sum().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(df_tempo["Data do Pedido"], df_tempo["Vendas"], label="Vendas")
plt.plot(df_tempo["Data do Pedido"], df_tempo["Lucro"], label="Lucro")
plt.legend()
plt.title("Evolução de Vendas e Lucro ao Longo do Tempo")
plt.xlabel("Data")
plt.ylabel("Valor")
plt.tight_layout()
plt.show()

# Boxplots
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="Modo de Envio", y="Lucro")
plt.title("Dispersão de Lucro por Modo de Envio")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="Modo de Envio", y="Vendas")
plt.title("Dispersão de Vendas por Modo de Envio")
plt.tight_layout()
plt.show()

# Análise adicional: Região
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x="Região", y="Vendas", estimator=sum, ci=None)
plt.title("Total de Vendas por Região")
plt.tight_layout()
plt.show()

# Margem de lucro
df['Margem (%)'] = (df['Lucro'] / df['Vendas']) * 100
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="Categoria", y="Margem (%)")
plt.title("Margem de Lucro por Categoria")
plt.tight_layout()
plt.show()

# Tempo de entrega
df["Data de Envio"] = pd.to_datetime(df["Data de Envio"], errors="coerce")
df["Prazo de Entrega"] = (df["Data de Envio"] - df["Data do Pedido"]).dt.days
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="Modo de Envio", y="Prazo de Entrega")
plt.title("Prazo de Entrega por Modo de Envio")
plt.tight_layout()
plt.show()

# Frequência de pedidos por cliente
frequencia_clientes = df["ID do Cliente"].value_counts()
plt.figure(figsize=(10, 6))
sns.histplot(frequencia_clientes, bins=20, kde=True)
plt.title("Frequência de Pedidos por Cliente")
plt.xlabel("Número de Pedidos")
plt.ylabel("Quantidade de Clientes")
plt.tight_layout()
plt.show()

# Análise por Subcategoria
df_sub = df.groupby("Subcategoria")["Lucro"].sum().sort_values(ascending=False)
df_sub.plot(kind="bar", figsize=(12, 6), title="Lucro por Subcategoria")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Correlação entre variáveis
plt.figure(figsize=(8, 6))
sns.heatmap(df[["Vendas", "Lucro", "Quantidade", "Desconto"]].corr(), annot=True, cmap="coolwarm")
plt.title("Matriz de Correlação")
plt.tight_layout()
plt.show()

# Outliers: listar top valores
print("\nTop 5 pedidos com maior lucro:")
print(df.sort_values(by="Lucro", ascending=False)[["ID do Pedido", "Lucro", "Produto"]].head())

print("\nTop 5 pedidos com maior desconto:")
print(df.sort_values(by="Desconto", ascending=False)[["ID do Pedido", "Desconto", "Produto"]].head())

