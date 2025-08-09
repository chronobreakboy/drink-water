import streamlit as st
from datetime import date
import random, time
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Hidrata, princesinha 💖", layout="centered")

# ====================== Estado ======================
today = str(date.today())
if "goal_ml" not in st.session_state: st.session_state.goal_ml = 2000
if "cup_ml"  not in st.session_state: st.session_state.cup_ml  = 200
if "counts"  not in st.session_state: st.session_state.counts  = {}
if today not in st.session_state.counts: st.session_state.counts[today] = 0
if "pack" not in st.session_state: st.session_state.pack = "Emojis fofos"
if "images" not in st.session_state: st.session_state.images = []
if "flash_ts" not in st.session_state: st.session_state.flash_ts = 0.0  # pra reiniciar animação no clique

count   = st.session_state.counts[today]
goal_ml = st.session_state.goal_ml
cup_ml  = st.session_state.cup_ml
total   = count * cup_ml
pct     = min(int(total / goal_ml * 100), 100)

# ====================== CSS: pôr-do-sol + estrelas animadas + efeitos ======================
STAR_COUNT = 28  # quantidade de estrelinhas flutuantes
random.seed(42)
stars_html = "\n".join(
    f"<div class='star' style='left:{random.randint(0,100)}%;"
    f" top:{random.randint(0,100)}%; animation-delay:{random.uniform(0,4):.2f}s;"
    f" animation-duration:{random.uniform(5,10):.2f}s'></div>"
    for _ in range(STAR_COUNT)
)

st.markdown(f"""
<style>
:root{{
  --bg-1: #e9c6f5; --bg-2: #ffc9da; --bg-3: #ffe3b8;
  --card: #fff7de; --stroke: #f2d278;
  --text: #5b402f; --muted:#6f5b51;
  --accent:#ffb1c4; --accent2:#ffd59f;
  --shadow: 0 10px 28px rgba(255, 140, 180, .25);
  --radius:18px;
}}

html, body, [data-testid="stAppViewContainer"]{{
  background:
    radial-gradient(1200px 600px at 50% -50%, #fff5f8 0%, #ffe9f0 40%, transparent 60%),
    linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 45%, var(--bg-3) 100%);
  color: var(--text);
}}
/* céu com estrelinhas */
.sky {{
  position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background: radial-gradient(2px 2px at 20% 30%, #fff8 40%, transparent 41%),
              radial-gradient(2px 2px at 80% 20%, #fff8 40%, transparent 41%),
              radial-gradient(2px 2px at 60% 70%, #fff8 40%, transparent 41%),
              transparent;
  animation: skyShift 32s linear infinite;
}}
@keyframes skyShift {{
  0% {{ transform: translateY(0px) }}
  50% {{ transform: translateY(8px) }}
  100%{{ transform: translateY(0px) }}
}}
.star {{
  position: fixed; width:6px; height:6px; border-radius:50%;
  background: radial-gradient(circle,#fff,#fff0);
  box-shadow: 0 0 10px #fff8;
  opacity:.8; pointer-events:none; z-index:1;
  animation: twinkle linear infinite;
}}
@keyframes twinkle {{
  0%,100% {{ transform: translateY(0px) scale(1); opacity:.6 }}
  50%     {{ transform: translateY(-12px) scale(1.2); opacity:1 }}
}}

.main, [data-testid="stAppViewContainer"] > .main{{ padding-top: 8px; position: relative; z-index: 2; }}
.container{{ max-width: 480px; margin: 0 auto; }}

.cute-window{{
  background: var(--card); border:3px solid var(--stroke);
  border-radius:14px; box-shadow: var(--shadow); overflow:hidden; position:relative;
}}
/* flash fofo no clique */
.flash {{
  position:absolute; inset:-2px; border-radius:14px; pointer-events:none;
  background: radial-gradient(circle at 50% 50%, #fff6 0%, transparent 60%);
  animation: flashPop .7s ease forwards;
}}
@keyframes flashPop {{ 0%{{opacity:.0}} 15%{{opacity:1}} 100%{{opacity:0}} }}

.cute-titlebar{{
  background:#ffe7ad; padding:10px 14px;
  display:flex; align-items:center; gap:8px; font-weight:700; color:#7a5d00;
}}
.dot{{ width:10px;height:10px;border-radius:50% }}
.dot.red{{background:#ff7a7a}} .dot.yellow{{background:#ffcf6f}} .dot.green{{background:#70d38a}}

.cute-body{{ padding:18px 16px 14px 16px; color:var(--text); }}

h1.title{{ font-size:26px; text-align:center; color:#6e4d00; text-shadow:0 1px 0 #fff3; margin:0 0 8px }}
.subtitle{{ text-align:center; font-size:14px; color:var(--muted); margin-bottom:14px }}

.stButton>button{{ width:100%; padding:14px 16px; font-weight:800; border-radius:var(--radius); border:0; box-shadow:var(--shadow) }}
.stButton>button:not([kind]){{ background:var(--accent); color:#5a2a37; }}
button[kind="secondary"]{{ background:var(--accent2); color:#583d26 !important; }}

.progress-wrap{{ margin: 14px 2px 10px 2px }}
.progress-label{{ font-size: 13px; color: var(--muted); margin-bottom:8px }}
.bar{{ height:12px; width:100%; background:#fff9; border-radius:999px; overflow:hidden; border:2px solid #ffd89b }}
.fill{{ height:100%; background:linear-gradient(90deg,#ffa1bc,#ffcf6f); width:0%; transition:width .25s ease }}

.cups{{ display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; margin-top:12px }}
.cup{{ background:white; border:2px solid #ffe2a9; border-radius:12px;
       display:flex; align-items:center; justify-content:center;
       font-size:34px; padding:10px; min-height:60px;
       box-shadow:0 3px 8px rgba(255,182,193,.25); animation: pop .15s ease }}
@keyframes pop{{ from{{ transform:scale(.95); opacity:.6 }} to{{ transform:scale(1); opacity:1 }} }}

.small{{ font-size:12px; text-align:center; color:var(--muted); margin-top:6px }}
.msg{{ text-align:center; font-weight:700; color:#6e4d00; margin-top:6px }}

@media (max-width:420px){{
  h1.title{{ font-size:22px }}
  .cups{{ grid-template-columns: repeat(4, 1fr) }}
}}
</style>

<!-- camada de estrelas -->
<div class="sky">{stars_html}</div>
""", unsafe_allow_html=True)

# ====================== UI ======================
st.markdown("""
<div class="container">
  <div class="cute-window">
    <div class="cute-titlebar">
      <div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div>
      <div>Hidrata &lt;3</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# o flash aparece quando flash_ts muda (reinicia animação)
if st.session_state.flash_ts:
    st.markdown(f"<div class='container'><div class='cute-window'><div class='flash' style='animation-name:flashPop;'></div></div></div>", unsafe_allow_html=True)

st.markdown(
    "<h1 class='title'>💧 Já bebeu água hoje, minha princesinha?</h1>"
    "<div class='subtitle'>Clica no botão pra ganhar um copinho fofo 🥤✨</div>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2, gap="small")
with col1:
    if st.button(f"➕ um copinho", use_container_width=True):
        st.session_state.counts[today] += 1
        st.session_state.flash_ts = time.time()  # dispara flash
        if (st.session_state.counts[today] * cup_ml) >= goal_ml:
            st.balloons()
        st.rerun()
with col2:
    if st.button("↩️ Desfazer", use_container_width=True, key="undo"):
        if st.session_state.counts[today] > 0:
            st.session_state.counts[today] -= 1
            st.session_state.flash_ts = time.time()
            st.rerun()

# Barra de progresso
total   = st.session_state.counts[today] * cup_ml
pct     = min(int(total / goal_ml * 100), 100)
st.markdown(f"""
<div class="progress-wrap">
  <div class="progress-label">{total} / {goal_ml} ml ({pct}%) — cada copinho: {cup_ml} ml</div>
  <div class="bar"><div class="fill" style="width:{pct}%"></div></div>
</div>
""", unsafe_allow_html=True)

# Mensagens de incentivo dinâmicas
def incentivo(p):
    if p == 0:
        return "Começa com um golinho? 🥺👉👈"
    if p < 20:
        return "Amooo! Já senti a sede indo embora 💖"
    if p < 40:
        return "Good girl! Segue no foco que você tá brilhando ✨"
    if p < 60:
        return "Metade do copão vem aí! Orgulho de você 🥹"
    if p < 80:
        return "Quase láaa! Só mais uns golinhos 😘"
    if p < 100:
        return "Últimos goles pra vitória! 🏁💪"
    return "META BATIDA! Princesinha hidratadaaa! 🥳💦"

st.markdown(f"<div class='msg'>{incentivo(pct)}</div>", unsafe_allow_html=True)

# Packs de copinhos
emoji_pack = ["🥤","🧃","🫖","🍹","🧋","🍑","💖","🌸","⭐","🫧"]

# Grade de copinhos
st.markdown("<div class='cups'>", unsafe_allow_html=True)
if st.session_state.counts[today] == 0:
    st.markdown("<div class='small'>Sem copinhos ainda… bora começar com um? 💕</div>", unsafe_allow_html=True)
else:
    for _ in range(st.session_state.counts[today]):
        if st.session_state.pack == "Minhas imagens" and st.session_state.images:
            img = random.choice(st.session_state.images)
            st.image(img, use_container_width=True)
        else:
            st.markdown(f"<div class='cup'>{random.choice(emoji_pack)}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    st.session_state.goal_ml = st.number_input("Meta diária (ml)", 200, 10000, st.session_state.goal_ml, 100)
    st.session_state.cup_ml  = st.number_input("Tamanho do copo (ml)", 50, 1000, st.session_state.cup_ml, 50)

    st.markdown("---")
    st.subheader("Copinhos")
    st.session_state.pack = st.radio("Pacote", ["Emojis fofos", "Minhas imagens"], horizontal=False)
    if st.session_state.pack == "Minhas imagens":
        up = st.file_uploader("Envie imagens (PNG/JPG)", type=["png","jpg","jpeg"], accept_multiple_files=True)
        if up:
            st.session_state.images = []
            for f in up:
                img = Image.open(BytesIO(f.read())).convert("RGBA")
                st.session_state.images.append(img)
            st.success(f"{len(st.session_state.images)} imagem(ns) carregadas!")
        st.caption("Uso pessoal: pode usar stickers que você curte. 💗")
