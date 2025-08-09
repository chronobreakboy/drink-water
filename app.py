import streamlit as st
from datetime import date
import random
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Hidrata, princesinha 💖", layout="centered")

# ====================== CSS: Pôr-do-sol + contraste ======================
st.markdown("""
<style>
:root{
  --bg-1: #e9c6f5;  /* lilás pastel */
  --bg-2: #ffc9da;  /* rosinha */
  --bg-3: #ffe3b8;  /* pêssego */
  --card: #fff7de;  /* amarelinho suave */
  --stroke: #f2d278;
  --text: #5b402f;  /* marrom quente (boa leitura) */
  --muted: #6f5b51;
  --accent: #ffb1c4;   /* rosa */
  --accent2:#ffd59f;   /* pêssego */
  --shadow: 0 10px 28px rgba(255, 140, 180, .25);
  --radius: 18px;
}

html, body, [data-testid="stAppViewContainer"]{
  background: radial-gradient(1200px 600px at 50% -50%, #fff5f8 0%, #ffe9f0 40%, transparent 60%) ,
              linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 45%, var(--bg-3) 100%);
  color: var(--text);
}
.main, [data-testid="stAppViewContainer"] > .main{ padding-top: 8px; }
.container{ max-width: 480px; margin: 0 auto; }

.cute-window{
  background: var(--card);
  border: 3px solid var(--stroke);
  border-radius: 14px;
  box-shadow: var(--shadow);
  overflow: hidden;
}

.cute-titlebar{
  background: #ffe7ad;
  padding: 10px 14px;
  display:flex; align-items:center; gap:8px;
  font-weight:700; color:#7a5d00; letter-spacing:.3px;
}
.dot{ width:10px; height:10px; border-radius:50%; }
.dot.red{ background:#ff7a7a } .dot.yellow{ background:#ffcf6f } .dot.green{ background:#70d38a }

.cute-body{ padding: 18px 16px 14px 16px; color: var(--text); }

h1.title{
  font-size: 26px; line-height:1.25; margin: 0 0 8px 0;
  text-align:center; color:#6e4d00; text-shadow: 0 1px 0 #fff3;
}
.subtitle{ text-align:center; font-size:14px; color: var(--muted); margin-bottom:14px; }

.stButton>button{
  width:100%; padding: 14px 16px; font-weight:800; border-radius: var(--radius);
  border:0; box-shadow: var(--shadow);
}
button[kind="secondary"]{ background: var(--accent2); color:#583d26 !important; }
.stButton>button:not([kind]){ background: var(--accent); color:#5a2a37; }

.progress-wrap{ margin: 14px 2px 10px 2px; }
.progress-label{ font-size: 13px; color: var(--muted); margin-bottom:8px; }
.bar{
  height: 12px; width: 100%; background: #fff9;
  border-radius: 999px; overflow: hidden; border:2px solid #ffd89b;
}
.fill{ height:100%; background: linear-gradient(90deg, #ffa1bc, #ffcf6f); width:0%; transition: width .25s ease; }

.cups{ display:grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 12px; }
.cup{
  background: white; border:2px solid #ffe2a9; border-radius:12px;
  display:flex; align-items:center; justify-content:center;
  font-size:34px; padding:10px; min-height:60px;
  box-shadow: 0 3px 8px rgba(255, 182, 193, .25);
  animation: pop .15s ease;
}
@keyframes pop{ from{ transform:scale(.95); opacity:.6 } to{ transform:scale(1); opacity:1 } }

.small{ font-size: 12px; text-align:center; color: var(--muted); margin-top: 6px; }

/* mobile */
@media (max-width: 420px){
  h1.title{ font-size: 22px; }
  .cups{ grid-template-columns: repeat(4, 1fr); }
}
</style>

<div class="container">
  <div class="cute-window">
    <div class="cute-titlebar">
      <div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div>
      <div>Hidrata &lt;3</div>
    </div>
    <div class="cute-body"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ====================== Estado ======================
today = str(date.today())
if "goal_ml" not in st.session_state: st.session_state.goal_ml = 2000
if "cup_ml"  not in st.session_state: st.session_state.cup_ml  = 200
if "counts"  not in st.session_state: st.session_state.counts  = {}
if today not in st.session_state.counts: st.session_state.counts[today] = 0
if "pack" not in st.session_state: st.session_state.pack = "Emojis fofos"
if "images" not in st.session_state: st.session_state.images = []  # PIL Images

count   = st.session_state.counts[today]
goal_ml = st.session_state.goal_ml
cup_ml  = st.session_state.cup_ml
total   = count * cup_ml
pct     = min(int(total / goal_ml * 100), 100)

# ====================== UI ======================
st.markdown(
    "<h1 class='title'>💧 Já bebeu água hoje, minha princesinha?</h1>"
    "<div class='subtitle'>Clica no botão pra ganhar um copinho fofo 🥤✨</div>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2, gap="small")
with col1:
    if st.button(f"➕ {cup_ml} ml", use_container_width=True):
        st.session_state.counts[today] += 1
        if (st.session_state.counts[today] * cup_ml) >= goal_ml:
            st.balloons()
        st.rerun()
with col2:
    if st.button("↩️ Desfazer", use_container_width=True, key="undo"):
        if st.session_state.counts[today] > 0:
            st.session_state.counts[today] -= 1
            st.rerun()

# Barra de progresso combinando com o card
st.markdown(f"""
<div class="progress-wrap">
  <div class="progress-label">{total} / {goal_ml} ml ({pct}%)</div>
  <div class="bar"><div class="fill" style="width:{pct}%"></div></div>
</div>
""", unsafe_allow_html=True)

# ====================== Sidebar: pacotes de copinhos ======================
with st.sidebar:
    st.header("⚙️ Configurações")
    st.session_state.goal_ml = st.number_input("Meta diária (ml)", 200, 10000, st.session_state.goal_ml, 100)
    st.session_state.cup_ml  = st.number_input("Tamanho do copo (ml)", 50, 1000, st.session_state.cup_ml, 50)

    st.markdown("---")
    st.subheader("Copinhos")
    st.session_state.pack = st.radio("Pacote", ["Emojis fofos", "Minhas imagens"], horizontal=False)

    if st.session_state.pack == "Minhas imagens":
        up = st.file_uploader("Envie 1+ imagens (PNG/JPG)", type=["png","jpg","jpeg"], accept_multiple_files=True)
        if up:
            st.session_state.images = []
            for f in up:
                img = Image.open(BytesIO(f.read())).convert("RGBA")
                st.session_state.images.append(img)
            st.success(f"{len(st.session_state.images)} imagem(ns) carregadas!")
        st.caption("⚠️ Use imagens que você possa usar. Personagens licenciados (Disney etc.) só para uso pessoal.")

# ====================== Render dos copinhos ======================
emoji_pack = ["🥤","🧃","🫖","🍹","🧋","🍑","💖","🌸","⭐","🫧"]

st.markdown("<div class='cups'>", unsafe_allow_html=True)
if count == 0:
    st.markdown("<div class='small'>Começa com um golinho? 🥺👉👈</div>", unsafe_allow_html=True)
else:
    for i in range(count):
        if st.session_state.pack == "Minhas imagens" and st.session_state.images:
            # mostra imagem enviada (escolhe aleatória para variar)
            img = random.choice(st.session_state.images)
            st.image(img, use_container_width=True)
        else:
            # mostra emoji aleatório do pacote
            st.markdown(f"<div class='cup'>{random.choice(emoji_pack)}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
