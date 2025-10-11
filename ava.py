# Trabalho-MD
# Trabalho avaliativo
app.py
streamlit
git add .
git commit -m "App Streamlit criado"
git push
import streamlit as st
import pandas as pd
import altair as alt

# --- Cabeçalho do app ---
st.title("App de Língua Portuguesa - por Samira Colombi")
st.write("Bem-vindo! Explore os conteúdos nas colunas abaixo.")

# --- Criação das 4 colunas ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Ortografia")
    st.write("Aprenda a diferença entre **mas** e **mais**.")
    st.write("Ex: Eu queria ir, **mas** estava chovendo.")

with col2:
    st.subheader("Pontuação")
    st.write("Veja a importância da vírgula:")
    st.write("**Vamos comer, crianças!** vs **Vamos comer crianças!**")

with col3:
    st.subheader("Figuras de Linguagem")
    st.write("- Metáfora 🌻")
    st.write("- Hipérbole 💥")
    st.write("- Ironia 😏")

with col4:
    st.subheader("Gramática")
    st.write("Sujeito, verbo e predicado.")
    st.write("Ex: **O gato** (sujeito) **miou** (verbo).")

# --- Base de dados ---
dados = {
    "Aluno": ["Ana", "Bruno", "Carla", "Diego", "Eduarda"],
    "Ortografia": [8.5, 7.0, 9.0, 6.5, 8.0],
    "Pontuação": [9.0, 6.0, 8.5, 7.5, 9.5],
    "Gramática": [7.5, 8.0, 9.0, 6.0, 8.5]
}

df = pd.DataFrame(dados)

st.header("📊 Desempenho dos alunos")
st.dataframe(df)

st.subheader("📈 Estatísticas descritivas")
st.write(df.describe())

# --- Gráfico com Altair ---
df_melted = df.melt(id_vars=["Aluno"], var_name="Categoria", value_name="Nota")

grafico = (
    alt.Chart(df_melted)
    .mark_bar()
    .encode(
        x="Aluno",
        y="Nota",
        color="Categoria",
        tooltip=["Aluno", "Categoria", "Nota"]
    )
)

st.altair_chart(grafico, use_container_width=True)

# --- Rodapé ---
st.markdown("---")
st.caption("Desenvolvido por Samira Colombi 💡")



