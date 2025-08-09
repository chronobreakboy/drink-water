import streamlit as st
from datetime import date
from pathlib import Path
from PIL import Image
import json, random

st.set_page_config(page_title="Beba Água 🌸", page_icon="💧", layout="centered")

# ================== TEMA / FUNDO CINTILANTE ==================
STAR_COUNT = 28
random.seed(42)  # só pro fundo
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

.flash{{position:fixed; inset:0; pointer-events:none; z-index:3;
       background: radial-gradient(circle at 50% 50%, #fff5 0%, transparent 60%);
       animation: flashPop .7s ease;}}
@keyframes flashPop{{0%{{opacity:0}}15%{{opacity:1}}100%{{opacity:0}}}}

@media (max-width:420px){{ .title{{font-size:22px}} .cups{{grid-template-columns:repeat(4,1fr)}} }}
</style>
<div class="sky">{stars_html}</div>
""", unsafe_allow_html=True)

# ================== CARREGAR PNGs DE /pixel ==================
@st.cache_resource
def load_images(folder="pixel"):
    base = Path(folder)
    if not base.exists():
        return []
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    files = sorted([p for p in base.iterdir() if p.suffix.lower() in exts])
    imgs = []
    for p in files:
        try:
            im = Image.open(p).convert("RGBA")
            im.thumbnail((512, 512))  # acelera no mobile; remova se quiser original
            imgs.append({"path": str(p), "img": im})
        except Exception:
            pass
    return imgs

images = load_images("pixel")  # coloque seus PNGs em /pixel

# ================== PERSISTÊNCIA EM ARQUIVO (por dia) ==================
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
today = date.today().isoformat()
state_path = DATA_DIR / f"state_{today}.json"

def save_state(shown_indices, pool_indices, goal_ml, cup_ml):
    payload = {
        "shown_indices": shown_indices,
        "pool_indices": pool_indices,
        "goal_ml": goal_ml,
        "cup_ml": cup_ml,
    }
    state_path.write_text(json.dumps(payload), encoding="utf-8")

def load_state():
    if state_path.exists():
        try:
            d = json.loads(state_path.read_text(encoding="utf-8"))
            return (
                d.get("shown_indices", []),
                d.get("pool_indices", []),
                d.get("goal_ml", 3500),
                d.get("cup_ml", 350),
            )
        except Exception:
            pass
    # inicial: embaralha uma ordem para hoje
    pool = list(range(len(images)))
    random.shuffle(pool)
    return [], pool, 3500, 350

# carrega ou cria estado de hoje (fora do session_state pra sobreviver a refresh)
shown_indices_file, pool_indices_file, goal_default, cup_default = load_state()

# ================== ESTADO EM SESSÃO (UI) ==================
# meta e copo com defaults vindos do arquivo
if "goal_ml" not in st.session_state: st.session_state.goal_ml = goal_default
if "cup_ml"  not in st.session_state: st.session_state.cup_ml  = cup_default
if "shown_indices" not in st.session_state: st.session_state.shown_indices = shown_indices_file
if "pool_indices"  not in st.session_state: st.session_state.pool_indices  = pool_indices_file
if "flash"         not in st.session_state: st.session_state.flash = False

# garante consistência caso número de imagens mude
max_idx = len(images) - 1
st.session_state.shown_indices = [i for i in st.session_state.shown_indices if 0 <= i <= max_idx]
st.session_state.pool_indices  = [i for i in st.session_state.pool_indices  if 0 <= i <= max_idx]
if not st.session_state.pool_indices and images:
    # reembaralha as que ainda não foram mostradas hoje (se todas já foram, permite repetir)
    remaining = [i for i in range(len(images)) if i not in st.session_state.shown_indices]
    if not remaining:
        remaining = list(range(len(images)))
    random.shuffle(remaining)
    st.session_state.pool_indices = remaining

# ================== CABEÇALHO ==================
st.markdown("<div class='container'><div class='card'>", unsafe_allow_html=True)
st.markdown("<h1 class='title'>💧 Já bebeu água hoje, minha princesinha?</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Clica no botão pra ganhar um copinho fofo 🥤✨</div>", unsafe_allow_html=True)

# ================== BOTÕES ==================
col1, col2 = st.columns(2, gap="small")
with col1:
    if st.button("➕ um copinho", use_container_width=True):
        if images:
            # pega próximo índice do pool (sem repetir até esgotar)
            idx = st.session_state.pool_indices.pop(0)
            st.session_state.shown_indices.append(idx)
            st.session_state.flash = True
            # salva no arquivo pra persistir no refresh
            save_state(
                st.session_state.shown_indices,
                st.session_state.pool_indices,
                st.session_state.goal_ml,
                st.session_state.cup_ml,
            )
            # balões se bateu meta
            if len(st.session_state.shown_indices) * st.session_state.cup_ml >= st.session_state.goal_ml:
                st.balloons()
        st.rerun()
with col2:
    if st.button("↩️ Desfazer", use_container_width=True):
        if st.session_state.shown_indices:
            st.session_state.shown_indices.pop()
            # devolve um índice ao início do pool (pra não perder a ordem)
            if images:
                # se já mostramos algo, o "desfeito" volta pra frente do pool
                last = st.session_state.shown_indices[-1] if st.session_state.shown_indices else None
                # simples: apenas reponho um qualquer válido
                used = set(st.session_state.shown_indices)
                candidates = [i for i in range(len(images)) if i not in used]
                if candidates:
                    st.session_state.pool_indices = candidates + st.session_state.pool_indices
            save_state(
                st.session_state.shown_indices,
                st.session_state.pool_indices,
                st.session_state.goal_ml,
                st.session_state.cup_ml,
            )
            st.session_state.flash = True
            st.rerun()

# ================== PROGRESSO ==================
goal_ml = st.session_state.goal_ml
cup_ml  = st.session_state.cup_ml
total   = len(st.session_state.shown_indices) * cup_ml
pct     = min(int(total / goal_ml * 100), 100)
st.markdown(f"""
<div class="progress-wrap">
  <div class="progress-label">{total} / {goal_ml} ml ({pct}%) — cada copinho: {cup_ml} ml</div>
  <div class="bar"><div class="fill" style="width:{pct}%"></div></div>
</div>
""", unsafe_allow_html=True)

# ================== MENSAGEM MOTIVACIONAL ==================
def incentivo(p):
    if p == 0:   return "Começa com um golinho? 🥺👉👈"
    if p < 20:   return "Primeiro passo dado! 💖"
    if p < 40:   return "Good girl! Segue no foco ✨"
    if p < 60:   return "Metade do copão chegando! Orgulho 🥹"
    if p < 80:   return "Quase lá! Só mais uns golinhos 😘"
    if p < 100:  return "Reta final, você consegue! 🏁💪"
    return "META BATIDA! Princesinha hidratadaaa! 🥳💦"
st.markdown(f"<div class='msg'>{incentivo(pct)}</div>", unsafe_allow_html=True)

# ================== GRID DE COPINHOS (IMAGENS QUE FICAM) ==================
st.markdown("<div class='cups'>", unsafe_allow_html=True)
if not st.session_state.shown_indices:
    st.markdown("<div class='small'>Sem copinhos ainda… bora começar com um? 💕</div>", unsafe_allow_html=True)
else:
    cols = st.columns(4)
    for i, idx in enumerate(st.session_state.shown_indices):
        with cols[i % 4]:
            if images:
                st.image(images[idx]["img"], use_container_width=True)
            else:
                st.markdown("<div class='cup'>🥤</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div></div>", unsafe_allow_html=True)

# ================== FLASH CINTILANTE ==================
if st.session_state.flash:
    st.session_state.flash = False
    st.markdown("<div class='flash'></div>", unsafe_allow_html=True)

# ================== SIDEBAR (só configs úteis) ==================
with st.sidebar:
    st.header("⚙️ Configurações")
    new_goal = st.number_input("Meta diária (ml)", 200, 10000, goal_ml, 100)
    new_cup  = st.number_input("Tamanho do copo (ml)", 50, 1000, cup_ml, 50)
    if new_goal != goal_ml or new_cup != cup_ml:
        st.session_state.goal_ml = new_goal
        st.session_state.cup_ml  = new_cup
        save_state(
            st.session_state.shown_indices,
            st.session_state.pool_indices,
            st.session_state.goal_ml,
            st.session_state.cup_ml,
        )
    st.caption("As imagens de hoje ficam fixas. Amanhã sorteia outra ordem automaticamente. 💕")
    if st.button("🔄 Resetar dia (manual)"):
        # esvazia estado de hoje e salva
        st.session_state.shown_indices = []
        st.session_state.pool_indices  = list(range(len(images)))
        random.shuffle(st.session_state.pool_indices)
        save_state(st.session_state.shown_indices, st.session_state.pool_indices, st.session_state.goal_ml, st.session_state.cup_ml)
        st.rerun()
