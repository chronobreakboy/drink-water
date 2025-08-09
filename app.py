import streamlit as st
from datetime import date
from pathlib import Path
from PIL import Image
import random, time

st.set_page_config(page_title="Beba Água 🌸", page_icon="💧", layout="centered")

# ================== TEMA ROSINHA + ESTRELAS + EFEITOS ==================
STAR_COUNT = 28
random.seed(42)
stars_html = "\n".join(
    f"<div class='star' style='left:{random.randint(0,100)}%; top:{random.randint(0,100)}%; "
    f"animation-delay:{random.uniform(0,4):.2f}s; animation-duration:{random.uniform(5,10):.2f}s'></div>"
    for _ in range(STAR_COUNT)
)

st.markdown(f"""
<style>
:root{{
  --bg-1:#e9c6f5; --bg-2:#ffc9da; --bg-3:#ffe3b8;
  --card:#fff7de; --stroke:#f2d278;
  --text:#5b402f; --muted:#6f5b51;
  --accent:#ffb1c4; --accent2:#ffd59f;
  --shadow:0 10px 28px rgba(255,140,180,.25);
  --radius:18px;
}}
html, body, [data-testid="stAppViewContainer"]{{
  background:
    radial-gradient(1200px 600px at 50% -50%, #fff5f8 0%, #ffe9f0 40%, transparent 60%),
    linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 45%, var(--bg-3) 100%);
  color:var(--text);
}}
/* estrelas animadas no fundo */
.sky{{position:fixed; inset:0; pointer-events:none; z-index:0;
     animation: skyShift 32s linear infinite;}}
@keyframes skyShift{{0%{{transform:translateY(0)}}50%{{transform:translateY(8px)}}100%{{transform:translateY(0)}}}}
.star{{position:fixed; width:6px; height:6px; border-radius:50%;
      background: radial-gradient(circle,#fff,#fff0); box-shadow:0 0 10px #fff8; opacity:.8; pointer-events:none; z-index:1;
      animation: twinkle linear infinite;}}
@keyframes twinkle{{0%,100%{{transform:translateY(0) scale(1); opacity:.6}}50%{{transform:translateY(-12px) scale(1.2); opacity:1}}}}

.main,[data-testid="stAppViewContainer"]>.main{{padding-top:8px; position:relative; z-index:2;}}
.container{{max-width:480px; margin:0 auto;}}
.card{{background:var(--card); border:3px solid var(--stroke); border-radius:14px; box-shadow:var(--shadow); overflow:hidden; position:relative; padding:16px;}}
.title{{text-align:center; font-size:26px; color:#6e4d00; text-shadow:0 1px 0 #fff3; margin:0 0 6px}}
.subtitle{{text-align:center; font-size:14px; color:var(--muted); margin-bottom:12px}}
.stButton>button{{width:100%; padding:14px 16px; font-weight:800; border-radius:var(--radius); border:0; box-shadow:var(--shadow)}}
.stButton>button:not([kind]){{background:var(--accent); color:#5a2a37}}
button[kind="secondary"]{{background:var(--accent2); color:#583d26 !important}}

.progress-wrap{{margin: 12px 2px 8px 2px}}
.progress-label{{font-size:13px; color:var(--muted); margin-bottom:8px}}
.bar{{height:12px; width:100%; background:#fff9; border-radius:999px; overflow:hidden; border:2px solid #ffd89b}}
.fill{{height:100%; background:linear-gradient(90deg,#ffa1bc,#ffcf6f); width:0%; transition:width .25s ease}}

.cups{{display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:12px}}
.cup{{background:white; border:2px solid #ffe2a9; border-radius:12px; display:flex; align-items:center; justify-content:center;
     font-size:34px; padding:10px; min-height:60px; box-shadow:0 3px 8px rgba(255,182,193,.25); animation:pop .15s ease}}
@keyframes pop{{from{{transform:scale(.95); opacity:.6}} to{{transform:scale(1); opacity:1}}}}

.small{{font-size:12px; text-align:center; color:var(--muted); margin-top:6px}}
.msg{{text-align:center; font-weight:700; color:#6e4d00; margin-top:6px}}

/* flash cintilante no clique */
.flash{{position:fixed; inset:0; pointer-events:none; z-index:3;
       background: radial-gradient(circle at 50% 50%, #fff5 0%, transparent 60%);
       animation: flashPop .7s ease;}}
@keyframes flashPop{{0%{{opacity:0}}15%{{opacity:1}}100%{{opacity:0}}}}

@media (max-width:420px){{ .title{{font-size:22px}} .cups{{grid-template-columns:repeat(4,1fr)}} }}
</style>
<div class="sky">{stars_html}</div>
""", unsafe_allow_html=True)

# ================== CARREGAR IMAGENS DA PASTA pixel/ ==================
@st.cache_resource
def carregar_stickers(pasta: str = "pixel"):
    base = Path(pasta)
    if not base.exists():
        return []
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    arquivos = sorted([p for p in base.iterdir() if p.suffix.lower() in exts])
    imgs = []
    for p in arquivos:
        try:
            img = Image.open(p).convert("RGBA")
            # redimensiona suave pra acelerar no mobile (comente se quiser original)
            img.thumbnail((512, 512))
            imgs.append(img)
        except Exception:
            pass
    return imgs

stickers = carregar_stickers("pixel")  # coloque seus PNGs em /pixel

# ================== ESTADO PADRÃO (meta 3500, copo 350) ==================
today = str(date.today())
if "goal_ml" not in st.session_state: st.session_state.goal_ml = 3500
if "cup_ml"  not in st.session_state: st.session_state.cup_ml  = 350
if "counts"  not in st.session_state: st.session_state.counts  = {}
if "day_key" not in st.session_state: st.session_state.day_key = today
if "flash"   not in st.session_state: st.session_state.flash   = False

# lista de índices exibidos HOJE (o que já está na tela não muda)
if "shown_indices" not in st.session_state:
    st.session_state.shown_indices = []  # ordem de exibição de hoje

# pool embaralhado de índices para consumir HOJE (garante “diferente a cada clique”)
if "pool_indices" not in st.session_state:
    st.session_state.pool_indices = list(range(len(stickers)))
    random.shuffle(st.session_state.pool_indices)

# troca de dia? reseta tudo pra hoje começar do zero
if st.session_state.day_key != today:
    st.session_state.day_key = today
    st.session_state.counts[today] = 0
    st.session_state.shown_indices = []
    st.session_state.pool_indices = list(range(len(stickers)))
    random.shuffle(st.session_state.pool_indices)

# count do dia atual é o tamanho do que já mostramos
st.session_state.counts.setdefault(today, 0)
st.session_state.counts[today] = len(st.session_state.shown_indices)

goal_ml = st.session_state.goal_ml
cup_ml  = st.session_state.cup_ml
count   = st.session_state.counts[today]
total   = count * cup_ml
pct     = min(int(total / goal_ml * 100), 100)

# ================== FUNÇÕES ==================
def incentivo(p):
    if p == 0:   return "Começa com um golinho? 🥺👉👈"
    if p < 20:   return "Primeiro passo dado! 💖"
    if p < 40:   return "Good girl! Segue no foco ✨"
    if p < 60:   return "Metade do copão chegando! Orgulho 🥹"
    if p < 80:   return "Quase lá! Só mais uns golinhos 😘"
    if p < 100:  return "Reta final, você consegue! 🏁💪"
    return "META BATIDA! Princesinha hidratadaaa! 🥳💦"

def proximo_indice_para_hoje():
    """Puxa o próximo índice do pool embaralhado; se acabar, reembaralha para permitir mais cliques sem repetir até esgotar novamente."""
    if not stickers:
        return None
    if not st.session_state.pool_indices:
        # todas já usadas hoje; reembaralha pra permitir continuar (agora pode repetir)
        st.session_state.pool_indices = list(range(len(stickers)))
        random.shuffle(st.session_state.pool_indices)
    return st.session_state.pool_indices.pop(0)

# ================== CABEÇALHO / CARD ==================
st.markdown("<div class='container'><div class='card'>", unsafe_allow_html=True)
st.markdown("<h1 class='title'>💧 Já bebeu água hoje, minha princesinha?</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Clica no botão pra ganhar um copinho fofo 🥤✨</div>", unsafe_allow_html=True)

# ================== BOTÕES ==================
col1, col2 = st.columns(2, gap="small")
with col1:
    if st.button("➕ um copinho", use_container_width=True):
        idx = proximo_indice_para_hoje()
        if idx is not None:
            st.session_state.shown_indices.append(idx)  # adiciona novo “copo” com imagem diferente
            st.session_state.flash = True               # flash cintilante
        # balões se bateu a meta
        if (len(st.session_state.shown_indices) * cup_ml) >= goal_ml:
            st.balloons()
        st.rerun()

with col2:
    if st.button("↩️ Desfazer", use_container_width=True):
        if st.session_state.shown_indices:
            st.session_state.shown_indices.pop()  # remove o último “copo”
            st.session_state.flash = True
            st.rerun()

# ================== PROGRESSO + MENSAGEM ==================
total = len(st.session_state.shown_indices) * cup_ml
pct   = min(int(total / goal_ml * 100), 100)
st.markdown(f"""
<div class="progress-wrap">
  <div class="progress-label">{total} / {goal_ml} ml ({pct}%) — cada copinho: {cup_ml} ml</div>
  <div class="bar"><div class="fill" style="width:{pct}%"></div></div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"<div class='msg'>{incentivo(pct)}</div>", unsafe_allow_html=True)

# ================== RENDER COPINHOS DE HOJE (permanecem) ==================
st.markdown("<div class='cups'>", unsafe_allow_html=True)
if not st.session_state.shown_indices:
    st.markdown("<div class='small'>Sem copinhos ainda… bora começar com um? 💕</div>", unsafe_allow_html=True)
else:
    cols = st.columns(4)
    for i, idx in enumerate(st.session_state.shown_indices):
        with cols[i % 4]:
            if stickers:
                st.image(stickers[idx], use_container_width=True)
            else:
                # fallback se não houver imagens em /pixel
                st.markdown("<div class='cup'>🥤</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)  # fecha card/container

# ================== FLASH NO CLIQUE ==================
if st.session_state.flash:
    st.session_state.flash = False
    st.markdown("<div class='flash'></div>", unsafe_allow_html=True)

# ================== SIDEBAR (config) ==================
with st.sidebar:
    st.header("⚙️ Configurações")
    st.session_state.goal_ml = st.number_input("Meta diária (ml)", 200, 10000, st.session_state.goal_ml, 100)
    st.session_state.cup_ml  = st.number_input("Tamanho do copo (ml)", 50, 1000, st.session_state.cup_ml, 50)
    st.caption("As imagens ficam fixas durante o dia. No dia seguinte, começa outra ordem aleatória 💕")
    if st.button("🔄 Resetar dia (manual)"):
        st.session_state.day_key = ""  # força reset no próximo rerun
        st.rerun()
