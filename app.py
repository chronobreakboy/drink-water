import streamlit as st
from datetime import date
from pathlib import Path
from PIL import Image
import json, random, base64

st.set_page_config(page_title="Beba Água 🌸", page_icon="💧", layout="centered")

# ================== TEMA / FUNDO CINTILANTE ==================
STAR_COUNT = 28
random.seed(42)  # só para o fundo
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
  --btn-grad: linear-gradient(180deg,#ffd0e0,#ffb1c4);
  --btn-grad-2: linear-gradient(180deg,#ffe1b8,#ffd59f);
  --shadow:0 14px 36px rgba(255,140,180,.30);
  --radius:20px;
}}
html, body, [data-testid="stAppViewContainer"]{{
  background:
    radial-gradient(1200px 600px at 50% -50%, #fff5f8 0%, #ffe9f0 40%, transparent 60%),
    linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 45%, var(--bg-3) 100%);
  color:var(--text);
}}
.sky{{position:fixed; inset:0; pointer-events:none; z-index:0; animation: skyShift 32s linear infinite;}}
@keyframes skyShift{{0%{{transform:translateY(0)}}50%{{transform:translateY(8px)}}100%{{transform:translateY(0)}}}}
.star{{position:fixed; width:6px; height:6px; border-radius:50%;
      background: radial-gradient(circle,#fff,#fff0); box-shadow:0 0 10px #fff8;
      opacity:.8; pointer-events:none; z-index:1; animation: twinkle linear infinite;}}
@keyframes twinkle{{0%,100%{{transform:translateY(0) scale(1); opacity:.6}}50%{{transform:translateY(-12px) scale(1.2); opacity:1}}}}

.main,[data-testid="stAppViewContainer"]>.main{{padding-top:8px; position:relative; z-index:2;}}
.container{{max-width:520px; margin:0 auto;}}
.card{{background:var(--card); border:3px solid var(--stroke); border-radius:16px; box-shadow:var(--shadow); overflow:hidden; position:relative; padding:16px;}}
.title{{text-align:center; font-size:32px; font-weight:800; color:#6e4d00; text-shadow:0 1px 0 #fff3; margin:6px 0}}
.subtitle{{text-align:center; font-size:14px; color:var(--muted); margin-bottom:14px}}

.stButton>button{{width:100%; padding:16px 18px; font-weight:900; border-radius:var(--radius); border:0; box-shadow:var(--shadow);
                  letter-spacing:.2px; transform: translateY(0); transition: transform .05s ease, filter .15s ease;}}
.btn-primary{{ background: var(--btn-grad); color:#5a2a37; }}
.btn-primary:hover{{ filter: brightness(1.05); transform: translateY(-1px); }}
.btn-sec{{ background: var(--btn-grad-2); color:#583d26 !important; }}
.btn-sec:hover{{ filter: brightness(1.05); transform: translateY(-1px); }}

.progress-wrap{{margin: 12px 2px 8px 2px}}
.progress-label{{font-size:13px; color:var(--muted); margin-bottom:8px}}
.bar{{height:12px; width:100%; background:#fff9; border-radius:999px; overflow:hidden; border:2px solid #ffd89b}}
.fill{{height:100%; background:linear-gradient(90deg,#ffa1bc,#ffcf6f); width:0%; transition:width .25s ease}}

.cups{{display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:12px}}
.cup{{background:white; border:2px solid #ffe2a9; border-radius:12px; display:flex; align-items:center; justify-content:center;
     font-size:34px; padding:10px; min-height:60px; box-shadow:0 3px 8px rgba(255,182,193,.25); animation:pop .15s ease}}
@keyframes pop{{from{{transform:scale(.95); opacity:.6}} to{{transform:scale(1); opacity:1}}}}

.small{{font-size:12px; text-align:center; color:var(--muted); margin-top:6px}}
.msg{{text-align:center; font-weight:800; color:#6e4d00; margin-top:8px}}

.flash{{position:fixed; inset:0; pointer-events:none; z-index:4;
       background: radial-gradient(50% 50% at 50% 50%, #fff6 0%, transparent 60%);
       animation: flashPop .7s ease;}}
@keyframes flashPop{{0%{{opacity:0}}15%{{opacity:1}}100%{{opacity:0}}}}
.burst{{position:fixed; left:50%; top:46%; width:0; height:0; pointer-events:none; z-index:5}}
.burst span{{position:absolute; font-size:22px; animation: fly .8s ease-out forwards; opacity:0}}
@keyframes fly{{
  0%  {{transform:translate(-50%,-50%) scale(.6); opacity:.0}}
  20% {{opacity:1}}
  100%{{transform:translate(var(--x), var(--y)) scale(1.2); opacity:0}}
}}

@media (max-width:420px){{ .title{{font-size:26px}} .cups{{grid-template-columns:repeat(4,1fr)}} }}
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
            im.thumbnail((512, 512))  # acelera no mobile
            imgs.append({"path": str(p), "img": im})
        except Exception:
            pass
    return imgs

images = load_images("pixel")

# ================== CARREGAR yay.mp3 (base64) ==================
@st.cache_resource
def load_yay_b64(path="yay.mp3"):
    p = Path(path)
    if not p.exists():
        return None
    b = p.read_bytes()
    return base64.b64encode(b).decode("ascii")

YAY_B64 = load_yay_b64("yay.mp3")

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
    pool = list(range(len(images)))
    random.shuffle(pool)
    return [], pool, 3500, 350

shown_indices_file, pool_indices_file, goal_default, cup_default = load_state()

# ================== ESTADO EM SESSÃO ==================
if "goal_ml" not in st.session_state: st.session_state.goal_ml = goal_default
if "cup_ml"  not in st.session_state: st.session_state.cup_ml  = cup_default
if "shown_indices" not in st.session_state: st.session_state.shown_indices = shown_indices_file
if "pool_indices"  not in st.session_state: st.session_state.pool_indices  = pool_indices_file
if "do_effect"     not in st.session_state: st.session_state.do_effect = False
if "fx_nonce"      not in st.session_state: st.session_state.fx_nonce  = 0  # muda a cada clique p/ forçar execução do som
if "sound_ok"      not in st.session_state: st.session_state.sound_ok  = False  # iOS: habilitar som

# sanity se número de imagens mudou
max_idx = len(images) - 1
st.session_state.shown_indices = [i for i in st.session_state.shown_indices if 0 <= i <= max_idx]
st.session_state.pool_indices  = [i for i in st.session_state.pool_indices  if 0 <= i <= max_idx]
if not st.session_state.pool_indices and images:
    remaining = [i for i in range(len(images)) if i not in st.session_state.shown_indices]
    if not remaining: remaining = list(range(len(images)))
    random.shuffle(remaining)
    st.session_state.pool_indices = remaining

# ================== CABEÇALHO ==================
st.markdown("<div class='container'><div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='title'>💧 Já bebeu água hoje, minha princesinha?</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Clica no botão para ganhar um sticker fofinho 🧋✨</div>", unsafe_allow_html=True)

# ---- Botão para habilitar som no iPhone (cria window.YAY e destrava) ----
col_enable, _ = st.columns([1,3])
with col_enable:
    if not st.session_state.sound_ok and st.button("🔊 Ativar som no iPhone"):
        st.session_state.sound_ok = True
        src_line = f"const SRC='data:audio/mpeg;base64,{YAY_B64}';" if YAY_B64 else "const SRC=null;"
        st.components.v1.html(f"""
        <script>
        (function(){{
          {src_line}
          if (!window.YAY) {{
            const a = document.createElement('audio');
            a.setAttribute('playsinline',''); a.setAttribute('preload','auto'); a.volume = 1.0;
            if (SRC) a.src = SRC;
            document.body.appendChild(a);
            window.YAY = a;
          }}
          try {{
            const a = window.YAY; a.muted=false; a.currentTime=0;
            const p = a.play(); if (p && p.then) p.then(()=>{{a.pause(); a.currentTime=0;}}).catch(()=>{{}});
          }} catch(e){{}}
        }})();
        </script>
        """, height=0)
        st.rerun()

# ================== BOTÕES ==================
col1, col2 = st.columns(2, gap="small")
clicked = col1.button("➕  um copinho", use_container_width=True, key="add")
undo    = col2.button("↩️  Desfazer",   use_container_width=True, key="undo")

# aplicar classes fofas via JS
st.markdown("""
<script>
const btns = Array.from(parent.document.querySelectorAll('button'));
btns.forEach(b=>{
  if(b.innerText.includes('um copinho')) b.classList.add('btn-primary');
  if(b.innerText.includes('Desfazer'))   b.classList.add('btn-sec');
});
</script>
""", unsafe_allow_html=True)

# ---- Overlay que toca o som IMEDIATAMENTE e clica o botão real (iPhone) ----
st.components.v1.html(f"""
<style>
#yay-overlay {{
  position: fixed; left: 0; top: 0; width: 0; height: 0;
  pointer-events: none; z-index: 9; background: transparent;
}}
</style>
<div id="yay-overlay"></div>
<script>
(function(){{
  const root = document.getElementById('yay-overlay');

  function placeOverlay() {{
    // acha o botão real
    const btns = Array.from(parent.document.querySelectorAll('button'));
    const target = btns.find(b => /um copinho/i.test(b.innerText));
    if (!target) {{ root.style.pointerEvents='none'; return; }}
    const r = target.getBoundingClientRect();
    // posiciona exatamente por cima
    root.style.left   = r.left + 'px';
    root.style.top    = r.top  + 'px';
    root.style.width  = r.width + 'px';
    root.style.height = r.height + 'px';
    root.style.pointerEvents = 'auto';
  }}

  function playYay() {{
    try {{
      if (window.YAY) {{
        window.YAY.currentTime = 0;
        const p = window.YAY.play();
        if (p && p.catch) p.catch(()=>{{}});
      }}
    }} catch(e) {{}}
  }}

  root.onclick = function(ev){{
    ev.preventDefault();
    playYay();
    // clica o botão real
    const btns = Array.from(parent.document.querySelectorAll('button'));
    const target = btns.find(b => /um copinho/i.test(b.innerText));
    target && target.click();
  }};

  // reposiciona quando necessário
  placeOverlay();
  window.addEventListener('resize', placeOverlay);
  window.addEventListener('scroll', placeOverlay, true);
  setInterval(placeOverlay, 700); // garante ajuste após re-render do Streamlit
}})();
</script>
""", height=0)

# ================== LÓGICA CLIQUES ==================
if clicked:
    if images and st.session_state.pool_indices:
        idx = st.session_state.pool_indices.pop(0)
        st.session_state.shown_indices.append(idx)
        st.session_state.do_effect = True
        st.session_state.fx_nonce += 1  # não usamos mais pro som, mas mantém se quiser
        save_state(
            st.session_state.shown_indices,
            st.session_state.pool_indices,
            st.session_state.goal_ml,
            st.session_state.cup_ml,
        )
        if len(st.session_state.shown_indices) * st.session_state.cup_ml >= st.session_state.goal_ml:
            st.balloons()
    st.rerun()

if undo:
    if st.session_state.shown_indices:
        st.session_state.shown_indices.pop()
        used = set(st.session_state.shown_indices)
        st.session_state.pool_indices = [i for i in range(len(images)) if i not in used]
        random.shuffle(st.session_state.pool_indices)
        save_state(
            st.session_state.shown_indices,
            st.session_state.pool_indices,
            st.session_state.goal_ml,
            st.session_state.cup_ml,
        )
    st.rerun()

# ================== PROGRESSO + MENSAGEM ==================
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

def incentivo(p):
    if p == 0:   return "Começa com um golinho? 🥺👉👈"
    if p < 20:   return "Primeiro passo dado! 💖"
    if p < 40:   return "Good girl! Segue no foco ✨"
    if p < 60:   return "Metade do copão chegando! Orgulho 🥹"
    if p < 80:   return "Quase lá! Só mais uns golinhos 😘"
    if p < 100:  return "Reta final, você consegue! 🏁💪"
    return "META BATIDA! Princesinha hidratadaaa! 🥳💦"

st.markdown(f"<div class='msg'>{incentivo(pct)}</div>", unsafe_allow_html=True)

# ================== GRID DE STICKERS (permanecem) ==================
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

# ================== EFEITO YAAAY (VISUAL) ==================
# (o som já toca via overlay antes do clique real)
if st.session_state.get("do_effect"):
    st.session_state.do_effect = False
    burst = "".join(
        f"<span style='--x:{random.randint(-160,160)}px; --y:{random.randint(-140,140)}px'>"
        f"{random.choice(['✨','💧','🌟','🫧','💖','🎉'])}</span>"
        for _ in range(24)
    )
    st.markdown(f"<div class='flash'></div><div class='burst'>{burst}</div>", unsafe_allow_html=True)

# ================== SIDEBAR (só configs úteis) ==================
with st.sidebar:
    st.header("⚙️ Configurações")
    new_goal = st.number_input("Meta diária (ml)", 200, 10000, st.session_state.goal_ml, 100)
    new_cup  = st.number_input("Tamanho do copo (ml)", 50, 1000, st.session_state.cup_ml, 50)
    if new_goal != st.session_state.goal_ml or new_cup != st.session_state.cup_ml:
        st.session_state.goal_ml = new_goal
        st.session_state.cup_ml  = new_cup
        save_state(st.session_state.shown_indices, st.session_state.pool_indices, new_goal, new_cup)
    st.caption("As imagens de hoje ficam fixas. Amanhã sorteia outra ordem automaticamente. 💕")
    if st.button("🔄 Resetar dia (manual)"):
        st.session_state.shown_indices = []
        st.session_state.pool_indices  = list(range(len(images)))
        random.shuffle(st.session_state.pool_indices)
        save_state(st.session_state.shown_indices, st.session_state.pool_indices, st.session_state.goal_ml, st.session_state.cup_ml)
        st.rerun()
