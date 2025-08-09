import streamlit as st
from datetime import date
from pathlib import Path
from PIL import Image
import random

st.set_page_config(page_title="Beba Água 🌸", page_icon="💧", layout="centered")

# --- CSS fofinho ---
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #ffbfd9, #ffd1b3);
    color: #5c2a42;
    font-family: 'Comic Sans MS', cursive, sans-serif;
}
.cups {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
    margin-top: 10px;
}
.cup {
    font-size: 40px;
    text-align: center;
}
.small {
    font-size: 20px;
    text-align: center;
    margin-top: 10px;
}
.star {
    position: fixed;
    width: 4px;
    height: 4px;
    background: white;
    border-radius: 50%;
    animation: twinkle 3s infinite;
}
@keyframes twinkle {
    0%, 100% { opacity: 0; }
    50% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# --- Gera estrelinhas animadas ---
for _ in range(15):
    st.markdown(f"<div class='star' style='top:{random.randint(0,100)}%; left:{random.randint(0,100)}%;'></div>", unsafe_allow_html=True)

# --- Carrega imagens fofinhas ---
@st.cache_resource
def carregar_stickers_pixel(pasta: str = "pixel"):
    base = Path(pasta)
    if not base.exists():
        return []
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    arquivos = [p for p in base.iterdir() if p.suffix.lower() in exts]
    imgs = []
    for p in arquivos:
        try:
            imgs.append(Image.open(p).convert("RGBA"))
        except Exception:
            pass
    return imgs

stickers_pixel = carregar_stickers_pixel("pixel")

# --- Estado ---
if "counts" not in st.session_state:
    st.session_state.counts = {}
if "pixel_idx" not in st.session_state:
    st.session_state.pixel_idx = 0
if "pixel_shuffle" not in st.session_state:
    st.session_state.pixel_shuffle = list(range(len(stickers_pixel)))
    random.shuffle(st.session_state.pixel_shuffle)

today = str(date.today())

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configurações")
    goal = st.number_input("Meta diária (ml)", min_value=500, max_value=10000, step=100, value=3500)
    cup_ml = st.number_input("Tamanho do copo (ml)", min_value=50, max_value=1000, step=50, value=350)
    modo = st.radio("Como exibir copinhos?",
                    ["Aleatório a cada copinho", "Ciclar na ordem", "Mostrar todos (grade)"], index=0)
    if modo == "Aleatório a cada copinho" and st.button("🔀 Reembaralhar"):
        st.session_state.pixel_shuffle = list(range(len(stickers_pixel)))
        random.shuffle(st.session_state.pixel_shuffle)
        st.session_state.pixel_idx = 0
    if st.button("🔄 Resetar dia"):
        st.session_state.counts[today] = 0

# --- Funções ---
def pegar_imagem_por_indice(i: int):
    if not stickers_pixel:
        return None
    if modo == "Ciclar na ordem":
        return stickers_pixel[i % len(stickers_pixel)]
    elif modo == "Aleatório a cada copinho":
        if st.session_state.pixel_idx >= len(stickers_pixel):
            st.session_state.pixel_shuffle = list(range(len(stickers_pixel)))
            random.shuffle(st.session_state.pixel_shuffle)
            st.session_state.pixel_idx = 0
        idx = st.session_state.pixel_shuffle[st.session_state.pixel_idx]
        st.session_state.pixel_idx += 1
        return stickers_pixel[idx]
    return None

# --- Título ---
st.title("💖 Beba Água 💖")
st.markdown("<div class='small'>Começa com um golinho? 🥺👉👈</div>", unsafe_allow_html=True)

# --- Contador ---
if today not in st.session_state.counts:
    st.session_state.counts[today] = 0

if st.button(f"+ {cup_ml} ml 💧"):
    st.session_state.counts[today] += 1
    if modo == "Aleatório a cada copinho":
        pegar_imagem_por_indice(st.session_state.counts[today])

total_ml = st.session_state.counts[today] * cup_ml
st.progress(min(total_ml / goal, 1.0))
st.write(f"Você bebeu **{total_ml} ml** de **{goal} ml** hoje!")

# --- Render copos ---
emoji_pack = ["🥤","🧃","🫖","🍹","🧋","🍑","💖","🌸","⭐","🫧"]
st.markdown("<div class='cups'>", unsafe_allow_html=True)

if st.session_state.counts[today] > 0:
    if modo == "Mostrar todos (grade)" and stickers_pixel:
        cols = st.columns(4)
        for i, img in enumerate(stickers_pixel):
            with cols[i % 4]:
                st.image(img, use_container_width=True)
    else:
        cols = st.columns(4)
        for i in range(st.session_state.counts[today]):
            img = pegar_imagem_por_indice(i)
            with cols[i % 4]:
                if img is not None:
                    st.image(img, use_container_width=True)
                else:
                    st.markdown(f"<div class='cup'>{random.choice(emoji_pack)}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
