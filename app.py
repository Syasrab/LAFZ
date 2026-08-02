import os
import json
import streamlit as st
import google.generativeai as genai
from PIL import Image

PREFS_FILE = "preferences.json"

api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3.6-flash")

st.set_page_config(page_title="Lafz 🌸", page_icon="🌸", layout="centered")

# ---------- Aesthetic styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400;1,600&family=Poppins:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 8% 12%, rgba(232,168,148,0.15) 0%, transparent 35%),
        radial-gradient(circle at 92% 88%, rgba(232,168,148,0.15) 0%, transparent 35%),
        radial-gradient(circle at 85% 15%, rgba(243,201,181,0.18) 0%, transparent 30%),
        linear-gradient(180deg, #fdf6f0 0%, #fbeee6 60%, #f8e5da 100%);
}

/* Hide default streamlit chrome for a cleaner feel */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.top-ornament {
    text-align: center;
    color: #e8a894;
    font-size: 1.3rem;
    letter-spacing: 12px;
    margin-bottom: -10px;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-weight: 600;
    font-size: 3.2rem;
    color: #8a5a45;
    text-align: center;
    margin-bottom: 0;
    letter-spacing: 1px;
}

.hero-sub {
    text-align: center;
    color: #a37c68;
    font-size: 1rem;
    margin-top: 0.3rem;
    margin-bottom: 0.3rem;
    letter-spacing: 1px;
    font-style: italic;
}

.hero-tagline {
    text-align: center;
    color: #c49682;
    font-size: 0.8rem;
    margin-bottom: 1.8rem;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.divider {
    text-align: center;
    color: #e8a894;
    font-size: 1.1rem;
    margin: 1.2rem 0;
    letter-spacing: 8px;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #6b4a3a !important;
}

h5, h6 {
    color: #8a5a45 !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    justify-content: center;
}

.stTabs [data-baseweb="tab"] {
    background-color: #fff3ec;
    border-radius: 14px 14px 0 0;
    padding: 12px 22px;
    color: #8a5a45;
    font-weight: 500;
    border: 1px solid #f3d9cb;
    border-bottom: none;
}

.stTabs [aria-selected="true"] {
    background-color: #f3c9b5 !important;
    color: #5a3826 !important;
}

.stButton>button {
    background: linear-gradient(135deg, #e8a894, #d68f78);
    color: white;
    border-radius: 24px;
    border: none;
    padding: 0.6rem 1.8rem;
    font-family: 'Poppins', sans-serif;
    font-weight: 500;
    letter-spacing: 0.5px;
    box-shadow: 0 3px 10px rgba(214, 143, 120, 0.35);
    transition: 0.25s;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #d68f78, #c47a62);
    box-shadow: 0 4px 14px rgba(196, 122, 98, 0.45);
    transform: translateY(-1px);
}

.result-card {
    background-color: #fffaf6;
    border: 1px solid #f0d9cc;
    border-radius: 20px;
    padding: 1.8rem;
    margin-top: 1.2rem;
    box-shadow: 0 4px 20px rgba(180, 120, 100, 0.1);
    position: relative;
}

.result-card::before {
    content: "🌸";
    position: absolute;
    top: -14px;
    left: 20px;
    background: #fdf6f0;
    padding: 0 8px;
    font-size: 1.1rem;
}

.note-card {
    background-color: #fffaf6;
    border-left: 4px solid #e8a894;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.7rem;
    color: #5a3826;
    box-shadow: 0 2px 8px rgba(180, 120, 100, 0.06);
}

.quote-box {
    text-align: center;
    font-family: 'Playfair Display', serif;
    font-style: italic;
    color: #a37c68;
    font-size: 0.95rem;
    padding: 1rem 2rem;
    margin: 0.5rem 0 1.5rem 0;
    border-top: 1px solid #f0d9cc;
    border-bottom: 1px solid #f0d9cc;
}

textarea, .stTextArea textarea {
    border-radius: 14px !important;
    border: 1px solid #f0d9cc !important;
    background-color: #fffaf6 !important;
}

[data-testid="stFileUploaderDropzone"] {
    border-radius: 18px;
    border: 2px dashed #e8a894 !important;
    background-color: #fffaf6;
}

.section-label {
    color: #c49682;
    font-size: 0.75rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

.app-footer {
    text-align: center;
    color: #c49682;
    font-size: 0.8rem;
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid #f0d9cc;
    font-style: italic;
    letter-spacing: 0.5px;
}
</style>
""", unsafe_allow_html=True)

def load_prefs():
    if os.path.exists(PREFS_FILE):
        with open(PREFS_FILE, "r") as f:
            return json.load(f)
    return {"style_notes": []}

def save_prefs(prefs):
    with open(PREFS_FILE, "w") as f:
        json.dump(prefs, f, indent=2)

def generate(prefs, image=None, text_context=""):
    style_context = "\n".join(prefs["style_notes"]) if prefs["style_notes"] else "No style preferences learned yet."

    prompt = f"""Here are the user's learned style preferences from past posts:
{style_context}

Additional context from user: {text_context}

Based on the image (if provided) and their style preferences, give:
1. Three Instagram caption options matching their usual tone/words
2. Two real song suggestions (title and artist) that fit the vibe and their past song preferences

Be specific and match their style, do not be generic."""

    if image:
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content(prompt)

    return response.text

if "prefs" not in st.session_state:
    st.session_state.prefs = load_prefs()

# ---------- Header ----------
st.markdown('<p class="top-ornament">❀ ❀ ❀</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-title">Lafz</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">لفظ ۔ words for your moments</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-tagline">captions · songs · sukoon k lamhat</p>', unsafe_allow_html=True)

st.markdown('<div class="quote-box">"kuch lamhat jo theher gaye, kuch lafz jo unhe zinda rakhein"</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🌷 Generate", "🖋️ Teach Style", "📖 My Style Profile"])

with tab1:
    st.markdown('<p class="section-label">upload your moment</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Drop your photo here", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")

    st.markdown('<p class="section-label">a little more context (optional)</p>', unsafe_allow_html=True)
    extra_context = st.text_area("context", placeholder="e.g. this is with my best friend at a beach, golden hour, feeling grateful", label_visibility="collapsed")

    if uploaded_file:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    center = st.columns([1, 2, 1])
    with center[1]:
        generate_clicked = st.button("✨ Generate Captions & Songs", use_container_width=True)

    if generate_clicked:
        with st.spinner("finding the right words for you..."):
            img = Image.open(uploaded_file) if uploaded_file else None
            result = generate(st.session_state.prefs, image=img, text_context=extra_context)
        st.markdown(f'<div class="result-card">{result}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<p class="section-label">teach lafz how you write</p>', unsafe_allow_html=True)
    new_note = st.text_area("note", placeholder="e.g. for friendship pics I write Urdu captions like 'sukoon k lamhat', songs like Osho Jain", label_visibility="collapsed", height=120)
    center = st.columns([1, 2, 1])
    with center[1]:
        save_clicked = st.button("💌 Save this preference", use_container_width=True)
    if save_clicked:
        if new_note.strip():
            st.session_state.prefs["style_notes"].append(new_note.strip())
            save_prefs(st.session_state.prefs)
            st.success("saved to your style profile 🌸")
        else:
            st.warning("write something first")

with tab3:
    st.markdown('<p class="section-label">your saved style notes</p>', unsafe_allow_html=True)
    if st.session_state.prefs["style_notes"]:
        for i, note in enumerate(st.session_state.prefs["style_notes"]):
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f'<div class="note-card">{note}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("✕", key=f"del_{i}"):
                    st.session_state.prefs["style_notes"].pop(i)
                    save_prefs(st.session_state.prefs)
                    st.rerun()
    else:
        st.info("no style notes yet, add some in the Teach Style tab 🌷")

st.markdown('<div class="app-footer">made with 🤍 for words that stay</div>', unsafe_allow_html=True)