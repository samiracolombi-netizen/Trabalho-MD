import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="App de Língua Portuguesa - Quiz e Ranking", layout="wide")

# -------------------------
# Perguntas (5 por tema)
# -------------------------
QUESTIONS = {
    "Ortografia": [
        {"q": "Escolha a forma correta:", "options": ["Mas", "Mais"], "answer": "Mas", "hint": "contraste"},
        {"q": "Escolha a forma correta:", "options": ["Aonde", "Onde"], "answer": "Onde", "hint": "movimento vs lugar"},
        {"q": "Qual é a ortografia correta?", "options": ["Excessão", "Exceção"], "answer": "Exceção", "hint": "palavra comum"},
        {"q": "Qual grafia está certa?", "options": ["Cigarro", "Cigarre"], "answer": "Cigarro", "hint": "palavra com 'rr'"},
        {"q": "Escolha a forma correta:", "options": ["Conciencia", "Consciência"], "answer": "Consciência", "hint": "com 's' e 'ci'"},
    ],
    "Pontuação": [
        {"q": "Onde colocar a vírgula para separar vocativo?", "options": ["Vamos comer crianças", "Vamos comer, crianças"], "answer": "Vamos comer, crianças", "hint": "vocativo separado por vírgula"},
        {"q": "Escolha a frase com pontuação correta:", "options": ["O menino, que chegou cedo é esperto.", "O menino que chegou cedo, é esperto."], "answer": "O menino, que chegou cedo é esperto.", "hint": "oração explicativa vs restritiva"},
        {"q": "Qual uso do ponto-final está correto?", "options": ["Use ponto no fim de frases declarativas", "Use ponto antes de cada enumeração"], "answer": "Use ponto no fim de frases declarativas", "hint": "fim de sentença"},
        {"q": "Escolha a frase correta com travessão/vírgula:", "options": ["Ela — disse a professora — sorriu.", "Ela disse a professora, sorriu."], "answer": "Ela — disse a professora — sorriu.", "hint": "discurso intercalação"},
        {"q": "Onde vai a vírgula?: 'Entretanto ____ não iremos.'", "options": [",", ""], "answer": ",", "hint": "advérbio deslocado"},
    ],
    "Figuras de Linguagem": [
        {"q": "Exemplo de metáfora:", "options": ["Mar de gente", "Choveu muito"], "answer": "Mar de gente", "hint": "comparação implícita"},
        {"q": "Exemplo de hipérbole:", "options": ["Estou morrendo de sede", "Ele é alto"], "answer": "Estou morrendo de sede", "hint": "exagero intencional"},
        {"q": "Exemplo de ironia:", "options": ["Que ótimo, perdi o ônibus", "O ônibus chegou cedo"], "answer": "Que ótimo, perdi o ônibus", "hint": "dizer o contrário do que se pensa"},
        {"q": "Exemplo de personificação:", "options": ["O vento sussurrou", "Ele comprou pão"], "answer": "O vento sussurrou", "hint": "atribuir ação humana a algo não humano"},
        {"q": "Qual figura é comparar sem usar 'como'?", "options": ["Metáfora", "Comparação (símile)"], "answer": "Metáfora", "hint": "sem 'como'"},
    ],
    "Gramática": [
        {"q": "Identifique o sujeito: 'O gato miou.'", "options": ["O gato", "miou"], "answer": "O gato", "hint": "quem realiza a ação"},
        {"q": "Qual é o predicado: 'Maria estudou ontem.'", "options": ["Maria", "estudou ontem"], "answer": "estudou ontem", "hint": "informa sobre o sujeito"},
        {"q": "Qual é verbo nesta frase: 'Eles correram rápido.'", "options": ["correram", "rápido"], "answer": "correram", "hint": "ação"},
        {"q": "Escolha a forma correta do plural: 'O lápis' ->", "options": ["Os lápis", "Os lápises"], "answer": "Os lápis", "hint": "substantivo terminado em 's'"},
        {"q": "Qual é o pronome na frase 'Ela trouxe seu livro'?", "options": ["Ela", "seu"], "answer": "Ela", "hint": "substitui o nome"},
    ],
}

# -------------------------
# Inicializações de estado
# -------------------------
if 'db' not in st.session_state:
    st.session_state['db'] = {}

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

if 'current_quiz' not in st.session_state:
    st.session_state['current_quiz'] = None

# -------------------------
# Sidebar - navegação
# -------------------------
st.sidebar.title("Menu")
if st.sidebar.button("🏠 Início"):
    st.session_state['page'] = 'home'
if st.sidebar.button("📚 Fazer Quiz"):
    st.session_state['page'] = 'quiz'
if st.sidebar.button("📊 Acompanhamento / Ranking"):
    st.session_state['page'] = 'ranking'

st.sidebar.markdown("---")
st.sidebar.write("Desenvolvido por Samira Colombi - 2025")

# -------------------------
# Funções utilitárias
# -------------------------
def start_quiz(nome, tema, n_questions=5):
    pool = QUESTIONS.get(tema, [])
    questions = random.sample(pool, k=n_questions) if len(pool) >= n_questions else pool.copy()
    st.session_state['current_quiz'] = {
        'name': nome,
        'theme': tema,
        'questions': questions,
        'index': 0,
        'correct_count': 0,
        'answered': 0,
    }

def record_result(nome, tema, answered, correct):
    db = st.session_state['db']
    if nome not in db:
        db[nome] = {'total_points': 0, 'by_theme': {}}
    if tema not in db[nome]['by_theme']:
        db[nome]['by_theme'][tema] = {'answered': 0, 'correct': 0}
    db[nome]['by_theme'][tema]['answered'] += answered
    db[nome]['by_theme'][tema]['correct'] += correct
    db[nome]['total_points'] += correct
    st.session_state['db'] = db

def get_ranking_df():
    rows = []
    for name, info in st.session_state['db'].items():
        rows.append({
            'Aluno': name,
            'Pontuação Total': info.get('total_points', 0),
            'Detalhe (por tema)': "; ".join(
                f"{tema}: {v['correct']}/{v['answered']}"
                for tema, v in info.get('by_theme', {}).items()
            )
        })
    df = pd.DataFrame(rows)
    return df.sort_values('Pontuação Total', ascending=False).reset_index(drop=True) if not df.empty else df

# -------------------------
# PÁGINA: Home
# -------------------------
if st.session_state['page'] == 'home':
    st.title("App de Língua Portuguesa - Quiz e Ranking")
    st.write("Bem-vindo! Use a barra lateral para navegar.")
    st.markdown("### Como funciona")
    st.write("- O aluno informa o **nome** e escolhe um tema.\n- Cada quiz tem **5 perguntas**.\n- Os acertos são somados no **ranking geral**.")

# -------------------------
# PÁGINA: Fazer Quiz
# -------------------------
elif st.session_state['page'] == 'quiz':
    st.title("📚 Fazer Quiz")

    nome = st.text_input("Digite seu nome (ex: Ana):")
    tema = st.selectbox("Escolha o tema do quiz:", options=list(QUESTIONS.keys()))

    if st.button("Iniciar quiz"):
        if not nome.strip():
            st.warning("Por favor, informe seu nome antes de iniciar o quiz.")
        else:
            start_quiz(nome.strip(), tema)
            st.rerun()

    cq = st.session_state.get('current_quiz')
    if cq and cq['name'] == nome.strip():
        q_idx = cq['index']
        q_obj = cq['questions'][q_idx]
        st.write(f"**Pergunta {q_idx + 1}:** {q_obj['q']}")
        choice = st.radio("Escolha:", q_obj['options'])

        if st.button("Confirmar resposta"):
            cq['answered'] += 1
            if choice == q_obj['answer']:
                cq['correct_count'] += 1
                st.success("✅ Correta!")
            else:
                st.error(f"❌ Errada! Resposta correta: {q_obj['answer']}")

            if cq['index'] + 1 < len(cq['questions']):
                cq['index'] += 1
                st.rerun()
            else:
                record_result(cq['name'], cq['theme'], cq['answered'], cq['correct_count'])
                st.session_state['current_quiz'] = None
                st.success(f"Fim do quiz! Você acertou {cq['correct_count']} de {cq['answered']}.")
                st.rerun()

# -------------------------
# PÁGINA: Ranking
# -------------------------
elif st.session_state['page'] == 'ranking':
    st.title("📊 Ranking de Alunos")

    df = get_ranking_df()
    if df.empty:
        st.info("Nenhum resultado registrado ainda.")
    else:
        st.dataframe(df)