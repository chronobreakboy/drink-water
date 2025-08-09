import streamlit as st
from datetime import date

st.set_page_config(page_title="Hidrata, princesinha 💖", layout="centered")

# ---------------- CSS cute + mobile ----------------
st.markdown("""
<style>
:root{
  --bg: #ffe9ef;           /* rosinha fundo */
  --card: #fff7d6;         /* amarelinho pastel */
  --accent: #ffb3c7;       /* rosa botão */
  --accent-2: #ffd3a3;     /* pêssego */
  --text: #5a4b57;
  --shadow: 0 8px 20px rgba(255, 126, 160, .25);
  --radius: 18px;
}

html, body, [data-testid="stAppViewContainer"]{
  background: linear-gradient(180deg, #ffd7e5 0%, #ffe9ef 30%, #fff7f9 100%);
}

.main, [data-testid="stAppViewContainer"] > .main{
  padding-top: 8px;
}

.container{
  max-width: 460px;        /* largura pensada pro mobile; expande bem no desktop */
  margin: 0 auto;
}

.cute-window{
  background: var(--card);
  border: 3px solid #f2d278;
  border-radius: 14px;
  box-shadow: var(--shadow);
  overflow: hidden;
}

.cute-titlebar{
  background: #ffe6a8;
  padding: 10px 14px;
  display:flex; align-items:center; gap:8px;
  font-weight:700; color:#7a5d00;
  letter-spacing:.3px;
}
.dot{ width:10px; height:10px; border-radius:50%; }
.dot.red{ background:#ff7a7a }
.dot.yellow{ background:#ffcf6f }
.dot.green{ background:#70d38a }

.cute-body{ padding: 18px 16px 14px 16px; color: var(--text); }

h1.title{
  font-size: 24px; line-height: 1.25; margin: 0 0 8px 0;
  text-align:center; color:#7a5d00;
}

.subtitle{
  text-align:center; font-size:14px; opacity:.85; margin-bottom:14px;
}

.buttons{ display:flex; gap:10px; }
.btn{
  flex:1;
  background: var(--accent);
  color: #5a2a37;
  border: 0; border-radius: var(--radius);
  padding: 14px 16px;
  font-weight: 700;
  box-shadow: var(--shadow);
  transition: transform .05s ease;
  text-align:center;
}
.btn:active{ transform: translateY(1px); }
.btn.secondary{ background: var(--accent-2); color:#6a4b2a; }

.progress-wrap{ margin: 14px 2px 6px 2px; }
.progress-label{ font-size: 13px; opacity:.85; margin-bottom:8px; }
.bar{
  height: 12px; width: 100%;
  background: rgba(255,255,255,.6);
  border-radius: 999px; overflow: hidden; border:2px solid #ffd89b;
}
.fill{
  height:100%;
  background: linear-gradient(90deg, #ffa1bc, #ffcf6f);
  width: 0%;
  transition: width .25s ease;
}

.cups{
  display:grid; grid-template-columns: repeat(5, 1fr);
  gap: 10px; margin-top: 14px;
}
.cup{
  background: white; border:2px solid #ffe2a9; border-radius:12px;
  display:flex; align-items:center; justify-content:center;
  font-size:34px; padding:10px;
  box-shadow: 0 3px 8px rgba(255, 182, 193, .25);
}

.small{
  font-size: 12px; text-align:center; opacity:.8; margin-top: 6px;
}

/* mobile tuning */
@media (max-width: 420px){
  h1.title{ font-size: 20px; }
  .btn{ padding: 12px; }
  .cups{ grid-template-columns: repeat(4, 1fr); }
}
</style>
<div class="container">
  <div class="cute-window">
    <div class="cute-titlebar">
      <div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div>
      <div>Hidrata <3</div>
    </div>
    <div class="cute-body" id="cute-body">
      <!-- conteúdo vem do Streamlit abaixo -->
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------------- Estado ----------------
today = str(date.today())
if "goal_ml" not in st.session_state: st.session_state.goal_ml = 2000
if "cup_ml"  not in st.session_state: st.session_state.cup_ml  = 200
if "counts"  not in st.session_state: st.session_state.counts  = {}
if today not in st.session_state.counts: st.session_state.counts[today] = 0

count   = st.session_state.counts[today]
goal_ml = st.session_state.goal_ml
cup_ml  = st.session_state.cup_ml
total   = count * cup_ml
pct     = min(int(total / goal_ml * 100), 100)

# ---------------- Conteúdo (HTML + components) ----------------
# título
st.markdown(
    "<h1 class='title'>💧 Já bebeu água hoje, minha princesinha?</h1>"
    "<div class='subtitle'>Clica no botão pra ganhar um copinho fofo 🥤✨</div>",
    unsafe_allow_html=True
)

# botões grandes
col1, col2 = st.columns(2, gap="small")
with col1:
    if st.button(f"➕ {cup_ml} ml", use_container_width=True):
        st.session_state.counts[today] += 1
        if (st.session_state.counts[today] * cup_ml) >= goal_ml:
            st.balloons()
        st.rerun()
with col2:
    if st.button("↩️ Desfazer", use_container_width=True):
        if st.session_state.counts[today] > 0:
            st.session_state.counts[today] -= 1
            st.rerun()

# barra de progresso cute (nossa, pra combinarmos com o card)
st.markdown(f"""
<div class="progress-wrap">
  <div class="progress-label">{total} / {goal_ml} ml ({pct}%)</div>
  <div class="bar"><div class="fill" style="width:{pct}%"></div></div>
</div>
""", unsafe_allow_html=True)

# grade de copinhos (emoji; depois podemos trocar por imagem pixel art)
st.markdown("<div class='cups'>", unsafe_allow_html=True)
if count == 0:
    st.markdown("<div class='small'>Começa com um golinho? 🥺👉👈</div>", unsafe_allow_html=True)
else:
    for i in range(count):
        st.markdown("<div class='cup'>🥤</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Sidebar (config) ----------------
with st.sidebar:
    st.header("⚙️ Configurações")
    st.session_state.goal_ml = st.number_input("Meta diária (ml)", 200, 10000, st.session_state.goal_ml, 100)
    st.session_state.cup_ml  = st.number_input("Tamanho do copo (ml)", 50, 1000, st.session_state.cup_ml, 50)
    st.caption("Dica: meta 2000 ml e copo 200 ml = 10 copinhos 💕")
